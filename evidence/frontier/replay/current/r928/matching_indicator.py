from pathlib import Path
BASE=Path(__file__).resolve().parent
exec((BASE/'cyclotomic_arithmetic.py').read_text())
from pathlib import Path
from fractions import Fraction as Q
BASE=Path(__file__).resolve().parent
p=next(x for x in json.load(open(BASE/'prior/spectral_reduction.json'))['patterns'] if x['pattern']==186)
B=[[int(Q(a)+Q(b)) for a,b in zip(x,y)] for x,y in zip(p['baseline_M'],p['fixed_Q0'])]
dims=[];sq2=add(rt[N//8],rt[-N//8]);sq3=add(rt[N//12],rt[-N//12]);sq6=mul(sq2,sq3)
for d in p['dimensions']:dims.append(add(*(scale(int(a),b) for a,b in zip(d,[rt[0],sq2,sq3,sq6]))))
D=add(scale(144,rt[0]),scale(96,sq2),scale(80,sq3),scale(56,sq6));D2=mul(D,D)
rows=json.load(open(BASE/'matching_vafa.json'))['results'];kept=[]
for row in rows:
 t,k,A,bt,h=row['phase'];phase=[0]*4+[N//4,t*12]+A+[v*12 for v in bt]+h+[k,t*12]
 # Restrict to the 12 W-nu2 survivors reported independently by r928 agent.
 if t!=96 or tuple(bt)!=(60,60,108) or A not in ([288,288,648,648,864],[288,288,864,1512,1512]):continue
 baseline=add(*(scale(2*B[i][j],mul(mul(dims[i],dims[j]),rt[(2*(phase[i]-phase[j]))%N])) for i in range(20) for j in range(20) if B[i][j]))
 edges={tuple(edge) for mat in row['matchings'] for edge in mat};delta={}
 for a,b in edges:
  assert dims[a]==dims[b]
  delta[a,b]=scale(2,mul(mul(dims[a],dims[a]),add(scale(2,rt[0]),scale(-1,rt[(2*(phase[a]-phase[b]))%N]),scale(-1,rt[(2*(phase[b]-phase[a]))%N]))))
 ok=[]
 for mat in row['matchings']:
  if add(baseline,*(delta[tuple(edge)] for edge in mat))==D2:ok.append(mat)
 print('phase',row['phase'],'initial',len(row['matchings']),'nu2C1',len(ok))
 if ok:kept.append({'phase':row['phase'],'matchings':ok})
print('PHASES',len(kept),'MATCHINGS',sum(len(r['matchings']) for r in kept))
(BASE/'matching_indicator.json').write_text(json.dumps({'results':kept},indent=2)+'\n')
