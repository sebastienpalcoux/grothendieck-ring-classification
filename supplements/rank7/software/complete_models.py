"""Complete positive-model registry: every tensor is constructed without a census label.
This module supplements, rather than replaces, the pre-existing constructors.
Existence references and parameters are recorded for every returned model.
"""
import itertools
import sympy as s
from exact import require
from positive_models import cyclic,su2
from oriented_signed import validate_general
from quantum_rank2 import principal

def pointed_s3():
    els=list(itertools.permutations(range(3)));idx={g:i for i,g in enumerate(els)}
    return [[[int(idx[tuple(g[h[a]] for a in range(3))]==k) for k in range(6)] for h in els] for g in els]

def tambara_cyclic(n):
    R=[[[0]*(n+1) for _ in range(n+1)] for _ in range(n+1)]
    for i,j in itertools.product(range(n),repeat=2):R[i][j][(i+j)%n]=1
    for i in range(n):R[i][n][n]=R[n][i][n]=1;R[n][n][i]=1
    return R

def small_ising_zest(cyclic_group,dual_pair):
    """Four dimension-eight rings; the three twists are realized in LPR §4.3."""
    R=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][(i+j)%4 if cyclic_group else i^j]=1
    for g in range(4):
        for x in range(2):R[g][4+x][4+(x^(g&1))]=R[4+x][g][4+(x^(g&1))]=1
    for x,y in itertools.product(range(2),repeat=2):
        a=x^y^int(dual_pair);R[4+x][4+y][a]=R[4+x][4+y][a+2]=1
    return R

def metaplectic5(twisted=False):
    # (1,z,y1,y2,x1,x2), the formulas of LPR Theorem 4.7.
    n=6;R=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i in range(n):R[0][i][i]=R[i][0][i]=1
    R[1][1][0]=1
    for i in [2,3]:R[1][i][i]=R[i][1][i]=1
    for i in [4,5]:R[1][i][9-i]=R[i][1][9-i]=1
    def add(i,j,k,c=1):R[i][j][k]+=c
    for i in [2,3]:
        add(i,i,0);add(i,i,1);add(i,i,5-i)
        for a in [4,5]:
            for b in [4,5]:R[i][a][b]=R[a][i][b]=1
    R[2][3][2]=R[2][3][3]=R[3][2][2]=R[3][2][3]=1
    for a,b in itertools.product([4,5],repeat=2):
        R[a][b][int((a!=b)^bool(twisted))]=1;R[a][b][2]=R[a][b][3]=1
    return R

def generalized_dihedral(moduli):
    A=list(itertools.product(*(range(m) for m in moduli)));zero=A[0]
    neg=lambda x:tuple(-a%m for a,m in zip(x,moduli))
    plus=lambda x,y:tuple((a+b)%m for a,b,m in zip(x,y,moduli))
    representatives=sorted({min(x,neg(x)) for x in A if x!=zero});n=len(representatives)+2
    ix={x:i+2 for i,u in enumerate(representatives) for x in (u,neg(u))}
    R=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i in range(n):R[0][i][i]=R[i][0][i]=1
    R[1][1][0]=1
    for i in range(2,n):R[1][i][i]=R[i][1][i]=1
    for i,u in enumerate(representatives,2):
        for j,v in enumerate(representatives,2):
            for w in [plus(u,v),plus(u,neg(v))]:
                if w==zero:R[i][j][0]+=1;R[i][j][1]+=1
                else:R[i][j][ix[w]]+=1
    return R

