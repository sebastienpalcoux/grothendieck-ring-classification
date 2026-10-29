#!/usr/bin/env python3
"""Package the new research, frozen previous inputs, and optional builders."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
OUTPUT = WORK/'Fusion_ring_unresolved11_retry_2026-10-24.zip'
ALLOWED = {'.md', '.json', '.gz', '.py', '.tex', '.pdf', '.txt', '.cpp'}
DEPENDENCIES = [
    'phase3/quadratic_s_symmetry/quadratic_s_symmetry.py',
    'phase3/noncomm1975/symmetry.py',
    'phase3/noncomm1975/center.py',
    'phase2/quadratic_theory/quadratic_center.py',
    'phase2/integral_theory/center_lp.py',
    'sources/rings.py', 'sources/exact.py', 'sources/induction.py',
    'sources/higher_traces.py', 'sources/tensor_rotation.py',
    'sources/balanced_traces.py', 'sources/match_models.py',
    'work/scalar_characters.py', 'work/common.py',
]

def main():
    entries = {}
    previous_zip = WORK/'Fusion_ring_unresolved11_research_2026-10-24.zip'
    if previous_zip.exists():
        with zipfile.ZipFile(previous_zip) as z:
            for name in z.namelist():
                if name.endswith('/'):
                    continue
                if not name.startswith('unresolved11_20261024/') or '..' in Path(name).parts:
                    raise ValueError('Unexpected prior archive path')
                entries[name] = z.read(name)
    else:
        for p in (WORK/'unresolved11_20261024').rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix in ALLOWED:
                entries[p.relative_to(WORK).as_posix()] = p.read_bytes()
    for p in HERE.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix in ALLOWED:
            entries[p.relative_to(WORK).as_posix()] = p.read_bytes()
    for rel in DEPENDENCIES:
        p = WORK/'rank9_m2_research'/rel
        entries[p.relative_to(WORK).as_posix()] = p.read_bytes()
    entries['START_HERE.txt'] = (
        'New result: R10_1_189 is unitarily categorified.\n'
        'Classification delta: 1 modeled, 0 excluded, 10 unresolved.\n'
        'Read unresolved11_retry_20261024/README.md.\n'
        'Manuscript: unresolved11_retry_20261024/rank10/rank10_conformal_model.pdf\n'
        'Portable replay: python unresolved11_retry_20261024/verify_retry.py\n'
        'Earlier files are frozen history; their former zero-resolution summary is superseded.\n'
    ).encode()
    entries['rank9_m2_research/REBUILD_DEPENDENCIES.txt'] = (
        'Optional source matrix rebuilders; portable exact replays need none of these packages.\n'
        'Observed successful discovery environment:\n'
        'sympy==1.14.0\nnumpy==2.3.5\nscipy==1.17.0\npython-flint==0.9.0\n'
        'These are copied research builders, not a complete repository checkout.\n'
    ).encode()
    inventory = {'schema': 'fusion-retry-bundle/v1', 'date': '2026-10-24',
                 'files': [{'path': name, 'bytes': len(raw),
                            'sha256': hashlib.sha256(raw).hexdigest()}
                           for name, raw in sorted(entries.items())]}
    entries['BUNDLE_MANIFEST.json'] = (json.dumps(inventory, indent=2)+'\n').encode()
    with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(entries.items()):
            z.writestr(name, raw)
    with zipfile.ZipFile(OUTPUT) as z:
        for item in inventory['files']:
            raw = z.read(item['path'])
            if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
                raise ValueError('Archive integrity failure: '+item['path'])
    print(json.dumps({'path': str(OUTPUT), 'files': len(entries),
                      'bytes': OUTPUT.stat().st_size,
                      'sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}, indent=2))

if __name__ == '__main__':
    main()
