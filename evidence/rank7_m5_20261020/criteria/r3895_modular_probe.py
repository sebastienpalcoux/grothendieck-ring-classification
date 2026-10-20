"""Exact modular-data necessary test for R3895, never a general exclusion."""
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
import sympy as s
import q5_modular_low as m
q=m.q
HERE=Path(__file__).resolve().parent


def run(write_receipt=True):
    start=time.monotonic();rid='R7_5_3895'
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    q.require(q.tensor_hash(N)=='590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0','pinned R3895 source tensor')
    from rings import validate
    validate(N)
    q.require(all(N[i][j][0]==int(i==j) for i in range(7) for j in range(7)), 'all source simples are self-dual')
    d,D,B,zs,T,signs=q.source_data(N,rid)
    table=m.ExactQuadraticCharacterTable(N,d,5);K=table.K
    dims=[K.from_sympy(s.Rational(a)+s.Rational(b)*s.sqrt(5)) for a,b in d]
    sqrtD=K.from_sympy(20+8*s.sqrt(5))
    q.require(sqrtD**2==table.D,'exact source square root dimension')
    domains=[[h for h,f in enumerate(table.codegrees) if f==table.D/dim**2] for dim in dims]
    assignments=[p for p in itertools.product(*domains) if len(set(p))==7]
    q.require(len(assignments)==4,'complete dimension-compatible character assignments')
    x=s.Symbol('x');polynomial=s.Poly(s.cyclotomic_poly(40,x),x,domain=s.QQ)
    q.require(polynomial.degree()==16,'cyclotomic degree forty')
    def reduce(expr):return s.Poly(expr,x,domain=s.QQ).rem(polynomial)
    root5=reduce(1+2*(x**8+x**32))
    q.require(reduce(root5.as_expr()**2).as_expr()==5,'cyclotomic embedding of sqrt-five')
    def pair(value):
        result=m.quadratic_coeff(value,K)
        q.require(result is not None,'source modular data lie in the real quadratic field')
        return result
    def conjugate(value):
        a,b=pair(value);return K.from_sympy(s.Rational(a)-s.Rational(b)*s.sqrt(5))
    def cyclotomic_expression(value):
        a,b=pair(value);return s.Rational(a)+s.Rational(b)*root5.as_expr()
    dimension_expressions=[cyclotomic_expression(z) for z in dims]
    inverse_dimension=cyclotomic_expression(K.one/table.D)
    def second_indicators(exponents,tensor=N,dimensions=dimension_expressions,dimension_inverse=inverse_dimension):
        result=[]
        n=len(tensor)
        for k in range(n):
            numerator=sum(tensor[i][j][k]*dimensions[i]*dimensions[j]*x**((2*(exponents[i]-exponents[j]))%40)
                          for i in range(n) for j in range(n))
            value=reduce(numerator*dimension_inverse)
            q.require(value.degree()<=0,'computed modular second indicator is rational')
            q.require(value.nth(0).is_Integer,'computed modular second indicator is integral')
            result.append(int(value.nth(0)))
        return result
    fib=second_indicators([0,16],[[[1,0],[0,1]],[[0,1],[1,1]]],[1,(1+root5.as_expr())/2],(5-root5.as_expr())/10)
    semion=second_indicators([0,10],[[[1,0],[0,1]],[[0,1],[1,0]]],[1,1],s.Rational(1,2))
    q.require(fib==[1,1] and semion==[1,-1],'known modular indicator normalization controls')
    def table_vectors(value,scale):
        a,b=pair(value);expr=scale*(s.Rational(a)+s.Rational(b)*root5.as_expr())
        result=[]
        for exponent in range(40):
            poly=reduce(expr*x**exponent)
            row=[poly.nth(j) for j in range(16)]
            q.require(all(z.is_Integer for z in row),'exact scaled cyclotomic integer coefficients')
            result.append(list(map(int,row)))
        return np.asarray(result,dtype=np.int64)
    cases=[]
    for assignment in assignments:
        S=[[table.rows[assignment[j]][i]*dims[j]/sqrtD for j in range(7)] for i in range(7)]
        symmetric=all(S[i][j]==S[j][i] for i in range(7) for j in range(7))
        record={'assignment':list(assignment),'symmetric':symmetric}
        cases.append(record)
        if not symmetric:continue
        q.require(all(sum((S[i][k]*S[k][j] for k in range(7)),K.zero)==K(int(i==j)) for i in range(7) for j in range(7)),'normalized S is real orthogonal')
        perm=[];eps=[]
        for i in range(7):
            row=list(map(conjugate,S[i]))
            matches=[(j,e) for j in range(7) for e in (1,-1) if all(a==e*b for a,b in zip(row,S[j]))]
            q.require(len(matches)==1,'unique signed quadratic Galois row permutation')
            perm.append(matches[0][0]);eps.append(matches[0][1])
        q.require(perm==[6,1,2,3,5,4,0],'computed source Galois permutation')
        record.update({'galois_permutation':perm,'galois_signs':eps,'S':[[str(K.to_sympy(z)) for z in row] for row in S]})
        candidates=[]
        for c in range(5):
            fixed=[k for k in range(40) if k%5==(-c)%5]
            for k1,k2,k3,k4 in itertools.product(fixed,fixed,fixed,range(40)):
                exponents=[0,k1,k2,k3,k4,(8*c+9*k4)%40,8*c]
                q.require(all((exponents[perm[i]]-exponents[perm[0]]-9*exponents[i])%40==0 for i in range(7)),'all quadratic Galois twist congruences')
                candidates.append(exponents)
        candidates=np.asarray(candidates,dtype=np.int64)
        q.require(len(candidates)==102400,'complete Galois-compatible forty-root search')
        unnormalized=[[z*sqrtD for z in row] for row in S]
        scale=math.lcm(*(v.denominator for z in dims+sum(unnormalized,[]) for v in pair(z)))
        dim_vectors=[table_vectors(z,scale) for z in dims]
        # The vectorized sieve uses exact signed 64-bit integer arithmetic.
        # Bound every partial sum before carrying it out, including cancellation.
        dimension_vector_bound=max(int(abs(z).max()) for z in dim_vectors)
        q.require(max(sum(N[i][j]) for i in range(7) for j in range(7))*dimension_vector_bound < 2**62,'no integer overflow in balancing sums')
        history=[]
        for i,j in itertools.combinations_with_replacement(range(1,7),2):
            coefficients=table_vectors(unnormalized[i][j],scale)
            q.require(int(abs(coefficients).max())<2**62,'no integer overflow in balancing coefficients')
            left=coefficients[(candidates[:,i]+candidates[:,j])%40]
            right=np.zeros_like(left)
            for k in range(7):
                if N[i][j][k]:right += N[i][j][k]*dim_vectors[k][candidates[:,k]]
            mask=np.all(left==right,axis=1)
            old=len(candidates);candidates=candidates[mask]
            history.append({'pair':[i,j],'before':old,'after':len(candidates)})
            if not len(candidates):break
        indicators=[second_indicators(exponents) for exponents in candidates.tolist()]
        q.require(all(values[3] not in (-1,1) for values in indicators),'every balanced candidate violates the selfdual-simple second-indicator condition')
        record.update({'balancing_sieve':history,'twist_exponents_mod40':candidates.tolist(),'cyclotomic_integer_scale':scale,'second_indicators':indicators})
        print(json.dumps({'event':'assignment','assignment':list(assignment),'symmetric':True,'balanced_twists':len(candidates)}),flush=True)
    generated=[]
    for a in range(1,7):
        support={0,a}
        while True:
            enlarged=support|{k for i in support for j in support for k in range(7) if N[i][j][k]}
            if enlarged==support:break
            support=enlarged
        q.require(len(support)==7,'every nonunit basis object generates the whole fusion ring')
        generated.append({'generator':a,'closure':sorted(support)})
    result={'id':rid,'scope':'braided_categorification_exclusion_given_galois_pseudounitary_reduction','source_sha256':q.tensor_hash(N),'dimension_compatible_assignments':len(assignments),'cases':cases,'nonunit_generated_subrings':generated,'positive_controls':{'Fibonacci':fib,'semion':semion},'seconds':time.monotonic()-start}
    if write_receipt:
        (HERE/'R7_5_3895_modular_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'id':rid,'scope':result['scope'],'symmetric_assignments':sum(c['symmetric'] for c in cases),'balanced_twists':sum(len(c.get('twist_exponents_mod40',[])) for c in cases),'seconds':result['seconds']}))
    return result


if __name__=='__main__':run()
