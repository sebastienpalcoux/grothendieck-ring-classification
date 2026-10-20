"""Independent exact conductor-60 trace identities and certificate mutations."""
import copy
import json
import math

import sympy as s

from q60_center_trace import HERE, verify, require

x=s.Symbol('x')


def relative_trace(M,n,k):
    units=[u for u in range(M) if math.gcd(u,M)==1 and s.kronecker_symbol(60,u)==1]
    poly=s.Poly(sum(x**((M//n*k*u)%M) for u in units),x,domain=s.QQ)/len(units)
    return s.rem(poly,s.Poly(s.cyclotomic_poly(M,x),x,domain=s.QQ))


def sqrt15(M):
    gauss=s.Poly(sum(s.kronecker_symbol(60,u)*x**((M//60*u)%M) for u in range(60) if math.gcd(u,60)==1),x,domain=s.QQ)
    return s.rem(gauss/2,s.Poly(s.cyclotomic_poly(M,x),x,domain=s.QQ))


def main():
    checked=0
    for M in (60,120):
        root=sqrt15(M);mod=s.Poly(s.cyclotomic_poly(M,x),x,domain=s.QQ)
        require(s.rem(root*root,mod)==s.Poly(15,x,domain=s.QQ), 'exact quadratic Gauss sum')
        for k in range(M):
            if math.gcd(k,M)!=1:continue
            first=relative_trace(M,M,k);second=relative_trace(M,M,2*k)
            expected=s.Poly(s.kronecker_symbol(60,k)*root.as_expr()/8,x,domain=s.QQ)
            if M==60:
                require(first==expected and second==s.Poly(-s.Rational(1,8),x,domain=s.QQ), 'primitive 60 traces')
            else:
                require(first==s.Poly(0,x,domain=s.QQ) and second==expected, 'primitive 120 traces')
            for u in range(M):
                if math.gcd(u,M)==1:
                    require(relative_trace(M,M,k*u*u)==first, 'relative trace invariance under square automorphisms')
            checked+=1
    rejected=[]
    for rid in ('R7_5_443','R7_5_1214'):
        original=json.loads((HERE/(rid+'_q60_trace.json')).read_text())
        bad=copy.deepcopy(original);bad['branches'].pop()
        try:verify(rid,bad,write_receipt=False)
        except RuntimeError:rejected.append([rid,'missing_frame'])
        else:raise RuntimeError('missing low frame accepted')
        bad=copy.deepcopy(original);bad['separators']=[[0]*45 for _ in bad['separators']]
        try:verify(rid,bad,write_receipt=False)
        except RuntimeError:rejected.append([rid,'zero_separator'])
        else:raise RuntimeError('zero separating inequality accepted')
    report={'status':'PASS','primitive_twist_trace_pairs_checked':checked,
            'exact_quadratic_gauss_identities':2,'square_automorphism_trace_invariance':True,
            'malformed_certificates_rejected':rejected}
    (HERE/'q60_controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
