"""Extra associative C2 zesting with arbitrary neutral central currents.

Categorical lifts are justified by the braided input, a displayed factor,
or the established central lifts of the pseudo-PSU(2)6 and TY categories.
No existence inference is made from centrality of a ring element alone.
"""
from pathlib import Path
import collections,itertools,json,sys,time

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE))
import models as base_models
import additional_models as extra_models
from state import current
from zest_models import gradings
import common

def inverts(R):
    du=common.dual(R)
    return [a for a in range(len(R))if sum(R[a][du[a]])==1]

def zest(R,g,h):
    n=len(R)
    common.require(g[h]==0 and all(R[h][a]==R[a][h]and sum(R[h][a])==1 for a in range(n)),'neutral central ring current')
    act=[R[h][a].index(1)for a in range(n)]
    T=[[[0]*n for _ in range(n)]for _ in range(n)]
    for i,j,k in itertools.product(range(n),repeat=3):
        T[i][j][act[k]if g[i]*g[j]else k]=R[i][j][k]
    return T

def candidates():
    for name,R,kind,par,braided in base_models.direct():
        currents={0:'unit'}
        if braided is True:
            currents.update({h:'canonical lift from a specified braided realization'for h in inverts(R)})
        elif isinstance(braided,list):
            currents.update({h:'specified central lift from the left factor'for h in braided})
        if kind=='ty_cyclic_equivariant':
            currents.update({h:'GNN Proposition4.1 TY central invertible over a fixed group element, orthogonal-action equivariantization'for h in inverts(R)})
        if kind=='deligne_product':
            left=par['left_tensor'];right=par['right_tensor'];rn=par['right_name'];r=len(right)
            if rn in ['pseudo-PSU(2)_6','TY(C3)','Tambara--Yamagami category for $C_5$']:
                for a,b in itertools.product(inverts(left),inverts(right)):
                    currents[a*r+b]='Deligne product of a braided left current with the explicit '+rn+' central lift'
        yield name,R,kind,par,currents
    for name,R,kind,par,h in extra_models.candidates():
        yield name,R,kind,par,{0:'unit',h:'specified inherited Ising fermion or preserved equivariantization boson'}

def main():
    start=time.monotonic();data=json.loads((BASE/'tensors.json').read_text());ex,mo=current()
    unresolved={rid:R for rid,R in data.items()if rid not in ex and rid not in mo}
    buckets=collections.defaultdict(list)
    for rid,R in unresolved.items():buckets[common.coarse(R)].append((rid,R))
    hits=collections.defaultdict(list);attempts=[];seen=set()
    for name,R,kind,par,currents in candidates():
        if len(R)!=12 or max(v for A in R for row in A for v in row)>1:continue
        for g in gradings(R):
            for h,premise in currents.items():
                if not h or g[h]:continue
                T=zest(R,g,h);key=common.sha(T)
                if key in seen:continue
                seen.add(key);common.validate(T);targets=[]
                for rid,S in buckets[common.coarse(T)]:
                    p=common.based_iso(S,T)
                    if p is None:continue
                    common.require(all(S[i][j][k]==T[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 coefficients')
                    rec=dict(name='General central C2 zest of '+name,constructor='general_central_C2_zest',parameters=dict(base_constructor=kind,base_parameters=par,base_name=name,base_tensor=R,grading=g,central_invertible=h,central_lift_premise=premise,existence='DGP Definition3.2/Proposition3.4; ENO extension obstruction H4(C2,U1)=0; unitary scalar correction'),model_tensor=T,basis_map_source_to_model=p)
                    hits[rid].append(rec);targets.append(rid)
                    print('HIT',rid,name,'h',h,'grading',g,flush=True)
                attempts.append(dict(base_name=name,h=h,grading=g,lift=premise,tensor_sha256=key,matches=targets))
    rows=[dict(id=rid,tensor_sha256=common.sha(data[rid]),models=ms)for rid,ms in hits.items()]
    (HERE/'extended_zest_models.json').write_text(json.dumps(rows,indent=2)+'\n')
    (HERE/'extended_zest_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print(json.dumps(dict(unique_models=len(hits),identifications=sum(map(len,hits.values())),candidates=len(attempts),seconds=time.monotonic()-start)),flush=True)
if __name__=='__main__':main()
