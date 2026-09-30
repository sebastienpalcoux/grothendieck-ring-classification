"""Exact dimension-block Fourier bounds (Schopieray, arXiv:2609.35287)."""
import itertools,json,math,sys,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'software'))
from exact import require,evaluate,vector,field,embeddings
from round3_m4 import data_for

IDS=['R6_4_22','R6_4_91','R6_4_155','R6_4_629','R6_5_1204','R6_8_1660']
def check(R):
 d=data_for(R,1); C=d['C']; F=d['F']; D=d['DD']; units=[a for a in range(F) if math.gcd(a,F)==1]
 auto=lambda x,a:evaluate(x.to_list(),C.unit**a,C)
 values=list(dict.fromkeys(auto(D,a) for a in units)); reps=[next(a for a in units if auto(D,a)==x) for x in values]
 ix={a:values.index(auto(D,a)) for a in units}; n=len(values); identity=ix[1]
 mult=[[ix[a*b%F] for b in reps] for a in reps]
 g1=len({tuple(auto(x,a) for x in d['dims']) for a in units})
 require(g1%n==0,'invalid dimension field extension'); e=g1//n
 orders=[]
 for j in range(n):
  a=j;k=1
  while a!=identity:a=mult[a][j];k+=1
  orders.append(k)
 L=math.lcm(*orders); EF=math.lcm(F,L)
 if EF!=F:
  EC=field(s.Poly(s.cyclotomic_poly(EF,s.Symbol('t')),s.Symbol('t')))
  values=[evaluate(v.to_list(),EC.unit**(EF//F),EC) for v in values]; C=EC
 characters=[]
 for phases in itertools.product(range(L),repeat=n):
  if phases[identity] or any((phases[i]+phases[j]-phases[mult[i][j]])%L for i in range(n) for j in range(n)):continue
  conductor=next(int(f) for f in s.divisors(F) if all(a%f!=b%f or phases[ix[a]]==phases[ix[b]] for a in units for b in units))
  total=sum((C.unit**(EF//L*k)/v for k,v in zip(phases,values)),C.zero)
  square=total*evaluate(total.to_list(),C.unit**(EF-1),C); margin=C(1)/C(e*e*conductor)-square
  # Exact sign in the chosen real embedding, also handling nonrational norms.
  U_poly=s.Poly(s.minpoly(2*s.cos(2*s.pi/EF),s.Symbol('t')),s.Symbol('t'))
  U=field(U_poly); u=C.unit+C.unit**(EF-1)
  matrix=s.Matrix.hstack(*(vector(u**k,C.mod.degree()) for k in range(U_poly.degree())))
  coeff,free=matrix.gauss_jordan_solve(vector(margin,C.mod.degree()))
  require(not free.rows,'nonunique real-field coordinates')
  mU=sum((U(x)*U.unit**k for k,x in enumerate(coeff)),U.zero)
  sign=embeddings(U_poly)[-1].sign(mU)
  characters.append(dict(phases=list(phases),root_order=L,conductor=conductor,
    squared_fourier=list(map(str,square.to_list())),bound=str(s.Rational(1,e*e*conductor)),margin_sign=sign,passed=sign>=0))
 require(len(characters)==n,'incomplete character enumeration')
 return dict(ambient_conductor=F,calculation_conductor=EF,dimension_field_degree=g1,global_dimension_field_degree=n,e=e,
   global_dimension=list(map(str,D.to_list())),characters=characters,passed=all(c['passed'] for c in characters))

if __name__=='__main__':
 census={x['id']:x['N'] for x in json.load(open(P/'data/census.json'))}
 out={'source':'https://arxiv.org/html/2609.35287v1','theorem':'5.1','scope':'pseudo_unitary_dimension_functions','python_optimized':not __debug__,'cases':{}}
 for rid in IDS:
  out['cases'][rid]=check(census[rid]);print(rid,out['cases'][rid]['passed'],flush=True)
 out['passed']=all(c['passed'] for c in out['cases'].values())
 out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
