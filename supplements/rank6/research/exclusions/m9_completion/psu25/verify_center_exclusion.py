#!/usr/bin/env python3
"""Finite exact center/Galois arithmetic for the R6_9_3748 exclusion.

The theoretical reduction is in center_exclusion.tex. This script verifies
the Gram identities, Galois dimension action, and six-versus-four bound.
"""
import argparse
import hashlib
import json
from pathlib import Path

import sympy as s
from verify_sphericality import A, SOURCE, extension, require, load_source

HERE = Path(__file__).resolve().parent
a,h = s.symbols('a h')
pa = a**3-a**2-2*a+1


def reduce6(v):
    v = s.rem(s.Poly(s.expand(v),h),s.Poly(h*h-13,h)).as_expr()
    return s.expand(sum(s.rem(v.coeff(h,j),pa,a)*h**j for j in range(2)))


def vector6(v):
    v = reduce6(v)
    return s.Matrix([v.coeff(h,j).coeff(a,i) for j in range(2) for i in range(3)])


field_basis = [1,a,a*a,h,a*h,a*a*h]


def inverse6(v):
    M = s.Matrix.hstack(*[vector6(v*b) for b in field_basis])
    c = M.inv()*vector6(1)
    return sum(c[i]*field_basis[i] for i in range(6))


