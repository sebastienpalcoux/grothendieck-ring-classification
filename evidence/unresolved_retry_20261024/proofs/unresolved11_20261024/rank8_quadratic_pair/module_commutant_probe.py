import itertools,json
from pathlib import Path
import sympy as s
P=Path(__file__).parent;a=json.loads((P/'gh6_m2_module_probe.json').read_text())
small=[0,1,2,3,4,7];big=[5,6]
for index,c in enumerate(a['completions']):
 Ns=c['full_action'];perms=[]
 for q in itertools.permutations(small):
  for r in [(5,6),(6,5)]:
   p=[None]*8
   for i,j in zip(small,q):p[i]=j
   for i,j in zip(big,r):p[i]=j
   if all(all(N[p[i]][p[j]]==N[i][j]for i in range(8)for j in range(8))for N in Ns):perms.append(p)
 def order(p):
  q=list(range(8))
  for n in range(1,100):
   q=[p[x]for x in q]
   if q==list(range(8)):return n
 print(index,len(perms),'orders',[order(p)for p in perms])
 six=[p for p in perms if order(p)==6]
 print('six',six)
 for p in six:
  cyc=[0]
  for k in range(1,6):cyc.append(p[cyc[-1]])
  if len(set(cyc))!=6 or p[5]!=6:continue
  for sign in [1,-1]:
   rho=s.zeros(8)
   for k,i in enumerate(cyc):rho[cyc[(-k)%6],i]=1
   for i in small:
    for j in big:rho[i,j]=rho[j,i]=1
   rho[5,5]=rho[6,6]=(11+sign)//2;rho[5,6]=rho[6,5]=(11-sign)//2
   if all(rho*s.Matrix(N)==s.Matrix(N)*rho for N in Ns):print('GH(C6,2) commutes:',p,sign)
