from cls_soft import *
BASE=HERE.parents[1]/'rank12-m1-offline-20261025';sys.path.insert(0,str(BASE/'sources/work/rank11'));import common
DATA=json.loads((BASE/'tensors.json').read_text());rows=[]
for parity in [0,1]:
 labels=[(a,e)for a in range(6)for e in [1,-1]];R=[[[0]*12 for _ in range(12)]for _ in range(12)]
 for p,(a,sa)in enumerate(labels):
  for q,(b,sb)in enumerate(labels):
   for r,(c,sc)in enumerate(labels):
    n=N[a][b][c]
    if not n:continue
    # eta_a=(-1)^(parity*degree_a); chosen equivariance square roots r_a=i^(parity*degree_a).
    phase=(-1)**(parity*int(a==5 and b==5))
    tr=phase*sa*sb*sc*s.trace(J(a,b,c));v=s.simplify((n+tr)/2)
    if not(v.is_Integer and v>=0):raise ValueError(v)
    R[p][q][r]=int(v)
 common.validate(R);hits=[]
 for rid,R0 in DATA.items():
  if common.coarse(R0)!=common.coarse(R):continue
  p=common.based_iso(R0,R)
  if p is not None:
   common.require(all(R0[a][b][c]==R[p[a]][p[b]][p[c]]for a,b,c in itertools.product(range(12),repeat=3)),'full tensor matching');hits.append(rid)
   rows.append(dict(id=rid,parity=parity,model_tensor=R,labels=labels,basis_map_source_to_model=p,source='Choi-Lu-Sun 2310.19867v2 Tables3/4',constructor='soft_C2_equivariantization'))
 print('PARITY',parity,'MATCH',hits,flush=True)
(HERE/'soft_models.json').write_text(json.dumps(rows,indent=2)+'\n')
