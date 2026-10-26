from pathlib import Path
import itertools,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parent
BASE=ROOT
import group_ops as gt
import monomial

def candidate():
 vals,E=gt.matrix_group(5,True);z=vals.index((4,0,0,4));inv=[next(j for j in range(120)if E[i][j]==0)for i in range(120)]
 reps=sorted({min(i,E[z][i])for i in range(120)});ind={a:i for i,x in enumerate(reps)for a in [x,E[z][x]]};Q=[[ind[E[a][b]]for b in reps]for a in reps]
 r=next(i for i in range(120)if gt.order(E,i)==5);C=set(gt.subgroup(E,[r]));s=next(i for i in range(120)if gt.order(E,i)==4 and E[E[i][r]][inv[i]]==inv[r]);D=gt.subgroup(Q,[ind[r],ind[s]])
 sec=list(reps);sign={};powers=[0]
 for _ in range(4):powers.append(E[powers[-1]][r])
 for k,t in itertools.product(range(5),range(2)):
  g=E[powers[k]][s if t else 0];sec[ind[g]]=g;sign[ind[g]]=t
 lam=[[int(E[sec[a]][sec[b]]!=sec[Q[a][b]])for b in range(60)]for a in range(60)]
 for a,b in itertools.product(range(60),repeat=2):monomial.require(E[sec[a]][sec[b]]==E[z if lam[a][b]else 0][sec[Q[a][b]]],'actual Schur cover')
 for a,b,c in itertools.product(range(60),repeat=3):monomial.require((lam[b][c]+lam[a][Q[b][c]]-lam[Q[a][b]][c]-lam[a][b])%2==0,'all216000 Schur cocycle equations')
 for a,b in itertools.product(D,repeat=2):monomial.require(lam[a][b]==sign[a]*sign[b],'adapted D10 Schur section')
 G=gt.group_product(Q,[[0,1],[1,0]]);H=sorted(2*a+sign[a]for a in D)
 monomial.require(H==gt.subgroup(G,H),'graph subgroup')
 return G,H,lam

def main():
 start=time.monotonic();G,H,lam=candidate();data=json.load(open(BASE/'source_tensors.json'));out=[]
 for eps in [0,1]:
  w=lambda a,b,c:10*eps*((lam[a//2][b//2]+(a%2)*(b%2))*(c%2)%2)
  R,info=monomial.construct(G,H,w)
  hits=[]
  if R is not None:
   gt.common.validate(R)
   for rid,S in data.items():
    if gt.common.coarse(S)!=gt.common.coarse(R):continue
    p=gt.common.based_iso(S,R)
    if p is not None:
     monomial.require(all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'full exact matching')
     hits.append(dict(id=rid,basis_map_source_to_model=p,tensor_sha256=gt.common.sha(S)))
  result=dict(eps=eps,group_table=G,subgroup=H,schur_cocycle=lam,model_tensor=R,info=info,matches=hits,seconds=time.monotonic()-start)
  out.append(result);(ROOT/'graph_twist_models.json').write_text(json.dumps(out,indent=2)+'\n');print('EPS',eps,'matches',hits,'info', {k:v for k,v in info.items()if k!='objects'},'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
