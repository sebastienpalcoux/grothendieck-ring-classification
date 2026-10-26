from pathlib import Path
import sys,json,itertools,collections,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
from extra_models import a4_table
common=gm.common
D=json.loads((BASE/'tensors.json').read_text());F={r['id']:r['family']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']in ['D24','D40','D32']}

def subs(M,size):
 seen=set()
 for a,b in itertools.product(range(len(M)),repeat=2):
  H=tuple(gm.subgroup(M,[a,b]))
  if len(H)==size and H not in seen:seen.add(H);yield list(H)

def main():
 groups=[('A4 x C2',gm.group_product(a4_table(),[[0,1],[1,0]])),('S4',gm.permutation_group(4)[1]),('SL(2,3)',gm.matrix_group(3,True)[1])]
 buckets=collections.defaultdict(list)
 for rid in F:buckets[common.coarse(D[rid])].append(rid)
 out={};att=[]
 for name,G in groups:
  seen=[];inv=[next(b for b in range(len(G))if G[a][b]==0)for a in range(len(G))]
  for H in subs(G,4):
   if any({G[G[g][a]][inv[g]]for a in H}==set(K)for K in seen for g in range(len(G))):continue
   seen.append(H);T,info=gm.fusion(G,H);hits=[]
   if T is not None:
    for rid in buckets[common.coarse(T)]:
     p=common.based_iso(D[rid],T)
     if p is not None:
      out.setdefault(rid,[]).append(dict(name='C('+name+',1,H4,1)',constructor='group_theoretical',parameters=dict(group_table=G,subgroup=H,cocycle='trivial',subgroup_cochain='trivial'),model_tensor=T,basis_map_source_to_model=p));hits.append(rid)
   att.append(dict(group=name,subgroup=H,info=info,matches=hits));print(name,H,info,hits,flush=True)
 (OUT/'group_results.json').write_text(json.dumps([dict(id=rid,family=F[rid],models=ms)for rid,ms in out.items()],indent=2)+'\n');(OUT/'group_attempts.json').write_text(json.dumps(att,indent=2)+'\n')
if __name__=='__main__':main()
