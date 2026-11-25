"""Complete the four dimension-matched conductor-five tables and compare induction modulo two."""
from itertools import combinations_with_replacement, permutations, product

import sympy as sp

from golden_orbit_check import mul, one
from golden_rational_two_check import match, ordinary_rows, profiles, tables


INDICES = range(6)
PAIRS = tuple(combinations_with_replacement(INDICES, 2))


def subtraction(a, n, b):
    return (a[0] - n*b[0], a[1] - n*b[1])


def ordinary_completions(signed, dims):
    # Rigidity determines the dual from the coefficient of the unit.
    dual = []
    for i in INDICES:
        support = [j for j in INDICES if signed[i][j][0]]
        if len(support) != 1 or abs(signed[i][support[0]][0]) != 1:
            return
        dual.append(support[0])
    if any(dual[dual[i]] != i for i in INDICES):
        return
    # Coefficients of 1 in triple products are symmetric, also under simultaneous duality.
    def key(i, j, k):
        triple = (i,j,dual[k])
        return min(tuple(sorted(triple)), tuple(sorted(dual[t] for t in triple)))
    rows = {(i,j): tuple(key(i,j,k) for k in INDICES) for i,j in PAIRS}
    lower = {}
    for (i,j), keys in rows.items():
        for k, v in enumerate(keys):
            a = abs(signed[i][j][k])
            if v in lower and (lower[v]-a) % 2:
                return
            lower[v] = max(a,lower.get(v,0))
    known = {key(0,i,k): int(i == k) for i,k in product(INDICES,repeat=2)}
    if any(a < lower[v] or (a-lower[v])%2 for v,a in known.items()):
        return
    def options(i, j, fixed):
        target = mul(dims[i],dims[j])
        weights = {}
        for k, v in enumerate(rows[i,j]):
            if v in fixed:
                target = subtraction(target,fixed[v],dims[k])
            else:
                a,b = weights.get(v,(0,0))
                weights[v] = (a+dims[k][0],b+dims[k][1])
        unknown = tuple(sorted(weights, key=lambda v: sum(weights[v]), reverse=True))
        def fill(pos,rem,values):
            if pos == len(unknown):
                if rem == (0,0):
                    yield values
                return
            v=unknown[pos]
            a,b=weights[v]
            # All the surviving dimensions have nonnegative integral coordinates.
            assert a>=0 and b>=0 and (a or b)
            cap = min(rem[t]//w for t,w in enumerate((a,b)) if w)
            for n in range(lower[v],cap+1,2):
                yield from fill(pos+1,subtraction(rem,n,(a,b)),{**values,v:n})
        yield from fill(0,target,{})
    def complete(pairs,fixed):
        if not pairs:
            yield [[[fixed[key(i,j,k)] for k in INDICES] for j in INDICES] for i in INDICES]
            return
        # Fewest new coefficients first. This ordering changes only running time.
        ij=min(pairs,key=lambda ij:(len(set(rows[ij])-fixed.keys()),sum(mul(dims[ij[0]],dims[ij[1]]))))
        for assignment in options(*ij,fixed):
            yield from complete(pairs-{ij},fixed|assignment)
    for tensor in complete(set(PAIRS),known):
        yield tensor,dual


def witness(tensor, dual):
    # Rows of a multiplication matrix are images of basis elements.
    M=[sp.Matrix(row) for row in tensor]
    C=sum((tensor[i][dual[i]][0]*M[i]*M[dual[i]] for i in INDICES),sp.zeros(6))
    x=sp.symbols('x')
    _,factors=sp.factor_list(C.charpoly(x).as_expr(),x)
    p=sp.Poly(0,x,domain=sp.QQ)
    modulus=sp.Poly(1,x,domain=sp.QQ)
    for q,_ in factors:
        q=sp.Poly(q,x,domain=sp.QQ).monic()
        assert q.degree() in (1,2)
        value=1 if q.degree()==1 else x**2/q.TC()
        correction=((sp.Poly(value,x,domain=sp.QQ)-p)*sp.invert(modulus,q)).rem(q)
        p+=modulus*correction
        modulus*=q
    mat=sp.zeros(6)
    for coeff in p.all_coeffs():
        mat=mat*C+coeff*sp.eye(6)
    return tuple(mat[0,k] for k in INDICES)


if __name__ == '__main__':
    seen={}
    for m,H,a,b,D in profiles():
        for X,Y,T in tables(m,H,a,b):
            for u in ordinary_rows(D):
                for perm in sorted(set(permutations(u))):
                    dims=(one,*perm)
                    if not match(X,Y,T,dims):
                        continue
                    if m == 60:
                        y = dims.index((4,8))
                        v = dims.index((8,12))
                        assert T[y][y][v] == -2
                    report=[]
                    for R,dual in ordinary_completions(T,dims):
                        uR,uT=witness(R,dual),witness(T,dual)
                        assert all(x.is_Integer for x in uR+uT)
                        assert any((x-y)%2 for x,y in zip(uR,uT))
                        report.append(tuple(i for i in INDICES if (uR[i]-uT[i])%2))
                    if m == 20:
                        assert report == [(3, 5)]
                        assert uR == (1,1,1,2,1,3) and uT == (1,1,1,1,1,2)
                    else:
                        assert m == 60 and not report
                    seen.setdefault(m,set()).add((X,Y,dims))
                    print(m,report)
    assert {m:len(s) for m,s in seen.items()} == {20:2,60:2}
