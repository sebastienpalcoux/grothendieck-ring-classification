"""Exact rank-seven known-model and cited-theorem identifications.

The constructions are independent of the census.  F210 nonexistence is a cited
published theorem; its local Groebner computation is not rerun by this module.
"""
import itertools
from fractions import Fraction as F
from functools import lru_cache
from exact import require
from prepare import key

A6_URL='https://www.people.maths.bris.ac.uk/~matyd/GroupNames/356/A6.html'
TPE_URL='https://arxiv.org/abs/2203.06522v5'

@lru_cache(None)
def a6():
    # Characters of A6, class order 1,2,3A,3B,4,5A,5B; Q(sqrt(5)).
    def q(a,b=0):return F(a),F(b)
    def mul(x,y):return x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
    sizes=[1,45,40,40,90,72,72]
    chars=[[q(v) for v in row] for row in [[1]*7,[5,1,2,-1,-1,0,0],
        [5,1,-1,2,-1,0,0],[8,0,-1,-1,0,0,0],[8,0,-1,-1,0,0,0],
        [9,1,0,0,1,-1,-1],[10,-2,1,1,0,0,0]]]
    chars[3][5]=chars[4][6]=q(F(1,2),F(-1,2))
    chars[3][6]=chars[4][5]=q(F(1,2),F(1,2))
    def scalar(*rows):
        z=q(0)
        for c in range(7):
            v=q(sizes[c])
            for row in rows:v=mul(v,row[c])
            z=(z[0]+v[0],z[1]+v[1])
        require(z[1]==0 and (z[0]/360).denominator==1,'A6 scalar product is nonintegral')
        return int(z[0]/360)
    require(sum(sizes)==360,'A6 class-size sum')
    require(all(scalar(chars[i],chars[j])==int(i==j)
        for i,j in itertools.product(range(7),repeat=2)),'A6 character orthogonality')
    return [[[scalar(chars[i],chars[j],chars[k]) for k in range(7)]for j in range(7)]for i in range(7)]

@lru_cache(None)
def f210():
    # Liu--Palcoux--Ren--Vercleyen, arXiv:2203.06522v5, Section 7.1, p.30.
    data=[
      '1000000 0100000 0010000 0001000 0000100 0000010 0000001',
      '0100000 1101011 0010111 0100111 0011111 0111111 0111111',
      '0010000 0010111 1110011 0001111 0101111 0111111 0111111',
      '0001000 0100111 0001111 1011011 0110111 0111111 0111111',
      '0000100 0011111 0101111 0110111 1111111 0111121 0111112',
      '0000010 0111111 0111111 0111111 0111121 1111212 0111122',
      '0000001 0111111 0111111 0111111 0111112 0111122 1111221']
    return [[list(map(int,row))for row in M.split()]for M in data]

def f210_certificate(R):
    S=f210();dims=[1,5,5,5,6,7,7]
    if len(R)!=7:return None
    for tail in itertools.permutations(range(1,7)):
        p=(0,)+tail # source labels -> input labels
        if not all(R[p[i]][p[j]][p[k]]==S[i][j][k]
                   for i,j,k in itertools.product(range(7),repeat=3)
                   if not (i>=5 and j>=5 and k>=5)):continue
        if not all(dims[i]*dims[j]==sum(R[p[i]][p[j]][p[k]]*dims[k]for k in range(7))
                   for i,j in itertools.product(range(7),repeat=2)):continue
        exact=all(R[p[i]][p[j]][p[k]]==S[i][j][k]
                   for i,j,k in itertools.product(range(7),repeat=3))
        return {'kind':'localized_TPE_F210','theorem':'Liu--Palcoux--Ren--Vercleyen, arXiv:2203.06522v5, Corollary 6.2, Theorem 6.4 and proof of Theorem 7.2',
                'source_url':TPE_URL,'source_to_census':list(p),
                'scope':'all complex fusion categories','exact_source_tensor':exact,
                'dimensions_in_source_order':dims,
                'unconstrained_tensor_cube':[5,6],
                'verification':'Exact equality of every coefficient outside the seven-dimensional-object cube and of the positive dimension character; these determine the identical inconsistent local TPE systems. Published Groebner calculation not rerun.'}
    return None

def verify_f210(R,c):
    require(c==f210_certificate(R) and c is not None,'invalid F210 local-template identification')

