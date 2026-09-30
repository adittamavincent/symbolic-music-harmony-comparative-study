"""Save a bounded OpenAlex literature search with its reproducibility metadata."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.openalex.org/works"
DEFAULT_QUERIES = ROOT / "research/literature/openalex_queries.json"
FIELDS = (
    "id,display_name,publication_year,doi,authorships,cited_by_count,"
    "type,primary_location,open_access,is_retracted"
)
CSV_FIELDS = (
    "openalex_id", "title", "year", "doi", "authors", "cited_by_count",
    "type", "venue", "landing_page", "is_oa", "is_retracted",
)


def api_key() -> str | None:
    if os.environ.get("OPENALEX_API_KEY", "").strip():
        return os.environ["OPENALEX_API_KEY"].strip()
    local_env = ROOT / ".env.local"
    if local_env.exists():
        for line in local_env.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"\s*OPENALEX_API_KEY\s*=\s*(.*?)\s*", line)
            if match:
                return match.group(1).strip("\"'") or None
    return None


def request_url(query: str, page: int, page_size: int, from_year: int | None) -> str:
    params = {"search": query, "per_page": page_size, "page": page, "select": FIELDS}
    if from_year is not None:
        params["filter"] = f"from_publication_date:{from_year}-01-01"
    return f"{API_URL}?{urlencode(params)}"


def fetch(url: str, key: str | None) -> dict:
    headers = {"Accept": "application/json", "User-Agent": "symbolic-music-thesis-openalex/1.0"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(f"OpenAlex HTTP {exc.code}; check query or remaining API budget") from exc
        except URLError as exc:
            if attempt == 2:
                raise RuntimeError(f"Could not reach OpenAlex: {exc.reason}") from exc
        time.sleep(2**attempt)
    raise AssertionError("unreachable")


def csv_row(work: dict) -> dict:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    access = work.get("open_access") or {}
    return {
        "openalex_id": work.get("id"),
        "title": work.get("display_name"),
        "year": work.get("publication_year"),
        "doi": work.get("doi"),
        "authors": "; ".join(
            (item.get("author") or {}).get("display_name", "")
            for item in work.get("authorships", [])
        ),
        "cited_by_count": work.get("cited_by_count"),
        "type": work.get("type"),
        "venue": source.get("display_name"),
        "landing_page": location.get("landing_page_url"),
        "is_oa": access.get("is_oa"),
        "is_retracted": work.get("is_retracted"),
    }


def load_queries(path: Path) -> list[dict]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read query file {path}: {exc}") from exc
    if not isinstance(document, dict) or document.get("version") != 1:
        raise RuntimeError("Query file must be an object with version 1")
    queries = document.get("queries")
    if not isinstance(queries, list) or not queries:
        raise RuntimeError("Query file must contain a nonempty queries list")
    seen = set()
    for index, item in enumerate(queries, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"Query {index} must be an object")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9-]+", identifier):
            raise RuntimeError(f"Query {index} needs a lowercase hyphenated id")
        if identifier in seen:
            raise RuntimeError(f"Duplicate query id: {identifier}")
        seen.add(identifier)
        for field in ("theme", "purpose", "search"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise RuntimeError(f"Query {identifier} needs nonempty {field}")
        limit = item.get("limit")
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise RuntimeError(f"Query {identifier} limit must be 1–1000")
        year = item.get("from_year")
        if year is not None and (type(year) is not int or not 1000 <= year <= datetime.now().year):
            raise RuntimeError(f"Query {identifier} from_year is invalid")
    return queries


def search_works(query: str, limit: int, from_year: int | None, key: str | None):
    page_size = min(100, limit)
    works = []
    urls = []
    count = None
    page = 1
    while len(works) < limit:
        url = request_url(query, page, page_size, from_year)
        response = fetch(url, key)
        results = response.get("results")
        if not isinstance(results, list):
            raise RuntimeError("OpenAlex response has no results list")
        urls.append(url)
        if count is None:
            count = response.get("meta", {}).get("count")
        works.extend(results[: limit - len(works)])
        if not results or (isinstance(count, int) and len(works) >= count):
            break
        page += 1
    return works, urls, count


def save_search(item: dict, output_dir: Path, key: str | None, stem_name: str | None = None):
    query, limit, from_year = item["search"].strip(), item["limit"], item["from_year"]
    works, urls, count = search_works(query, limit, from_year, key)
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")[:50] or "search"
    stem = output_dir / (stem_name or f"{stamp}-{slug}")
    with stem.with_suffix(".jsonl").open("w", encoding="utf-8") as output:
        for work in works:
            output.write(json.dumps(work, ensure_ascii=False) + "\n")
    with stem.with_suffix(".csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(csv_row(work) for work in works)
    manifest = {
        "retrieved_at_utc": stamp,
        "provider": "OpenAlex",
        "query_id": item.get("id"),
        "theme": item.get("theme"),
        "purpose": item.get("purpose"),
        "query": query,
        "from_year": from_year,
        "requested_limit": limit,
        "reported_result_count": count,
        "saved_count": len(works),
        "request_urls": urls,
        "authenticated": bool(key),
        "note": "Discovery metadata only; verify bibliographic details and claim support in primary sources.",
    }
    stem.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Saved {len(works)} works (OpenAlex reported {count} matches): {stem}")
    return works, manifest


def run_batch(queries: list[dict], query_file: Path, output_dir: Path, key: str | None) -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_dir = output_dir / f"{stamp}-batch"
    run_dir.mkdir(parents=True, exist_ok=False)
    snapshot = run_dir / "queries.snapshot.json"
    shutil.copyfile(query_file, snapshot)
    summary = {
        "retrieved_at_utc": stamp,
        "query_file": str(query_file),
        "query_file_sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        "authenticated": bool(key),
        "queries": [],
    }
    combined = {}
    for item in queries:
        identifier = item["id"]
        try:
            works, manifest = save_search(item, run_dir, key, identifier)
        except RuntimeError as exc:
            summary["queries"].append({"id": identifier, "status": "failed", "error": str(exc)})
            print(f"{identifier}: {exc}", file=sys.stderr)
            continue
        summary["queries"].append({
            "id": identifier, "status": "complete", "saved_count": manifest["saved_count"],
            "reported_result_count": manifest["reported_result_count"],
            "request_urls": manifest["request_urls"],
        })
        for work in works:
            work_id = work.get("id")
            if not work_id:
                continue
            if work_id not in combined:
                combined[work_id] = {**csv_row(work), "query_ids": []}
            combined[work_id]["query_ids"].append(identifier)
    with (run_dir / "combined.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=(*CSV_FIELDS, "query_ids"))
        writer.writeheader()
        for row in combined.values():
            writer.writerow({**row, "query_ids": "; ".join(row["query_ids"])})
    summary["unique_works"] = len(combined)
    (run_dir / "batch_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Batch: {len(combined)} unique works in {run_dir / 'combined.csv'}")
    return int(any(item["status"] == "failed" for item in summary["queries"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--query", help="One keyword query sent to OpenAlex search")
    mode.add_argument("--batch", action="store_true", help="Run every query in the tracked JSON file")
    parser.add_argument("--query-file", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--limit", type=int, help="Maximum single-query records, 1–1000 (default: 25)")
    parser.add_argument("--from-year", type=int, help="Earliest single-query publication year")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "research/outputs/openalex")
    parser.add_argument("--dry-run", action="store_true", help="Show planned requests without API use")
    args = parser.parse_args()
    if args.batch:
        if args.limit is not None or args.from_year is not None:
            parser.error("--limit and --from-year belong in the JSON file for batch runs")
        queries = load_queries(args.query_file)
    else:
        query = args.query.strip()
        if not query:
            parser.error("--query must contain text")
        limit = args.limit if args.limit is not None else 25
        if not 1 <= limit <= 1000:
            parser.error("--limit must be between 1 and 1000")
        if args.from_year is not None and not 1000 <= args.from_year <= datetime.now().year:
            parser.error("--from-year must be between 1000 and the current year")
        queries = [{"search": query, "limit": limit, "from_year": args.from_year}]

    key = api_key()
    if args.dry_run:
        print(f"API key: {'configured' if key else 'absent; keyless budget applies'}")
        for item in queries:
            url = request_url(item["search"], 1, min(100, item["limit"]), item["from_year"])
            print(f"{item.get('id', 'single')}: {url}")
        return 0
    if args.batch:
        return run_batch(queries, args.query_file, args.output_dir, key)
    save_search(queries[0], args.output_dir, key)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
