"""Additional positive models reconstructed independently of the census.
Character tables are checked against an explicitly constructed finite group.
ADE products are computed from graph/induction formulas stated in the paper.
"""
import itertools,json,math
from pathlib import Path
import sympy as s
from exact import require
from prepare import key
from oriented_signed import validate_general
from positive_models import su2,check_fermionic_cochain
P=Path(__file__).resolve().parents[1]

def e6_graph():
    n=6;X=s.zeros(n)
    for i,j in [(0,1),(1,2),(2,3),(3,4),(2,5)]:X[i,j]=X[j,i]=1
    powers=[X**j for j in range(n)];V=s.Matrix.vstack(*(A[0,:] for A in powers));require(V.det()!=0,'E6 graph unit not cyclic');co=V.inv()
    mats=[sum((co[i,j]*powers[j] for j in range(n)),s.zeros(n)) for i in range(n)]
    require(all(v.q==1 and v>=0 for A in mats for v in A),'E6 graph coefficients')
    R=[[[int(v) for v in row] for row in A.tolist()] for A in mats];validate_general(R);return R

def graded_fermionic_zest(R,g,degree):
    n=len(R);require(len(degree)==n and degree[0]==degree[g]==0,'bad grading');require(R[g][g]==[1]+[0]*(n-1),'not an involution')
    for i,j,k in itertools.product(range(n),repeat=3):
        if R[i][j][k]:require(degree[k]==degree[i]^degree[j],'not a C2 grading')
    action=[row.index(1) for row in R[g]]
    require(all(sum(row)==1 for row in R[g]),'zesting object not invertible');check_fermionic_cochain()
    out=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i,j,k in itertools.product(range(n),repeat=3):out[i][j][action[k] if degree[i]*degree[j] else k]+=R[i][j][k]
    validate_general(out);return out

