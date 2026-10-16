#!/usr/bin/env python3
"""Replay every local census record and the general signed-cover proof.

Default: regenerate and verify the complete signed cover, then replay the full
1692-record ledger. --ledger-only checks every ledger witness but assumes the
recorded full-cover completeness; it is explicitly not fresh-cover verification.
"""
from pathlib import Path
from collections import Counter
import argparse, json, subprocess, sys, time
from classify import (ROOT, CENSUS, RESULTS, inputs, make_record, summarize, digest,
                      STAGES, KIND_STAGE)
from rings import (canonical, sd_tensor, ns_tensor, permute, PERMS, dual, validate)
from rapid import check_dnumber, check_cyclotomic
from applications import check_rank_two
from dispatch import check
from signed import Search
from exact import require


def check_record(row, certificate, models, search):
    R = row['tensor']; validate(R)
    require(certificate['census_id'] == row['id'] and
            certificate['canonical_sha256'] == row['canonical_sha256'], 'ledger/input identity')
    require(certificate['tag'] == row['tag'] and certificate['multiplicity'] == row['multiplicity'],
            'ledger metadata mismatch')
    c = certificate['certificate']; kind = c['kind']; stage = certificate['stage']
    if kind == 'rank_two_moment':
        require(stage == 'rank_two', 'rank-two stage'); check_rank_two(R, c)
    elif kind == 'dnumber':
        require(stage == 'formal_codegree_dnumber', 'd-number stage'); check_dnumber(R, c)
    elif kind == 'cyclotomic':
        require(stage == 'cyclotomicity', 'cyclotomic stage'); check_cyclotomic(R, c)
    elif kind == 'model':
        require(stage == 'model' and tuple(c['basis']) in PERMS, 'model stage/basis')
        found = [m for m in models if m['model'] == c['model']]
        require(len(found) == 1 and permute(R, c['basis']) == found[0]['matrices'], 'model identity')
    elif kind == 'outside_nonselfdual_candidates':
        require(stage == 'nonselfdual' and sum(i == j for i, j in enumerate(dual(R))) == 2,
                'non-self-dual theorem hypothesis')
        candidates = [m['matrices'] for m in models if dual(m['matrices']) != [0,1,2,3]]
        require(len(candidates) == 6, 'non-self-dual model list')
        candidates.append(ns_tensor((0,0,0,1,2,2)))
        require(all(canonical(R) != canonical(A) for A in candidates),
                'ring is one of the seven candidates')
    elif kind == 'nonselfdual_quadratic':
        m = c['m']
        require(stage == 'nonselfdual' and type(m) is int and m >= 2 and tuple(c['basis']) in PERMS,
                'quadratic non-self-dual hypotheses')
        require(permute(R,c['basis']) == ns_tensor((0,0,0,1,m,m)), 'quadratic non-self-dual tensor')
        # From Theorem finite:thm:nonselfdual-quadratic, 3L-2dD =
        # 4m+(2m^2-8)d > 0, with d>0 and m>=2.
        require(4*m > 0 and 2*m*m-8 >= 0, 'strict moment gap')
    elif kind == 'general_witness':
        require(tuple(c['basis']) in PERMS and row['tag'] == 'S', 'general witness basis/type')
        T = sd_tensor(c['tuple'])
        require(permute(R, c['basis']) == T, 'witness is for another ring')
        require(KIND_STAGE[c['proof']['kind']] == stage, 'witness/stage mismatch')
        check(T, c['proof'], models, search)
    else:
        raise ValueError('unknown ledger certificate kind: '+str(kind))
    require(certificate['status'] == ('realized' if stage == 'model' else 'excluded'), 'unproved status')


def run(ledger_only=False, engine='cpp'):
    started = time.monotonic()
    if not ledger_only:
        subprocess.run([sys.executable, str(ROOT/'verify_compact.py'), '--engine', engine], check=True)
    compact = json.loads((ROOT/'verification/compact_summary.json').read_text())
    require(compact['unresolved'] == 0 and compact['positive_catalog_coverage'], 'signed proof incomplete')
    require(compact['certificate_sha256'] == digest(ROOT/'data/positive_certificates.jsonl.gz'),
            'stale signed witness report')
    if ledger_only:
        print('EXPLICIT ASSUMPTION: ledger-only mode uses the recorded signed-cover completeness.', flush=True)
    else:
        require(compact['global_catalog_regenerated_in_this_run'], 'fresh signed cover required')
    census, manifest, models, by_model, bank = inputs()
    ledger = [json.loads(l) for l in (RESULTS/'certificates.jsonl').read_text().splitlines()]
    require(len(ledger) == len(census) == manifest['number_of_rings'], 'ledger/census coverage')
    search = Search(engine)
    for row, record in zip(census, ledger):
        require(record == make_record(row, by_model, bank), 'ledger/order differs from deterministic pipeline')
        check_record(row, record, models, search)
    expected = summarize(ledger, manifest)
    summary = json.loads((RESULTS/'summary.json').read_text())
    require({k:summary[k] for k in expected} == expected, 'summary counts or identities differ')
    require(summary['ledger_sha256'] == digest(RESULTS/'certificates.jsonl'), 'ledger hash mismatch')
    surviving = [r for r in ledger if r['stage'] == 'model']
    require(surviving == json.loads((RESULTS/'survivors.json').read_text()), 'survivor file mismatch')
    require({r['certificate']['model'] for r in surviving} == {m['model'] for m in models},
            'not all fifteen models occur exactly once')
    report = {'all_checks_passed': True, 'checked_rings': len(ledger), 'excluded': len(ledger)-len(surviving),
              'models': len(surviving), 'unresolved': 0, 'strict_dimension_bound': 1000,
              'census_sha256': digest(CENSUS/'rings.jsonl'), 'ledger_sha256': digest(RESULTS/'certificates.jsonl'),
              'fresh_signed_cover_in_this_run': not ledger_only,
              'signed_checked_records': compact['checked_records'], 'local_search_engine': engine,
              'nonselfdual_inputs': manifest['type_counts']['N'],
              'nonselfdual_scope': 'Checks exact hypotheses of the independently proved non-self-dual reduction and S(2) obstruction; does not formalize their categorical proofs.',
              'elapsed_seconds': round(time.monotonic()-started,3)}
    (RESULTS/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger-only', action='store_true')
    parser.add_argument('--engine', choices=['cpp','python'], default='cpp')
    args = parser.parse_args(); run(args.ledger_only, args.engine)
