"""Exact Ising-centralizer reconstruction from a frozen induction frontier.

No numerical optimization is used. A surviving modular datum is necessary data,
not a categorification. The adjunction identity V^t V=N_{I(1)} is the key
reduction; the original category is not assumed to split as a tensor product.
"""
import argparse,hashlib,itertools,json,math,time
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as s
from exact import require,evaluate,discover_roots,check_roots,t
from round4_quartic_profiles import enumerate_affine
from round4_quartic_twists import table_for
from round3_m4 import data_for
from spectral_induction import Spectrum
from rings import permute,validate
ROOT=Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def multiply(R,i,v):
    return tuple(sum(R[i][j][k]*v[j] for j in range(len(R))) for k in range(len(R)))


def ising_labels(R,data,columns,lab,g,sigma):
    """Identify the Ising coordinate of every low summand from two S entries."""
    tab=table_for(R,data);pure=lambda i:tuple(int(j==i) for j in range(len(R)))
    sp=Spectrum(tab,columns,[(pure(g)[1:],None),(pure(sigma)[1:],None)])
    types=dict(zip(sp.vectors,sp.types));labels=[]
    for a,v in enumerate(columns):
        d=tab.dims[tuple(v)];u=types[pure(g)][lab[a]]/d;w=types[pure(sigma)][lab[a]]/d
        if u==-data['C'].one and not w:labels.append(2)
        elif u==data['C'].one and w==data['C'].one:labels.append(0)
        elif u==data['C'].one and w==-data['C'].one:labels.append(1)
        else:raise ValueError('incompatible Ising low eigenvalues')
    return labels


