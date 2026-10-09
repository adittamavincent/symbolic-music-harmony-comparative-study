"""Analysis of a protocol-version-2 run (BAB III, Metode Analisis Data).

Reads <run>/evaluation/ and writes <run>/analysis/:

    descriptive.csv        n, median, IQR, mean, SD of each rate per model x origin (and Bach reference)
    attempts_summary.csv   attempts, ok, QC passes, and failures by reason per model x origin
    melody_features.csv    features of the two melody groups, including Huang et al.'s limits
    copy_share.csv         how often each model sounds Bach's own alto, tenor, and bass pitch on Bach melodies
    bach_difference.csv    model minus Bach on the same Bach melodies
    q2_wilcoxon.csv        question 2: DeepBach vs Coconet, paired by melody, Holm over five rules
    q3_zone.csv            question 3 (protocol 3.0): fermata zone vs inside the phrase per model, paired by
                           melody, Holm within model
    zone_pattern.csv       pooled zone rates and shares for each model and for Bach's own harmonizations
    q3_mannwhitney.csv     question 3 of protocol 2.1 only: Strube vs Bach melodies within each model
    sensitivity_*.csv      the same tests on the fermata and merged variants and on complete melodies
    seen_unseen.csv        DeepBach seen vs unseen Bach melodies, only when a verified membership file exists
    power.csv              minimum detectable effect for the analysed group sizes
    summary.json           everything above in one file, with software versions
    tables/*.tex           LaTeX tables in Indonesian for BAB IV

A test with no usable data (for example every paired difference zero) is
reported with its reason instead of a p-value. Rates come from the per-melody
means; repeated generations are never treated as independent observations.
Which question-3 test runs follows the protocol: `zone_test` (3.0) or
`q3_test` with Strube melodies in the run (2.1).
"""

import csv
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

RULES = ("parallel_fifths", "parallel_octaves", "spacing", "crossing", "overlap")
RULE_LABELS = {
    "parallel_fifths": "Kuint sejajar",
    "parallel_octaves": "Oktaf sejajar",
    "spacing": "Jarak suara atas",
    "crossing": "Persilangan di atas sopran",
    "overlap": "Tumpang tindih",
    "weighted": "Indeks tertimbang",
}
MODEL_LABELS = {"deepbach": "DeepBach", "coconet": "Coconet", "bach": "Bach (acuan)", "fake": "Fake"}
ORIGIN_LABELS = {"bach": "Chorale Bach", "strube": "Latihan Strube"}
ARE_RANK_TESTS = 0.864  # Hodges and Lehmann (1956)


def read_csv(path):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def number(value):
    return float(value) if value not in ("", None) else None


def describe(values):
    values = np.array([v for v in values if v is not None], dtype=float)
    if len(values) == 0:
        return {"n": 0, "median": "", "q1": "", "q3": "", "iqr": "", "mean": "", "sd": "", "share_zero": ""}
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    return {"n": len(values), "median": median, "q1": q1, "q3": q3, "iqr": q3 - q1, "mean": values.mean(),
            "sd": values.std(ddof=1) if len(values) > 1 else "", "share_zero": float(np.mean(values == 0))}


def holm(p_values):
    """Holm step-down adjusted p-values; None entries stay None and are not counted."""
    indexed = sorted((p, i) for i, p in enumerate(p_values) if p is not None)
    m = len(indexed)
    adjusted = [None] * len(p_values)
    running = 0.0
    for rank, (p, i) in enumerate(indexed):
        running = max(running, min(1.0, (m - rank) * p))
        adjusted[i] = running
    return adjusted


