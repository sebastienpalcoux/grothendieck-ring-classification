"""Exact full regular-action and modular completion of the R6_4_22 frontier.

Only necessary central fusion and modular data are asserted. The complete
finite word-Gram domains, integral counts, dualities and regular actions are
reconstructed without numerical optimization.
"""
import argparse,itertools,json,time
from pathlib import Path
from collections import defaultdict
import numpy as np
import sympy as s
from exact import require,evaluate,discover_roots,check_roots,t
from round3_m4 import data_for
from spectral_induction import Spectrum
from round5_unified import low_word_data,joint_coefficient_domains,count_system
from round4_quartic_profiles import enumerate_affine
from round5_low_actions import low_action_system,general_action_system,enumerate_actions,spectral_polynomial
from round5_quartic_pair import digest,field_solve
ROOT=Path(__file__).resolve().parents[1]


def conjugate_dualities(R,wd,high):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)];stlow=wd['low_duality'];wi={tuple(w):j for j,w in enumerate(wd['words'])};pw=[wi[tuple(sorted(stlow[a] for a in w))] for w in wd['words']]
    choices=[[j+n for j,(w,y) in enumerate(high) if w==[v[du[k]] for k in range(n)] and y==[x[k] for k in pw]] for v,x in high]
    for hst in itertools.product(*choices):
        star=stlow+list(hst)
        if all(star[star[i]]==i for i in range(len(star))):yield star


def fusion_check(N,star):
    n=len(N);bound=max(x for m in N for row in m for x in row);require(n*bound*bound<2**62,'integer matrix bound exceeds implementation range');M=[np.array(v,dtype=np.int64) for v in N]
    require(all(N[i][j][0]==int(star[i]==j) and N[i][j]==N[j][i] for i in range(n) for j in range(n)),'unit/duality/commutativity')
    require(N[0]==[[int(i==j) for j in range(n)] for i in range(n)],'unit')
    require(all(np.array_equal(M[i]@M[j],sum((N[i][j][k]*M[k] for k in range(n)),np.zeros((n,n),dtype=np.int64))) for i in range(n) for j in range(n)),'associativity')


def center_modular(N,W,star,data,low,high,labs,progress=None):
    C=data['C'];F=data['F'];n=len(N);ds=[sum((C(v[i])*data['dims'][i] for i in range(len(v))),C.zero) for v in W];D=sum((v*v for v in ds),C.zero);mats=list(map(s.Matrix,N));seed=None
    for i,j in itertools.combinations(range(1,n),2):
        for k in range(1,4):
            H=mats[i]+k*mats[j];p=H.charpoly(t).as_poly()
            if s.gcd(p,p.diff()).degree()==0:seed=(i,j,k);break
        if seed:break
    require(seed is not None,'no small separating pair; incomplete implementation')
    V=s.Matrix.hstack(*[(H**i)[0,:].T for i in range(n)]);inv=V.inv();coeff=[list(inv*mats[i][0,:].T) for i in range(n)];roots=discover_roots(p,C);require(roots is not None,'character field requires enlargement');check_roots(p,C,roots);chars=[tuple(evaluate(list(reversed(co)),root,C) for co in coeff) for root in roots]
    require(all(row[i]*row[j]==sum((C(N[i][j][k])*row[k] for k in range(n)),C.zero) for row in chars for i in range(n) for j in range(n)),'character products')
    fs=[sum((row[i]*row[star[i]] for i in range(n)),C.zero) for row in chars];bydim=[[j for j,f in enumerate(fs) if f*ds[i]**2==D] for i in range(n)];bydim[0]=[chars.index(tuple(ds))];sp=Spectrum(data['tab'],low,[(tuple(v),None) for v in high]);types=dict(zip(sp.vectors,sp.types));lab_cases=[]
    for lab in labs:
        allowed=[[j for j in choices if all(chars[j][a]==types[tuple(W[i])][lab[a]] for a in range(len(low)))] for i,choices in enumerate(bydim)];assignments=[]
        def dfs(chosen):
            i=len(chosen)
            if i==n:assignments.append(chosen);return
            for j in allowed[i]:
                if j not in chosen and all(ds[i]*chars[j][k]==ds[k]*chars[a][i] for k,a in enumerate(chosen)):dfs(chosen+[j])
        dfs([]);cases=[]
        for si,ass in enumerate(assignments):
            S=[[ds[j]*chars[ass[j]][i] for j in range(n)] for i in range(n)];require(all(sum((S[i][k]*S[k][j] for k in range(n)),C.zero)==D*C(int(star[i]==j)) for i in range(n) for j in range(n)),'S square');A=[];b=[]
            for i in range(len(low)):A.append([C(int(j==i)) for j in range(n)]);b.append(C.one)
            for i in range(len(low)):
                for j in range(n):
                    row=[C(N[star[i]][j][k])*ds[k] for k in range(n)];row[j]-=S[i][j];A.append(row);b.append(C.zero)
            rr,piv=field_solve(A,b,C);case=dict(S=si,consistent=rr is not None,linear_rank=len(piv));cases.append(case)
            if rr is None:continue
            require(len(piv)==n,'underdetermined twists; incomplete implementation');theta=[C.zero]*n
            for i,j in enumerate(piv):theta[j]=rr[i][-1]
            exps=[next((e for e in range(F) if v==C.unit**e),None) for v in theta];require(all(v is not None for v in exps),'forced twist outside certified root set')
            balance=all(sum((C(N[star[i]][j][k])*ds[k]*theta[k] for k in range(n)),C.zero)==theta[i]*theta[j]*S[i][j] for i in range(n) for j in range(n));tau=sum((ds[i]**2*theta[i] for i in range(n)),C.zero);sts=all(sum((S[i][k]*theta[k]*S[k][j] for k in range(n)),C.zero)==tau*S[i][j]/(theta[i]*theta[j]) for i in range(n) for j in range(n));case.update(twist_exponents=exps,full_balance=balance,modular_relation=sts,charge_one=tau==data['DD'])
        lab_cases.append(dict(labelling=lab,allowed=allowed,assignments=assignments,cases=cases))
        if progress:progress('modular',lab,len(assignments),[(c['consistent'],c['linear_rank']) for c in cases])
    return dict(separating_seed=list(seed),roots=[[str(x) for x in v.to_list()] for v in roots],characters=[[[str(x) for x in v.to_list()] for v in row] for row in chars],dimensions=[[str(x) for x in v.to_list()] for v in ds],labellings=lab_cases)


