from extra_models import *
import sys,importlib.util
p=REPO/'supplements/rank6/software';sys.path.insert(0,str(p))
spec=importlib.util.spec_from_file_location('gt',p/'group_theoretical.py');gt=importlib.util.module_from_spec(spec);spec.loader.exec_module(gt)
def subgroups(G):
 n=len(G);found={frozenset([0])};queue=[frozenset([0])]
 for H in queue:
  for a in range(1,n):
   if a in H:continue
   J=frozenset(gt.subgroup(G,list(H)+[a]))
   if J not in found:found.add(J);queue.append(J)
 return sorted(found,key=lambda x:(len(x),sorted(x)))
def rank_est(G,H):
 # invariant estimate character count; supported groups stabilizers.
 inv=[row.index(0)for row in G];seen=set();r=0
 for z in range(len(G)):
  if z in seen:continue
  D={G[G[a][z]][b]for a in H for b in H};seen|=D
  K=[a for a in H if G[G[inv[z]][a]][z]in H]
  # number conjugacy classes in stabilizer
  seenK=set();k=0
  for x in K:
   if x not in seenK:seenK|={G[G[a][x]][inv[a]]for a in K};k+=1
  r+=k
 return r

def candidates():
 perms,S4=gt.permutation_group(4);_,A4=gt.permutation_group(4,True)
 groups=[('S4',S4),('S4xC2',[[2*S4[a//2][b//2]+((a%2)^(b%2))for b in range(48)]for a in range(48)])]
 for name,G in groups:
  inv=[row.index(0)for row in G];seen=set()
  for H0 in subgroups(G):
   H=sorted(H0)
   if len(H)not in[1,2,4,6,8,10]:continue
   if tuple(H)in seen:continue
   seen|={tuple(sorted(G[G[a][h]][inv[a]]for h in H))for a in range(len(G))}
   r=rank_est(G,H)
   if r not in[9,10]:continue
   try:T=gt.fusion(G,H)
   except Exception as e:print('SKIP',name,H,str(e),flush=True);continue
   if max(v for M in T for row in M for v in row)>1:continue
   yield name,G,H,T

def run():
 known=json.load(open(OUT/'known_models_zested.json'));lookup={x['id']:x for x in known};by=collections.defaultdict(list)
 for n in[9,10]:
  for i,R in enumerate(read(n),1):by[(n,coarse(R))].append((f'R{n}_1_{i}',R))
 new=[]
 for name,G,H,T in candidates():
  print('CONSTRUCT',name,H,len(T),flush=True)
  for rid,R in by[(len(T),coarse(T))]:
   bm=based_iso(R,T)
   if bm is None:continue
   rec={'model':f'C({name},1,H,1), H={H}','constructor':'group_theoretical','parameters':{'group_name':name,'group_table':G,'subgroup':H},'reference':'Untwisted group-theoretical category via H-biequivariant vector bundles on G; explicit stabilizer-character convolution','basis_map_source_to_model':bm,'model_tensor':T}
   if rid not in lookup:lookup[rid]={'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[]};new.append(rid)
   lookup[rid]['models'].append(rec);print('MATCH',rid,flush=True)
 known=sorted(lookup.values(),key=lambda x:tuple(map(int,x['id'].replace('R','').split('_'))))
 (OUT/'known_models_group.json').write_text(json.dumps(known,indent=2)+'\n');print('NEW',new)
if __name__=='__main__':run()
