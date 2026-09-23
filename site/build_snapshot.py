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
    # The project scope is ranks 2–6. Show only fully or partially assessed
    # bands; purely enumerated higher-rank or unassessed bands stay in source.
    classifications = [r for r in classifications if r["rank"] in (2,3,4,5,6) and
                       r["classification_coverage"]!="census_only"]
    covered = {(r["rank"],r["multiplicity"]) for r in classifications}
    rows = [r for r in rows if (r["rank"],r["multiplicity"]) in covered]
    def scope_record(rank,through,title):
        band=[r for r in classifications if r["rank"]==rank and r["multiplicity"]<=through]
        if len(band)!=through or any(r["classification_coverage"]!="complete_classification" for r in band):
            raise ValueError(f"Claimed complete scope r={rank}, m≤{through} is not supported by status ledger")
        realized=sum(r["realized_unitary"]+r["realized_other_or_unspecified"]+
                     r["realized_spherical_nonpseudounitary"] for r in band)
        remaining=[r for r in classifications if r["rank"]==rank and
                   r["classification_coverage"]=="partial_classification"]
        unresolved=sum(r["unresolved_general"] for r in remaining)
        note=(f"Ledger to m = {max(r['multiplicity'] for r in remaining)}; "
              f"{unresolved} general residual{'s' if unresolved!=1 else ''}."
              if remaining else "")
        complete_beyond=[r for r in classifications if r["rank"]==rank and
                         r["multiplicity"]>through and
                         r["classification_coverage"]=="complete_classification"]
        if complete_beyond:
            bands=", ".join(str(r["multiplicity"]) for r in complete_beyond)
            if all(r["excluded_general"]==r["rings"] for r in complete_beyond):
                note += f" Exact m = {bands}: all excluded."
            else:
                note += f" Exact m = {bands}: completely classified."
        return {"rank":rank,"through":through,"kind":"complete",
                "rings":sum(r["rings"] for r in band),"positive":realized,"paper":title,
                "note":note}
    data = {
        "snapshot": "2026-09-23",
        "source_repository": counts.get("census_repository", "https://github.com/sebastienpalcoux/fusion-ring-census"),
        "census_commit": counts.get("census_commit", ""),
        "classification_repository": "https://github.com/sebastienpalcoux/grothendieck-ring-classification",
        "rows": rows,
        "classification_rows": classifications,
        "scope": [
            {"rank": 2, "through": None, "kind": "complete", "rings": None, "positive": 2,
             "note": "Two categorifiable ring types; a self-contained proof over ℂ.",
             "paper": "Rank-two Grothendieck rings"},
            {"rank": 3, "through": None, "kind": "complete", "rings": None, "positive": 5,
             "note": "Five categorifiable ring types; an unrestricted self-contained proof.",
             "paper": "Rank-three sphericality"},
            scope_record(4,128,"Rank-four Grothendieck rings through multiplicity 128"),
            scope_record(5,17,"Rank-five Grothendieck rings through multiplicity twenty: two general residuals at eighteen"),
            scope_record(6,2,"Rank-six Grothendieck rings"),
        ],
    }
    output = HERE / "dist" / "data" / "atlas.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    status["rows"] = classifications
    status["site_filter"] = "Only ranks 2–6 with complete or partial classification coverage; unassessed census-only bands are omitted."
    (output.parent / "classification_status.json").write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n")
    with (output.parent / "counts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("rank", "multiplicity", "rings", "source", "verification"))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} count rows to {output}")


if __name__ == "__main__":
    main()
