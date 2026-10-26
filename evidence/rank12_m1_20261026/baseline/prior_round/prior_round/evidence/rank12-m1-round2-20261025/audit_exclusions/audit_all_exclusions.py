"""Independent complete coverage of all 393 first-round excluded input IDs."""
from itertools import product
from collections import Counter
from fractions import Fraction
import hashlib,json,time
import sympy as s
import independent_audit as a
from liptrap_independent import check as liptrap

def val(n,p):
    n=abs(int(n));a.require(n>0,'nonzero norm');v=0
    while n%p==0:v+=1;n//=p
    return v

def rank8_spherical(R):
    n=len(R);N=list(map(s.Matrix,R));t=a.t;du=a.dual(R)
    a.require(all(A*B==B*A for A in N for B in N),'rank8 source commutative')
    H=N[0]+sum((2**(i-1)*N[i]for i in range(1,n)),s.zeros(n))
    p=H.charpoly(t).as_poly();a.require(s.gcd(p,p.diff()).degree()==0,'all characters separated')
    V=s.Matrix.hstack(*[(H**i)[0,:].T for i in range(n)])
    co=[V.inv()*N[i][0,:].T for i in range(n)]
    a.require(all(N[i]==sum((co[i][j]*H**j for j in range(n)),s.zeros(n))for i in range(n)),'complete character coordinates')
    required=a.casimir(R).charpoly(t).as_poly().factor_list()[1];out=[]
    for f,m in p.factor_list()[1]:
        K=s.QQ.alg_field_from_poly(f);ds=[K(s.Poly.from_list(list(reversed(list(v))),t).rem(f).all_coeffs())for v in co]
        a.require(ds[0]==K.one and all(sum((K(R[i][j][k])*ds[k]for k in range(n)),K.zero)==ds[i]*ds[j]for i,j in product(range(n),repeat=2)),'all rank8 character products')
        if any(not d for d in ds):why='zero dimension'
        elif any(ds[i]!=ds[du[i]]for i in range(n)):why='unequal dual dimensions'
        else:
            D=sum((ds[i]*ds[du[i]]for i in range(n)),K.zero);u=K([1,0]);deg=f.degree()
            def col(v):
                c=list(reversed(v.to_list()));return s.Matrix(c+[0]*(deg-len(c)))
            norm=s.Matrix.hstack(*(col(D*u**j)for j in range(deg))).det();a.require(norm.q==1,'global dimension norm integer')
            witnesses=[(q,int(prime))for q,m in required for prime,power in s.factorint(abs(int(q.TC()))).items()if val(norm,prime)*q.degree()<int(power)*deg]
            a.require(bool(witnesses),'global norm contradiction in each remaining spherical orbit')
            q,prime=witnesses[0];why=dict(norm=str(norm),required_codegree=list(map(str,q.all_coeffs())),prime=prime)
        out.append(dict(character_field=list(map(str,f.all_coeffs())),obstruction=why))
    return out

def main():
    start=time.monotonic();accepted=a.main();data=json.loads((a.BASE/'tensors.json').read_text());proofs={};receipts=[]
    sub=json.loads((a.BASE/'subrings.json').read_text())
    for i,r in enumerate(sub['classes']):
        if r['certificate']:a.arithmetic(r['tensor'],r['certificate']);proofs[i]='independent arithmetic'
    for r in json.loads((a.BASE/'feudal.json').read_text())['records']:
        if r['certificate']:receipts.append(dict(id=r['id'],route='Liptrap',details=liptrap(data[r['id']],r['certificate'])));accepted.add(r['id'])
    for r in json.loads((a.BASE/'lower_known.json').read_text())['class_proofs']:
        R=sub['classes'][r['class_index']]['tensor'];c=r['certificate'];kind=c['kind']
        if kind=='liptrap_complex_obstruction':detail=liptrap(R,c)
        elif kind.startswith('central_dimension'):
            du=a.dual(R);G=[i for i in range(len(R))if sum(R[i][du[i]])==1];X=[i for i in range(len(R))if i not in G]
            n0=len(G);n1=len(X)
            field=dict(field_polynomial=c['field_polynomial'],dimensions_in_field=[['1']if i in G else[str(s.Rational(1,n1)),str(-s.Rational(n0,n1))]for i in range(len(R))])
            a.central(R,field,c);detail='independent quadratic field/order proof'
        elif kind=='frozen_rank8_signed_proof':detail=rank8_spherical(R)
        else:raise ValueError(kind)
        proofs[r['class_index']]=r['known_source_id'];receipts.append(dict(id=r['known_source_id'],route=kind,details=detail))
    embeddings=0
    for r in sub['records']:
        R=data[r['id']];du=a.dual(R)
        for E in r['subrings']:
            J=E['subset'];p=E['source_to_class_basis_map'];C=sub['classes'][E['class_index']]['tensor'];n=len(J)
            a.require(0 in J and J[0]==0 and 1<n<12 and p[0]==0 and sorted(p)==list(range(n)),'proper unit-preserving based embedding')
            a.require(all(du[j]in J for j in J),'dual-closed subcategory')
            a.require(all(not R[i][j][k]for i,j in product(J,repeat=2)for k in range(12)if k not in J),'product-closed subcategory')
            a.require(all(R[J[i]][J[j]][J[k]]==C[p[i]][p[j]][p[k]]for i,j,k in product(range(n),repeat=3)),'entire embedded tensor')
            embeddings+=1
            if E['class_index']in proofs:accepted.add(r['id'])
    expected={r['id']for r in json.loads((a.BASE/'ledger.json').read_text())['records']if r['status']=='excluded'}
    a.require(accepted==expected and len(accepted)==393,'independent coverage of every first-round excluded input and no modeled/unresolved input')
    out=dict(status='PASS',first_round_exclusions=393,independently_covered_ids=sorted(accepted,key=lambda v:int(v.rsplit('_',1)[1])),closed_subring_embeddings=embeddings,
             lower_rank_and_liptrap_receipts=receipts,scope='Arbitrary complex fusion categorification; categorical hypotheses reviewed in findings.md.',elapsed_seconds=time.monotonic()-start)
    (a.HERE/'all_exclusions_independent.json').write_text(json.dumps(out,indent=2)+'\n');print('ALL393 PASS; embeddings',embeddings,'seconds',out['elapsed_seconds'])

if __name__=='__main__':main()
