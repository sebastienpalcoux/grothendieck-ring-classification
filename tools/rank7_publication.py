"""Current rank-seven extension metadata, separate from historical M<=4 proofs."""
from collections import Counter
from pathlib import Path
import hashlib
import json

LEDGER = "supplements/rank7/output/rank7_ledger.json"
HISTORICAL_LEDGER = "supplements/rank7/output/rank7_ledger_through_m4.json"
TABLES = "supplements/rank7/data/rank7_tables.txt.gz"
HISTORICAL_TABLES = "supplements/rank7/data/rank7_tables_through_m4.txt.gz"
HISTORICAL_TABLES_SHA256 = "6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9"
HISTORICAL_SHA256 = "00edf884caa59384a1f7b9a91d7273539306443035db5144c02f9bda5bda3d2b"

def extension(repo):
    path = Path(repo) / LEDGER
    records = json.loads(path.read_text())
    rows = [x for x in records if x["multiplicity"] == 5]
    if not rows:
        return None
    counts = Counter(x["status"] for x in rows)
    if set(counts) - {"excluded", "unitarily_realized", "unresolved"}:
        raise ValueError("Unknown rank-seven extension status")
    return {"date": "2026-10-19", "rank": 7, "multiplicity": 5,
            "rings": len(rows), "excluded": counts["excluded"],
            "realized": counts["unitarily_realized"], "unresolved": counts["unresolved"],
            "remaining_ids": [x["id"] for x in rows if x["status"] == "unresolved"],
            "realized_ids": [x["id"] for x in rows if x["status"] == "unitarily_realized"],
            "ledger": LEDGER, "ledger_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def remaining_ids(repo):
    paths = ("supplements/rank6/data/decisions.json", LEDGER,
             "supplements/rank8/data/decisions.json")
    return [row["id"] for name in paths for row in json.loads((Path(repo)/name).read_text())
            if row["status"] == "unresolved"]

def historical_rank7_bytes(repo):
    raw = (Path(repo)/HISTORICAL_LEDGER).read_bytes()
    if hashlib.sha256(raw).hexdigest() != HISTORICAL_SHA256:
        raise ValueError("Historical rank-seven ledger changed")
    current = json.loads((Path(repo)/LEDGER).read_text())
    if [x for x in current if x["multiplicity"] <= 4] != json.loads(raw):
        raise ValueError("Extension changes a historical rank-seven decision")
    return raw

def summary(repo):
    item = extension(repo)
    if item is None:
        return ""
    return (f"The 19 October rank-seven extension addresses all {item['rings']:,} "
            f"exact-multiplicity-five rings: {item['excluded']:,} general exclusions, "
            f"{item['realized']} {'realization' if item['realized']==1 else 'realizations'} and {item['unresolved']} unresolved cases. "
            f"The classification is complete through multiplicity {4 if item['unresolved'] else 5}. "
            + ("The new realization R7_5_5678 is Rep(AGL(1,7)). " if item['realized_ids']==['R7_5_5678'] else "")
            + ("The unresolved records remain open for general complex categorification." if item['unresolved'] else ""))


def historical_sources(repo):
    raw = (Path(repo)/HISTORICAL_TABLES).read_bytes()
    if hashlib.sha256(raw).hexdigest() != HISTORICAL_TABLES_SHA256:
        raise ValueError("Historical rank-seven compressed tensor source changed")
    return {LEDGER: historical_rank7_bytes(repo), TABLES: raw}
