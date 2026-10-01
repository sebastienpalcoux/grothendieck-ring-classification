#!/usr/bin/env python3
"""Exact general exclusion of R(8), independent of bounded signed search.

Use verify_bundle.py to check the frozen tensor and certificate.
The new mathematical bridge is explained in gauss8200_proof.tex.
"""
import hashlib
import itertools as it
import json
import math

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(R):
    return hashlib.sha256(json.dumps(R,separators=(',', ':')).encode()).hexdigest()

def saturated_signs(R):
    # The proof normalizes every repeated-index triple, using only saturated
    # associativity and positivity of N_iik. This is NOT an indicator gauge.
    n=len(R)
    require(all(R[i][i][k]>0 for i in range(1,n) for k in range(1,n)),
            'the proved repeated-index sign gauge does not apply')
    triples=list(it.combinations(range(1,n),3))
    pairs=list(it.combinations(range(1,n),2))
    entries=list(it.combinations(range(n),2))
    survivors=[]
    for signs in it.product((-1,1),repeat=len(triples)):
        T=[[row[:] for row in mat] for mat in R]
        for tri, sign in zip(triples, signs):
            for i,j,k in it.permutations(tri):
                T[i][j][k] *= sign
        # The matrices are symmetric. Their commutators are skew symmetric,
        # so the following upper triangles are the entire associativity test.
        if all(sum(T[i][a][l]*T[j][l][b]-T[j][a][l]*T[i][l][b]
                   for l in range(n))==0
               for i,j in pairs for a,b in entries):
            survivors.append(list(signs))
    return {'gauge':'repeated-index associativity saturation',
            'indicator_restrictions':False,
            'normalized_repeated_triples':math.comb(n+1,3)-len(triples),
            'free_distinct_triples':[list(t) for t in triples],
            'complete_assignments_checked':2**len(triples),
            'surviving_signs':survivors}

def certificate(R):
    import sympy as s
    from common import validate,permute,casimir
    from gauss_family import identify,check_characters,certificate as gauss_certificate
    from common import arithmetic

    validate(R)
    found=identify(R)
    require(found is not None and found[0]==8,'not the parameter-eight family tensor')
    m,p=found
    N=permute(R,p)
    G=check_characters(N,m)
    t=s.Symbol('t')
    cp=G.charpoly(t).as_poly()
    cp2=s.Poly(cp.as_expr(),t, modulus=2)
    expected=s.Poly(t**2*(t+1)**4,t,modulus=2)
    require(cp2==expected,'Casimir zero multiplicity at two is not two')
    q=401
    require(s.isprime(q) and q%8==1,'the dimension field does not split at two')
    D=4010+200*s.sqrt(q)
    require(s.simplify(D-(5*(25*m*m+4)+25*m*s.sqrt(25*m*m+4))/2)==0,
            'incorrect original codegree')
    require(s.minpoly(D/2,t)==t*t-4010*t+10025,
            'D/2 was not verified integral')
    chars=[]
    for tail in it.product((0,1),repeat=5):
        d=(1,)+tail
        if all((d[i]*d[j]-sum(N[i][j][k]*d[k] for k in range(6)))%2==0
               for i,j in it.product(range(6),repeat=2)):
            chars.append(list(d))
    require(chars==[[1,0,0,1,0,0]],'nonunique F2 character')
    require(sum(x*x for x in chars[0])==2,'unexpected sum of residue squares')
    # O_E=Z[omega], omega^2-omega-100=0. Modulo two its two projections
    # are the only two residue maps, both forcing this same F2 character.
    require(s.discriminant(t*t-t-100,t)==q,'incorrect maximal-order basis')
    arith=arithmetic(N)
    require(arith is not None,'trace-ideal arithmetic inapplicable')
    trace_multiple=math.lcm(arith['dimension_trace_multiple'],4)
    T=int(s.trace(G))
    budget=T-trace_multiple
    require(trace_multiple==8020 and T==8040 and budget==20,
            'incorrect strengthened trace arithmetic')
    require(0<=budget<arith['minimum_positive_magnitude_deficit']==28,
            'magnitude saturation failed')
    signs=saturated_signs(N)
    require(signs['surviving_signs']==[[1]*10], 'nongauge saturated signed tensor survives')
    # check_characters above verifies the complete explicit character table,
    # including its nonzero determinant and every multiplication identity.
    # Its final four rows have zeros; its first two are the FP Galois orbit.
    orig={'complete_character_table_checked':True,
          'FP_orbit_rows':[0,1],
          'zero_dimensions_by_character_row':{'2':[4,5],'3':[4,5],'4':[1,2],'5':[1,2]}}
    pseudo=gauss_certificate(N)
    require(pseudo is not None,'PU Gauss certificate missing')
    require(pseudo['uniform_root_count']==770 and pseudo['Gauss']['minimum_root_count']=='3200',
            'incorrect final all-orders Gauss gap')
    return {'kind':'quadratic_gauss_even_codegree_parity_exclusion',
            'scope':'general_complex_fusion_categories',
            'tensor_sha256':digest(R),'family_parameter':m,'permutation':p,
            'canonical_tensor_sha256':digest(N),
            'Casimir_polynomial':[int(x) for x in cp.all_coeffs()],
            'Casimir_polynomial_mod2':[int(x)%2 for x in cp.all_coeffs()],
            'zero_primary_rank_mod2':2,
            'original_codegree_half_minpoly':[1,-4010,10025],
            'dimension_field':{'radicand':q,'degree':2,'integral_basis_polynomial':[1,-1,-100],
                               'split_at_two':True},
            'F2_characters':chars,'dimension_square_sum_mod4':[2,0],
            'dimension_trace_divisible_by':4,'original_trace_ideal':arith,
            'strengthened_dimension_trace_multiple':trace_multiple,
            'signed_Casimir_deficit_budget':budget,
            'signed_saturation':signs,'original_characters':orig,
            'pseudo_unitary_exclusion':pseudo,
            'claim':'No complex fusion category has this Grothendieck ring.'}

def verify(R,c):
    require(certificate(R)==c,'complete tensor-based certificate does not match')
    return True

