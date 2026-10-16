"""Exact universal arithmetic filters, with optional FLINT acceleration.

Both backends factor the same integer polynomials and apply the same
coefficient divisibilities and unramified Frobenius tests. No numerical
approximation assigns an exclusion.
"""
try:
    from rapid_flint import (casimir_polynomial, dnumber, check_dnumber,
                             cyclotomic_failure, check_cyclotomic)
    BACKEND = "python-flint"
except ModuleNotFoundError as error:
    if error.name != "flint":
        raise
    from functools import lru_cache
    import sympy as s
    from exact import t, cyclotomic_failure as _cyclotomic_failure
    from exact import check_cyclotomic as _check_cyclotomic
    BACKEND = "sympy-exact"

    def _charpoly(A):
        # Newton identities through degree four, using Python integers.
        power = [[int(i == j) for j in range(4)] for i in range(4)]
        traces = [0]
        coefficients = [1]
        for k in range(1, 5):
            power = [[sum(power[i][l] * A[l][j] for l in range(4))
                      for j in range(4)] for i in range(4)]
            traces.append(sum(power[i][i] for i in range(4)))
            numerator = -sum(coefficients[k-i] * traces[i] for i in range(1,k+1))
            if numerator % k:
                raise ValueError("nonintegral characteristic coefficient")
            coefficients.append(numerator // k)
        return tuple(coefficients)

    @lru_cache(maxsize=32768)
    def _factors(coefficients):
        return tuple(s.Poly.from_list(list(coefficients),t,domain=s.ZZ).factor_list()[1])

    def _coefficients(R):
        C = [[sum(R[i][j][l]*R[i][k][l] for i in range(4) for l in range(4))
              for k in range(4)] for j in range(4)]
        return _charpoly(C)

    def casimir_polynomial(R):
        return tuple(reversed(_coefficients(R)))

    def dnumber(R):
        for q, exponent in _factors(_coefficients(R)):
            co = tuple(map(int,q.all_coeffs()))
            degree, norm = q.degree(), abs(co[-1])
            if not norm:
                raise ValueError("zero formal codegree")
            for j in range(1,degree+1):
                if pow(co[j],degree,norm**j):
                    return {"kind":"dnumber","factor":list(map(str,co)),"j":j}
        return None

    def check_dnumber(R, certificate):
        q = s.Poly.from_list([int(a) for a in certificate["factor"]],t,domain=s.ZZ)
        if not any(q == g for g,e in _factors(_coefficients(R))):
            raise ValueError("unrelated d-number factor")
        j = certificate["j"]
        co = list(map(int,q.all_coeffs()))
        if type(j) is not int or not 1 <= j <= q.degree() or not co[-1]:
            raise ValueError("invalid d-number index or norm")
        if not pow(co[j],q.degree(),abs(co[-1])**j):
            raise ValueError("d-number divisibility holds")

    def cyclotomic_failure(R):
        polys = [s.Poly.from_list(list(_charpoly(A)),t,domain=s.ZZ) for A in R]
        return _cyclotomic_failure(polys,limit=120)

    def check_cyclotomic(R, certificate):
        polys = [s.Poly.from_list(list(_charpoly(A)),t,domain=s.ZZ) for A in R]
        return _check_cyclotomic(polys,certificate)
