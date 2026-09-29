"""Exhaustive induction profiles in a supported quartic character field.

This is a necessary-data reduction, not a categorification or exclusion result.
It uses exact bounded affine-lattice enumeration and low-word integrality.
"""
import argparse,hashlib,itertools,json,math,signal,time
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as s
from exact import require,vector,evaluate
from character_induction import Ineligible
from induction import low_failure
from round3_m4 import data_for as ambient_data,high_vectors
from spectral_induction import Spectrum
ROOT=Path(__file__).resolve().parents[1]


def enumerate_affine(A,b,bounds,node_limit=5000000):
    """Enumerate every bounded integral solution of Ax=b, with exact pruning."""
    n=len(bounds);M=s.Matrix([list(row)+[rhs] for row,rhs in zip(A,b)])
    rr,piv=M.rref()
    if n in piv:return [],{'inconsistent':True,'nodes':0,'rank':len(piv)-1,'free_variables':0}
    free=[j for j in range(n) if j not in piv];co=[[int(i==j) for j in free] for i in range(n)];const=[0]*n;den=[1]*n
    for row,i in enumerate(piv):
        pp=[Fraction(rr[row,-1])]+[-Fraction(rr[row,j]) for j in free];dd=math.lcm(*(x.denominator for x in pp));den[i]=dd;const[i]=int(pp[0]*dd);co[i]=[int(x*dd) for x in pp[1:]]
    order=sorted(range(len(free)),key=lambda j:(bounds[free[j]],-sum(abs(c[j]) for c in co)))
    co=[[c[j] for j in order] for c in co];ub=[bounds[free[j]] for j in order];m=len(free)
    mn=[[0]*n for _ in range(m+1)];mx=[[0]*n for _ in range(m+1)]
    for level in range(m-1,-1,-1):
        for i in range(n):
            z=co[i][level]*ub[level];mn[level][i]=mn[level+1][i]+min(0,z);mx[level][i]=mx[level+1][i]+max(0,z)
    out=[];nodes=0
    def dfs(level,partial):
        nonlocal nodes
        nodes+=1
        if nodes>node_limit:raise TimeoutError('exact profile node budget; no completeness claim')
        if any(p+mx[level][i]<0 or p+mn[level][i]>bounds[i]*den[i] for i,p in enumerate(partial)):return
        if level==m:
            if all(p%den[i]==0 for i,p in enumerate(partial)):out.append(tuple(p//den[i] for i,p in enumerate(partial)))
            return
        for x in range(ub[level]+1):dfs(level+1,[p+co[i][level]*x for i,p in enumerate(partial)])
    dfs(0,const);out.sort()
    require(all(all(sum(a*x for a,x in zip(row,v))==rhs for row,rhs in zip(A,b)) for v in out),'affine enumeration integrity')
    return out,dict(inconsistent=False,nodes=nodes,rank=len(piv),free_variables=m,free_bounds=ub)


def profile_domain(data,cols,node_limit):
    tab=data['tab'];n=tab.n;G,V=high_vectors(data,cols);sp=Spectrum(tab,cols,[(v,None) for v in V])
    bad=set(map(tuple,sp.forbidden));V=[v for v in V if v not in bad]
    if sp.missing_low:return None,dict(spectrum=sp.metadata(),missing_low=True)
    A=[];b=[]
    for i in range(n-1):
        for j in range(i,n-1):A.append([v[i]*v[j] for v in V]);b.append(int(G[i,j]))
    aa,bb=sp.balance([(v,None) for v in V],len(V));A+=aa;b+=bb
    bounds=[min(int(G[i,i])//(v[i]*v[i]) for i in range(n-1) if v[i]) for v in V]
    profiles,stats=enumerate_affine(A,b,bounds,node_limit)
    return (V,sp,profiles),dict(spectrum=sp.metadata(),high_vectors=list(map(list,V)),gram=list(map(list,[[int(G[i,j]) for j in range(n-1)] for i in range(n-1)])),enumeration=stats,gram_galois_profiles=list(map(list,profiles)))


def word_forms(data,cols,V,sp,lab,height):
    """Exact integer coefficient forms for all nonunit low words of one degree."""
    tab=data['tab'];C=data['C'];typ=dict(zip(sp.vectors,sp.types));allv=list(dict.fromkeys(map(tuple,cols)))+[(0,)+v for v in V];lows=Counter(map(tuple,cols));ww={v:tab.dims[v]**2/tab.D**2 for v in allv}
    powers={v:[[C.one]+[typ[v][lab[a]]**k for k in range(1,height+1)] for a in range(1,tab.n)] for v in allv}
    for word in itertools.combinations_with_replacement(range(1,tab.n),height):
        weights=dict(ww)
        for a,k in Counter(word).items():
            for v in allv:weights[v]*=powers[v][a-1][k]
        const=sum((C(k)*weights[v] for v,k in lows.items()),C.zero)
        vv=[vector(x,C.mod.degree()) for x in [const]+[weights[(0,)+v] for v in V]];forms=[]
        for h in range(C.mod.degree()):
            values=[Fraction(x[h]) for x in vv];den=math.lcm(*(x.denominator for x in values));forms.append((den,tuple(int(x*den) for x in values)))
        yield word,forms


def moment_value(forms,profile):
    numer=[row[0]+sum(a*b for a,b in zip(row[1:],profile)) for den,row in forms]
    good=not any(numer[1:]) and numer[0]>=0 and numer[0]%forms[0][0]==0
    return good,(numer[0]//forms[0][0] if good else [str(Fraction(z,forms[j][0])) for j,z in enumerate(numer)])


def filter_profiles(R,data,cols,V,sp,profiles,lab,height):
    tab=data['tab'];C=data['C'];n=len(R);active={i:list(p) for i,p in enumerate(profiles)};rejected=[];triples={i:{} for i in active};counts={}
    for degree in range(3,height+1):
        nw=0
        for word,forms in word_forms(data,cols,V,sp,lab,degree):
            nw+=1
            for i,p in list(active.items()):
                ok,value=moment_value(forms,p)
                if not ok:
                    rejected.append(dict(profile_index=i,reason='low_word_multiplicity',word=list(word),power_basis_value=value));del active[i]
                elif degree==3:triples[i][word]=value
        counts[str(degree)]=nw
        if degree==3:
            conjugate=lambda x:evaluate(x.to_list(),C.unit**(data['F']-1),C)
            star=[lab.index(tab.rows.index(tuple(conjugate(x) for x in tab.rows[lab[a]]))) for a in range(n)]
            for ix,p in list(active.items()):
                bad=None
                for a,b in itertools.combinations_with_replacement(range(1,n),2):
                    prod=[sum(cols[a][j]*cols[b][k]*R[j][k][i] for j in range(n) for k in range(n)) for i in range(n)]
                    residual=[prod[i]-int(a==star[b] and i==0)-sum(triples[ix][tuple(sorted((a,b,star[c]))) ]*cols[c][i] for c in range(1,n)) for i in range(n)]
                    if any(v<0 for v in residual):bad=dict(profile_index=ix,reason='negative_restriction_remainder',pair=[a,b],remainder=residual);break
                if bad:rejected.append(bad);del active[ix]
        counts['survivors_after_'+str(degree)]=len(active)
    return dict(labelling=list(lab),word_counts=counts,rejected=rejected,survivors=[dict(profile_index=i,counts=p,rank=len(cols)+sum(p),low_triples=[dict(word=list(w),multiplicity=z) for w,z in sorted(triples[i].items())]) for i,p in active.items()])


def certificate(R,height=6,node_limit=5000000,progress=None):
    require(type(height) is int and 3<=height<=8,'unsupported word height')
    from rings import Characters
    ch=Characters(R)
    if ch.fp()[0].degree()!=4:raise Ineligible('quartic FP field required by this implementation')
    data=ambient_data(R,3);tab=data['tab'];branches=[]
    for ix,cols in enumerate(data['lows']):
        br={'columns':list(map(list,cols))};branches.append(br)
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:br['ordinary']=why;continue
        labs=tab.assignments(cols);br['labellings']=list(map(list,labs))
        if not labs:continue
        domain,rec=profile_domain(data,cols,node_limit);br.update(rec)
        if domain is None:continue
        V,sp,profiles=domain;br['cases']=[]
        for lab in labs:
            case=filter_profiles(R,data,cols,V,sp,profiles,lab,height);br['cases'].append(case)
            if progress:progress(ix,lab,len(profiles),len(case['survivors']))
    return {'kind':'quartic_exact_induction_profiles','version':1,'scope':'pseudo_unitary_necessary_profiles','height':height,'node_limit':node_limit,'ambient_conductor':data['F'],'columns_counts':list(map(len,data['columns'])),'table':tab.metadata(),'branches':branches,'categorification_claimed':False}


def verify(R,c):
    require(c.get('kind')=='quartic_exact_induction_profiles' and c.get('version')==1,'wrong exact-profile record')
    rebuilt=certificate(R,c['height'],c['node_limit']);require(rebuilt==c,'profile certificate differs from exhaustive exact reconstruction')
    return dict(passed=True,scope=c['scope'],optimizer_used=False,low_frames=len(c['branches']),survivors_by_branch=[dict(low=i,labelling=x['labelling'],profiles=len(x['survivors']),ranks=[p['rank'] for p in x['survivors']]) for i,br in enumerate(c['branches']) for x in br.get('cases',[])])


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('id');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--height',type=int,default=6);ap.add_argument('--verify',action='store_true');ap.add_argument('--seconds',type=int,default=840);a=ap.parse_args();R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==a.id)
    def stop(*_):raise TimeoutError('explicit wall-time budget; incomplete computation')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds);st=time.monotonic()
    if a.verify:
        import scipy.optimize
        def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during exact replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied;print(json.dumps(verify(R,json.load(open(a.output))['certificate']),indent=2))
    else:
        try:c=certificate(R,a.height,progress=lambda *v:print(v,flush=True));rec=dict(id=a.id,outcome='exact_necessary_profile_reduction',certificate=c)
        except (Ineligible,TimeoutError) as e:rec=dict(id=a.id,outcome='ineligible' if isinstance(e,Ineligible) else 'budget_incomplete',reason=str(e))
        rec['seconds']=time.monotonic()-st;a.output.write_text(json.dumps(rec,separators=(',',':'))+'\n');print({k:v for k,v in rec.items() if k!='certificate'},flush=True)
