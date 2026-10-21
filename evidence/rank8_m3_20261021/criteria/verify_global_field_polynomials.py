"""Independent multiplication-matrix checks of convex biquadratic filters."""
from fractions import Fraction as Q
import itertools,json
import sympy as s
import global_induction as g

def main():
    reports=[]
    for q,r in [(2,3),(3,5),(3,7),(3,13)]:
        def mul(a,b):
            out=[Q(0)]*4
            for i,x in enumerate(a):
                for j,y in enumerate(b):out[i^j]+=x*y*(q if i&j&1 else 1)*(r if i&j&2 else 1)
            return tuple(out)
        count=0
        for z in itertools.product((-1,0,1),repeat=4):
            matrix=s.Matrix.hstack(*(s.Matrix(mul(z,tuple(int(i==j) for i in range(4)))) for j in range(4)))
            expected=[Q(str(x)) for x in matrix.charpoly().as_poly().sqf_part().monic().all_coeffs()]
            actual=g.biquadratic_polynomial(z,mul);g.require(actual==expected,'biquadratic minpoly mismatch '+str((q,r,z)))
            count+=1
        reports.append({'radicands':[q,r],'exact_checks':count})
    out={'result':'PASS','method':'independent rational multiplication matrix characteristic polynomial, squarefree part','reports':reports}
    (g.HERE/'global_field_polynomial_validation.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps(out))
if __name__=='__main__':main()
