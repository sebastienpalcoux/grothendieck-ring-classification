#!/usr/bin/env python3
"""Build the site snapshot from the exact, curated classification repository.

Run this in the site checkout with --classification PATH. The repository's
data/counts.json is the source of truth; no count is scraped from a PDF.
"""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_counts(path: Path):
    payload = json.loads(path.read_text())
    if isinstance(payload, list):
        return {"rows": payload}
    for key in ("rows", "counts", "data"):
        if isinstance(payload.get(key), list):
            payload["rows"] = payload[key]
            return payload
    raise ValueError(f"No count rows in {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--classification", type=Path, required=True)
    args = parser.parse_args()
    repo = args.classification.resolve()
    counts = read_counts(repo / "data" / "counts.json")
    rows = []
    for row in counts["rows"]:
        rank = int(row["rank"])
        multiplicity = int(row["multiplicity"])
        rings = int(row["rings"])
        if min(rank, multiplicity, rings) < 0:
            raise ValueError(f"Negative coordinate/count: {row}")
        if "source" not in row:
            raise ValueError(f"Missing source: {row}")
        rows.append({
            "rank": rank,
            "multiplicity": multiplicity,
            "rings": rings,
            "source": row["source"],
            "verification": row.get("verification", ""),
        })
    keys = [(r["rank"], r["multiplicity"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate rank/multiplicity")
    rows.sort(key=lambda r: (r["rank"], r["multiplicity"]))
    for summary in counts.get("rank_summary", []):
        band = [r for r in rows if r["rank"] == summary["rank"]]
        expected = list(range(1,summary["recorded_through"]+1))
        if [r["multiplicity"] for r in band] != expected:
            raise ValueError(f"Incomplete census coverage for rank {summary['rank']}")
        if sum(r["rings"] for r in band) != summary["classes_at_recorded_bound"]:
            raise ValueError(f"Cumulative census mismatch for rank {summary['rank']}")
    status_file = repo / "data" / "classification_status.json"
    status = json.loads(status_file.read_text())
    if not isinstance(status.get("rows"), list):
        raise ValueError("Classification status file has no rows")
    census_index = {(r["rank"], r["multiplicity"]):r["rings"] for r in rows}
    classifications = status["rows"]
    for record in classifications:
        key=(record["rank"],record["multiplicity"])
        if census_index.get(key) != record["rings"]:
            raise ValueError(f"Census/ledger mismatch for {key}")
        fields = ("excluded_general","realized_unitary","realized_other_or_unspecified",
                  "realized_spherical_nonpseudounitary","unresolved_general","unassessed")
        if sum(record[k] for k in fields) != record["rings"]:
            raise ValueError(f"Status sum mismatch for {key}")
    # Publish ranks with a manuscript and a genuine categorification ledger.
    # A census-only rank is never represented as classified research.
    classifications = [r for r in classifications if 2 <= r["rank"] <= 8 and
                       r["classification_coverage"]!="census_only"]
    covered = {(r["rank"],r["multiplicity"]) for r in classifications}
    rows = [r for r in rows if (r["rank"],r["multiplicity"]) in covered]
    def positive(record):
        return sum(record[field] for field in (
            "realized_unitary", "realized_other_or_unspecified",
            "realized_spherical_nonpseudounitary"))
    positive_rows = [{"rank":r["rank"],"multiplicity":r["multiplicity"],"rings":positive(r),
                      "is_lower_bound":r["classification_coverage"]!="complete_classification"}
                     for r in classifications if positive(r)>0]
    def scope_record(rank):
        band=sorted((r for r in classifications if r["rank"]==rank),key=lambda r:r["multiplicity"])
        through=0
        for r in band:
            if r["multiplicity"]!=through+1 or r["classification_coverage"]!="complete_classification":break
            through+=1
        unresolved=sum(r["unresolved_general"] for r in band)
        return {"rank":rank,"through":through,"analyzed_through":max(r["multiplicity"] for r in band),
                "kind":"complete" if len(band)==through else "partial",
                "rings":sum(r["rings"] for r in band),"positive":sum(positive(r) for r in band),
                "unresolved":unresolved,
                "paper":f"Rank-{rank} classification manuscript",
                "note":("General existence remains open for the stated residuals." if unresolved else
                        "All analyzed bands are classified by a model or exclusion.")}
    scoped_ranks=sorted({r["rank"] for r in classifications})
    scope=[{"rank":rank,"through":None,"analyzed_through":None,"kind":"unrestricted",
            "rings":None,"positive":sum(positive(r) for r in classifications if r["rank"]==rank),
            "unresolved":0,"paper":f"Rank-{rank} classification manuscript",
            "note":"Unrestricted complex classification."}
           if rank in (2,3) else scope_record(rank) for rank in scoped_ranks]
    data = {
        "snapshot": "2026-09-23",
        "source_repository": counts.get("census_repository", "https://github.com/sebastienpalcoux/fusion-ring-census"),
        "census_commit": counts.get("census_commit", ""),
        "classification_repository": "https://github.com/sebastienpalcoux/grothendieck-ring-classification",
        "rows": rows,
        "grothendieck_rows":positive_rows,
        "scope":scope,
    }
    output = HERE / "dist" / "data" / "atlas.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    status["rows"] = classifications
    status["site_filter"] = "Ranks 2–8 with complete or partial categorification analysis; unassessed census-only bands omitted."
    (output.parent / "classification_status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n")
    with (output.parent / "counts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("rank", "multiplicity", "rings", "source", "verification"))
        writer.writeheader()
        writer.writerows(rows)
    with (output.parent / "grothendieck_counts.csv").open("w", newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=("rank","multiplicity","rings","is_lower_bound"))
        writer.writeheader();writer.writerows(positive_rows)
    print(f"Wrote {len(rows)} count rows to {output}")


if __name__ == "__main__":
    main()
