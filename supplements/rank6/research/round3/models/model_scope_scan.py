#!/usr/bin/env python3
"""Exact residual/model and theorem-scope audit; never changes a ledger."""
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'software'))
from rings import casimir
from new_module_spectral import perron_factor
from exact import pc, require
from existence import REGISTRIES
from positive_models import quadratic

spec = importlib.util.spec_from_file_location('nrw_scan', ROOT / 'research/m8_frontier/nrw_rank6_scan.py')
nrw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nrw)

def iso(source, target):
    for tail in itertools.permutations(range(1, 6)):
        p = (0,) + tail
        if all(source[p[i]][p[j]][p[k]] == target[i][j][k]
               for i in range(6) for j in range(6) for k in range(6)):
            return list(p)
    return None

def run():
    census = json.loads((ROOT / 'data/census.json').read_text())
    residuals = json.loads((ROOT / 'data/unresolved_tensors.json').read_text())
    source_records = nrw.tensors(ROOT / 'research/m8_frontier/NsdGOL6.g')
    source_keys = {nrw.canonical(r['N']) for r in source_records}
    positive = []
    for registry in REGISTRIES:
        positive.extend(json.loads((ROOT / f'data/{registry}.json').read_text()))
    positive_keys = {nrw.canonical(r['N']) for r in positive}
    rows = []
    for r in residuals:
        factors = [f for f,m in casimir(r['N']).charpoly().as_poly().factor_list()[1]]
        which, interval = perron_factor(factors)
        pD = factors[which]
        can = nrw.canonical(r['N'])
        rows.append({'id': r['id'], 'global_FPdim_minpoly': [str(c) for c in pD.all_coeffs()],
                     'global_FPdim_degree': pD.degree(),
                     'weakly_integral_scope_eligible': pD.degree() == 1,
                     'NRW_modular_tensor_match': can in source_keys,
                     'existing_positive_tensor_match': can in positive_keys})
        print(r['id'], pD.degree(), flush=True)
    named = []
    for name,N in [('R(2,2)',quadratic(2,2)), ('R(4,4)',quadratic(4,4)),
                   ("Rprime(4)",quadratic(4,4,True))]:
        hist = nrw.histogram(N)
        hits = []
        for r in census:
            if nrw.histogram(r['N']) != hist:
                continue
            p = iso(N,r['N'])
            if p is not None:
                hits.append({'id': r['id'], 'basis_permutation': p})
        require(len(hits) == 1, 'Meng-Yu family match must be unique')
        named.append({'source_family': name, 'matches': hits})
    return {'input_residual_count': len(residuals),
            'input_residual_SHA256': hashlib.sha256((ROOT/'data/unresolved_tensors.json').read_bytes()).hexdigest(),
            'scope': 'model matching and eligibility only; no new categorical decision',
            'NRW_source': nrw.SOURCE_URL, 'NRW_source_SHA256': nrw.SOURCE_SHA256,
            'NRW_tensor_records': len(source_records), 'NRW_distinct_rings': len(source_keys),
            'positive_constructor_records': len(positive), 'positive_distinct_rings': len(positive_keys),
            'Meng_Yu_open_families_as_of_arxiv2608_06064v1': named,
            'residuals': rows}

if __name__ == '__main__':
    result = run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('residuals',)}))
