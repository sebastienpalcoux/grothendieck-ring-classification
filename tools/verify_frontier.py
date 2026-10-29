#!/usr/bin/env python3
"""Validate the current unified frontier and its immutable mathematical inputs.

This verifies published metadata, complete ledger projections, profile scope,
document bytes and exact structural properties. The saved twelve-check replay
and six rational separators are source-bound here; they are not rerun by this
publication validator. Full census coverage has its own independent checks.
"""
from pathlib import Path, PurePosixPath
from collections import Counter
from fractions import Fraction
import argparse
import ast
import hashlib
import json
import sys

from frontier import ROOT, DATE, EVIDENCE, LEDGER, EXACT_LEDGER, BASELINE, REMAINING, R8_REMAINING, FINDINGS, validate_ledger

OLD_ACCEPTED = 'evidence/frontier_20261027/accepted.json'
OLD_ACCEPTED_SHA = 'a9ef88bf0f02920925b400b999cd69bf36984f302fab9b1d4b74c44c4f20c4d1'
OLD_LEDGER = 'evidence/frontier_20261027/rank9_m2_ledger.json'
OLD_LEDGER_SHA = '12bb011413fd8a97e9425124ddaed8e7c6f31a7209feda0f8f7109dd49b362f0'
OLD_INPUT = 'evidence/rank9_m2_20261024/ledger.json'
OLD_INPUT_SHA = '0f8c9b45f328d084735eb2c514308a87bbf176c7fb0a7fcd99578f18d0d0097e'
OLD_EXCLUSIONS = {'R9_2_1607', 'R9_2_1975', 'R9_2_1976'}
R8_BASELINE_SHA = '16a4723f149222ba8cb4f91d07d8ef75176ba5e95b20ff7594ed17e8e4e033fe'
INHERITED = {
    'evidence/rank8_research_20261022/pivotality/general_spherical_gates.json':
        '89ad25baeb05b69c95519670eb4cdd894a29d3b7f4d920535b1f404f46ba13d4',
    'evidence/rank8_creative_20261022/r1768/verification.json':
        '2a2472719aa4e953b7f514dfb4f811a4bef162b2c779cf4bb367a6c21bb977b8',
}
EXPECTED_REPLAYS = {
    'new/root/pivotal_conjugation_parity.py',
    'new/r155/verify_morita_ring_rigidity.py',
    'new/r1660_941/verify.py',
    'new/r1660_941/quantum_routes.py',
    'new/r1660_941/r941_galois_followup.py',
    'new/r928/verify_spectral_reduction.py',
    'new/r1154/verify_simple_center_inputs.py',
    'new/r1154/verify_conjugation_audit.py',
    'new/r137/verify_structural.py',
    'new/r155/verify_r137_forced_galois_audit.py',
    'new/r1768/verify_palindromic_exclusion.py',
    'new/r1768/replay_palindromic_center.py',
}
PROPERTIES = {'integral', 'weakly_integral', 'pointed', 'perfect', 'simple',
              'commutative', 'self_dual', 'multiplicity_free'}
REPORT_TEX = 'manuscripts/frontier/Fusion_Ring_Frontier.tex'
REPORT_PDF = 'manuscripts/frontier/Fusion_Ring_Frontier.pdf'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source(repo, name, expected):
    path = PurePosixPath(name)
    need(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name,
         'Safe source path: ' + name)
    file = repo / name
    need(file.is_file() and sha(file) == expected, 'Source binding: ' + name)


