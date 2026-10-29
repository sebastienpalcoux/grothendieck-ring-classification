"""Exact bounded matching checks for the two pattern-40 phase candidates."""
from pathlib import Path
BASE=Path(__file__).resolve().parent
exec((BASE/'cyclotomic_arithmetic.py').read_text())
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
BASE=Path(__file__).resolve().parent
p=next(x for x in json.load(open(BASE/'prior/spectral_reduction.json'))['patterns'] if x['pattern']==40)
n=p['rank'];Bq=[[Q(a)+Q(b) for a,b in zip(x,y)] for x,y in zip(p['baseline_M'],p['fixed_Q0'])]
assert all(x.denominator==1 for row in Bq for x in row)
B=[[int(x) for x in row] for row in Bq];u=B[3];M=p['N_c_squared'][3]
dims=[];sq2=add(rt[N//8],rt[-N//8]);sq3=add(rt[N//12],rt[-N//12]);sq6=mul(sq2,sq3)
for d in p['dimensions']:dims.append(add(*(scale(int(a),b) for a,b in zip(d,[rt[0],sq2,sq3,sq6]))))
D=add(scale(144,rt[0]),scale(96,sq2),scale(80,sq3),scale(56,sq6));D2=mul(D,D)
def matchings(indices,k):
 if k==0:
  yield [];return
 if len(indices)<2*k:return
 a=indices[0]
 yield from matchings(indices[1:],k)
 for j,b in enumerate(indices[1:]):
  rem=indices[1:j+1]+indices[j+2:]
  for tail in matchings(rem,k-1):yield [(a,b)]+tail
allmatch=[];gs=[list(range(6,15)),list(range(15,18)),list(range(18,22))]
for counts in product(*(range(len(g)//2+1) for g in gs)):
 if sum(counts)!=3:continue
 for tup in product(*(list(matchings(g,k)) for g,k in zip(gs,counts))):allmatch.append(sum(tup,[]))
assert len(allmatch)==5427,len(allmatch)
output=[]
for row in json.load(open(BASE/'pattern40_indicators.json'))['survivors']:
 phase=[0]*4+[N//4,row['t']*12]+row['A']+[v*12 for v in row['B']]+row['H']+[row['t']*12]
 assert len(phase)==n
 base=[(M[j]*phase[j]-3*sum(u[r]*B[r][j]*phase[r] for r in range(n)))%N for j in range(n)]
 survive=[]
 for pairs in allmatch:
  z=base[:]
  for a,b in pairs:
   assert u[a]==u[b]
   q=3*u[a]*(phase[b]-phase[a]);z[a]=(z[a]+q)%N;z[b]=(z[b]-q)%N
  if not any(z):survive.append(pairs)
 hist=[{'test':'3C-Vafa','before':len(allmatch),'after':len(survive)}]
 for k in [2,3,4]:
  baseline=add(*(scale(2*B[i][j],mul(mul(dims[i],dims[j]),rt[(k*(phase[i]-phase[j]))%N])) for i in range(n) for j in range(n) if B[i][j]))
  edges={tuple(edge) for mat in survive for edge in mat};delta={}
  for a,b in edges:
   delta[a,b]=scale(2,mul(mul(dims[a],dims[a]),add(scale(2,rt[0]),scale(-1,rt[(k*(phase[a]-phase[b]))%N]),scale(-1,rt[(k*(phase[b]-phase[a]))%N]))))
  phi=int(s.totient(k));basis=[dict(mul(D2,rt[j*N//k])) for j in range(phi)]
  inds=sorted(set().union(*(set(a) for a in basis)))
  BM=s.Matrix([[a.get(i,0) for a in basis] for i in inds]);piv=BM.T.rref()[1];iv=BM[list(piv),:].inv();kept=[];coefs=[]
  for mat in survive:
   z=dict(add(baseline,*(delta[tuple(edge)] for edge in mat)))
   co=iv*s.Matrix([z.get(inds[i],0) for i in piv]);good=not(set(z)-set(inds)) and BM*co==s.Matrix([z.get(i,0) for i in inds]) and all(x.q==1 for x in co)
   if k==2:good=good and co[0]==1
   if k==3:
    good=good and co[1]==0 and (17-int(co[0]))%3==0 and (17-int(co[0]))//3>=0 and (17+2*int(co[0]))//3>=0
   if good:kept.append(mat);coefs.append([str(v) for v in co])
  hist.append({'test':f'nu{k}C','before':len(survive),'after':len(kept),'coefficients':sorted(set(tuple(c) for c in coefs))});survive=kept
 print('H',row['H'][0],hist,'matchings',survive)
 output.append({'phase':row,'history':hist,'matchings':survive})
(BASE/'pattern40_matching.json').write_text(json.dumps(output,indent=2)+'\n')
