"""Bind evidence directly to the immutable complete rank-seven census."""
import collections
import gzip
import hashlib
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'supplements/rank7/software/rings.py').is_file()
            or ((p / 'software/rings.py').is_file()
                and (p / 'data/rank7_tables.txt.gz').is_file()))
RANK7 = ROOT / 'supplements/rank7' if (ROOT / 'supplements/rank7').is_dir() else ROOT
SOFTWARE = RANK7 / 'software'
SOURCE = RANK7 / 'data/rank7_tables.txt.gz'
SOURCE_SHA256 = '6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def fingerprint(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()

def engine_source_path(relative_path):
    """Preserve repository hash names in a standalone rank-seven archive."""
    prefix = 'supplements/rank7/'
    return RANK7 / relative_path[len(prefix):] if relative_path.startswith(prefix) else ROOT / relative_path

def read_cases(ids):
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
            'complete census hash changed')
    counts = collections.Counter()
    out = {}
    with gzip.open(SOURCE, 'rt') as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            tensor = json.loads(line.replace('{', '[').replace('}', ']'))
            multiplicity = max(v for matrix in tensor for row in matrix for v in row)
            counts[multiplicity] += 1
            case_id = f'R7_{multiplicity}_{counts[multiplicity]}'
            if case_id in ids:
                out[case_id] = {'id': case_id, 'source_line': line_number,
                                'tensor': tensor, 'tensor_sha256': fingerprint(tensor)}
    require(dict(counts) == {1: 43, 2: 319, 3: 1059, 4: 2780}, 'source census totals changed')
    require(set(out) == set(ids), 'requested source case missing')
    return out