def check_inherited(repo):
    """Retain the three older exclusions and all their accepted proof bindings."""
    source(repo, OLD_ACCEPTED, OLD_ACCEPTED_SHA)
    old = read(repo / OLD_ACCEPTED)
    need(old['schema'] == 'frontier-20261027/v1' and old['date'] == '2026-10-27',
         'Inherited acceptance identity')
    source(repo, OLD_INPUT, OLD_INPUT_SHA)
    source(repo, OLD_LEDGER, OLD_LEDGER_SHA)
    initial, final = read(repo / OLD_INPUT), read(repo / OLD_LEDGER)
    need(len(initial) == len(final) == 2083, 'Inherited exact rank-nine coverage')
    changed = []
    for a, b in zip(initial, final):
        need(a['id'] == b['id'] and a['tensor_sha256'] == b['tensor_sha256'],
             'Inherited rank-nine tensor/order')
        if a != b:
            changed.append(a['id'])
            need(a['status'] == 'unresolved' and b['status'] == 'excluded',
                 'Inherited decision direction')
            need(all(a.get(k) == b.get(k) for k in set(a) | set(b)
                     if k not in ('status', 'exclusion_certificates')),
                 'Unrelated inherited rank-nine field')
    need(set(changed) == OLD_EXCLUSIONS and len(changed) == 3,
         'Exactly the three inherited exclusions')
    need(Counter(r['status'] for r in final) ==
         Counter(excluded=2046, unitarily_realized=36, unresolved=1),
         'Inherited rank-nine partition')
    for item in old['transitions']:
        need(item['id'] in OLD_EXCLUSIONS, 'Inherited transition identifier')
        source(repo, item['proof'], item['proof_sha256'])
    for name, digest in old['source_sha256'].items():
        source(repo, name, digest)
    for key in ('replay_archive', 'exact_replay'):
        value = old[key]
        source(repo, value['path'], value['sha256'])
    receipt = read(repo / old['exact_replay']['path'])
    need(receipt['status'] == 'PASS' and len(receipt['checks']) == 14 and
         receipt['archive_sha256'] == old['replay_archive']['sha256'],
         'Inherited fourteen-check replay')
    for name, digest in INHERITED.items():
        source(repo, name, digest)
    return {r['id']: r for r in final}


def check_acceptance(repo):
    accepted = read(repo / EVIDENCE / 'accepted.json')
    need(accepted['schema'] == 'fusion-ring-frontier/v1' and accepted['date'] == DATE,
         'Current accepted stage identity')
    need(accepted['baseline_commit'] == 'd920cc2531d8b03583c797886a3c2ab6170a281a',
         'Published baseline commit')
    need(accepted['baseline_ledger'] == BASELINE and
         accepted['baseline_ledger_sha256'] == R8_BASELINE_SHA,
         'Frozen rank-eight baseline identity')
    source(repo, BASELINE, R8_BASELINE_SHA)
    need(accepted['new_general_exclusions'] == ['R8_3_1768'] and
         accepted['new_models'] == [] and accepted['remaining_ids'] == REMAINING,
         'Exactly one new exclusion, no models, six unresolved')
    bindings = accepted['source_sha256']
    need(bool(bindings), 'Nonempty complete proof input bindings')
    for name, digest in bindings.items():
        source(repo, name, digest)
    replay = accepted['exact_replay']
    source(repo, replay['path'], replay['sha256'])
    receipt = read(repo / replay['path'])
    need(receipt['all_pass'] is True and replay['checks'] == 12 and
         len(receipt['checks']) == 12, 'Complete twelve-check replay receipt')
    need({r['script'] for r in receipt['checks']} == EXPECTED_REPLAYS and
         all(r['exit_code'] == 0 for r in receipt['checks']), 'All required checks passed')
    for name in EXPECTED_REPLAYS:
        need(EVIDENCE + '/replay/' + name in bindings, 'Replay program is bound: ' + name)
    need(len(accepted['mathematical_dependencies']) == 4,
         'Categorical premises remain explicit')
    rpath = EVIDENCE + '/replay/new/r1768/palindromic_center_receipt.json'
    need(rpath in bindings, 'Six-certificate receipt source binding')
    cert = read(repo / rpath)
    need(cert['verification'] == 'PASS' and cert['arithmetic_domain_replayed'] is True,
         'Exact full-domain certificate replay')
    need(cert['tensor_sha256'] ==
         '240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0',
         'R1768 certificate tensor')
    need(cert['palindromic_signs'] == [[1,-1,1,1,-1,1,-1,-1],[1]*8],
         'Complete two-sign pivotal domain')
    branches = cert['negative_sign_five_Gram_branches']
    need([r['V'] for r in branches] == list(range(5)), 'All five primitive-37 branches')
    for row in branches:
        need(row['U'] + 4 * row['V'] == 16 and row['allowed_columns'] == 6100 and
             row['indicators'] == [-1,1,1,-1,1,-1,-1], 'Negative-sign branch domain')
    positive = cert['positive_sign_branch']
    need(positive['allowed_columns'] == 10711 and positive['indicators'] == [1]*7,
         'All-positive complete C2 domain')
    for row in branches + [positive]:
        need(row['negative_columns'] == 0 and Fraction(row['minimum_column_pairing']) >= 0 and
             Fraction(row['rhs']) < 0, 'Exact separating signs')
    return accepted


