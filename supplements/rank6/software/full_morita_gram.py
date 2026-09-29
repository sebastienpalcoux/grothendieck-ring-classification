"""Full Morita-action Gram obstruction for a forced split involution algebra.

Uses integer fusion/module tensors and exact exhaustive bounded columns.
Floating-point optimization only proposes exact Farkas certificates.
No pivotal, spherical, braided or positivity-of-categorical-dimension hypothesis.
"""
import itertools, math, json, time
from collections import Counter
import sympy as s
from exact import require
from involution_module import invs
from module_dual_gram import anti_representations, module_matrices
from higher_traces import farkas, check_farkas


def full_gram(M):
    r=M[0].rows
    return s.Matrix(r*r,r*r,lambda p,q:sum(m[q//r,p//r]*m[q%r,p%r] for m in M))


def first_columns(M,g):
    r=M[0].rows;done=set();cols=[]
    for a in range(r):
        if a in done:continue
        b=next(b for b in range(r) if M[g][a,b])
        require(sum(M[g][a,j] for j in range(r))==1 and M[g][b,a]==1,'g not involution on module')
        v=[0]*r;v[a]=1
        if a==b:cols += [tuple(v),tuple(v)]
        else:v[b]=1;cols += [tuple(v)]
        done.update((a,b))
    return cols


def image_candidates(G,V,col,row,node_limit=2000000):
    r=len(col);nn=r*r;inds=list(range(0,nn,r))+list(range(1,r));vals=list(col)+list(row[1:])
    try:sol,pars=V.extract(inds,range(V.cols)).gauss_jordan_solve(s.Matrix(vals))
    except ValueError:return []
    ans=V*sol;v=ans.subs({p:0 for p in pars});W=ans.jacobian(pars)
    if W.cols:
        piv=list(W.T.rref()[1]);H=W*W.extract(piv,range(W.cols)).inv();b=v-H*v.extract(piv,[0])
        bounds=[math.isqrt(int(G[i,i])) for i in piv]
        if math.prod(t+1 for t in bounds)>node_limit:raise TimeoutError('full Morita candidate box exceeds exact enumeration budget')
        den=math.lcm(*(int(x.q) for x in list(H)+list(b)))
        hs=[[int(H[i,j]*den) for j in range(H.cols)] for i in range(nn)];bs=[int(x*den) for x in b]
        out=[];diag=[int(G[i,i]) for i in range(nn)];gg=[list(map(int,row)) for row in G.tolist()]
        for z in itertools.product(*(range(t+1) for t in bounds)):
            nums=[bs[i]+sum(h*zz for h,zz in zip(hs[i],z)) for i in range(nn)]
            if any(t<0 or t%den for t in nums):continue
            x=tuple(t//den for t in nums)
            if any(t*t>diag[i] for i,t in enumerate(x)):continue
            if any(x[i]*x[j]>gg[i][j] for i in range(nn) for j in range(i,nn)):continue
            out.append(x)
        return out
    x=list(v)
    if all(z.is_Integer and z>=0 for z in x) and all(x[i]*x[j]<=G[i,j] for i in range(nn) for j in range(i,nn)):
        return [tuple(map(int,x))]
    return []


def system(R,g,fixed,T,node_limit=2000000):
    labels,M=module_matrices(R,g,fixed,T);r=len(labels);G=full_gram(M)
    require(G==G.T,'full Morita Gram not symmetric')
    cols=first_columns(M,g);counts=Counter(cols);unique=sorted(counts);rank=G.rank()
    if rank>len(cols):return None,{'reason':'rank','gram_rank':rank,'dual_rank':len(cols)}
    V=s.Matrix.hstack(*G.columnspace());allcs=[];classes=[]
    ident=tuple(int(i==j) for i in range(r) for j in range(r))
    for t,c in enumerate(unique):
        cs=set()
        for row in unique:cs.update(image_candidates(G,V,c,row,node_limit))
        # Every right action commutes with every left action.
        for x in sorted(cs):
            B=s.Matrix(r,r,x)
            if all(B*m==m*B for m in M):allcs.append(x);classes.append(t)
    u=tuple(int(i==0) for i in range(r));counts[u]-=1
    require(counts[u]>=0,'missing dual unit')
    nn=r*r;ij=list(itertools.combinations_with_replacement(range(nn),2))
    A=[[x[i]*x[j] for x in allcs] for i,j in ij]
    A += [[int(c==t) for c in classes] for t in range(len(unique))]
    b=[int(G[i,j])-ident[i]*ident[j] for i,j in ij]+[counts[c] for c in unique]
    # Zero rows are kept: a nonzero RHS gives a transparent exact contradiction.
    meta={'gram_rank':rank,'dual_rank':len(cols),'rows':len(b),'columns':len(allcs),
          'column_types':[list(c) for c in unique],'candidate_counts':[classes.count(t) for t in range(len(unique))]}
    return (A,b),meta


def certificate(R,node_limit=2000000,report=None):
    n=len(R)
    if not all(R[i][j]==R[j][i] for i in range(n) for j in range(n)):return None
    for g in invs(R):
        info=anti_representations(R,g)
        if info is None:continue
        fixed,seed,nodes,reps=info;branches=[]
        for ti,T in enumerate(reps):
            ab,meta=system(R,g,fixed,T,node_limit)
            if report is not None:report.append({'g':g,'branch':ti,**meta})
            if ab is None:branches.append({'T':[list(x) for x in T],**meta});continue
            A,b=ab
            if len(A[0]):y=farkas(A,b)
            elif any(b):
                y=[0]*len(b);j=next(j for j,z in enumerate(b) if z);y[j]=-1 if b[j]>0 else 1
            else:y=None
            if y is None:
                if report is not None:report[-1]['outcome']='no_exact_obstruction'
                break
            check_farkas(A,b,y);branches.append({'T':[list(x) for x in T],'meta':meta,'y':y})
            if report is not None:report[-1]['outcome']='exact_obstruction'
        if len(branches)==len(reps):return {'kind':'full_morita_gram','involution':g,'fixed':fixed,'generators':list(seed),'generator_tuples':nodes,'branches':branches}
    return None


def verify(R,c):
    require(c['kind']=='full_morita_gram' and c['involution'] in invs(R),'invalid full Morita input')
    info=anti_representations(R,c['involution']);require(info is not None,'ineligible module size')
    fixed,seed,nodes,reps=info
    require(c['fixed']==fixed and c['generators']==list(seed) and c['generator_tuples']==nodes,'wrong exhaustive module domain')
    require([b['T'] for b in c['branches']]==[[list(x) for x in T] for T in reps],'missing module action branches')
    for T,b in zip(reps,c['branches']):
        ab,meta=system(R,c['involution'],fixed,T)
        if ab is None:require(all(b.get(k)==v for k,v in meta.items()),'wrong rank obstruction')
        else:require(b['meta']==meta,'wrong full Gram system');check_farkas(*ab,b['y'])
    return True

if __name__=='__main__':
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1]
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scan',action='store_true');p.add_argument('--id');p.add_argument('--output',type=Path);a=p.parse_args()
    census={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};ledger=json.load(open(ROOT/'data/decisions.json'))
    chosen=[r for r in ledger if r['existence']['general']=='unknown' and (not a.id or r['id']==a.id)]
    result=[]
    for row in chosen:
        start=time.monotonic();diag=[]
        try:
            c=certificate(census[row['id']]['N'],report=diag)
            if c:verify(census[row['id']]['N'],c)
            record={'id':row['id'],'multiplicity':row['m'],'outcome':'excluded' if c else 'no_exact_obstruction','certificate':c,'diagnostics':diag}
        except (TimeoutError,ValueError) as e:record={'id':row['id'],'multiplicity':row['m'],'outcome':'incomplete','error':str(e),'diagnostics':diag}
        record['seconds']=time.monotonic()-start;result.append(record)
        if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:record[k] for k in ('id','outcome','seconds')}),flush=True)