def wilcoxon_paired(x, y):
    """Two-sided Wilcoxon signed-rank on x - y with the matched-pairs rank-biserial correlation."""
    diff = np.array(x, dtype=float) - np.array(y, dtype=float)
    nonzero = diff[diff != 0]
    result = {"n_pairs": len(diff), "n_nonzero": len(nonzero), "median_difference": float(np.median(diff)) if len(diff) else ""}
    if len(nonzero) == 0:
        return {**result, "statistic": "", "p_value": None, "effect_size": "", "note": "all paired differences are zero"}
    ranks = stats.rankdata(np.abs(nonzero))
    w_plus, w_minus = ranks[nonzero > 0].sum(), ranks[nonzero < 0].sum()
    test = stats.wilcoxon(diff, zero_method="wilcox", alternative="two-sided", method="auto")
    return {**result, "statistic": float(test.statistic), "p_value": float(test.pvalue),
            "effect_size": float((w_plus - w_minus) / (w_plus + w_minus)), "note": ""}


def mann_whitney(x, y, alternative):
    """Mann-Whitney U of x (Strube) against y (Bach) with the rank-biserial correlation (positive: x higher)."""
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    result = {"n_strube": len(x), "n_bach": len(y), "median_strube": float(np.median(x)) if len(x) else "",
              "median_bach": float(np.median(y)) if len(y) else ""}
    if len(x) == 0 or len(y) == 0:
        return {**result, "statistic": "", "p_value": None, "p_two_sided": None, "effect_size": "",
                "note": "a group is empty"}
    if np.all(np.concatenate([x, y]) == np.concatenate([x, y])[0]):
        return {**result, "statistic": "", "p_value": None, "p_two_sided": None, "effect_size": 0.0,
                "note": "all values are identical"}
    test = stats.mannwhitneyu(x, y, alternative=alternative, method="auto")
    two = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
    u_x = stats.mannwhitneyu(x, y, alternative="greater", method="auto").statistic
    return {**result, "statistic": float(test.statistic), "p_value": float(test.pvalue),
            "p_two_sided": float(two.pvalue), "effect_size": float(2 * u_x / (len(x) * len(y)) - 1), "note": ""}


def minimum_detectable_d(n1, n2=None, alpha=0.05, power=0.8, paired=False, are=ARE_RANK_TESTS):
    """Smallest standardized effect a t-test detects at the given power, inflated by 1/ARE for rank tests.

    Two-sided. For paired data n1 is the number of pairs and the effect is d_z.
    """
    if (paired and n1 < 3) or (not paired and (n1 < 2 or n2 < 2)):
        return None
    n_eff1 = n1 * are
    n_eff2 = None if paired else n2 * are

    def achieved(d):
        if paired:
            df, nc = n_eff1 - 1, d * math.sqrt(n_eff1)
        else:
            df, nc = n_eff1 + n_eff2 - 2, d * math.sqrt(n_eff1 * n_eff2 / (n_eff1 + n_eff2))
        critical = stats.t.ppf(1 - alpha / 2, df)
        return 1 - stats.nct.cdf(critical, df, nc) + stats.nct.cdf(-critical, df, nc)

    low, high = 0.0, 10.0
    for _ in range(60):
        middle = (low + high) / 2
        if achieved(middle) < power:
            low = middle
        else:
            high = middle
    return high


def rate(row, variant, rule):
    column = f"{variant}_weighted_rate" if rule == "weighted" else f"{variant}_{rule}_rate"
    return number(row.get(column))


def q2_tests(per_melody, variant, rules, subset=None):
    by = {}
    for row in per_melody:
        if row["model"] in ("deepbach", "coconet") and (subset is None or row["melody_id"] in subset):
            by.setdefault(row["melody_id"], {})[row["model"]] = row
    rows = []
    for rule in rules:
        x, y = [], []
        for melody_id, models in sorted(by.items()):
            a, b = models.get("deepbach"), models.get("coconet")
            if a and b and rate(a, variant, rule) is not None and rate(b, variant, rule) is not None:
                x.append(rate(a, variant, rule))
                y.append(rate(b, variant, rule))
        rows.append({"variant": variant, "rule": rule, **wilcoxon_paired(x, y)})
    return rows


def zone_rate(row, variant, rule, zone):
    """Flags divided by opportunities in one zone, from counts summed over the melody's valid generations."""
    count = number(row.get(f"{variant}_zone_{rule}_{zone}_count"))
    opportunities = number(row.get(f"{variant}_zone_{rule}_{zone}_opportunities"))
    return count / opportunities if count is not None and opportunities else None


