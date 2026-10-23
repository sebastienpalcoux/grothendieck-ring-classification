from arithmetic import *
from functools import lru_cache
import field_automorphisms as fa

@lru_cache(None)
def automorphism_obstruction(co):
 f=fa.parse(co);x=fa.x
 if not 3<=f.degree()<=6:return None
 K=s.QQ.alg_field_from_poly(f);fac=s.Poly(f,x,domain=K).factor_list()[1];roots=[]
 for p,e in fac:
  if p.degree()==1:
   a=-p.rep.to_list()[-1]/p.rep.to_list()[0];roots.append(s.Poly.from_list([s.Rational(v.numerator,v.denominator) for v in a.to_list()],x,domain=s.QQ))
 for a,b in itertools.combinations(roots,2):
  v=fa.compose(a,b,f)-fa.compose(b,a,f)
  if v:return dict(kind='noncommuting_field_automorphisms',factor=list(co),automorphisms=[fa.coeff(a),fa.coeff(b)],commutator_difference=fa.coeff(v))
 return None

def main():
 surv={r['id'] for r in json.load(open(HERE/'survivors.json'))};out=[]
 for r in read():
  if r['id'] not in surv or not comm(r['tensor']):continue
  R=r['tensor'];cs=[];p=casimir(R).charpoly(t).as_poly()
  for q,e in p.factor_list()[1]:
   d=q.degree();norm=abs(int(q.TC()))
   if all(v<d for v in s.factorint(norm).values()) and (d!=len(R) or e!=1 or p!=q):
    cs.append(dict(kind='primitive_codegree',factor=list(map(int,q.all_coeffs())),degree=d,norm=norm,reference='Schopieray 2021 Theorem 4.4 and Corollary 4.3'))
  for i,A in enumerate(R):
   for f,m in s.Matrix(A).charpoly(fa.x).as_poly().factor_list()[1]:
    c=automorphism_obstruction(tuple(fa.coeff(f)))
    if c:
     c=dict(c,object=i);fa.verify(R,c);cs.append(c);break
   if any(c['kind']=='noncommuting_field_automorphisms' for c in cs):break
  out.append(dict(id=r['id'],rank=r['rank'],tensor_sha256=r['tensor_sha256'],certificates=cs))
  if cs:print(r['id'],cs,flush=True)
  if len(out)%10==0:(HERE/'extra_arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'extra_arithmetic.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TOTAL',len(out),'EXCLUSIONS',sum(bool(x['certificates']) for x in out),'CACHED_POLYS',automorphism_obstruction.cache_info())
if __name__=='__main__':main()
