"""All fixed-invertible extension classes for coherent C2 actions.

For an involution fixing only four invertibles, every action-dependent
fusion coefficient is on that fixed subgroup. Its possible equivariant
extensions are enumerated by H2(F,C2). All classes are solved together as
right-hand sides of the exact scalar tensorator/coherence equations.
"""
from pathlib import Path
import collections,itertools,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(BASE/'sources/work/rank11'))
import common
from feudal import prime_power_solve
from ising_equivariants import maps
from gauge_actions import reconstructed,equations,verify_action,equiv

def cocycles(R,fixed):
 mul=lambda a,b:R[a][b].index(1);pairs=list(itertools.product(fixed[1:],repeat=2));all0=[]
 for bits in itertools.product(range(2),repeat=len(pairs)):
  d=dict(zip(pairs,bits));s=lambda a,b:d.get((a,b),0)
  if all((s(b,c)+s(a,mul(b,c))-s(mul(a,b),c)-s(a,b))%2==0 for a,b,c in itertools.product(fixed,repeat=3)):all0.append(bits)
 cob=[]
 for bits in itertools.product(range(2),repeat=len(fixed)-1):
  v=dict(zip(fixed,[0]+list(bits)));cob.append(tuple((v[a]+v[b]-v[mul(a,b)])%2 for a,b in pairs))
 seen=set();out=[]
 for b in all0:
  if b in seen:continue
  seen|={tuple(x^y for x,y in zip(b,c))for c in cob};out.append(dict(zip(pairs,b)))
 return out

def main():
 start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());fam=json.loads((BASE/'unresolved_families.json').read_text())['records'];targets={r['id']:D[r['id']]for r in fam if r['family']=='D32'};buckets=collections.defaultdict(list)
 for rid,R in targets.items():buckets[common.coarse(R)].append((rid,R))
 receipts=[];hits=collections.defaultdict(list);seen=set();q=256;total=0
 for row in json.loads((BASE/'feudal.json').read_text())['records']:
  c=row['model']
  if not c or len(c['serfs'])!=8 or len(c['lords'])!=4:continue
  R=D[row['id']];F=reconstructed(R,c,q);count=0
  for p in maps(R,c):
   fixed=[i for i in range(len(R))if p[i]==i];cc=cocycles(R,fixed);A,B,keys=equations(R,F,p,q);basecols=len(keys);ix={k:i for i,k in enumerate(keys)}
   ukeys=[('u',i)for i in fixed if i];keys+=ukeys;ix.update({k:basecols+j for j,k in enumerate(ukeys)});extra=[];rhs=[]
   def add(terms,vals):
    z=collections.Counter()
    for a,k in terms:
     if k in ix:z[ix[k]]+=a
    extra.append(z);rhs.append(vals)
   for i in fixed:
    if i:add([(1,('eta',i)),(-2,('u',i))],[0]*len(cc))
   for a,b in itertools.product(fixed[1:],repeat=2):
    d=R[a][b].index(1)
    add([(1,('u',a)),(1,('u',b)),(-1,('u',d)),(-1,('J',a,b,d))],[(q//2)*z[a,b]for z in cc])
   AA=np.zeros((A.shape[0]+len(extra),len(keys)),dtype=np.int64);AA[:A.shape[0],:basecols]=A
   BB=np.tile(B,(1,len(cc)))
   BB=np.vstack((BB,np.array(rhs,dtype=np.int64)))
   for i,r in enumerate(extra):
    for j,v in r.items():AA[A.shape[0]+i,j]=v
   sols=prime_power_solve(AA,BB,2,8);total+=len(cc)
   for col,sol in sols.items():
    common.require(np.all((AA@sol-BB[:,col])%q==0),'all original action/class equations');count+=1
    J={key[1:]:int(sol[i])for i,key in enumerate(keys)if key[0]=='J'};eta=[0]+[int(sol[ix['eta',i]])for i in range(1,len(R))];u={0:0,**{i:int(sol[ix['u',i]])for i in fixed if i}}
    verify_action(R,F,p,J,eta,q);lift=[2*u[i]if i in u else eta[i]for i in range(len(R))];T,labs=equiv(R,p,J,lift,q);key=common.sha(T)
    if key in seen:continue
    seen.add(key);common.validate(T);matched=[]
    for rid,S in buckets[common.coarse(T)]:
     bm=common.based_iso(S,T)
     if bm is None:continue
     common.require(all(S[i][j][k]==T[bm[i]][bm[j]][bm[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 model coefficients');matched.append(rid)
     hits[rid].append(dict(name='Coherent C2 equivariantization of generalized Ising '+row['id'],constructor='liptrap_C2_equivariant',parameters=dict(base_id=row['id'],base_tensor=R,base_liptrap_model=c,automorphism=p,phase_modulus=q,tensorator_phases=[[*k,v]for k,v in J.items()],square_coherence_phases=eta,fixed_reference_phases=[[i,v]for i,v in u.items()],fixed_subgroup_cocycle=[[a,b,z]for(a,b),z in cc[col].items()],labels=labs),model_tensor=T,basis_map_source_to_model=bm))
     print('HIT',rid,'base',row['id'],'p',p,'class',col,flush=True)
    receipts.append(dict(base_id=row['id'],automorphism=p,class_index=col,status='verified_unitary_action',matches=matched,tensor_sha256=key))
   receipts.append(dict(base_id=row['id'],automorphism=p,class_count=len(cc),verified_classes=sorted(map(int,sols)),not_an_exclusion=True))
  print('base',row['id'],'verified action/classes',count,'seconds',time.monotonic()-start,flush=True)
 rows=[dict(id=rid,tensor_sha256=common.sha(D[rid]),models=ms)for rid,ms in hits.items()]
 (HERE/'cocycle_equivariant_models.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'cocycle_equivariant_attempts.json').write_text(json.dumps(dict(records=receipts,action_classes_considered=total,seconds=time.monotonic()-start),indent=2)+'\n')
 print('TOTAL',len(hits),'models',sum(map(len,hits.values())),'distinct candidates',len(seen),'actionclasses',total,'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