def packet_gram(R,columns,high,profile,labels,g,sigma):
    """Enumerate all Ising packets and endpoint orientations up to column copies."""
    counts=Counter(map(tuple,columns));counts.update({(0,)+tuple(v):k for v,k in zip(high,profile) if k});V=sorted(counts);packets={}
    for v in V:
        gv=multiply(R,g,v);sv=multiply(R,sigma,v);pk=Counter([v,gv,sv])
        if all(counts[x]>=k for x,k in pk.items()):packets[tuple(sorted(pk.items()))]=[min(v,gv),max(v,gv),sv]
    packets=list(packets.values());A=[[Counter(p)[v] for p in packets] for v in V]
    bounds=[min(counts[v]//k for v,k in Counter(p).items()) for p in packets]
    covers,stats=enumerate_affine(A,[counts[v] for v in V],bounds)
    wanted=Counter(tuple(v) for v,l in zip(columns,labels) if l==0)
    require(sum(wanted.values())==2 and wanted[tuple(columns[0])]==1,'adjoint algebra must have shape 1+c')
    ccol=next(v for v in wanted if v!=tuple(columns[0]));survivors=[];reports=[]
    for ci,sol in enumerate(covers):
        active=[(p,k) for p,k in zip(packets,sol) if k];ranges=[range(k+1) if p[0]!=p[1] else [k] for p,k in active];tested=0;reject=Counter()
        for choices in itertools.product(*ranges):
            tested+=1;W=[]
            for (p,k),a in zip(active,choices):W +=[p[0]]*a+[p[1]]*(k-a)
            if Counter(v for v in W if v[0])!=wanted:reject['low_Ising_component']+=1;continue
            mat=s.Matrix(W).T;Nc=mat.T*mat-s.eye(len(W))
            if any(x<0 for x in Nc):reject['negative_fusion_entry']+=1;continue
            i=W.index(ccol);j=W.index(tuple(columns[0]))
            if list(Nc[:,j])!=[int(k==i) for k in range(len(W))]:reject['unit_column']+=1;continue
            RFc=sum((ccol[k]*s.Matrix(R[k]).T for k in range(len(R))),s.zeros(len(R)))
            if mat*Nc!=RFc*mat:reject['restriction_product']+=1;continue
            survivors.append(dict(cover=ci,choices=list(choices),W=[list(v) for v in W],Nc=[[int(x) for x in row] for row in Nc.tolist()]))
        reports.append(dict(cover=ci,tested=tested,rejections=dict(reject)))
    return dict(packets=[[list(v) for v in p] for p in packets],covers=[list(v) for v in covers],enumeration=stats,orientations=reports,survivors=survivors)


def dualities(R,W,forced_pairs):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    starcol=lambda v:[v[du[i]] for i in range(n)]
    choices=[[j for j,w in enumerate(W) if w==starcol(v)] for v in W]
    for st in itertools.product(*choices):
        if all(st[st[i]]==i for i in range(len(W))) and all(st[i]==j and st[j]==i for i,j in forced_pairs):yield list(st)


def fusion_system(R,W,Nc,star,ccol):
    """Necessary full fusion tensor equations; x_ijk=N_ij^{k*} is symmetric."""
    r=len(W);unit=W.index([1]+[0]*(len(R)-1));c=W.index(list(ccol));keys=list(itertools.combinations_with_replacement(range(r),3));fixed={};variables={};bounds=[]
    key=lambda i,j,k:tuple(sorted((i,j,star[k])))
    for k in keys:
        if unit in k:
            q=list(k);q.remove(unit);fixed[k]=int(q[0]==star[q[1]])
        elif c in k:
            q=list(k);q.remove(c);fixed[k]=Nc[q[0]][star[q[1]]]
        else:
            bd=10**9
            for i,j,l in [k,(k[1],k[2],k[0]),(k[2],k[0],k[1])]:
                v=W[star[l]];prod=[sum(W[i][a]*W[j][b]*R[a][b][h] for a in range(len(R)) for b in range(len(R))) for h in range(len(R))]
                bd=min(bd,min(prod[h]//v[h] for h in range(len(R)) if v[h]))
            if not bd:fixed[k]=0
            else:variables[k]=len(variables);bounds.append(bd)
    rows=[];rhs=[]
    def add(terms,target):
        row={}
        for k,a in terms:
            if k in fixed:target-=a*fixed[k]
            else:j=variables[k];row[j]=row.get(j,0)+a
        row={j:a for j,a in row.items() if a}
        if row or target:rows.append(row);rhs.append(target)
    for i in range(r):
        for j in range(i,r):
            for h in range(len(R)):
                target=sum(W[i][a]*W[j][b]*R[a][b][h] for a in range(len(R)) for b in range(len(R)))
                add([(key(i,j,k),W[k][h]) for k in range(r) if W[k][h]],target)
    for i in range(r):
        for j in range(r):
            for k in range(r):add([(key(i,j,l),Nc[l][k]) for l in range(r) if Nc[l][k]]+[(key(i,l,k),-Nc[j][l]) for l in range(r) if Nc[j][l]],0)
    for i,j,k in keys:add([(key(i,j,k),1),(key(star[i],star[j],star[k]),-1)],0)
    return dict(W=W,Nc=Nc,star=star,fixed=[[list(k),v] for k,v in fixed.items()],variables=[list(k) for k in variables],upper=bounds,rows=[list(map(list,row.items())) for row in rows],rhs=rhs)


def projected_matrices(system,x):
    """Project exact linear equations to one generator, then impose normality."""
    n=len(system['variables']);project=[j for j,k in enumerate(system['variables']) if x in k];rest=[j for j in range(n) if j not in project];order=rest+project
    rr,piv=s.Matrix([[dict(row).get(j,0) for j in order]+[b] for row,b in zip(system['rows'],system['rhs'])]).rref()
    sub=[list(rr.row(i))[len(rest):] for i,j in enumerate(piv) if j>=len(rest)];A=[];b=[]
    for row in sub:
        den=math.lcm(*(int(s.denom(v)) for v in row));A.append([int(v*den) for v in row[:-1]]);b.append(int(row[-1]*den))
    bounds=[system['upper'][j] for j in project];reorder=sorted(range(len(bounds)),key=lambda j:-bounds[j]);A=[[row[j] for j in reorder] for row in A];bounds=[bounds[j] for j in reorder]
    solutions,stats=enumerate_affine(A,b,bounds);fixed={tuple(k):v for k,v in system['fixed']};variables={tuple(k):j for j,k in enumerate(system['variables'])};r=len(system['W']);star=system['star'];key=lambda i,j,k:tuple(sorted((i,j,star[k])));survivors=[];rejections=[]
    for si,ss in enumerate(solutions):
        vals={project[j]:v for j,v in zip(reorder,ss)}
        def value(k):return fixed[k] if k in fixed else vals[variables[k]]
        M=np.array([[value(key(x,j,k)) for k in range(r)] for j in range(r)],dtype=np.int64);comm=M@M.T-M.T@M
        if np.any(comm):
            a,bb=next(zip(*np.where(comm!=0)));rejections.append([si,int(a),int(bb),int(comm[a,bb])])
        else:survivors.append(dict(solution=si,M=M.tolist(),values=[list(v) for v in vals.items()]))
    return dict(project_variables=len(project),project_equations=len(sub),enumeration=stats,solution_count=len(solutions),rejections=rejections,survivors=survivors)


def complete_generator(system,normal):
    r=len(system['W']);n=len(system['variables']);star=system['star'];fixed={tuple(k):v for k,v in system['fixed']};variables={tuple(k):j for j,k in enumerate(system['variables'])};key=lambda i,j,k:tuple(sorted((i,j,star[k])));rows=[dict(row) for row in system['rows']];b=list(system['rhs']);M=normal['M']
    def add(terms,target):
        row={}
        for k,a in terms:
            if k in fixed:target-=a*fixed[k]
            else:j=variables[k];row[j]=row.get(j,0)+a
        row={j:a for j,a in row.items() if a}
        if row or target:rows.append(row);b.append(target)
    for j,v in normal['values']:rows.append({j:1});b.append(v)
    for i in range(r):
        for j in range(r):
            for k in range(r):add([(key(i,j,l),M[l][k]) for l in range(r) if M[l][k]]+[(key(i,l,k),-M[j][l]) for l in range(r) if M[j][l]],0)
    order=sorted(range(n),key=lambda j:-system['upper'][j]);A=[[row.get(j,0) for j in order] for row in rows];bounds=[system['upper'][j] for j in order];solutions,stats=enumerate_affine(A,b,bounds);survivors=[];rejections=[]
    for si,ss in enumerate(solutions):
        vals=[0]*n
        for j,v in zip(order,ss):vals[j]=v
        def value(k):return fixed[k] if k in fixed else vals[variables[k]]
        N=[[[value(key(i,j,k)) for k in range(r)] for j in range(r)] for i in range(r)];mats=[np.array(m,dtype=np.int64) for m in N];bad=None
        for i in range(r):
            for j in range(r):
                a=mats[i]@mats[j];bb=sum((N[i][j][k]*mats[k] for k in range(r)),np.zeros((r,r),dtype=np.int64))
                if not np.array_equal(a,bb):
                    y,z=next(zip(*np.where(a!=bb)));bad=[si,i,j,int(y),int(z),int(a[y,z]),int(bb[y,z])];break
            if bad:break
        if bad:rejections.append(bad)
        else:
            unit=system['W'].index([1]+[0]*(len(system['W'][0])-1));validate(permute(N,[unit]+[i for i in range(r) if i!=unit]));survivors.append(N)
    return dict(generator_solution=normal['solution'],enumeration=stats,solution_count=len(solutions),rejections=rejections,survivors=survivors)


def field_solve(A,b,K):
    rows=[row[:]+[v] for row,v in zip(A,b)];piv=[];h=0
    for j in range(len(A[0])):
        ii=next((i for i in range(h,len(rows)) if rows[i][j]),None)
        if ii is None:continue
        rows[ii],rows[h]=rows[h],rows[ii];q=rows[h][j];rows[h]=[v/q for v in rows[h]]
        for i in range(len(rows)):
            if i!=h and rows[i][j]:
                q=rows[i][j];rows[i]=[x-q*y for x,y in zip(rows[i],rows[h])]
        piv.append(j);h+=1
        if h==len(rows):break
    if any(not any(row[:-1]) and row[-1] for row in rows):return None,piv
    return rows,piv


def modular_data(R,W,data,component_indices,ising_exponents):
    """All symmetric character labellings and all compatible twist solutions."""
    C=data['C'];n=len(R);unit=W.index([1]+[0]*(len(W[0])-1));order=[unit]+[i for i in range(n) if i!=unit];R=permute(R,order);W=[W[i] for i in order];ds=[sum((C(v[i])*data['dims'][i] for i in range(len(v))),C.zero) for v in W];D=sum((d*d for d in ds),C.zero);N=list(map(s.Matrix,R))
    # Find a small separating pair automatically, with a finite guaranteed fallback.
    seed=None
    for i,j in itertools.combinations(range(1,n),2):
        for k in range(1,4):
            H=N[i]+k*N[j];p=H.charpoly(t).as_poly()
            if s.gcd(p,p.diff()).degree()==0:seed=(i,j,k);break
        if seed:break
    require(seed is not None,'no small separating pair; implementation ineligible')
    V=s.Matrix.hstack(*[(H**i)[0,:].T for i in range(n)]);inv=V.inv();coeff=[list(inv*N[i][0,:].T) for i in range(n)];roots=discover_roots(p,C);require(roots is not None,'character field needs enlargement');check_roots(p,C,roots)
    characters=[tuple(evaluate(list(reversed(co)),root,C) for co in coeff) for root in roots];du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    require(len(set(characters))==n,'incomplete character table')
    require(all(row[i]*row[j]==sum((C(R[i][j][k])*row[k] for k in range(n)),C.zero) for row in characters for i in range(n) for j in range(n)),'character product')
    fs=[sum((row[i]*row[du[i]] for i in range(n)),C.zero) for row in characters];allowed=[[j for j,f in enumerate(fs) if f*ds[i]**2==D] for i in range(n)];allowed[0]=[characters.index(tuple(ds))];assignments=[]
    def dfs(chosen):
        i=len(chosen)
        if i==n:assignments.append(chosen);return
        for j in allowed[i]:
            if j not in chosen and all(ds[i]*characters[j][k]==ds[k]*characters[a][i] for k,a in enumerate(chosen)):dfs(chosen+[j])
    dfs([]);cases=[]
    for si,assignment in enumerate(assignments):
        S=[[ds[j]*characters[assignment[j]][i] for j in range(n)] for i in range(n)]
        require(all(sum((S[i][k]*S[k][j] for k in range(n)),C.zero)==D*C(int(du[i]==j)) for i in range(n) for j in range(n)),'S square')
        for exp in ising_exponents:
            fixed={0:C.one}
            for old,label in component_indices:
                fixed[order.index(old)]=C.one if label==0 else -C.one if label==1 else C.unit**((-exp)%data['F'])
            A=[];b=[]
            for i,v in fixed.items():A.append([C(int(j==i)) for j in range(n)]);b.append(v)
            for i,v in fixed.items():
                for j in range(n):
                    row=[C(R[du[i]][j][k])*ds[k] for k in range(n)];row[j]-=v*S[i][j];A.append(row);b.append(C.zero)
            rr,piv=field_solve(A,b,C);rec=dict(S=si,ising_twist_exponent=exp,linear_rank=len(piv),consistent=rr is not None);cases.append(rec)
            if rr is None:continue
            require(len(piv)==n,'underdetermined twists; implementation incomplete');theta=[C.zero]*n
            for i,j in enumerate(piv):theta[j]=rr[i][-1]
            exponents=[next((i for i in range(data['F']) if v==C.unit**i),None) for v in theta]
            require(all(v is not None for v in exponents),'twists outside proved root set')
            balance=all(sum((C(R[du[i]][j][k])*ds[k]*theta[k] for k in range(n)),C.zero)==theta[i]*theta[j]*S[i][j] for i in range(n) for j in range(n))
            tau=sum((ds[i]**2*theta[i] for i in range(n)),C.zero);sts=all(sum((S[i][k]*theta[k]*S[k][j] for k in range(n)),C.zero)==tau*S[i][j]/(theta[i]*theta[j]) for i in range(n) for j in range(n));charge=tau*C.unit**exp==data['DD']/C(2)
            rec.update(twist_exponents=exponents,full_balance=balance,modular_relation=sts,center_charge_one=charge)
    return dict(order=order,tensor=R,restriction=W,separating_seed=list(seed),roots=[[str(x) for x in v.to_list()] for v in roots],characters=[[[str(x) for x in v.to_list()] for v in row] for row in characters],dimension_coefficients=[[str(x) for x in v.to_list()] for v in ds],allowed=allowed,assignments=assignments,cases=cases)


def reconstruct(R,inherited,progress=None):
    data=data_for(R,3);recognition=inherited['recognized_subcategories'];require(len(recognition['ising_pairs'])==1,'one Ising pair required');g,sigma=recognition['ising_pairs'][0]
    cases=[q for q in inherited['cases'] if 'variables' in q or q.get('retained_without_exact_decision')];profiles=[];done={};lab_checks=[]
    for case in cases:
        low=case['low'];br=inherited['profiles']['branches'][low];lab=case['lab'];labels=ising_labels(R,data,br['columns'],lab,g,sigma);tab=table_for(R,data)
        conjugate=lambda x:evaluate(x.to_list(),data['C'].unit**(data['F']-1),data['C'])
        low_star=[lab.index(tab.rows.index(tuple(conjugate(x) for x in tab.rows[lab[a]]))) for a in range(len(R))]
        siglow=[a for a,l in enumerate(labels) if l==2]
        require(len(siglow)==2 and low_star[siglow[0]]==siglow[1] and low_star[siglow[1]]==siglow[0],'sigma low summands must be a dual pair')
        lab_checks.append(dict(low=low,labelling=lab,labels=labels,dual=low_star));key=(low,case['profile_index'])
        if key in done:
            require(done[key]==(labels,low_star),'deduplicated low labellings differ')
            continue
        done[key]=(labels,low_star);pcase=next(x for x in br['cases'] if x['labelling']==lab);profile=next(q for q in pcase['survivors'] if q['profile_index']==case['profile_index']);counts=Counter(map(tuple,br['columns']));counts.update({(0,)+tuple(v):k for v,k in zip(br['high_vectors'],profile['counts']) if k})
        require(counts[tuple(int(j==g) for j in range(len(R)))]==1 and counts[tuple(int(j==sigma) for j in range(len(R)))]==1,'Ising lifts not unique')
        pkt=packet_gram(R,br['columns'],br['high_vectors'],profile['counts'],labels,g,sigma);rec=dict(low=low,profile_index=profile['profile_index'],center_rank=profile['rank'],packets=pkt,fusion_cases=[]);profiles.append(rec)
        for pi,p in enumerate(pkt['survivors']):
            W=p['W'];Nc=p['Nc'];r=len(W);ccol=next(v for v,l in zip(br['columns'][1:],labels[1:]) if l==0)
            # Two nonreal low summands in the sigma coordinate force a dual pair in E.
            sigcols=[v for v,l in zip(br['columns'],labels) if l==2];require(len(sigcols)==2 and sigcols[0]==sigcols[1],'sigma low support ineligible')
            mids=[i for i,v in enumerate(W) if multiply(R,sigma,v)==tuple(sigcols[0])];require(len(mids)==2,'sigma representatives not unique')
            pure=[i for i,v in enumerate(W) if sum(v)==1 and v[0]==0 and v.index(1) not in (g,sigma)];require(pure,'no small projected generator');x=next((i for i in pure if W[i].index(1)==1),pure[0])
            for st in dualities(R,W,[tuple(mids)]):
                system=fusion_system(R,W,Nc,st,ccol);proj=projected_matrices(system,x);fc=dict(packet=pi,star=st,system_sha256=digest(system),system_shape=[len(system['rows']),len(system['variables'])],generator=x,projection=proj,completions=[]);rec['fusion_cases'].append(fc)
                for normal in proj['survivors']:fc['completions'].append(complete_generator(system,normal))
                if progress:progress('fusion',profile['rank'],st,proj['solution_count'],len(proj['survivors']),sum(len(q['survivors']) for q in fc['completions']))
        tensors=[(fc['packet'],N) for fc in rec['fusion_cases'] for co in fc['completions'] for N in co['survivors']];rec['fusion_orbits']=[]
        for pi,N in tensors:
            W=pkt['survivors'][pi]['W'];groups={tuple(v):[i for i,w in enumerate(W) if w==v] for v in W};matched=False
            for oi,orb in enumerate(rec['fusion_orbits']):
                if orb['packet']!=pi:continue
                for dst in itertools.product(*(list(itertools.permutations(v)) for v in groups.values())):
                    pp=list(range(len(W)))
                    for src,tar in zip(groups.values(),dst):
                        for a,b in zip(src,tar):pp[a]=b
                    if permute(N,pp)==orb['tensor']:orb['members'].append(dict(tensor_sha256=digest(N),permutation=pp));matched=True;break
                if matched:break
            if not matched:rec['fusion_orbits'].append(dict(packet=pi,tensor=N,members=[dict(tensor_sha256=digest(N),permutation=list(range(len(W))))]))
        for orb in rec['fusion_orbits']:
            W=pkt['survivors'][orb['packet']]['W'];indices=[]
            for col,l in zip(br['columns'][1:],labels[1:]):
                if l==0:ids=[W.index(col)]
                elif l==1:ids=[W.index(list(multiply(R,g,col)))]
                else:ids=[i for i,v in enumerate(W) if multiply(R,sigma,v)==tuple(col)]
                indices.extend((i,l) for i in ids)
            exponents=[a for a in range(1,data['F'],2) if data['C'].unit**(2*a)+data['C'].unit**((-2*a)%data['F'])==data['C'](case['indicators'][sigma-1])*data['dims'][sigma]]
            orb['modular']=modular_data(orb['tensor'],W,data,indices,exponents)
            if progress:progress('modular',profile['rank'],len(orb['members']),len(orb['modular']['assignments']),sum(c['consistent'] for c in orb['modular']['cases']))
    return dict(kind='ising_centralizer_full_reconstruction',version=1,scope='general_necessary_center_fusion_and_modular_data',source_sha256=digest(inherited),ising_pair=[g,sigma],low_labellings=lab_checks,profiles=profiles,categorification_claimed=False)


def summary(c):
    return dict(passed=True,optimizer_used=False,categorification_claimed=False,profiles=[dict(center_rank=p['center_rank'],fusion_tensors=sum(len(q['survivors']) for f in p['fusion_cases'] for q in f['completions']),fusion_orbits=len(p['fusion_orbits']),modular_data=sum(q['consistent'] and q.get('full_balance') and q.get('modular_relation') and q.get('center_charge_one') for o in p['fusion_orbits'] for q in o['modular']['cases'])) for p in c['profiles']])


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--id',default='R6_4_91');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify',action='store_true');ap.add_argument('--replay-inherited',action='store_true');a=ap.parse_args();R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==a.id);source=ROOT/f'research/round4/quartic_front/{a.id}_frontier_certificate.json';inherited=json.load(open(source))['certificate']
    if a.verify:
        import scipy.optimize
        def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied
    if a.replay_inherited:
        from round4_quartic_twists import verify
        print(json.dumps({'inherited':verify(R,inherited)}),flush=True)
    st=time.monotonic();cert=reconstruct(R,inherited,progress=lambda *q:print(q,flush=True))
    if a.verify:require(cert==json.load(open(a.output))['certificate'],'reconstructed certificate differs')
    else:a.output.write_text(json.dumps(dict(id=a.id,certificate=cert),separators=(',',':'))+'\n')
    print(json.dumps({**summary(cert),'seconds':time.monotonic()-st}),flush=True)
