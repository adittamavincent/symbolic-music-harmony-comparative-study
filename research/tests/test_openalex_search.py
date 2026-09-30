"""Check OpenAlex search pagination and reproducibility artifacts without network access."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from research.scripts import openalex_search


class OpenAlexSearchTests(unittest.TestCase):
    def test_tracked_query_plan_is_valid(self):
        queries = openalex_search.load_queries(openalex_search.DEFAULT_QUERIES)
        self.assertGreaterEqual(len(queries), 8)
        self.assertEqual(len({item["id"] for item in queries}), len(queries))

    def test_duplicate_query_ids_are_rejected_before_api_use(self):
        query = {
            "id": "duplicate", "theme": "theme", "purpose": "purpose",
            "search": "chorale", "from_year": None, "limit": 2,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queries.json"
            path.write_text(json.dumps({"version": 1, "queries": [query, query]}), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Duplicate query id"):
                openalex_search.load_queries(path)

    def test_request_is_encoded_and_has_no_api_key(self):
        url = openalex_search.request_url("chorale & voice leading", 1, 25, 2020)
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["search"], ["chorale & voice leading"])
        self.assertEqual(params["filter"], ["from_publication_date:2020-01-01"])
        self.assertNotIn("api_key", params)

    def test_pagination_saves_unique_rows_and_provenance(self):
        seen_urls = []

        def fake_fetch(url, key):
            self.assertEqual(key, "secret-for-test")
            seen_urls.append(url)
            params = parse_qs(urlparse(url).query)
            self.assertEqual(params["per_page"], ["100"])
            page = int(params["page"][0])
            start = (page - 1) * 100
            count = 100 if page == 1 else 25
            return {
                "meta": {"count": 125},
                "results": [
                    {"id": f"https://openalex.org/W{index}", "display_name": f"Work {index}"}
                    for index in range(start, start + count)
                ],
            }

        with tempfile.TemporaryDirectory() as directory:
            with patch.object(openalex_search, "api_key", return_value="secret-for-test"), \
                 patch.object(openalex_search, "fetch", side_effect=fake_fetch), \
                 patch.object(sys, "argv", [
                     "openalex_search.py", "--query", "chorale generation",
                     "--limit", "125", "--output-dir", directory,
                 ]):
                self.assertEqual(openalex_search.main(), 0)

            self.assertEqual(len(seen_urls), 2)
            csv_path = next(Path(directory).glob("*.csv"))
            with csv_path.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 125)
            self.assertEqual(len({row["openalex_id"] for row in rows}), 125)
            self.assertEqual(rows[-1]["title"], "Work 124")

            manifest_path = next(Path(directory).glob("*.manifest.json"))
            manifest_text = manifest_path.read_text(encoding="utf-8")
            manifest = json.loads(manifest_text)
            self.assertEqual(manifest["saved_count"], 125)
            self.assertEqual(manifest["reported_result_count"], 125)
            self.assertEqual(manifest["request_urls"], seen_urls)
            self.assertNotIn("secret-for-test", manifest_text)

    def test_batch_deduplicates_works_and_records_query_origins(self):
        queries = [
            {"id": "q01", "theme": "first", "purpose": "first topic", "search": "chorale",
             "from_year": None, "limit": 2},
            {"id": "q02", "theme": "second", "purpose": "second topic", "search": "voice leading",
             "from_year": 2020, "limit": 2},
        ]

        def fake_fetch(url, key):
            self.assertEqual(key, "secret-for-test")
            search = parse_qs(urlparse(url).query)["search"][0]
            ids = ("W1", "W2") if search == "chorale" else ("W2", "W3")
            return {
                "meta": {"count": 2},
                "results": [
                    {"id": f"https://openalex.org/{identifier}", "display_name": identifier}
                    for identifier in ids
                ],
            }

        with tempfile.TemporaryDirectory() as directory:
            query_file = Path(directory) / "queries.json"
            query_file.write_text(json.dumps({"version": 1, "queries": queries}), encoding="utf-8")
            output_dir = Path(directory) / "out"
            with patch.object(openalex_search, "fetch", side_effect=fake_fetch):
                self.assertEqual(
                    openalex_search.run_batch(queries, query_file, output_dir, "secret-for-test"), 0
                )
            run_dir = next(output_dir.iterdir())
            self.assertEqual((run_dir / "queries.snapshot.json").read_bytes(), query_file.read_bytes())
            with (run_dir / "combined.csv").open(encoding="utf-8", newline="") as stream:
                rows = {row["title"]: row for row in csv.DictReader(stream)}
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows["W2"]["query_ids"], "q01; q02")
            summary = json.loads((run_dir / "batch_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["unique_works"], 3)
            self.assertEqual([item["status"] for item in summary["queries"]], ["complete", "complete"])
            self.assertNotIn("secret-for-test", json.dumps(summary))

    def test_batch_records_failed_query_without_losing_successful_results(self):
        queries = [
            {"id": "q01", "theme": "first", "purpose": "first", "search": "chorale",
             "from_year": None, "limit": 1},
            {"id": "q02", "theme": "second", "purpose": "second", "search": "voice leading",
             "from_year": None, "limit": 1},
        ]

        def fake_fetch(url, _key):
            if parse_qs(urlparse(url).query)["search"] == ["voice leading"]:
                raise RuntimeError("simulated API failure")
            return {"meta": {"count": 1}, "results": [
                {"id": "https://openalex.org/W1", "display_name": "Work 1"}
            ]}

        with tempfile.TemporaryDirectory() as directory:
            query_file = Path(directory) / "queries.json"
            query_file.write_text(json.dumps({"version": 1, "queries": queries}), encoding="utf-8")
            output_dir = Path(directory) / "out"
            with patch.object(openalex_search, "fetch", side_effect=fake_fetch):
                self.assertEqual(openalex_search.run_batch(queries, query_file, output_dir, None), 1)
            run_dir = next(output_dir.iterdir())
            summary = json.loads((run_dir / "batch_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual([item["status"] for item in summary["queries"]], ["complete", "failed"])
            self.assertEqual(summary["unique_works"], 1)


if __name__ == "__main__":
    unittest.main()