def rep_c3_c4():
    els=list(itertools.product(range(3),range(4)))
    chars=[[s.I**(j*k) for v,k in els] for j in range(4)]
    for sign in [1,-1]:chars.append([0 if k%2 else sign**(k//2)*(2 if v==0 else -1) for v,k in els])
    R=[]
    for a in chars:
        mat=[]
        for b in chars:
            row=[]
            for c in chars:
                z=s.simplify(sum(u*v*s.conjugate(w) for u,v,w in zip(a,b,c))/12)
                require(z.is_Integer and z>=0,'invalid induced group character product');row.append(int(z))
            mat.append(row)
        R.append(mat)
    return R

def generalized_haagerup_c3():
    n=3;R=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for a,b in itertools.product(range(n),repeat=2):
        R[a][b][(a+b)%n]=1;R[a][n+b][n+(a+b)%n]=1;R[n+a][b][n+(a-b)%n]=1
        R[n+a][n+b][(a-b)%n]=1
        for c in range(n):R[n+a][n+b][n+c]=1
    return R

def ghj3311_prime():
    # Izumi--Jones--Morrison--Snyder, §5.1, Figure 2; order (1,B,C,C',D,g).
    rows=[
      ['1','B','C','c','D','g'],
      ['B','1 B C c D','B c D','B C D','B C c D g','D'],
      ['C','B c D','1 2C g','B D','B c D','C'],
      ['c','B C D','B D','1 2c g','B C D','c'],
      ['D','B C c D g','B c D','B C D','1 B C c D','B'],
      ['g','D','C','c','B','1']]
    ix={a:i for i,a in enumerate(['1','B','C','c','D','g'])};R=[[[0]*6 for _ in range(6)] for _ in range(6)]
    for i,j in itertools.product(range(6),repeat=2):
        for tok in rows[i][j].split():
            a=tok[-1];coef=int(tok[:-1]) if len(tok)>1 else 1;R[i][j][ix[a]]+=coef
    return R

def examples():
    yield 'Vec(S3)',pointed_s3(),'LPR Theorem 1.1; group multiplication'
    yield 'TY(C5)',tambara_cyclic(5),'Tambara--Yamagami construction; LPR Theorem 1.1'
    for cg,dp in [(True,False),(True,True),(False,True)]:
        yield f'Ising zest G={"C4" if cg else "V4"}, dual_pair={int(dp)}',small_ising_zest(cg,dp),'LPR Sections 4.3 and 4.6; unitary pentagon solutions'
    yield 'Rep(C3 semidirect C4)',rep_c3_c4(),'Induced characters of C3 semidirect C4; LPR Section 3.6'
    for mods,name in [((9,),'Rep(D9)'),((3,3),'Rep((C3 x C3) semidirect C2)')]:yield name,generalized_dihedral(mods),'Generalized dihedral induced-character formula; LPR Section 3.6'
    yield 'SO(5)_2',metaplectic5(),'LPR Theorem 1.1 and Section 4.6'
    yield 'Zested SO(5)_2',metaplectic5(True),'LPR Theorem 4.7 and Section 4.5'
    yield 'Haagerup H3',generalized_haagerup_c3(),'Generalized Haagerup C3 category; LPR Theorem 1.1'
    for level in [10,11]:yield f'PSU(2)_{level}',su2(level,True),'Principal SU(2) even subcategory; LPR Theorem 1.1'
    yield 'GHJ 3311 dual even part',ghj3311_prime(),'Izumi--Jones--Morrison--Snyder, Section 5.1, Figure 2'
    yield 'G2 level 3',principal('G2',3)[0],'Principal unitary WZW category; exact Weyl-character reconstruction'
    from twisted_group_models import twisted_s4
    yield 'Twisted S4 three-double-coset model',twisted_s4()[0],'Three-double-coset realization theorem; explicit fourth-root cochain certificate'

if __name__=='__main__':
    import json,time
    from pathlib import Path
    from prepare import key
    P=Path(__file__).resolve().parents[1];idx={key(r['N']):r for r in json.load(open(P/'data/census.json'))};out=[]
    for name,R,ref in examples():
        validate_general(R);r=idx.get(key(R));require(r is not None,'model outside census');print(name,r['id'],flush=True)
        out.append({'name':name,'id':r['id'],'N':R,'reference':ref})
    (P/'data/complete_positive_models.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
