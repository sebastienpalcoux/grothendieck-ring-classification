"""Complete joint Galois spectrum tests for the remaining quadratic NC cases."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import central_integral_filters as filters
import integral_gram
v=filters.v;c=v.c;need=c.require


def record(number):
    v.modular.full.base.install()
    row=next(r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())if r['id']==f'R8_3_{number}')
    R=row['tensor'];a=c.w.data(R);K=a['K'];need(a['factor'].degree()==2,'quadratic scalar field')
    chs=v.modular.characters(R,a);need(chs[0]==a['ds'],'tensor unit is explicit FP character')
    if number==721:
        p=FRONTIER/'noncommutative/integral_gram_721_rotations.json';saved=json.loads(p.read_text());cols=a['lows'][saved['low_index']]
        domain,meta=integral_gram.completions(a,cols);patterns=[tuple(x['multiplicities'])for x in saved['cases']]
        need(domain==sorted(patterns)and len(patterns)==4,'complete four-pattern integer Gram enumeration')
        indices=list(range(4));dependencies=[p]
    else:
        p=FRONTIER/'central_integrality/integer_gram_1154.json';saved=json.loads(p.read_text());cols=a['lows'][saved['low_index']]
        need([list(x)for x in cols]==saved['low_columns'],'bound low restriction domain')
        f=FRONTIER/'noncommutative/central_integral_filters_1154.json';accepted=json.loads(f.read_text());indices=accepted['combined_survivor_indices']
        need(len(saved['completions'])==14211 and len(indices)==1238,'complete prior Gram/cubic/spectral domain')
        patterns=[saved['completions'][i]for i in indices];dependencies=[p,f]
    need(saved['tensor_sha256']==row['tensor_sha256'],'tensor hash binding')
    _,high=v.modular.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))
    if number==1154:need([list(x)for x,z in high]==saved['high_columns'],'bound complete high vectors')
    allcols=[tuple(x)for x in cols]+[(0,)+tuple(x)for x,z in high];values=[]
    for col in allcols:
        d=sum((K(x)*y for x,y in zip(col,a['ds'])),K.zero)
        values.append(tuple(tuple(filters.coordinates(a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*v.modular.value(ch,col,K)/d))for E,ch in enumerate(chs)))
    coefficient=int(a['factor'].all_coeffs()[1]);conjugate=lambda t:tuple((-x,y-coefficient*x)for x,y in t)
    cases=[]
    for index,pattern in zip(indices,patterns):
        need(len(pattern)==len(high),'complete integer multiplicity length')
        counts=Counter()
        for t,m in zip(values,[1]*5+list(pattern)):counts[t]+=m
        bad=next((t for t in sorted(counts)if counts[t]!=counts[conjugate(t)]),None)
        failure=None if bad is None else{'tuple':[list(map(str,z))for z in bad],
            'conjugate_tuple':[list(map(str,z))for z in conjugate(bad)],'multiplicity':counts[bad],'conjugate_multiplicity':counts[conjugate(bad)]}
        cases.append({'pattern_index':index,'passes':failure is None,'first_exact_failure':failure})
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],'minimal_polynomial':str(a['factor'].as_expr()),
        'coordinate_convention':'(coefficient of alpha, rational constant), alpha is the saved quadratic field generator',
        'low_columns':[list(x)for x in cols],'high_columns':[list(x)for x,z in high],
        'low_high_joint_eigenvalue_tuples':[[list(map(str,z))for z in t]for t in values],
        'matrix_character_divisor':2,'complete_input_pattern_count':len(patterns),'cases':cases,
        'surviving_indices':[r['pattern_index']for r in cases if r['passes']],
        'dependencies_sha256':{str(p.relative_to(FRONTIER)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dependencies},
        'scope':'complete joint spectra of distinguished commuting integral fusion matrices in the center; necessary general-complex condition after the independently verified Galois-pseudo-unitary gate'}


def run(write):
    out={'kind':'complete_quadratic_noncommutative_joint_Galois_spectra','records':[record(n)for n in(721,1154)]};path=HERE/'results.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==json.loads(path.read_text()),'complete quadratic joint-spectrum receipt')
    for r in out['records']:print(r['id'],'joint Galois survivors',len(r['surviving_indices']),'/',r['complete_input_pattern_count'],flush=True)
    print('PASS quadratic noncommutative joint spectra',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');run(p.parse_args().write)
