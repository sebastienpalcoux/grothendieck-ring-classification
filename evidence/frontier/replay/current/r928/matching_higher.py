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
rows=json.load(open(BASE/'matching_indicator.json'))['results'];output=[]
for row in rows:
 t,k,A,bt,h=row['phase'];phase=[0]*4+[N//4,t*12]+A+[v*12 for v in bt]+h+[k,t*12]
 if k!=936 or h[0] not in (162,378):continue
 for n in [3,4,6,8,9]:
  baseline=add(*(scale(2*B[i][j],mul(mul(dims[i],dims[j]),rt[(n*(phase[i]-phase[j]))%N])) for i in range(20) for j in range(20) if B[i][j]))
  edges={tuple(edge) for mat in row['matchings'] for edge in mat};delta={}
  for a,b in edges:
   delta[a,b]=scale(2,mul(mul(dims[a],dims[a]),add(scale(2,rt[0]),scale(-1,rt[(n*(phase[a]-phase[b]))%N]),scale(-1,rt[(n*(phase[b]-phase[a]))%N]))))
  phi=int(s.totient(n));basis=[dict(mul(D2,rt[j*N//n])) for j in range(phi)]
  inds=sorted(set().union(*(set(a) for a in basis)))
  BM=s.Matrix([[a.get(i,0) for a in basis] for i in inds]);piv=BM.T.rref()[1];minor=BM[list(piv),:];iv=minor.inv();results=[]
  for mat in row['matchings']:
   z=dict(add(baseline,*(delta[tuple(edge)] for edge in mat)))
   co=iv*s.Matrix([z.get(inds[i],0) for i in piv]);reconstructed=BM*co
   good=not(set(z)-set(inds)) and reconstructed==s.Matrix([z.get(i,0) for i in inds]) and all(x.q==1 for x in co)
   results.append({'matching':mat,'in_field_integral':bool(good),'coefficients':[str(v) for v in co] if good else None})
  print('H',h[0],'n',n,'good',sum(x['in_field_integral'] for x in results),'coeffs',sorted(set(tuple(x['coefficients']) for x in results if x['in_field_integral'])))
  output.append({'phase':row['phase'],'n':n,'results':results})
(BASE/'matching_higher.json').write_text(json.dumps(output,indent=2)+'\n')
