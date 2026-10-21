"""Exact real degree-six character fields for residuals 3413 and 3472.

Adapter API matches partial_s.RealTable; its integral-closure test uses
the rational multiplication-operator characteristic polynomial. No
cyclotomic power-basis integrality shortcut is used in these subfields.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
from fractions import Fraction
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import partial_s as ps
from exact import discover_roots,check_roots,key,embeddings
from rings import Characters
from rank_two_and_models import need


def rational_vector(value,d=6):
    co=[s.Rational(c.numerator,c.denominator)for c in value.to_list()]
    return s.Matrix(list(reversed([s.Rational(0)]*(d-len(co))+co)))


class SexticTable(ps.Table):
    """Full real splitting over Q(sqrt(5),zeta9+) or Q(sqrt(2),zeta7+)."""
    def __init__(self,R,a):
        q=a['q'];need(q in (2,5),'degree-six adapter supports q=2 or q=5')
        self.R=R;self.a=a;self.degree=6
        x=s.Symbol('x');cubic=x**3-3*x+1 if q==5 else x**3+x*x-2*x-1
        defining=s.Poly(s.expand(cubic.subs(x,x-s.sqrt(q))*cubic.subs(x,x+s.sqrt(q))),x)
        need(defining.degree()==6 and defining.is_irreducible and defining.count_roots()==6,
             'expected totally real degree-six field')
        self.K=K=s.QQ.alg_field_from_poly(defining,alias='u');u=K([1,0])
        embedding=max(embeddings(defining),key=lambda e:e.hi)
        roots_q=discover_roots(s.Poly(x*x-q,x),K);need(roots_q is not None,'quadratic subfield missing')
        check_roots(s.Poly(x*x-q,x),K,roots_q)
        radical=next(r for r in roots_q if embedding.sign(r)>0)
        theta=u-radical
        need(sum((K(c)*theta**j for j,c in enumerate(reversed(cubic.all_coeffs() if isinstance(cubic,s.Poly) else s.Poly(cubic,x).all_coeffs()))),K.zero)==K.zero,
             'primitive generator does not equal radical plus chosen cubic root')
        self.basis=[u**j for j in range(6)]
        self.coordinates=lambda value:tuple(Fraction(str(c))for c in rational_vector(value))
        self.conjugate=lambda value:value
        self.ds=[K(s.Rational(str(v[0])))+K(s.Rational(str(v[1])))*radical for v in a['dimensions']]
        self.D=sum((d*d for d in self.ds),K.zero)
        need(all(embedding.sign(d)>0 for d in self.ds),'FP dimensions not positive')
        need(all(self.ds[i]*self.ds[j]==sum((K(R[i][j][k])*self.ds[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'positive FP homomorphism fails')
        need(self.D==K(s.Rational(str(a['global_dimension'][0])))+
             K(s.Rational(str(a['global_dimension'][1])))*radical,'global dimension embedding fails')
        ch=Characters(R);roots=discover_roots(ch.p,K)
        need(roots is not None,'source character polynomial does not split in degree-six field')
        check_roots(ch.p,K,roots)
        self.characters=[tuple(sum((K(c)*root**j for j,c in enumerate(v)),K.zero)for v in ch.coeff)for root in roots]
        need(len(set(self.characters))==8 and tuple(self.ds)in self.characters,'incomplete character table')
        for row in self.characters:
            need(row[0]==K.one and all(row[i]*row[j]==sum((K(R[i][j][k])*row[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'character multiplication failed')
            need(all(row[ch.du[i]]==row[i]for i in range(8)),'real character duality failed')
        self.codegrees=[sum((row[i]*row[ch.du[i]]for i in range(8)),K.zero)for row in self.characters]
        need(all(f!=K.zero for f in self.codegrees),'zero formal codegree')
        for i,row in enumerate(self.characters):
            for j,other in enumerate(self.characters):
                need(sum((row[k]*other[ch.du[k]]for k in range(8)),K.zero)==(self.codegrees[i]if i==j else K.zero),
                     'character orthogonality failed')
        self.beta=[self.D/f for f in self.codegrees]
        self.cache={};self._values={};self._allowed={};self._integral={}
        self._operators=[s.Matrix.hstack(*(rational_vector(b*c)for c in self.basis))for b in self.basis]
        self.metadata={'field':'real_degree_six_character_splitting_field','degree':6,'FP_radicand':q,
            'cubic_polynomial':list(map(int,s.Poly(cubic,x).all_coeffs())),
            'field_polynomial':list(map(int,defining.all_coeffs())),
            'radical_power_coordinates':list(map(str,self.coordinates(radical))),
            'cubic_root_power_coordinates':list(map(str,self.coordinates(theta))),
            'character_generator':ch.k,
            'characters':[[list(map(str,key(v)))for v in row]for row in self.characters],
            'codegrees':[list(map(str,key(v)))for v in self.codegrees],
            'integrality_method':'characteristic polynomial of rational multiplication operator'}

    def integral(self,value):
        vk=tuple(key(value))
        if vk not in self._integral:
            co=rational_vector(value)
            operator=sum((c*M for c,M in zip(co,self._operators)),s.zeros(6))
            poly=operator.charpoly().all_coeffs()
            self._integral[vk]=(all(c.q==1 for c in poly),list(map(str,poly)))
        return self._integral[vk]

    def failure(self,v):
        v=tuple(v)
        if v in self.cache:return self.cache[v]
        K=self.K;dim=sum((K(n)*d for n,d in zip(v,self.ds)),K.zero)
        need(dim!=K.zero,'zero proposed central dimension')
        for E,(row,beta)in enumerate(zip(self.characters,self.beta)):
            value=beta*sum((K(n)*ch for n,ch in zip(v,row)),K.zero)/dim
            okay,poly=self.integral(value)
            if not okay:
                result={'character':E,'multiplication_characteristic_polynomial':poly}
                self.cache[v]=result;return result
        self.cache[v]=None;return None


def simple_data(index):
    """Only exact FP input is needed to construct the table, not cone enumeration."""
    q=5 if index==3413 else 2
    dims=([1,(5+3*s.sqrt(5))/2,(5+3*s.sqrt(5))/2,(7+3*s.sqrt(5))/2,
           (5+3*s.sqrt(5))/2,(5+3*s.sqrt(5))/2,(9+3*s.sqrt(5))/2,(9+3*s.sqrt(5))/2]
          if index==3413 else[1,6+5*s.sqrt(2),6+5*s.sqrt(2),7+5*s.sqrt(2),
                                  6+5*s.sqrt(2),8+5*s.sqrt(2),8+5*s.sqrt(2),8+5*s.sqrt(2)])
    def co(expr):
        expr=s.expand(expr);b=expr.coeff(s.sqrt(q));a=s.simplify(expr-b*s.sqrt(q));return [a,b]
    return {'q':q,'dimensions':[co(d)for d in dims],'global_dimension':co(sum(d*d for d in dims))}


def run():
    records=[]
    for index in [3413,3472]:
        row=ps.st.load_ring(f'R8_3_{index}');R=row['tensor'];T=SexticTable(R,simple_data(index))
        sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
        need(sha==row['tensor_sha256'],'source tensor digest mismatch')
        # Every character value is an algebraic integer as an eigenvalue
        # of an integer fusion matrix. This supplies 64 exact controls.
        need(all(T.integral(value)[0]for rowch in T.characters for value in rowch),'integral source character rejected')
        K=T.K;u=K([1,0]);need(T.integral(u)[0]and not T.integral(K(s.Rational(1,2)))[0],
             'integral-closure controls failed')
        # Cross-check by direct field multiplication, rather than the cached
        # linear combination of precomputed multiplication operators.
        samples=[v for rowch in T.characters for v in rowch]+T.beta+[K(s.Rational(1,2)),u/K(2)]
        for v in samples:
            op=s.Matrix.hstack(*(rational_vector(v*b)for b in T.basis))
            poly=list(map(str,op.charpoly().all_coeffs()))
            need(T.integral(v)[1]==poly,'independent direct multiplication operator disagrees')
        records.append({'id':row['id'],'tensor_sha256':sha,'table':T.metadata,
                        'complete_characters':8,'source_character_integrality_controls':64,
                        'independent_direct_operator_samples':len(samples)})
    # Known positive model embedded in the q=5 degree-six field.
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):R[i][j][4*z+(g^k)]+=1
    a={'q':5,'dimensions':[[1,0]]*4+[[s.Rational(1,2),s.Rational(1,2)]]*4,'global_dimension':[10,2]}
    T=SexticTable(R,a);known=[]
    for g in range(4):
        for u,v in[(1,0),(0,1),(1,1)]:
            column=[0]*8;column[g]=u;column[g+4]=v
            need(T.failure(column)is None,'known center column rejected in sextic overfield');known.append(column)
    return {'kind':'exact_degree_six_character_adapters','records':records,
            'positive_control':{'model':'Fibonacci tensor Vec(C2 times C2)',
                                'known_center_restriction_columns_retained':known},
            'scope':'full arithmetic adapter; using partial-S as a categorical obstruction retains the center theorem hypotheses'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'sextic_character_table_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'sextic character adapter receipt changed')
    print('PASS: exact degree-six complete character adapters for3413/3472 and known positive control')
