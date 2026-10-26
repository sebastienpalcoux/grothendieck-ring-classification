"""Two ring-level Sylow candidates only; existence NOT asserted."""
from pathlib import Path
import json,itertools
P=Path(__file__).resolve().parent
# D8 elements r^i s^j, with r^4=s^2=1 and srs=r^-1; H=<r^2>.
G=[(i,j)for j in range(2)for i in range(4)];idx={g:i for i,g in enumerate(G)}
def prod(g,h):return ((g[0]+(-1)**g[1]*h[0])%4,(g[1]+h[1])%2)
# A=G/H=C2^2, coordinate(i mod2,j). Universal feudal group S=C4 x C2,
# odd representatives t*b^e, t^3*b^e, with t²=chosen A element.
for a0 in [(1,0),(0,1)]:
 b=(1,1) # V4(normal double-transpositions)/H
 embA={(0,0):(0,0),a0:(2,0),b:(0,1),(a0[0]^b[0],a0[1]^b[1]):(2,1)}
 invA={v:k for k,v in embA.items()};O=[(1,0),(3,0),(1,1),(3,1)];oi={x:i+8 for i,x in enumerate(O)}
 def plus(x,y):return((x[0]+y[0])%4,(x[1]+y[1])%2)
 R=[[[0]*12 for _ in range(12)]for _ in range(12)]
 for i,g in enumerate(G):
  for j,h in enumerate(G):R[i][j][idx[prod(g,h)]]=1
  for x in O:R[i][oi[x]][oi[plus(embA[(g[0]%2,g[1])],x)]]=R[oi[x]][i][oi[plus(x,embA[(g[0]%2,g[1])])]]=1
 for x,y in itertools.product(O,repeat=2):
  a=invA[plus(x,y)]
  for g in G:
   if (g[0]%2,g[1])==a:R[oi[x]][oi[y]][idx[g]]=1
 for i,j,k,l in itertools.product(range(12),repeat=4):
  if sum(R[i][j][v]*R[v][k][l]for v in range(12))!=sum(R[j][k][v]*R[i][v][l]for v in range(12)):raise ValueError('associativity')
 name='sylow_a'+''.join(map(str,a0))
 (P/(name+'.json')).write_text(json.dumps(R,separators=(',',':'))+'\n')
 print(name,'duals',[next(j for j in range(12)if R[i][j][0])for i in range(12)])
