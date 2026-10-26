"""Independent audit of the C4 TY action and the Liptrap C2 Morita dual.

No discovery.  The Morita tensor is recomputed from monomial intertwiners,
not the constructor's cyclotomic stabilizer-character trace formula.
"""
from pathlib import Path
import collections,hashlib,itertools,json,sys,time
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
OTHER=HERE.parent/'family_graded'
sys.path[:0]=[str(BASE),str(BASE/'sources/work/rank11'),str(OTHER)]
from feudal_dual import reconstruct,construct

def need(ok,text):
    if not ok:raise ValueError(text)

class Relations:
    """Relations e_x = zeta^phase e_y, including vanishing components."""
    def __init__(self,n,q):
        self.parent=list(range(n));self.phase=[0]*n;self.bad=set();self.q=q
    def find(self,x):
        p=self.parent[x]
        if p==x:return x,0
        r,a=self.find(p);self.phase[x]=(self.phase[x]+a)%self.q;self.parent[x]=r
        return r,self.phase[x]
    def relate(self,x,y,a):
        r,b=self.find(x);s,c=self.find(y)
        if r==s:
            if (b-a-c)%self.q:self.bad.add(r)
        else:
            bad=r in self.bad or s in self.bad
            self.parent[r]=s;self.phase[r]=(a+c-b)%self.q
            if bad:self.bad.add(s)
    def dimension(self):
        roots={self.find(i)[0]for i in range(len(self.parent))}
        bad={self.find(i)[0]for i in self.bad}
        return len(roots-bad)

