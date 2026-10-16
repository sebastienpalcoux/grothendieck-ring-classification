"""Exact integer chart: TP irreducible abelian quartics, trace<=13, norm1/4.
No floating-point root filter, root finder, or black-box Galois group.
The docstring in the accompanying proof explains every finite test.
"""
from math import isqrt
from fractions import Fraction
import json
from pathlib import Path


def square(n):
    return n >= 0 and isqrt(n) ** 2 == n


def rational_square(q):
    q = Fraction(q)
    return q >= 0 and square(q.numerator) and square(q.denominator)


def reducible(t, s, r, h):
    for root in range(1, h + 1):
        if h % root == 0 and root**4-t*root**3+s*root**2-r*root+h == 0:
            return True
    for b in range(1, h + 1):
        if h % b:
            continue
        d = h // b
        for a in range(1, t):
            c = t-a
            if a*c+b+d == s and a*d+b*c == r:
                return True
    return False


out = {}
for h in (1,4):
    g = isqrt(h)
    for t in range(4,14):
        for z in range(2*g, t*t//4-2*g+1):
            B = z*z-4*h
            for s in range(z+1,3*t*t//8+1):
                A = t*t-4*s+4*z
                if A < 0 or not square(A*B):
                    continue
                for sign in (-1,1):
                    twice_r = t*z+sign*isqrt(A*B)
                    if twice_r % 2:
                        continue
                    r = twice_r//2
                    if not (1 <= r <= t**3//16):
                        continue
                    if h == 4 and (t % 2 or s % 2 or r % 4):
                        continue
                    S = t*t-2*s-2*z
                    J = s*s+2*s*z-3*z*z-4*t*r+16*h
                    if S <= 0 or J <= 0 or reducible(t,s,r,h):
                        continue
                    d = A if A else B
                    if not d or square(d):
                        continue
                    if square(J):
                        group = 'V4'
                    elif rational_square(Fraction(J,d)):
                        group = 'C4'
                    else:
                        continue
                    key=(t,s,r,h)
                    out.setdefault(key,{'polynomial':[1,-t,s,-r,h],
                                        'group':group,'resolvent_witnesses':[]})
                    witness={'z':z,'A':A,'B':B,'J':J}
                    if witness not in out[key]['resolvent_witnesses']:
                        out[key]['resolvent_witnesses'].append(witness)

rows=[out[key] for key in sorted(out)]
path=Path(__file__).with_name('quartic_trace13_exact_resolvent_chart.json')
path.write_text(json.dumps(rows,indent=2)+'\n')
print('Total rows:',len(rows))
for bound in (10,11,12,13):
    print('Trace at most',bound,':',sum(-row['polynomial'][1]<=bound for row in rows))
for row in rows:
    print(row)

# The manuscript table and machine-readable witnesses have one source.
assert len(rows) == 22, "unexpected trace-chart size"
def tex_cells(row):
    _, mt, s, mr, h = row["polynomial"]
    return [str(-mt), str(s), str(-mr), str(h),
            str(row["resolvent_witnesses"][0]["z"]),
            "C_4" if row["group"] == "C4" else "V_4"]
lines = [r"\begin{array}{rrrrrl|rrrrrl}",
         r"t&s&r&h&z&G&t&s&r&h&z&G\\\hline"]
for left, right in zip(rows[:11], rows[11:]):
    lines.append("&".join(tex_cells(left)+tex_cells(right))+r"\\")
lines.append(r"\end{array}")
Path(__file__).with_name("quartic_trace13_table.tex").write_text("\n".join(lines)+"\n")
