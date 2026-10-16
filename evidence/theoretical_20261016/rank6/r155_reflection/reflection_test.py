"""Experimental exact necessary braid spectral reflection filter; not a category witness."""
from functools import lru_cache

MOD=144

def star_data(exponents,counts):
    # The identity-product tuple is (D^-1,B,A). Hurwitz permutations preserve
    # conjugacy-class feasibility, so its three spectral legs may be reordered.
    rows=[[(e if j<2 else -e,m) for e,m in zip(es,ms) if m] for j,(es,ms) in enumerate(zip(exponents,counts))]
    n=sum(counts[0]); alpha=[n]; q=[-sum(row[0][0] for row in rows)%MOD]; edges=[]
    for row in rows:
        # Eigenvalues can be reordered; put biggest multiplicities first.
        row.sort(key=lambda x:(-x[1],x[0]))
    q=[-sum(row[0][0] for row in rows)%MOD]
    for row in rows:
        left=n; prev=0
        for j in range(len(row)-1):
            left-=row[j][1]; v=len(alpha); alpha.append(left)
            q.append((row[j][0]-row[j+1][0])%MOD);edges.append((prev,v));prev=v
    return alpha,q,edges

@lru_cache(None)
def reflection_test(exponents,counts):
    alpha,q,edges=star_data(exponents,counts)
    if sum(a*x for a,x in zip(alpha,q))%MOD!=0:raise ValueError('Reflection determinant congruence')
    adjacency=[[] for _ in alpha]
    for u,v in edges:adjacency[u].append(v);adjacency[v].append(u)
    trace=[]
    while True:
        support=[i for i,a in enumerate(alpha) if a]
        if not support:return False,tuple(trace),"zero"
        if sum(alpha)==1:return q[support[0]]==0,tuple(trace),"simple"
        seen={support[0]}; stack=list(seen)
        while stack:
            for v in adjacency[stack.pop()]:
                if alpha[v] and v not in seen:seen.add(v);stack.append(v)
        if len(seen)!=len(support):return False,tuple(trace),"disconnected"
        pairs=[2*a-sum(alpha[u] for u in adjacency[v]) for v,a in enumerate(alpha)]
        positive=[v for v,p in enumerate(pairs) if p>0]
        if not positive:return True,tuple(trace),"fundamental"
        # All positive vertices are constraints; a zero parameter kills immediately.
        zero=next((v for v in positive if q[v]==0),None)
        if zero is not None:return False,tuple(trace),"zero-parameter-positive-pair"
        v=max(positive,key=lambda x:pairs[x]); old=q[v]
        trace.append((tuple(alpha),tuple(q),v))
        alpha[v]-=pairs[v]
        if alpha[v]<0:return False,tuple(trace),"negative"
        q[v]=-old%MOD
        for u in adjacency[v]:q[u]=(q[u]+old)%MOD
        if sum(a*x for a,x in zip(alpha,q))%MOD!=0:raise ValueError('Reflection determinant congruence')

if __name__=='__main__':
    import json
    from pathlib import Path
    data=json.loads(Path(__file__).with_name('braid_results_20261016.json').read_text())
    tally={}; failed=[]
    for key,v in data['results'].items():
        if v['verdict']!='PASS_NECESSARY':continue
        ex=tuple(tuple(e for e,m in row) for row in v['spectra_mod144'])
        for part in v['witness']:
            ok,tr,reason=reflection_test(ex,tuple(tuple(row) for row in part))
            tally[(ok,reason)]=tally.get((ok,reason),0)+1
            if not ok:failed.append((key,sum(part[0]),reason))
    print(tally);print('failed',failed)
