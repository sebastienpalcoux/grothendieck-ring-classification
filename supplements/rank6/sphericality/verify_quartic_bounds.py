"""Verify the finite substitutions and the constant comparisons in the quartic proofs."""
from fractions import Fraction as Q
from math import gcd, isqrt


def pairs(c, bound, minimum_u=Q(0)):
    rows = []
    for n in range(1, bound + 1):
        for ell in range(2*c, n//2+1, c):
            delta = ell**2 - 4*n
            if ell*ell % n or Q(ell,n) < minimum_u:
                continue
            if not 0 < 2*c*delta <= gcd(c,4)*n*n or delta % c:
                continue
            if isqrt(delta//c)**2 == delta//c:
                rows.append((c,ell,n))
    return rows


g = Q(4, 94)
four = [(8,16,32), (8,24,72), (12,36,81), (12,24,96)]
assert pairs(8,98)+pairs(12,98)==four
for c,ell,n in four[1:]:
    t=1-Q(ell,n)
    v2=Q(ell*ell-4*n,n*n)
    assert t>g and (t-g)**2>Q(gcd(c,4),c)-2*v2
assert Q(1,12)-Q(4,99)>g
assert (Q(1,2)-Q(2,94))**2>Q(2,9)
assert (Q(1,2)-g)**2>Q(1,5)
assert (Q(3,4)-g)**2>Q(1,2)
assert (Q(71,100)-Q(1,350))**2>Q(1,2)
assert Q(13)*Q(29,100)**2-2*Q(29,100)>Q(1,2)
assert 40*Q(1,4)**2-2*Q(1,4)==2
for c,m in [(24,5217),(28,315)]:
    assert int(4/(Q(29,100)**2-Q(gcd(c,4),2*c)))==m
    assert pairs(c,m,Q(29,100))==[]
assert int(4/(Q(36,100)**2-Q(1,10)))==135
assert pairs(5,135,Q(36,100))==[(5,10,20)]
assert 8*(94**2//4-4)==17640
assert 1024*17640==18063360
print('Four small conductor-8/12 cases, the conductor-24/28 exclusions,')
print('the unique short conductor-5 pair, and all numerical gaps verified.')
