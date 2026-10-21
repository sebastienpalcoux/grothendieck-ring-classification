"""Independent scratch-only reconstruction of the R1154 quartic bound.
Uses no functions from either follow-up producer. Read-only unless --write.
"""
import argparse, hashlib, itertools, json, math, sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=Path.cwd())
ap.add_argument('--write',action='store_true')
args=ap.parse_args();root=args.root.resolve()
p=root/'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0,str(p))
import central_support as c
import character_modular as md
import rotation_search as base
base.install();s=c.s

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(f):return json.loads(f.read_text())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rational(z):
    co=list(map(s.Rational,c.ec(z)));need(len(co)<=1,'rational value');return co[0] if co else s.S.Zero
record=next(r for r in read(c.OLD.parent/'pipeline/census_m3.json') if r['id']=='R8_3_1154')
R=record['tensor'];a=c.w.data(R);K=a['K'];low=a['lows'][31]
chars=md.characters(R,a)
need(all(ch[j]==ch[a['du'][j]] for ch in chars for j in range(8)),'selfdual low objects')
need(md.assignments(a,chars,low)==[(0,1,2,3,4)],'complete character assignment')
L=s.Matrix.hstack(*map(s.Matrix,low));Q7,high=md.full.base.grams.high_columns(a,L)
columns=list(map(tuple,low))+[(0,)+tuple(v) for v,z in high]
d=[sum((K(n)*di for n,di in zip(v,a['ds'])),K.zero) for v in columns]
sv=[[a['D']/a['codegrees'][i]/K(a['multiplicities'][i])*md.value(chars[i],v,K) for v in columns] for i in range(5)]
need(sv[0]==d,'FP normalization')
triples=list(itertools.combinations_with_replacement(range(1,5),3))
quads=list(itertools.combinations_with_replacement(range(1,5),4))
pairs=list(itertools.combinations_with_replacement(range(1,5),2))
def coefficients(word):
    vv=[]
    for z in range(len(columns)):
        v=K.one
        for i in word:v*=sv[i][z]
        vv.append(v/(a['D']**2*d[z]**(len(word)-2)))
    vv=[sum(vv[:5],K.zero)]+vv[5:]
    co=[]
    for v in vv:
        q=list(map(s.Rational,c.ec(v)));need(len(q)<=2,'quadratic coordinates');co.append([s.S.Zero]*(2-len(q))+q)
    den=math.lcm(*(int(q.q) for v in co for q in v))
    return [[int(q*den) for q in v] for v in co],den
