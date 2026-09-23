"""Tensor constructors for positive models, independent of census labels."""
import itertools,json
from pathlib import Path
import sympy as s
from exact import require
from oriented_signed import validate_general
from prepare import key
P=Path(__file__).resolve().parents[1]

def product(A,B):
    a,b=len(A),len(B)
    return [[[A[i//b][j//b][k//b]*B[i%b][j%b][k%b] for k in range(a*b)] for j in range(a*b)] for i in range(a*b)]
def cyclic(n):return [[[int((i+j)%n==k) for k in range(n)] for j in range(n)] for i in range(n)]
def rank2(m):return [[[1,0],[0,1]],[[0,1],[1,m]]]
def ng2(m):
    return [[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,m]]]
def su2(level,even=False):
    basis=list(range(0,level+1,2 if even else 1))
    return [[[int(abs(i-j)<=k<=min(i+j,2*level-i-j) and (i+j+k)%2==0) for k in basis] for j in basis] for i in basis]
def quadratic(m,n,nonselfdual=False):
    R=[[[0]*6 for j in range(6)] for i in range(6)]
    for i,j in itertools.product(range(4),repeat=2):R[i][j][i^j]=1
    for g in range(4):
        for i in (4,5):R[g][i][4+((i-4)^(g&1))]=R[i][g][4+((i-4)^(g&1))]=1
    for i,j in itertools.product((4,5),repeat=2):
        diff=(i!=j)^nonselfdual;R[i][j][int(diff)]=R[i][j][2+int(diff)]=1
        R[i][j][4]=m if i==j else n;R[i][j][5]=n if i==j else m
    return R

def tt3():
    text=[['1 2f s b r u','f b','f s b u','f s b r','f s'],
          ['f s','1 r','f','b u','b'],
          ['f s b r','s u','f b','1 f u','f'],
          ['f s b u','f','1 f r','f s','b r'],
          ['f b','s','s r','f','1 u']]
    names={'1':0,'f':1,'r':2,'s':3,'b':4,'u':5};R=[[[0]*6 for j in range(6)] for i in range(6)]
    for i in range(6):R[0][i][i]=R[i][0][i]=1
    for i,j in itertools.product(range(5),repeat=2):
        for token in text[i][j].split():
            c=int(token[:-1]) if len(token)>1 else 1;R[i+1][j+1][names[token[-1]]]+=c
    return R

def f36():
    """Characters of (C3 x C3) semidirect C4, rotation (x,y)->(-y,x)."""
    V=list(itertools.product(range(3),repeat=2));els=[(v,k) for k in range(4) for v in V]
    def rot(v):return (-v[1]%3,v[0])
    seen={(0,0)};orbits=[]
    for v in V:
        if v in seen:continue
        orb=[];w=v
        for k in range(4):orb.append(w);w=rot(w)
        seen.update(orb);orbits.append(orb)
    # Nonzero character orbits contain their negatives, hence their values are integers.
    chars=[[s.I**(j*k) for v,k in els] for j in range(4)]
    for orb in orbits:
        vals=[]
        for v,k in els:
            if k:vals.append(s.Integer(0));continue
            c0=sum((a*v[0]+b*v[1])%3==0 for a,b in orb);vals.append(s.Rational(3*c0-4,2))
        chars.append(vals)
    R=[]
    for a in chars:
        mat=[]
        for b in chars:
            row=[]
            for c in chars:
                x=s.simplify(sum((u*v*s.conjugate(w) for u,v,w in zip(a,b,c)),s.Integer(0))/36)
                require(x.is_Integer and x>=0,'nonintegral character product');row.append(int(x))
            mat.append(row)
        R.append(mat)
    return R

def zest_c2(R,g):
    """Central order-two zesting of D x Vec(C2); tensor order (X,a)."""
    n=len(R);out=[[[0]*(2*n) for j in range(2*n)] for i in range(2*n)]
    action=[next(k for k,v in enumerate(R[i][g]) if v) for i in range(n)]
    require(all(sum(R[i][g])==1 for i in range(n)), 'zesting object not invertible')
    for i,j in itertools.product(range(2*n),repeat=2):
        x,a=divmod(i,2);y,b=divmod(j,2)
        for k,c in enumerate(R[x][y]):out[i][j][2*(action[k] if a*b else k)+(a^b)]+=c
    return out

def check_fermionic_cochain():
    for a,b,c,d in itertools.product(range(2),repeat=4):
        exponent=b*c*d+a*(b^c)*d+a*b*c-(a^b)*c*d-a*b*(c^d)
        require(exponent%4==(2*a*b*c*d)%4,'zesting pentagon scalar failed')
    return True

def examples():
    for name,A in [('VecC2',rank2(0)),('Fib',rank2(1))]:
        for nameB,B in [('VecC3',cyclic(3)),('Ising',ng2(0)),('RepS3',ng2(1)),('AdE6',ng2(2)),('PSU2_5',su2(5,True))]:
            yield name+' x '+nameB,product(A,B),'Deligne products; rank-two and rank-three unitary models'
    check_fermionic_cochain()
    yield 'Fermionic C2-zesting of AdE6 x VecC2',zest_c2(ng2(2),1),'Central-fermion lemma and associative zesting theorem in this manuscript'
    yield 'TT3',tt3(),'Edie-Michell arXiv:1904.08909, Definition 2.5'
    for m,n in [(0,0),(0,1),(0,2),(4,6)]:yield f'R({m},{n})',quadratic(m,n),'Meng-Yu arXiv:2608.06064v1, Proposition 5.1'
    for m in [0,2]:yield f"Rprime({m})",quadratic(m,m,True),'Meng-Yu arXiv:2608.06064v1, Lemma 5.2 and Corollary 5.8'
    yield 'Rep((C3 x C3) semidirect C4)',f36(),'Explicit finite-group character computation'

if __name__=='__main__':
    rows=json.load(open(P/'data/census.json'));idx={key(r['N']):r['id'] for r in rows};out=[]
    for name,R,ref in examples():
        validate_general(R);rid=idx.get(key(R));print(name,rid,flush=True);require(rid is not None,'constructed model not in census');out.append({'name':name,'id':rid,'N':R,'reference':ref})
    (P/'data/constructed_positive_models.json').write_text(json.dumps(out,separators=(',',':')))
