"""Exact fifth/sixth moment integer projection of all R1154 pair completions."""
import sys,json,itertools,math,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
P=ROOT/'evidence/rank8_frontier_20261021/noncommutative';sys.path.insert(0,str(P))
import central_support as c,character_modular as md,rotation_search as base
base.install();s=c.s
def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=next(x for x in json.load(open(c.OLD.parent/'pipeline/census_m3.json'))if x['id']=='R8_3_1154')
R=r['tensor'];a=c.w.data(R);K=a['K'];cols=a['lows'][31];chars=md.characters(R,a)
high=md.full.base.grams.high_columns(a,s.Matrix.hstack(*map(s.Matrix,cols)))[1]
allcols=list(cols)+[(0,)+tuple(v) for v,z in high]
dims=[sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero)for v in allcols]
values=[[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*md.value(ch,v,K)/d for E,ch in enumerate(chars)]for v,d in zip(allcols,dims)]
weights=[d*d/a['D']**2 for d in dims]
domainpath=P.parent/'central_integrality/integer_gram_1154.json';domain=json.load(open(domainpath))
fiberpath=HERE/'joint_quartic_fibers.json';fibers=json.load(open(fiberpath))
need(fibers['verifier_sha256']==digest(HERE/'joint_quartic_fibers.py'),'fiber verifier binding')
need(fibers['all_histogram_solutions_enumerated']and fibers['complete'],'complete joint pair domain')
quarticpath=ROOT/'evidence/rank8_center_followup_20261021/r1154_quartic_necessary_filters.json'
quartic=json.load(open(quarticpath));groups={g['group']:g for g in quartic['groups']}
pairs=list(itertools.combinations_with_replacement(range(1,5),2));triples=list(itertools.combinations_with_replacement(range(1,5),3))
words=[()]+[(i,)for i in range(1,5)]+pairs
moment_coefficients={}
for deg in range(7):
    for word in itertools.combinations_with_replacement(range(1,5),deg):
        co=[]
        for vs,wt in zip(values,weights):
            value=wt
            for i in word:value*=vs[i]
            raw=list(map(F,c.ec(value)));co.append([F(0)]*(2-len(raw))+raw)
        co=[[sum(v[j]for v in co[:5])for j in range(2)]]+co[5:]
        den=math.lcm(*(z.denominator for rr in co for z in rr))
        moment_coefficients[word]=([[int(z*den)for z in rr]for rr in co],den)

@lru_cache(None)
def projection(signature):
    moments=dict(zip(moment_coefficients,signature))
    moment=lambda word:moments[tuple(sorted(word))]
    G=s.Matrix(15,15,lambda i,j:moment(words[i]+words[j]))
    inds=list(G.rref()[1]);Gb=G.extract(inds,inds);Gi=Gb.inv()
    V=s.Matrix(len(inds),20,lambda i,j:moment(words[inds[i]]+triples[j]))
    C=Gi*V
    beta=[moment(t+t)-(V[:,j].T*C[:,j])[0]for j,t in enumerate(triples)]
    need(all(b>=0 for b in beta),'positive residual triple norms')
    return inds,[[F(x)for x in row]for row in C.tolist()],[F(x)for x in beta],moments

failures=[];survivors=[];statistics={};start=time.monotonic()
for row in fibers['results']:
    if row['status']!='exact_joint_fiber_witness':continue
    ix=row['index'];ns=[1]+domain['completions'][ix];signature=[]
    for word,(co,den)in moment_coefficients.items():
        irr=sum(n*v[0]for n,v in zip(ns,co));rat=sum(n*v[1]for n,v in zip(ns,co))
        need(irr==0 and rat%den==0 and rat>=0,'integer nonnegative scalar moments')
        signature.append(rat//den)
    inds,C,beta,moments=projection(tuple(signature));g=groups[row['group']]
    h=list(map(F,quartic['h']));X0=[[F(x)for x in rr]for rr in g['minimum_norm_rows_by_high_type']]
    lowrows=[]
    for j in range(5):
        lowrows.append([int(j==k)for k in range(5)]+[moments[tuple(sorted(pair+(j,)))]if j else int(pair[0]==pair[1])for pair in pairs])
    for number,histograms in enumerate(row['pair11_histogram_solutions_by_high_type']):
        vectors=[(1,v)for v in lowrows]
        for typ,hist in enumerate(histograms):
            for x,n in hist:
                if n:
                    xs=[v+(F(x)-X0[typ][0])*hh for v,hh in zip(X0[typ],h)]
                    need(all(z.denominator==1 and z>=0 for z in xs),'integer nonnegative pair coefficients')
                    vectors.append((n,[0]*5+xs))
        bounds=[F(0)]*20;why=None
        for n,v in vectors:
            vb=[v[i]for i in inds]
            zs=[sum(x*C[k][j]for k,x in enumerate(vb))for j in range(20)]
            for j,z in enumerate(zs):
                # Every actual triple-product coefficient is nonnegative integer.
                m=max(0,z.numerator//z.denominator)
                dist=min((F(m)-z)**2,(F(m+1)-z)**2)
                bounds[j]+=n*dist
        for j,(lb,b)in enumerate(zip(bounds,beta)):
            if lb>b:
                why={'triple':triples[j],'minimum_square_sum':str(lb),'residual_norm':str(b)};break
        out={'index':ix,'histogram_solution':number}
        if why:failures.append(dict(out,**why))
        else:survivors.append(out)
    print(json.dumps({'pattern':ix,'pair_completions':len(row['pair11_histogram_solutions_by_high_type']),'failures':len(failures),'survivors':len(survivors),'moment_groups':projection.cache_info().currsize,'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
surviving_patterns=sorted(set(x['index']for x in survivors))
print(json.dumps({'schema':'r1154-triple-projection/v1','id':r['id'],'tensor_sha256':r['tensor_sha256'],
 'scope':'Necessary integer triple-product projections from exact fifth and sixth moments; no categorification assertion',
 'incoming_patterns':224,'incoming_pair_completions':2904,'excluded_pair_completions':len(failures),'surviving_pair_completions':len(survivors),'remaining_patterns':len(surviving_patterns),'surviving_pattern_indices':surviving_patterns,
 'moment_groups':projection.cache_info().currsize,'failures':failures,'survivors':survivors,
 'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [domainpath,fiberpath,quarticpath]},'verifier_sha256':digest(Path(__file__))},indent=2))