def support40_certificate(R):
    n=len(R)
    if n!=7:return None
    du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    invertible=[i for i in range(n)if R[i][du[i]]==[1]+[0]*(n-1)]
    if len(invertible)!=4:return None
    non=[i for i in range(n)if i not in invertible]
    for two in non:
        ds=[1 if i in invertible else 2 if i==two else 4 for i in range(n)]
        if not all(ds[i]*ds[j]==sum(R[i][j][k]*ds[k]for k in range(n))
                   for i,j in itertools.product(range(n),repeat=2)):continue
        require(sum(d*d for d in ds)==40,'wrong solvable dimension')
        S=[i for i in range(n)if ds[i]<=2]
        for i,j,k,l in itertools.product(range(n),repeat=4):
            if not R[i][j][l]:continue
            support=[m for m in range(n)if R[j][k][m] and any(R[i][m][x]for x in S)]
            lhs=F(sum(R[l][k][x]*ds[x]for x in S),ds[l])
            rhs=F(sum(R[j][k][m]*ds[m]for m in support),ds[j])
            if lhs>rhs:
                return {'kind':'solvable_minkowski_support','dimensions':ds,'global_dimension':40,
                    'ijk':[i,j,k],'l':l,'subset':S,'right_support':support,
                    'lhs':str(lhs),'rhs':str(rhs),
                    'reduction':'ENO arXiv:0809.3031 Theorem 1.6: dimension 2^3*5 implies solvable; Galindo--Hong--Rowell arXiv:1105.5048 Theorem 5.20: weakly group-theoretical implies unitarizable',
                    'inequality':'Lim arXiv:2601.13490 Corollary 3.4, positive p-th-root limit as p tends to infinity',
                    'scope':'all complex fusion categories'}
    return None

def verify_support40(R,c):
    require(c==support40_certificate(R) and c is not None,'invalid solvable support obstruction')


def models():
    from analyze import frobenius_prime
    from quantum_rank2 import principal
    from ty_equivariant_models import models as ty_models
    from quaternion_equivariant_model import models as quaternion_models
    from verify_r7_4_2019_chern import models as chern_models
    return [
      ('Rep(A6)',a6(),'Ordinary complex representations of A6; exact character products over Q(sqrt(5)).',
       'A6 character table (GroupNames); GAP Character Table Library A6, originating in ATLAS of Finite Groups.',A6_URL),
      ('Rep(C13rtimesC4)',frobenius_prime(13,4,5),'Ordinary complex representations of C13 semidirect C4, generator acting by exponent 5; exact induced characters.',
       'Character induction for the explicit finite semidirect product C13 semidirect_5 C4; 5 has order four modulo 13.',
       'https://www.ams.org/books/surv/205/'),
      ('Adj(SU(3)_5)',principal('A2',5,True)[0],'The triality-zero fusion subcategory of the standard unitary SU(3) level-five category; exact Weyl alternants over Q(zeta24).',
       'Wenzl, C*-tensor categories from quantum groups, J. Amer. Math. Soc. 11 (1998), 261-282; adjoint SU(3)_5 fusion reconstructed by exact Weyl alternants.',
       'https://doi.org/10.1090/S0894-0347-98-00253-7')]+ty_models()+quaternion_models()+chern_models()

def model_records(rows):
    by_key={key(r['tensor']):r for r in rows};result=[]
    max_m=max((r['multiplicity'] for r in rows),default=0)
    for name,S,construction,reference,url in models():
        if max(x for matrix in S for row in matrix for x in row)>max_m:
            continue
        r=by_key.get(key(S));require(r is not None,'new model missing from census')
        p=next(((0,)+tail for tail in itertools.permutations(range(1,7))
            if all(S[i][j][k]==r['tensor'][((0,)+tail)[i]][((0,)+tail)[j]][((0,)+tail)[k]]
              for i,j,k in itertools.product(range(7),repeat=3))),None)
        require(p is not None,'new model has no full tensor match')
        result.append({'id':r['id'],'rank':7,'multiplicity':r['multiplicity'],'name':name,
            'source_construction':construction,'source_reference':reference,'source_url':url,
            'basis_permutation_model_to_census':list(p),'tensor':r['tensor'],
            'existence':{x:'yes'for x in ('general','pivotal','spherical','pseudo_unitary','unitary')}})
    return result
