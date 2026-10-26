"""Small exact checks supporting the theoretical D24 pointed-extension proof."""
from itertools import product,combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def need(v,msg):
    if not v:raise ValueError(msg)

def main():
    V=list(product(range(2),repeat=3))
    basis=[lambda v:v[0],lambda v:v[1],lambda v:v[2],lambda v:v[0]*v[1],lambda v:v[0]*v[2],lambda v:v[1]*v[2],lambda v:v[0]*v[1]*v[2]]
    functions=[];kernel=[];full_kernel=[]
    for coeff in product(range(2),repeat=7):
        q={v:sum(c*f(v) for c,f in zip(coeff,basis))%2 for v in V};functions.append(tuple(q[v] for v in V))
        if all(q[v]==0 for v in V if v[0]==0 or v[1]==0):kernel.append(coeff)
        if all(q[g]==q[h] for g,h in product(V,repeat=2) if g[0]==h[1]):full_kernel.append(coeff)
    need(len(set(functions))==128,'faithful seven cyclic restrictions')
    need(len(kernel)==4 and all(all(c==0 for i,c in enumerate(v) if i not in [3,6]) for v in kernel),'two-plane restriction kernel')
    need(full_kernel==[(0,)*7],'full bimodule stabilizer kills all associator classes')
    # Integer H4 restrictions for C4 times C2: r*x²+s*xy+t*y².
    cyclic_pair=[];mixed_pair=[]
    for r,s,t in product(range(4),range(2),range(2)):
        if r==0 and (r+2*s)%4==0:cyclic_pair.append([r,s,t])
        if r==0 and r%2==s==t==0:mixed_pair.append([r,s,t])
    need(cyclic_pair==[[0,0,0],[0,0,1]] and mixed_pair==[[0,0,0]],'C4 times C2 associator restrictions')
    # Enumerate all elementary order8 subgroups of B[2]=F2^4.
    def span(vs):
        out={0}
        for v in vs:out|={x^v for x in list(out)}
        return frozenset(out)
    planes={span(vs) for vs in combinations(range(1,16),3)}
    planes={P for P in planes if len(P)==8}
    counts={}
    for kind in ['hyperbolic_C2','double_semion_C2']:
        def q(v):
            u=(v>>2)&1;w=(v>>3)&1
            return (2*u*w if kind=='hyperbolic_C2' else u+2*u*w)%4
        lag=[P for P in planes if all(q(v)==0 for v in P)]
        need(all({0,1,2,3}<=P for P in lag),'all elementary Lagrangians contain characteristic2B')
        counts[kind]=len(lag)
    need(counts=={'hyperbolic_C2':2,'double_semion_C2':1},'odd-action fixed-Lagrangian sets')
    result=dict(status='PASS',V8_cyclic_restriction_classes=len(functions),V8_two_plane_kernel=kernel,V8_full_stabilizer_kernel=full_kernel,C4C2_two_cyclic_kernel=cyclic_pair,C4C2_mixed_kernel=mixed_pair,elementary_Lagrangian_counts=counts,scope='Small arithmetic support; categorical proof is d24_c3_pointed_extension_lemma.md')
    (HERE/'quotient_metric_lemmas.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