def check_profiles(repo, rank9):
    rows = {}
    for name in ('unresolved_cases.json', 'resolved_cases.json', 'rank9_m2.json'):
        payload = read(repo / 'site/dist/data' / name)
        if name == 'rank9_m2.json':
            need({r['id'] for r in payload['cases']} == set(rank9),
                 'All rank-nine profiles retain complete accepted coverage')
            for row in payload['cases']:
                decision = rank9[row['id']]
                need(row['status'] == decision['status'] and
                     row['tensor_sha256'] == decision['tensor_sha256'],
                     'Rank-nine profile retains its accepted decision: ' + row['id'])
        for row in payload['cases']:
            if row['id'] in rows:
                need(rows[row['id']]['status'] == row['status'] and
                     rows[row['id']]['fusion_tensor'] == row['fusion_tensor'],
                     'Duplicate current profile consistency')
            rows[row['id']] = row
    need({rid for rid, row in rows.items() if row['status'] == 'unresolved'} == set(REMAINING),
         'Exactly six current unresolved profiles')
    ledger = {r['id']: r for r in read(repo / LEDGER)}
    realized = read(repo/'site/dist/data/realized_rings.json')
    models = [r for r in realized.get('records', realized.get('cases', []))
              if r['id'].startswith('R8_')]
    need({r['id'] for r in models} ==
         {rid for rid, r in ledger.items() if r['status'] == 'unitarily_realized'},
         'All ninety-three rank-eight model profiles unchanged in identity')
    for row in models:
        tensor = row.get('fusion_tensor', row.get('tensor'))
        digest = hashlib.sha256(json.dumps(tensor, separators=(',',':')).encode()).hexdigest()
        need(digest == ledger[row['id']]['tensor_sha256'],
             'Exact rank-eight model tensor: ' + row['id'])
    for rid in {'R8_3_1768'} | OLD_EXCLUSIONS:
        row = rows[rid]
        scope = row['categorification_scope']
        need(row['status'] == row['existence'] == scope['general_status'] == 'excluded' and
             scope['level_status'] == {k: 'excluded' for k in
             ('general','pivotal','spherical','pseudo_unitary','unitary')} and
             scope['strongest_excluded'] == 'general', 'General-complex profile scope: ' + rid)
        decision = next(r for r in row['research']
                        if r.get('title') == 'Current accepted case decision')
        need(decision['data'] == (ledger[rid] if rid == 'R8_3_1768' else rank9[rid]),
             'Profile decision matches accepted ledger: ' + rid)
    for rid in FINDINGS:
        row = rows[rid]
        need(row['summary'] == FINDINGS[rid][0], 'Unified current finding: ' + rid)
        for item in row['evidence']:
            if 'path' in item and 'sha256' in item:
                source(repo, item['path'], item['sha256'])
    module = ast.parse((repo / 'data/current_remaining_cases.py').read_text())
    values = {n.targets[0].id: ast.literal_eval(n.value) for n in module.body
              if isinstance(n, ast.Assign)}
    need(set(values['TENSORS']) == set(values['METADATA']) == set(REMAINING),
         'Six-case tensor and metadata download')
    for rid, tensor in values['TENSORS'].items():
        need(rows[rid]['fusion_tensor'] == tensor, 'Exact current tensor: ' + rid)
    need((repo/'data/current_remaining_cases.py').read_bytes() ==
         (repo/'site/dist/downloads/current_remaining_cases.py').read_bytes(),
         'Current tensor download mirror')
    atlas = read(repo/'site/dist/data/atlas.json')
    need(atlas['snapshot'] == DATE and atlas['remaining_ids'] == REMAINING,
         'Current Atlas date and frontier')
    summary = read(repo/'data/classification_summary_all_ranks.json')
    need(summary['date'] == DATE and sum(r['unresolved_general'] for r in summary['rows']) == 6,
         'All-rank unresolved partition')
    band = next(r for r in summary['rows'] if r['rank'] == 8 and r['multiplicity'] == 3)
    need((band['rings'], band['excluded_general'], band['realized_unitary'],
          band['unresolved_general']) == (3527,3508,16,3), 'Rank-eight summary band')
    return rows


