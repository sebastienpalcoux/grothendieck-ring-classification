"""Build a research snapshot; omit external papers, caches and supplied raw data."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'Fusion_ring_unresolved11_research_2026-10-24.zip'

def selected(path):
    rel = path.relative_to(ROOT)
    if any(part.startswith('.') or part == '__pycache__' for part in rel.parts):
        return False
    if rel.parts[0] == 'laptop_feedback':
        return False
    if path.name == 'ARCHIVE_INVENTORY.json':
        return False
    return path.is_file() and (path.suffix in {'.md', '.json', '.py', '.log', '.tex'}
                              or path.name.endswith('.json.gz'))

def main():
    source = json.loads((ROOT / 'inputs/manifest.json').read_text())
    status = {
        'source_commit': source['source_commit'],
        'date': '2026-10-24',
        'new_whole_ring_exclusions': 0,
        'new_categorical_models': 0,
        'remaining_unresolved': len(source['cases']),
        'cases': {rid: 'unresolved' for rid in source['cases']},
        'new_positive_TY_sign_exclusions': ['R9_2_1607', 'R9_2_1975', 'R9_2_1976'],
        'new_extreme_Morita_branch_exclusion': 'R9_2_1975, (alpha,a)=(2,0)',
        'new_all_rank_module_rigidity': 'R8_3_928',
        'online_changes': False,
    }
    (ROOT / 'STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
    content = [(p.relative_to(ROOT).as_posix(), p.read_bytes())
               for p in sorted(ROOT.rglob('*')) if selected(p)]
    inventory = {
        'source_commit': source['source_commit'],
        'files': [{'path': name, 'bytes': len(data),
                   'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in content],
        'exclusions': ['downloaded third-party papers', 'interpreter caches',
                       'transfer helpers', 'original supplied laptop archive'],
    }
    encoded = (json.dumps(inventory, indent=2) + '\n').encode()
    (ROOT / 'ARCHIVE_INVENTORY.json').write_bytes(encoded)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in content:
            archive.writestr(ROOT.name + '/' + name, data)
        archive.writestr(ROOT.name + '/ARCHIVE_INVENTORY.json', encoded)
    with zipfile.ZipFile(OUT) as archive:
        if archive.testzip() is not None:
            raise ValueError('Corrupt archive')
        for record in inventory['files']:
            data = archive.read(ROOT.name + '/' + record['path'])
            if hashlib.sha256(data).hexdigest() != record['sha256']:
                raise ValueError('Archive hash mismatch: ' + record['path'])
    print(json.dumps({'file': str(OUT), 'files': len(content) + 1,
                      'bytes': OUT.stat().st_size,
                      'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest()}))

if __name__ == '__main__':
    main()
