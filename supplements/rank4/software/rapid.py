"""Exact FLINT acceleration for formal-codegree d-number certificates.

All coefficients are arbitrary-precision integers. FLINT factors over Z;
no floating-point approximation or census label enters a decision.
The reference SymPy implementation remains in rings.dnumber/check_dnumber.
"""
from flint import fmpz_mat, fmpz_poly


def casimir_polynomial(R):
    matrices = [fmpz_mat(N) for N in R]
    # Fusion reciprocity gives N_(i*) = N_i^T, for either duality type.
    C = sum((N*N.transpose() for N in matrices), fmpz_mat(4, 4))
    return C.charpoly()


def dnumber(R):
    for q, exponent in casimir_polynomial(R).factor()[1]:
        degree, norm = q.degree(), abs(int(q[0]))
        if norm == 0:
            raise ValueError('zero formal codegree')
        for j in range(1, degree+1):
            if pow(int(q[degree-j]), degree, norm**j):
                return {'kind':'dnumber', 'factor':[str(q[k]) for k in range(degree,-1,-1)], 'j':j}
    return None


def check_dnumber(R, certificate):
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


SMALL_PRIMES=(2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113)

def cyclotomic_failure(R):
    """Exhibit unequal unramified Frobenius cycle lengths, using exact Z/Fp arithmetic."""
    from flint import nmod_poly
    for matrix_index,N in enumerate(R):
        for q,exponent in fmpz_mat(N).charpoly().factor()[1]:
            if q.degree()<3:continue
            coefficients=[int(q[k]) for k in range(q.degree()+1)]
            for prime in SMALL_PRIMES:
                factors=nmod_poly(coefficients,prime).factor()[1]
                if all(e==1 for g,e in factors) and len({g.degree() for g,e in factors})>1:
                    return {'kind':'cyclotomic','matrix':matrix_index,
                        'polynomial':[str(a) for a in coefficients[::-1]],'prime':prime}
    return None


def check_cyclotomic(R,certificate):
    from flint import nmod_poly
    index=certificate['matrix'];prime=certificate['prime']
    if type(index) is not int or not 0<=index<4 or prime not in SMALL_PRIMES:
        raise ValueError('invalid cyclotomic matrix or prime witness')
    q=fmpz_poly([int(a) for a in certificate['polynomial'][::-1]])
    if not any(q==g for g,e in fmpz_mat(R[index]).charpoly().factor()[1]):
        raise ValueError('unrelated cyclotomic irreducible factor')
    factors=nmod_poly([int(q[k]) for k in range(q.degree()+1)],prime).factor()[1]
    if not all(e==1 for g,e in factors) or len({g.degree() for g,e in factors})<=1:
        raise ValueError('Frobenius cycle lengths compatible with abelianity')
