#!/usr/bin/env python3
"""Build/check small reader downloads; only rebuilding page counts needs pypdf."""
from pathlib import Path
import argparse
import ast
import gzip
import hashlib
import itertools
import json
from rank7_publication import STATUS_REPORT
from rank8_publication import current_date, current_report, active as rank8_active, LEDGER as RANK8_LEDGER

ROOT = Path(__file__).resolve().parents[1]
IDS = ('R6_4_155', 'R6_8_1660')
RESOURCE_NAMES = ('remaining_cases.py', 'manuscript_page_counts.json')
PAPERS = (
    ('Rank two', 'rank2.pdf', 'mathematical_manuscript'),
    ('Rank three', 'rank3.pdf', 'mathematical_manuscript'),
    ('Rank four: finite classification', 'rank4/papers/finite.pdf', 'mathematical_manuscript'),
    ('Rank four: unrestricted classification', 'rank4/papers/companion.pdf', 'mathematical_manuscript'),
    ('Rank five', 'rank5/papers/manuscript.pdf', 'mathematical_manuscript'),
    ('Rank six', 'rank6/papers/manuscript.pdf', 'mathematical_manuscript'),
    ('Rank seven', 'rank7/papers/manuscript.pdf', 'mathematical_manuscript'),
    ('Rank eight', 'rank8/paper/rank8.pdf', 'mathematical_manuscript'),
    ('Rank-four verification guide', 'rank4/papers/verification_guide.pdf', 'verification_guide'),
    ('Rank-five verification guide', 'rank5/papers/verification_guide.pdf', 'verification_guide'),
    ('Rank-six verification guide', 'rank6/papers/verification_guide.pdf', 'verification_guide'),
    ('Research status and verification', STATUS_REPORT, 'research_status_report'),
)


def current_papers(repo):
    return tuple((title,current_report(repo) if kind=='research_status_report' else path,kind) for title,path,kind in PAPERS)

def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def flat(tensor):
    return tuple(value for matrix in tensor for row in matrix for value in row)


def tensor_hash(tensor):
    return sha(json.dumps(tensor, separators=(',', ':')).encode())


def validate_tensor(tensor):
    n = len(tensor)
    need(all(len(matrix) == n and all(len(row) == n for row in matrix)
             for matrix in tensor), 'Cubic tensor shape')
    need(all(type(x) is int and x >= 0 for x in flat(tensor)), 'Nonnegative integer coefficients')
    dual = []
    for i in range(n):
        matches = [j for j in range(n) if tensor[i][j][0]]
        need(len(matches) == 1, 'Unique dual')
        dual.append(matches[0])
    for i, j in itertools.product(range(n), repeat=2):
        need(dual[dual[i]] == i and tensor[i][j][0] == int(dual[i] == j), 'Duality')
        for k in range(n):
            need(tensor[0][i][k] == tensor[i][0][k] == int(i == k), 'Unit is basis index zero')
            need(tensor[i][j][k] == tensor[dual[i]][k][j] == tensor[k][dual[j]][i], 'Frobenius reciprocity')
    for i, j, k, l in itertools.product(range(n), repeat=4):
        need(sum(tensor[i][j][a] * tensor[a][k][l] for a in range(n)) ==
             sum(tensor[j][k][a] * tensor[i][a][l] for a in range(n)), 'Associativity')
    return dual


def source_cases(repo):
    path6 = 'supplements/rank6/data/unresolved_tensors.json'
    records6 = {r['id']: r for r in json.loads((repo / path6).read_text())}
    tensors = {name: records6[name]['N'] for name in IDS}
    path7 = 'supplements/rank7/output/rank7_ledger.json'
    records7 = {r['id']: r for r in json.loads((repo / path7).read_text()) if r['status']=='unresolved'}
    tensors.update({name: row['tensor'] for name, row in records7.items()})
    path8 = RANK8_LEDGER
    source8 = 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    if rank8_active(repo):
        rows8 = json.loads((repo/path8).read_text())
        census8 = {r['id']:r['tensor'] for r in json.loads((repo/source8).read_text())}
        tensors.update({r['id']:census8[r['id']] for r in rows8 if r['status']=='unresolved'})
    duals, metadata = {}, {}
    for name, tensor in tensors.items():
        duals[name] = validate_tensor(tensor)
        rank, multiplicity, index = map(int, name[1:].split('_'))
        need(len(tensor) == rank and max(flat(tensor)) == multiplicity, 'Rank and exact multiplicity')
        source = path6 if rank == 6 else path7 if rank == 7 else source8
        metadata[name] = {
            'rank': rank, 'multiplicity': multiplicity, 'index': index,
            'status': 'unresolved', 'unit_index': 0,
            'source': source, 'source_sha256': sha((repo / source).read_bytes()),
            'tensor_sha256': tensor_hash(tensor),
            'selection': 'JSON record with this id',
        }
        if rank == 6:
            need(duals[name] == records6[name]['dual'], 'Recorded rank-six duality')
        ledger_path = 'supplements/rank6/data/decisions.json' if rank == 6 else path7 if rank == 7 else path8
        record = next(r for r in json.loads((repo / ledger_path).read_text()) if r['id'] == name)
        need(record['status'] == 'unresolved', 'Current unresolved ledger status')
        for scope_key in ('unitary_status', 'pseudo_unitary_status'):
            if scope_key in record:
                metadata[name][scope_key] = record[scope_key]
        if 'tensor_sha256' in record:
            need(record['tensor_sha256'] == tensor_hash(tensor), 'Tensor/ledger source identity')
    return tensors, duals, metadata


