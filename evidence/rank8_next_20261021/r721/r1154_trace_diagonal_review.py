"""Independent singleton-induction and pattern3994 negative-diagonal review.

Recomputes moments directly from characters and exhaustively enumerates the
small triple fiber by Cartesian integer multisets, without discovery solvers.
"""
from pathlib import Path
import sys,json,itertools,hashlib,math
from functools import lru_cache
from fractions import Fraction as F
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'evidence/rank8_next_20261021/r1154'
up=P/'triple_projection.py';env={'__file__':str(up)}
exec(compile(up.read_text().split('moment_coefficients={}')[0],str(up),'exec'),env)
s=env['s'];c=env['c'];a=env['a'];K=env['K'];R=env['R'];cols=env['cols'];domain=env['domain'];fibers=env['fibers'];quartic=env['quartic'];groups=env['groups'];values=env['values'];weights=env['weights'];words=env['words'];pairs=env['pairs'];triples=env['triples'];need=env['need']
acts=json.loads((P/'a2_action_probe.json').read_text());trace=json.loads((P/'single_induction_trace.json').read_text())
trace_results=[]
for ix in acts['surviving_pattern_indices']:
    objects=list(domain['low_columns'])+[(0,)+tuple(v)for n,v in zip(domain['completions'][ix],domain['high_columns'])for _ in range(n)]
    kills=[]
    for x in range(1,8):
        support=[(i,v[x])for i,v in enumerate(objects)if v[x]]
        if len(support)==1:kills.append((x,support[0][1]))
    expected=next(r for r in trace['results']if r['index']==ix)
    need(bool(kills)==(expected['status']=='excluded_single_induction_support'),'independent singleton-support result')
    trace_results.append({'index':ix,'singleton_source_multiplicities':kills})
need([r['index']for r in trace_results if not r['singleton_source_multiplicities']]==[3994,6971,8766,8772],'four surviving trace patterns')
ix=3994;counts=domain['completions'][ix];multip=[1]*5+counts
@lru_cache(None)
def moment(word):
    result=K.zero
    for n,vs,weight in zip(multip,values,weights):
        value=K(n)*weight
        for i in word:value*=vs[i]
        result+=value
    raw=result.to_list();need(len(raw)<=1 and(not raw or raw[0].denominator==1),'exact integer moment')
    return int(raw[0])if raw else 0
m=lambda word:moment(tuple(sorted(word)))
@lru_cache(None)
def restriction(word):
    row=[1]+[0]*7
    for label in word:row=[sum(row[i]*cols[label][j]*R[i][j][k]for i in range(8)for j in range(8))for k in range(8)]
    return row
fw=s.Matrix([restriction(w)for w in words]);G=s.Matrix(15,15,lambda i,j:m(words[i]+words[j]));G=G.row_join(fw).col_join(fw.T.row_join(a['Gram']));piv=list(G.rref()[1]);need(len(piv)==9,'augmented rank9')
Gi=G.extract(piv,piv).inv();TG=s.Matrix(23,20,lambda i,j:m(words[i]+triples[j])if i<15 else restriction(triples[j])[i-15]);C=Gi*TG[piv,:]
H=s.Matrix(20,20,lambda i,j:m(triples[i]+triples[j]))-TG[piv,:].T*C
alpha=H[7,7];hh=H[7,:]/alpha;need(H==alpha*hh.T*hh,'one-dimensional triple residual')
row=next(r for r in fibers['results']if r['index']==3994)
need(len(row['pair11_histogram_solutions_by_high_type'])==1,'unique incoming pairhistogram')
rows=[];meta=[]
for j in range(5):
    raw=[int(j==k)for k in range(5)]+[m(p+(j,))if j else int(p[0]==p[1])for p in pairs]+list(cols[j])
    rows.append(raw);meta.append(('low',j,1))
X0=[[s.Rational(x)for x in rr]for rr in groups[1]['minimum_norm_rows_by_high_type']];h=list(map(s.Rational,quartic['h']))
for typ,hist in enumerate(row['pair11_histogram_solutions_by_high_type'][0]):
    for x,n in hist:
        if n:
            pp=[v+(x-X0[typ][0])*hv for v,hv in zip(X0[typ],h)]
            rows.append([0]*5+pp+[0]+list(domain['high_columns'][typ]));meta.append((typ,x,n))
