from pathlib import Path
import json,itertools,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
S=json.loads((P.parent/'inputs/R9_2_1975.json').read_text())['fusion_tensor'];lower=json.loads((ROOT/'rank9_m2_research/phase4/quadratic_noncomm/lower_tensors.json').read_text())['rows'];outs=[]
for group in ('V4','C4'):
 e=[0,2,1,3];G=[[a^b if group=='V4' else e.index((e[a]+e[b])%4)for b in range(4)]for a in range(4)]
 T=[[[0]*6 for _ in range(6)]for _ in range(6)]
 for a,b in itertools.product(range(4),repeat=2):T[a][b][G[a][b]]=1
 for a in range(4):
  for x in range(2):T[a][4+x][4+(x^(a//2))]=T[4+x][a][4+(x^(a//2))]=1
 for x,y in itertools.product(range(2),repeat=2):
  for a in ([2,3]if x==y else[0,1]):T[4+x][4+y][a]=1
  T[4+x][4+y][4]=T[4+x][4+y][5]=4
 F=[[0]*6 for _ in range(9)]
 for i in (0,5):F[i][0]=1
 for i in (6,7):F[i][1]=1
 F[8][2]=F[8][3]=1
 for i in (1,3):F[i][4]=1
 for i in (2,4):F[i][5]=1
 assert all(sum(S[i][j][r]*F[r][k]for r in range(9))==sum(F[i][a]*F[j][b]*T[a][b][k]for a,b in itertools.product(range(6),repeat=2))for i,j,k in itertools.product(range(9),range(9),range(6)))
 matches=[]
 for row in lower:
  R=row['N']
  for tail in itertools.permutations(range(1,6)):
   p=(0,)+tail
   if all(T[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(6),repeat=3)):
    matches.append({'id':row['id'],'basis_map':p});break
 assert matches
 outs.append({'group':group,'quotient_tensor':T,'source_to_quotient':F,'matches':matches})
print([(o['group'],o['matches'])for o in outs])
(P/'central_quotients.json').write_text(json.dumps({'source':'R9_2_1975','source_sha256':hashlib.sha256(json.dumps(S,separators=(',',':')).encode()).hexdigest(),'conditional_quotients':outs,'scope':'Requires central Tannakian lift of b5, not established by this ring calculation.'},indent=2)+'\n')
