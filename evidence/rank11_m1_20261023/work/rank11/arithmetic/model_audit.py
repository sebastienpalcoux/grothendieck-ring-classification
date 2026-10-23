#!/usr/bin/env python3
"""Independent cochain and tensor audit of the rank-eleven unitary models.

The action certificates are read, not rediscovered. Equivariantization uses
orbits of fusion-channel bases rather than the discovery scripts' traces.
"""
from pathlib import Path
import collections, hashlib, itertools, json, sys
import sympy as s
from run import HERE, exact, require
sys.path.insert(0,str(HERE.parent))
import common
MODELS=HERE.parent/'known_models'
I=itertools.product

def full_match(r,m,T):
    R=common.read()[r['id']];p=m['basis_map_source_to_model'];n=len(R)
    require(common.sha(R)==r['tensor_sha256'],'input hash')
    require(sorted(p)==list(range(n)) and p[0]==0,'basis permutation')
    require(T==m['model_tensor'],'reconstructed model tensor')
    require(all(R[a][b][c]==T[p[a]][p[b]][p[c]] for a,b,c in I(range(n),repeat=3)),'all tensor coefficients')
    common.validate(T)

def su2(k,even=False):
    labels=list(range(0,k+1,2 if even else 1));n=len(labels)
    return [[[int(abs(a-b)<=c<=min(a+b,2*k-a-b) and (a+b+c)%2==0)
             for c in labels] for b in labels] for a in labels]

def cyclic_tensor(n):
    return [[[int((a+b)%n==c) for c in range(n)] for b in range(n)] for a in range(n)]

def group_table(orders):
    labels=list(I(*(range(n) for n in orders)));ix={a:i for i,a in enumerate(labels)}
    return [[ix[tuple((a[k]+b[k])%orders[k] for k in range(len(orders)))] for b in labels] for a in labels]

def ty(orders):
    G=group_table(orders);n=len(G);R=[[[0]*(n+1) for _ in range(n+1)] for _ in range(n+1)]
    for a,b in I(range(n),repeat=2):R[a][b][G[a][b]]=1
    for a in range(n):R[a][n][n]=R[n][a][n]=R[n][n][a]=1
    return R

