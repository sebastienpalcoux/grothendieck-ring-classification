"""Optional FLINT acceleration with an exact SymPy fallback.

Missing FLINT never prevents regeneration or verification.

All coefficients are arbitrary-precision integers. FLINT factors over Z;
no floating-point approximation or census label enters a decision.
The reference SymPy implementation remains in rings.dnumber/check_dnumber.
"""
try:
    from flint import fmpz_mat, fmpz_poly
except ImportError:
    fmpz_mat = fmpz_poly = None

BACKEND = 'python-flint' if fmpz_mat is not None else 'sympy'



def casimir_polynomial(R):
    if fmpz_mat is None:
        from rings import codegree_poly
        return codegree_poly(R)
    matrices = [fmpz_mat(N) for N in R]
    # Fusion reciprocity gives N_(i*) = N_i^T, for either duality type.
    C = sum((N*N.transpose() for N in matrices), fmpz_mat(4, 4))
    return C.charpoly()


def dnumber(R):
    if fmpz_mat is None:
        from rings import dnumber as reference_dnumber
        return reference_dnumber(R)
    # FLINT's factor discovery order can vary between runs. Canonicalize
    # it so the exact certificate agrees with the SymPy reference.
    ordered = sorted(casimir_polynomial(R).factor()[1],
                     key=lambda item: (item[0].degree(),
                         tuple(int(item[0][k]) for k in range(item[0].degree(), -1, -1))))
    for q, exponent in ordered:
        degree, norm = q.degree(), abs(int(q[0]))
        if norm == 0:
            raise ValueError('zero formal codegree')
        for j in range(1, degree+1):
            if pow(int(q[degree-j]), degree, norm**j):
                return {'kind':'dnumber', 'factor':[str(q[k]) for k in range(degree,-1,-1)], 'j':j}
    return None


def check_dnumber(R, certificate):
    if fmpz_mat is None:
        from rings import check_dnumber as reference_check
        return reference_check(R, certificate)
    # Regenerate the exact characteristic polynomial and its irreducible
    # factorization. In particular, do not trust a proposed factor's degree.
    q = fmpz_poly([int(a) for a in certificate['factor'][::-1]])
    if not any(q == g for g,e in casimir_polynomial(R).factor()[1]):
        raise ValueError('unrelated d-number irreducible factor')
    j, degree, norm = certificate['j'], q.degree(), abs(int(q[0]))
    if not isinstance(j,int) or not 1<=j<=degree or norm==0:
        raise ValueError('invalid d-number coefficient index or norm')
    if pow(int(q[degree-j]), degree, norm**j)==0:
        raise ValueError('d-number divisibility holds')

