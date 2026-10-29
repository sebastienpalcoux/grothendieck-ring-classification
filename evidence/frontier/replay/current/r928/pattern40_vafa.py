from pathlib import Path
BASE=Path(__file__).resolve().parent
exec((BASE/'cyclotomic_arithmetic.py').read_text())
from pathlib import Path
BASE=Path(__file__).resolve().parent
data=json.load(open(BASE/'pattern40_singletons.json'));As={t:set() for t in (60,84,96)}
for t in As:
 for smallroots in data[str(t)]:
  missing=9-len(smallroots);p=[a*72 for a in smallroots]
  if not missing:As[t].add(tuple(p))
  elif missing in (2,3):
   for o in orbits:
    if len(o)==missing:As[t].add(tuple(sorted(p+o)))
print('Acounts',{t:len(a) for t,a in As.items()},flush=True)
H=json.load(open(BASE/'vafa_probe.json'))['H_quartets'];Bs={60:[(96,96,108)],84:[(36,96,96)],96:[(60,60,108),(36,84,84)]}
p=next(x for x in json.load(open(BASE/'prior/spectral_reduction.json'))['patterns'] if x['pattern']==40);W=p['N_W'];n=p['rank'];M=[sum(W[4][r]*W[r][j] for r in range(n)) for j in range(n)]
groups=[[i] for i in range(6)]+[list(range(6,15)),list(range(15,18)),list(range(18,22)),[22]]
assert all(W[r][j]==W[g[0]][j] for g in groups for r in g for j in range(n))
coeff=[[3*W[4][g[0]]*W[g[0]][j] for g in groups] for j in range(n)]
survive=[]
for t in As:
 for A in sorted(As[t]):
  for bt in Bs[t]:
   for h in H:
    phase=[0]*4+[432,t*12]+list(A)+[v*12 for v in bt]+h+[t*12]
    sums=[sum(phase[i] for i in g) for g in groups]
    if all((M[j]*phase[j]+M[j]*3*432-sum(a*b for a,b in zip(coeff[j],sums)))%N==0 for j in range(n)):
     survive.append({'t':t,'A':A,'B':bt,'H':h})
print('survivors',len(survive),'counts',dict(Counter(x['t'] for x in survive)))
(BASE/'pattern40_vafa.json').write_text(json.dumps({'A_counts':{t:len(a) for t,a in As.items()},'survivors':survive},indent=2)+'\n')