def zone_tests(per_melody, variant, rules, subset=None):
    """Question 3 (protocol 3.0): fermata-zone rate minus inside-phrase rate, paired by melody, per model."""
    rows = []
    for model in ("deepbach", "coconet"):
        for rule in rules:
            fermata, inside = [], []
            for row in per_melody:
                if row["model"] != model or (subset is not None and row["melody_id"] not in subset):
                    continue
                a, b = zone_rate(row, variant, rule, "F"), zone_rate(row, variant, rule, "I")
                if a is not None and b is not None:
                    fermata.append(a)
                    inside.append(b)
            rows.append({"variant": variant, "model": model, "rule": rule, **wilcoxon_paired(fermata, inside)})
    return rows


def zone_pattern(rows, source, variant="main"):
    """Pooled flags, opportunities, rates, and shares per zone for one source (a model or Bach)."""
    result = []
    for rule in RULES:
        totals = {}
        for zone in ("F", "I"):
            totals[zone] = [sum(number(r.get(f"{variant}_zone_{rule}_{zone}_{kind}")) or 0 for r in rows)
                            for kind in ("count", "opportunities")]
        (flags_f, opp_f), (flags_i, opp_i) = totals["F"], totals["I"]
        rate_f = flags_f / opp_f if opp_f else None
        rate_i = flags_i / opp_i if opp_i else None
        result.append({"source": source, "variant": variant, "rule": rule, "flags_F": flags_f, "flags_I": flags_i,
                       "opportunities_F": opp_f, "opportunities_I": opp_i,
                       "flag_share_F": flags_f / (flags_f + flags_i) if flags_f + flags_i else "",
                       "opportunity_share_F": opp_f / (opp_f + opp_i) if opp_f + opp_i else "",
                       "rate_F": "" if rate_f is None else rate_f, "rate_I": "" if rate_i is None else rate_i,
                       "rate_ratio": rate_f / rate_i if rate_f is not None and rate_i else ""})
    return result


def q3_tests(per_melody, variant, rules, one_sided, subset=None):
    rows = []
    for model in ("deepbach", "coconet"):
        for rule in rules:
            strube = [rate(r, variant, rule) for r in per_melody if r["model"] == model and r["origin"] == "strube"
                      and (subset is None or r["melody_id"] in subset)]
            bach = [rate(r, variant, rule) for r in per_melody if r["model"] == model and r["origin"] == "bach"
                    and (subset is None or r["melody_id"] in subset)]
            strube = [v for v in strube if v is not None]
            bach = [v for v in bach if v is not None]
            alternative = "greater" if rule in one_sided else "two-sided"
            rows.append({"variant": variant, "model": model, "rule": rule, "alternative": alternative,
                         **mann_whitney(strube, bach, alternative)})
    return rows


def apply_holm(rows, family_key=None):
    families = {}
    for index, row in enumerate(rows):
        if row["rule"] == "weighted":
            row["p_holm"] = ""
            row["family"] = "secondary (no correction)"
            continue
        key = row.get(family_key) if family_key else "all"
        families.setdefault(key, []).append(index)
    for key, indexes in families.items():
        adjusted = holm([rows[i]["p_value"] for i in indexes])
        for i, value in zip(indexes, adjusted):
            rows[i]["p_holm"] = "" if value is None else value
            rows[i]["family"] = f"{key}"
    for row in rows:
        row["p_value"] = "" if row["p_value"] is None else row["p_value"]
        if "p_two_sided" in row:
            row["p_two_sided"] = "" if row["p_two_sided"] is None else row["p_two_sided"]
    return rows


def fmt(value, digits=3):
    if value in ("", None):
        return "--"
    if isinstance(value, str):
        return value
    if abs(value) < 0.001 and value != 0:
        return "<0{,}001"
    return f"{value:.{digits}f}".replace(".", "{,}")


