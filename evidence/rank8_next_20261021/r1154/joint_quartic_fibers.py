"""Complete exact joint restriction/norm fibers for the 292 R1154 patterns.

The finite domains are consequences of the already verified fourth-moment
rank-one Gram identity. Interchangeable copies of a restriction-column type
are represented by histograms, without discarding any labelled solution.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def need(ok,message):
    if not ok: raise ValueError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load_inputs(root):
    base=root/'evidence/rank8_center_followup_20261021'
    paths=[base/'r1154_quartic_necessary_filters.json',base/'r1154_quartic_coordinate_propagation.json',
           root/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json']
    a,b,d=[json.loads(p.read_text()) for p in paths]
    need(a['tensor_sha256']==b['tensor_sha256']==d['tensor_sha256'],'tensor identity')
    need(len(b['survivor_indices'])==292,'exact incoming domain')
    need(digest(paths[0])==b['base_receipt_sha256'],'preceding receipt binding')
    for name,value in a['source_sha256'].items():need(digest(root/name)==value,'immutable source '+name)
    return a,b,d,{p.relative_to(root).as_posix():digest(p) for p in paths}

def histogram_options(n,values,costs,budget):
    """All histograms on this type whose nonnegative excess cost fits budget."""
    out=[]
    def visit(k,left,sy,cost,hs):
        if k==len(values)-1:
            total=cost+left*costs[k]
            if total<=budget:out.append((sy+left*values[k],total,tuple(hs+[left])))
            return
        cap=left if not costs[k] else min(left,(budget-cost)//costs[k])
        for m in range(cap+1):visit(k+1,left-m,sy+m*values[k],cost+m*costs[k],hs+[m])
    visit(0,n,0,0,[])
    return out

def solve(counts,cols,group,all_solutions=False):
    alpha=F(group['alpha']);qs=[F(row[0]) for row in group['minimum_norm_rows_by_high_type']]
    den=math.lcm(*(q.denominator for q in qs),alpha.denominator)
    need(den==205,'expected common denominator')
    target_norm=alpha*den*den;need(target_norm.denominator==1,'integer scaled norm')
    target_norm=int(target_norm)
    domains=[];bases=[];minimum=0
    for n,q,(lo,hi) in zip(counts,qs,group['integer_pair11_ranges']):
        values=[x for x in range(lo,hi+1) if (F(x)-q)**2<=alpha] if n else []
        if n and not values:return None,{'reason':'empty_initial_domain','nodes':0}
        domains.append(values)
        z=[int(den*(F(x)-q)) for x in values]
        v=min(z,key=lambda x:x*x) if n else 0
        bases.append(v);minimum+=n*v*v
    if minimum>target_norm:return None,{'reason':'minimum_norm','nodes':0}
    need((target_norm-minimum)%den==0,'excess norm integrality')
    budget=(target_norm-minimum)//den
    # Columns span rank three. Coordinates 0,2,5 are independent; final
    # reconstruction below checks all seven restriction coordinates directly.
    rows=(0,2,5)
    rawtarget=[-sum(n*col[j]*v for n,col,v in zip(counts,cols,bases)) for j in rows]
    if any(x%den for x in rawtarget):return None,{'reason':'linear_congruence','nodes':0}
    target=tuple(x//den for x in rawtarget)
    types=[]
    for i,n in enumerate(counts):
        if not n:continue
        zs=[int(den*(F(x)-qs[i])) for x in domains[i]]
        vals=[(z-bases[i])//den for z in zs]
        costs=[(z*z-bases[i]*bases[i])//den for z in zs]
        need(all(c>=0 for c in costs),'nonnegative excess costs')
        os=histogram_options(n,vals,costs,budget)
        # For existence it is enough to retain one histogram for each identical
        # sum and norm contribution; all omitted histograms give the same state.
        dedup={}
        for sy,cost,hist in os:dedup.setdefault((sy,cost),(sy,cost,hist))
        if not all_solutions:os=list(dedup.values())
        types.append((i,tuple(cols[i][j] for j in rows),os))
    # Fail-fast order, keeping rare independent coordinates first.
    types.sort(key=lambda z:(z[1][1]==0,len(z[2]),-max(z[1])))
    N=len(types);lows=[[0]*4 for _ in range(N+1)];highs=[[0]*4 for _ in range(N+1)]
    for k in range(N-1,-1,-1):
        i,col,os=types[k]
        for j in range(4):
            vals=[cost if j==3 else sy*col[j] for sy,cost,hist in os]
            lows[k][j]=lows[k+1][j]+min(vals)
            highs[k][j]=highs[k+1][j]+max(vals)
    nodes=0
    @lru_cache(None)
    def search(k,t0,t1,t2,cost):
        nonlocal nodes
        nodes+=1;state=(t0,t1,t2,cost)
        if any(not lows[k][j]<=state[j]<=highs[k][j] for j in range(4)):return ()
        if k==N:return ((),) if state==(0,0,0,0) else ()
        i,col,os=types[k]
        answers=[]
        for sy,dc,hist in os:
            if dc>cost:continue
            tails=search(k+1,t0-sy*col[0],t1-sy*col[1],t2-sy*col[2],cost-dc)
            for tail in tails:
                answers.append((hist,)+tail)
                if not all_solutions:return tuple(answers)
        return tuple(answers)
    found=search(0,*target,budget)
    statistics={'nodes':nodes,'budget':budget,'type_options':{str(i):len(os)for i,c,os in types},
                'cache_hits':search.cache_info().hits}
    if not found:return None,dict(statistics,reason='complete_joint_fiber_empty')
    solutions=[]
    for answer in found:
        histograms=[[]for i in counts]
        for (i,col,os),hist in zip(types,answer):histograms[i]=list(zip(domains[i],hist))
        linear=[F(0)]*7;norm=F(0)
        for n,col,q,hist in zip(counts,cols,qs,histograms):
            need(sum(m for x,m in hist)==n,'histogram multiplicity')
            for x,m in hist:
                t=F(x)-q
                norm+=m*t*t
                for j in range(7):linear[j]+=m*col[j]*t
        need(all(x==0 for x in linear) and norm==alpha,'direct full witness verification')
        solutions.append(histograms)
    statistics['histogram_solutions']=len(solutions)
    return solutions,dict(statistics,reason='exact_joint_fiber_witness')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--limit',type=int)
    ap.add_argument('--all-solutions',action='store_true')
    args=ap.parse_args();root=args.root.resolve()
    a,b,d,sources=load_inputs(root)
    byindex={i:g for g in a['groups']for i in g['indices']}
    indices=b['survivor_indices'][:args.limit]if args.limit else b['survivor_indices']
    out=[];start=time.monotonic()
    for ix in indices:
        wit,stats=solve(d['completions'][ix],d['high_columns'],byindex[ix],args.all_solutions)
        row={'index':ix,'group':byindex[ix]['group'],'status':stats.pop('reason'),'statistics':stats}
        if wit is not None:row['pair11_histogram_solutions_by_high_type']=wit
        out.append(row)
        print(json.dumps({'done':len(out),'index':ix,'status':row['status'],'nodes':stats['nodes'],'seconds':round(time.monotonic()-start,3)}),file=sys.stderr,flush=True)
    result={'schema':'r1154-joint-quartic-fibers/v1','id':a['id'],'tensor_sha256':a['tensor_sha256'],
            'scope':'Exact necessary pair-product Gram completion only; no complete fusion ring or category is asserted',
            'incoming_patterns':len(b['survivor_indices']),'processed_patterns':len(out),'complete':indices==b['survivor_indices'],
            'all_histogram_solutions_enumerated':args.all_solutions,
            'counts':dict(Counter(row['status']for row in out)), 'results':out,
            'source_sha256':sources,'verifier_sha256':digest(Path(__file__))}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
