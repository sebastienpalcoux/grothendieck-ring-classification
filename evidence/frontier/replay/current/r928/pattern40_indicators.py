from pathlib import Path
BASE=Path(__file__).resolve().parent
exec((BASE/'cyclotomic_arithmetic.py').read_text())
from pathlib import Path
BASE=Path(__file__).resolve().parent
p=next(x for x in json.load(open(BASE/'prior/spectral_reduction.json'))['patterns'] if x['pattern']==40)
W=p['N_W'];groups=[[i] for i in range(6)]+[list(range(6,15)),list(range(15,18)),list(range(18,22)),[22]]
assert all(W[i][j]==W[g[0]][h[0]] for g in groups for h in groups for i in g for j in h)
sq2=add(rt[N//8],rt[-N//8]);sq3=add(rt[N//12],rt[-N//12]);sq6=mul(sq2,sq3)
dims=[add(*(scale(int(a),b) for a,b in zip(p['dimensions'][g[0]],[rt[0],sq2,sq3,sq6]))) for g in groups]
D=add(scale(144,rt[0]),scale(96,sq2),scale(80,sq3),scale(56,sq6));D2=mul(D,D)
weights={(i,j):scale(2*W[g[0]][h[0]],mul(dims[i],dims[j])) for i,g in enumerate(groups) for j,h in enumerate(groups) if W[g[0]][h[0]]}
rows=json.load(open(BASE/'pattern40_vafa.json'))['survivors'];history=[]
for n in [2,3,4,6,8,9]:
 phi=int(s.totient(n));basis=[dict(mul(D2,rt[j*N//n])) for j in range(phi)]
 inds=sorted(set().union(*(set(a) for a in basis)));BM=s.Matrix([[a.get(i,0) for a in basis] for i in inds]);piv=BM.T.rref()[1];iv=BM[list(piv),:].inv()
 kept=[]
 for row in rows:
  t,A,bt,h=row['t'],row['A'],row['B'],row['H'];phase=[0]*4+[432,t*12]+list(A)+[v*12 for v in bt]+h+[t*12]
  pos=[add(*(rt[n*phase[k]%N] for k in g)) for g in groups];neg=[add(*(rt[-n*phase[k]%N] for k in g)) for g in groups]
  z=dict(add(*(mul(w,mul(pos[i],neg[j])) for (i,j),w in weights.items())))
  co=iv*s.Matrix([z.get(inds[i],0) for i in piv])
  good=not(set(z)-set(inds)) and BM*co==s.Matrix([z.get(i,0) for i in inds]) and all(x.q==1 for x in co)
  if good and n==2:good=list(co)==[1]
  if good and n==3:
   a,b=map(int,co);m=(17-a-b)
   good=m%3==0 and min(m//3,a+m//3,b+m//3)>=0
  if good:
   row.setdefault('indicators',{})[str(n)]=[str(x) for x in co];kept.append(row)
 print('n',n,'before',len(rows),'after',len(kept),'values',sorted(set(tuple(r['indicators'][str(n)]) for r in kept)),flush=True)
 history.append({'n':n,'before':len(rows),'after':len(kept)});rows=kept
(BASE/'pattern40_indicators.json').write_text(json.dumps({'history':history,'survivors':rows},indent=2)+'\n')