def reconstruct(R,inherited,progress=None):
    data=data_for(R,3,20);n=len(R);oldcases=[q for q in inherited['cases'] if q.get('rank')==36];require(len(oldcases)==2,'wrong inherited rank36 branches');rec=oldcases[0];br=inherited['profiles']['branches'][rec['low']];getprofile=lambda c:next(p for q in br['cases'] if q['labelling']==c['lab'] for p in q['survivors'] if p['profile_index']==c['profile_index']);profile=getprofile(rec);words=list(itertools.combinations_with_replacement(range(1,n),2))+list(itertools.combinations_with_replacement(range(1,n),3));wd=low_word_data(R,data,br['columns'],br['high_vectors'],profile['counts'],rec['lab'],words=words);labchecks=[]
    for case in oldcases:
        require(case['low']==rec['low'] and getprofile(case)['counts']==profile['counts'],'rank36 profiles differ');other=low_word_data(R,data,br['columns'],br['high_vectors'],profile['counts'],case['lab'],words=words);require(other==wd,'conjugate low-word data differ');labchecks.append(case['lab'])
    dom=joint_coefficient_domains(wd,node_limit=3000000,time_limit=60);require(dom['complete'],'word coefficient domains incomplete');ss=count_system(wd,dom);rows=[{int(j):v for j,v in row.items()} for row in ss['rows']];bounds=[None]*len(ss['labels'])
    for row,b,desc in zip(rows,ss['rhs'],ss['descriptions']):
        if desc[0]=='count':
            for j,v in row.items():require(v==1);bounds[j]=b
    require(all(v is not None for v in bounds));order=sorted(range(len(bounds)),key=lambda j:-bounds[j]);solutions,stats=enumerate_affine([[row.get(j,0) for j in order] for row in rows],ss['rhs'],[bounds[j] for j in order]);sols=[]
    for sol in solutions:
        v=[0]*len(bounds)
        for j,x in zip(order,sol):v[j]=x
        sols.append(v)
    if progress:progress('cubic_counts',len(sols),stats)
    sp=Spectrum(data['tab'],br['columns'],[(tuple(v),None) for v in br['high_vectors']]);types=dict(zip(sp.vectors,sp.types));cols=list(map(tuple,br['columns']))+[(0,)+tuple(v) for v,m in zip(br['high_vectors'],profile['counts']) for _ in range(m)];polys={a:spectral_polynomial(data['C'],[types[v][rec['lab'][a]] for v in cols]) for a in range(1,n)};action_cases=[];orbits=[]
    for si,sol in enumerate(sols):
        high=[lab for ct,lab in zip(sol,ss['labels']) for _ in range(ct)];W=br['columns']+[v for v,x in high];r=len(W);U=[wd['low_coefficients'][j]+[x[j] for v,x in high] for j in range(len(words))]
        for star in conjugate_dualities(R,wd,high):
            case=dict(pattern=si,star=star,actions=[]);action_cases.append(case);active=[{}]
            for a in [1,2,3,4]:
                alive=[]
                for bi,known in enumerate(active):
                    system=low_action_system(R,W,star,words,U,a,known_actions=list(known.values()),trace=-polys[a][1]);result=enumerate_actions(system,expected_charpoly=polys[a]);case['actions'].append(dict(a=a,previous_branch=bi,system_sha256=digest(system),result=result))
                    for M in result['matrices']:
                        nxt={**known,a:M}
                        if star[a]!=a:nxt[star[a]]=[list(v) for v in zip(*M)]
                        alive.append(nxt)
                active=alive
                if not active:break
            case['complete_low_actions']=active
            if progress:progress('low_actions',si,star,len(active))
            groups=defaultdict(list)
            for j,(v,x) in enumerate(high,n):groups[(tuple(v),tuple(x))].append(j)
            for known in active:
                matched=False
                for oi,orb in enumerate(orbits):
                    if orb['W']!=W or orb['star']!=star:continue
                    for dst in itertools.product(*(list(itertools.permutations(v)) for v in groups.values())):
                        pp=list(range(r))
                        for src,tar in zip(groups.values(),dst):
                            for x,y in zip(src,tar):pp[x]=y
                        if not all(pp[star[i]]==star[pp[i]] for i in range(r)):continue
                        if all([[known[a][pp[i]][pp[j]] for j in range(r)] for i in range(r)]==orb['low_actions'][a] for a in known):orb['members'].append(dict(pattern=si,permutation=pp));matched=True;break
                    if matched:break
                if not matched:orbits.append(dict(W=W,star=star,low_actions=known,members=[dict(pattern=si,permutation=list(range(r)))]))
    for orb in orbits:
        W=orb['W'];star=orb['star'];r=len(W);active=[orb['low_actions']];stages=[];orb['completion']=stages;pure=[i for i,v in enumerate(W) if v==[0,1,0,0,0,0]];require(len(pure)==1,'unique small pure generator required')
        inv=[i for i in range(n) if sum(R[i][next(j for j in range(n) if R[i][j][0])])==1]
        first=pure+[j for j,v in enumerate(W) if j and sum(v)==1 and v.index(1) in inv]
        order=first+[i for i in range(1,r) if i not in first]
        for a in order:
            alive=[];stage=dict(a=a,branches=[])
            for bi,known in enumerate(active):
                if a in known:alive.append(known);continue
                system=general_action_system(R,W,star,a,known);result=enumerate_actions(system);normal=[]
                for ix,M in enumerate(result['matrices']):
                    bound=max(map(max,M));require(r*bound*bound<2**62);B=np.array(M,dtype=np.int64)
                    if np.array_equal(B@B.T,B.T@B):normal.append(ix)
                stage['branches'].append(dict(previous=bi,system_sha256=digest(system),result=result,normal_indices=normal))
                for ix in normal:
                    M=result['matrices'][ix];nxt={**known,a:M}
                    if star[a]!=a:nxt[star[a]]=[list(v) for v in zip(*M)]
                    alive.append(nxt)
            if stage['branches']:stages.append(stage)
            active=alive
            if not active:break
        tensors=[]
        for known in active:
            N=[[[int(i==j) for j in range(r)] for i in range(r)]]+[known[a] for a in range(1,r)];fusion_check(N,star);tensors.append(N)
        orb['fusion_tensors']=tensors;orb['modular']=[center_modular(N,W,star,data,br['columns'],br['high_vectors'],labchecks,progress) for N in tensors]
        if progress:progress('full_fusion',len(tensors))
    return dict(kind='quartic_full_regular_completion',version=1,scope='general_necessary_center_fusion_and_modular_data',source_sha256=digest(inherited),rank=36,labellings=labchecks,word_data=wd,domains=dom,count_system_sha256=digest(ss),count_enumeration=stats,count_solutions=sols,low_action_cases=action_cases,orbits=orbits,categorification_claimed=False)


