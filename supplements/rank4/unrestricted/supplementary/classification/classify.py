#!/usr/bin/env python3
"""Produce a complete general-case certificate ledger for the local D<1000 census.

The census is generated locally, not imported from the pivotal package.
Rank-two and universal arithmetic witnesses are found afresh. Later self-dual
stages reuse the supplied exact witness bank (not its status fields). The
separate verifier checks each witness and its basis identification.
"""
from pathlib import Path
from collections import Counter
import argparse, gzip, hashlib, json, sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'software'))
from rings import canonical, sd_tensor, ns_tensor, PERMS, permute, dual, codegree_factors
from rapid import cyclotomic_failure
from exact import require

CENSUS = ROOT.parent / 'census/data'
RESULTS = ROOT / 'results'
STAGES = [
    ('rank_two', 'Rank-two subring obstruction'),
    ('formal_codegree_dnumber', r'Formal-codegree $d$-numbers'),
    ('cyclotomicity', 'Character cyclotomicity'),
    ('nonselfdual', 'Non-self-dual reduction'),
    ('dimension_reduction', 'Two-dimension and weak-integral reductions'),
    ('subring', 'Subring dimension divisibility'),
    ('involution_moments', 'Involution moment obstructions'),
    ('automatic_spherical', 'Automatic sphericality and spherical tests'),
    ('signed', 'Signed characters and central induction'),
]
KIND_STAGE = {'rank_two_moment': 'rank_two', 'two_dimensions': 'dimension_reduction',
              'weak_integral': 'dimension_reduction', 'subring': 'subring',
              'diagonal_involution_moments': 'involution_moments',
              'involution_propagation_42': 'involution_moments',
              'automatic_spherical': 'automatic_spherical', 'signed': 'signed', 'model': 'model'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def dnumber(R):
    """Choose a reproducible witness independently of factorization backend.

    Every factor is exact and irreducible. Sorting its integer coefficient
    tuple fixes the first failed divisibility when several witnesses exist.
    """
    factors=sorted((tuple(map(int,p.all_coeffs())) for p,m in codegree_factors(R)))
    for co in factors:
        degree=len(co)-1;norm=abs(co[-1])
        require(norm>0,'zero formal codegree')
        for j in range(1,degree+1):
            if pow(co[j],degree,norm**j):
                return {'kind':'dnumber','factor':list(map(str,co)),'j':j}
    return None


def rank_two_witness(R):
    for i in range(1, 4):
        a = R[i][i][i]
        if a >= 2 and R[i][i] == [int(j == 0) + a*int(j == i) for j in range(4)]:
            return {'kind': 'rank_two_moment', 'object': i, 'a': a}
    return None


def basis_to(R, target):
    for p in PERMS:
        if permute(R, p) == target:
            return list(p)
    raise ValueError('claimed based-ring identification does not exist')


def inputs():
    census = [json.loads(l) for l in (CENSUS / 'rings.jsonl').read_text().splitlines()]
    manifest = json.loads((CENSUS / 'manifest.json').read_text())
    require(manifest['dimension_exclusive_bound'] == 1000 and manifest['maximum_multiplicity'] == 31,
            'incorrect census scope')
    require(digest(CENSUS/'rings.jsonl') == manifest['sha256']['rings.jsonl'], 'census identity')
    models = json.loads((ROOT / 'data/models.json').read_text())
    by_model = {canonical(m['matrices']): m for m in models}
    require(len(by_model) == 15, 'model distinctness')
    with gzip.open(ROOT / 'data/positive_certificates.jsonl.gz', 'rt') as f:
        header = json.loads(next(f))
        bank = {}
        for line in f:
            row = json.loads(line)
            key = canonical(sd_tensor(row['tuple']))
            require(key not in bank, 'duplicate witness-bank input')
            bank[key] = row
    require(header['bound'] == 31 and len(bank) == header['records'], 'witness-bank coverage')
    return census, manifest, models, by_model, bank


def make_record(row, by_model, bank):
    R = row['tensor']; key = canonical(R)
    proof = rank_two_witness(R)
    if proof is not None:
        stage = 'rank_two'
    elif (proof := dnumber(R)) is not None:
        stage = 'formal_codegree_dnumber'
    elif (proof := cyclotomic_failure(R)) is not None:
        stage = 'cyclotomicity'
    elif key in by_model:
        model = by_model[key]
        stage = 'model'
        proof = {'kind': 'model', 'model': model['model'], 'basis': basis_to(R, model['matrices'])}
    elif row['tag'] == 'N':
        # The seven candidates are supplied by Larson only after the manuscript's
        # automatic-sphericality and Galois-pseudo-unitary reduction.
        extra = ns_tensor((0, 0, 0, 1, 2, 2))
        stage = 'nonselfdual'
        if key == canonical(extra):
            proof = {'kind': 'nonselfdual_quadratic', 'm': 2, 'basis': basis_to(R, extra)}
        else:
            proof = {'kind': 'outside_nonselfdual_candidates'}
    else:
        require(row['tag'] == 'S' and key in bank, 'self-dual survivor missing from witness bank')
        witness = bank[key]
        kind = witness['certificate']['kind']
        require(kind in KIND_STAGE and kind != 'model', 'unexpected witness kind')
        stage = KIND_STAGE[kind]
        # A basis isomorphism is explicit; no source index or status proves anything.
        proof = {'kind': 'general_witness', 'basis': basis_to(R, sd_tensor(witness['tuple'])),
                 'tuple': witness['tuple'], 'proof': witness['certificate']}
    return {'census_id': row['id'], 'canonical_sha256': row['canonical_sha256'],
            'tag': row['tag'], 'multiplicity': row['multiplicity'], 'stage': stage,
            'status': 'realized' if stage == 'model' else 'excluded', 'certificate': proof}


def summarize(records, manifest):
    counts = Counter(r['stage'] for r in records)
    remaining = len(records); stages = []
    for key, title in STAGES:
        remaining -= counts[key]
        stages.append({'filter': key, 'title': title, 'excluded': counts[key], 'remaining': remaining})
    require(remaining == counts['model'] == 15, 'incomplete classification ledger')
    return {'rank': 4, 'dimension_exclusive_bound': 1000, 'maximum_multiplicity': 31,
            'census_count': len(records), 'type_counts': manifest['type_counts'],
            'stages': stages, 'model_count': remaining, 'excluded': len(records)-remaining,
            'unresolved': 0, 'census_sha256': digest(CENSUS/'rings.jsonl'),
            'witness_bank_sha256': digest(ROOT/'data/positive_certificates.jsonl.gz'),
            'interpretation': 'Ordered, mutually exclusive recorded rejection stages. Later stages replay supplied mathematical witnesses. These counts do not assert that every possible earlier obstruction was found.'}


def run(output=RESULTS):
    census, manifest, models, by_model, bank = inputs()
    records = [make_record(row, by_model, bank) for row in census]
    output.mkdir(parents=True, exist_ok=True)
    (output / 'certificates.jsonl').write_text(''.join(encode(r)+'\n' for r in records))
    summary = summarize(records, manifest)
    summary['ledger_sha256'] = digest(output/'certificates.jsonl')
    (output / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (output / 'survivors.json').write_text(json.dumps([r for r in records if r['stage']=='model'], indent=2)+'\n')
    print(json.dumps(summary, indent=2), flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=RESULTS)
    run(parser.parse_args().output)
