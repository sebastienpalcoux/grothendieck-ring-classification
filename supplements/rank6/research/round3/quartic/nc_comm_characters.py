"""Correctly normalized original formal codegrees for commutative signed sectors."""
from nc_comm_enum import *
from rings import dual,Characters
from oriented_extension import linear_data
from proofs import norm_failure,field_failure,signed_adjoint_parity
from exact import pc,ec
from collections import Counter

def check(R,rid):
 start=time.monotonic();p,source,groups=make_problem(R);out=Path(__file__).parent;meta=json.load(open(out/(rid+'_comm.json')));require(meta['complete'],'enumeration incomplete');vals=sorted(tuple(map(int,line.split())) for line in open(out/(rid+'_comm_values.txt')));require(len(vals)==meta['solutions']==len(set(vals)),'wrong complete count');n=len(R);du=dual(R)
 signs=[(1,)+tail for tail in itertools.product((-1,1),repeat=n-1) if all(((1,)+tail)[i]==((1,)+tail)[du[i]] for i in range(n))];factors=[tuple(e[a]*e[b]*e[c] for orb in p['active'] for a,b,c in [orb[0]]) for e in signs];orbits={};allvalues=set(vals)
 for v in vals:
  orb={tuple(x*y for x,y in zip(v,f)) for f in factors};require(orb<=allvalues,'gauge orbit not complete');orbits.setdefault(min(orb),set()).add(v)
 pp,co,q,fe,original_cf=linear_data(R);print(rid,'orbits',len(orbits),'formal',[(str(ff),m)for ff,m in original_cf],flush=True);branches=[];survivors=[]
 for v,orb in sorted(orbits.items()):
  T=from_values(R,p,v);validate_general(T);require(all(T[i][j]==T[j][i] for i in range(n)for j in range(n)),'noncommutable signed table');a=Characters(T);rec={'values':v,'orbit_size':len(orb),'generator':a.k,'characters':[]}
  for f,m in a.components:
   K,ds,delta,pD=a.component(f);required=list(original_cf)+list(a.cf);zero=next((i for i,d in enumerate(ds)if not d),None);uneq=next((i for i,d in enumerate(ds)if d!=ds[du[i]]),None)
   why={'kind':'zero','object':zero}if zero is not None else {'kind':'duality','object':uneq}if uneq is not None else norm_failure(pD,required)or field_failure(f,required)
   item={'factor':pc(f),'global_dimension_polynomial':pc(pD),'dimensions':[ec(d)for d in ds],'obstruction':why};rec['characters'].append(item)
   if why is None:survivors.append({'values':v,'factor':pc(f)})
  branches.append(rec);print('branch',len(branches),'chars',len(rec['characters']),'remaining',len(survivors),flush=True)
 result={'id':rid,'complete':True,'signed_tables':len(vals),'sign_orbits':len(orbits),'original_linear_codegree_polynomial':pc(q),'original_matrix_block_formal_codegree':str(fe),'branches':branches,'survivors':survivors,'seconds':time.monotonic()-start};(out/(rid+'_comm_characters.json')).write_text(json.dumps(result,indent=2)+'\n');print('RESULT',rid,'survivors',len(survivors),'seconds',result['seconds'],flush=True)
if __name__=='__main__':
 rings={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))}
 for rid in sys.argv[1:]or['R6_7_200','R6_8_491']:check(rings[rid],rid)