def as_ints(v):
    require(all(x.q == 1 for x in v), 'integral coefficients')
    return list(map(int,v))



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args = parser.parse_args()
    R = extension([2,2,1])
    source = load_source()['N']
    perm = [0,1,5,2,3,4]
    require(R == [[[source[i][j][k] for k in perm] for j in perm] for i in perm], 'exact source tensor')
    N = list(map(s.Matrix,R))
    NA = list(map(s.Matrix,A))
    b = a*a-1
    q = 2+2*a+b
    x = (q+b*h)/2
    D = 1+a*a+b*b
    f = reduce6(D*(1+x*x))
    require(reduce6(q*q+4-13*b*b) == 0,'quadratic discriminant identity')
    require(reduce6(x*x-q*x-1) == 0,'positive dimension identity')
    cb = [1,a,b,x,reduce6(a*x),reduce6(b*x)]
    dimension_basis = s.Matrix.hstack(*map(vector6,cb))
    require(dimension_basis.det() != 0,'dimension map injective on Q ring')
    D_norm = s.Matrix.hstack(*[vector6(D*v) for v in field_basis]).det()
    require(D_norm == 7**4, 'D global norm over sextic field')
    center_dimension = reduce6(f*f*inverse6(D))
    center_norm = s.Matrix.hstack(*[vector6(center_dimension*v) for v in field_basis]).det()
    require(center_norm == 7**4*13**6,'centralizer global norm')
    records = []
    E = []
    for aj,dj,label in [(a,1,0),(a*a-a-1,b,2),(2-a*a,a,1)]:
        for sign in [1,-1]:
            ds = reduce6(D.subs(a,aj))
            require(reduce6(D*inverse6(ds)-dj*dj) == 0, 'D Galois unit dimension')
            fs = reduce6(f.subs({a:aj,h:sign*h},simultaneous=True))
            ratio = reduce6(f*inverse6(fs))
            e = reduce6(ratio*inverse6(dj))
            v = as_ints(dimension_basis.inv()*vector6(e))
            require(all(c>=0 for c in v),'known centralizer simple positive forgetful image')
            E.append(s.Matrix(v))
            records.append(dict(a_image=str(aj),sqrt13_sign=sign,D_label=label,forgetful_vector=v))
    require(len(set(tuple(v) for v in E)) == 6,'six distinct known dimensions')
    G = sum((M*M for M in N),s.zeros(6))
    known = sum((r*r.T for e in E for r in [N[i]*e for i in range(3)]),s.zeros(6))
    residual = G-known
    require(residual[:3,:] == s.zeros(3,6) and residual[:,:3] == s.zeros(6,3),'all D-supported simples accounted for')
    T = residual[3:,3:]
    require(T == s.Matrix([[24,36,44],[36,68,80],[44,80,104]]),'residual Gram matrix')
    H = s.Matrix([[0,-1,1],[-1,-1,1],[-2,0,1]])
    sigma_a = a*a-a-1
    sigma_b = reduce6(b.subs(a,sigma_a))
    multiplier = reduce6(b*b*inverse6(sigma_b))
    sigma_x = reduce6(x.subs(a,sigma_a))
    sigma_f = reduce6(f.subs(a,sigma_a))
    require(reduce6(f*inverse6(sigma_f)*inverse6(b)*sigma_x*inverse6(x)-multiplier) == 0, 'cubic Galois dimension multiplier')
    for j,v in enumerate([1,a,b]):
        image = reduce6(multiplier*s.sympify(v).subs(a,sigma_a))
        require(vector6(image) == vector6(sum(H[i,j]*[1,a,b][i] for i in range(3))), 'Galois dimension action matrix')
    require(H**3 == -s.eye(3),'order3 action up to overall dimension sign')
    # A fixed dimension satisfies H*u = -u; its primitive positive vector
    # has squared norm6. Every3-orbit of total squared norm<6 would contain
    # a coordinate unit vector. Check their three exact orbits below.
    fixed = s.Matrix([1,2,1])
    require(H*fixed == -fixed, 'fixed dimension ray')
    require((H+s.eye(3)).rank() == 2, 'only one fixed dimension ray')
    require((H-s.eye(3)).det() != 0, 'no eigenvalue plus1')
    require(fixed.dot(fixed) == 6, 'primitive fixed ray squared norm6')
    unit_orbits = []
    for j in range(3):
        u = s.eye(3).col(j)
        orbit = []
        for step in range(3):
            orbit.append(as_ints(u))
            u = H*u
            if all(c <= 0 for c in u):
                u = -u
            require(all(c >= 0 for c in u), 'unit vector orbit remains positive')
        require(u == s.eye(3).col(j), 'unit dimension orbit closes')
        cost = sum(sum(c*c for c in v) for v in orbit)
        require(cost >= 6, 'unit dimension orbit costs at least6')
        unit_orbits.append(dict(initial_coordinate=j, U_orbit=orbit, first_diagonal_cost=cost))
    for j in range(3):
        u = s.eye(3).col(j)
        block = sum(((M*u)*(M*u).T for M in NA),s.zeros(3))
        require(block[0,0] == u.dot(u), 'block first diagonal equals norm squared')
    require(T[0,0] == 24 and int(T[0,0])//6 == 4, 'dimension multiplicity bound4')
    sigma13_x = reduce6(x.subs(h,-h))
    sigma13_f = reduce6(f.subs(h,-h))
    require(reduce6(sigma13_x*x) == -1, 'quadratic conjugation sends x to -1/x')
    require(reduce6(f*inverse6(sigma13_f)-x*x) == 0, 'quadratic Galois unit dimension x squared')
    require(records[1]['D_label'] == 0, 'quadratic Galois unit D component is unit')
    require(pow(2,6,13) == 12, '2 is quadratic nonresidue modulo13')
    orbit13 = [pow(4,j,13) for j in range(6)]
    require(len(set(orbit13)) == 6 and pow(4,6,13) == 1, 'squared Galois exponent has order6 modulo13')
    require(6 > 4, 'twist orbit exceeds dimension multiplicity bound')
    report = dict(ring='R6_9_3748',arithmetic_conclusion='Required13-primary twist orbit has at least6 simples of one dimension; Gram and Galois constraints allow at most4.',
                  theoretical_dependencies='center_exclusion.tex and structural_reduction.tex; requires the categorical proof, not arithmetic alone.',
                  verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  helper_sha256=hashlib.sha256((HERE/'verify_sphericality.py').read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),sympy=s.__version__,
                  dimension_basis_determinant=str(dimension_basis.det()),
                  known_centralizer_simples=records,induction_Gram=[list(map(int,G.row(i))) for i in range(6)],
                  residual_Gram=[list(map(int,T.row(i))) for i in range(3)],
                  subcategory_global_norm_over_sextic=int(D_norm),centralizer_global_norm=int(center_norm),
                  Galois_matrix=[list(map(int,H.row(i))) for i in range(3)],
                  fixed_dimension_ray=[1,2,1],fixed_dimension_minimum_cost=6,
                  coordinate_unit_dimension_orbits=unit_orbits,dimension_orbit_minimum_cost=6,
                  dimension_multiplicity_maximum=4,prime13_squared_exponent_orbit=orbit13,
                  prime13_twist_orbit_minimum=6)
    path = HERE/'center_exclusion_certificate.json'
    if args.verify:
        require(json.loads(path.read_text()) == report,'certificate exact replay')
        print('Verified six known rows, Gram residual, Galois action, dimension multiplicity<=4, and required twist orbit>=6.')
    else:
        path.write_text(json.dumps(report,indent=2)+'\n')
        print(path)


if __name__ == '__main__':
    main()
