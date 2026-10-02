"""Exact hypotheses for a general dimension-140 half-partition obstruction.

Ostrik 1309.4822, Proposition 2.8 and Theorem 2.13; ENO 0809.3031,
Corollary 7.2, Proposition 7.4, Theorems 1.5, 1.6 and 9.2.
See the accompanying manuscript for the categorical argument.
"""
import hashlib,itertools,json
from functools import lru_cache
import sympy as s
from exact import require

def certificate(R):
    n=len(R)
    if n!=7 or any(R[i][j]!=R[j][i] for i,j in itertools.product(range(n),repeat=2)):
        return None
    invertible=[i for i in range(n) if all(sum(row)==1 for row in R[i])]
    if len(invertible)!=4:return None
    others=[i for i in range(n) if i not in invertible]
    d=None
    for last in others:
        v=[1 if i in invertible else 8 if i==last else 6 for i in range(n)]
        if all(sum(R[i][j][k]*v[k] for k in range(n))==v[i]*v[j]
               for i,j in itertools.product(range(n),repeat=2)):
            d=v;break
    if d is None:return None
    D=sum(x*x for x in d);require(D==140,'dimension')
    star=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    N=[s.Matrix(R[i]) for i in range(n)];x=s.Symbol('x')
    Q=sum((N[i]*N[star[i]] for i in range(n)),s.zeros(n));p=Q.charpoly(x).as_expr()
    if s.expand(p-(x-140)*(x-20)**2*(x-7)*(x-4)**3)!=0:return None
    fs=[140,20,20,7,4,4,4];dims=[D//f for f in fs]
    require(all(D%f==0 for f in fs) and sum(dims)==D,'induction dimensions')
    halves=[list(t) for k in range(7) for t in itertools.combinations(range(1,7),k)
            if sum(dims[j] for j in t)==D//2]
    require(halves==[[4,5],[4,6],[5,6]],'half partitions')
    require(all(1 not in t and 2 not in t for t in halves),'odd prime summands centralize every fermion')
    divisors=[g for g in range(2,D+1) if D%g==0]
    require(all(g in(2,4) or len(s.factorint(D//g))<=2 for g in divisors),'Tannakian quotient reduction')
    require(D%6!=0,'Frobenius contradiction')
    return {'kind':'half_partition_tannakian','scope':'all complex fusion categories',
            'dimension_vector':d,'global_dimension':D,'formal_codegrees':fs,
            'formal_codegree_characteristic_polynomial':[int(v) for v in s.Poly(p,x).all_coeffs()],
            'induced_unit_dimensions':dims,'negative_half_subsets':halves,
            'forced_centralizing_prime_dimensions':[7,7],
            'tannakian_group_order_divisors':divisors,
            'small_group_orders_requiring_integral_descent':[2,4],
            'integral_descent_dimension':70,'nondividing_simple_dimension':6,
            'source_references':['Ostrik arXiv:1309.4822, Proposition 2.8 and Theorem 2.13',
              'ENO arXiv:0809.3031, Corollary 7.2, Proposition 7.4, Theorems 1.5, 1.6 and 9.2'],
            'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()}

def verify(R,c):
    require(c is not None and c==certificate(R),'invalid half-partition Tannakian obstruction')

def odd_pointed120_certificate(R):
    from fractions import Fraction as F
    n=len(R)
    if n!=7 or any(R[i][j]!=R[j][i] for i,j in itertools.product(range(n),repeat=2)):
        return None
    invertible=[i for i in range(n) if all(sum(row)==1 for row in R[i])]
    if len(invertible)!=3:return None
    others=[i for i in range(n) if i not in invertible];d=None
    for small in others:
        v=[1 if i in invertible else 3 if i==small else 6 for i in range(n)]
        if all(sum(R[i][j][k]*v[k] for k in range(n))==v[i]*v[j]
               for i,j in itertools.product(range(n),repeat=2)):
            d=v;break
    if d is None:return None
    D=sum(v*v for v in d);require(D==120,'dimension')
    star=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    N=[s.Matrix(R[i]) for i in range(n)];x=s.Symbol('x')
    Q=sum((N[i]*N[star[i]] for i in range(n)),s.zeros(n));p=Q.charpoly(x).as_expr()
    if s.expand(p-(x-120)*(x-60)**2*(x-24)*(x-4)*(x-3)**2)!=0:return None
    fs=[120,60,60,24,4,3,3];dims=[D//f for f in fs]
    witness=None
    for i,j,k,l,z in itertools.product(range(n),repeat=5):
        if not R[i][j][l]:continue
        T=[m for m in range(n) if R[j][k][m] and R[i][m][z]]
        lhs=F(R[l][k][z]*d[z],d[l]);rhs=sum((F(R[j][k][m]*d[m],d[j]) for m in T),F(0))
        if lhs>rhs:
            witness={'ijk':[i,j,k],'l':l,'subset':[z],'right_support':T,'lhs':str(lhs),'rhs':str(rhs)};break
    if witness is None:return None
    return {'kind':'odd_pointed_tannakian_120','scope':'all complex fusion categories',
            'dimension_vector':d,'global_dimension':D,'invertible_labels':invertible,
            'formal_codegrees':fs,'formal_codegree_characteristic_polynomial':[int(v) for v in s.Poly(p,x).all_coeffs()],
            'induced_unit_dimensions':dims,'prime_power_central_dimension':2,
            'unitary_support_witness':witness,
            'source_references':['Ostrik arXiv:1309.4822, Theorem 2.13',
              'ENO arXiv:0809.3031, Corollary 7.2',
              'Li Dai, Frobenius property for fusion categories of dimension 120 (2025), Lemmas 2.5 and 3.1, doi:10.33044/revuma.4390',
              'Galindo-Hong-Rowell arXiv:1105.5048, Theorem 5.20',
              'Lim arXiv:2601.13490, Corollary 3.4, positive p-th-root limit'],
            'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()}

def verify_odd120(R,c):
    require(c is not None and c==odd_pointed120_certificate(R),'invalid odd-pointed dimension-120 obstruction')
