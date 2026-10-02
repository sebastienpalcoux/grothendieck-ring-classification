"""Independent exact controls. SymPy is used only for the known SU(2)4 matrices."""
from collections import Counter
from itertools import combinations, product
from functools import lru_cache
import json
from pathlib import Path
import sympy as s


def require(value, message):
    if not value:
        raise ValueError(message)


def eq(a,b):
    return s.simplify(s.expand_complex(a-b)) == 0


def matrix_eq(a,b):
    return all(eq(x,y) for x,y in zip(a,b))


def partition(A,B,D):
    """Independent all-size brute-force control in common exponent modulus144."""
    @lru_cache(None)
    def search(A,B,D):
        n=len(A)
        if not n:
            return ()
        for r in range(1,n+1):
            for tail in combinations(range(1,n),r-1):
                ia=(0,)+tail
                aa=tuple(A[i] for i in ia)
                for ib in combinations(range(n),r):
                    bb=tuple(B[i] for i in ib)
                    for idd in combinations(range(n),r):
                        dd=tuple(D[i] for i in idd)
                        if (sum(aa)+sum(bb)-sum(dd))%144:
                            continue
                        if r>1:
                            ca,cb,cd=map(Counter,(aa,bb,dd))
                            if sum(v*v for c in (ca,cb,cd) for v in c.values())>r*r+2:
                                continue
                            if any(max(x.values())+max(y.values())>r for x,y in ((ca,cb),(ca,cd),(cb,cd))):
                                continue
                            if any(ca[a]+cb[b]+cd.get((a+b)%144,0)>r for a,b in product(ca,cb)):
                                continue
                        rest=search(tuple(A[i] for i in range(n) if i not in ia),
                                    tuple(B[i] for i in range(n) if i not in ib),
                                    tuple(D[i] for i in range(n) if i not in idd))
                        if rest is not None:
                            return ((aa,bb,dd),)+rest
        return None
    return search(tuple(sorted(A)),tuple(sorted(B)),tuple(sorted(D)))


def run():
    I=s.I
    theta=[s.expand_complex(s.exp(s.pi*I*j*(j+2)/12)) for j in range(5)]
    S=s.Matrix(5,5,lambda j,k:s.sin((j+1)*(k+1)*s.pi/6)/s.sqrt(3))
    N=lambda j,k,l:int(abs(j-k)<=l<=min(j+k,8-j-k) and (j+k+l)%2==0)
    def nu(n,c,b,a):
        return s.simplify(s.expand_complex(sum((theta[d]/theta[e])**n*S[c,d]*s.conjugate(S[b,e])*N(d,e,a)
                            for d,e in product(range(5),repeat=2))))
    A=s.diag((-1+I)/s.sqrt(2), (s.sqrt(6)+s.sqrt(2)+I*(s.sqrt(6)-s.sqrt(2)))/4)
    F=s.Matrix([[1/s.sqrt(3),s.sqrt(s.Rational(2,3))],[s.sqrt(s.Rational(2,3)),-1/s.sqrt(3)]])
    C=F*A*F
    require(matrix_eq(A*C*A,C*A*C),'known braid relation')
    B=A*C
    D=B*A
    require(matrix_eq(B**3,-I*s.eye(2)) and matrix_eq(D**2,-I*s.eye(2)),'known center')
    require(eq(s.trace(D),0),'known Delta trace')
    require(eq(s.trace(B),-s.sqrt(3)/2+I/2),'known beta trace')
    require(eq(nu(2,1,1,1)/theta[1],s.trace(D)),'BJT n2 matrix comparison')
    require(eq(nu(3,0,1,1)/theta[1],s.trace(B)),'BJT n3 matrix comparison')
    require(eq(nu(2,2,2,2)/theta[2],-s.Rational(1,2)-s.sqrt(3)*I/2),'dimension3 Delta')
    require(eq(nu(3,0,2,2)/theta[2],0),'dimension3 beta')
    # Convert the independently known spectra into common zeta144 exponents.
    A2,B2,D2=[54,6],[36,84],[54,126]
    A3,B3,D3=[96,48,24],[112,16,64],[96,96,24]
    p2,p3,p4=partition(A2,B2,D2),partition(A3,B3,D3),partition(A2*2,B2*2,D2*2)
    neg=partition([0,0],[48,96],[0,0])
    require(p2 is not None and p3 is not None and p4 is not None,'positive partitions')
    require(neg is None,'negative partition')
    require(sum(v*v for c in map(Counter,(A2*2,B2*2,D2*2)) for v in c.values())>4*4+2,'reducible whole-block fails Scott')
    receipt=dict(status='PASS',su2_4_exact_matrix_braid_relation=True,
                 indicator_matrix_phase_comparisons=2,
                 dimension3_indicator_comparisons=2,
                 dimension2_constituents=[len(t[0]) for t in p2],
                 dimension3_constituents=[len(t[0]) for t in p3],
                 reducible_dimension4_constituents=[len(t[0]) for t in p4],
                 artificial_negative='exhaustive failure',
                 positive_spectra_mod144={'dim2':[A2,B2,D2],'dim3':[A3,B3,D3]})
    return receipt


if __name__=='__main__':
    receipt=run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
