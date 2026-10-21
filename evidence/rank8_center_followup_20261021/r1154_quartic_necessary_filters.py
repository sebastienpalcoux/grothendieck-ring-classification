"""Exact, bounded, read-only R1154 fourth-Verlinde necessary filters.

No repository writes, no solver, and no coupled integer enumeration. The domain
is exactly the 1,238 cubic survivors in the accepted 14,211 integral Gram file.
This is exploratory evidence, not a ring exclusion or categorification.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
sys.dont_write_bytecode = True
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]/'grothendieck-ring-classification')
args=ap.parse_args()
ROOT=args.root.resolve()
P=ROOT/'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0,str(P))
import central_support as c
import character_modular as md
import rotation_search as base
import central_integral_filters as cf
s=c.s

def need(condition,message):
    if not condition:raise RuntimeError(message)

def read(p):return json.loads(p.read_text())
def jsrat(x):return str(x)
def matrix_json(X):return [[str(v) for v in row] for row in X.tolist()]

base.install()
census_path=c.OLD.parent/'pipeline/census_m3.json'
census={r['id']:r for r in read(census_path)}
domain_path=P.parent/'central_integrality/integer_gram_1154.json'
filters_path=P/'central_integral_filters_1154.json'
domain=read(domain_path);filters=read(filters_path)
row=census['R8_3_1154'];R=row['tensor'];a=c.w.data(R);K=a['K'];cols=a['lows'][31]
need(domain['tensor_sha256']==row['tensor_sha256']==filters['tensor_sha256'],'tensor binding')
need([list(v) for v in cols]==domain['low_columns'],'low domain')
chars=md.characters(R,a)
need(all(ch[i]==ch[a['du'][i]] for ch in chars for i in range(8)),'selfdual low character rows')
need(md.assignments(a,chars,cols)==[(0,1,2,3,4)],'unique low assignment')
high=md.full.base.grams.high_columns(a,s.Matrix.hstack(*map(s.Matrix,cols)))[1]
need([list(v) for v,z in high]==domain['high_columns'],'high column ordering')
need(cf.cubic_rows(R,a,cols,(0,1,2,3,4))==filters['cubic_rows'],'cubic coefficient replay')
indices=[i for i,counts in enumerate(domain['completions']) if cf.cubic_values(filters['cubic_rows'],counts) is not None]
need(indices==filters['cubic_survivor_indices'],'complete cubic survivor domain')
need(len(domain['completions'])==14211 and len(indices)==1238,'domain cardinalities')
pairs=list(itertools.combinations_with_replacement(range(1,5),2))
quads=list(itertools.combinations_with_replacement(range(1,5),4))
allcols=[tuple(v) for v in cols]+[(0,)+tuple(v) for v,z in high]
values=[[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*md.value(ch,v,K) for E,ch in enumerate(chars)] for v in allcols]
dims=[sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero) for v in allcols]
quartics=[]
for quad in quads:
    i,j,k,l=quad
    vs=[sv[i]*sv[j]*sv[k]*sv[l]/(d*d*a['D']**2) for sv,d in zip(values,dims)]
    vs=[sum(vs[:5],K.zero)]+vs[5:]
    cs=[]
    for v in vs:
        z=list(map(F,c.ec(v)));need(len(z)<=2,'quadratic field');cs.append([F(0)]*(2-len(z))+z)
    den=math.lcm(*(x.denominator for z in cs for x in z))
    quartics.append(([[int(x*den) for x in z] for z in cs],den))
V=s.Matrix.hstack(*(s.Matrix((0,)+tuple(v)) for v,z in high))
vs=V.tolist()
def high_gram(counts):
    return tuple(tuple(sum(n*vs[i][k]*vs[j][k] for k,n in enumerate(counts)) for j in range(8)) for i in range(8))
Qtuple=high_gram(domain['completions'][indices[0]]);Q=s.Matrix(Qtuple)
ind=list(Q.rref()[1]);need(Q.rank()==3,'restriction rank')
Qb=Q.extract(ind,ind);Qinv=Qb.inv();h=s.Matrix([[1,0,1,-1,0,0,0,1,-1,1]])
groups={};failures=[];survivors=[]
for ix in indices:
    counts=domain['completions'][ix];need(len(counts)==16 and all(type(n) is int and n>=0 for n in counts),'integral multiplicities')
    need(high_gram(counts)==Qtuple,'every pattern has same exact restriction Gram')
    cubic=cf.cubic_values(filters['cubic_rows'],counts);need(cubic is not None,'cubic survivor')
    moments=[]
    for co,den in quartics:
        irr=sum(n*z[0] for n,z in zip([1]+counts,co));num=sum(n*z[1] for n,z in zip([1]+counts,co))
        need(irr==0 and num>=0 and num%den==0,'scalar fourth moment')
        moments.append(num//den)
    key=(tuple(cubic),tuple(moments))
    if key not in groups:
        low={tuple(r['triple']):v for r,v in zip(filters['cubic_rows'],cubic)};four=dict(zip(quads,moments))
        G=s.Matrix(10,10,lambda p,q:four[tuple(sorted(pairs[p]+pairs[q]))]-int(pairs[p][0]==pairs[p][1])*int(pairs[q][0]==pairs[q][1])-sum(low[tuple(sorted(pairs[p]+(e,)))]*low[tuple(sorted(pairs[q]+(e,)))] for e in range(1,5)))
        T=s.Matrix(8,10,lambda k,p:sum(cols[pairs[p][0]][u]*cols[pairs[p][1]][v]*R[u][v][k] for u in range(8) for v in range(8))-int(pairs[p][0]==pairs[p][1] and k==0)-sum(low[tuple(sorted(pairs[p]+(e,)))]*cols[e][k] for e in range(1,5)))
        C=Qinv*T[ind,:]
        # Individual high rows repeat according to counts. Their minimum-norm
        # solution rows are V[ind,:]^T C; use MM^T=Q to avoid expansion.
        Xtypes=V[ind,:].T*C
        need(Q[:,ind]*C==T,'minimum-norm solution consistency')
        H=G-C.T*Qb*C;alpha=H[0,0]
        need(alpha>0 and H==alpha*h.T*h,'exact positive rank-one residual Gram')
        need(G.rank()==3,'pair Gram rank')
        minima=[];corrections=[];ranges=[]
        for xs in Xtypes.tolist():
            q=xs[0]
            need(all((xs[j]-h[j]*q).q==1 for j in range(10)),'row integrality congruence')
            need(all(xs[j]>=0 for j in range(10) if h[j]==0),'fixed row nonnegativity')
            L=max(int(s.ceiling(q-xs[j])) for j in range(10) if h[j]==1)
            U=min(int(s.floor(q+xs[j])) for j in range(10) if h[j]==-1)
            ranges.append([L,U])
            if L>U:minima.append(None);corrections.append([]);continue
            candidates={min(U,max(L,int(s.floor(q)))),min(U,max(L,int(s.ceiling(q))))}
            minimum=min((s.Integer(n)-q)**2 for n in candidates)
            minima.append(minimum);corrections.append(sorted(s.Integer(n)-q for n in candidates if (s.Integer(n)-q)**2==minimum))
        groups[key]={'index':len(groups),'representative':ix,'indices':[],'alpha':alpha,'Xtypes':Xtypes,'minimum_squares':minima,'minimizers':corrections,'integer_pair11_ranges':ranges,'failure_indices':[],'survivor_indices':[]}
    g=groups[key];g['indices'].append(ix)
    need(sum(counts)-3>=1,'residual rank versus kernel dimension')
    if any(n and v is None for n,v in zip(counts,g['minimum_squares'])):
        failures.append({'index':ix,'group':g['index'],'reason':'empty_coordinate_domain'});g['failure_indices'].append(ix)
    else:
        lb=sum(n*v for n,v in zip(counts,g['minimum_squares']) if n)
        if lb>g['alpha']:
            failures.append({'index':ix,'group':g['index'],'reason':'sum_coordinate_minimum_squares_exceeds_residual_norm','lower_bound':str(lb),'residual_norm':str(g['alpha'])});g['failure_indices'].append(ix)
        else:
            survivors.append(ix);g['survivor_indices'].append(ix)
need(sorted([r['index'] for r in failures]+survivors)==indices,'disjoint exhaustive outcome partition')
sources=[domain_path,filters_path,census_path]
# Bind every imported Python dependency from the frozen repository.
for module in tuple(sys.modules.values()):
    name=getattr(module,'__file__',None)
    if name:
        path=Path(name).resolve()
        # The running verifier is separately bound below, whether inside or outside ROOT.
        if path.is_relative_to(ROOT) and path.suffix=='.py' and path!=Path(__file__).resolve():sources.append(path)
sources=sorted(set(sources))
result={
 'scope':'exploratory exact necessary pattern filters; no ring exclusion, no category or complete central fusion construction',
 'id':row['id'],'tensor_sha256':row['tensor_sha256'],'low_index':31,
 'domain':{'all_integral_gram_patterns':14211,'cubic_surviving_patterns':len(indices),'high_column_types':16,'high_simple_count_range':[min(sum(domain['completions'][i]) for i in indices),max(sum(domain['completions'][i]) for i in indices)]},
 'method':{'equations':['M X=T','X^T X=G','X has nonnegative integer entries'],'minimum_norm_solution':'X0=M^T Q^+ T, Q=M M^T; implemented through independent rows','residual_form':'G-X0^T X0=alpha h^T h','necessary_correction':'X=X0+t h, M t=0, sum(t_i^2)=alpha','coordinate_bound':'For q=X0[i,0], t_i=n-q. Integrality and nonnegativity give integer interval L<=n<=U. The squared distance from q to its nearest integer in that interval is a coordinate lower bound. Sum over all repeated rows cannot exceed alpha.','not_checked':'Remaining coupled M t=0 and exact norm/integer feasibility for surviving patterns'},
 'pair_order':pairs,'h':list(map(int,h)),'restriction_gram_rank':3,'pair_gram_rank':3,'residual_gram_rank':1,
 'scalar_quartic_psd_and_rank_passes':len(indices),'coordinate_exclusions':len(failures),'remaining_patterns':len(survivors),
 'groups':[{'group':g['index'],'representative':g['representative'],'patterns':len(g['indices']),'alpha':str(g['alpha']),'minimum_norm_rows_by_high_type':matrix_json(g['Xtypes']),'coordinate_minimum_squares':[None if x is None else str(x) for x in g['minimum_squares']],'coordinate_minimizers':[[str(x) for x in xs] for xs in g['minimizers']],'integer_pair11_ranges':g['integer_pair11_ranges'],'excluded':len(g['failure_indices']),'surviving':len(g['survivor_indices']),'indices':g['indices']} for g in groups.values()],
 'failures':failures,'survivor_indices':survivors,
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
print(json.dumps(result,indent=2))
