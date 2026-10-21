#!/usr/bin/env python3
"""Exact cocycle, stable-element, and tensor certificate for R8_3_3342.

The categorical construction and the Mackey/determinant argument are in
proof.md. Default mode replays certificate.json; --write regenerates it.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
TARGET = 'R8_3_3342'
TARGET_SHA = '964e7a672186047744b854ccf9cf3a89dd177d1efbe595f3a1fb8384d3fe238f'
OTHER_SHA = 'af42e7282350264c21616caff6aeebd8d323b04b6c727b3c6230aad9933a7cf8'
G = list(itertools.product(range(4), range(2)))
UNIT = (0, 0)
H = [a for a in G if a[0] % 2 == a[1]]
K = [a for a in G if a[0] % 2 == 0]
T = (0, 1)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()

def mul(a, b):
    return ((a[0]+(-1)**a[1]*b[0]) % 4, (a[1]+b[1]) % 2)

def linear_solve(equations, n, tracking=False):
    pivots, combinations = {}, {}
    mask = (1 << n)-1
    for number, original in enumerate(equations):
        r, combination = original, 1 << number
        while r & mask:
            p = (r & -r).bit_length()-1
            if p in pivots:
                r ^= pivots[p]
                if tracking:
                    combination ^= combinations[p]
            else:
                pivots[p] = r
                combinations[p] = combination
                break
        else:
            require(not (r >> n), 'inconsistent affine cochain equations')
    solution = 0
    for p in sorted(pivots, reverse=True):
        r = pivots[p]
        value = (r >> n) ^ ((r & solution).bit_count() % 2)
        if value:
            solution |= 1 << p
    require(all(((r & solution).bit_count() % 2) == (r >> n) for r in equations),
            'linear solution does not replay')
    return solution, pivots, combinations

def local_relative_cocycle():
    variables = [('w', a, b, c) for a, b, c in itertools.product(G[1:], repeat=3)]
    variables += [('v', a, b) for a, b in itertools.product([k for k in K if k != UNIT], repeat=2)]
    index = {v: i for i, v in enumerate(variables)}
    n = len(variables)
    equations = []
    def row(terms, rhs=0):
        value = rhs << n
        for term in terms:
            if all(g != UNIT for g in term[1:]):
                value ^= 1 << index[term]
        return value
    for a,b,c,d in itertools.product(G[1:], repeat=4):
        equations.append(row([('w',b,c,d),('w',mul(a,b),c,d),('w',a,mul(b,c),d),
                              ('w',a,b,mul(c,d)),('w',a,b,c)]))
    for a,b,c in itertools.product([h for h in H if h != UNIT], repeat=3):
        equations.append(row([('w',a,b,c)]))
    for a,b,c in itertools.product([k for k in K if k != UNIT], repeat=3):
        cubic = ((a[0]//2)*(b[0]//2)*c[1]+(a[0]//2)*b[1]*c[1]) % 2
        equations.append(row([('w',a,b,c),('v',b,c),('v',mul(a,b),c),
                              ('v',a,mul(b,c)),('v',a,b)], cubic))
    solution, pivots, combinations = linear_solve(equations, n, True)
    def omega(a,b,c):
        return 0 if UNIT in [a,b,c] else (solution >> index[('w',a,b,c)]) & 1
    def conjugate(a):
        return mul(mul(T,a),T)
    def alpha(a,b):
        # Gelaki--Naidu, Section 5.1, multiplier psi^g, with psi=1.
        # Every a,b in H=V4 is its own inverse; all values lie in F2.
        return omega(a,b,T)^omega(a,mul(b,T),conjugate(b))^omega(mul(mul(a,b),T),conjugate(b),conjugate(a))
    require(all(alpha(b,c)^alpha(mul(a,b),c)^alpha(a,mul(b,c))^alpha(a,b) == 0
                for a,b,c in itertools.product(H, repeat=3)), 'local stabilizer multiplier is not a cocycle')
    u,v=(2,0),(1,1)
    functional = row([('w',u,v,T),('w',u,mul(v,T),conjugate(v)),
                      ('w',mul(mul(u,v),T),conjugate(v),conjugate(u)),
                      ('w',v,u,T),('w',v,mul(u,T),conjugate(u)),
                      ('w',mul(mul(v,u),T),conjugate(u),conjugate(v))])
    remainder, combination = functional, 0
    while remainder & ((1 << n)-1):
        p=(remainder & -remainder).bit_length()-1
        require(p in pivots, 'commutator is not forced by the relative equations')
        remainder ^= pivots[p]
        combination ^= combinations[p]
    require(remainder == 1 << n, 'forced commutator is not negative')
    equation_indices = [i for i in range(len(equations)) if combination >> i & 1]
    witness = functional
    for i in equation_indices:
        witness ^= equations[i]
    require(witness == 1 << n, 'dual linear witness does not replay')
    require(alpha(u,v)^alpha(v,u) == 1, 'chosen local cocycle has wrong multiplier')
    values = [[[omega(a,b,c) for c in G] for b in G] for a in G]
    cert = {'D8_elements_r_power_s_power': G, 'point_fixing_V4': H, 'other_V4': K,
            'normalizing_involution': T, 'variable_count': n, 'equation_count': len(equations),
            'equation_rank': len(pivots), 'solution_bits': [solution >> i & 1 for i in range(n)],
            'normalized_D8_cocycle': values, 'relative_equations_sha256': fingerprint(equations),
            'forced_negative_commutator_dual_witness_equation_indices': equation_indices,
            'multiplier_on_point_fixing_V4': [[alpha(a,b) for b in H] for a in H]}
    return omega, cert

def permutation_multiply(a,b):
    return tuple(a[b[i]] for i in range(6))

def permutation_inverse(a):
    return tuple(a.index(i) for i in range(6))

def cycles(*items):
    p=list(range(6))
    for cy in items:
        for i,x in enumerate(cy):
            p[x]=cy[(i+1) % len(cy)]
    return tuple(p)

def stable_elements(omega):
    e=tuple(range(6))
    r=cycles((0,1,2,3),(4,5))
    s=cycles((0,2),(4,5))
    def power(a,n):
        z=e
        for _ in range(n):
            z=permutation_multiply(z,a)
        return z
    embedding={g:permutation_multiply(power(r,g[0]),power(s,g[1])) for g in G}
    inverse_embedding={v:k for k,v in embedding.items()}
    require(len(inverse_embedding) == 8, 'D8 embedding not injective')
    require(all(permutation_multiply(embedding[a],embedding[b]) == embedding[mul(a,b)]
                for a,b in itertools.product(G,repeat=2)), 'D8 embedding not a homomorphism')
    require(all(embedding[h][4] == 4 and embedding[h][5] == 5 for h in H), 'wrong V4 embedding')
    alternating=[p for p in itertools.permutations(range(6))
                 if sum(p[i]>p[j] for i in range(6) for j in range(i+1,6)) % 2 == 0]
    require(len(alternating) == 360, 'incorrect alternating group order')
    records=[]
    for g in alternating:
        gi=permutation_inverse(g)
        def conjugate(a):
            return permutation_multiply(permutation_multiply(gi,embedding[a]),g)
        E=[a for a in G if conjugate(a) in inverse_embedding]
        theta={a:inverse_embedding[conjugate(a)] for a in E}
        J=[a for a in E if a != UNIT]
        pairs=list(itertools.product(J,repeat=2))
        index={ab:i for i,ab in enumerate(pairs)}
        n=len(index)
        equations=[]
        for a,b,c in itertools.product(J,repeat=3):
            rhs=omega(a,b,c)^omega(theta[a],theta[b],theta[c])
            row=rhs << n
            for ab in [(b,c),(mul(a,b),c),(a,mul(b,c)),(a,b)]:
                if UNIT not in ab:
                    row ^= 1 << index[ab]
            equations.append(row)
        solution,_,_=linear_solve(equations,n)
        records.append({'conjugating_permutation':g,'intersection_local_indices':[G.index(a) for a in E],
                        'conjugation_image_local_indices':[G.index(theta[a]) for a in E],
                        'coboundary_two_cochain_bits':[solution >> i & 1 for i in range(n)]})
    histogram=Counter(len(x['intersection_local_indices']) for x in records)
    require(dict(histogram)=={8:8,1:256,4:32,2:64}, 'unexpected Sylow intersection counts')
    return {'A6_order':360, 'A5_point_stabilizer_order':60, 'Sylow2_order':8,
            'r_permutation':r,'s_permutation':s,
            'intersection_order_counts':[[k,histogram[k]] for k in sorted(histogram)],
            'all_conjugations':records}

def model_tensor():
    # Exact ordinary A5 characters, with classes 1,2A,3A,5A,5B.
    phi=(1+sp.sqrt(5))/2
    phibar=(1-sp.sqrt(5))/2
    chars=[[1,1,1,1,1],[3,-1,0,phi,phibar],[3,-1,0,phibar,phi],
           [4,0,1,-1,-1],[5,1,-1,0,0]]
    sizes=[1,15,20,12,12]
    require(all(sp.simplify(sum(sizes[c]*chars[i][c]*chars[j][c] for c in range(5))) ==
                60*int(i==j) for i,j in itertools.product(range(5),repeat=2)), 'A5 character orthogonality failed')
    R=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j,k in itertools.product(range(5),repeat=3):
        value=sp.simplify(sum(sizes[c]*chars[i][c]*chars[j][c]*chars[k][c] for c in range(5))/sp.Integer(60))
        require(value.is_Integer and value>=0, 'A5 character product is not nonnegative integral')
        R[i][j][k]=int(value)
    action=[[[int(i==j) for j in range(3)] for i in range(3)],
            [[1]*3 for _ in range(3)], [[1]*3 for _ in range(3)],
            [[1+int(i==j) for j in range(3)] for i in range(3)],
            [[2-int(i==j) for j in range(3)] for i in range(3)]]
    for a,i,j in itertools.product(range(5),range(3),range(3)):
        R[a][5+i][5+j]=R[5+i][a][5+j]=R[5+i][5+j][a]=action[a][i][j]
    pairs=[(i,j) for i in range(3) for j in range(i,3)]
    completions=[]
    for choices in itertools.product(range(3),repeat=6):
        if choices[0] != 0:
            continue
        N=[[[3]*3 for _ in range(3)] for _ in range(3)]
        for (i,j),k in zip(pairs,choices):
            N[i][j][k]=N[j][i][k]=2
        if all(N[i][j][k]==N[i][k][j] for i,j,k in itertools.product(range(3),repeat=3)):
            completions.append(N)
    require(len(completions)==1, 'off-sector completion is not unique')
    for i,j,k in itertools.product(range(3),repeat=3):
        R[5+i][5+j][5+k]=completions[0][i][j][k]
    dims=[1,3,3,4,5,10,10,10]
    require(all(sum(R[i][j][k]*dims[k] for k in range(8))==dims[i]*dims[j]
                for i,j in itertools.product(range(8),repeat=2)), 'model dimension character failed')
    require(all(sum(R[i][j][a]*R[a][k][b] for a in range(8))==
                sum(R[j][k][a]*R[i][a][b] for a in range(8))
                for i,j,k,b in itertools.product(range(8),repeat=4)), 'model associativity failed')
    return R, {'dimensions':dims, 'global_dimension':sum(d*d for d in dims),
               'ordinary_sector_basis':['1','3a','3b','4','5'],
               'spin_sector_basis':['rho0','rho1','rho2'],
               'neutral_sector_actions':action,'off_sector_completion_count':len(completions),
               'off_sector_tensor':completions[0],'tensor':R,'tensor_sha256':fingerprint(R)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    omega,local=local_relative_cocycle()
    stability=stable_elements(omega)
    model,model_cert=model_tensor()
    census=json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    source=next(r for r in census if r['id']==TARGET)
    other=next(r for r in census if r['id']=='R8_3_3344')
    require(fingerprint(source['tensor'])==source['tensor_sha256']==TARGET_SHA,'source tensor hash mismatch')
    require(fingerprint(other['tensor'])==other['tensor_sha256']==OTHER_SHA,'comparison tensor hash mismatch')
    mapping=[0,1,2,6,7,3,4,5]
    inverse_mapping=[mapping.index(i) for i in range(8)]
    require(all(model[i][j][k]==source['tensor'][mapping[i]][mapping[j]][mapping[k]]
                for i,j,k in itertools.product(range(8),repeat=3)), 'full source tensor match failed')
    require(all(other['tensor'][i][i][i]==3 for i in [3,4,5]), 'comparison distinction changed')
    result={'model':'C(A6,omega,A5,psi), with a stable relative mu2 cocycle',
            'scope':'unitary group-theoretical construction',
            'local_relative_cocycle':local,'global_stable_element_verification':stability,
            'constructed_fusion_tensor':model_cert,
            'match':{'id':TARGET,'tensor_sha256':TARGET_SHA,'source_line':source['source_line'],
                     'model_to_source_basis':mapping,'source_to_model_basis':inverse_mapping,
                     'verified_coefficients':512},
            'comparison':{'id':'R8_3_3344','tensor_sha256':OTHER_SHA,
                          'off_sector_square_diagonal_coefficients':[3,3,3],
                          'conclusion':'not the ring of this construction; no general exclusion asserted'}}
    destination=HERE/'certificate.json'
    if args.write:
        destination.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(json.loads(destination.read_text())==json.loads(json.dumps(result)), 'saved certificate does not replay')
    print(json.dumps({'model':TARGET,'coefficients_verified':512,'stable_conjugations':360,
                      'relative_multiplier_commutator':-1,'mode':'write' if args.write else 'compare'}))

if __name__=='__main__':
    main()