rows=[coefficients(word) for word in triples+quads]
domain=read(p.parent/'central_integrality/integer_gram_1154.json')
need(domain['high_columns']==[list(v) for v,z in high] and domain['low_columns']==[list(v) for v in low],'ordered complete source column binding')
V=s.Matrix.hstack(*(s.Matrix(v) for v in columns[5:]))
Q=s.zeros(8);Q[1:,1:]=Q7
Qplus=Q.pinv();need(Q*Qplus*Q==Q,'Moore-Penrose restriction inverse')
groups={};all_indices=[];excluded=[];survived=[]
producer=read(HERE/'r1154_quartic_necessary_filters.json')
for ix,counts in enumerate(domain['completions']):
    need(len(counts)==16 and all(type(v) is int and v>=0 for v in counts),'nonnegative integer pattern')
    values=[];cubic_ok=True
    for k,(co,den) in enumerate(rows):
        x=[1]+counts;irr=sum(n*z[0] for n,z in zip(x,co));num=sum(n*z[1] for n,z in zip(x,co))
        if k<len(triples) and (irr or num<0 or num%den):cubic_ok=False;break
        need(not irr and num>=0 and num%den==0,'scalar quartic integrality')
        values.append(num//den)
    if not cubic_ok:continue
    all_indices.append(ix)
    need(V*s.diag(*counts)*V.T==Q,'full pattern restriction Gram')
    key=tuple(values)
    if key not in groups:
        C=dict(zip(triples,values[:len(triples)]));U=dict(zip(quads,values[len(triples):]))
        G=s.Matrix(10,10,lambda j,k:U[tuple(sorted(pairs[j]+pairs[k]))]-int(pairs[j][0]==pairs[j][1])*int(pairs[k][0]==pairs[k][1])-sum(C[tuple(sorted(pairs[j]+(i,)))]*C[tuple(sorted(pairs[k]+(i,)))] for i in range(1,5)))
        T=s.Matrix(8,10,lambda k,j:sum(low[pairs[j][0]][u]*low[pairs[j][1]][v]*R[u][v][k] for u,v in itertools.product(range(8),repeat=2))-int(k==0 and pairs[j][0]==pairs[j][1])-sum(C[tuple(sorted(pairs[j]+(i,)))]*low[i][k] for i in range(1,5)))
        B=Qplus*T;Xtypes=V.T*B
        need(Q*B==T,'restriction solvability')
        H=G-T.T*Qplus*T;need(H.rank()==1,'rank-one residual')
        pivot=next(i for i in range(10) if H[i,i]);alpha=H[pivot,pivot];h=H[pivot,:]/alpha
        need(alpha>0 and h[pivot]==1 and H==alpha*h.T*h,'exact residual factorization')
        minima=[];intervals=[]
        for row in Xtypes.tolist():
            q=row[pivot];lower=0;upper=None
            # n=X[row,pivot] is a nonnegative integer. Each of ten entries
            # gives an exact lower/upper bound; enumerate the entire interval.
            for x,hi in zip(row,list(h)):
                off=x-hi*q
                need(hi.q==1 and off.q==1,'integrality congruence')
                if hi>0:lower=max(lower,math.ceil(-off/hi))
                elif hi<0:upper=min(upper,math.floor(-off/hi)) if upper is not None else math.floor(-off/hi)
                else:need(off>=0,'constant coordinate nonnegativity')
            need(upper is not None,'finite complete integer interval')
            feasible=[s.Integer(n)-q for n in range(lower,upper+1) if all((x+(s.Integer(n)-q)*hi).q==1 and x+(s.Integer(n)-q)*hi>=0 for x,hi in zip(row,list(h)))]
            minima.append(min((t*t for t in feasible),default=None));intervals.append([int(lower),int(upper)])
        groups[key]={'alpha':alpha,'h':list(h),'Xtypes':Xtypes,'minima':minima,'intervals':intervals,'indices':[],'excluded':[],'survived':[]}
    g=groups[key];g['indices'].append(ix)
    fail=any(n and v is None for n,v in zip(counts,g['minima']))
    lb=sum(n*v for n,v in zip(counts,g['minima']) if n and v is not None)
    if fail or lb>g['alpha']:excluded.append(ix);g['excluded'].append(ix)
    else:survived.append(ix);g['survived'].append(ix)
need(len(all_indices)==1238 and len(groups)==4,'complete four-group domain')
need(sorted(excluded)==sorted(r['index'] for r in producer['failures']) and survived==producer['survivor_indices'],'independent complete classification agrees')
summary=[]
for g in groups.values():
    pg=next(z for z in producer['groups'] if z['representative']==g['indices'][0])
    need(pg['minimum_norm_rows_by_high_type']==[[str(x) for x in row] for row in g['Xtypes'].tolist()],'independent minimum-norm rows')
    need(pg['coordinate_minimum_squares']==[None if v is None else str(v) for v in g['minima']],'entire-interval enumeration agrees with minimum formula')
    summary.append({'alpha':str(g['alpha']),'h':list(map(int,g['h'])),'patterns':len(g['indices']),'excluded':len(g['excluded']),'survived':len(g['survived']),'coordinate_intervals':g['intervals'],'minimum_squares':[None if v is None else str(v) for v in g['minima']]})
# Independently propagate on separate INDIVIDUAL copies, rather than type counts.
prop=read(HERE/'r1154_quartic_coordinate_propagation.json')
prop_failed=[];prop_survived=[]
for g in groups.values():
    alpha=g['alpha']
    for ix in g['survived']:
        counts=domain['completions'][ix]
        types=[j for j,m in enumerate(counts) for _ in range(m)]
        mm=V[:,types]
        choices=[]
        for j in types:
            q=g['Xtypes'][j,0];lo,hi=g['intervals'][j]
            choices.append([s.Integer(k)-q for k in range(lo,hi+1) if (s.Integer(k)-q)**2<=alpha])
        failed=False
        while True:
            if any(not cs for cs in choices):failed=True;break
            mins=[min(t*t for t in cs) for cs in choices];maxs=[max(t*t for t in cs) for cs in choices]
            lower=sum(mins);upper=sum(maxs)
            if lower>alpha or upper<alpha:failed=True;break
            linear_lo=[sum(mm[k,j]*min(cs) for j,cs in enumerate(choices)) for k in range(8)]
            linear_hi=[sum(mm[k,j]*max(cs) for j,cs in enumerate(choices)) for k in range(8)]
            if any(l>0 or u<0 for l,u in zip(linear_lo,linear_hi)):failed=True;break
            updated=[]
            for j,cs in enumerate(choices):
                updated.append([t for t in cs if lower-mins[j]+t*t<=alpha and all(linear_lo[k]-mm[k,j]*min(cs)+mm[k,j]*t<=0<=linear_hi[k]-mm[k,j]*max(cs)+mm[k,j]*t for k in range(8))])
            if choices==updated:break
            choices=updated
        (prop_failed if failed else prop_survived).append(ix)
need(sorted(prop_failed)==sorted(z['index'] for z in prop['failures']) and sorted(prop_survived)==sorted(prop['survivor_indices']),'independent individual-copy propagation')
height_path=p.parent/'central_integrality/fixed_gram_rotation_1154_h6.json'
height=read(height_path)
need(height['metadata']['tensor_sha256']==record['tensor_sha256'],'prior height-six tensor binding')
for path,key in [(p.parent/'central_integrality/integer_gram_1154.json','gram_domain_sha256'),(p/'central_integral_filters_1154.json','filtered_domain_sha256')]:
    need(hashlib.sha256(json.dumps(read(path),separators=(',',':')).encode()).hexdigest()==height['metadata'][key],'prior exact domain hash')
height_indices=[j for z in height['cases'] for j in z['pattern_indices']]
need(len(height_indices)==len(set(height_indices))==1238 and set(height_indices)==set(all_indices),'prior complete partition')
old_fail={j for z in height['cases'] if z['kind']=='farkas_family' for j in z['pattern_indices']}
need(len(old_fail)==8 and old_fail<=set(excluded),'old eight are in first-stage 892')
reconciliation={'old_height6_exclusions':sorted(old_fail),'norm_exclusions':len(excluded),'additional_propagation_exclusions':len(prop_failed),'union_exclusions':len(set(excluded)|set(prop_failed)|old_fail),'remaining_patterns':len(prop_survived),'new_exclusions_beyond_height6':len(set(excluded)|set(prop_failed))-len(old_fail)}
inputs=[HERE/'r1154_quartic_necessary_filters.py',HERE/'r1154_quartic_necessary_filters.json',p.parent/'central_integrality/integer_gram_1154.json',p/'central_support.py',p/'character_modular.py',p/'rotation_search.py',HERE/'r1154_quartic_coordinate_propagation.py',HERE/'r1154_quartic_coordinate_propagation.json',height_path]
result={'status':'PASS','scope':'946 necessary center patterns excluded; 292 patterns remain unclassified by these bounds. No R1154 exclusion or model.','independent_methods':['direct third/fourth spectral moments','full 14,211-pattern cubic filter','Moore-Penrose Q inverse','complete coordinate integer interval enumeration'],'groups':summary,'excluded_indices':excluded,'stage1_survivor_indices':survived,'propagation_excluded_indices':sorted(prop_failed),'survivor_indices':sorted(prop_survived),'reconciliation':reconciliation,'source_sha256':{('followup/'+str(x.relative_to(HERE)) if x.is_relative_to(HERE) else 'repo/'+str(x.relative_to(root))):sha(x) for x in inputs},'reviewer_sha256':sha(Path(__file__))}
target=HERE/'r1154_quartic_independent_review.json'
if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
else:need(read(target)==result,'saved review mismatch')
print(json.dumps({'status':'PASS','excluded':len(excluded)+len(prop_failed),'survived':len(prop_survived),'receipt':target.name},indent=2))
