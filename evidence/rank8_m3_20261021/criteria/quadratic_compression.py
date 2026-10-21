"""Exact multiquadratic full-I(1) compression consequences.

Proof: evidence/theoretical_20261016/compression/full_I1_compression.tex.
The regular Casimir multiplicities already include the square of each
representation degree. Sphericalization divides the known-sector norm by4.
"""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json,math,sys
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software')]
from exact import require
from rings import Characters

def squareclass_rank(values):
    primes=sorted({int(p) for q in values for p in s.factorint(q)})
    pivots={}
    for q in values:
        v=sum(1<<i for i,p in enumerate(primes) if s.factorint(q).get(p,0)%2)
        while v:
            i=v.bit_length()-1
            if i in pivots:v^=pivots[i]
            else:pivots[i]=v;break
    return len(pivots)

def discover(R):
    n=len(R);B=sum((s.Matrix(M)*s.Matrix(M).T for M in R),s.zeros(n));factors=B.charpoly().as_poly().factor_list()[1]
    fields={};factor_rows=[]
    for f,m in factors:
        coefficients=list(map(int,f.all_coeffs()));factor_rows.append({'coefficients':coefficients,'multiplicity':m})
        if f.degree()!=2:continue
        a,b,c=coefficients;require(a==1,'nonmonic Casimir factor');disc=b*b-4*c
        require(disc>0,'Casimir spectrum not real');q=math.prod(int(p) for p,e in s.factorint(disc).items() if e%2)
        conductor=q if q%4==1 else 4*q
        fields.setdefault(q,{'conductor':conductor,'ratio':Fraction(0),'factors':[]})
        fields[q]['ratio']+=Fraction(conductor*m*disc,c*c);fields[q]['factors'].append({'coefficients':coefficients,'multiplicity':m})
    rank=squareclass_rank(fields)
    if not rank:return None
    rows=[{'radicand':q,'conductor':z['conductor'],'ratio':str(z['ratio']),'factors':z['factors']} for q,z in sorted(fields.items())]
    common={'kind':'quadratic_casimir_compression','factors':factor_rows,'squareclass_rank':rank,'quadratic_fields':rows}
    for q,z in sorted(fields.items()):
        if (2**(rank-1))*z['ratio']>4:
            return dict(common,gate='sphericalization',radicand=q,extension_degree_lower_bound=2**(rank-1),upper_bound=4)
    # Existing general-to-Galois-pseudo-unitary theorem. A pseudo-unitary
    # conjugate is spherical, so the stronger compression bound applies.
    if all(R[i][j]==R[j][i] for i in range(n) for j in range(n)):ch=Characters(R)
    else:
        sys.path.insert(0,str(HERE.parent/'noncommutative'))
        from scalar_sieve import ScalarCharacters
        ch=ScalarCharacters(R)
    f,K,ds,D,pD,embedding=ch.fp()
    gate='weak_integrality' if pD.degree()==1 else 'two_FP_values' if len(set(ds))==2 else None
    if gate:
        for q,z in sorted(fields.items()):
            if 2**(rank-1)*z['ratio']>1:
                return dict(common,gate=gate,radicand=q,extension_degree_lower_bound=2**(rank-1),upper_bound=1)
    return None

def verify(R,c):require(discover(R)==c,'quadratic compression certificate changed or is not an exclusion')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    source=HERE.parent/'pipeline/survivors_m3.json';rows=json.loads(source.read_text());dest=HERE/'quadratic_compression.json'
    if args.verify:
        saved=json.loads(dest.read_text());byid={r['id']:r for r in rows}
        for rec in saved['records']:
            row=byid[rec['id']];require(row['tensor_sha256']==rec['tensor_sha256'],'source hash mismatch');verify(row['tensor'],rec['certificate'])
        print('PASS',len(saved['records']));return
    records=[]
    for row in rows:
        c=discover(row['tensor'])
        if c:
            verify(row['tensor'],c);records.append({'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'general_complex_fusion_category','certificate':c})
    result={'result':'PASS','records':records,'counts':dict((gate,sum(r['certificate']['gate']==gate for r in records)) for gate in sorted({r['certificate']['gate'] for r in records}))}
    dest.write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps({'records':len(records),'counts':result['counts']}))
if __name__=='__main__':main()
