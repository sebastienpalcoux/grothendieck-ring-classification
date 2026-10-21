"""Exact two-dimensional residual lattice test for all R1154 triple words.

Twenty triple products have residual rank two after projection on words of
length <=2.  Each simple-coordinate residual lies in an explicit rational
ellipse, on the lattice requiring every triple coefficient to be an integer.
The sum of residual Mahalanobis squared norms equals two.  Exhaustive local
integer enumeration therefore gives a necessary lower bound.
"""
import sys,json,math,time,hashlib
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
UPSTREAM=Path(__file__).resolve().with_name('triple_projection.py')
exec(compile(UPSTREAM.read_text().split('failures=[];')[0],str(UPSTREAM),'exec'))
@lru_cache(None)
def coupled(signature):
    inds,C,beta,moments=projection(signature)
    T=triples; V=s.Matrix(len(inds),20,lambda i,j:moments[tuple(sorted(words[inds[i]]+T[j]))])
    H=s.Matrix(20,20,lambda i,j:moments[tuple(sorted(T[i]+T[j]))])-V.T*s.Matrix(C)
    need(H.rank()==2,'rank two triple residual')
    piv=[T.index((1,3,3)),T.index((3,3,4))]; Hb=H.extract(piv,piv); Hi=Hb.inv()
    Q=Hi*H.extract(piv,list(range(20)))
    need(H==Q.T*Hb*Q,'complete residual parametrization')
    return inds,C,beta,moments,piv,[[F(v)for v in rr]for rr in Hi.tolist()],[[F(v)for v in rr]for rr in Q.tolist()]
@lru_cache(None)
def local_options(zs,piv,beta,Hi,Q):
    # Loose square-root bounds are outward rounded using integer arithmetic.
    ranges=[]
    for i in piv:
        B=math.isqrt(beta[i].numerator//beta[i].denominator)+2
        lo=max(0,zs[i].numerator//zs[i].denominator-B);hi=zs[i].numerator//zs[i].denominator+B+1
        ranges.append(range(lo,hi+1))
    options=[]
    for x in ranges[0]:
        dx=F(x)-zs[piv[0]]
        if dx*dx>beta[piv[0]]:continue
        for y in ranges[1]:
            dy=F(y)-zs[piv[1]]
            if dy*dy>beta[piv[1]]:continue
            cost=Hi[0][0]*dx*dx+2*Hi[0][1]*dx*dy+Hi[1][1]*dy*dy
            if cost>2:continue
            vv=tuple(z+dx*Q[0][j]+dy*Q[1][j]for j,z in enumerate(zs))
            if all(v.denominator==1 and v>=0 for v in vv):options.append((x,y,cost))
    return tuple(options)
failures=[];survivors=[];start=time.monotonic();localstats={}
for row in fibers['results']:
    if row['status']!='exact_joint_fiber_witness':continue
    ix=row['index'];ns=[1]+domain['completions'][ix];signature=[]
    for word,(co,den)in moment_coefficients.items():
        irr=sum(n*v[0]for n,v in zip(ns,co));rat=sum(n*v[1]for n,v in zip(ns,co))
        need(irr==0 and rat%den==0 and rat>=0,'integer nonnegative scalar moments')
        signature.append(rat//den)
    inds,C,beta,moments,piv,Hi,Q=coupled(tuple(signature));Hi=tuple(map(tuple,Hi));Q=tuple(map(tuple,Q));piv=tuple(piv);beta=tuple(beta)
    g=groups[row['group']];h=list(map(F,quartic['h']));X0=[[F(x)for x in rr]for rr in g['minimum_norm_rows_by_high_type']]
    for number,histograms in enumerate(row['pair11_histogram_solutions_by_high_type']):
        minimum=F(0);why=None;counts=[]
        for typ,hist in enumerate(histograms):
            for x,n in hist:
                if not n:continue
                xs=[v+(F(x)-X0[typ][0])*hh for v,hh in zip(X0[typ],h)];v=[0]*5+xs;vb=[v[i]for i in inds]
                zs=tuple(sum(x*C[k][j]for k,x in enumerate(vb))for j in range(20))
                opts=local_options(zs,piv,beta,Hi,Q);counts.append(len(opts))
                if not opts:why={'empty_type':typ,'pair11':x};break
                minimum+=n*min(v[2]for v in opts)
            if why:break
        if not why and minimum>2:why={'minimum_total_mahalanobis_norm':str(minimum),'required_total':2}
        out={'index':ix,'histogram_solution':number}
        if why:failures.append(dict(out,**why))
        else:survivors.append(out)
        for n in counts:localstats[n]=localstats.get(n,0)+1
    print(json.dumps({'pattern':ix,'failures':len(failures),'survivors':len(survivors),'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
print(json.dumps({'schema':'r1154-triple-coupled-lattice/v1','id':r['id'],'tensor_sha256':r['tensor_sha256'],'scope':'Necessary coupled triple-product integer residual lattice bound; no categorification assertion',
 'incoming_patterns':224,'incoming_pair_completions':2904,'excluded_pair_completions':len(failures),'surviving_pair_completions':len(survivors),'remaining_patterns':len(set(x['index']for x in survivors)),
 'surviving_pattern_indices':sorted(set(x['index']for x in survivors)),'failures':failures,'survivors':survivors,'local_option_count_histogram':localstats,
 'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [domainpath,fiberpath,quarticpath,UPSTREAM]},'verifier_sha256':digest(Path(__file__))},indent=2))
