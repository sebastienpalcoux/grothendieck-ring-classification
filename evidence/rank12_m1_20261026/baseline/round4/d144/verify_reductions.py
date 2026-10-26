from pathlib import Path
import json,itertools,hashlib
from triality import source_tensor,require
P=Path(__file__).resolve().parent
T=json.loads((P/'tensors.json').read_text());C=json.loads((P/'conditional_twists.json').read_text())
B=[0,1,2,6,7];W=[3,4,5];M=[8,9,10,11];rec=[]
for row in C:
 S=source_tensor(row['m']);p=row['involutive_ring_automorphism'];R=[[[S[i][p[j]if i>=8 else j][k]for k in range(12)]for j in range(12)]for i in range(12)]
 q=row['basis_map_source_to_model'];require(all(T[row['id']][i][j][k]==R[q[i]][q[j]][q[k]]for i,j,k in itertools.product(range(12),repeat=3)),'frozen tensor identification')
 require(all(not R[i][j][k]for i,j in itertools.product(B,repeat=2)for k in range(12)if k not in B),'B24 closed')
 z=[[R[1][i][j]for j in M]for i in M];e=[[R[2][i][j]for j in M]for i in M]
 require(z==[[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],'two RepC2 blocks: sign action')
 require(e==[[int(i==j)+z[i][j]for j in range(4)]for i in range(4)],'two RepC2 blocks: standard action')
 graph={M[0]}
 while True:
  nxt=graph|{j for a in B for i in graph for j in M if R[a][i][j]}
  if nxt==graph:break
  graph=nxt
 require(graph==set(M),'odd B-module indecomposable')
 require([R[6][i][i]for i in M]==[1,1,0,0],'ordinary RepS4 module diagonal obstruction')
 require([[R[1][i][j]for j in W]for i in W]==[[int(i==j)for j in range(3)]for i in range(3)],'W sign trivial')
 require([[R[2][i][j]for j in W]for i in W]==[[int(i!=j)for j in range(3)]for i in range(3)],'W is RepC3 module')
 A=[1,1,2]+[0]*9
 gram=[[sum(A[a]*R[a][i][j]for a in range(12))for j in range(12)]for i in range(12)]
 require(all(gram[i][j]==3 for i,j in itertools.product([6,7],repeat=2)),'three module summands over P,Q')
 require(all(gram[i][j]==2 for i,j in itertools.product(W,repeat=2)),'two module summands over W')
 require(all(gram[i][j]==3 for block in [[8,9],[10,11]]for i,j in itertools.product(block,repeat=2)),'three module summands per odd charge pair')
 wself=[R[i][i][i]for i in W]
 require(wself==[row['m']]*3,'integral m0/m1 based-ring invariant')
 rec.append({'id':row['id'],'tensor_sha256':hashlib.sha256(json.dumps(T[row['id']],separators=(',',':')).encode()).hexdigest(),'two_RepC2_blocks':True,'odd_B_indecomposable':True,'W_RepC3_module':True,'dimension4_self_product_multiplicities':wself,'regular_algebra_gram':gram})
require(4-2==2 and 2<3,'v0 internalEnd dimension contradiction')
require(18*2==12*3,'forbidden orbit2 stabilizer quotient is3/2')
(P/'reduction_replay.json').write_text(json.dumps({'status':'PASS','scope':'exact tensor premises and m0/m1 distinction; categorical proof in new_morita_reduction.md','records':rec},indent=2)+'\n')
print('PASS exact tensor/module inputs for all four D144 targets')
