"""Exact R721 necessary modular-data completion; not a fusion category.

Run with --output PATH to save the complete fusion tensor and S/T data.
Otherwise prints the compact verification receipt. All algebra is exact.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'evidence/rank8_frontier_20261021/noncommutative'
FOLLOW=ROOT/'evidence/rank8_center_followup_20261021'
sys.path.insert(0,str(OLD))
import central_support as c
import character_modular as md
import rotation_search as base
from twist_balancing import rref,need
s=c.s

def prepare():
    base.install()
    source=next(r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text()) if r['id']=='R8_3_721')
    need(source['tensor_sha256']=='76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5','source tensor identity')
    R=source['tensor'];a=c.w.data(R);K=a['K'];cols=a['lows'][10];chs=md.characters(R,a)
    high=md.full.base.grams.high_columns(a,s.Matrix.hstack(*map(s.Matrix,cols)))[1]
    rc=json.loads((FOLLOW/'r721_center_extension_receipt.json').read_text())['case_results'][7]
    witness=next(w for w in rc['witnesses'] if w['matching_size']==2)
    Ns=[s.eye(22)]+[s.Matrix(v)for v in witness['matrices']]
    types=[i for i,n in enumerate(rc['counts'])for _ in range(n)]
    columns=list(cols)+[(0,)+tuple(high[t][0])for t in types]
    dimensions=[md.value(chs[0],v,K)for v in columns]
    groups=[[j]for j in range(5)]+[[5+j for j,t in enumerate(types)if t==k]for k in sorted(set(types))]
    U=s.zeros(22,9)
    for j,g in enumerate(groups):
        for k in g:U[k,j]=1
    Ui=(U.T*U).inv()*U.T;small=[Ui*N*U for N in Ns[1:]]
    perm=rc['permutation'];inv=[perm.index(i)for i in range(5)]
    S0=[[K.zero for j in range(22)]for i in range(22)]
    for group in groups:
        j=group[0]
        lam=[md.value(chs[inv[i]],columns[j],K)*a['D']/a['codegrees'][inv[i]]/K(a['multiplicities'][inv[i]])/dimensions[j]for i in range(1,5)]
        equations=[]
        for M,li in zip(small,lam):
            for r in range(9):equations.append([K(M[r,t])-(li if r==t else K.zero)for t in range(9)]+[K.zero])
        equations.append([K(int(t==0))for t in range(9)]+[dimensions[j]])
        reduced,pivots=rref(equations,K);need(pivots==list(range(9)),'unique cyclic S projection')
        vec=[row[-1]for row in reduced]
        for col in group:
            for k,gg in enumerate(groups):
                for row in gg:S0[row][col]=vec[k]
    need(all(S0[i][j]==S0[j][i]for i in range(22)for j in range(22)),'symmetric cyclic S')
    Q=[];vectors=[]
    for name in ('A','C'):
        e=[];projector=s.zeros(22)
        for u,v in witness[name+'_matching']:
            q=s.zeros(22,1);q[rc[name+'_labels'][u]]=1;q[rc[name+'_labels'][v]]=-1
            e.append(q);projector+=q*q.T/2
        Q.append(projector);vectors.append(e)
    va=s.zeros(22,1);vc=s.zeros(22,1)
    for pos in range(4):
        va[rc['A_labels'][pos]]=s.Rational(1,2)*(1 if pos<2 else -1)
        vc[rc['C_labels'][pos]]=s.Rational(1,2)*(1 if pos<2 else -1)
    return source,R,a,S0,columns,Ns,Q,vectors,va,vc

def main():
    source,R,a,S0,columns,Ns,Q,vectors,va,vc=prepare()
    x=s.Symbol('x');L=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(17,x),x));zeta=L.unit
    qr={k*k%17 for k in range(1,17)}
    rad=L.one+2*sum((zeta**k for k in qr),L.zero)
    need(rad**2==L(17),'quadratic Gauss sum')
    convert=lambda v:sum((L(co)*(21+5*rad)**i for i,co in enumerate(reversed(v.to_list()))),L.zero)
    D=convert(a['D']);ss=[[convert(S0[i][j])/D for j in range(22)]for i in range(22)]
    tw=[zeta**(3*l*l%17)for l in range(1,9)]
    leg=lambda k:1 if k%17 in qr else -1
    sigma=lambda v,k:sum((L(co)*zeta**((i*k)%17)for i,co in enumerate(reversed(v.to_list()))),L.zero)
    # Galois symmetry reduces the D block to B_lm=Legendre(lm)*sigma_lm(b).
    # Unit-D STS determines b in the 8-dimensional real cyclotomic field.
    constant=sum((ss[0][k]*ss[k][14]*(L(-1)if 5<=k<=8 else L.one)for k in range(10)),L.zero)
    basis=[L.one]+[zeta**j+zeta**(17-j)for j in range(1,8)]
    equations=[]
    for j in range(1,9):
        coefficients=[ss[0][14]*sum((tw[l-1]*L(leg(l*j))*sigma(v,l*j)for l in range(1,9)),L.zero)for v in basis]
        target=ss[0][14]/tw[j-1]-constant
        vectors17=[([s.Rational(str(t))for t in v.to_list()][::-1]+[s.Rational(0)]*16)[:16]for v in coefficients+[target]]
        equations.extend([[v[k]for v in vectors17]for k in range(16)])
    reduced,pivots=s.Matrix(equations).rref()
    need(pivots==tuple(range(8)),'unique D-block Galois solution')
    b=sum((L(co)*v for co,v in zip(list(reduced[:8,-1]),basis)),L.zero)
    need(b==-(zeta**6+zeta**11)/rad,'negative cosine D block')
    B=[[L(leg(l*j))*sigma(b,l*j)for j in range(1,9)]for l in range(1,9)]
    need(all(B[l-1][j-1]==-(zeta**(6*l*j%17)+zeta**(-6*l*j%17))/rad for l in range(1,9)for j in range(1,9)),'cosine formula for entire D block')
    results=[];artifacts=[]
    for ctype in (1,):
        e=vectors[1]
        CC=(-e[0]*e[0].T+e[1]*e[1].T)/2 if ctype==0 else -(e[0]*e[1].T+e[1]*e[0].T)/2
        correction=-Q[0]+va*vc.T+vc*va.T+CC
        S=[[ss[i][j]+L(correction[i,j])for j in range(22)]for i in range(22)]
        for i in range(8):
            for j in range(8):S[14+i][14+j]=B[i][j]
        need(all(S[i][j]==S[j][i]for i in range(22)for j in range(22)),'full S symmetric')
        need(all(sum((S[i][k]*S[k][j]for k in range(22)),L.zero)==L(int(i==j))for i in range(22)for j in range(22)),'full S squared identity')
        # Work in Q(zeta17)[u]/(u^4+1); u is a primitive eighth root.
        cexp=[0,4,2,6]if ctype==0 else[1,5,3,7]
        texp=[0]*5+[4]*4+[0]+cexp+[0]*8
        t17=[L.one]*14+tw
        def reduce_u(exponent,coefficient):
            exponent%=8
            return exponent%4, coefficient if exponent<4 else -coefficient
        for i in range(22):
            for j in range(22):
                lhs=[L.zero]*4
                for k in range(22):
                    at,value=reduce_u(texp[k],S[i][k]*S[k][j]*t17[k]);lhs[at]+=value
                at,value=reduce_u(-texp[i]-texp[j],S[i][j]/t17[i]/t17[j])
                lhs[at]-=value
                need(all(v==L.zero for v in lhs),'full STS relation: case='+str(ctype)+', entry='+str((i,j))+', residual='+str(lhs))
        fusion=[[[0]*22 for _ in range(22)]for _ in range(22)]
        for i,j,k in itertools.combinations_with_replacement(range(22),3):
            value=sum((S[i][l]*S[j][l]*S[k][l]/S[0][l]for l in range(22)),L.zero)
            coefficients=value.to_list()
            need(len(coefficients)<=1 and(not coefficients or(coefficients[0].denominator==1 and coefficients[0]>=0)),'all Verlinde coefficients nonnegative integral')
            v=int(coefficients[0])if coefficients else 0
            for ii,jj,kk in set(itertools.permutations((i,j,k))):fusion[ii][jj][kk]=v
        need(all(fusion[0][i][j]==int(i==j)for i in range(22)for j in range(22)),'fusion unit and selfduality')
        need(all(fusion[i][j][k]==int(Ns[i][k,j])for i in range(1,5)for j in range(22)for k in range(22)),'all four prescribed distinguished actions')
        # Associativity follows exactly from the orthogonal Verlinde diagonalization.
        # Verify the forgetful map for every pair and all eight source coordinates.
        for i in range(22):
            for j in range(22):
                for k in range(8):
                    lhs=sum(fusion[i][j][t]*columns[t][k]for t in range(22))
                    rhs=sum(columns[i][u]*columns[j][v]*R[u][v][k]for u in range(8)for v in range(8))
                    need(lhs==rhs,'full fusion restriction homomorphism')
        payload=json.dumps(fusion,separators=(',',':')).encode()
        record=dict(name='C_fourth_roots'if ctype==0 else'C_primitive_eighth_roots',
                    center_rank=22,twist_order=68 if ctype==0 else 136,
                    tensor_sha256=hashlib.sha256(payload).hexdigest(),maximum_fusion_coefficient=max(v for a in fusion for b in a for v in b),
                    unordered_Verlinde_triples=2024,full_STS_entries=484,forgetful_product_coordinates=3872,
                    symmetric_S=True,S_squared_identity=True,nonnegative_integral_Verlinde=True,
                    exact_associativity_by_Verlinde_diagonalization=True,full_source_restriction_homomorphism=True)
        results.append(record)
        artifacts.append(dict(**record,S_coefficients_ascending=[[[str(t)for t in v.to_list()[::-1]]for v in row]for row in S],
                              S_field='Q(zeta17), zeta17^16+...+zeta17+1=0',
                              T_exponents_mod_136=[17*t for t in texp[:14]]+[(8*3*l*l)%136 for l in range(1,9)],
                              fusion_tensor=fusion,restriction_columns=columns))
    if '--output' in sys.argv:
        destination=Path(sys.argv[sys.argv.index('--output')+1]);destination.write_text(json.dumps(artifacts,indent=2)+'\n')
    print(json.dumps(dict(ring='R8_3_721',source_tensor_sha256=source['tensor_sha256'],
          scope='Explicit necessary modular-data and based-ring candidates; no associator, braided category, or categorification is constructed.',
          normalized_D_block='-(zeta17^(6*l*m)+zeta17^(-6*l*m))/sqrt(17)',
          D_twists='zeta17^(3*l^2), l=1,...,8',results=results),indent=2))

if __name__=='__main__':main()