def latex_table(path, caption, label, header, rows):
    lines = [r"\begin{table}[ht]", r"\centering", r"\small",
             r"\begin{tabular}{" + "|".join(["l"] + ["r"] * (len(header) - 1)) + "}", r"\hline",
             " & ".join(rf"\textbf{{{h}}}" for h in header) + r" \\ \hline"]
    lines += [" & ".join(cells) + r" \\ \hline" for cells in rows]
    lines += [r"\end{tabular}", rf"\caption{{{caption}}}", rf"\label{{{label}}}", r"\end{table}"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def analyze_run(run_dir, protocol=None, membership_file=None):
    run_dir = Path(run_dir)
    info = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    protocol = protocol or info["protocol"]
    settings = protocol["analysis"]
    alpha = settings["alpha"]
    one_sided = set(settings.get("q3_one_sided_rules", []))
    evaluation = run_dir / "evaluation"
    per_melody = read_csv(evaluation / "per_melody.csv")
    reference = read_csv(evaluation / "bach_reference.csv")
    qc = read_csv(evaluation / "qc.csv")
    melodies = read_csv(run_dir / "melodies.csv")
    attempts = [json.loads(line) for line in (run_dir / "attempts.jsonl").read_text(encoding="utf-8").splitlines() if line]
    out = run_dir / "analysis"
    all_rules = list(RULES) + ["weighted"]
    origins = [o for o in ("bach", "strube") if any(m["origin"] == o for m in melodies)]
    run_origin_test = "q3_test" in settings and "strube" in origins
    run_zone_test = "zone_test" in settings

    # Attempts and quality control
    summary_rows = []
    origin_of = {m["melody_id"]: m["origin"] for m in melodies}
    for model in sorted({a["model"] for a in attempts}):
        for origin in origins:
            cell = [a for a in attempts if a["model"] == model and a["origin"] == origin]
            passed = [q for q in qc if q["model"] == model and origin_of.get(q["melody_id"]) == origin and q["passed"] == "1"]
            reasons = {}
            for a in cell:
                if a["status"] != "ok":
                    reasons[a["status"]] = reasons.get(a["status"], 0) + 1
            for q in qc:
                if q["model"] == model and origin_of.get(q["melody_id"]) == origin and q["passed"] == "0":
                    reasons["qc_failed"] = reasons.get("qc_failed", 0) + 1
            summary_rows.append({"model": model, "origin": origin, "attempts": len(cell),
                                 "ok": sum(a["status"] == "ok" for a in cell), "qc_passed": len(passed),
                                 **{f"failed_{k}": v for k, v in sorted(reasons.items())}})
    write_csv(out / "attempts_summary.csv", summary_rows)

    # Descriptive statistics (question 1)
    descriptive = []
    for variant in ("main", "fermata", "merged"):
        for model in sorted({r["model"] for r in per_melody}):
            for origin in origins:
                for rule in all_rules:
                    values = [rate(r, variant, rule) for r in per_melody if r["model"] == model and r["origin"] == origin]
                    descriptive.append({"variant": variant, "model": model, "origin": origin, "rule": rule,
                                        **describe(values)})
        for rule in all_rules:
            values = [rate(r, variant, rule) for r in reference]
            descriptive.append({"variant": variant, "model": "bach", "origin": "bach", "rule": rule, **describe(values)})
    write_csv(out / "descriptive.csv", descriptive)

    # Model minus Bach on the Bach melodies
    ref_by = {r["melody_id"]: r for r in reference}
    differences = []
    for model in ("deepbach", "coconet"):
        for rule in all_rules:
            diffs = [rate(r, "main", rule) - rate(ref_by[r["melody_id"]], "main", rule)
                     for r in per_melody if r["model"] == model and r["origin"] == "bach"
                     and r["melody_id"] in ref_by and rate(r, "main", rule) is not None]
            differences.append({"model": model, "rule": rule, **describe(diffs)})
    write_csv(out / "bach_difference.csv", differences)

    # Copy share on Bach melodies (memorisation check, PROGRESS decision 9)
    copies = []
    for model in sorted({r["model"] for r in per_melody}):
        values = [number(r.get("copy_share")) for r in per_melody if r["model"] == model and r["origin"] == "bach"]
        copies.append({"model": model, **describe(values)})
    write_csv(out / "copy_share.csv", copies)

    # Melody features (manipulation check)
    features = []
    for origin in origins:
        group = [m for m in melodies if m["origin"] == origin]
        row = {"origin": origin, "n": len(group)}
        for name in ("measures", "notes", "lowest_midi", "highest_midi", "ambitus", "largest_leap", "fermatas"):
            values = [number(m.get(name)) for m in group if m.get(name) not in ("", None)]
            row[f"{name}_median"] = float(np.median(values)) if values else ""
            row[f"{name}_mean"] = float(np.mean(values)) if values else ""
        inside = [m for m in group if m.get("within_huang_limits") == "1"]
        row["share_outside_huang_limits"] = 1 - len(inside) / len(group) if group else ""
        row["meters"] = ";".join(sorted({m.get("meter", "") for m in group}))
        row["share_minor"] = sum(m.get("key_mode") == "minor" for m in group) / len(group) if group else ""
        features.append(row)
    write_csv(out / "melody_features.csv", features)

    # Hypothesis tests on the main variant
    q2 = apply_holm(q2_tests(per_melody, "main", all_rules))
    write_csv(out / "q2_wilcoxon.csv", q2)
    q3 = apply_holm(q3_tests(per_melody, "main", all_rules, one_sided), family_key="model") if run_origin_test else []
    if run_origin_test:
        write_csv(out / "q3_mannwhitney.csv", q3)
    zone, pattern = [], []
    if run_zone_test:
        zone = apply_holm(zone_tests(per_melody, "main", RULES), family_key="model")
        write_csv(out / "q3_zone.csv", zone)
        for model in ("deepbach", "coconet"):
            pattern += zone_pattern([r for r in per_melody if r["model"] == model], model)
        pattern += zone_pattern(reference, "bach")
        write_csv(out / "zone_pattern.csv", pattern)

    # Sensitivity analyses a, c, d
    sensitivity = {}
    complete = {r["melody_id"] for r in per_melody if r["model"] == "deepbach" and r["all_valid"] == "1"} & \
               {r["melody_id"] for r in per_melody if r["model"] == "coconet" and r["all_valid"] == "1"}
    for name, variant, subset in (("a_fermata", "fermata", None), ("c_complete", "main", complete),
                                  ("d_merged", "merged", None)):
        s2 = apply_holm(q2_tests(per_melody, variant, all_rules, subset))
        write_csv(out / f"sensitivity_{name}_q2.csv", s2)
        sensitivity[name] = {"q2": s2, "n_melodies": len(subset) if subset is not None else None}
        if run_origin_test:
            s3 = apply_holm(q3_tests(per_melody, variant, all_rules, one_sided, subset), family_key="model")
            write_csv(out / f"sensitivity_{name}_q3.csv", s3)
            sensitivity[name]["q3"] = s3
        if run_zone_test and variant in ("main", "merged"):
            sz = apply_holm(zone_tests(per_melody, variant, RULES, subset), family_key="model")
            write_csv(out / f"sensitivity_{name}_q3_zone.csv", sz)
            sensitivity[name]["q3_zone"] = sz

    # Sensitivity b: only with a verified membership file
    seen_unseen = []
    if membership_file and Path(membership_file).exists():
        membership = {r["melody_id"]: r for r in read_csv(membership_file)}
        if all(r.get("verified") == "1" for r in membership.values()):
            for rule in all_rules:
                seen = [rate(r, "main", rule) for r in per_melody if r["model"] == "deepbach" and r["origin"] == "bach"
                        and membership.get(r["melody_id"], {}).get("split") == "train"]
                unseen = [rate(r, "main", rule) for r in per_melody if r["model"] == "deepbach" and r["origin"] == "bach"
                          and membership.get(r["melody_id"], {}).get("split") in ("validation", "evaluation")]
                result = mann_whitney([v for v in unseen if v is not None], [v for v in seen if v is not None], "two-sided")
                seen_unseen.append({"rule": rule, "group_x": "unseen", "group_y": "seen", **result})
    write_csv(out / "seen_unseen.csv", seen_unseen or [{"note": "not run: no verified training-membership file"}])

    # Power: minimum detectable effects for the analysed sizes
    n_pairs = q2[0]["n_pairs"] if q2 else 0
    power_rows = [{"test": "q2 Wilcoxon (paired)", "n": n_pairs,
                   "minimum_detectable_effect": minimum_detectable_d(n_pairs, alpha=alpha, paired=True)}]
    for model in ("deepbach", "coconet"):
        row = next((r for r in q3 if r["model"] == model), None)
        if row:
            power_rows.append({"test": f"q3 Mann-Whitney ({model})", "n": f"{row['n_strube']} vs {row['n_bach']}",
                               "minimum_detectable_effect": minimum_detectable_d(row["n_strube"], row["n_bach"], alpha=alpha)})
        row = next((r for r in zone if r["model"] == model), None)
        if row:
            power_rows.append({"test": f"q3 zone Wilcoxon ({model}, {RULE_LABELS[row['rule']]})", "n": row["n_pairs"],
                               "minimum_detectable_effect": minimum_detectable_d(row["n_pairs"], alpha=alpha, paired=True)})
    write_csv(out / "power.csv", power_rows)

    # LaTeX tables for BAB IV
    tables = out / "tables"
    latex_table(tables / "q2_wilcoxon.tex",
                "Perbandingan laju pelanggaran per birama antara DeepBach dan Coconet pada melodi yang sama (uji peringkat bertanda Wilcoxon)",
                "tab:hasil-q2", ["Kaidah", "Pasangan", "Median selisih", "p", "p Holm", "r"],
                [[RULE_LABELS[r["rule"]], str(r["n_pairs"]), fmt(r["median_difference"]), fmt(r["p_value"]),
                  fmt(r["p_holm"]), fmt(r["effect_size"], 2)] for r in q2])
    if run_origin_test:
        latex_table(tables / "q3_mannwhitney.tex",
                    "Perbandingan laju pelanggaran per birama antara melodi latihan Strube dan melodi chorale Bach pada setiap model (uji Mann--Whitney)",
                    "tab:hasil-q3", ["Model", "Kaidah", "n Strube", "n Bach", "p", "p Holm", "r"],
                    [[MODEL_LABELS[r["model"]], RULE_LABELS[r["rule"]], str(r["n_strube"]), str(r["n_bach"]),
                      fmt(r["p_value"]), fmt(r["p_holm"]), fmt(r["effect_size"], 2)] for r in q3])
    if run_zone_test:
        latex_table(tables / "q3_zona.tex",
                    "Perbandingan laju pelanggaran per kesempatan di zona fermata dan di dalam frasa pada setiap model (uji peringkat bertanda Wilcoxon)",
                    "tab:hasil-q3", ["Model", "Kaidah", "Melodi", "Median selisih", "p", "p Holm", "r"],
                    [[MODEL_LABELS[r["model"]], RULE_LABELS[r["rule"]], str(r["n_pairs"]), fmt(r["median_difference"], 4),
                      fmt(r["p_value"]), fmt(r["p_holm"]), fmt(r["effect_size"], 2)] for r in zone])
        latex_table(tables / "pola_zona.tex",
                    "Laju pelanggaran per kesempatan di zona fermata dan di dalam frasa, digabung atas semua melodi",
                    "tab:hasil-pola-zona", ["Sumber", "Kaidah", "Laju zona fermata", "Laju dalam frasa", "Rasio"],
                    [[MODEL_LABELS[r["source"]], RULE_LABELS[r["rule"]], fmt(r["rate_F"], 4), fmt(r["rate_I"], 4),
                      fmt(r["rate_ratio"], 2)] for r in pattern])
    main_desc = [d for d in descriptive if d["variant"] == "main"]
    latex_table(tables / "deskriptif.tex",
                "Median dan rentang antarkuartil laju pelanggaran per birama menurut model dan asal melodi",
                "tab:hasil-deskriptif", ["Model", "Asal melodi", "Kaidah", "n", "Median", "IQR", "Rata-rata"],
                [[MODEL_LABELS.get(d["model"], d["model"]), ORIGIN_LABELS[d["origin"]], RULE_LABELS[d["rule"]],
                  str(d["n"]), fmt(d["median"]), fmt(d["iqr"]), fmt(d["mean"])] for d in main_desc])

    summary = {
        "run_id": info["run_id"], "stage": info.get("stage"), "alpha": alpha,
        "software": {"numpy": np.__version__, "scipy": scipy.__version__},
        "attempts": summary_rows, "melody_features": features, "q2": q2, "q3": q3, "q3_zone": zone,
        "zone_pattern": pattern, "power": power_rows, "sensitivity": sensitivity, "seen_unseen": seen_unseen,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    return summary


def plot_run(run_dir):
    """Box plots of each rule's per-melody rate by origin and model (BAB IV figures)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    run_dir = Path(run_dir)
    per_melody = read_csv(run_dir / "evaluation" / "per_melody.csv")
    reference = read_csv(run_dir / "evaluation" / "bach_reference.csv")
    out = run_dir / "figures"
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for rule in list(RULES) + ["weighted"]:
        groups, labels = [], []
        for model in ("deepbach", "coconet"):
            for origin in ("bach", "strube"):
                values = [rate(r, "main", rule) for r in per_melody if r["model"] == model and r["origin"] == origin]
                values = [v for v in values if v is not None]
                if values:
                    groups.append(values)
                    labels.append(f"{MODEL_LABELS[model]}\n{ORIGIN_LABELS[origin]}")
        values = [rate(r, "main", rule) for r in reference]
        if values:
            groups.append([v for v in values if v is not None])
            labels.append("Bach\n(acuan)")
        if not groups:
            continue
        figure, axis = plt.subplots(figsize=(7, 4))
        axis.boxplot(groups, showfliers=True)
        axis.set_xticks(range(1, len(labels) + 1), labels, fontsize=8)
        axis.set_ylabel("Pelanggaran per birama")
        axis.set_title(RULE_LABELS[rule])
        figure.tight_layout()
        for suffix in ("pdf", "png"):
            path = out / f"boxplot_{rule}.{suffix}"
            figure.savefig(path, dpi=200)
            written.append(path)
        plt.close(figure)

    # Question 3 (protocol 3.0): pooled rate in the fermata zone and inside the phrase, per source
    pattern = read_csv(run_dir / "analysis" / "zone_pattern.csv")
    if pattern and "rule" in pattern[0]:
        sources = [s for s in ("deepbach", "coconet", "bach") if any(r["source"] == s for r in pattern)]
        figure, axes = plt.subplots(1, len(RULES), figsize=(12, 3.2))
        for axis, rule in zip(axes, RULES):
            rows = {r["source"]: r for r in pattern if r["rule"] == rule}
            positions = np.arange(len(sources))
            fermata = [number(rows[s]["rate_F"]) or 0 for s in sources]
            inside = [number(rows[s]["rate_I"]) or 0 for s in sources]
            axis.bar(positions - 0.2, fermata, width=0.4, label="Zona fermata")
            axis.bar(positions + 0.2, inside, width=0.4, label="Dalam frasa")
            axis.set_xticks(positions, [MODEL_LABELS[s].split(" ")[0] for s in sources], fontsize=7)
            axis.set_title(RULE_LABELS[rule], fontsize=8)
            axis.tick_params(axis="y", labelsize=7)
        axes[0].set_ylabel("Pelanggaran per kesempatan", fontsize=8)
        axes[0].legend(fontsize=7)
        figure.tight_layout()
        for suffix in ("pdf", "png"):
            path = out / f"zona_fermata.{suffix}"
            figure.savefig(path, dpi=200)
            written.append(path)
        plt.close(figure)
    return written
