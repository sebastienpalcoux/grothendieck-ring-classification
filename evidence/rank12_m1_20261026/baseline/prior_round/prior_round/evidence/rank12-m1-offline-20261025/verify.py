"""Exact accepted-witness replay; no discovery search or online operation.

Direct integer/phase checks are separate from the search implementations.
Standard number-field arithmetic is shared; literature existence statements
and the accepted lower-rank category proofs remain the categorical premises.
"""
from pathlib import Path
from fractions import Fraction as Q
import collections,hashlib,itertools,json,math,subprocess,sys,time
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common
from state import current
from fp import fp_character,exact
from field_checks import central_order,pu_gate
from feudal import setup
from twisted_c2_models import construct as bimodules
from group_models import order
sys.path.insert(0,str(ROOT/'sources/work/models'))
sys.path.insert(0,str(ROOT/'sources/work/root_models'))
import match_models as mm
import extra_models as em
from construct import half_even_metaplectic
need=common.require;t=s.Symbol('t');data=json.loads((ROOT/'tensors.json').read_text())
profiles={p['id']:p for p in json.loads((ROOT/'profile.json').read_text())['records']}

def casimir(R):
    n=len(R)
    return s.Matrix([[sum(R[a][i][k]*R[a][j][k]for a,k in itertools.product(range(n),repeat=2))for j in range(n)]for i in range(n)])

