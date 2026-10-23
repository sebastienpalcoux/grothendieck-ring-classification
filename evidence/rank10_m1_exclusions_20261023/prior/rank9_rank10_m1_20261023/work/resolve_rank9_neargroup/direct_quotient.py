"""Census-independent integer quotient completion for the D48 source rings.

Only the four SOURCE tensors and their verified dimension vectors enter the
enumeration.  R117 is consulted only AFTER enumeration, for an isomorphism.
The positive linear constraints force all tensor coefficients to be binary;
this is checked before any binary enumeration begins.
"""
from pathlib import Path
from itertools import product, permutations
from collections import Counter
from functools import lru_cache
import hashlib, json, math, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = json.loads((ROOT / 'work/input_audit/tensors.json').read_text())
AUDIT = json.loads((ROOT / 'work/input_audit/audit.json').read_text())
RECS = {r['id']: r for r in AUDIT['9']['rings']}
N = 9
DIMS = (1, 1, 1, 1, 2, 2, 2, 2, 2)
ALPHA = (0, 1, 3, 2, 4, 6, 5, 8, 7)
TRIPLES = list(product(range(N), repeat=3))

def require(c, msg):
    if not c: raise ValueError(msg)

def star(T):
    return tuple(next(j for j in range(N) if T[i][j][0]) for i in range(N))

def dimensions(rid):
    sq = RECS[rid]['squared_fp_dimensions_exact']
    d = [math.isqrt(x) for x in sq]
    T = DATA[rid]
    require(all(a*a == b for a,b in zip(d,sq)), 'nonintegral dimension')
    require(all(sum(T[i][j][k]*d[k] for k in range(N)) == d[i]*d[j]
                for i,j in product(range(N), repeat=2)), 'wrong dimension')
    return d

def orbits(p):
    seen=set(); out=[]
    for i in range(N):
        if i not in seen:
            o=sorted({i,p[i]}); seen.update(o); out.append(o)
    return out