def dihedral_character_tensor(m,dicyclic=False):
    require(not dicyclic or m%4==0,'current dicyclic input has symmetric linear-character group')
    linears=[(0,1),(0,-1)] if m%2 else [(0,1),(0,-1),(m//2,1),(m//2,-1)]
    chars=[([a],b)for a,b in linears]+[([k,(-k)%m],None)for k in range(1,(m+1)//2)]
    n=len(chars);T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for i,j,k in I(range(n),repeat=3):
        A,sa=chars[i];B,sb=chars[j];C,sc=chars[k]
        rot=sum((a+b-c)%m==0 for a in A for b in B for c in C)
        refl=0
        if sa is not None and sb is not None and sc is not None and (A[0]+B[0]-C[0])%m==0:refl=sa*sb*sc
        require((rot+refl)%2==0,'integer character inner product')
        T[i][j][k]=(rot+refl)//2
    return T

def pointed_equivariant(par):
    G=par['group_table'];p=par['automorphism'];n=len(G)
    require(p[0]==0 and sorted(p)==list(range(n)) and all(p[p[a]]==a for a in range(n)),'pointed action involution')
    require(all(G[0][a]==G[a][0]==a for a in range(n)),'group unit')
    require(all(G[G[a][b]][c]==G[a][G[b][c]] for a,b,c in I(range(n),repeat=3)),'group associativity')
    require(all(any(G[a][b]==G[b][a]==0 for b in range(n)) for a in range(n)),'group inverses')
    require(all(p[G[a][b]]==G[p[a]][p[b]] for a,b in I(range(n),repeat=2)),'strict group automorphism')
    R=[[[int(G[a][b]==c)for c in range(n)]for b in range(n)]for a in range(n)]
    labs=[];seen=set()
    for a in range(n):
        if a in seen:continue
        O=sorted({a,p[a]});seen.update(O)
        labs.extend([(O,0),(O,2)] if len(O)==1 else [(O,None)])
    return orbit_tensor(R,p,labs,lambda a,b,c,sa,sb,sc:sa+sb-sc,4)

def odd_metaplectic(N):
    q=(N-1)//2;n=q+4;T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for i in range(n):T[0][i][i]=T[i][0][i]=1
    T[1][1][0]=1
    for x in (2,3):T[1][x][5-x]=T[x][1][5-x]=1
    for y in range(4,n):T[1][y][y]=T[y][1][y]=1
    for x,z in I((2,3),repeat=2):
        T[x][z][int(x!=z)]=1
        for y in range(4,n):T[x][z][y]=1
    for x,y in I((2,3),range(4,n)):
        for z in (2,3):T[x][y][z]=T[y][x][z]=1
    for a,b in I(range(1,q+1),repeat=2):
        for v in (a+b,a-b):
            c=min(v%N,(-v)%N)
            if c:
                T[a+3][b+3][c+3]+=1
            else:T[a+3][b+3][0]+=1;T[a+3][b+3][1]+=1
    return T

def half_even(N):
    require(N%8==0,'current half-even base has N divisible by eight')
    D=dihedral_character_tensor(N//2);d=len(D);n=d+2
    T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for a,b,c in I(range(d),repeat=3):T[a][b][c]=D[a][b][c]
    for a in range(4):
        for e in range(2):T[a][d+e][d+(e^(a%2))]=T[d+e][a][d+(e^(a%2))]=1
    for a in range(4,d):
        for e,f in I(range(2),repeat=2):T[a][d+e][d+f]=T[d+e][a][d+f]=1
    for e,f in I(range(2),repeat=2):
        for a in range(4):T[d+e][d+f][a]=int((a%2)==(e^f))
        for a in range(4,d):T[d+e][d+f][a]=1
    return T

def base_construct(kind,p):
    if kind=='su2':return su2(p['level'],p['even']),True
    if kind=='rep_dihedral':return dihedral_character_tensor(p['m'],p.get('dicyclic',False)),True
    if kind=='even_metaplectic':require(p['N']==8,'SO8 base');return so8(),True
    if kind=='odd_metaplectic':return odd_metaplectic(p['N']),True
    if kind=='half_even_metaplectic':return half_even(p['N']),True
    if kind=='pointed_equivariant':
        G=p['group_table'];return pointed_equivariant(p),all(G[a][b]==G[b][a]for a,b in I(range(len(G)),repeat=2))
    raise ValueError(('unhandled base constructor',kind))

def standard_check(r,m):
    kind=m['constructor'];p=m['parameters']
    if kind=='associative_C2_zest':
        B,braided=base_construct(p['base_constructor'],p['base_parameters']);require(braided,'braided base supplies central lifts')
        require(B==p['base_tensor'],'independently rebuilt base');g=p['grading'];h=p['central_invertible'];n=len(B)
        require(g[0]==g[h]==0 and set(g)=={0,1},'faithful grading and neutral coefficient')
        require(B[h][h]==[1]+[0]*(n-1),'involutory coefficient')
        require(all(g[c]==(g[a]^g[b])for a,b,c in I(range(n),repeat=3)if B[a][b][c]),'C2 grading')
        action=[]
        for a in range(n):
            require(sum(B[h][a])==1 and B[h][a]==B[a][h],'central invertible object')
            action.append(B[h][a].index(1))
        T=[[[0]*n for _ in range(n)]for _ in range(n)]
        for a,b,c in I(range(n),repeat=3):T[a][b][action[c] if g[a] and g[b] else c]=B[a][b][c]
        obstruction='H4(C2,U(1))=0; DGPRZ Proposition3.9 and Remark3.10; unitary lift'
    else:T,braided=base_construct(kind,p);obstruction=None
    full_match(r,m,T)
    return {'id':r['id'],'kind':kind,'tensor_coefficients':len(T)**3,'categorical_obstruction':obstruction,'status':'PASS'}

def orbit_tensor(R,p,labels,phase,modulus):
    """C2 action, using free channel orbits and fixed-channel phases."""
    n=len(labels);T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for a,b,c in I(range(n),repeat=3):
        A,sa=labels[a];B,sb=labels[b];C,sc=labels[c];z=C[0]
        channels={(x,y) for x in A for y in B if R[x][y][z]}
        if len(C)==2:T[a][b][c]=len(channels);continue
        seen=set();v=0
        for x,y in sorted(channels):
            if (x,y) in seen:continue
            other=(p[x],p[y]);require(other in channels,'stabilizer preserves channel')
            seen.update([(x,y),other])
            if other!=(x,y):v+=1;continue
            e=phase(x,y,z,sa,sb,sc)%modulus
            require(e in (0,modulus//2),'fixed-channel eigenvalue is a sign')
            v+=int(e==0)
        T[a][b][c]=v
    return T

def check_c2_labels(p,labels,half_modulus):
    expected=[];seen=set()
    for a in range(len(p)):
        if a in seen:continue
        O=sorted({a,p[a]});seen.update(O)
        expected.extend([[O,0],[O,half_modulus]] if len(O)==1 else [[O,None]])
    require(labels==expected,'complete C2 orbit and projective-stabilizer labels')

def spin_check(r,m):
    par=m['parameters'];R=su2(6);p=par['permutation'];mu=par['coherence_exponents_mod4']
    J={(a,b,c):v for a,b,c,v in par['tensorator_exponents_mod2']}
    require(sorted(p)==list(range(7)) and p[0]==0 and all(p[p[a]]==a for a in range(7)),'spin involution')
    require(all(R[a][b][c]==R[p[a]][p[b]][p[c]] for a,b,c in I(range(7),repeat=3)),'spin based automorphism')
    require(set(J)=={(a,b,c) for a,b,c in I(range(7),repeat=3) if R[a][b][c]},'all tensorator channels')
    require(all(v in (0,1) for v in J.values()) and all(J[0,a,a]==J[a,0,a]==0 for a in range(7)),'unit tensorator')
    require(mu[0]==0 and all(mu[p[a]]==mu[a] for a in range(7)),'C2 associativity')
    for a,b,c in J:
        require((mu[a]+mu[b]-mu[c]-2*J[a,b,c]-2*J[p[a],p[b],p[c]])%4==0,'monoidal square coherence')
    # Independently evaluate the quantum-Racah gauge in a fresh number field.
    t=exact.t;f=s.Poly(t**4-4*t**2+2,t);K=exact.field(f);u=K([1,0]);emb=exact.Embedding(f,('1847759/1000000','1847760/1000000'))
    q=[K.zero,K.one]
    for a in range(2,9):q.append(u*q[-1]-q[-2])
    require(q[8]==K.zero and all(emb.sign(q[a])==1 for a in range(1,8)),'positive quantum dimensions')
    fac=[K.one]
    for a in range(1,8):fac.append(fac[-1]*q[a])
    cache={}
    def F(a,b,c,d,e,h):
        key=(a,b,c,d,e,h)
        if key in cache:return cache[key]
        triangles=[(a,b,e),(e,c,d),(b,c,h),(a,h,d)]
        if not all(R[x][y][z] for x,y,z in triangles):return K.zero,0
        delta=K.one;lower=[]
        for x,y,z in triangles:
            j=(x+y+z)//2;lower.append(j)
            delta*=fac[j-x]*fac[j-y]*fac[j-z]/fac[j+1]
        upper=[(a+b+c+d)//2,(a+c+e+h)//2,(b+d+e+h)//2]
        zsum=K.zero
        for z in range(max(lower),min(upper)+1):
            ds=[z-v for v in lower]+[v-z for v in upper]
            require(all(0<=v<8 for v in ds),'no zero Racah denominator')
            if z>=7:continue
            den=K.one
            for v in ds:den*=fac[v]
            zsum+=((-1)**z)*fac[z+1]/den
        mag=q[e+1]*q[h+1]*delta*zsum*zsum
        sg=(-1)**((a+b+c+d)//2)*emb.sign(zsum)
        cache[key]=mag,sg;return mag,sg
    nonzero=zeros=0
    for a,b,c,d,e,h in I(range(7),repeat=6):
        if not(R[a][b][e] and R[e][c][d] and R[b][c][h] and R[a][h][d]):continue
        mag,sg=F(a,b,c,d,e,h);mag2,sg2=F(*(p[x] for x in (a,b,c,d,e,h)))
        require(mag==mag2,'all transformed F magnitudes')
        if not mag:zeros+=1;continue
        nonzero+=1
        left=(J[a,b,e]+J[e,c,d]-J[b,c,h]-J[a,h,d])%2
        require(sg2==((-1)**left)*sg,'all transformed F phases')
    labels=par['labels'];check_c2_labels(p,labels,4)
    T=orbit_tensor(R,p,labels,lambda a,b,c,ea,eb,ec:4*J[a,b,c]+mu[a]+mu[b]-mu[c]+ea+eb-ec,8)
    full_match(r,m,T)
    return {'id':r['id'],'kind':'spin_C2','nonzero_F_equations':nonzero,'zero_F_entries':zeros,'tensor_coefficients':11**3,'square_coherence_channels':len(J),'status':'PASS'}

def twisted_check(r,m):
    par=m['parameters'];n=par['cyclic_order'];t=par['cocycle_class'];p=par['automorphism'];J=par['tensorator_mod16'];mu=par['coherence_mod32'];R=cyclic_tensor(n)
    require(p[0]==0 and sorted(p)==list(range(n)) and all(p[p[a]]==a for a in range(n)),'pointed involution')
    require(all(p[(a+b)%n]==(p[a]+p[b])%n for a,b in I(range(n),repeat=2)),'group automorphism')
    w=lambda a,b,c:(t*a*((b+c)//n))%n
    require(mu[0]==0 and all(mu[p[a]]==mu[a] for a in range(n)),'coherent C2 associativity')
    require(all(J[0][a]==J[a][0]==0 for a in range(n)),'normalized tensorator')
    for a,b,c,d in I(range(n),repeat=4):
        require((w(b,c,d)-w((a+b)%n,c,d)+w(a,(b+c)%n,d)-w(a,b,(c+d)%n)+w(a,b,c))%n==0,'3-cocycle')
    for a,b,c in I(range(n),repeat=3):
        lhs=(w(a,b,c)+J[(a+b)%n][c]+J[a][b])%n
        rhs=(J[a][(b+c)%n]+J[b][c]+w(p[a],p[b],p[c]))%n
        require(lhs==rhs,'monoidal functor pentagon')
    for a,b in I(range(n),repeat=2):
        require((mu[(a+b)%n]+2*J[a][b]+2*J[p[a]][p[b]]-mu[a]-mu[b])%(2*n)==0,'monoidal F-square')
    check_c2_labels(p,par['labels'],2*n)
    T=orbit_tensor(R,p,par['labels'],lambda a,b,c,ea,eb,ec:-4*J[a][b]+mu[a]+mu[b]-mu[c]+ea+eb-ec,4*n)
    full_match(r,m,T)
    return {'id':r['id'],'kind':'twisted_pointed_C2','cocycle_equations':n**4,'functor_equations':n**3,'square_equations':n*n,'tensor_coefficients':11**3,'status':'PASS'}

def so8():
    # Independent block rules: V4, one adjoint object, three 2-element torsors.
    G=range(4);n=11;T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for a,b in I(G,repeat=2):T[a][b][a^b]=1
    for a in G:T[a][4][4]=T[4][a][4]=T[4][4][a]=1
    for block,stab in enumerate((1,2,3)):
        X=[5+2*block,6+2*block]
        for x in X:
            for a in G:
                y=x if a in (0,stab) else X[0]+X[1]-x
                T[a][x][y]=T[x][a][y]=1
            for y in X:T[4][x][y]=T[x][4][y]=1
        for x,y in I(X,repeat=2):
            T[x][y][4]=1
            for a in G:T[x][y][a]=int((a in (0,stab))==(x==y))
    for x,y in I(range(5,11),repeat=2):
        bx,by=(x-5)//2,(y-5)//2
        if bx==by:continue
        b=3-bx-by
        T[x][y][5+2*b]=T[x][y][6+2*b]=1
    common.validate(T);return T

def v4_check(r,m):
    par=m['parameters'];B=so8();g=par['grading'];lam=par['cocycle'];n=11
    require(B==par['base_tensor'],'SO8 base rules')
    require(g[:5]==[0]*5 and set(g)==set(range(4)),'faithful V4 grading')
    require(all(g[c]==(g[a]^g[b]) for a,b,c in I(range(n),repeat=3) if B[a][b][c]),'graded products')
    require(all(lam[0][a]==lam[a][0]==0 for a in range(4)),'normalized zest cocycle')
    for a,b,c in I(range(4),repeat=3):require((lam[a][b]^lam[a^b][c])==(lam[b][c]^lam[a][b^c]),'V4 cocycle identity')
    T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for a,b in I(range(n),repeat=2):
        h=lam[g[a]][g[b]];require(0<=h<4 and g[h]==0,'neutral coefficient')
        for c in range(n):
            if not B[a][b][c]:continue
            outputs=[d for d in range(n) if B[h][c][d]];require(len(outputs)==1,'invertible action')
            T[a][b][outputs[0]]+=B[a][b][c]
    full_match(r,m,T)
    return {'id':r['id'],'kind':'V4_Tannakian_zest','cocycle_equations':64,'tensor_coefficients':1331,'categorical_obstruction':'trivial in the strictly symmetric pointed gauge for the neutral Tannakian V4','status':'PASS'}

def ty_check(r,m):
    par=m['parameters'];orders=par['orders'];G=group_table(orders);n=len(G);R=ty(orders)
    if m['constructor']=='ty':full_match(r,m,R);return {'id':r['id'],'kind':'TY','status':'PASS'}
    p=par['automorphism'];M=par['group_order'];pp=par['parity'];labs=par['labels']
    require(p[n]==n and sorted(p)==list(range(n+1)),'TY automorphism')
    power=list(range(n+1))
    for j in range(M):power=[p[x] for x in power]
    require(power==list(range(n+1)),'cyclic action order')
    require(all(p[G[a][b]]==G[p[a]][p[b]] for a,b in I(range(n),repeat=2)),'group automorphism')
    if 'bicharacter_exponents' in par:chi=par['bicharacter_exponents'];mod=par['bicharacter_modulus']
    else:
        require(len(orders)==1,'explicit form required for noncyclic group');mod=n;chi=[[a*b%n for b in range(n)]for a in range(n)]
    require(all(chi[a][b]==chi[b][a] and chi[p[a]][p[b]]==chi[a][b] for a,b in I(range(n),repeat=2)),'symmetric invariant bicharacter')
    require(all(any(chi[a][b]%mod for b in range(n)) for a in range(1,n)),'nondegenerate bicharacter')
    require(all((chi[G[a][b]][c]-chi[a][c]-chi[b][c])%mod==0 for a,b,c in I(range(n),repeat=3)),'bicharacter multiplicativity')
    require(pp[:n]==[0]*n and (M==2 or pp[n]==0),'allowed parity coherence')
    require(all((pp[a]+pp[b]-pp[c])%2==0 for a,b,c in I(range(n+1),repeat=3) if R[a][b][c]),'parity is a tensor natural automorphism')
    expected=[];seen=set()
    for a in range(n+1):
        if a in seen:continue
        O=[];b=a
        while b not in O:O.append(b);b=p[b]
        require(b==a and M%len(O)==0,'object orbit');seen.update(O)
        expected.extend([[O,j]for j in range(M//len(O))])
    require(labs==expected,'complete orbit and stabilizer-character labels')
    # Stabilizer-channel cycles, each contributing one invariant exactly when
    # its full cycle phase is trivial.
    rank=len(labs);T=[[[0]*rank for _ in range(rank)] for _ in range(rank)]
    powers=[list(range(n+1))]
    for j in range(1,M):powers.append([p[a] for a in powers[-1]])
    for i,j,k in I(range(rank),repeat=3):
        A,ja=labs[i];B,jb=labs[j];C,jc=labs[k];c=C[0];lc=len(C)
        channels={(a,b)for a in A for b in B if R[a][b][c]};seen=set();count=0
        for pair in sorted(channels):
            if pair in seen:continue
            cyc=[];z=pair
            while z not in cyc:
                require(z in channels,'stabilizer channel');cyc.append(z);z=(powers[lc%M][z[0]],powers[lc%M][z[1]])
            require(z==pair,'channel cycle');seen.update(cyc)
            expo=(2*(ja+jb-jc)+pp[A[0]]+pp[B[0]]-pp[C[0]])*lc*len(cyc)
            if expo%(2*M)==0:count+=1
        T[i][j][k]=count
    full_match(r,m,T)
    return {'id':r['id'],'kind':'TY_cyclic_equivariant','tensor_coefficients':rank**3,'bicharacter_order':n,'action_order':M,'status':'PASS'}

def main():
    result={'checks':[],'scope':'Independent exact action/cochain and full tensor checks, with categorical existence arguments in model_audit.md.'}
    audited={}
    for filename,fn in [('su2_spin_models.json',spin_check),('twisted_cyclic_models.json',twisted_check),('v4_zest_models.json',v4_check)]:
        for r in json.loads((MODELS/filename).read_text()):
            for m in r['models']:
                z=fn(r,m);result['checks'].append(z);audited.setdefault(r['id'],[]).append(m);print(z,flush=True)
    for r in json.loads((MODELS/'standard_models.json').read_text())+json.loads((MODELS/'pointed16_models.json').read_text()):
        for m in r['models']:
            audited.setdefault(r['id'],[]).append(m)
            if m['constructor'] in ('ty','ty_cyclic_equivariant'):
                z=ty_check(r,m);result['checks'].append(z)
            elif m['constructor']=='pointed':
                G=group_table(m['parameters']['orders']);n=len(G)
                T=[[[int(G[a][b]==c)for c in range(n)]for b in range(n)]for a in range(n)]
                full_match(r,m,T);result['checks'].append({'id':r['id'],'kind':'pointed','status':'PASS'})
            else:result['checks'].append(standard_check(r,m))
    result['status']='PASS';result['distinct_ids']=sorted({r['id']for r in result['checks']},key=lambda x:int(x.split('_')[-1]))
    selected=json.loads((MODELS/'selected_models.json').read_text())
    require({r['id'] for r in selected}==set(result['distinct_ids']),'all selected inputs audited')
    for r in selected:require(r['model'] in audited[r['id']],'selected recipe audited in full')
    result['selected_recipes']=len(selected)
    result['input_model_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in MODELS.glob('*_models.json')}
    (HERE/'model_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',len(result['checks']),'construction checks',len(result['distinct_ids']),'distinct ids',flush=True)
if __name__=='__main__':main()
