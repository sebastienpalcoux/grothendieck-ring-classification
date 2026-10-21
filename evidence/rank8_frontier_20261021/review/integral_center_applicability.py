#!/usr/bin/env python3
"""Exact applicability table for the two-prime integral-center criterion."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
SCALAR=REPO/'evidence/rank8_m3_20261021/noncommutative/scalar_sieve.py'
sys.path.insert(0,str(SCALAR.parent))
from scalar_sieve import ScalarCharacters,t
from integral_center_subcategory import closure

def need(x,m):
    if not x:raise ValueError(m)

def enc(x):return list(map(str,x))

def compute():
    source=REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    rows={r['id']:r for r in json.loads(source.read_text())};records=[]
    witnesses={439:[1],455:[97,1800,35640],567:[1],721:[1],
               928:[11,630,36900],941:[11,630,36900],1154:[1]}
    for ident,w in witnesses.items():
        row=rows[f'R8_3_{ident}'];R=row['tensor']
        need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==row['tensor_sha256'],'source hash')
        a=ScalarCharacters(R);f,K,ds,D,pD,embedding=a.fp();d=f.degree()
        coords=[]
        for x in ds:
            c=[F(str(z))for z in reversed(x.to_list())];c += [F(0)]*(d-len(c));coords.append(c)
        integrals=[i for i,c in enumerate(coords)if not any(c[1:])]
        need(all(coords[i][0].denominator==1 for i in integrals),'rational source dimensions integral')
        need(len(w)==d-1,'functional dimension')
        dots=[sum(x*y for x,y in zip(w,c[1:]))for c in coords]
        need(all(v==0 if i in integrals else v>0 for i,v in enumerate(dots)),'exact positive radical functional')
        need(closure(R,integrals)==integrals and all(a.du[i]in integrals for i in integrals),'integral source fusion subcategory')
        inv=[i for i in range(8)if sum(R[i][a.du[i]])==1]
        central=[i for i in inv if all(R[i][j]==R[j][i]for j in range(8))]
        ad=closure(R,{k for i in range(8)for k,c in enumerate(R[i][a.du[i]])if c})
        components=[];unseen=set(range(8))
        while unseen:
            seed=min(unseen);component={seed}
            while True:
                new=component|{k for i in ad for j in component for k,c in enumerate(R[i][j])if c}
                if new==component:break
                component=new
            need(component<=unseen,'disjoint adjoint components')
            components.append(sorted(component));unseen-=component
        need(components[0]==ad,'neutral adjoint component')
        if len(components)==1 and central==[0]:center_gate='proved_trivial'
        elif len(components)==1 and len(central)==2:center_gate='not_determined; possible orders 1 or 2'
        elif len(components)==2 and central==[0]:
            label={i:k for k,comp in enumerate(components)for i in comp}
            need(all(not R[i][j][k]or label[k]==(label[i]^label[j])
                     for i,j,k in itertools.product(range(8),repeat=3)),'complete faithful C2 universal grading')
            center_gate='proved_nontrivial; order 2 from Aut_tensor(Id)=Hom(C2,C*)'
        else:raise ValueError('unexpected center gate case')
        need(pD.is_irreducible and pD.LC()==1,'minimal global dimension polynomial')
        e=pD.degree();normD=abs(int((-1)**e*pD.TC()))
        # The independent regular matrix of D^2 in Q[D] checks the actual
        # degree and norm of the center dimension, without a field-degree assumption.
        M=s.Matrix(e,e,lambda i,j:s.rem(s.Poly(t**(j+2),t),pD).nth(i))
        pCenter=M.charpoly(t).as_poly()
        need(pCenter.is_irreducible,'center dimension generates the same field')
        normCenter=abs(int((-1)**e*pCenter.TC()))
        need(normCenter==normD**2,'norm of squared dimension')
        primes=sorted(map(int,s.factorint(normCenter)))
        applies=center_gate=='proved_trivial'and len(primes)<=2
        records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],
            'FP_character_field_polynomial':enc(f.all_coeffs()),
            'FP_dimensions_ascending_power_basis':[enc(c)for c in coords],
            'positive_functional_on_nonconstant_power_coefficients':w,
            'exact_functional_values':enc(dots),'integral_source_labels':integrals,
            'source_invertibles':inv,'ring_central_invertibles':central,
            'adjoint_labels':ad,'universal_grading_components':components,
            'center_invertible_gate':center_gate,
            'global_FP_dimension_polynomial':enc(pD.all_coeffs()),'global_FP_dimension_norm':normD,
            'center_FP_dimension_polynomial':enc(pCenter.all_coeffs()),'center_FP_dimension_norm':normCenter,
            'center_norm_prime_factorization':{str(p):int(v)for p,v in s.factorint(normCenter).items()},
            'two_prime_norm_gate':len(primes)<=2,'integral_center_subcategory_fusion_closure_proved':True,
            'integral_center_subcategory_is_Vec_proved':applies,
            'integral_subcategory_dimension_divides':normD if applies and e==2 else None})
    need([r['id']for r in records if r['integral_center_subcategory_is_Vec_proved']]==
         ['R8_3_439','R8_3_567','R8_3_721'],'exact applicability set')
    paths=[source,SCALAR,HERE/'integral_center_subcategory.py',HERE/'INTEGRAL_CENTER_SUBCATEGORY.md']
    return {'kind':'exact_seven_noncommutative_integral_center_applicability',
            'source_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},
            'records':records,'scope':'necessary integral-center constraints only; no additional categorification decision'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    result=compute();path=HERE/'integral_center_applicability.json'
    if a.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'applicability receipt mismatch')
    print('PASS: exact all-seven NC applicability; no integral central simples for439,567,721 only, with all gates explicit.')
