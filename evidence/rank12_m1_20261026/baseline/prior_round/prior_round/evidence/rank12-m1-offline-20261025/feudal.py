"""Liptrap's established reconstruction: exact phases or C*-contradictions.

Unlike a bounded phase search, a negative certificate is an integer monomial
relation, for every possible nondegenerate bicharacter assignment. Variable
tau is retained for negatives, so no two-lord gauge lemma is extrapolated.
"""
from pathlib import Path
from fractions import Fraction as F
import collections,itertools,json,math,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/literature'))
from gty_liptrap import solve_mod_batch,character_forms
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
from common import require,sha

def setup(R,variable_tau=False):
    n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    S=[i for i in range(n)if sum(R[i][du[i]])==1];M=[i for i in range(n)if i not in S]
    if not M or any(R[i][j][k]for i in M for j in M for k in M):return None
    mul={(a,b):next(k for k in range(n)if R[a][b][k])for a,b in itertools.product(range(n),repeat=2)if a in S or b in S}
    H=[a for a in S if mul[a,M[0]]==M[0]];h=len(H)
    require(all([a for a in S if mul[a,m]==m]==H==[a for a in S if mul[m,a]==m]for m in M),'common stabilizer')
    require(all(not R[i][j][k]for i in M for j in M for k in M),'feudal parity')
    if any(mul[a,b]!=mul[b,a]for a,b in itertools.product(H,repeat=2)):return dict(nonabelian=True,S=S,M=M,H=H)
    keys=[(f,a,b,m)for f in ['chi','upsilon']for a in S if a for b in S if b for m in M]
    if variable_tau:keys += [('tau',m)for m in M]
    ki={k:i for i,k in enumerate(keys)};equations=[];desc=[]
    def add(terms,label):
        row=collections.Counter()
        for a,k in terms:
            if k in ki:row[ki[k]]+=a
        row={k:v for k,v in row.items()if v}
        if row:equations.append(row);desc.append(label)
    for a,b,m in itertools.product(S,S,M):
        terms=[(1,('chi',b,a,du[m])),(-1,('chi',a,b,mul[mul[a,m],b]))]
        if variable_tau:terms += [(-1,('tau',mul[mul[a,m],b])),(-1,('tau',m)),(1,('tau',mul[a,m])),(1,('tau',mul[m,b]))]
        add(terms,['quasisymmetry',a,b,m])
    for a,b,c,m in itertools.product(S,S,S,M):
        add([(1,('upsilon',a,b,m)),(-1,('upsilon',a,b,mul[m,du[c]])),(1,('chi',mul[a,b],c,m)),(-1,('chi',a,c,m)),(-1,('chi',b,c,mul[du[a],m]))],['biderivation',a,b,c,m])
    if variable_tau:
        for m in M:add([(1,('tau',m)),(1,('tau',du[m]))],['tau_product',m])
    forms=character_forms(mul,H,h);assignments=list(itertools.product(range(len(forms)),repeat=len(M)))
    B=[[0]*len(assignments)for _ in equations]
    for im,m in enumerate(M):
        for ia,a in enumerate(H):
            for ib,b in enumerate(H):
                row={ki[('chi',a,b,m)]:1}if a and b else{}
                values=[forms[choice[im]][ia][ib]for choice in assignments]
                if row or any(values):equations.append(row);desc.append(['bicharacter',a,b,m]);B.append(values)
    return dict(S=S,M=M,H=H,du=du,mul=mul,keys=keys,equations=equations,descriptions=desc,B=B,forms=forms,assignments=assignments)

def prime_solve(A,B,p):
    A=A.copy()%p;B=B.copy()%p;rank=0;piv=[]
    for j in range(A.shape[1]):
        hits=np.flatnonzero(A[rank:,j])
        if not len(hits):continue
        i=int(hits[0])+rank
        A[[rank,i]]=A[[i,rank]];B[[rank,i]]=B[[i,rank]]
        c=pow(int(A[rank,j]),-1,p);A[rank]=A[rank]*c%p;B[rank]=B[rank]*c%p
        for i in np.flatnonzero(A[:,j]):
            if i==rank:continue
            c=int(A[i,j]);A[i]=(A[i]-c*A[rank])%p;B[i]=(B[i]-c*B[rank])%p
        piv.append(j);rank+=1
        if rank==A.shape[0]:break
    good=np.all(B[rank:]==0,axis=0);out={}
    for col in np.flatnonzero(good):
        v=np.zeros(A.shape[1],dtype=np.int64)
        for i,j in enumerate(piv):v[j]=B[i,col]
        out[int(col)]=v
    return out

