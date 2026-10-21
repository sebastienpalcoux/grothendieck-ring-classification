"""Exact necessary Galois signed-permutation test on the 36 frozen pair fibers.
Enumerates arbitrary bijections modulo identical target rows; no involution assumption.
"""
import sys,json,itertools,time,hashlib,collections
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[3];H=ROOT/'evidence/rank8_next_20261021/r1154'
sys.dont_write_bytecode=True;sys.path.insert(0,str(H));import joint_triple_after_a2 as j
K=j.K;D=j.a['D'];need=j.need

def sigma(z):
    co=list(map(F,j.c.ec(z)))
    if len(co)<2:return z
    a,b=co;return -K(a)*K.unit+K(1684*a+b)
def key(z):return tuple(map(str,j.c.ec(z)))
def tuplesum(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-v for v in x)
def cell(yi,yj,li,lj,sgn):
    rr=[sgn*a*b for a in yi for b in yj]
    if li>=0 and lj>=0:rr[5*li+lj]-=sgn
    return tuple(rr)

need(sigma(K.unit)==K(1684)-K.unit,'specified field involution')
results=[];start=time.monotonic()
for ix in (6971,8766,8772):
    pr=next(r for r in j.fibers['results']if r['index']==ix);counts=j.domain['completions'][ix];ns=[1]+counts
    sig=tuple(sum(n*v[1]for n,v in zip(ns,co))//den for co,den in j.moment_coefficients.values());inds,C,aa,hh,mom=j.augmented(sig)
    for z,n in zip(j.values,[1]*5+counts):
        if n:need(sigma(z[1])*z[1]==K.one,'reciprocal A1 eigenvalue')
    for pno,hist in enumerate(pr['pair11_histogram_solutions_by_high_type']):
        labels=[];ys=[];ds=[];ls=[]
        for t in range(5):
            labels.append({'low':t});ys.append(tuple([int(t==1)]+[int(mom[tuple(sorted((1,k,t)))])if t else int(k==1)for k in range(1,5)]));ds.append(j.dims[t]);ls.append(t)
        for typ,his in enumerate(hist):
            for x,n in his:
                if not n:continue
                row,bs,q,vs=j.row_data(pr['group'],typ,x,sig);y=tuple([0]+[int(row[5+j.pairs.index((1,k))])for k in range(1,5)])
                for _ in range(n):labels.append({'type':typ,'pair11':x});ys.append(y);ds.append(j.dims[5+typ]);ls.append(-1)
        dimclasses=collections.defaultdict(list)
        for at,d in enumerate(ds):dimclasses[key(d)].append(at)
        need(sum(d==ds[1]for d in ds)==1,'A1 unique dimension, hence self-dual')
        options=[];class_summary=[];target_keys=[]
        for dk,src in dimclasses.items():
            target=D*sigma(ds[src[0]])/sigma(D);sgn=j.a['embedding'].sign(target);need(sgn in (-1,1),'nonzero dimension transform');target*=K(sgn);dst=dimclasses.get(key(target),[])
            need(len(dst)==len(src),'Galois dimension multiplicity equality');target_keys.append(key(target))
            # A target is distinguished only by its Y row and any low coordinate.
            dtypes=list(collections.Counter((ys[t],ls[t])for t in dst).items());remaining=[n for _,n in dtypes]
            mats=set()
            costs=[[cell(ys[i],yy,ls[i],ll,sgn)for (yy,ll),nn in dtypes]for i in src]
            def rec(pos,acc):
                if pos==len(src):mats.add(acc);return
                for q,num in enumerate(remaining):
                    if not num:continue
                    remaining[q]-=1;rec(pos+1,tuplesum(acc,costs[pos][q]));remaining[q]+=1
            rec(0,(0,)*25)
            options.append(mats);class_summary.append({'source_dimension':list(dk),'target_dimension':list(key(target)),'sign':sgn,'multiplicity':len(src),'distinct_effects':len(mats)})
        need(len(set(target_keys))==len(dimclasses),'disjoint exhaustive target dimension classes')
        # Merge smallest sets first; exact equality of all 25 entries.
        options.sort(key=len);states={(0,)*25};sizes=[]
        for opts in options:
            states={tuplesum(x,y)for x in states for y in opts};sizes.append(len(states))
        passed=(0,)*25 in states
        out={'index':ix,'pair_histogram':pno,'center_rank':len(ds),'compatible_galois_effect':passed,'dimension_classes':class_summary,'dynamic_state_counts':sizes,'final_effect_count':len(states)};results.append(out)
        print(json.dumps({'index':ix,'pair_histogram':pno,'pass':passed,'max_states':max(sizes),'seconds':round(time.monotonic()-start,3)}),file=sys.stderr,flush=True)
need(len(results)==36,'complete inherited pair-fiber domain')
source_paths=[H/'joint_quartic_fibers.py',H/'joint_quartic_fibers.json',H/'joint_triple_after_a2.py',H/'triple_projection.py',H/'a2_action_probe.json',H/'single_induction_trace.json',H/'group1_negative_diagonal.json',j.domainpath,j.quarticpath]
source_bindings={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in source_paths}
print(json.dumps({'complete':True,'source_sha256':source_bindings,'scope':'Necessary normalized modular Galois signed-permutation equation on five known A1 columns; arbitrary dimension-compatible signed permutations, no involution assumption','field_polynomial':[1,-1684,28159],'total_pair_histograms':len(results),'surviving_pair_histograms':sum(r['compatible_galois_effect']for r in results),'surviving_patterns':sorted(set(r['index']for r in results if r['compatible_galois_effect'])),'results':results,'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
