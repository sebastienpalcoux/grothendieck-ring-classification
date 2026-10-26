from pathlib import Path
import itertools,json,sys,time,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm;import common
sys.path.insert(0,str(ROOT/'rank12-m1-round2-20261025/family_integral'));from order48_models import conjugacy_subgroups

def cyclic(n):return [[(a+b)%n for b in range(n)]for a in range(n)]
def semidirect(K,phi):
 n=len(K);phis=[list(range(n)),phi,[phi[phi[a]]for a in range(n)]]
 common.require(all(phi[phis[2][a]]==a for a in range(n)),'order3 automorphism')
 common.require(all(phi[K[a][b]]==K[phi[a]][phi[b]]for a,b in itertools.product(range(n),repeat=2)),'automorphism')
 return [[K[a//3][phis[a%3][b//3]]*3+(a%3+b%3)%3 for b in range(3*n)]for a in range(3*n)]
def groups():
 C2=cyclic(2);C4=cyclic(4)
 yield 'A4xC4',gm.group_product(gm.a4_table(),C4)
 vals,S=gm.matrix_group(3,True);yield'SL2_3xC2',gm.group_product(S,C2)
 # central quotient SL2(3)xC4 by (-I,2)
 minus=vals.index((2,0,0,2));P=gm.group_product(S,C4);z=4*minus+2;reps=sorted({min(a,P[a][z])for a in range(96)});ix={a:i for i,a in enumerate(reps)}
 yield 'SL2_3_central_C4',[[ix[min(P[a][b],P[P[a][b]][z])]for b in reps]for a in reps]
 K=gm.group_product(C4,C4);phi=[((-(a%4))%4)*4+(a//4-a%4)%4 for a in range(16)]
 yield 'C4square_sdp_C3',semidirect(K,phi)
 K=[[a^b for b in range(16)]for a in range(16)]
 def transform(a):
  b,c,d,e=[(a>>i)&1 for i in range(4)]
  return c+2*(b^c)+4*e+8*(d^e)
 yield 'C2four_sdp_C3_fixedpointfree',semidirect(K,[transform(a)for a in range(16)])
 yield 'A4xV4',gm.group_product(gm.a4_table(),[[a^b for b in range(4)]for a in range(4)])

def main():
 D=json.loads((BASE/'tensors.json').read_text());U=json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text());ids=[r['id']for r in U if r['exact_dimension_character']['family']=='D48'];rows=[];attempts=[];start=time.monotonic()
 for name,G in groups():
  A=np.array(G);common.require(all(np.array_equal(A[A[a],:],A[a,A])for a in range(48)),'associative group')
  for size in [4,8]:
   for H in conjugacy_subgroups(G,size):
    try:R,info=gm.fusion(G,H)
    except ValueError as e: R=None;info=dict(unsupported=str(e))
    hits=[]
    if R is not None:
     for rid in ids:
      p=common.based_iso(D[rid],R)
      if p is not None:
       hits.append(rid);rows.append(dict(id=rid,status='unitarily_realized',name='C('+name+',H,1)',group=G,subgroup=H,tensor=R,source_to_model=p))
    attempts.append(dict(name=name,subgroup=H,info=info,hits=hits));print(name,H,info,hits,flush=True)
    (OUT/'extra_group_models.json').write_text(json.dumps(rows,indent=2)+'\n');(OUT/'extra_group_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print('DONE',len(rows),time.monotonic()-start)
if __name__=='__main__':main()
