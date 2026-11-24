"""Check the exchanged-pair norm restrictions and final congruence comparison.

No fusion tables, conductor files, or global dimension range are inputs.
"""
from fractions import Fraction as Q
from math import gcd, isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gap(f, conductor):
    return (f-2)**2 - Q(4*f*f, conductor)


def check_profiles():
    # f^2-20f-60 is increasing for f>10 and is positive at f=23.
    require(23**2-20*23-60 > 0, "Maximum possible codegree")
    profiles = {
        2+2*u*u+v*v: (u, v) for u in range(1, isqrt(10)+1)
        for v in range(1, isqrt(18)+1) if gcd(u, v) == 1 and 2+2*u*u+v*v <= 22
    }
    require(profiles == {5: (1, 1), 8: (1, 2), 11: (2, 1), 13: (1, 3),
                         19: (2, 3), 20: (1, 4), 21: (3, 1)}, "Codegree profiles")
    require(all(gap(f, 8) > 16 for f in profiles if f >= 11), "Fields above codegree 8")
    require(gap(8, 13) > 16, "Largest possible conductor at codegree 8")
    caps = {(19, 5): 80, (21, 5): 1, (8, 12): 1, (8, 8): 4, (20, 5): 4, (5, 12): 24}
    require(all(16//gap(f, cond) == cap for (f, cond), cap in caps.items()), "Norm bounds")
    require(2*Q(9, 22)**2 - Q(4, 121) - Q(4, 44) > Q(1, 5), "Codegree eleven")
    for f in (8, 20):
        w = profiles[f][1]
        disc = f*w*w
        # For c>=w+1 even the smaller of the two discriminants is too large
        # and it increases thereafter.
        def value(c, u):
            return ((w+Q(2, w))*c)**2 + Q(8*u*c, w) + 4
        require(value(w+1, -1) > disc, "End of quadratic comparison")
        require([(c, u) for c in range(w+1) for u in (-1, 1) if value(c, u) == disc]
                == [(w, -1)], "Remaining rational character")
    require([(c, u) for c in range(3) for u in (-1, 1)
             if (9*c*c+8*u*c+4) <= 30 and (9*c*c+8*u*c+4) % 5 == 0]
            == [(1, -1)], "Codegree five at conductor at least twelve")
    print("Seven possible rational codegrees; only (f,F)=(5,5),(8,8),(20,5) remain.")


def check_final_congruence():
    require([s for s in range(45) if s % 9 == 4 and (9*s*s+8*s+4) % 5 == 0]
            == [4], "Third-indicator congruence")
    # Bound 94/122^2 + 18 sqrt(3/2)/122 < 1/4 at c>=41.
    remainder = Q(1, 4) - Q(94, 122**2)
    require(remainder > 0 and remainder**2 > Q(18**2*3, 2*122**2),
            "Two-center moment contradiction")
    require(Q(1, 4) < Q(44, 175), "Two-center moment comparison")
    print("Codegree five leaves (c,u)=(1,-1),(4,1) before the endpoint moment test.")


if __name__ == '__main__':
    check_profiles()
    check_final_congruence()