def check_documents(repo):
    from pypdf import PdfReader
    lower = [rid for rid in REMAINING if int(rid.split('_')[0][1:]) <= 8]
    for name in ('current_document_revision.json', 'current_publication_revision.json'):
        value = read(repo/'data'/name)
        need(value['date'] == DATE, 'Current manifest date: ' + name)
        need(value['remaining_ids'] == (lower if name == 'current_document_revision.json' else REMAINING),
             'Manifest open-case scope: ' + name)
        if name == 'current_publication_revision.json':
            need(value['current_unresolved_total'] == 6, 'Publication open total')
        docs = value['documents']
        need(REPORT_TEX in docs and REPORT_PDF in docs, 'Unified frontier report in ' + name)
        need(not any('prepublication-review-' in p for p in docs), 'No superseded current report in ' + name)
        for path, item in docs.items():
            source(repo, path, item['sha256'])
            need((repo/path).stat().st_size == item['bytes'], 'Current document length: ' + path)
        need(value['web_copies'].get('papers/frontier.pdf') == REPORT_PDF,
             'Canonical frontier web PDF: ' + name)
        need(not any('prepublication-review-' in p for p in value['web_copies']),
             'No superseded report mirror')
        for web, path in value['web_copies'].items():
            need((repo/path).read_bytes() == (repo/'site/dist'/web).read_bytes(),
                 'Website document mirror: ' + web)
        need((repo/'data'/name).read_bytes() == (repo/'site/dist/data'/name).read_bytes(),
             'Website manifest copy: ' + name)
    for prefix in ('rank6/papers', 'rank8/paper'):
        for path in (repo/'manuscripts'/prefix).rglob('*'):
            if path.is_file() and path.suffix in ('.tex', '.pdf'):
                mirror = repo/'supplements'/prefix/path.relative_to(repo/'manuscripts'/prefix)
                if mirror.exists():
                    need(path.read_bytes() == mirror.read_bytes(), 'Supplement mirror: ' + str(path.relative_to(repo)))
    page_cache = {}
    for name in ('manuscript_page_counts.json', 'current_manuscript_page_counts.json'):
        value = read(repo/'data'/name)
        need(value['date'] == DATE, 'Current page inventory date')
        documents = value['documents']
        need(len({r['path'] for r in documents}) == len(documents), 'Unique page inventory paths')
        reports = [r for r in documents if r['kind'] == 'research_status_report']
        need(len(reports) == 1 and reports[0]['path'] == REPORT_PDF, 'One unified status report')
        totals, counts = Counter(), Counter()
        for row in documents:
            source(repo, row['path'], row['sha256'])
            need((repo/row['path']).stat().st_size == row['bytes'], 'Page inventory byte count')
            if row['path'] not in page_cache:
                page_cache[row['path']] = len(PdfReader(repo/row['path']).pages)
            need(row['pages'] == page_cache[row['path']], 'Actual PDF page count: ' + row['path'])
            totals[row['kind']] += row['pages']
            counts[row['kind']] += 1
        for key, number in totals.items():
            need(value['totals'][key] == number, 'Page-kind total: ' + key)
        need(value['totals']['all_distinct_documents'] == sum(totals.values()) and
             value['totals']['mathematical_manuscripts_and_guides'] ==
             totals['mathematical_manuscript'] + totals['verification_guide'], 'Distinct current page totals')
        for kind, key in [('mathematical_manuscript','mathematical_manuscripts'),
                          ('verification_guide','verification_guides'),
                          ('research_status_report','research_status_reports')]:
            need(value['document_counts'][key] == counts[kind], 'Distinct document counts')
        need((repo/'data'/name).read_bytes() == (repo/'site/dist/downloads'/name).read_bytes(),
             'Download page inventory mirror')


