"""Exact complete character adapter in Q(sqrt(3),sqrt(5),i) for R901.

This additive adapter never changes the FP relative-trace field. Its
integrality test uses the full rational multiplication characteristic
polynomial, not an integral-coordinate shortcut.
"""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
import sympy as s
from sextic_character_table import ps,Characters,discover_roots,check_roots,key,need,rational_vector
HERE=Path(__file__).resolve().parent


class OcticTable(ps.Table):
    def __init__(self,R,a):
        need(a.get('field',{}).get('radicands',[3,5])==[3,5],'octic adapter expects FP radicals3,5')
        self.R=R;self.a=a;self.degree=8
        self.K=K=s.QQ.algebraic_field(s.sqrt(3),s.sqrt(5),s.I,alias='u')
        u=K([1,0]);r3=K.from_sympy(s.sqrt(3));r5=K.from_sympy(s.sqrt(5));eta=K.from_sympy(s.I)
        polynomial=[1,0,-28,0,238,0,372,0,441]
        need(list(map(int,K.mod.to_list()))==polynomial and s.Poly.from_list(polynomial,s.Symbol('t')).is_irreducible,
             'wrong degree-eight field')
        need(r3*r3==K(3)and r5*r5==K(5)and eta*eta==-K.one and u==r3+r5+eta,'incorrect primitive decomposition')
        conjugate_u=r3+r5-eta
        def conjugate(value):
            ans=K.zero
            for c in value.to_list():ans=ans*conjugate_u+K(s.Rational(c.numerator,c.denominator))
            return ans
        self.conjugate=conjugate;self.basis=[u**j for j in range(8)]
        self.coordinates=lambda value:tuple(Fraction(str(c))for c in rational_vector(value,8))
        need(conjugate(r3)==r3 and conjugate(r5)==r5 and conjugate(eta)==-eta,'wrong complex involution')
        need(all(conjugate(conjugate(v))==v for v in self.basis),'conjugation not involutive')
        need(all(conjugate(v*w)==conjugate(v)*conjugate(w)for v in self.basis for w in self.basis),'conjugation not multiplicative')
        realbasis=[K.one,r3,r5,r3*r5];symbolic=[1,s.sqrt(3),s.sqrt(5),s.sqrt(15)]
        self.ds=[sum((K(s.Rational(str(c)))*b for c,b in zip(v,realbasis)),K.zero)for v in a['dimensions']]
        need(all(sum(s.Rational(str(c))*b for c,b in zip(v,symbolic))>0 for v in a['dimensions']),'FP positivity failed')
        self.D=sum((d*d for d in self.ds),K.zero)
        need(self.D==sum((K(s.Rational(str(c)))*b for c,b in zip(a['global_dimension'],realbasis)),K.zero),'global dimension embedding failed')
        need(all(self.ds[i]*self.ds[j]==sum((K(R[i][j][k])*self.ds[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'positive dimension homomorphism failed')
        ch=Characters(R);roots=discover_roots(ch.p,K);need(roots is not None,'incomplete octic character splitting');check_roots(ch.p,K,roots)
        self.characters=[tuple(sum((K(c)*root**j for j,c in enumerate(v)),K.zero)for v in ch.coeff)for root in roots]
        need(len(set(self.characters))==8 and tuple(self.ds)in self.characters,'incomplete character table or missing FP embedding')
        for row in self.characters:
            need(row[0]==K.one and all(row[i]*row[j]==sum((K(R[i][j][k])*row[k]for k in range(8)),K.zero)
                 for i in range(8)for j in range(8)),'character multiplication failed')
            need(all(row[ch.du[i]]==conjugate(row[i])for i in range(8)),'complex character duality failed')
        self.codegrees=[sum((row[i]*row[ch.du[i]]for i in range(8)),K.zero)for row in self.characters]
        for i,row in enumerate(self.characters):
            for j,other in enumerate(self.characters):
                need(sum((row[k]*other[ch.du[k]]for k in range(8)),K.zero)==(self.codegrees[i]if i==j else K.zero),'character orthogonality failed')
        self.beta=[self.D/f for f in self.codegrees];self.cache={};self._allowed={};self._values={};self._integral={}
        self._operators=[s.Matrix.hstack(*(rational_vector(v*w,8)for w in self.basis))for v in self.basis]
        self.metadata={'field':'complex_degree_eight_character_splitting_field','degree':8,'FP_radicands':[3,5],
            'negative_radicand':1,'field_polynomial':polynomial,'primitive_expression':'sqrt(3)+sqrt(5)+i',
            'radical_power_coordinates':[list(map(str,self.coordinates(v)))for v in[r3,r5,eta]],
            'conjugate_generator_power_coordinates':list(map(str,self.coordinates(conjugate_u))),
            'character_generator':ch.k,'character_polynomial':list(map(str,ch.p.all_coeffs())),
            'characters':[[list(map(str,key(v)))for v in row]for row in self.characters],
            'codegrees':[list(map(str,key(v)))for v in self.codegrees],
            'integrality_method':'rational multiplication-operator characteristic polynomial'}

    def integral(self,value):
        vk=tuple(key(value))
        if vk not in self._integral:
            operator=sum((c*M for c,M in zip(rational_vector(value,8),self._operators)),s.zeros(8))
            poly=operator.charpoly().all_coeffs();self._integral[vk]=(all(c.q==1 for c in poly),list(map(str,poly)))
        return self._integral[vk]

    def failure(self,v):
        v=tuple(v)
        if v in self.cache:return self.cache[v]
        K=self.K;dim=sum((K(n)*d for n,d in zip(v,self.ds)),K.zero);need(dim!=K.zero,'zero central dimension')
        for E,(row,beta)in enumerate(zip(self.characters,self.beta)):
            value=beta*sum((K(n)*x for n,x in zip(v,row)),K.zero)/dim;okay,poly=self.integral(value)
            if not okay:
                answer={'character':E,'multiplication_characteristic_polynomial':poly};self.cache[v]=answer;return answer
        self.cache[v]=None;return None


def simple_data(R):
    from exact import vector
    ch=Characters(R);f,K,ds,D,pD,e=ch.fp();need(f.degree()==4,'expected quartic FP field')
    t=s.Symbol('t');radicals=[]
    for q in[3,5]:
        roots=discover_roots(s.Poly(t*t-q,t),K);need(roots is not None,'missing FP radical')
        radicals.append(next(v for v in roots if e.sign(v)>0))
    matrix=s.Matrix.hstack(*(vector(v,4)for v in[K.one,*radicals,radicals[0]*radicals[1]]));inverse=matrix.inv()
    coords=lambda v:[str(c)for c in inverse*vector(v,4)]
    return {'field':{'radicands':[3,5]},'dimensions':[coords(v)for v in ds],'global_dimension':coords(D)}


def run():
    source=ps.st.load_ring('R8_3_901');R=source['tensor'];T=OcticTable(R,simple_data(R));K=T.K
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest();need(digest==source['tensor_sha256'],'source tensor digest')
    need(all(T.integral(v)[0]for row in T.characters for v in row),'algebraic integer character rejected')
    need(T.integral(K([1,0]))[0]and not T.integral(K(s.Rational(1,2)))[0],'integral-closure controls fail')
    samples=[v for row in T.characters for v in row]+T.beta+[K(s.Rational(1,2)),K([1,0])/K(2)]
    for v in samples:
        operator=s.Matrix.hstack(*(rational_vector(v*b,8)for b in T.basis))
        need(list(map(str,operator.charpoly().all_coeffs()))==T.integral(v)[1],'direct multiplication operator mismatch')
    control=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):control[i][j][4*z+(g+k)%4]+=1
    data={'field':{'radicands':[3,5]},'dimensions':[[1,0,0,0]]*4+[[s.Rational(1,2),0,s.Rational(1,2),0]]*4,
          'global_dimension':[10,0,2,0]}
    U=OcticTable(control,data);need(any(U.conjugate(v)!=v for row in U.characters for v in row),'positive control lacks complex characters')
    retained=[]
    for g in range(4):
        for a,b in[(1,0),(0,1),(1,1)]:
            v=[0]*8;v[g]=a;v[g+4]=b;need(U.failure(v)is None,'known complex model restriction rejected');retained.append(v)
    return {'kind':'exact_complex_octic_character_adapter','id':source['id'],'tensor_sha256':digest,
            'table':T.metadata,'complete_characters':8,'integral_character_controls':64,
            'independent_operator_samples':len(samples),'positive_control':{'model':'Fibonacci tensor Vec(C4)',
            'nonreal_characters_present':True,'known_center_restrictions_retained':retained},
            'scope':'complete arithmetic adapter; categorical use retains center theorem assumptions'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=run();path=HERE/'octic_complex_character_table_results.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(path.read_text())==result,'octic character receipt changed')
    print('PASS:901 exact octic full character field with nonreal known-model control',flush=True)
