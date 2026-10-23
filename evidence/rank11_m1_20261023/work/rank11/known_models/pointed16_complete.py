"""All strict involutive automorphisms with two fixed points in groups oforder16.

The candidate list independently enumerates all extensions of abelian groups of
order8 byC2, then verifies fourteen distinct groupisomorphism classes. All groups
oforder16 have an abelian index-two subgroup (standard order16classification).
"""
from standard import *
from extra_models import element_order

def giso(A,B):
 n=len(A);cl={0};gens=[]
 for a in range(1,n):
  if a in cl:continue
  gens.append(a)
  while True:
   cc=cl|{A[x][g]for x in cl for g in gens}
   if cc==cl:break
   cl=cc
 oa=[element_order(A,a)for a in range(n)];ob=[element_order(B,a)for a in range(n)]
 if sorted(oa)!=sorted(ob):return None
 for imgs in itertools.product(*[[b for b in range(n)if ob[b]==oa[a]]for a in gens]):
  mp={0:0};q=[0];good=True
  for x in q:
   for a,b in zip(gens,imgs):
    y,z=A[x][a],B[mp[x]][b]
    if y in mp:
     if mp[y]!=z:good=False;break
    elif z in mp.values():good=False;break
    else:mp[y]=z;q.append(y)
   if not good:break
  if good and len(mp)==n:
   p=[mp[a]for a in range(n)]
   if not all(p[A[a][b]]==B[p[a]][p[b]]for a,b in itertools.product(range(n),repeat=2)):raise ValueError('groupisomorphism')
   return p
 return None

def allgroups():
 groups=[]
 for oo in[(8,),(4,2),(2,2,2)]:
  A=abelian_table(oo)
  for s in auts(A):
   if not all(s[s[a]]==a for a in range(8)):continue
   for z in range(8):
    if s[z]!=z:continue
    G=[[2*A[A[a][s[b]if e else b]][z if e*f else 0]+((e+f)%2)for b in range(8)for f in range(2)]for a in range(8)for e in range(2)]
    if any(giso(G,g) is not None for g,pa in groups):continue
    if not all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(16),repeat=3)):raise ValueError('grouplaw')
    groups.append((G,{'abelian_index2_orders':oo,'sigma':s,'z':z}))
 if len(groups)!=14:raise ValueError(('order16groupcount',len(groups)))
 return groups

def main():
 data=targets();records={};attempts=[];groups=allgroups();print('groupclasses',len(groups),flush=True)
 for no,(G,pars)in enumerate(groups,1):
  sigmas=[s for s in auts(G)if sum(s[a]==a for a in range(16))==2 and all(s[s[a]]==a for a in range(16))]
  print('GROUP',no,'admissibleactions',len(sigmas),flush=True)
  for s in sigmas:
   T=pointed_equivariant(G,s);validate(T);hits=[]
   for rid,R in data.items():
    p=based_iso(R,T)
    if p is None:continue
    hits.append(rid)
    if rid in records:continue
    records[rid]={'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[{'name':f'Vec(G16_{no})^C2','constructor':'pointed_equivariant','parameters':{'group_name':f'G16_{no}','group_table':G,'automorphism':s,'group_construction':pars},'reference':'Canonical strict group-automorphism action on unitary Vec(G)','model_tensor':T,'basis_map_source_to_model':p}]}
   attempts.append({'group_index':no,'automorphism':s,'matches':hits})
   print('HIT',hits,flush=True)
 (HERE/'pointed16_models.json').write_text(json.dumps(list(records.values()),indent=2)+'\n');(HERE/'pointed16_attempts.json').write_text(json.dumps({'group_classes':14,'groups':[{'table':g,'construction':p}for g,p in groups],'actions':attempts},indent=2)+'\n')
 print('TOTAL',list(records),flush=True)
if __name__=='__main__':main()
