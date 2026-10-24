#!/usr/bin/env python3
"""Exact paired-module helpers extracted unchanged from the published verifier.

Source: evidence/rank8_research_20261022/r982/module_types.py
Repository: grothendieck-ring-classification
Published commit: 323c4227ffb796a72eef506f1eb289437fbc95db
Source file SHA256: b64883e6099cb8938dc6d14eaeef018ee0e75f23817a951eb80b276a260eac10

The five function bodies below are byte-identical source excerpts. This
module makes no categorification or module-associator existence claim.
"""
import itertools
import math
import sympy as s

def gram(R,a):
    return s.Matrix([[sum(a[k]*R[j][k][i]for k in range(8))
                      for j in range(8)]for i in range(8)])

def vectors(norm,signed=False):
    b=math.isqrt(norm)
    return [v for v in itertools.product(range(-b if signed else 0,b+1),repeat=3)
            if sum(x*x for x in v)==norm]

def three_column_factors(H,signed=False):
    """All integral 3-by-3 Gram factors; positive columns modulo permutation."""
    V=[vectors(H[i][i],signed)for i in range(3)]
    out=set()
    for a in V[0]:
        # Positive column permutations are exhausted by sorting the first row.
        if not signed and a!=tuple(sorted(a)):continue
        for b in V[1]:
            if sum(x*y for x,y in zip(a,b))!=H[0][1]:continue
            for c in V[2]:
                if sum(x*y for x,y in zip(a,c))!=H[0][2]:continue
                if sum(x*y for x,y in zip(b,c))!=H[1][2]:continue
                cols=tuple(zip(a,b,c))
                out.add(cols if signed else tuple(sorted(cols)))
    return sorted(out)

def ends(actions):
    return [tuple(int(M[j,j])for M in actions)for j in range(8)]

def module_equivalence(A,B):
    ea,eb=ends(A),ends(B)
    domains=[[j for j in range(8)if ea[i]==eb[j]]for i in range(8)]
    for p in itertools.product(*domains):
        if len(set(p))!=8:continue
        if all(A[k][i,j]==B[k][p[i],p[j]]
               for k,i,j in itertools.product(range(8),repeat=3)):return list(p)
    return None
