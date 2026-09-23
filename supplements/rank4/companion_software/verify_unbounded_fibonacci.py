#!/usr/bin/env python3
"""Exact certificate for the unrestricted Fibonacci-subring theorem.

No numerical approximations, external packages, factorization, or search over
fusion rings are used.  The proved bound a+b*phi<36 makes this short integer
enumeration exhaustive.  Coefficient tuples mean 1, phi, x, phi*x.
"""
from fractions import Fraction as F
from math import isqrt
import json


def add(u, v):
    return tuple(c+d for c, d in zip(u, v))


def scale(c, u):
    return tuple(c*d for d in u)


def mul(u, v, a, b):
    out = [F(0)]*4
    def term(i, j, c):
        if not c:
            return
        if i >= 2:
            term(i-2, j, c)
            term(i-1, j, c)
        elif j >= 2:
            term(i, j-2, c)
            term(i, j-1, a*c)
            term(i+1, j-1, b*c)
        else:
            out[i+2*j] += c
    for k, c in enumerate(u):
        for l, d in enumerate(v):
            term(k % 2+l % 2, k//2+l//2, c*d)
    return tuple(out)


expected = [(0,2),(1,1),(2,2),(2,4),(2,8),(3,1),(4,4),
            (4,6),(4,10),(6,10),(6,11),(8,2),(8,11),(8,17),
            (10,8),(10,13),(10,16),(16,1),(21,5)]
# V and exact coefficients of 9 L_V - D(3 dim(V)+2).
witnesses = {
    (0,2): ('Y',(28,8,-4,12)),
    (2,2): ('X',(28,8,18,8)),
    (2,4): ('Y',(76,20,-10,2)),
    (2,8): ('X',(64,8,204,458)),
    (3,1): ('X',(34,14,64,51)),
    (4,4): ('X',(64,20,132,154)),
    (4,6): ('X',(76,20,8,-8)),
    (4,10): ('X',(100,20,192,640)),
    (6,10): ('Y',(208,56,-8,6)),
    (6,11): ('X',(130,32,86,219)),
    (8,11): ('X',(154,44,498,689)),
    (8,17): ('X',(190,44,1494,2741)),
    (10,8): ('X',(160,56,1516,1882)),
    (10,13): ('X',(190,56,1314,1879)),
    (10,16): ('Y',(340,92,42,10)),
}

one, phi, x, phix = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
records = []
bounded_count = 0
for a in range(36):
    for b in range(1,23):
        h0 = 72-2*a-b
        if h0 <= 0 or 5*b*b >= h0*h0:
            continue
        bounded_count += 1
        u, v = a*a+b*b+4, 2*a*b+b*b
        N = u*u+u*v-v*v
        r = isqrt(N)
        if r*r == N:
            kind = 1
        elif N % 5 == 0 and isqrt(N//5)**2 == N//5:
            r, kind = isqrt(N//5), 5
        else:
            continue
        P = a**3+2*a*a*b+4*a-b**3
        Q = a**3+3*a*a*b+a*b*b+4*a-2*b**3-4*b
        if kind == 1:
            dp, dq = F(P,r), F(Q,r)
        else:
            dp, dq = F(2*Q-P,5*r), F(2*P+Q,5*r)
        p, q = (F(a+b)-dp)/2, (F(a+2*b)-dq)/2
        pp, qq = a+b-p, a+2*b-q
        columns = [one, (1,0,a,b), (1,1,p,q), (1,1,pp,qq)]
        rec = {'a':a,'b':b,'N':N,'p':str(p),'q':str(q),
               'p_complement':str(pp),'q_complement':str(qq)}
        if any(t.denominator != 1 or t < 0 for t in [p,q,pp,qq]):
            assert (a,b) in [(8,2),(16,1),(21,5)]
            rec['obstruction'] = 'restriction coefficient'
        elif (a,b) == (1,1):
            rec['realization'] = 'Ad(E8)'
        else:
            V, target = witnesses[(a,b)]
            i, dimV = (2,x) if V == 'X' else (3,phix)
            low = (0,0,0,0)
            for col in columns:
                low = add(low, scale(col[i], col))
            D = mul((2,1,0,0), add(one,mul(x,x,a,b)), a,b)
            deficit = add(scale(9,low), scale(-1,mul(D,add(scale(3,dimV),scale(2,one)),a,b)))
            assert deficit == target, ((a,b), deficit, target)
            # Positivity certificates use only 3/2 < phi < 2 and x>0,
            # except two rows, where x < s+1 is additionally used.
            c0,c1,c2,c3 = target
            assert c0>0 and c1>0
            if (a,b) in [(2,4),(4,6)]:
                lower = add((c0,c1,0,0),mul((c2,c3,0,0),(a+1,b,0,0),a,b))
                assert lower == ((54,-6,0,0) if (a,b)==(2,4) else (68,-20,0,0))
                assert lower[0]+2*lower[1]>0
            else:
                assert c2+c3*(F(3,2) if c3>=0 else 2)>0
            rec['obstruction'] = 'Fejer '+V
            rec['positive_deficit_coefficients'] = target
        records.append(rec)

assert [(r['a'],r['b']) for r in records] == expected
assert len(records) == 19
assert bounded_count == 394
assert sum('Fejer' in r.get('obstruction','') for r in records) == 15
# The exact bound uses phi<34/21 and F increasing at x=36.
assert 7290-F(4491*34,21) == F(132,7)
assert 210-F(116*34,21)>0
print(json.dumps({'bounded_integer_pairs': bounded_count,
                  'normality_candidates':len(records),
                  'certificates':records},indent=2))