def canonical_restriction(rid):
    C = DATA[rid]; d = dimensions(rid)
    valid=[]
    for g in range(1,N):
        if d[g] != 1: continue
        p=tuple(C[g][i].index(1) for i in range(N))
        require(all(p[p[i]] == i for i in range(N)), 'sign not involutive')
        oo=orbits(p)
        profile=sorted(x for o in oo for x in ([d[o[0]]] if len(o)==2 else [d[o[0]]//2]*2))
        if profile != list(DIMS): continue
        F=[[0]*N for _ in range(N)]
        slots={(1,2): iter([(0,),(1,)]), (2,1):iter([(2,3)]),
               (2,2):iter([(4,)]), (4,1):iter([(5,6),(7,8)])}
        for o in oo:
            dest=next(slots[d[o[0]],len(o)])
            for i in o:
                for k in dest: F[i][k]=1
        require(F[0][0]==1 and sum(F[0])==1, 'unit restriction')
        require(all(sum(F[i][k]*DIMS[k] for k in range(N))==d[i] for i in range(N)), 'F dimensions')
        require(all(F[i][k]==F[i][ALPHA[k]] for i,k in product(range(N),repeat=2)), 'F alpha')
        valid.append((g,F))
    require(len(valid)==1, 'expected one sign of this profile')
    return valid[0]

def possible_stars(C,F):
    cs=star(C)
    options=[[b for b in range(N) if DIMS[a]==DIMS[b] and
              all(F[i][a]==F[cs[i]][b] for i in range(N))] for a in range(N)]
    out=[]
    for s in product(*options):
        if s[0]!=0 or len(set(s))!=N: continue
        if any(s[s[i]]!=i or s[ALPHA[i]]!=ALPHA[s[i]] for i in range(N)):continue
        out.append(s)
    return out

class DSU:
    def __init__(self): self.p=list(range(N**3))
    def find(self,x):
        while x!=self.p[x]: self.p[x]=self.p[self.p[x]];x=self.p[x]
        return x
    def join(self,a,b): self.p[self.find(a)]=self.find(b)

def ti(i,j,k): return (i*N+j)*N+k

def linear_problem(C,F,s):
    uf=DSU()
    for i,j,k in TRIPLES:
        v=ti(i,j,k)
        uf.join(v,ti(s[i],k,j))
        uf.join(v,ti(k,s[j],i))
        uf.join(v,ti(ALPHA[i],ALPHA[j],ALPHA[k]))
    reps=sorted({uf.find(x) for x in range(N**3)})
    var={r:i for i,r in enumerate(reps)}
    V=[var[uf.find(x)] for x in range(N**3)]
    equations=set()
    def equation(terms,rhs):
        c=Counter()
        for v,w in terms:c[V[v]]+=w
        equations.add((tuple(sorted(c.items())),rhs))
    for i,j in product(range(N),repeat=2):
        equation([(ti(0,i,j),1)],int(i==j))
        equation([(ti(i,0,j),1)],int(i==j))
        equation([(ti(i,j,0),1)],int(s[i]==j))
        equation([(ti(i,j,k),DIMS[k]) for k in range(N)],DIMS[i]*DIMS[j])
        for k in range(N):
            equation([(ti(a,b,k),1) for a in range(N) if F[i][a]
                      for b in range(N) if F[j][b]],
                     sum(C[i][j][h]*F[h][k] for h in range(N)))
    return V,sorted(equations),len(reps)

@lru_cache(None)
def sums(weights):
    mask=1
    for w in weights: mask |= mask<<w
    return mask

def solve(V,equations,nvars):
    stats={'nodes':0,'linear_completions':0,'associative_completions':0}
    answers=[]
    def recurse(a):
        stats['nodes']+=1
        while True:
            changed=False; unresolved=[]
            for terms,rhs in equations:
                rest=[];r=rhs
                for v,w in terms:
                    if a[v]<0:rest.append((v,w))
                    else:r-=a[v]*w
                weights=tuple(w for v,w in rest)
                if r<0 or not ((sums(weights)>>r)&1):return
                if not rest:continue
                unresolved.append(rest)
                for q,(v,w) in enumerate(rest):
                    others=weights[:q]+weights[q+1:];mask=sums(others)
                    ok0=bool((mask>>r)&1)
                    ok1=r>=w and bool((mask>>(r-w))&1)
                    if ok0 and ok1:continue
                    value=int(ok1)
                    if a[v]<0:a[v]=value;changed=True
                    elif a[v]!=value:return
            if not changed:break
        if unresolved:
            smallest=min(unresolved,key=len)
            degrees=Counter(v for rest in unresolved for v,w in rest)
            v=max((v for v,w in smallest),key=degrees.get)
            for value in (0,1):
                b=a.copy();b[v]=value;recurse(b)
            return
        require(all(x>=0 for x in a),'unconstrained variable')
        stats['linear_completions']+=1
        T=[[[a[V[ti(i,j,k)]] for k in range(N)] for j in range(N)] for i in range(N)]
        if not all(sum(T[i][j][p]*T[p][k][l] for p in range(N))==
                   sum(T[j][k][p]*T[i][p][l] for p in range(N))
                   for i,j,k,l in product(range(N),repeat=4)):return
        stats['associative_completions']+=1;answers.append(T)
    recurse([-1]*nvars)
    return stats,answers

def binary_bounds(equations,nvars):
    """Every nonnegative integer solution satisfies these one-row bounds."""
    bounds=[10**9]*nvars; witnesses=[None]*nvars
    for q,(terms,rhs) in enumerate(equations):
        require(rhs>=0 and all(w>0 for v,w in terms),'nonpositive bound row')
        for v,w in terms:
            b=rhs//w
            if b<bounds[v]:bounds[v]=b;witnesses[v]=q
    require(max(bounds)<=1,'binary enumeration would miss integer solutions')
    require(all(q is not None for q in witnesses),'unbounded coefficient')
    return bounds,witnesses

def isomorphism(A,B):
    bd=dimensions('R9_1_117')
    iv=[i for i in range(1,N) if bd[i]==1];nn=[i for i in range(N) if bd[i]==2]
    for a in permutations(iv):
        for b in permutations(nn):
            p=(0,)+a+b
            if all(A[i][j][k]==B[p[i]][p[j]][p[k]] for i,j,k in TRIPLES):return p
    return None

def main():
    receipt={'method':'Complete nonnegative integer tensor enumeration from source restriction identities, dimensions, unit, duality, Frobenius reciprocity and alpha. Positive linear equations force every variable to 0 or 1 before enumeration; full associativity then checked. No quotient census filter.', 'quotient_basis':['1','a','b','c','m','x','xprime','y','yprime'],'quotient_dimensions':DIMS,'involution':ALPHA,'sources':[]}
    for rid in ('R9_1_12','R9_1_62','R9_1_87','R9_1_108'):
        t=time.monotonic();C=DATA[rid];g,F=canonical_restriction(rid);st=possible_stars(C,F)
        rec={'source':rid,'source_tensor_sha256':hashlib.sha256(json.dumps(C,separators=(',',':')).encode()).hexdigest(),'sign':g,'restriction':F,'dual_branches':[]}
        print(rid,'dual branches',len(st),flush=True)
        for s in st:
            V,eqs,nv=linear_problem(C,F,s)
            bounds,witnesses=binary_bounds(eqs,nv)
            stats,ans=solve(V,eqs,nv)
            row={'dual':s,'variables':nv,'equations':len(eqs),'coefficient_upper_bounds':bounds,'upper_bound_equation_indices':witnesses,**stats,'solutions':[]}
            for T in ans:
                p=isomorphism(T,DATA['R9_1_117'])
                require(p is not None,'new quotient not R117')
                row['solutions'].append({'tensor':T,'quotient_to_R117':p})
            rec['dual_branches'].append(row)
            print(' ',s,nv,stats,flush=True)
        require(sum(b['associative_completions'] for b in rec['dual_branches'])>0,'no quotient')
        print(' done',round(time.monotonic()-t,3),'s',flush=True);receipt['sources'].append(rec)
    (HERE/'direct_quotient.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: every directly completed quotient is R9_1_117; no census completeness premise.')

if __name__=='__main__':main()
