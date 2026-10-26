"""Exact one-dimensional characters through the commutator annihilator."""
from signed_mod4 import *
import sympy as s
sys.path.insert(0,str(BASE/'sources/work/rank11/arithmetic/legacy'))
import exact
t=exact.t

def characters(R):
 n=len(R);N=list(map(s.Matrix,R));C=s.Matrix.vstack(*(N[i]*N[j]-N[j]*N[i]for i in range(n)for j in range(i)))
 V=s.Matrix.hstack(*C.nullspace());r=V.cols
 L=(V.T*V).inv()*V.T;B=[L*A*V for A in N]
 common.require(all(A*V==V*M for A,M in zip(N,B)),'commutator-annihilator invariant')
 common.require(all(A*M==M*A for A in B for M in B),'commutative restricted algebra')
 for k in range(1,20):
  H=sum((k**i*A for i,A in enumerate(B)),s.zeros(r));p=H.charpoly(t).as_poly()
  if s.gcd(p,p.diff()).degree()==0:break
 else:raise ValueError('separating element budget')
 v=L[:,0];W=s.Matrix.hstack(*(H**j*v for j in range(r)))
 common.require(W.det()!=0,'cyclic unit projection');Wi=W.inv();co=[Wi*A*v for A in B]
 common.require(all(A==sum((c[j]*H**j for j in range(r)),s.zeros(r))for A,c in zip(B,co)),'all exact character coordinates')
 out=[]
 for f,m in p.factor_list()[1]:
  common.require(m==1,'separating multiplicity');K=exact.field(f)
  ds=[K(s.Poly.from_list(list(reversed(list(c))),t).rem(f).all_coeffs())for c in co]
  zero=[i for i,d in enumerate(ds)if not d];du=common.dual(R);baddu=[i for i in range(n)if ds[i]!=ds[du[i]]]
  common.require(all(sum((K(R[i][j][k])*ds[k]for k in range(n)),K.zero)==ds[i]*ds[j]for i,j in itertools.product(range(n),repeat=2)),'all character products')
  D=sum((ds[i]*ds[du[i]]for i in range(n)),K.zero)
  out.append(dict(field_polynomial=exact.pc(f),dimensions=[exact.ec(d)for d in ds],zero_objects=zero,unequal_duals=baddu,global_dimension=exact.ec(D)))
 return dict(one_dimensional_count=r,separating_k=k,characters=out)

if __name__=='__main__':
 data=json.loads((BASE/'tensors.json').read_text());out=[]
 for i in (63,64,215,365,332,350,561,623,628):
  start=time.monotonic();q=characters(data[f'R12_1_{i}']);q.update(id=f'R12_1_{i}',seconds=time.monotonic()-start);out.append(q)
  print(q['id'],'chars',q['one_dimensional_count'],'surviving',[(r['field_polynomial'],r['global_dimension'])for r in q['characters']if not r['zero_objects']and not r['unequal_duals']],'seconds',q['seconds'],flush=True)
 (Path(__file__).resolve().parent/'characters.json').write_text(json.dumps(out,indent=2)+'\n')
