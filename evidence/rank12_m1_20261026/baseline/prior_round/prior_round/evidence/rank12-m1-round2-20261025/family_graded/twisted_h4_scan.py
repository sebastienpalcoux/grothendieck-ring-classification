from pathlib import Path
import itertools,json,sys,collections
from h4_bimodules import construct,linear_solutions,common,need
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
D=json.loads((BASE/'tensors.json').read_text());F={r['id']:r['family']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']in ['D24','D48','D40','D32']}
def coordinates():
 els=list(itertools.product(range(3),range(2),range(2),range(2)));ix={a:i for i,a in enumerate(els)}
 def act(s,a,b):
  for _ in range(s):a,b=b,a^b
  return a,b
 def mul(x,y):
  s,a,b,z=x;t,c,d,w=y;c,d=act(s,c,d);return((s+t)%3,a^c,b^d,z^w)
 G=[[ix[mul(x,y)]for y in els]for x in els];H=[i for i,(s,a,b,z)in enumerate(els)if s==0 and z==a]
 def cocycle(i,j,k):
  s,a,b,z=els[i];t,c,d,w=els[j];u,e,f,v=els[k];c,d=act(s,c,d)
  return 2*((z*w+a*c+b*d+a*d)*v%2)
 return els,G,H,cocycle

def psi_solutions(G,H,w):
 keys=[(a,b)for a in H if a for b in H if b];ki={k:i for i,k in enumerate(keys)};A=[];B=[]
 for a,b,c in itertools.product(H,repeat=3):
  row=[0]*len(keys)
  for sign,k in [(1,(a,b)),(1,(G[a][b],c)),(-1,(b,c)),(-1,(a,G[b][c]))]:
   if k in ki:row[ki[k]]+=sign
  A.append(row);B.append(w(a,b,c))
 vals=linear_solutions(A,B)
 need(bool(vals),'subgroup multiplication cochain')
 v=vals[0];return {(a,b):0 if not a or not b else int(v[ki[a,b]])for a,b in itertools.product(H,repeat=2)}

def main():
 els,G,H,w1=coordinates();n=len(G)
 need(all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(n),repeat=3)),'semidirect group')
 need(all((w1(b,c,d)+w1(a,G[b][c],d)+w1(a,b,c)-w1(G[a][b],c,d)-w1(a,b,G[c][d]))%4==0 for a,b,c,d in itertools.product(range(n),repeat=4)),'all cocycle equations')
 buckets=collections.defaultdict(list)
 for rid in F:buckets[common.coarse(D[rid])].append(rid)
 out={};attempts=[]
 for omega in [0,1]:
  w=lambda a,b,c:omega*w1(a,b,c)
  psi0=psi_solutions(G,H,w)
  for schur in [0,1]:
   psi=lambda a,b:(psi0[a,b]+2*schur*els[a][1]*els[b][2])%4
   M,info=construct(G,H,w,psi);hits=[]
   if M is not None:
    for rid in buckets[common.coarse(M)]:
     p=common.based_iso(D[rid],M)
     if p is not None:
      hits.append(rid);out.setdefault(rid,[]).append(dict(name=f'C(A4 x C2,omega{omega},H4,psi{schur})',constructor='twisted_group_theoretical_h4',parameters=dict(group_table=G,group_coordinates=els,subgroup=H,cocycle_type=omega,subgroup_schur_class=schur,subgroup_cochain=[[a,b,psi(a,b)]for a,b in itertools.product(H,repeat=2)],cocycle_values=[[[w(a,b,c)for c in range(n)]for b in range(n)]for a in range(n)]),model_tensor=M,basis_map_source_to_model=p,object_receipt=info))
   attempts.append(dict(omega=omega,schur=schur,rank=info['rank'],matches=hits));print(omega,schur,info['rank'],hits,flush=True)
 (OUT/'h4_results.json').write_text(json.dumps([dict(id=rid,family=F[rid],models=ms)for rid,ms in out.items()],indent=2)+'\n');(OUT/'h4_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
if __name__=='__main__':main()
