"""Exact degree-four complex character adapters for residuals65 and1055.

The field is Q(sqrt(5),i) or Q(sqrt(37),sqrt(-3)). Complex conjugation
is an explicitly checked field involution. Integral closure is tested by
the rational multiplication-operator characteristic polynomial.
"""
from pathlib import Path
import argparse
import hashlib
import json
from fractions import Fraction
import sympy as s
from sextic_character_table import ps,Characters,discover_roots,check_roots,key,need,rational_vector

HERE=Path(__file__).resolve().parent


class QuarticComplexTable(ps.Table):
    def __init__(self,R,a):
        q=a['q'];need(q in (5,37),'complex adapter requires q5 or37')
        r=1 if q==5 else 3;x=s.Symbol('x')
        defining=s.Poly(x**4+2*(r-q)*x*x+(q+r)**2,x)
        need(defining.is_irreducible and defining.count_roots()==0,'wrong nonreal quartic field')
        self.R=R;self.a=a;self.degree=4;self.K=K=s.QQ.alg_field_from_poly(defining,alias='u');u=K([1,0])
        radical=(u*u+K(q+r))/(K(2)*u);eta=u-radical
        need(radical*radical==K(q) and eta*eta==-K(r),'quartic radical decomposition failed')
        conjugate_u=radical-eta
        def conjugate(value):
            ans=K.zero
            for c in value.to_list():ans=ans*conjugate_u+K(s.Rational(c.numerator,c.denominator))
            return ans
        self.conjugate=conjugate;self.basis=[u**i for i in range(4)]
        self.coordinates=lambda value:tuple(Fraction(str(c))for c in rational_vector(value,4))
        need(conjugate(radical)==radical and conjugate(eta)==-eta,'incorrect complex conjugation')
        need(all(conjugate(conjugate(b))==b for b in self.basis),'conjugation not involutive')
        need(all(conjugate(b*c)==conjugate(b)*conjugate(c)for b in self.basis for c in self.basis),
             'conjugation not a field homomorphism')
        self.ds=[K(s.Rational(str(v[0])))+K(s.Rational(str(v[1])))*radical for v in a['dimensions']]
        self.D=sum((d*d for d in self.ds),K.zero)
        # The embedding radical -> positive sqrt(q), eta -> i sqrt(r)
        # exists by the checked decomposition. Verify positivity there.
        need(all(s.Rational(str(v[0]))+s.Rational(str(v[1]))*s.sqrt(q)>0 for v in a['dimensions']),
             'nonpositive proposed FP dimensions')
        need(all(self.ds[i]*self.ds[j]==sum((K(R[i][j][k])*self.ds[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'positive dimension homomorphism failed')
        need(self.D==K(s.Rational(str(a['global_dimension'][0])))+
             K(s.Rational(str(a['global_dimension'][1])))*radical,'global dimension embedding failed')
        ch=Characters(R);roots=discover_roots(ch.p,K);need(roots is not None,'incomplete quartic splitting')
        check_roots(ch.p,K,roots)
        self.characters=[tuple(sum((K(c)*root**j for j,c in enumerate(v)),K.zero)for v in ch.coeff)for root in roots]
        need(len(set(self.characters))==8 and tuple(self.ds)in self.characters,'incomplete character table')
        for row in self.characters:
            need(row[0]==K.one and all(row[i]*row[j]==sum((K(R[i][j][k])*row[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'character multiplication failed')
            need(all(row[ch.du[i]]==conjugate(row[i])for i in range(8)),'complex character duality failed')
        self.codegrees=[sum((row[i]*row[ch.du[i]]for i in range(8)),K.zero)for row in self.characters]
        for i,row in enumerate(self.characters):
            for j,other in enumerate(self.characters):
                need(sum((row[k]*other[ch.du[k]]for k in range(8)),K.zero)==(self.codegrees[i]if i==j else K.zero),
                     'character orthogonality failed')
        self.beta=[self.D/f for f in self.codegrees];self.cache={};self._values={};self._allowed={};self._integral={}
        self._operators=[s.Matrix.hstack(*(rational_vector(b*c,4)for c in self.basis))for b in self.basis]
        self.metadata={'field':'complex_degree_four_character_splitting_field','degree':4,
            'FP_radicand':q,'negative_radicand':r,'field_polynomial':list(map(int,defining.all_coeffs())),
            'real_radical_power_coordinates':list(map(str,self.coordinates(radical))),
            'imaginary_radical_power_coordinates':list(map(str,self.coordinates(eta))),
            'conjugate_generator_power_coordinates':list(map(str,self.coordinates(conjugate_u))),
            'character_generator':ch.k,
            'characters':[[list(map(str,key(v)))for v in row]for row in self.characters],
            'codegrees':[list(map(str,key(v)))for v in self.codegrees],
            'integrality_method':'rational multiplication-operator characteristic polynomial'}

    def integral(self,value):
        vk=tuple(key(value))
        if vk not in self._integral:
            op=sum((c*M for c,M in zip(rational_vector(value,4),self._operators)),s.zeros(4))
            poly=op.charpoly().all_coeffs();self._integral[vk]=(all(c.q==1 for c in poly),list(map(str,poly)))
        return self._integral[vk]

    def failure(self,v):
        v=tuple(v)
        if v in self.cache:return self.cache[v]
        K=self.K;dim=sum((K(n)*d for n,d in zip(v,self.ds)),K.zero);need(dim!=K.zero,'zero proposed central dimension')
        for E,(row,beta)in enumerate(zip(self.characters,self.beta)):
            value=beta*sum((K(n)*ch for n,ch in zip(v,row)),K.zero)/dim;okay,poly=self.integral(value)
            if not okay:
                result={'character':E,'multiplication_characteristic_polynomial':poly};self.cache[v]=result;return result
        self.cache[v]=None;return None


def simple_data(index):
    q=5 if index==65 else 37
    dims=([[1,0]]*3+[[s.Rational(11,2),s.Rational(5,2)]]*4+[[1,0]] if index==65 else
          [[1,0],[5,1],[5,1],[1,0],[6,1],[6,1],[7,1],[7,1]])
    D=[sum(a*a+q*b*b for a,b in dims),sum(2*a*b for a,b in dims)]
    return {'q':q,'dimensions':dims,'global_dimension':D}


def run():
    records=[]
    for index in[65,1055]:
        row=ps.st.load_ring(f'R8_3_{index}');R=row['tensor'];T=QuarticComplexTable(R,simple_data(index));K=T.K
        sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest();need(sha==row['tensor_sha256'],'source hash')
        need(all(T.integral(v)[0]for r in T.characters for v in r),'integral source character rejected')
        need(T.integral(K([1,0]))[0]and not T.integral(K(s.Rational(1,2)))[0],'integral closure controls failed')
        samples=[v for r in T.characters for v in r]+T.beta+[K(s.Rational(1,2)),K([1,0])/K(2)]
        for v in samples:
            op=s.Matrix.hstack(*(rational_vector(v*b,4)for b in T.basis))
            need(list(map(str,op.charpoly().all_coeffs()))==T.integral(v)[1],'direct multiplication operator mismatch')
        records.append({'id':row['id'],'tensor_sha256':sha,'table':T.metadata,'complete_characters':8,
            'source_character_integrality_controls':64,'independent_direct_operator_samples':len(samples)})
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):R[i][j][4*z+(g^k)]+=1
    a={'q':5,'dimensions':[[1,0]]*4+[[s.Rational(1,2),s.Rational(1,2)]]*4,'global_dimension':[10,2]}
    T=QuarticComplexTable(R,a);known=[]
    for g in range(4):
        for u,v in[(1,0),(0,1),(1,1)]:
            c=[0]*8;c[g]=u;c[g+4]=v;need(T.failure(c)is None,'known center restriction rejected');known.append(c)
    return {'kind':'exact_complex_quartic_character_adapters','records':records,
            'positive_control':{'model':'Fibonacci tensor Vec(C2 times C2)','known_center_restriction_columns_retained':known},
            'scope':'complete arithmetic character adapter; categorical uses retain partial-S theorem assumptions'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'quartic_complex_character_table_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'complex quartic adapter receipt changed')
    print('PASS: exact complex quartic complete character adapters for65/1055 and known positive control')