def d_even(level,even=False):
    """C(SU2,level)_{1+V_level}; level divisible by 8.
    The two fixed-point summands are self-dual in this congruence class.
    """
    require(level>0 and level%8==0,'self-dual D-type congruence');m=level//2;n=m+2;SU=su2(level);R=[[[0]*n for _ in range(n)] for _ in range(n)]
    alpha,beta=m,m+1
    def ind(j):
        if j==m:return [(alpha,1),(beta,1)]
        return [(min(j,level-j),1)]
    for i,j in itertools.product(range(m),repeat=2):
        for k,c in enumerate(SU[i][j]):
            for a,z in ind(k):R[i][j][a]+=c*z
    for i in range(m):
        total=[0]*n
        for j,c in enumerate(SU[i][m]):
            for a,z in ind(j):total[a]+=c*z
        require(all(total[j]%2==0 for j in range(m)),'unsplittable free coefficient')
        for j in range(m):
            R[i][alpha][j]=R[alpha][i][j]=R[i][beta][j]=R[beta][i][j]=total[j]//2
        eig=0 if i%2 else (-1)**(i//2)
        require((total[alpha]+eig)%2==0,'fixed coefficient parity')
        aa=(total[alpha]+eig)//2;bb=(total[alpha]-eig)//2
        for a in [alpha,beta]:
            R[i][a][a]=R[a][i][a]=aa;other=alpha+beta-a;R[i][a][other]=R[a][i][other]=bb
    for i in range(m):
        R[alpha][alpha][i]=R[beta][beta][i]=R[i][alpha][alpha]
        R[alpha][beta][i]=R[beta][alpha][i]=R[i][alpha][beta]
    R[alpha][alpha][alpha]=R[beta][beta][beta]=1
    validate_general(R)
    if even:
        ix=list(range(0,m,2))+[alpha,beta];R=[[[R[i][j][k] for k in ix] for j in ix] for i in ix];validate_general(R)
    return R

def gl3f2_group():
    def rows(x):return [(x>>(3*i))&7 for i in range(3)]
    def rk(x):
        a=rows(x);r=0
        for k in range(3):
            z=next((j for j in range(r,3) if a[j]&(1<<k)),None)
            if z is None:continue
            a[r],a[z]=a[z],a[r]
            for j in range(3):
                if j!=r and a[j]&(1<<k):a[j]^=a[r]
            r+=1
        return r
    G=[273]+[x for x in range(512) if x!=273 and rk(x)==3];idx={x:i for i,x in enumerate(G)};require(len(G)==168,'wrong GL3F2 order')
    def mul(x,y):
        a,b=rows(x),rows(y);return sum((sum(((a[i]>>k)&1)*((b[k]>>j)&1) for k in range(3))%2)<<(3*i+j) for i in range(3) for j in range(3))
    return [[idx[mul(x,y)] for y in G] for x in G]

def psl2_7():
    M=gl3f2_group();n=len(M);inv=[next(j for j in range(n) if M[i][j]==0) for i in range(n)];left=set(range(n));classes=[]
    def order(x):
        a=x;k=1
        while a!=0:a=M[a][x];k+=1
        return k
    while left:
        x=min(left);cl=sorted({M[M[h][x]][inv[h]] for h in range(n)});classes.append(cl);left-=set(cl)
    classes.sort(key=lambda c:(order(c[0]),c[0]));sizes=list(map(len,classes));require(sizes==[1,21,56,42,24,24],'unexpected conjugacy classes');which={x:i for i,c in enumerate(classes) for x in c};C=[]
    for A in classes:
        mat=[]
        for B in classes:
            counts=[0]*6
            for x in A:
                for y in B:counts[which[M[x][y]]]+=1
            require(all(counts[j]%sizes[j]==0 for j in range(6)),'class convolution');mat.append([counts[j]//sizes[j] for j in range(6)])
        C.append(mat)
    z=s.Symbol('z');K=s.QQ.alg_field_from_poly(s.Poly(z*z+7,z),alias='sqrt_minus7');w=K.unit;a=(-K.one+w)/K(2);b=(-K.one-w)/K(2)
    chars=[[K(v) for v in row] for row in [[1,1,1,1,1,1],[3,-1,0,1,0,0],[3,-1,0,1,0,0],[6,2,0,0,-1,-1],[7,-1,1,-1,0,0],[8,0,-1,0,1,1]]]
    chars[1][4:]=[a,b];chars[2][4:]=[b,a];du=[0,2,1,3,4,5]
    # The class algebra has exactly six distinct one-dimensional characters.
    # This verifies the table as actual irreducible group characters, not just
    # an orthogonal array with convenient multiplication coefficients.
    for chi in chars:
        lam=[K(sizes[i])*chi[i]/chi[0] for i in range(6)]
        for i,j in itertools.product(range(6),repeat=2):require(lam[i]*lam[j]==sum((K(C[i][j][k])*lam[k] for k in range(6)),K.zero),'class-algebra character mismatch')
    for i,j in itertools.product(range(6),repeat=2):require(sum((K(sz)*chars[i][k]*chars[du[j]][k] for k,sz in enumerate(sizes)),K.zero)==K(n*int(i==j)),'group character orthogonality')
    R=[]
    for i in range(6):
        mat=[]
        for j in range(6):
            row=[]
            for k in range(6):
                v=sum((K(sz)*chars[i][l]*chars[j][l]*chars[du[k]][l] for l,sz in enumerate(sizes)),K.zero)/K(n);co=v.to_list();require(len(co)<=1 and (not co or co[0].denominator==1 and co[0]>=0),'character product integrality');row.append(int(co[0]) if co else 0)
            mat.append(row)
        R.append(mat)
    validate_general(R);return R

def izumi_dual(n=5):
    """Evans--Gannon Theorem 7, for the existing Izumi C5 subfactor.
    Basis: unit, a, b_1,...,b_r,c_1,...,c_r; indices identify i and -i.
    """
    require(n==5,'only the cited n=5 construction is allocated');h=(n-1)//2;r=n+1
    R=[[[0]*r for _ in range(r)] for _ in range(r)];bs=list(range(2,2+h));cs=list(range(2+h,r))
    def at(i,which):
        j=min(i%n,(-i)%n)
        return None if j==0 else (bs if which=='b' else cs)[j-1]
    for i in range(r):R[0][i][i]=R[i][0][i]=1
    common=[0,1]+[1]*(2*h)
    R[1][1]=[1]*r
    for i in range(1,h+1):
        bi=at(i,'b');ci=at(i,'c');v=common[:];v[bi]-=1;R[1][bi]=R[bi][1]=v[:]
        v=common[:];v[ci]+=1;R[1][ci]=R[ci][1]=v[:]
        for j in range(1,h+1):
            bj=at(j,'b');cj=at(j,'c');R[bi][cj]=R[cj][bi]=common[:]
            v=common[:];v[0]=int(i==j);v[1]=int(i!=j)
            for t in (i+j,i-j):
                k=at(t,'b')
                if k is not None:v[k]-=1
            R[bi][bj]=v
            v=common[:];v[0]=int(i==j);v[1]=1+int(i==j)
            for t in (i+j,i-j):
                k=at(t,'c')
                if k is not None:v[k]+=1
            R[ci][cj]=v
    validate_general(R);return R

def examples():
    yield 'Commutative even part of the Izumi C5 subfactor',izumi_dual(),'Izumi C5 existence; Evans--Gannon Theorem 7; Grossman--Snyder Section 6.6'
    E=e6_graph()
    yield 'E6 module category of SU(2)_10',E,'Connected commutative E6 algebra 1+V6; E6 graph algebra reconstruction'
    yield 'Fermionic grading zest of E6',graded_fermionic_zest(E,4,[0,1,0,1,0,1]),'Central image of V10 and the unitary fermionic C2-zesting theorem'
    yield 'D6 module category of SU(2)_8',d_even(8),'Simple-current commutative algebra 1+V8; resolved D6 fusion rules'
    yield 'Even D10 category from SU(2)_16',d_even(16,True),'Local modules over 1+V16; resolved even D10 fusion rules'
    yield 'Rep(GL(3,F2)) = Rep(PSL(2,7))',psl2_7(),'Explicit 168-element matrix group and verified class-algebra character table'

if __name__=='__main__':
    rows=json.load(open(P/'data/census.json'));index={key(r['N']):r['id'] for r in rows};out=[]
    for name,R,ref in examples():
        rid=index.get(key(R));require(rid is not None,'new model outside census');print(name,rid,flush=True);out.append({'name':name,'id':rid,'N':R,'reference':ref})
    (P/'data/additional_positive_models.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