def summary(cert):
    return dict(passed=True,optimizer_used=False,categorification_claimed=False,cubic_patterns=len(cert['count_solutions']),duality_cases=len(cert['low_action_cases']),low_action_orbits=len(cert['orbits']),fusion_tensors=sum(len(o['fusion_tensors']) for o in cert['orbits']),modular_data=sum(c['consistent'] and c.get('full_balance') and c.get('modular_relation') and c.get('charge_one') for o in cert['orbits'] for m in o['modular'] for l in m['labellings'] for c in l['cases']))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify',action='store_true');a=ap.parse_args();R=next(v['N'] for v in json.load(open(ROOT/'data/census.json')) if v['id']=='R6_4_22');old=json.load(open(ROOT/'research/round4/quartic_front/R6_4_22_frontier_certificate.json'))['certificate']
    if a.verify:
        import scipy.optimize
        def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied
    st=time.monotonic();cert=reconstruct(R,old,lambda *x:print(x,flush=True));cert=json.loads(json.dumps(cert))
    if a.verify:require(cert==json.load(open(a.output))['certificate'],'reconstructed certificate differs')
    else:a.output.write_text(json.dumps(dict(id='R6_4_22',certificate=cert),separators=(',',':'))+'\n')
    print(json.dumps({**summary(cert),'seconds':time.monotonic()-st}),flush=True)
