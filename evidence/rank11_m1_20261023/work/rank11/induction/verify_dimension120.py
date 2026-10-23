"""Exact finite hypotheses of the dimension-120 structural obstruction.

No restriction-frame search is used. Categorical implications are proved in
criteria_audit/D120_THEORY.md; this replay checks their tensor hypotheses.
"""
from pathlib import Path
import sys,json,itertools,collections
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from common import read,sha,dual,validate,require,dump

def verify(rid):
    T=read()[rid];validate(T);n=len(T);du=dual(T)
    c=json.load(open(HERE/(rid+'_reciprocity.json')))
    require(c['tensor_sha256']==sha(T),'source identity')
    x=s.Symbol('x');p=s.Poly.from_list(list(map(s.Rational,c['field_polynomial'])),x)
    require(p.is_irreducible,'character field is a field')
    K=s.QQ.algebraic_field(s.CRootOf(p,0))
    rows=[[K.new([s.QQ(a) for a in z]) for z in row] for row in c['characters']]
    require(len(rows)==n and len({tuple(tuple(v.to_list())for v in r)for r in rows})==n,'complete distinct character table')
    for r in rows:
        require(r[0]==K.one,'unit character')
        for i,j in itertools.product(range(n),repeat=2):
            require(r[i]*r[j]==sum((K(T[i][j][k])*r[k]for k in range(n)),K.zero),'character product')
    positive=[r for r in rows if all(len(v.to_list())==1 and v.to_list()[0]>0 and s.denom(v.to_list()[0])==1 for v in r)]
    require(len(positive)==1,'positive dimension character')
    ds=[int(v.to_list()[0])for v in positive[0]];D=sum(d*d for d in ds)
    require(D==120 and sorted(ds)==[1,1,2,3,3,4,4,4,4,4,4],'dimension type')
    g=[i for i,d in enumerate(ds) if d==1 and i!=0][0]
    require(T[g][g][0]==1,'involution')
    fs=[sum((r[i]*r[du[i]] for i in range(n)),K.zero)for r in rows]
    bs=[K(D)/f for f in fs]
    require(all(len(b.to_list())==1 and s.denom(b.to_list()[0])==1 for b in bs),'central integer dimensions')
    beta=[int(b.to_list()[0])for b in bs]
    require(sorted(beta)==[1,2,2,8,8,8,8,8,15,30,30],'complete induction dimensions')
    require(all(r[g]==K.one for r,b in zip(rows,beta)if b==2),'two central dimensions centralize one another')
    B=[[sum(T[a][j][k]*T[k][du[a]][i]for a in range(n)for k in range(n))for j in range(n)]for i in range(n)]
    require(B[0][0]==n and B[g][g]==11,'induction Gram bound')
    perm=[]
    for i in range(n):
        require(sum(T[g][i])==1,'invertible action')
        perm.append(T[g][i].index(1))
    require(all(perm[perm[i]]==i for i in range(n)),'order-two action')
    seen=set();orbits=[];quotient_dimensions=[]
    for i in range(n):
        if i in seen:continue
        o=sorted({i,perm[i]});seen.update(o);orbits.append(o)
        if len(o)==2:quotient_dimensions.append(ds[i])
        else:
            require(ds[i]%2==0,'fixed object dimension halves integrally')
            quotient_dimensions.extend([ds[i]//2]*2)
    require(sorted(quotient_dimensions)==[1]*3+[2]*12+[3],'de-equivariantization dimensions')
    small=[i for i,d in enumerate(ds)if d<4]
    require(len(small)==5 and sum(ds[i]**2 for i in small)==24,'small subcategory dimension')
    require(all(not T[i][j][k]for i in small for j in small for k in range(n)if k not in small),'small subcategory closed')
    # R40 has Rep(S4) fusion rules; R82 has a dual-pair variant. What the
    # proof needs is only the closed subcategory and its quotient dimensions.
    small_quotient=[]
    for o in orbits:
        if o[0] not in small:continue
        require(all(i in small for i in o),'small subcategory action')
        small_quotient.extend([ds[o[0]]]if len(o)==2 else[ds[o[0]]//2]*2)
    require(sorted(small_quotient)==[1,1,1,3],'neutral near-group subcategory')
    return dict(id=rid,tensor_sha256=sha(T),passed=True,dimensions=ds,global_dimension=D,
                formal_codegrees=sorted(D//b for b in beta),central_dimensions=sorted(beta),
                involution=g,involution_orbits=orbits,induction_gram_diagonal=B[g][g],
                small_subcategory=small,small_deequivariant_dimensions=sorted(small_quotient),
                deequivariant_dimensions=sorted(quotient_dimensions),
                neutral_dimension=12,neutral_rank=4,actual_rank=16,forced_rank=20,
                proof='criteria_audit/D120_THEORY.md')

if __name__=='__main__':
    rows=[verify(rid)for rid in ['R11_1_40','R11_1_82']]
    dump(HERE/'dimension120_verified.json',dict(records=rows))
    print('PASS: exact dimension-120 structural hypotheses for both rings')