def arithmetic(R,c):
    n=len(R);kind=c['kind'];du=common.dual(R);G=[i for i in range(n)if sum(R[i][du[i]])==1];X=[i for i in range(n)if i not in G]
    if kind=='casimir_dnumber':
        f=s.Poly.from_list(c['factor'],t);p=casimir(R).charpoly(t).as_poly();a=list(map(int,f.all_coeffs()));d=f.degree();j=c['index'];norm=abs(a[-1])
        need(f.is_irreducible and p.rem(f).is_zero and 1<=j<=d,'irreducible Casimir factor')
        need(pow(a[j],d,norm**j)==c['nonzero_remainder']!=0,'d-number divisibility contradiction')
    elif kind=='near_group_small_m':
        need(len(X)==1 and len(G)==n-1,'near-group partition');x=X[0]
        need(all(R[g][x][x]==R[x][g][x]==1 for g in G),'near-group action')
        need(all(R[x][x][g]==1 for g in G)and 0<R[x][x][x]<len(G)-1,'near-group small multiplicity')
    elif kind=='generalized_near_group_divisibility':
        x=c['object'];need(G==c['invertibles']and X==c['noninvertibles'],'two-value partition')
        need({next(k for k in range(n)if R[g][x][k])for g in G}==set(X),'transitive invertible action')
        H=[g for g in G if R[g][x][x]];r=sum(R[x][du[x]][k]for k in X);disc=r*r+4*len(H)
        need(H==c['stabilizer']and r==c['r']and disc==c['discriminant'],'quadratic dimension equation')
        need(math.isqrt(disc)**2!=disc and r%len(H)!=0,'irrational divisibility obstruction')
    elif kind in ['integral_drinfeld','noncomm_integral_drinfeld']:
        d=c['dims'];need(len(d)==n and d[0]==1 and all(type(v)is int and v>0 for v in d),'positive integral dimensions')
        need(all(sum(R[i][j][k]*d[k]for k in range(n))==d[i]*d[j]for i,j in itertools.product(range(n),repeat=2)),'integral dimension character')
        D=sum(v*v for v in d);need(D==c['global_dimension'],'global dimension')
        f=s.Poly.from_list(c['failed_factor'],t);p=casimir(R).charpoly(t).as_poly()
        need(f.is_irreducible and p.rem(f).is_zero,'Casimir factor')
        if kind=='integral_drinfeld':
            need(all(R[i][j]==R[j][i]for i,j in itertools.product(range(n),repeat=2)),'commutative integral-center scope')
            need(f.degree()>1 or D%int(-f.TC())!=0,'nonintegral distinguished center dimension')
        elif f.degree()==1:
            m=c['multiplicity'];need(p.rem(f**m).is_zero and not p.rem(f**(m+1)).is_zero,'exact eigenvalue multiplicity')
            lam=int(-f.TC());allowed=[e for e in range(1,math.isqrt(m)+1)if lam%e==0 and D%(lam//e)==0];reachable={0}
            for j in range(1,m+1):
                if any(j-e*e in reachable for e in allowed):reachable.add(j)
            need(m not in reachable,'impossible irreducible-degree square partition')
    else:raise ValueError('unsupported arithmetic witness '+kind)

def cyclic(R,c):
    n=len(R);g=c['g'];power=0;order0=0
    while True:
        row=R[power][g];need(sum(row)==1,'invertible cyclic subgroup');power=row.index(1);order0+=1
        if power==0:break
        need(order0<=n,'finite group order')
    need(order0==c['order']>1,'exact cyclic order');x,y,z=[c[k]for k in ['X','Y','Z']]
    unit=lambda a:[int(i==a)for i in range(n)]
    need(R[g][x]==unit(x)and R[y][g]==unit(y)and R[g][z]==R[z][g]==unit(z),'all four fixedness premises')
    m=R[x][y][z];need(m>0 and m==c['multiplicity'],'nonzero fusion coefficient')
    f=s.Poly.from_list(list(map(s.Rational,c['dimension_polynomial'])),t);p=s.Matrix(R[z]).charpoly(t).as_poly();iv=p.intervals(eps=s.Rational(1,10**15))[-1][0]
    need(f.is_irreducible and p.rem(f).is_zero,'irreducible dimension factor')
    need(f.eval(iv[0])==0 if iv[0]==iv[1]else f.count_roots(*iv)==1,'largest real root')
    q=order0//math.gcd(order0,m);scaled=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
    need(list(map(str,scaled.all_coeffs()))==c['normalized_dimension_polynomial']and any(v.q!=1 for v in scaled.all_coeffs()),'nonintegral scaled minimal polynomial')

def forms_independent(R,H):
    h=len(H);ix={a:i for i,a in enumerate(H)};M=[[ix[R[a][b].index(1)]for b in H]for a in H];chars=[]
    for v in itertools.product(range(h),repeat=h-1):
        row=(0,)+v
        if all(row[M[a][b]]==(row[a]+row[b])%h for a,b in itertools.product(range(h),repeat=2)):chars.append(row)
    need(len(chars)==h,'complete characters of abelian stabilizer');forms=[]
    for rows in itertools.product(chars,repeat=h-1):
        C=((0,)*h,)+rows
        if len(set(C))!=h or any(C[a][b]!=C[b][a]for a,b in itertools.product(range(h),repeat=2)):continue
        if all(C[M[a][b]][c]==(C[a][c]+C[b][c])%h for a,b,c in itertools.product(range(h),repeat=3)):forms.append(C)
    return sorted(forms)

def liptrap_negative(R,c):
    z=setup(R,True);H=z['H'];M=z['M'];h=len(H);mul=z['mul'];du=z['du'];forms=forms_independent(R,H)
    need(forms==sorted(z['forms'])and len(forms)==c['bicharacter_count'],'complete nondegenerate bicharacters')
    assignments=list(itertools.product(range(len(forms)),repeat=len(M)));need(len(assignments)==c['assignment_count'],'complete assignments at every lord')
    need(sorted(p['assignment_index']for p in c['contradictions'])==list(range(len(assignments))),'every assignment excluded')
    def row(desc):
        tag,*v=desc;terms=[]
        if tag=='quasisymmetry':
            a,b,m=v;amb=mul[mul[a,m],b]
            terms=[(1,('chi',b,a,du[m])),(-1,('chi',a,b,amb)),(-1,('tau',amb)),(-1,('tau',m)),(1,('tau',mul[a,m])),(1,('tau',mul[m,b]))]
        elif tag=='biderivation':
            a,b,d,m=v;terms=[(1,('upsilon',a,b,m)),(-1,('upsilon',a,b,mul[m,du[d]])),(1,('chi',mul[a,b],d,m)),(-1,('chi',a,d,m)),(-1,('chi',b,d,mul[du[a],m]))]
        elif tag=='tau_product':terms=[(1,('tau',v[0])),(1,('tau',du[v[0]]))]
        elif tag=='bicharacter':a,b,m=v;terms=[(1,('chi',a,b,m))]
        else:raise ValueError('unknown formal identity')
        out=collections.Counter()
        for a,k in terms:
            if k[0]=='tau'or k[1]and k[2]:out[k]+=a
        return out
    for proof in c['contradictions']:
        total=collections.Counter();rhs=0;choice=assignments[proof['assignment_index']]
        for i,mult in proof['row_combination']:
            desc=z['descriptions'][i]
            for k,v in row(desc).items():total[k]+=mult*v
            if desc[0]=='bicharacter':
                a,b,m=desc[1:];rhs+=mult*forms[choice[M.index(m)]][H.index(a)][H.index(b)]
        need(all(v==0 for v in total.values()),'integer combination cancels arbitrary complex unknowns')
        need(rhs%h==proof['nonzero_rhs_mod_stabilizer_order']!=0,'nontrivial root of unity contradiction')

def liptrap_positive(R,c):
    n=len(R);S=c['serfs'];M=c['lords'];H=c['stabilizer'];q=c['modulus'];du=common.dual(R);X={tuple(v[:-1]):v[-1]for v in c['phase_values']}
    mul=lambda a,b:R[a][b].index(1)
    phase=lambda f,a,b,m:X.get((f,a,b,m),0)
    tau=lambda m:X.get(('tau',m),0)
    need(all(not R[a][b][d]for a,b,d in itertools.product(M,repeat=3)),'feudal parity')
    need(all([a for a in S if mul(a,m)==m]==H==[a for a in S if mul(m,a)==m]for m in M),'common left/right stabilizer')
    for m in M:
        need((tau(m)+tau(du[m]))%q==0,'tau product normalization')
        C=[[phase('chi',a,b,m)%q for b in H]for a in H]
        need(len(set(map(tuple,C)))==len(H),'nondegeneracy')
        for a,b,d in itertools.product(H,repeat=3):
            need((phase('chi',a,b,m)-phase('chi',b,a,m))%q==0,'symmetric bicharacter')
            need((phase('chi',mul(a,b),d,m)-phase('chi',a,d,m)-phase('chi',b,d,m))%q==0,'bicharacter multiplication')
    for a,b,m in itertools.product(S,S,M):
        amb=mul(mul(a,m),b)
        need((phase('chi',b,a,du[m])-phase('chi',a,b,amb)-tau(amb)-tau(m)+tau(mul(a,m))+tau(mul(m,b)))%q==0,'complete quasisymmetry')
    for a,b,d,m in itertools.product(S,S,S,M):
        need((phase('upsilon',a,b,m)-phase('upsilon',a,b,mul(m,du[d]))+phase('chi',mul(a,b),d,m)-phase('chi',a,d,m)-phase('chi',b,d,mul(du[a],m)))%q==0,'complete biderivation')
    from feudal import check_positive
    return check_positive(R,c)

def equivariant_C2(R,sigma,parity):
    n=len(R);need(sorted(sigma)==list(range(n))and sigma[0]==0 and all(sigma[sigma[i]]==i for i in range(n)),'involutive based action')
    need(all(R[a][b][c]==R[sigma[a]][sigma[b]][sigma[c]]for a,b,c in itertools.product(range(n),repeat=3)),'action on every fusion coefficient')
    labs=[];seen=set()
    for a in range(n):
        if a in seen:continue
        O=sorted({a,sigma[a]});seen.update(O)
        for j in range(2 if len(O)==1 else 1):labs.append((O,j))
    m=len(labs);T=[[[0]*m for _ in range(m)]for _ in range(m)]
    for i,(A,a0)in enumerate(labs):
        for j,(B,b0)in enumerate(labs):
            for k,(C,c0)in enumerate(labs):
                c=C[0];d=sum(R[a][b][c]for a in A for b in B)
                if len(C)==2:T[i][j][k]=d;continue
                tr=0
                for a in A:
                    for b in B:
                        if sigma[a]!=a or sigma[b]!=b:continue
                        exp=(parity[a]+parity[b]-parity[c]+2*(a0+b0-c0))%4
                        need(exp in(0,2)or R[a][b][c]==0,'involutive Hom action')
                        tr+=R[a][b][c]*(1 if exp==0 else -1)
                need(d+tr>=0 and(d+tr)%2==0,'exact Fourier projection')
                T[i][j][k]=(d+tr)//2
    return T

def group_tensor(G):
    n=len(G);need(all(sorted(r)==list(range(n))for r in G),'group right translations')
    need(all(G[0][i]==G[i][0]==i for i in range(n)),'group identity')
    A=np.array(G,dtype=np.int64)
    need(all(np.array_equal(A[A[i,:],:],A[i,A])for i in range(n)),'group associativity')
    return [[[int(G[i][j]==k)for k in range(n)]for j in range(n)]for i in range(n)]

rebuild_cache={}
def rebuild(kind,p):
    key=hashlib.sha256(json.dumps([kind,p],sort_keys=True).encode()).hexdigest()
    if key in rebuild_cache:return rebuild_cache[key]
    if kind=='pointed':R=mm.group(tuple(p['orders']))
    elif kind=='pointed_group':R=group_tensor(p['group_table'])
    elif kind=='ty':R=mm.ty(tuple(p['orders']))
    elif kind=='su2':R=mm.su2(p['level'],p['even'])
    elif kind=='dihedral_rep':R=mm.rep_dihedral(p['m'],p['dicyclic'])
    elif kind=='odd_metaplectic':R=em.metaplectic(p['N'])
    elif kind=='half_even_metaplectic':R=half_even_metaplectic(p['N'])[0]
    elif kind=='haagerup_izumi_cyclic':
        m=p['group_order'];n=2*m;R=[[[0]*n for _ in range(n)]for _ in range(n)]
        for a,b in itertools.product(range(m),repeat=2):
            R[a][b][(a+b)%m]=1;R[a][m+b][m+(a+b)%m]=1;R[m+a][b][m+(a-b)%m]=1;R[m+a][m+b][(a-b)%m]=1
            for c in range(m):R[m+a][m+b][m+c]=1
        need(m==6 and 'Example4.5'in p['reference'],'exact literature model premise')
    elif kind=='deligne_product':
        A=p['left_tensor'];B=p['right_tensor'];known=json.loads((ROOT/'lower_rank6_all.json').read_text())+json.loads((ROOT/'lower_rank45_models.json').read_text())
        need(any(r['tensor']==B and r['name']==p['right_name']for r in known),'accepted lower-rank positive factor')
        R=mm.prod(A,B)
    elif kind=='pointed_equivariant':R=equivariant_C2(group_tensor(p['group_table']),p['automorphism'],[0]*len(p['group_table']))
    elif kind=='ty_cyclic_equivariant':
        A=mm.ty(tuple(p['orders']));sigma=p['automorphism'];h=len(A)-1;C=p['bicharacter_exponents'];mod=p['bicharacter_modulus']
        need(len(set(map(tuple,C)))==h and all(C[a][b]==C[b][a]for a,b in itertools.product(range(h),repeat=2)),'explicit symmetric nondegenerate bicharacter')
        G=em.abelian_table(tuple(p['orders']))
        need(all((C[G[a][b]][c]-C[a][c]-C[b][c])%mod==0 for a,b,c in itertools.product(range(h),repeat=3)),'bicharacter multiplication')
        need(all(C[sigma[a]][sigma[b]]==C[a][b]for a,b in itertools.product(range(h),repeat=2)),'orthogonality of TY action')
        need(p['parity'][:-1]==[0]*h and p['parity'][-1]in(0,1),'monoidal parity coherence')
        R=equivariant_C2(A,sigma,p['parity'])
    elif kind=='graded_pullback':
        A=p['left_tensor'];B=p['right_tensor'];g=p['right_grading'];labs=p['labels']
        need(any(r['id']==p['right_id']and r['tensor']==B for r in json.loads((ROOT/'lower_rank8_models.json').read_text())),'actual unitary rank-eight factor')
        need(g[0]==0 and all(g[k]==(g[i]^g[j])for i,j,k in itertools.product(range(8),repeat=3)if B[i][j][k]),'faithful grading')
        need(labs==[[a,b]for a in range(3)for b in range(8)if int(a==2)==g[b]],'complete matching-degree subcategory')
        R=[[[A[a][c][e]*B[b][d][f]for e,f in labs]for c,d in labs]for a,b in labs]
    elif kind=='metaplectic_character_crossed_product':
        B=equivariant_C2(p['TY_tensor'],p['TY_inversion'],p['TY_action_parity']);need(B==p['base_tensor'],'base equivariantization')
        act=p['action'];labs=p['labels'];need(act==[(i^1)if O==[5]else i for i,(O,j)in enumerate(labs)],'categorical parity-character involution')
        R=em.crossed(B,act)
    elif kind=='associative_C2_zest':
        A=rebuild(p['base_constructor'],p['base_parameters']);need(A==p['base_tensor'],'base construction')
        g=p['grading'];h=p['central_invertible'];n=len(A)
        need(g[0]==g[h]==0 and any(g),'neutral central current')
        need(A[h][h]==[1]+[0]*(n-1),'order-two current')
        need(all(g[k]==(g[i]^g[j])for i,j,k in itertools.product(range(n),repeat=3)if A[i][j][k]),'actual C2 grading')
        act=[A[h][i].index(1)for i in range(n)];R=[[[0]*n for _ in range(n)]for _ in range(n)]
        for i,j,k in itertools.product(range(n),repeat=3):R[i][j][act[k]if g[i]*g[j]else k]=A[i][j][k]
    elif kind=='group_theoretical':
        group_tensor(p['group_table']);need(len(p['subgroup'])==2,'independent C2-bimodule control')
        R,info=bimodules(p['group_table'],p['subgroup'][1],lambda a,b,c:0)
    elif kind=='twisted_group_theoretical_c2':
        G=p['group_table'];group_tensor(G);labels=p['quotient_labels'];cp=p['cocycle_parameters']
        if cp['quotient']=='C4':
            wq=lambda a,b,c:cp['cyclic_cocycle_class']*a[0]*((b[0]+c[0])//4)%4
            elements=[(a,)for a in range(4)];add=lambda a,b:((a[0]+b[0])%4,)
        else:
            wq=lambda a,b,c:2*(sum(bit*a[i]*b[j]*c[k]for bit,(i,j,k)in zip(cp['coefficients'],cp['trilinear_terms']))%2)
            elements=list(itertools.product(range(2),repeat=len(labels[0])));add=lambda a,b:tuple(x^y for x,y in zip(a,b))
        need(all(tuple(labels[G[a][b]])==add(labels[a],labels[b])for a,b in itertools.product(range(len(G)),repeat=2)),'actual quotient homomorphism')
        need(all((wq(b,c,d)+wq(a,add(b,c),d)+wq(a,b,c)-wq(add(a,b),c,d)-wq(a,b,add(c,d)))%4==0 for a,b,c,d in itertools.product(elements,repeat=4)),'complete cocycle premise')
        R,info=bimodules(G,p['subgroup_generator'],lambda a,b,c:wq(labels[a],labels[b],labels[c]))
    else:raise ValueError('unverified model constructor '+kind)
    need(R is not None,'categorical construction produces a tensor');common.validate(R);rebuild_cache[key]=R;return R

def verify_fields(R,c,profile):
    f,K,u,d,D,emb=fp_character(R);gate=pu_gate(R,profile);need(gate==c['gate'],'justified PU/Galois-PU bridge')
    result=central_order(R,f,K,u,d,D,emb,gate)
    need(result==c,'exact central field/order obstruction')

def main():
    start=time.monotonic();counts=collections.Counter();ex,models=current()
    need(len(data)==632 and not(set(ex)&set(models)),'complete, disjoint decisions')
    for rid,R in data.items():
        need(common.sha(R)==profiles[rid]['tensor_sha256'],'physical input binding');common.validate(R)
    for r in json.loads((ROOT/'arithmetic.json').read_text()):
        need(common.sha(data[r['id']])==r['tensor_sha256'],'arithmetic binding')
        for c in r['certificates']:arithmetic(data[r['id']],c);counts[c['kind']]+=1
    for r in json.loads((ROOT/'cyclic.json').read_text())['records']:
        if r['certificate']:cyclic(data[r['id']],r['certificate']);counts['cyclic']+=1
    S=json.loads((ROOT/'subrings.json').read_text());classes=S['classes']
    for C in classes:
        need(common.sha(C['tensor'])==C['tensor_sha256'],'subring class binding')
        if C['certificate']:arithmetic(C['tensor'],C['certificate']);counts['direct_lower_arithmetic']+=1
    for r in S['records']:
        R=data[r['id']];n=len(R);du=common.dual(R)
        for rec in r['subrings']:
            J=rec['subset'];p=rec['source_to_class_basis_map'];C=classes[rec['class_index']]['tensor'];m=len(J)
            need(J[0]==0 and all(du[i]in J for i in J)and all(not R[i][j][k]for i in J for j in J for k in range(n)if k not in J),'actual closed based subring')
            need(p[0]==0 and sorted(p)==list(range(m))and all(R[J[i]][J[j]][J[k]]==C[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(m),repeat=3)),'full embedded tensor identification')
            counts['embedded_subring']+=1
    P=ROOT/'sources/evidence/rank11_m1_20261023/work/rank11/structural';sys.path.insert(0,str(P))
    from verify_baseline import spectrum
    for z in json.loads((ROOT/'spectra.json').read_text()).values():
        for r in z['records']:
            if r['certificate']:spectrum(data[r['id']],r['certificate']);counts['spectrum']+=1
    for r in json.loads((ROOT/'field_checks.json').read_text())['records']:
        for c in r['certificates']:verify_fields(data[r['id']],c,profiles[r['id']]);counts['central_field_or_order']+=1
    for r in json.loads((ROOT/'primary_full.json').read_text())['records']:
        c=r['certificate']
        if not c:continue
        R=np.array(data[r['id']],dtype=np.int64);sq=c['squared_dimensions'];need(sq==profiles[r['id']]['squared_dimensions']and sum(sq)==c['global_dimension'],'exact weak-integrality certificate')
        D=sum(sq);need(len(s.factorint(D))<=2,'solvable-to-unitary bridge')
        V=np.array(c['vector'],dtype=np.int64).reshape((12,12,12));cs=[]
        for A in R:
            T=np.einsum('ai,ijk->ajk',A,V);T=np.einsum('bj,ajk->abk',A,T);T=np.einsum('ck,abk->abc',A,T);cs.append(int(np.sum(V*T)))
        need(cs==c['coefficients'],'independent tensor contraction')
        upper=Q(0);scale=10**9
        for a,q in zip(cs,sq):
            lo=math.isqrt(q*scale*scale);hi=lo if lo*lo==q*scale*scale else lo+1
            upper+=Q(a*(hi if a>=0 else lo),q*scale)
        need(upper<0,'exact negative primary quadratic form');counts['primary_full']+=1
    for r in json.loads((ROOT/'feudal.json').read_text())['records']:
        if r['model']:liptrap_positive(data[r['id']],r['model']);counts['Liptrap_unitary']+=1
        if r['certificate']:liptrap_negative(data[r['id']],r['certificate']);counts['Liptrap_complex_obstruction']+=1
    for r in json.loads((ROOT/'lower_known.json').read_text())['class_proofs']:
        R=classes[r['class_index']]['tensor'];c=r['certificate']
        if c['kind']=='liptrap_complex_obstruction':liptrap_negative(R,c)
        elif c['kind'].startswith('central_dimension'):
            du=common.dual(R);G=[i for i in range(len(R))if sum(R[i][du[i]])==1]
            verify_fields(R,c,dict(invertibles=G,squared_dimensions=None))
        else:subprocess.run([sys.executable,str(ROOT/'verify_lower_signed.py')],check=True,capture_output=True,text=True)
        counts['rechecked_lower_result']+=1
    # Module negatives overlap the accepted direct/subring proofs. Replay the
    # complete small finite systems as controls; they add no unsupported status.
    import adapted_module
    for r in json.loads((ROOT/'modules.json').read_text())['records']:
        if not r['certificate']:continue
        R=classes[int(r['id'].rsplit('_',1)[1])]['tensor']if r['id'].startswith('subring_class_')else data[r['id']]
        c=r['certificate'];z=adapted_module.solve(R,c['involution'])
        need(z is not None and not z['feasible'],'complete small involution module contradiction');counts['module_controls']+=1
    for rid,choices in models.items():
        for model in choices:
            if model.get('kind')=='liptrap_unitary_model':liptrap_positive(data[rid],model)
            else:
                M=rebuild(model['constructor'],model['parameters']);stored=model['model_tensor'];p=model['basis_map_source_to_model'];n=12
                # Convolution and stabilizer-trace implementations may choose
                # equivalent module bases, so first bind the constructed model.
                if M!=stored:need(common.based_iso(M,stored)is not None,'independent construction agrees with stored model')
                need(p[0]==0 and sorted(p)==list(range(n)),'unit-preserving basis bijection')
                need(all(data[rid][i][j][k]==stored[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(n),repeat=3)),'all 1728 input/model coefficients')
            counts['accepted_model_identifications']+=1
        counts['modeled_ring']+=1
    unresolved_rows=json.loads((ROOT/'unresolved_families.json').read_text())['records']
    need({r['id']for r in unresolved_rows}==set(data)-set(ex)-set(models),'complete unresolved inventory')
    for r in unresolved_rows:
        R=data[r['id']];need(common.sha(R)==r['tensor_sha256'],'unresolved tensor binding')
        f=exact.poly(r['field_polynomial']);need(f.is_irreducible,'unresolved field definition')
        K=exact.field(f);emb=max(exact.embeddings(f),key=lambda e:e.hi);ds=[K(list(map(s.Rational,v)))for v in r['dimensions_in_field']]
        need(ds[0]==K.one and all(emb.sign(d)>0 for d in ds),'positive unresolved character')
        need(all(sum((K(R[i][j][k])*ds[k]for k in range(12)),K.zero)==ds[i]*ds[j]for i,j in itertools.product(range(12),repeat=2)),'exact unresolved dimension pattern')
        counts['unresolved_exact_pattern']+=1
    need((len(ex),len(models),632-len(ex)-len(models))==(393,127,112),'final counts')
    out=dict(status='PASS',input_count=632,excluded=393,modeled=127,unresolved=112,checks=dict(counts),optimized_python=not __debug__,elapsed_seconds=time.monotonic()-start)
    (ROOT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
