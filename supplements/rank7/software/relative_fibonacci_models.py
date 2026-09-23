"""Exact relative-center reconstruction over a supplied Fibonacci subcategory.

This is a conditional categorical construction.  Existence is supplied by the
unitary parent and its Fibonacci subcategory, never by a Gram factorization alone.
The executable reconstruction uses no target tensor or census identifier.
"""
from functools import lru_cache
import itertools
import sympy as s
from exact import require
from oriented_signed import validate_general
from positive_models import tt3, rank2, product
from rings import dual


def forced_gram_columns(B):
    """Recover all remaining nonnegative columns by diagonal-one pivots.

    A pivot with diagonal 1 occurs in exactly one nonnegative integral Gram
    column, and that column is the pivot column of B.  Failure to find a pivot
    is inconclusive, not nonexistence.  Zero residual means there are no further
    columns because a simple object's restriction is nonzero.
    """
    B=s.Matrix(B); cols=[]; pivots=[]
    require(B==B.T and all(x.is_Integer and x>=0 for x in B),'invalid Gram residual')
    while any(B):
        choices=[i for i in range(B.rows) if B[i,i]==1]
        if not choices:return None
        i=min(choices);v=B[:,i];cols.append(v);pivots.append(i);B-=v*v.T
        if any(x<0 for x in B):return None
    return cols,pivots


def reconstruct(parent,a):
    validate_general(parent)
    n=len(parent)
    require(0<a<n and parent[a][a]==[int(k==0)+int(k==a) for k in range(n)],
            'not a Fibonacci basis subring')
    left=s.Matrix(parent[a]);right=s.Matrix([parent[i][a] for i in range(n)])
    B=s.eye(n)+left*right
    e=[s.eye(n)[:,i] for i in range(n)]
    low=[e[0],e[a],e[a],e[0]+e[a]]
    rem=B-sum((v*v.T for v in low),s.zeros(n))
    factor=forced_gram_columns(rem)
    if factor is None:return None
    high,pivots=factor
    high.sort(key=lambda v:(sum(v),tuple(v)))
    columns=low+high;r=len(columns)
    F=s.Matrix.hstack(*columns)
    require(F*F.T==B,'restriction Gram identity')
    star=dual(parent)
    # Low columns are the known, individually self-dual simples of Z(Fib).
    # A high column uniquely fixed by restriction duality forces its simple
    # object to be self-dual.  Duplicates are not silently resolved.
    if any(list(v)!=[v[star[i]] for i in range(n)] for v in high):return None
    if len({tuple(v) for v in high})!=len(high):return None
    if any(tuple(v) in {tuple(w) for w in low} for v in high):return None
    variables={t:s.Symbol('z_'+'_'.join(map(str,t)))
               for t in itertools.combinations_with_replacement(range(1,r),3)}
    N=[[[int(j==k) if i==0 else int(i==k) if j==0 else int(i==j) if k==0
         else variables[tuple(sorted((i,j,k)))] for k in range(r)]
        for j in range(r)] for i in range(r)]
    Z=product(rank2(1),rank2(1));eq=[]
    for i,j in itertools.product(range(4),repeat=2):
        for k in range(r):eq.append(N[i][j][k]-(Z[i][j][k] if k<4 else 0))
    for i,j in itertools.product(range(r),repeat=2):
        target=s.Matrix([sum(F[u,i]*F[v,j]*parent[u][v][k]
                           for u,v in itertools.product(range(n),repeat=2))
                         for k in range(n)])
        eq.extend(F*s.Matrix(N[i][j])-target)
    unknowns=list(variables.values())
    matrix,rhs=s.linear_eq_to_matrix(eq,unknowns)
    solutions=s.linsolve((matrix,rhs),unknowns)
    if len(solutions)!=1:return None
    values=next(iter(solutions))
    if any(v.free_symbols or not v.is_Integer or v<0 for v in values):return None
    assignment=dict(zip(unknowns,values))
    R=[[[int(s.sympify(x).subs(assignment)) for x in row] for row in block] for block in N]
    validate_general(R)
    data={'fibonacci_label':a,'parent_rank':n,'relative_rank':r,
          'restriction_matrix':[[int(x) for x in row] for row in F.tolist()],
          'induction_gram':[[int(x) for x in row] for row in B.tolist()],
          'diagonal_one_pivots':pivots,'symmetric_nonunit_unknowns':len(unknowns),
          'linear_equations':matrix.rows,'linear_rank':matrix.rank(),
          'unique_nonnegative_integral_solution':True}
    require(data['linear_rank']==len(unknowns),'fusion rules not uniquely determined')
    return R,data


@lru_cache(None)
def relative_tt3():
    result=reconstruct(tt3(),2)
    require(result is not None,'TT3 relative-center reconstruction failed')
    return result


def verify_controls():
    from prepare import key
    R,data=relative_tt3()
    second=reconstruct(tt3(),5)
    require(second is not None and key(R)==key(second[0]),'two Fibonacci inclusions disagree')
    control=reconstruct(rank2(1),1)
    require(control is not None and control[0]==product(rank2(1),rank2(1)),
            'relative center of Fib is not Fib x Fib')
    return {'passed':True,'tt3_inclusions':2,'fibonacci_parent_control':True,
            'relative_rank':len(R),'linear_rank':data['linear_rank']}

if __name__=='__main__':
    import json
    print(json.dumps({'construction':relative_tt3()[1],'controls':verify_controls()},indent=2))