def check_properties(repo, metadata_only):
    sys.path.insert(0, str(repo/'site'))
    from build_ring_properties import SOURCES, derive
    index = read(repo/'site/dist/data/ring_properties.json')
    flags = read(repo/'site/dist/data/ring_property_flags.json')
    need(index['source_sha256'] == flags['source_sha256'], 'Property index/flags bindings')
    need(set(index['records']) == set(flags['records']), 'Property flag coverage')
    seen = set()
    computed = set()
    for name in SOURCES:
        path = repo/'site/dist/data'/name
        need(index['source_sha256'][name] == sha(path), 'Property source binding: ' + name)
        value = read(path)
        for row in value.get('records', value.get('cases', [])):
            rid = row['id']
            tensor = row.get('fusion_tensor', row.get('tensor'))
            need(tensor is not None and rid in index['records'], 'Property tensor coverage: ' + rid)
            digest = hashlib.sha256(json.dumps(tensor, separators=(',',':')).encode()).hexdigest()
            entry = index['records'][rid]
            need(entry['tensor_sha256'] == digest, 'Property exact tensor digest: ' + rid)
            need(set(entry['properties']) == PROPERTIES and
                 all(isinstance(v,bool) for v in entry['properties'].values()), 'Complete boolean flags: ' + rid)
            need(flags['records'][rid] ==
                 {'tensor_sha256':digest, 'properties':entry['properties']}, 'Exact flags projection: ' + rid)
            if row.get('tensor_sha256'):
                need(row['tensor_sha256'] == digest, 'Profile tensor source digest: ' + rid)
            if not metadata_only and rid not in computed:
                expected = derive(tensor)
                need(entry['properties'] == expected['properties'] and
                     entry['certificate'] == expected['certificate'], 'Exact ring properties: ' + rid)
                computed.add(rid)
            seen.add(rid)
    need(seen == set(index['records']), 'No omitted or orphaned property records')
    return len(seen)


def main(metadata_only=False, repo=ROOT):
    repo = Path(repo).resolve()
    rank9 = check_inherited(repo)
    check_acceptance(repo)
    partition = validate_ledger(repo)
    need(len(read(repo/EXACT_LEDGER)) == 3527 and partition['remaining_ids'] == R8_REMAINING,
         'Complete exact-multiplicity-three projection')
    check_profiles(repo, rank9)
    check_documents(repo)
    count = check_properties(repo, metadata_only)
    result = {'status':'METADATA_PASS' if metadata_only else 'PASS',
              'date':DATE, 'new_general_exclusions':1, 'new_models':0,
              'unresolved':6, 'exact_property_records':count,
              'scope':'Immutable mathematical dependencies, one rank-eight transition, current documents and profiles; full census and finite categorical proof replay are separate.'}
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--repo', type=Path, default=ROOT)
    args = parser.parse_args()
    main(args.metadata_only, args.repo)

