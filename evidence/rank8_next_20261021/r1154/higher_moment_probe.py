"""Read-only higher mixed vacuum fusion-moment necessary screening."""
import sys,json,itertools,math,time
from pathlib import Path
from fractions import Fraction as F
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0,str(P))
import central_support as c,character_modular as md,rotation_search as base
base.install();s=c.s
r=next(x for x in json.load(open(c.OLD.parent/'pipeline/census_m3.json'))if x['id']=='R8_3_1154')
R=r['tensor'];a=c.w.data(R);K=a['K'];cols=a['lows'][31];chars=md.characters(R,a)
high=md.full.base.grams.high_columns(a,s.Matrix.hstack(*map(s.Matrix,cols)))[1]
allcols=list(cols)+[(0,)+tuple(v) for v,z in high]
dims=[sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero)for v in allcols]
values=[[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*md.value(ch,v,K)/d for E,ch in enumerate(chars)]for v,d in zip(allcols,dims)]
weights=[d*d/a['D']**2 for d in dims]
domain=json.load(open(P.parent/'central_integrality/integer_gram_1154.json'))
old=json.load(open(Path(__file__).with_name('joint_quartic_fibers.json')))
remaining=[x['index']for x in old['results']if x['status']=='exact_joint_fiber_witness'];failures=[]
start=time.monotonic()
for deg in range(5,13):
    terms=[]
    for word in itertools.combinations_with_replacement(range(1,5),deg):
        cs=[]
        for vs,wt in zip(values,weights):
            value=wt
            for i in word:value*=vs[i]
            cs.append(value)
        cs=[sum(cs[:5],K.zero)]+cs[5:]
        co=[]
        for v in cs:
            raw=list(map(F,c.ec(v)));co.append([F(0)]*(2-len(raw))+raw)
        den=math.lcm(*(z.denominator for rr in co for z in rr))
        terms.append((word,[[int(z*den)for z in rr]for rr in co],den))
    survivors=[]
    for ix in remaining:
        ns=[1]+domain['completions'][ix];bad=None
        for word,co,den in terms:
            b=sum(n*v[0]for n,v in zip(ns,co));q=sum(n*v[1]for n,v in zip(ns,co))
            if b or q<0 or q%den:
                bad={'index':ix,'degree':deg,'word':word,'value_coefficients':[str(F(b,den)),str(F(q,den))]};break
        if bad:failures.append(bad)
        else:survivors.append(ix)
    remaining=survivors
    print(json.dumps({'degree':deg,'words':len(terms),'remaining':len(remaining),'failures':len(failures),'seconds':time.monotonic()-start}),file=sys.stderr,flush=True)
    if not remaining:break
print(json.dumps({'id':r['id'],'scope':'necessary scalar mixed fusion moments','failures':failures,'remaining':remaining},indent=2))
