"""Exact character-trace compression calculation; research only."""
from pathlib import Path
import sys,json,math,collections
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'repo/supplements/rank6'
sys.path.insert(0,str(P/'software'))
sys.path.insert(0,str(P/'research/round5/m8_modrep'))
from finite_spectra48 import coefficient_field,mul
from exact import require
C=coefficient_field();x=s.Symbol('x')
def enc(a):return list(map(str,a.to_list()))
def linear_sum(row,counts,denom):
 return sum((C([s.Rational(z) for z in row[k]])*C(v) for k,v in counts.items()),C.zero)/C(denom)
def local(m):
 data=json.loads((P/f'research/round5/m8_modrep/sl2_{m}.json').read_text())
 group=data['group'];ix={tuple(g):i for i,cl in enumerate(group['classes']) for g in cl}
 S=(0,m-1,1,0);ts=[(1,j,0,1) for j in range(m)]
 c1=collections.Counter(ix[mul(t,S,m)] for t in ts)
 c2=collections.Counter(ix[mul(mul(mul(t,S,m),u,m),S,m)] for t in ts for u in ts)
 out=[]
 for i,r in enumerate(data['irreps']):
  n=r['T_multiplicities'][0]
  if not n:continue
  a=linear_sum(r['characters'],c1,m);b=linear_sum(r['characters'],c2,m*m)
  require(n in (1,2),'unexpected compression rank')
  if n==1:require(b==a*a,'rank-one trace mismatch')
  out.append(dict(index=i,rank=n,sign=r['central_sign'],trace=a,trace_square=b,det=(a*a-b)/C(2) if n==2 else a))
 return out
def poly(coeff):return s.Poly.from_list(coeff,x,domain=C)
L16=local(16);L3=local(3);combined=[]
for a in L16:
 for b in L3:
  require(b['rank']==1,'SL2(3) fixed rank')
  if a['sign']*b['sign']!=1:continue
  coeff=[C.one,-a['trace']*b['trace']]
  if a['rank']==2:coeff.append(a['det']*b['trace']**2)
  combined.append(dict(indices=[a['index'],b['index']],rank=a['rank'],poly=poly(coeff)))
print('Local fixed ranks',[(m,collections.Counter(r['rank'] for r in z)) for m,z in [(16,L16),(3,L3)]],flush=True)
print('Plus compression types',len(combined),len(set(tuple(r['poly'].rep.to_list()) for r in combined)),flush=True)
# Six low objects are exactly the twist-one sector by the new theorem.
import round3_m4 as M
R=next(r['N'] for r in json.loads((P/'data/census.json').read_text()) if r['id']=='R6_8_1660')
d=M.data_for(R,6,48);D=d['DD'];tab=d['tab'];n=6
def characteristic(B):
 I=[[C(int(i==j)) for j in range(n)] for i in range(n)]
 Q=I;co=[C.one]
 for k in range(1,n+1):
  Q=[[sum((B[i][a]*Q[a][j] for a in range(n)),C.zero) for j in range(n)] for i in range(n)]
  ck=-sum((Q[i][i] for i in range(n)),C.zero)/C(k);co.append(ck)
  for i in range(n):Q[i][i]+=ck
 return poly(co)
cert=json.loads((P/'research/round5/m8_actual48/certificate.json').read_text());results=[]
for br in cert['branches']:
 if br['outcome']!='profile_frontier':continue
 lo=d['lows'][br['low']];lab=br['labelling']
 dims=[sum((C(v[i])*d['dims'][i] for i in range(n)),C.zero) for v in lo]
 B=[[dims[a]*sum((C(lo[b][i])*tab.rows[lab[a]][i] for i in range(n)),C.zero)/D for b in range(n)] for a in range(n)]
 require(all(B[a][b]==B[b][a] for a in range(n) for b in range(n)),'low S block not symmetric')
 f=characteristic(B);eligible=[]
 for r in combined:
  q,rem=f.div(r['poly'])
  if rem.is_zero:eligible.append(r)
 types={}
 for r in eligible:types.setdefault(tuple(r['poly'].rep.to_list()),[]).append(r['indices'])
 divisors=[(poly(list(co)),inds) for co,inds in types.items()]
 decompositions=[]
 def walk(rem,start,parts):
  if rem.degree()==0:
   decompositions.append(parts);return
  for j in range(start,len(divisors)):
   q,rr=rem.div(divisors[j][0])
   if rr.is_zero:walk(q,j,parts+[j])
 walk(f,0,[])
 rec=dict(low=br['low'],labelling=lab,low_charpoly=[enc(z) for z in f.rep.to_list()],eligible_irrep_pairs=[r['indices'] for r in eligible],eligible_spectrum_types=[dict(polynomial=[enc(z) for z in q.rep.to_list()],pairs=inds) for q,inds in divisors],decompositions=decompositions)
 results.append(rec)
 print(json.dumps(dict(low=br['low'],labelling=lab,eligible_pairs=len(eligible),eligible_types=len(types),decompositions=len(decompositions))),flush=True)
out=dict(scope='exact necessary compression spectra; no categorification claimed',local={str(m):[{k:(enc(v) if k in ('trace','trace_square','det') else v) for k,v in r.items()} for r in rows] for m,rows in [(16,L16),(3,L3)]},branches=results)
(Path(__file__).parent/'compressed_spectra.json').write_text(json.dumps(out,indent=2)+'\n')
