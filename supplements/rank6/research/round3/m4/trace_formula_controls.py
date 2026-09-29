import sys,json,math,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round3_m4 import *
st=time.monotonic();results=[]
for F in [1,3,4,5,8,12,15,16,20,24]:
 C=field(s.Poly(s.cyclotomic_poly(F,s.Symbol('t')),s.Symbol('t')))
 for n in [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,32,45]:
  M=math.lcm(F,n)
  if int(s.totient(M))>64:continue
  W=field(s.Poly(s.cyclotomic_poly(M,s.Symbol('t')),s.Symbol('t')));kernel=[u for u in range(M) if math.gcd(u,M)==1 and (u-1)%F==0]
  if M==1:kernel=[0]
  for a in [0,1,2,3,4,5]:
   v=relative_root(C,F,n,a);embedded=evaluate(v.to_list(),W.unit**(M//F),W)
   explicit=sum((W.unit**((a*u*(M//n))%M) for u in kernel),W.zero)/W(len(kernel))
   require(embedded==explicit,f'relative trace mismatch F={F},n={n},a={a}')
  results.append([F,n])
report={'criterion':'normalized cyclotomic relative trace','passed':True,'pairs':results,'exact_comparisons':6*len(results),'seconds':time.monotonic()-st}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='pairs'})
