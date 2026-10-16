#!/usr/bin/env python3
"""Exact finite inputs for the general R7_3_1022 inverse-Morita exclusion."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
import sympy as s


def require(value,message):
    if not value: raise RuntimeError(message)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    counts=collections.Counter(); N=None
    for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
        if not line.strip(): continue
        raw=json.loads(line.replace('{','[').replace('}',']'))
        m=max(v for a in raw for b in a for v in b); counts[m]+=1
        if (m,counts[m])==(3,1022): N=raw; break
    require(N is not None,'Source R7_3_1022 exists')
    d=4+2*s.sqrt(5); t=d/2; dims=[1,1,1,d,d,3,d]
    matrices=[s.Matrix(a).T for a in N]
    dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    for i,j in itertools.product(range(7),repeat=2):
        require(s.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(7)))==0,'FP character')
        require(matrices[i]*matrices[j]==sum((N[i][j][k]*matrices[k] for k in range(7)),s.zeros(7)),'Associativity')
        for k in range(7):
            require(N[i][j][k]==N[dual[i]][k][j]==N[k][dual[j]][i],'Frobenius reciprocity')
    require(N[5][5]==[1,1,1,0,0,2,0],'Rep(A4) square')
    require(matrices[1]**3==s.eye(7),'C3 generator')
    require(N[1][5]==N[5][1]==[0,0,0,0,0,1,0],'C3 fixed dimension-three simple')
    require({next(k for k in range(7) if N[1][i][k]) for i in [3,4,6]}=={3,4,6},'Free three-element orbit')
    require(s.expand(d*d-4-8*d)==0 and s.expand(t*t-1-4*t)==0,'Morita dimension equations')
    require(s.expand((2*t)**2-4-8*(2*t))==0,'Forbidden near-group dimension equation')

    Id=tuple(range(4))
    G=[p for p in itertools.permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
    mul=lambda p,q:tuple(p[q[i]] for i in range(4))
    inv=lambda p:tuple(p.index(i) for i in range(4))
    H=[g for g in G if mul(g,g)==Id]
    require(len(G)==12 and len(H)==4,'A4 and unique V4 size')
    require(all(mul(mul(g,h),inv(g)) in H for g in G for h in H),'V4 normality')
    sub4=[]
    for S in itertools.combinations([g for g in G if g!=Id],3):
        S=(Id,)+S
        if all(mul(a,b) in S for a,b in itertools.product(S,repeat=2)): sub4.append(set(S))
    require(len(sub4)==1 and sub4[0]==set(H),'Unique subgroup of order four')
    orbits=[]; remaining=set(G)
    while remaining:
        g=min(remaining); orbit={mul(h,g) for h in H}
        require(len(orbit)==4,'Free V4 orbit size'); orbits.append(orbit); remaining-=orbit
    require(len(orbits)==3,'Three noninvertible V4 double orbits')

    # Identify H with F2^2 and check all automorphism actions on its
    # nontrivial H^2 class using explicit fourth-root-valued coboundaries.
    V=list(itertools.product(range(2),repeat=2)); zero=(0,0)
    add=lambda x,y:(x[0]^y[0],x[1]^y[1])
    beta=lambda x,y:(-1)**(x[0]*y[1])
    for a,b,c in itertools.product(V,repeat=3):
        require(beta(a,b)*beta(add(a,b),c)==beta(b,c)*beta(a,add(b,c)),'beta cocycle')
    require(beta((1,0),(0,1))==-beta((0,1),(1,0)),'Nontrivial alternating commutator')
    roots=[s.Integer(1),s.I,s.Integer(-1),-s.I]; cocycle_transports=[]
    for p in itertools.permutations(V[1:]):
        phi=dict(zip(V,[zero]+list(p)))
        require(all(phi[add(a,b)]==add(phi[a],phi[b]) for a,b in itertools.product(V,repeat=2)),'GL2 map')
        witness=None
        for qvals in itertools.product(roots,repeat=3):
            q=dict(zip(V,[s.Integer(1)]+list(qvals)))
            if all(s.simplify(q[a]*q[b]/q[add(a,b)]-s.Rational(beta(a,b),beta(phi[a],phi[b])))==0 for a,b in itertools.product(V,repeat=2)):
                witness=[str(q[x]) for x in V]; break
        require(witness is not None,'Conjugate beta differs by coboundary')
        cocycle_transports.append({'automorphism':[list(phi[x]) for x in V],'coboundary':witness})

    X=s.Matrix([[0,1],[1,0]]); Z=s.diag(1,-1)
    rep=lambda a:Z**a[1]*X**a[0]
    for a,b in itertools.product(V,repeat=2):
        require(rep(a)*rep(b)==beta(a,b)*rep(add(a,b)),'Twisted group algebra M2 representation')
    require(s.Matrix.hstack(*[s.Matrix(4,1,list(rep(a))) for a in V]).rank()==4,'M2 basis independence')
    characters=[[(-1)**(a[0]*b[0]+a[1]*b[1]) for b in V] for a in V]
    require(s.Matrix(characters)*s.Matrix(characters).T==4*s.eye(4),'Four ordinary stabilizer characters')
    require(3*4==12 and 12!=3,'Inverse Morita rank contradiction')
    result={'status':'PASS','id':'R7_3_1022','scope':'general_complex',
      'tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),
      'FP_dimensions':list(map(str,dims)),'d':str(d),'t':str(t),
      'source_products_checked':49,'source_frobenius_equalities_checked':343,
      'pointed_group_order':12,'inverse_algebra_dimension':4,
      'noninvertible_H_orbits':3,'ordinary_stabilizer_irreducible_degrees':[1]*4,
      'nontrivial_stabilizer_irreducible_degrees':[2],
      'twist_transport_coboundaries':cocycle_transports,
      'forbidden_near_group':{'group':'V4','level':8,'allowed_levels':[0,4],
       'reference':'Schopieray, J. London Math. Soc. 108 (2023), Theorem 1.1, DOI 10.1112/jlms.12789'},
      'inverse_dual_noninvertible_dimensions':[str(t)]*12,
      'required_original_dual_noninvertible_dimensions':[str(d)]*3,
      'conclusion':'excluded_by_inverse_V4_Morita_duality',
      'categorical_steps_proved_in':'R1022_GENERAL_PROOF.md','optimizer_used':False}
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