V=s.Matrix(rows);need(V.T*s.diag(*(x[2]for x in meta))*V==G,'actual pairhistogramGram')
projection=V[:,piv]*C
# Residuals on all five low coordinates vanish since e_low lies in W.
need(all(projection[j,k]==m(triples[k]+((j,)if j else()))for j in range(5)for k in range(20)),'exactlowtriplecoefficients')
options=[];domain_sizes=[]
for i,(typ,pair11,n)in enumerate(meta[5:],5):
    q=projection[i,7];bound=math.isqrt(int(alpha))+2;values_i=[]
    for x in range(max(0,int(s.floor(q))-bound),int(s.floor(q))+bound+2):
        t=x-q
        if t*t>alpha:continue
        actual=projection[i,:]+t*hh
        if all(v.q==1 and v>=0 for v in actual):values_i.append(x)
    tuples=[(x,)*n for x in values_i]if typ==10 else itertools.combinations_with_replacement(values_i,n)
    group_options=[]
    for xs in tuples:
        ts=[x-q for x in xs];cost=sum(t*t for t in ts)
        if cost<=alpha:group_options.append((xs,sum(ts),cost))
    options.append(group_options);domain_sizes.append(len(group_options))
# Exhaust all compressed multisets; the small product here is finite and explicit.
solutions=[];cartesian_count=0
for choice in itertools.product(*options):
    cartesian_count+=1
    if sum(r[2]for r in choice)!=alpha:continue
    residual=s.zeros(1,23)
    for i,opt in enumerate(choice,5):residual+=opt[1]*V[i,:]
    if residual!=s.zeros(1,23):continue
    solutions.append(choice)
need(len(solutions)==1,'independentexhaustiveunique triplefiber')
basewords=[(),(1,),(2,),(3,),(4,),(1,1),(1,2),(2,2),(1,1,1),(1,1,2)]
wordrows=[];labels=[]
for j in range(5):
    wordrows.append([int(j==k)for k in range(5)]+[m(w+((j,)if j else()))for w in basewords[5:]])
    labels.append({'low':j})
for i,choice in enumerate(solutions[0],5):
    typ,pair11,n=meta[i];q=projection[i,7]
    for copy,val in enumerate(choice[0]):
        actual=projection[i,:]+(val-q)*hh;lookup=dict(zip(words,list(V[i,:15])));lookup.update(dict(zip(triples,list(actual))))
        wordrows.append([lookup[w]for w in basewords]);labels.append({'type':typ,'pair11':pair11,'triple133':val,'copy':copy})
W=s.Matrix(wordrows);Gw=s.Matrix(10,10,lambda i,j:m(basewords[i]+basewords[j]));need(W.T*W==Gw and Gw.det()!=0,'complete rank10wordGram');inverse=Gw.inv()
fixed=[]
for obj in range(1,5):
    B=s.Matrix(10,10,lambda i,j:m(basewords[i]+(obj,)+basewords[j]));B2=s.Matrix(10,10,lambda i,j:m(basewords[i]+(obj,obj)+basewords[j]))
    need(B*inverse*B==B2,'fullwordspaninvariance');fixed.append(W*inverse*B*inverse*W.T)
# Independently tally everyjointtuple and inspect remaining A4 eigenvalues.
spectral={}
for n,v in zip(multip,values):
    if not n:continue
    key=tuple(tuple(c.ec(x))for x in v);spectral.setdefault(key,[v,0])[1]+=n
need(len(spectral)==10,'onecycliccopyofeveryjointtuple')
hidden=[(v[4],n-1)for v,n in spectral.values()if n>1]
need(sum(n for v,n in hidden)==W.rows-10 and all(a['embedding'].sign(v)<=0 for v,n in hidden),'completehiddenA4spectrum nonpositive')
bad=[(labels[i],str(fixed[3][i,i]))for i in range(W.rows)if fixed[3][i,i]<0]
need(len(bad)==1 and bad[0][1]=='-2','unique strictnegativefixeddiagonal')
print(json.dumps(dict(review='independent_R1154_trace_and_pattern3994',status='PASS',singleton_trace_results=trace_results,
      group3994=dict(compressed_triple_domain_sizes=domain_sizes,cartesian_multisets_examined=cartesian_count,
      complete_triple_solutions=len(solutions),cyclic_rank=10,center_rank=W.rows,hidden_A4_spectrum=[(c.ec(v),n)for v,n in hidden],
      negative_diagonal=bad,conclusion='Every actual A4 diagonal at this coordinate is <= -2, impossible for a fusion matrix.'),
      source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[P/'single_induction_trace.py',P/'group1_negative_diagonal.py',P/'group1_all_triples.json']}),indent=2,default=int))