PRECURSOR_CACHE={}
def precursor_checks(R,c):
    cachekey=hashlib.sha256(json.dumps([R,c],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if cachekey in PRECURSOR_CACHE:return PRECURSOR_CACHE[cachekey]
    q=c['modulus'];S=c['serfs'];M=c['lords'];H=c['stabilizer']
    need(q==5 and len(S)==20 and len(M)==4 and len(H)==5,'retained precursor type')
    dual=[next(j for j in range(24)if R[i][j][0])for i in range(24)]
    mul={(a,b):row.index(1)for a,A in enumerate(R)for b,row in enumerate(A)if a in S or b in S}
    p={tuple(v[:-1]):v[-1]%q for v in c['phase_values']}
    need(set(p)=={(f,a,b,m)for f in ['chi','upsilon']for a in S if a for b in S if b for m in M},'complete normalized phase data')
    def v(f,a,b,m):return p.get((f,a,b,m),0)
    counts=collections.Counter()
    for a,b,m in itertools.product(S,S,M):
        need((v('chi',b,a,dual[m])-v('chi',a,b,mul[mul[a,m],b]))%q==0,'constant-tau quasisymmetry');counts['quasisymmetry']+=1
    for a,b,d,m in itertools.product(S,S,S,M):
        t=v('upsilon',a,b,m)-v('upsilon',a,b,mul[m,dual[d]])+v('chi',mul[a,b],d,m)-v('chi',a,d,m)-v('chi',b,d,mul[dual[a],m])
        need(t%q==0,'biderivation');counts['biderivation']+=1
    for m in M:
        rows=[]
        for a in H:
            row=tuple(v('chi',a,b,m)for b in H);rows.append(row)
            for b,d in itertools.product(H,H):
                need(v('chi',a,b,m)==v('chi',b,a,m),'symmetric bicharacter')
                need((v('chi',mul[a,b],d,m)-v('chi',a,d,m)-v('chi',b,d,m))%q==0,'bicharacter law')
        need(len(set(rows))==5,'nondegenerate bicharacter')
    need(c['tau']=='positive_inverse_square_root'and c['tau_times_tau_dual']=='1/5','actual tau normalization')
    # With unit-modulus chi,upsilon, scalar F matrices have norm one and the
    # only nonscalar recouplings are Fourier matrices.  Test each normalized
    # Fourier Gram matrix without a complex floating-point representation.
    cosets=sorted({tuple(sorted(mul[a,h]for h in H))for a in S})
    def gamma(a,b,m):
        u=mul[dual[b],m]
        return(v('upsilon',dual[a],a,dual[u])-v('upsilon',dual[b],b,mul[u,dual[a]])-v('chi',b,a,m))%q
    for A,B,m in itertools.product(cosets,cosets,M):
        for a,b in itertools.product(A,A):
            co=[0]*5
            for x in B:co[(gamma(a,x,m)-gamma(b,x,m))%5]+=1
            if a==b:co[0]-=5
            need(len(set(co))==1,'Phi5 Fourier orthogonality')
        counts['unitary_Fourier_blocks']+=1
    F,mul,dual=reconstruct(R,c)
    supports=[[tuple(i for i,v in enumerate(row)if v)for row in A]for A in R]
    # With at most two lords, every nonempty F matrix is scalar.  Verify
    # the scalar pentagon on all these input quadruples, independently of
    # the reduced Liptrap equations above.
    from functools import lru_cache
    @lru_cache(None)
    def paths(a,b,d,out):
        L=[x for x in supports[a][b]if out in supports[x][d]]
        Q=[x for x in supports[b][d]if out in supports[a][x]]
        need(len(L)==len(Q)==1,'scalar recoupling path')
        return L[0],Q[0]
    Ms=set(M)
    for a,b,d,e in itertools.product(range(24),repeat=4):
        if sum(x in Ms for x in [a,b,d,e])>2:continue
        for u in supports[a][b]:
            for v0 in supports[u][d]:
                for out in supports[v0][e]:
                    q0=paths(u,d,e,out)[1];r=paths(a,b,q0,out)[1];p0=paths(a,b,d,v0)[1]
                    lhs=F(u,d,e,out)+F(a,b,q0,out)
                    rhs=F(a,b,d,v0)+F(a,p0,e,out)+F(b,d,e,r)
                    need((lhs-rhs)%5==0,'independent full mixed scalar pentagon')
                    counts['scalar_pentagons_at_most_two_lords']+=1
    result=F,mul,dual,dict(counts)
    PRECURSOR_CACHE[cachekey]=result
    return result

def morphism_tensor(R,cert,c,twist=None):
    F0,mul,dual,basecounts=precursor_checks(R,cert);counts=collections.Counter(basecounts)
    if twist is None:
        q=10;F=lambda a,b,d,k:2*F0(a,b,d,k)%q
    else:
        G=twist['grading_group_table'];degree=twist['grading'];w=twist['cocycle'];n=len(G)
        need(twist['modulus']==4,'retained normalized cocycle modulus')
        need(all(G[0][a]==G[a][0]==a for a in range(n))and all(G[G[a][b]][d]==G[a][G[b][d]]for a,b,d in itertools.product(range(n),repeat=3)),'actual grading group')
        need(all(len({G[a][b]for b in range(n)})==n for a in range(n)),'invertible grading elements')
        need(all(degree[k]==G[degree[a]][degree[b]]for a,b,k in itertools.product(range(24),repeat=3)if R[a][b][k]),'actual fusion grading')
        need(all(w[a][b][d]%4==0 for a,b,d in itertools.product(range(n),repeat=3)if not(a and b and d)),'normalized group cocycle')
        need(all((w[b][d][e]-w[G[a][b]][d][e]+w[a][G[b][d]][e]-w[a][b][G[d][e]]+w[a][b][d])%4==0 for a,b,d,e in itertools.product(range(n),repeat=4)),'full group three-cocycle equations')
        counts['normalized_group_cocycle_equations']=n**4
        q=20 if all(v%2==0 for A in w for row in A for v in row)else 40
        F=lambda a,b,d,k:((q//5)*F0(a,b,d,k)+(q//4)*w[degree[a]][degree[b]][degree[d]])%q
    need(mul[c,c]==0 and F(c,c,c,c)==0,'connected separable subgroup algebra 1+c')
    expected,info=construct(R,cert,c,twist=twist);objs=info['objects'];rank=len(objs)
    # Check every constituent action independently before tensoring.
    for O in objs:
        D=O['D'];L={int(k):v for k,v in O['L'].items()};P={int(k):v for k,v in O['R'].items()}
        for x in D:
            need((L[x]+L[mul[c,x]]+F(c,c,x,x))%q==0,'left module associativity')
            need((P[x]+P[mul[x,c]]-F(x,c,c,x))%q==0,'right module associativity')
            need((L[x]+P[mul[c,x]]-P[x]-L[mul[x,c]]-F(c,x,c,mul[mul[c,x],c]))%q==0,'commuting bimodule actions')
    out=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
    for i,A in enumerate(objs):
        for j,B in enumerate(objs):
            pairs=[(x,y,k)for x in A['D']for y in B['D']for k,v in enumerate(R[x][y])if v]
            ix={p:i for i,p in enumerate(pairs)};rel=Relations(len(pairs),q)
            for P in pairs:
                x,y,k=P;Q=(mul[x,c],mul[c,y],k)
                phase=F(mul[x,c],c,y,k)+B['L'][y]-A['R'][mul[x,c]]
                rel.relate(ix[P],ix[Q],phase)
            need(not rel.bad,'balanced coequalizer has no inconsistent orbit')
            roots=sorted({rel.find(a)[0]for a in range(len(pairs))});ri={a:i for i,a in enumerate(roots)}
            grades=[pairs[a][2]for a in roots];left=[];right=[]
            for a in roots:
                x,y,k=pairs[a]
                t,phase=rel.find(ix[(mul[c,x],y,mul[c,k])]);left.append((ri[t],(A['L'][x]-F(c,x,y,mul[c,k])+phase)%q))
                t,phase=rel.find(ix[(x,mul[y,c],mul[k,c])]);right.append((ri[t],(F(x,y,c,mul[k,c])+B['R'][y]+phase)%q))
            # Check quotient actions against both representatives of every
            # balancing relation, rather than only a chosen basis.
            for a,P in enumerate(pairs):
                x,y,k=P;r,phase=rel.find(a)
                for target,delta,op in [((mul[c,x],y,mul[c,k]),A['L'][x]-F(c,x,y,mul[c,k]),left),((x,mul[y,c],mul[k,c]),F(x,y,c,mul[k,c])+B['R'][y],right)]:
                    t,eps=rel.find(ix[target]);u,v=op[ri[r]]
                    need(ri[t]==u and(delta+eps-phase-v)%q==0,'independent balanced action descent')
            for k,C in enumerate(objs):
                active=[a for a,g in enumerate(grades)if g in C['D']];ai={a:b for b,a in enumerate(active)};hom=Relations(len(active),q)
                for a in active:
                    g=grades[a]
                    for op,source_phase in [(left,C['L'][g]),(right,C['R'][g])]:
                        b,phase=op[a]
                        # phi_source coefficients t satisfy
                        # t_target = zeta^(phase-source_action) t_source.
                        hom.relate(ai[b],ai[a],phase-source_phase)
                out[i][j][k]=hom.dimension()
            counts['balanced_products']+=1
    need(out==expected,'intertwiner dimensions agree with stabilizer-trace tensor')
    counts['independent_Hom_dimensions']=rank**3
    return out,dict(counts)

def c4_ty_check():
    rows=json.loads((OTHER/'zest_results.json').read_text());row=next(r for r in rows if r['id']=='R12_1_449');model=next(m for m in row['models']if not any(any(v for v in a)for a in m['parameters']['cocycle']))
    par=model['parameters'];R=par['base_tensor'];sigma=[0,4,3,2,1,5]
    # TY inversion preserves the entire bicharacter and the positive tau.
    need(all((sigma[a]*sigma[b]-a*b)%5==0 for a,b in itertools.product(range(5),repeat=2)),'orthogonal TY action')
    def deg(a):return int(a==5)
    # Cyclic carry eta(g,h)_X = (-1)^(floor((g+h)/4)*deg(X)).
    for g,h,k in itertools.product(range(4),repeat=3):
        need(((g+h)//4+((g+h)%4+k)//4-(h+k)//4-(g+(h+k)%4)//4)%2==0,'coherent C4 carry action')
    labs=par['labels'];need(len(labs)==12,'C4 orbit/stabilizer labels')
    # Recompute tensor multiplicities by character equality, without the
    # shared cyclic Fourier implementation.  On a stabilizer element g,
    # each fixed fusion summand contributes exp(pi*i*e/4).
    TY=[[[0]*6 for _ in range(6)]for _ in range(6)]
    for a,b in itertools.product(range(5),repeat=2):TY[a][b][(a+b)%5]=1
    for a in range(5):TY[a][5][5]=TY[5][a][5]=TY[5][5][a]=TY[5][5][a]=1
    for a in range(5):TY[5][5][a]=1
    powers=[list(range(6)),sigma,list(range(6)),sigma];T=[[[0]*12 for _ in range(12)]for _ in range(12)]
    for i,(A,a)in enumerate(labs):
        for j,(B,b)in enumerate(labs):
            for k,(C,c)in enumerate(labs):
                co=[0]*8;z=C[0]
                for g in range(0,4,len(C)):
                    for x in A:
                        for y in B:
                            if powers[g][x]==x and powers[g][y]==y:
                                co[((2*(a+b-c)+deg(x)+deg(y)-deg(z))*g)%8]+=TY[x][y][z]
                # Phi8(t)=t^4+1.
                for n in range(7,3,-1):co[n-4]-=co[n];co[n]=0
                d=4//len(C);need(not any(co[1:])and co[0]>=0 and co[0]%d==0,'exact C4 stabilizer multiplicity');T[i][j][k]=co[0]//d
    need(T==R==model['model_tensor'],'independent C4 TY tensor')
    D=json.loads((BASE/'tensors.json').read_text())['R12_1_449'];p=model['basis_map_source_to_model']
    need(all(D[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'R449 exact model identification')
    return dict(status='PASS',categorical_action='Orthogonal TY inversion with coherent C4 carry parity; F^4=epsilon, not a false assertion of inversion order four.',coefficients=1728)

def main():
    start=time.monotonic();audits=[];data=json.loads((BASE/'tensors.json').read_text())
    sourcefiles=[OTHER/f for f in ['feudal_dual_results.json','feudal_twist_results.json','feudal_abelian_twist_results.json']if(OTHER/f).exists()]
    for file in sourcefiles:
        for row in json.loads(file.read_text()):
            for index,model in enumerate(row['models']):
                p=model['parameters'];T,checks=morphism_tensor(p['feudal_tensor'],p['feudal_certificate'],p['subgroup_generator'],p.get('grading_twist'));N=data[row['id']];perm=model['basis_map_source_to_model']
                need(T==model['model_tensor'],'frozen Morita tensor');need(all(N[i][j][k]==T[perm[i]][perm[j]][perm[k]]for i,j,k in itertools.product(range(12),repeat=3)),'Morita input tensor')
                audits.append(dict(id=row['id'],source_file=file.name,model_index=index,status='PASS',checks=checks))
    checked=[OTHER/'feudal_dual.py',OTHER/'feudal40_models_sparse.json',OTHER/'zest_results.json',HERE/'audit_graded_models.py']+sourcefiles
    hashes={str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest()for f in checked}
    out=dict(status='PASS',TY_C4=c4_ty_check(),Morita_models=audits,optimized_python=not __debug__,examined_files_sha256=hashes,elapsed_seconds=time.monotonic()-start)
    (HERE/('audit_graded_models_optimized.json'if not __debug__ else'audit_graded_models.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
