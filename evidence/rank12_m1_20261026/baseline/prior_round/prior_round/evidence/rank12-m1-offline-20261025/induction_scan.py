"""Short complete low-I(1) necessary systems, in justified commutative PU scope.

Search limits yield 'no conclusion'; an exclusion requires every column and
every combination to be exhausted. No long frame or modular-data search.
"""
from pathlib import Path
import collections,itertools,json,math,time,signal
import sympy as s
from fp import fp_character,exact,require
from field_checks import pu_gate
from state import current
ROOT=Path(__file__).resolve().parent
sys=None

def columns(ds,beta,K,B,cap=250000):
    n=len(ds);deg=K.mod.degree();bound=[min(int(B[0,i]),math.isqrt(int(B[i,i])))for i in range(1,n)]
    vs=[exact.vector(d,deg)for d in ds[1:]];b=exact.vector(beta-K.one,deg)
    den=int(s.ilcm(*[v.q for z in vs+[b]for v in z]));C=[[int(v*den)for v in z]for z in vs];b=tuple(int(v*den)for v in b)
    order=sorted(range(n-1),key=lambda i:(sum(v!=0 for v in C[i]),sum(abs(v)for v in C[i])),reverse=True)
    C=[C[i]for i in order];bounds=[bound[i]for i in order];tail=n-1
    low=[[0]*deg for _ in range(tail+1)];high=[[0]*deg for _ in range(tail+1)]
    for i in range(tail-1,-1,-1):
        for j in range(deg):low[i][j]=low[i+1][j]+min(0,C[i][j]*bounds[i]);high[i][j]=high[i+1][j]+max(0,C[i][j]*bounds[i])
    out=[];nodes=0;vals=[0]*tail
    def dfs(i,target):
        nonlocal nodes
        nodes+=1
        if nodes>cap:raise TimeoutError('column node budget')
        if any(target[j]<low[i][j]or target[j]>high[i][j]for j in range(deg)):return
        if i==tail:
            v=[0]*tail
            for ix,k in enumerate(order):v[k]=vals[ix]
            out.append((1,)+tuple(v));return
        for x in range(bounds[i]+1):
            vals[i]=x;dfs(i+1,tuple(target[j]-x*C[i][j]for j in range(deg)))
    try:dfs(0,b)
    except TimeoutError:return None,nodes
    return sorted(out),nodes

def low_problem(R,profile):
    f,K,u,d,D,emb=fp_character(R);n=len(R)
    B=sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(n))
    # Direct induction-restriction formula, independent of the Casimir shortcut.
    du=profile['dual'];direct=s.Matrix([[sum(R[a][i][k]*R[k][du[a]][j]for a,k in itertools.product(range(n),repeat=2))for j in range(n)]for i in range(n)])
    require(direct==B,'commutative induction Gram identity')
    roots=[]
    for q,m in B.charpoly(exact.t).as_poly().factor_list()[1]:
        rr=exact.discover_roots(q,K)
        if rr is None:return dict(result='not_split')
        for root in rr:roots += [root]*m
    require(len(roots)==n and D in roots,'all commutative formal codegrees')
    roots.remove(D);sets=[];work=0;seen={}
    for root in roots:
        beta=D/root;key=tuple(exact.ec(beta))
        if key not in seen:seen[key]=columns(d,beta,K,B)
        cs,k=seen[key];work+=k
        if cs is None:return dict(result='column_budget',column_nodes=work)
        if not cs:return dict(result='excluded_empty_column',failed_dimension=exact.ec(beta),column_nodes=work)
        sets.append(cs)
    # Integer first row and residual Gram constraints; identical columns are
    # unordered, reducing work without losing any categorical possibility.
    sets.sort(key=len);A=[[int(B[i,j])-int(i==j==0)for j in range(n)]for i in range(n)]
    nodes=0;previous={};chosen=[];feasible=None
    def dfs(at,Q):
        nonlocal nodes,feasible
        nodes+=1
        if nodes>20000:raise TimeoutError('low combination budget')
        if at==len(sets):
            if any(Q[0]):return False
            LL=[[int(B[i,j])-Q[i][j]for j in range(n)]for i in range(n)]
            for i in range(1,n):
                low=sum((K(LL[i][j])*d[j]for j in range(n)),K.zero)
                gap=K(3)*low-D*d[i]if du[i]!=i else(K(3)*d[i]+K.one)*low-D*d[i]*(d[i]+K.one)
                if emb.sign(gap)>0:return False
            feasible=[list(c)for c in chosen];return True
        tag=id(sets[at]);prev=previous.get(tag)
        for v in sets[at]:
            if prev is not None and v<prev:continue
            T=[[Q[i][j]-v[i]*v[j]for j in range(n)]for i in range(n)]
            if any(x<0 for row in T for x in row):continue
            if any(T[i][i]*T[j][j]<T[i][j]**2 for i in range(n)for j in range(i)):continue
            previous[tag]=v;chosen.append(v)
            if dfs(at+1,T):return True
            chosen.pop()
            if prev is None:previous.pop(tag,None)
            else:previous[tag]=prev
        return False
    try:passed=dfs(0,A)
    except TimeoutError:return dict(result='low_combination_budget',column_counts=list(map(len,sets)),low_nodes=nodes)
    return dict(result='feasible'if passed else'excluded_low_Gram_or_twist_moment',column_counts=list(map(len,sets)),column_nodes=work,low_nodes=nodes,feasible_low_columns=feasible)

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());ex,mo=current();rows=[];cache={}
    path=ROOT/'induction.json'
    if path.exists():rows=json.loads(path.read_text())['records']
    done={r['id']for r in rows}
    def expire(*args):raise TimeoutError('one second short-check budget')
    signal.signal(signal.SIGALRM,expire)
    for p in json.loads((ROOT/'profile.json').read_text())['records']:
        rid=p['id'];gate=pu_gate(data[rid],p)
        if rid in done or rid in ex or rid in mo or not p['commutative']or not gate:continue
        R=data[rid];signal.setitimer(signal.ITIMER_REAL,1.0)
        try:q=low_problem(R,p)
        except TimeoutError:q=dict(result='short_time_budget')
        finally:signal.setitimer(signal.ITIMER_REAL,0)
        c=None
        if q['result'].startswith('excluded'):c=dict(kind='commutative_low_induction',gate=gate,scope='general_complex_fusion_category',**q)
        rows.append(dict(id=rid,tensor_sha256=p['tensor_sha256'],certificate=c,attempt=q))
        print(rid,q['result'],q.get('low_nodes'),flush=True)
        (ROOT/'induction.json').write_text(json.dumps(dict(records=rows,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('DONE',len(rows),'excluded',sum(bool(r['certificate'])for r in rows),'seconds',time.monotonic()-start)
if __name__=='__main__':main()