def render_tensors(repo):
    tensors, duals, metadata = source_cases(repo)
    text = '''"""Exact fusion tensors of the current open general-complex cases.

N[i][j][k] is the coefficient of basis object k in the product i * j.
Basis indices are zero-based; index 0 is the unit. Each named tensor is a
plain Python list of lists of lists. No third-party dependency is needed.
Example: from remaining_cases import R6_4_155, DUALS

These fusion rings are unresolved; tensor consistency does not construct
a fusion category. AI-generated research: independent human verification
and Lean formalization are pending. Use the results and data with caution.
Tensor hashes use UTF-8 JSON with separators=(',', ':') and no trailing newline.
"""

'''
    for name, tensor in tensors.items():
        text += name + ' = [\n'
        for matrix in tensor:
            text += '    [\n' + ''.join('        ' + repr(row) + ',\n' for row in matrix) + '    ],\n'
        text += ']\n\n'
    text += 'DUALS = ' + repr(duals) + '\n\n'
    text += 'METADATA = ' + json.dumps(metadata, indent=4) + '\n\n'
    text += 'TENSORS = {' + ', '.join(repr(name) + ': ' + name for name in tensors) + '}\n'
    return text


def page_totals(records):
    by_kind = {kind: sum(r['pages'] for r in records if r['kind'] == kind)
               for kind in ('mathematical_manuscript', 'verification_guide', 'research_status_report')}
    return {**by_kind, 'mathematical_manuscripts_and_guides': by_kind['mathematical_manuscript'] + by_kind['verification_guide'],
            'all_distinct_documents': sum(by_kind.values())}


def build_pages(repo):
    from pypdf import PdfReader
    records = []
    for title, relative, kind in current_papers(repo):
        path = repo / 'manuscripts' / relative
        records.append({'title': title, 'kind': kind, 'path': path.relative_to(repo).as_posix(),
                        'pages': len(PdfReader(path).pages), 'bytes': path.stat().st_size,
                        'sha256': sha(path.read_bytes())})
    return {'schema': 'manuscript-page-counts/v1', 'date': current_date(repo),
            'counting_rule': 'Count each distinct current document once, including its references and appendices; exclude website/supplement copies and compatibility aliases.',
            'document_counts': {'mathematical_manuscripts': 8, 'verification_guides': 3, 'research_status_reports': 1},
            'documents': records, 'totals': page_totals(records),
            'classification_scope': {'rank2': 'Unrestricted', 'rank3': 'Unrestricted',
                                     'rank4': 'Unrestricted complex classification: 15 Grothendieck rings; every categorification admits a spherical structure. The sharp bounds are FPdim ≤ 24+12√3 and multiplicity ≤ 6.'},
            'caution': 'AI-generated research; independent human verification and Lean formalization pending.'}


def validate_reader_resources(repo, check_web=False):
    repo = Path(repo)
    expected = render_tensors(repo)
    need((repo / 'data/remaining_cases.py').read_text() == expected, 'Regenerate exact reader tensors')
    # No module execution is needed to validate the downloadable Python constants.
    tree = ast.parse(expected)
    assigned = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
                if isinstance(n, ast.Assign) and n.targets[0].id != 'TENSORS'}
    need(all(isinstance(assigned[name], list) for name in IDS), 'Named plain-list tensor constants')
    pages = json.loads((repo / 'data/manuscript_page_counts.json').read_text())
    need(pages['schema'] == 'manuscript-page-counts/v1', 'Page-count schema')
    need(pages['document_counts'] == {'mathematical_manuscripts': 8, 'verification_guides': 3,
                                     'research_status_reports': 1}, 'Distinct document counts')
    records = pages['documents']
    need([(r['title'], r['path'], r['kind']) for r in records] ==
         [(title, 'manuscripts/' + path, kind) for title, path, kind in current_papers(repo)], 'Distinct current paper inventory')
    for record in records:
        raw = (repo / record['path']).read_bytes()
        need(type(record['pages']) is int and record['pages'] > 0, 'Positive integer page count')
        need(len(raw) == record['bytes'] and sha(raw) == record['sha256'], 'Page-count PDF binding: ' + record['path'])
    need(pages['totals'] == page_totals(records), 'Page totals')
    if check_web:
        for name in RESOURCE_NAMES:
            need((repo / 'data' / name).read_bytes() == (repo / 'site/dist/downloads' / name).read_bytes(),
                 'Reader download differs from source: ' + name)
    return {'status': 'PASS', 'case_ids': list(source_cases(repo)[0]), 'page_totals': pages['totals'],
            'resource_sha256': {name: sha((repo / 'data' / name).read_bytes()) for name in RESOURCE_NAMES}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not args.check:
        (repo / 'data/remaining_cases.py').write_text(render_tensors(repo))
        (repo / 'data/manuscript_page_counts.json').write_text(json.dumps(build_pages(repo), indent=2) + '\n')
        for name in RESOURCE_NAMES:
            (repo / 'site/dist/downloads' / name).write_bytes((repo / 'data' / name).read_bytes())
    print(json.dumps(validate_reader_resources(repo, check_web=True), indent=2))


if __name__ == '__main__':
    main()
