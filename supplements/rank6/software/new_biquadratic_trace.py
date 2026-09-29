"""Tensor-only general categorical obstruction from a biquadratic dimension field.

This implements the trace/orthogonality and d-number argument audited from
B13_General_Exclusion, for rank six self-dual commutative based rings.  It
uses exact integer arithmetic and recomputes every finite search in verify().
No spherical or pseudounitary hypothesis is imposed on the input category.
"""
import argparse
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
import json
from pathlib import Path
import sys
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from exact import require
from new_module_spectral import perron_factor


def squarefree(n):
    k = 1
    q = 1
    for p, e in s.factorint(n).items():
        k *= int(p) ** (e // 2)
        q *= int(p) ** (e % 2)
    return k, q


def field_discriminant(q):
    return q if q % 4 == 1 else 4*q


def tensor_data(R):
    n = len(R)
    if n != 6 or any(len(a) != n or any(len(b) != n for b in a) for a in R):
        return None
    if any(type(R[i][j][k]) is not int or R[i][j][k] < 0
           for i, j, k in product(range(n), repeat=3)):
        return None
    if any(R[0][i][j] != int(i == j) or R[i][j][0] != int(i == j)
           for i, j in product(range(n), repeat=2)):
        return None
    if any(R[i][j][k] != R[j][i][k] or R[i][j][k] != R[i][k][j]
           for i, j, k in product(range(n), repeat=3)):
        return None
    matrices = [s.Matrix(a) for a in R]
    if any(matrices[i]*matrices[j] != sum((R[i][j][k]*matrices[k]
              for k in range(n)), s.zeros(n)) for i in range(n) for j in range(i,n)):
        return None
    C = sum((M*M for M in matrices), s.zeros(n))
    t = s.Symbol('t')
    factors = C.charpoly(t).as_poly().factor_list()[1]
    # Restrict to quadratic formal-codegree fields and the unit factorization
    # D=5*sqrt(n)*u, u^2-s*u-1=0, n=s^2+4.
    if any(f.degree() > 2 for f, _ in factors):
        return None
    pf, interval = perron_factor([f for f, _ in factors])
    F = factors[pf][0]
    co = [int(a) for a in F.all_coeffs()]
    if F.degree() != 2 or co[0] != 1 or co[1] >= 0 or -co[1] % 5:
        return None
    radicand = -co[1] // 5
    if co[2] != 25*radicand or radicand <= 4 or isqrt(radicand-4)**2 != radicand-4:
        return None
    k, ell = squarefree(radicand)
    fields = {squarefree(int(s.discriminant(f.as_expr(), t)))[1]
              for f, _ in factors if f.degree() == 2}
    choices = []
    for p in sorted(fields - {ell}):
        # Orient the biquadratic basis with an odd discriminant first.
        if p <= 1 or p % 4 != 1:
            continue
        q = ell if gcd(p,ell) == 1 else ell // p if ell % p == 0 else 0
        if q <= 1 or gcd(field_discriminant(p), field_discriminant(q)) != 1:
            continue
        if any(a not in (1,p,q,p*q) for a in fields):
            continue
        choices.append((p,q))
    if not choices:
        return None
    p,q = choices[0]
    return {'rank': n, 'casimir_trace': int(s.trace(C)),
            'casimir_charpoly_mod2': [int(v)%2 for v in C.charpoly(t).all_coeffs()],
            'casimir_factors': [{'coefficients': [int(c) for c in f.all_coeffs()],
                                'multiplicity': int(m)} for f,m in factors],
            'perron_factor': co, 'perron_interval': interval,
            'radicand': radicand, 'unit_parameter': isqrt(radicand-4),
            'square_multiplier': k, 'squarefree_radicand': ell,
            'p': p, 'q': q, 'field_discriminants': [field_discriminant(p),field_discriminant(q)]}


def integral(x,y,z,w,p,q):
    e,h = (1,2) if q % 4 == 1 else (0,1)
    return (h*w % 2 == 0 and h*(z-w) % 4 == 0
            and (y-e*w) % 2 == 0 and (x-y-e*z+e*w) % 4 == 0)


def positive(a,b,c,d,p,q):
    if a <= 0 or a*a <= p*b*b:
        return False
    L = a*a+p*b*b-q*(c*c+p*d*d)
    H = 2*a*b-2*q*c*d
    return L > 0 and L*L > p*H*H


def norm_numerator(x,y,z,w,p,q):
    L = x*x+p*y*y-q*(z*z+p*w*w)
    H = 2*x*y-2*q*z*w
    return L*L-p*H*H


def inverse_trace(a,b,c,d,p,q):
    # For Delta=(a+b*sqrt(p)+c*sqrt(q)+d*sqrt(pq))/4,
    # the constant coefficient of the cubic conjugate product is
    # a^3-a*p*b^2-a*q*c^2-a*p*q*d^2+2*p*q*b*c*d.
    num = a*a*a-a*p*b*b-a*q*c*c-a*p*q*d*d+2*p*q*b*c*d
    return Fraction(16*num, norm_numerator(a,b,c,d,p,q))


def conjugate_polynomial(delta,p,q):
    t=s.Symbol('t')
    a,b,c,d=[s.Rational(v,4) for v in delta]
    L=(t-a)**2+p*b*b-q*c*c-p*q*d*d
    H=-2*b*(t-a)-2*q*c*d
    P=s.Poly(L*L-p*H*H,t)
    require(all(v.q==1 for v in P.all_coeffs()),'nonintegral conjugate polynomial')
    return P


def complementary_pairs(delta,T,p,q,original_mod2):
    a,b,c,d = delta
    remaining = 1-inverse_trace(a,b,c,d,p,q)
    if remaining <= 0:
        return []
    A,B = remaining.numerator, remaining.denominator
    out = []
    for k in range(1, (T-a)//A+1):
        S,P = A*k,B*k
        disc = S*S-4*P
        if disc < 0 or S <= 2 or P-S+1 <= 0:
            continue
        r = isqrt(disc)
        if r*r == disc:
            if (S-r) % 2 or (S-r)//2 <= 1:
                continue
        else:
            if S*S % P:
                continue
            # Every signed formal codegree also lies in the dimension field,
            # by the same induction theorem applied to sphericalization.
            if squarefree(disc)[1] not in (p,q,p*q):
                continue
        poly=s.Poly.from_list([1,-S,P],s.Symbol('t'))
        total=conjugate_polynomial(delta,p,q)*poly
        mod2=[int(v)%2 for v in total.all_coeffs()]
        out.append({'sum':S,'product':P,'polynomial':[1,-S,P],
                    'total_casimir_charpoly_mod2':mod2,
                    'parity_compatible':mod2==original_mod2})
    return out


def calculate(R):
    data = tensor_data(R)
    if data is None:
        return None
    p,q,k,ell,T = (data[a] for a in ('p','q','square_multiplier','squarefree_radicand','casimir_trace'))
    scale = 5*k
    denominator = scale*ell
    mmax = (T-3)//denominator
    lattice_m = [m for m in range(1,mmax+1) if denominator*m % (p*q) == 0]
    norm_survivors=[]
    eligible=positive_count=norm_count=0
    for m in lattice_m:
        if ell == q:
            rx=isqrt(m*m*q-1); ry=isqrt((m*m*q-1)//p); rw=isqrt((m*m-1)//p)
            iterator=((x,y,m,w) for w in range(-rw,rw+1) for x in range(-rx,rx+1) for y in range(-ry,ry+1))
        else:
            require(ell == p*q,'invalid field orientation')
            rx=isqrt(m*m*p*q-1); ry=isqrt(m*m*q-1); rz=isqrt(m*m*p-1)
            iterator=((x,y,z,m) for x in range(-rx,rx+1) for y in range(-ry,ry+1) for z in range(-rz,rz+1))
        for x,y,z,w in iterator:
            if not integral(x,y,z,w,p,q):
                continue
            eligible+=1
            if ell == q:
                delta=(scale*q*z,scale*q*w,scale*x,scale*y)
            else:
                delta=(scale*p*q*w,scale*q*z,scale*p*y,scale*x)
            if not positive(*delta,p,q):
                continue
            positive_count+=1
            norm_num=norm_numerator(x,y,z,w,p,q)
            require(norm_num > 0 and norm_num%256 == 0,'invalid integral norm')
            norm=norm_num//256
            if (ell*ell*m**4)%norm:
                continue
            norm_count+=1
            pairs=complementary_pairs(delta,T,p,q,data['casimir_charpoly_mod2'])
            norm_survivors.append({'theta_numerator':[x,y,z,w], 'theta_denominator':4,
                                  'theta_norm':norm,'delta_numerator':list(delta),
                                  'delta_denominator':4,'delta_trace':delta[0],
                                  'complementary_pairs':pairs})
    return {'kind':'biquadratic_spherical_trace','scope':'general_complex_fusion_categories',
            'data':data,'trace_parameter_upper_bound':mmax,'trace_lattice_parameters':lattice_m,
            'integral_box_candidates':eligible,'totally_positive_candidates':positive_count,
            'norm_survivors':norm_survivors,
            'excluded':all(not any(z['parity_compatible'] for z in r['complementary_pairs']) for r in norm_survivors)}


def certificate(R):
    c=calculate(R)
    return c if c is not None and c['excluded'] else None


def verify(R,c):
    require(c.get('kind')=='biquadratic_spherical_trace','incorrect certificate kind')
    recomputed=calculate(R)
    require(recomputed is not None and recomputed['excluded'],'tensor is not excluded by this criterion')
    require(recomputed==c,'recomputed certificate differs')
    return True


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all',action='store_true')
    ap.add_argument('--output',default=str(ROOT/'research/round2_external/biquadratic_trace_scan.json'))
    args=ap.parse_args()
    manifest=ROOT/'verification/round2/campaign_manifest.json'
    if args.all:
        rows=json.load(open(ROOT/'data/census.json'))
    elif manifest.exists():
        rows=json.load(open(manifest))['inputs']
    else:
        rows=json.load(open(ROOT/'data/unresolved_tensors.json'))
    found=[]
    for row in rows:
        c=calculate(row['N'])
        if c is not None:
            found.append({'id':row['id'],'certificate':c})
            print(row['id'],c['excluded'],c['trace_lattice_parameters'],len(c['norm_survivors']),flush=True)
    Path(args.output).write_text(json.dumps({'checked':len(rows),'applicable':found},indent=2)+'\n')

if __name__=='__main__':
    main()