def prime_power_solve(A,B,p,power):
    q=p**power;A=A.copy()%q;B=B.copy()%q;m,n=A.shape;T=np.eye(n,dtype=np.int64);r=0
    while r<min(m,n):
        nz=np.argwhere(A[r:,r:])
        if not len(nz):break
        def val(pos):
            a=int(A[r+int(pos[0]),r+int(pos[1])]);v=0
            while a%p==0:a//=p;v+=1
            return v
        pos=min(nz,key=val);i,j=map(int,pos+np.array([r,r]));d=p**val(pos)
        A[[r,i]]=A[[i,r]];B[[r,i]]=B[[i,r]];A[:,[r,j]]=A[:,[j,r]];T[:,[r,j]]=T[:,[j,r]]
        v=pow(int(A[r,r])//d,-1,q);A[r]=A[r]*v%q;B[r]=B[r]*v%q
        for i in np.flatnonzero(A[r+1:,r])+r+1:
            v=int(A[i,r])//d;A[i]=(A[i]-v*A[r])%q;B[i]=(B[i]-v*B[r])%q
        for j in np.flatnonzero(A[r,r+1:])+r+1:
            v=int(A[r,j])//d;A[:,j]=(A[:,j]-v*A[:,r])%q;T[:,j]=(T[:,j]-v*T[:,r])%q
        r+=1
    good=np.all(B[r:]==0,axis=0)
    for i in range(r):good &= B[i]%A[i,i]==0
    out={}
    for c in np.flatnonzero(good):
        y=np.zeros(n,dtype=np.int64)
        for i in range(r):y[i]=B[i,c]//A[i,i]
        out[int(c)]=(T@y)%q
    return out

def positive(z,base=16,odd_power=1):
    h=len(z['H']);odd=h**odd_power;q=base*(h if h==2 else odd)
    A=np.zeros((len(z['equations']),len(z['keys'])),dtype=np.int64)
    for i,row in enumerate(z['equations']):
        for j,v in row.items():A[i,j]=v
    B=np.array(z['B'],dtype=np.int64)*(q//h)
    if h==2:
        sols=solve_mod_batch(A,B,q)
    else:
        first=dict(solve_mod_batch(A,B,base));second=prime_solve(A,B,h)if odd_power==1 else prime_power_solve(A,B,h,odd_power);sols=[]
        for c in first.keys()&second.keys():
            x=first[c]+base*((second[c]-first[c])*pow(base,-1,odd)%odd)
            sols.append((c,x%q))
    if not sols:return None
    j,x=sols[0];require(np.all((A@x-B[:,j])%q==0),'complete phase equations')
    return dict(kind='liptrap_unitary_model',modulus=q,serfs=z['S'],lords=z['M'],stabilizer=z['H'],tau_times_tau_dual=f'1/{h}',tau='phase_times_inverse_square_root'if any(k[0]=='tau'for k in z['keys'])else'positive_inverse_square_root',bicharacter_assignment=list(z['assignments'][j]),phase_values=[list(k)+[int(x[i])]for i,k in enumerate(z['keys'])],reference='Liptrap 1002.3166v2 Definition4.3, Theorem4, Lemma5.4')

def combine(a,b,c):
    v=a.copy()
    for k,x in b.items():
        v[k]=v.get(k,F(0))+c*x
        if not v[k]:del v[k]
    return v

def contradictions(z):
    # Integer Euclidean row operations retain the saturated integer kernel.
    # Independently scaling rational kernel vectors can miss torsion relations.
    h=len(z['H']);piv={};proofs={};remaining=set(range(len(z['assignments'])))
    def bezout(a,b):
        oldr,r=a,b;olds,ss=1,0;oldt,tt=0,1
        while r:
            q=oldr//r;oldr,r=r,oldr-q*r;olds,ss=ss,olds-q*ss;oldt,tt=tt,oldt-q*tt
        if oldr<0:return -oldr,-olds,-oldt
        return oldr,olds,oldt
    for i,original in enumerate(z['equations']):
        row=original.copy();co={i:1}
        while row:
            k=min(row)
            if k not in piv:
                if row[k]<0:row={j:-v for j,v in row.items()};co={j:-v for j,v in co.items()}
                piv[k]=(row,co);break
            old,oldco=piv[k];a,b=old[k],row[k]
            if b%a==0:
                row=combine(row,old,-b//a);co=combine(co,oldco,-b//a)
            else:
                g,s0,t0=bezout(a,b)
                newpivot=combine({j:s0*v for j,v in old.items()},row,t0)
                newco=combine({j:s0*v for j,v in oldco.items()},co,t0)
                row=combine({j:(a//g)*v for j,v in row.items()},old,-b//g)
                co=combine({j:(a//g)*v for j,v in co.items()},oldco,-b//g)
                piv[k]=(newpivot,newco)
        if row:continue
        ints={k:int(v)for k,v in co.items()}
        chk=collections.Counter()
        for k,v in ints.items():
            for j,a in z['equations'][k].items():chk[j]+=v*a
        require(all(v==0 for v in chk.values()),'integer relation annihilates all complex variables')
        for col in list(remaining):
            rhs=sum(v*z['B'][k][col]for k,v in ints.items())%h
            if rhs:
                proofs[col]=dict(assignment_index=col,row_combination=sorted(ints.items()),nonzero_rhs_mod_stabilizer_order=rhs)
                remaining.remove(col)
        if not remaining:break
    if remaining:return None
    return dict(kind='liptrap_complex_obstruction',scope='general_complex_fusion_category',serfs=z['S'],lords=z['M'],stabilizer=z['H'],variable_tau=True,bicharacter_count=len(z['forms']),assignment_count=len(z['assignments']),contradictions=[proofs[i]for i in range(len(z['assignments']))])

def check_positive(R,c):
    z=setup(R,c['tau']=='phase_times_inverse_square_root');q=c['modulus'];X={tuple(v[:-1]):v[-1]for v in c['phase_values']}
    require(set(X)==set(z['keys']),'complete phase key set')
    x=[X[k]for k in z['keys']];choice=z['assignments'].index(tuple(c['bicharacter_assignment']))
    require(all((sum(a*x[j]for j,a in row.items())-B[choice]*(q//len(z['H'])))%q==0 for row,B in zip(z['equations'],z['B'])),'all defining equations')
    # The reconstructed non-scalar recouplings are Fourier matrices up to
    # row/column phases. Check every coset block exactly by cyclotomic division.
    import sympy as sp
    t=sp.Symbol('t');phi=list(map(int,sp.Poly(sp.cyclotomic_poly(q,t),t).all_coeffs()))[::-1];deg=len(phi)-1
    def zero(co):
        for k in range(len(co)-1,deg-1,-1):
            a=co[k]
            for j,b in enumerate(phi):co[k-deg+j]-=a*b
        return not any(co)
    def v(f,a,b,m):return X.get((f,a,b,m),0)
    mul=z['mul'];du=z['du'];H=z['H'];cosets=sorted({tuple(sorted(mul[a,h]for h in H))for a in z['S']})
    def gamma(a,b,m):
        u=mul[du[b],m]
        return (X.get(('tau',u),0)+v('upsilon',du[a],a,du[u])-v('upsilon',du[b],b,mul[u,du[a]])-v('chi',b,a,m))%q
    blocks=0
    for I,J,m in itertools.product(cosets,cosets,z['M']):
        for a,b in itertools.product(I,I):
            co=[0]*q
            for j in J:co[(gamma(a,j,m)-gamma(b,j,m))%q]+=1
            if a==b:co[0]-=len(H)
            require(zero(co),'exact recoupling block orthogonality')
        blocks+=1
    return dict(defining_equations=len(z['equations']),exact_unitary_fourier_blocks=blocks)

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());rows=[]
    for rid in json.loads((ROOT/'remaining_after_basic.json').read_text()):
        R=data[rid];z=setup(R)
        if z is None:continue
        if z.get('nonabelian'):
            c=dict(kind='nonabelian_feudal_stabilizer',scope='general_complex_fusion_category',stabilizer=z['H']);model=None;check=None
        else:
            model=positive(z);c=None;check=None
            if not model:model=positive(setup(R,True))
            if not model and len(z['H'])in(3,5):model=positive(setup(R,True),odd_power=3)
            if model:check=check_positive(R,model)
            else:c=contradictions(setup(R,True))
        rows.append(dict(id=rid,tensor_sha256=sha(R),model=model,certificate=c,verification=check))
        print(rid,'modeled'if model else'excluded'if c else'no conclusion',flush=True)
    (ROOT/'feudal.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('DONE',len(rows),'models',sum(bool(r['model'])for r in rows),'excluded',sum(bool(r['certificate'])for r in rows),'seconds',time.monotonic()-start)

if __name__=='__main__':main()
