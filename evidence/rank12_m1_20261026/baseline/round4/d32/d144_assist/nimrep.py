"""Complete small integer NIMrep forcing after the categorical orbit reduction."""
from pathlib import Path
import itertools,json,sys
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));from ring_checks import require,validate,based_iso
def source_tensor(m):
 require(m==0,'frozen integral m=0 source');return json.loads((HERE/'inputs/source_m0.json').read_text())
I=np.eye(4,dtype=int);Z=I[[1,0,3,2]];J=np.ones((4,4),dtype=int)
def P(s,t):
 A=J.copy()
 for b,v in enumerate([s,t]):A[2*b:2*b+2,2*b:2*b+2]=np.eye(2,dtype=int)[[0,1]if v==1 else[1,0]]
 return A

def candidate(s,t,du,m=0):
 base=source_tensor(m);L=[I,Z,I+Z,J,J,J,P(s,t),Z@P(s,t)];D=I[list(du)];Q=[D@a@D for a in L];R=np.zeros((12,12,12),dtype=int);R[:8,:8,:8]=np.array(base)[:8,:8,:8]
 for a in range(8):R[a,8:,8:]=L[a];R[8:,a,8:]=Q[a]
 for x,y,a in itertools.product(range(4),range(4),range(8)):R[x+8,y+8,a]=L[a][du[y],x]
 return R.tolist()
def main():
 p=HERE/'inputs';targets=json.loads((p/'tensors.json').read_text())|json.loads((p/'positive_tensors.json').read_text());out=[]
 for s,t in itertools.product([1,-1],repeat=2):
  for du in [(2,3,0,1),(3,2,1,0)]:
   R=candidate(s,t,du)
   try:validate(R);ok=True;err=None
   except Exception as e:ok=False;err=str(e)
   matches={}
   if ok:
    for k,S in targets.items():
     if isinstance(S,dict):S=S.get('tensor',S.get('fusion_tensor'))
     iso=based_iso(R,S)
     if iso is not None:matches[k]=iso
   witness=None
   if s==t:
    x=8;y=8+du[0];lhs=sum(R[x][x][a]*R[a][y][x]for a in range(12));rhs=sum(R[x][y][a]*R[x][a][x]for a in range(12));require((lhs,rhs)==(5,6),'explicit associativity contradiction');witness={'triple':[x,x,y],'output':x,'left':lhs,'right':rhs}
   row={'associativity_witness':witness,'P_signs':[s,t],'duality':du,'valid':ok,'error':err,'matches':matches};out.append(row);print(row,flush=True)
 require(sum(r['valid']for r in out)==4,'exactly four valid label choices')
 require(all(set(r['matches'])=={'R12_1_320'}for r in out if r['valid']),'all valid choices bind exactly R320')
 require(all(r['error']=='associativity'for r in out if not r['valid']),'all four other choices fail associativity')
 (HERE/'nimrep.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
