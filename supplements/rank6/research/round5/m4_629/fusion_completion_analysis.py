import sys,json,itertools,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];cc=json.load(open(here/'rank35_modular_completions.json'));br=next(x for x in cc['branches'] if x['obstruction'] is None);S=[[C([s.Rational(z) for z in v]) for v in row] for row in br['S']];n=len(S);N=[[[0]*n for _ in range(n)] for _ in range(n)];st=time.monotonic()
for i,j,k in itertools.combinations_with_replacement(range(n),3):
 z=sum((S[i][l]*S[j][l]*S[k][l]/S[0][l] for l in range(n)),C.zero);value=integer(z)
 for a,b,c in set(itertools.permutations((i,j,k))):N[a][b][c]=value
subs=set()
for a in range(1,n):
 known={0,a}
 while True:
  new=known|{k for i in known for j in known for k,c in enumerate(N[i][j]) if c}
  if new==known:break
  known=new
 subs.add(tuple(sorted(known)))
out={'rank':n,'signs':br['signs'],'fusion_tensor':N,'simple_generated_subrings':[list(x) for x in sorted(subs,key=lambda x:(len(x),x))]};(here/'rank35_fusion_data.json').write_text(json.dumps(out));print('subrings',[(len(x),x) for x in sorted(subs,key=len)],'seconds',time.monotonic()-st,flush=True)
