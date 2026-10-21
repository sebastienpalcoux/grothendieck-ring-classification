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
HISTORICAL_MODELS_CANONICAL_SHA256 = "05b8f324fe634b7653dab141784e9a36c395f21d26006dfd0be8b99a91ccea06"
HISTORICAL_OUTPUT_MODELS_CANONICAL_SHA256 = "794a2c85fd871baa8484493ecce613630c140c45b2deb0c8cf6e718546f4d2e2"
PUBLICATION_DATE = "2026-10-20"
PUBLICATION_DATE_LONG = "20 October 2026"
STATUS_REPORT = "prepublication-review-2026-10-20.pdf"

def extension(repo):
    path = Path(repo) / LEDGER
    records = json.loads(path.read_text())
    rows = [x for x in records if x["multiplicity"] == 5]
    if not rows:
        return None
    counts = Counter(x["status"] for x in rows)
    if set(counts) - {"excluded", "unitarily_realized", "unresolved"}:
        raise ValueError("Unknown rank-seven extension status")
    result = {"date": PUBLICATION_DATE, "rank": 7, "multiplicity": 5,
            "rings": len(rows), "excluded": counts["excluded"],
            "realized": counts["unitarily_realized"], "unresolved": counts["unresolved"],
            "remaining_ids": [x["id"] for x in rows if x["status"] == "unresolved"],
            "realized_ids": [x["id"] for x in rows if x["status"] == "unitarily_realized"],
            "ledger": LEDGER, "ledger_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    continuation = Path(repo) / 'evidence/rank7_m5_20261020/accepted/decisions.json'
    if continuation.is_file():
        accepted = json.loads(continuation.read_text())
        by_id = {row['id']: row for row in rows}
        if all(by_id[item['id']]['status'] == 'excluded' for item in accepted):
            proofs = {
                'quadratic_casimir_compression': 'criteria/QUADRATIC_COMPRESSION_PROOF.md',
                'oriented_signed_compression': 'criteria/R4569_GENERAL_PROOF.md',
                'quadratic_center_Galois_two_moment_q60': 'criteria/Q60_CENTER_TRACE_PROOF.md',
                'cyclic3_full_morita_rank13_descent': 'modules/README.md',
                'character': 'computation/README.md',
                'oriented_dimension_order': 'criteria/INDEPENDENT_SCOPE_AUDIT.md',
                'quadratic_center_coupled_cyclic_rotation': 'models/sqrt5/CYCLIC_ROTATION_OBSTRUCTION.md',
            }
            result['continuation_decisions'] = [
                {'id': item['id'], 'rank': 7, 'status': 'excluded', 'scope': 'general_complex',
                 'criterion': item['criterion'], 'proof_source': 'evidence/rank7_m5_20261020',
                 'proof': ({'R7_5_3895': 'models/sqrt5/R3895_CYCLIC_CHAIN.md',
                            'R7_5_5039': 'models/sqrt5/R5039_CYCLIC_CHAIN.md'}.get(
                                item['id'], proofs.get(item['criterion'], 'README.md')))}
                for item in accepted]
    return result

def replay_status(repo):
    """Report only full receipts bound to the current ledger, never old passes."""
    current = extension(repo)
    matched = []
    for mode in ('normal', 'optimized'):
        path = Path(repo) / f'supplements/rank7/output/m5/replay_{mode}.json'
        if not path.is_file():
            continue
        receipt = json.loads(path.read_text())
        if (receipt.get('status') == 'PASS' and receipt.get('mode') == 'full_exact_replay'
                and receipt.get('ledger_sha256') == current['ledger_sha256']
                and receipt.get('new_exclusions_replayed') == current['excluded']):
            matched.append(mode)
    if matched == ['normal', 'optimized']:
        return 'Exact normal and optimized aggregate replays passed for the current ledger.'
    if matched:
        return ('The exact ' + ' and '.join(matched) + ' aggregate replay passed for the current ledger; '
                + ' and '.join(m for m in ('normal', 'optimized') if m not in matched)
                + ' aggregate replay is pending for this revision.')
    return 'Full aggregate replays are pending for this ledger revision.'

def remaining_ids(repo):
    from rank8_publication import ledger_path
    paths = ("supplements/rank6/data/decisions.json", LEDGER, ledger_path(repo))
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
    return (f"The rank-seven multiplicity-five continuation addresses all {item['rings']:,} "
            f"supplied exact-multiplicity-five rings: {item['excluded']:,} general exclusions, "
            f"{item['realized']} {'realization' if item['realized']==1 else 'realizations'} and {item['unresolved']} unresolved {'case' if item['unresolved']==1 else 'cases'}. "
            f"The classification of the supplied census is complete through multiplicity {4 if item['unresolved'] else 5}. "
            + ("The new realization R7_5_5678 is Rep(AGL(1,7)). " if item['realized_ids']==['R7_5_5678'] else "")
            + (("The unresolved record remains open for general complex categorification." if item['unresolved']==1 else "The unresolved records remain open for general complex categorification.") if item['unresolved'] else "")).rstrip()


def historical_sources(repo):
    raw = (Path(repo)/HISTORICAL_TABLES).read_bytes()
    if hashlib.sha256(raw).hexdigest() != HISTORICAL_TABLES_SHA256:
        raise ValueError("Historical rank-seven compressed tensor source changed")
    ledger = historical_rank7_bytes(repo)
    model_ids = {row['id'] for row in json.loads(ledger)
                 if row['status'] == 'unitarily_realized'}
    models = json.loads((Path(repo)/'supplements/rank7/data/model_catalog.json').read_text())
    previous = [row for row in models if row['id'] in model_ids]
    canonical = json.dumps(previous, sort_keys=True, separators=(',', ':')).encode()
    if (len(previous) != len(model_ids)
            or hashlib.sha256(canonical).hexdigest() != HISTORICAL_MODELS_CANONICAL_SHA256):
        raise ValueError('Historical rank-seven model catalog changed')
    model_bytes = (json.dumps(previous, indent=2)+'\n').encode()
    # The old output alias predates the two unified-stage constructions.
    # Restore both historical views, each bound to its own immutable identity.
    old_output = [row for row in previous if row['id'] not in {'R7_4_35', 'R7_4_2665'}]
    canonical_output = json.dumps(old_output, sort_keys=True, separators=(',', ':')).encode()
    if hashlib.sha256(canonical_output).hexdigest() != HISTORICAL_OUTPUT_MODELS_CANONICAL_SHA256:
        raise ValueError('Historical rank-seven output model catalog changed')
    return {LEDGER: ledger, TABLES: raw,
            'supplements/rank7/data/model_catalog.json': model_bytes,
            'supplements/rank7/output/rank7_model_catalog.json':
                (json.dumps(old_output, separators=(',', ':'))+'\n').encode()}
