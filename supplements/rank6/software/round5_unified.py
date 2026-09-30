"""Exact simultaneous low-word coefficient domains.

This module constructs necessary conditions.  A feasible output is not a
fusion ring, modular datum, or categorification.  A bounded search that does
not finish has ``complete=False`` and must never be used as an exclusion.

The same bounded-image enumeration applies to restriction-word Gram matrices
and to the vectorized action matrices in the full Morita Gram criterion.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
import math
import time

import sympy as s


def _gram_lll(gram, *, max_steps=100_000):
    """Exact integral basis reduction for a positive definite rational Gram."""
    H = [[Fraction(x) for x in row] for row in gram]
    n = len(H)
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    def gs():
        mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        norm = [Fraction(0) for _ in range(n)]
        for i in range(n):
            for j in range(i):
                mu[i][j] = (H[i][j]-sum(mu[i][k]*mu[j][k]*norm[k]
                                        for k in range(j)))/norm[j]
            norm[i] = H[i][i]-sum(mu[i][k]**2*norm[k] for k in range(i))
            if norm[i] <= 0:
                raise ArithmeticError('Gram matrix is not positive definite on its image')
        return mu, norm
    mu, norm = gs()
    k, steps = 1, 0
    while k < n:
        steps += 1
        if steps > max_steps:
            raise TimeoutError('exact Gram-LLL step budget')
        for j in range(k-1, -1, -1):
            q = math.floor(mu[k][j]+Fraction(1,2))
            if not q:
                continue
            old = H[k][:]
            diagonal = H[k][k]-2*q*H[k][j]+q*q*H[j][j]
            for i in range(n):
                if i != k:
                    H[k][i] = H[i][k] = old[i]-q*H[j][i]
            H[k][k] = diagonal
            U[k] = [a-q*b for a,b in zip(U[k],U[j])]
            mu, norm = gs()
        if norm[k] >= (Fraction(3,4)-mu[k][k-1]**2)*norm[k-1]:
            k += 1
        else:
            H[k], H[k-1] = H[k-1], H[k]
            for row in H:
                row[k], row[k-1] = row[k-1], row[k]
            U[k], U[k-1] = U[k-1], U[k]
            mu, norm = gs()
            k = max(1,k-1)
    return H,U,mu,norm


def enumerate_gram_ellipsoid(gram, upper_bounds=None, *, node_limit=5_000_000,
                             time_limit=60):
    """Enumerate every possible integral rank-one summand of a Gram matrix.

    Uses the stronger Loewner inequality G-xx^t >= 0, rational Gram-LLL and
    exact LDL ellipsoid enumeration. This never uses floating eigenvalues.
    """
    started = time.monotonic()
    G = s.Matrix(gram)
    if G.rows != G.cols or G != G.T or any(not x.is_Integer for x in G):
        raise ValueError('symmetric integral Gram matrix required')
    n = G.rows
    base = dict(dimension=n, optimizer_used=False, complete=True, nodes=0,
                method='exact_Loewner_ellipsoid')
    if any(x < 0 for x in G):
        return dict(base, candidates=[], reason='negative_Gram_entry')
    bounds = [math.isqrt(int(G[i,i])) for i in range(n)]
    if upper_bounds is not None:
        if len(upper_bounds) != n or any(type(x) is not int for x in upper_bounds):
            raise ValueError('one integral upper bound per coordinate required')
        bounds = [min(a,b) for a,b in zip(bounds,upper_bounds)]
    if any(b < 0 for b in bounds):
        return dict(base, candidates=[], reason='negative_coefficient_bound')
    _, piv = G.rref()
    r = len(piv)
    if not r:
        return dict(base, rank=0, bounds=bounds, candidates=[[0]*n])
    H = G[list(piv),list(piv)]
    E = G[:,list(piv)]*H.inv()
    try:
        reduced,U,mu,norm = _gram_lll(H.tolist())
    except ArithmeticError as exc:
        return dict(base, rank=r, candidates=[], reason=str(exc))
    except TimeoutError as exc:
        return dict(base, rank=r, candidates=[], complete=False, budget_reason=str(exc))
    U = s.Matrix(U)
    if abs(U.det()) != 1 or U*H*U.T != s.Matrix(reduced):
        raise RuntimeError('integral Gram reduction integrity failure')
    M = E*U.inv()
    den, coef = [],[]
    for i in range(n):
        row = [Fraction(M[i,j]) for j in range(r)]
        d = math.lcm(*(z.denominator for z in row))
        den.append(d);coef.append([int(z*d) for z in row])
    z_bounds = [math.isqrt(int(reduced[j][j])) for j in range(r)]
    remaining_bound = [[0]*n for _ in range(r+1)]
    for k in range(r-1,-1,-1):
        for i in range(n):
            remaining_bound[k][i] = remaining_bound[k+1][i]+abs(coef[i][k])*z_bounds[k]
    out,nodes,complete=[],0,True
    class Budget(Exception):
        pass
    def dfs(k,remaining,orthogonal,current):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 512 == 1 and
                time.monotonic()-started > time_limit):
            raise Budget()
        if any(v+remaining_bound[k][i] < 0 or
               v-remaining_bound[k][i] > den[i]*bounds[i]
               for i,v in enumerate(current)):
            return
        if k == r:
            if any(v % den[i] for i,v in enumerate(current)):
                return
            x=[v//den[i] for i,v in enumerate(current)]
            if all(x[i]*x[j] <= G[i,j] for i in range(n) for j in range(i,n)):
                out.append(x)
            return
        # reduced = L diag(norm) L^t, L[k,j]=mu[k,j].
        center=sum(mu[k][j]*orthogonal[j] for j in range(k))
        radius2=norm[k]*remaining
        a,b=center.numerator,center.denominator
        radius_integer=math.isqrt((radius2.numerator*b*b)//radius2.denominator)
        low=max(-z_bounds[k],-((-(a-radius_integer))//b))
        high=min(z_bounds[k],(a+radius_integer)//b)
        for z in range(low,high+1):
            coordinate=Fraction(z)-center
            next_remaining=remaining-coordinate*coordinate/norm[k]
            if next_remaining < 0:
                raise RuntimeError('exact ellipsoid bound integrity failure')
            dfs(k+1,next_remaining,orthogonal+[coordinate],
                [v+coef[i][k]*z for i,v in enumerate(current)])
    try:
        dfs(0,Fraction(1),[],[0]*n)
    except Budget:
        complete=False
    out.sort()
    return dict(base, complete=complete,nodes=nodes,rank=r,bounds=bounds,
                candidates=out, reduced_diagonal=[str(reduced[i][i]) for i in range(r)],
                budget_reason=None if complete else 'node_or_time_budget')


def enumerate_gram_columns(gram, upper_bounds=None, *, node_limit=5_000_000,
                           time_limit=60):
    """Enumerate nonnegative integral x in im_Q(gram), with xx^t <= gram.

    The inequality is componentwise.  ``upper_bounds`` are additional exact
    coordinate bounds.  Zero is retained: a central simple may occur in none
    of the selected words.  No numerical arithmetic or optimizer is used.
    """
    started = time.monotonic()
    G = s.Matrix(gram)
    if G.rows != G.cols or G != G.T:
        raise ValueError('Gram matrix must be symmetric and square')
    if any(not x.is_Integer for x in G):
        raise ValueError('Gram matrix must be integral')
    n = G.rows
    base = dict(dimension=n, optimizer_used=False, complete=True, nodes=0)
    if any(x < 0 for x in G):
        return dict(base, candidates=[], reason='negative_Gram_entry')
    bounds = [math.isqrt(int(G[i, i])) for i in range(n)]
    if upper_bounds is not None:
        if len(upper_bounds) != n or any(type(x) is not int for x in upper_bounds):
            raise ValueError('one integral upper bound per coordinate required')
        bounds = [min(a, b) for a, b in zip(bounds, upper_bounds)]
    if any(b < 0 for b in bounds):
        return dict(base, candidates=[], reason='negative_coefficient_bound')
    # Select independent ACTUAL coordinates, smallest boxes first.  Thus all
    # free coordinates inherit genuine integral bounds without lattice gaps.
    _, independent_columns = G.rref()
    B = G[:, independent_columns]
    rank = len(independent_columns)
    if not rank:
        return dict(base, rank=0, free_coordinates=[], bounds=bounds,
                    candidates=[[0]*n])
    selected = []
    for i in sorted(range(n), key=lambda j: (bounds[j], j)):
        if B[selected+[i], :].rank() > len(selected):
            selected.append(i)
        if len(selected) == rank:
            break
    E = B * B[selected, :].inv()
    den, coeff = [], []
    for i in range(n):
        row = [Fraction(E[i, j]) for j in range(rank)]
        d = math.lcm(*(z.denominator for z in row))
        den.append(d)
        coeff.append([int(z*d) for z in row])
    free_bounds = [bounds[i] for i in selected]
    minimum = [[0]*n for _ in range(rank+1)]
    maximum = [[0]*n for _ in range(rank+1)]
    for k in range(rank-1, -1, -1):
        for i in range(n):
            c = coeff[i][k]*free_bounds[k]
            minimum[k][i] = minimum[k+1][i] + min(0, c)
            maximum[k][i] = maximum[k+1][i] + max(0, c)
    out, nodes, complete = [], 0, True
    class Budget(Exception):
        pass
    def dfs(k, current):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 512 == 1 and
                time.monotonic()-started > time_limit):
            raise Budget()
        if any(v+maximum[k][i] < 0 or
               v+minimum[k][i] > den[i]*bounds[i]
               for i, v in enumerate(current)):
            return
        if k == rank:
            if any(v % den[i] for i, v in enumerate(current)):
                return
            x = [v//den[i] for i, v in enumerate(current)]
            if all(x[i]*x[j] <= G[i,j]
                   for i in range(n) for j in range(i,n)):
                out.append(x)
            return
        for v in range(free_bounds[k]+1):
            dfs(k+1, [a+coeff[i][k]*v for i, a in enumerate(current)])
    try:
        dfs(0, [0]*n)
    except Budget:
        complete = False
    out.sort()
    return dict(base, complete=complete, nodes=nodes, rank=rank,
                free_coordinates=selected, free_bounds=free_bounds,
                bounds=bounds, candidates=out,
                budget_reason=None if complete else 'node_or_time_budget')


def low_word_data(R, data, low_columns, high_columns, multiplicities,
                  labelling, words=None, spectrum=None):
    """Compute exact residual Gram and restriction data of chosen low words.

    ``data`` is the ordinary ``round3_m4.data_for`` dictionary with keys C,
    F and tab. High columns omit their leading zero unit coordinate.
    Words are tuples of indices of low central simples (default: all
    unordered pairs of nonunit low simples). Complex duals are preserved.
    """
    from exact import evaluate
    from spectral_induction import Spectrum
    C, tab = data['C'], data['tab']
    n = len(R)
    low = list(map(tuple, low_columns))
    V = [tuple(v) for v in high_columns]
    if len(V) != len(multiplicities):
        raise ValueError('multiplicity/column mismatch')
    if any(type(x) is not int or x < 0 for x in multiplicities):
        raise ValueError('integral nonnegative profile required')
    sp = spectrum or Spectrum(tab, low, [(v, None) for v in V])
    types = dict(zip(sp.vectors, sp.types))
    counts = Counter(low)
    counts.update({(0,)+v: ct for v, ct in zip(V, multiplicities) if ct})
    weights = {v: C(ct)*tab.dims[v]**2/tab.D**2 for v,ct in counts.items()}
    conjugate = lambda z: evaluate(z.to_list(), C.unit**(data['F']-1), C)
    star = [labelling.index(tab.rows.index(tuple(conjugate(x) for x in
                        tab.rows[labelling[a]]))) for a in range(len(low))]
    words = list(words if words is not None else
                 combinations_with_replacement(range(1, len(low)), 2))
    cache = {}
    def moment(word):
        key = tuple(sorted(word))
        if key not in cache:
            z = C.zero
            for v, weight in weights.items():
                term = weight
                for a in key:
                    term *= types[v][labelling[a]]
                z += term
            coeff = z.to_list()
            if len(coeff) > 1 or (coeff and coeff[0].denominator != 1):
                raise ArithmeticError('nonintegral word moment '+str(key)+': '+str(z))
            value = int(coeff[0]) if coeff else 0
            if value < 0:
                raise ArithmeticError('negative word moment '+str(key)+': '+str(value))
            cache[key] = value
        return cache[key]
    known = [[moment(tuple(word)+(star[a],)) for a in range(len(low))]
             for word in words]
    G = [[moment(tuple(star[a] for a in wi)+tuple(wj)) -
          sum(x*y for x,y in zip(known[i], known[j]))
          for j,wj in enumerate(words)] for i,wi in enumerate(words)]
    restriction = []
    for k, word in enumerate(words):
        product = [1]+[0]*(n-1)
        for a in word:
            product = [sum(product[i]*low[a][j]*R[i][j][t]
                           for i in range(n) for j in range(n)) for t in range(n)]
        restriction.append([product[t]-sum(known[k][a]*low[a][t]
                            for a in range(len(low))) for t in range(n)])
    return dict(words=[list(w) for w in words], low_duality=star,
                low_coefficients=known, gram=G, restriction=restriction,
                high_columns=[list(v) for v in V], multiplicities=list(multiplicities))


def coefficient_domains(word_data, *, node_limit=5_000_000, time_limit=60,
                        ellipsoid=True):
    """Compute complete per-restriction possible simultaneous coefficients."""
    G, restriction = word_data['gram'], word_data['restriction']
    if any(x < 0 for row in restriction for x in row):
        return dict(complete=True, impossible=True,
                    reason='negative_restriction_remainder', domains=[])
    if any(x < 0 for row in G for x in row):
        return dict(complete=True, impossible=True,
                    reason='negative_Gram_entry', domains=[])
    cache, domains = {}, []
    for v, count in zip(word_data['high_columns'], word_data['multiplicities']):
        if not count:
            continue
        vector = [0]+v
        bounds = tuple(min(row[i]//x for i,x in enumerate(vector) if x)
                       for row in restriction)
        if bounds not in cache:
            enumerator = enumerate_gram_ellipsoid if ellipsoid else enumerate_gram_columns
            cache[bounds] = enumerator(
                G, list(bounds), node_limit=node_limit, time_limit=time_limit)
        domains.append(dict(column=vector, count=count, domain=cache[bounds]))
    return dict(complete=all(d['domain']['complete'] for d in domains),
                impossible=any(d['domain']['complete'] and not d['domain']['candidates']
                               for d in domains), domains=domains)


def enumerate_fixed_gram_block(restriction_gram, mixed, word_gram, fixed,
                               upper_bounds=None, *, node_limit=5_000_000,
                               time_limit=60):
    """Exact rank-one domains of the joint Gram with restriction v fixed.

    The joint Gram is [[Q,B^t],[B,G]], and a possible column is (v,x).
    Its Schur complement gives an affine ellipsoid in usually many fewer
    actual x coordinates. A prefix is pruned only by exact necessary bounds.
    """
    started=time.monotonic()
    Q,B,G=s.Matrix(restriction_gram),s.Matrix(mixed),s.Matrix(word_gram)
    v=s.Matrix(fixed)
    n=G.rows
    base=dict(complete=True,optimizer_used=False,nodes=0,
              method='joint_Gram_fixed_restriction_Schur')
    if Q != Q.T or G != G.T or B.rows != n or B.cols != Q.rows or v.rows != Q.rows:
        raise ValueError('inconsistent joint Gram block sizes')
    if any(x < 0 for M in [Q,B,G] for x in M):
        return dict(base,candidates=[],reason='negative_joint_Gram_entry')
    bounds=[math.isqrt(int(G[i,i])) for i in range(n)]
    if upper_bounds is not None:
        bounds=[min(a,int(b)) for a,b in zip(bounds,upper_bounds)]
    _,piv=Q.rref()
    p=list(piv)
    if not p:
        if any(v) or any(B):
            return dict(base,candidates=[],reason='zero_restriction_Gram_inconsistent')
        return enumerate_gram_ellipsoid(G.tolist(),bounds,node_limit=node_limit,time_limit=time_limit)
    inv=Q[p,p].inv()
    if Q[:,p]*inv*v[p,:] != v or Q[:,p]*inv*B[:,p].T != B.T:
        return dict(base,candidates=[],reason='restriction_image_inconsistent')
    center=B[:,p]*inv*v[p,:]
    C=G-B[:,p]*inv*B[:,p].T
    radius=Fraction(1-(v[p,:].T*inv*v[p,:])[0])
    if radius < 0:
        return dict(base,candidates=[],reason='fixed_column_violates_Loewner')
    # Nonnegativity of each mixed entry gives the familiar restriction bound.
    for i in range(n):
        bounds[i]=min([bounds[i]]+[int(B[i,j])//int(v[j])
                                  for j in range(len(fixed)) if v[j] > 0])
    _,col=C.rref()
    rank=len(col)
    if not rank:
        x=[Fraction(z) for z in center]
        good=all(z.denominator==1 and 0<=z<=bounds[i] for i,z in enumerate(x))
        good=good and all(x[i]*x[j]<=G[i,j] for i in range(n) for j in range(i,n))
        return dict(base,rank=0,bounds=bounds,candidates=[[int(z) for z in x]] if good else [],
                    reason=None if good else 'forced_nonintegral_or_negative_coefficients')
    selected=[]
    image=C[:,col]
    for i in sorted(range(n),key=lambda j:(bounds[j],j)):
        if image[selected+[i],:].rank() > len(selected):
            selected.append(i)
        if len(selected)==rank:
            break
    H=C[selected,selected]
    try:
        # Exact positivity of all leading principal minors is sufficient here.
        determinants=[H[:k,:k].det() for k in range(1,rank+1)]
        if any(d<=0 for d in determinants):
            return dict(base,rank=rank,candidates=[],reason='nonpositive_Schur_Gram')
        inverse=[None]+[H[:k,:k].inv() for k in range(1,rank+1)]
    except Exception as exc:
        raise ArithmeticError('failed exact Schur image positivity check') from exc
    E=C[:,selected]*H.inv()
    const=center-E*center[selected,:]
    den,coef,initial=[],[],[]
    for i in range(n):
        values=[Fraction(const[i])]+[Fraction(E[i,j]) for j in range(rank)]
        d=math.lcm(*(z.denominator for z in values))
        den.append(d);initial.append(int(values[0]*d));coef.append([int(z*d) for z in values[1:]])
    free_bounds=[bounds[i] for i in selected]
    lower=[[0]*n for _ in range(rank+1)]
    upper=[[0]*n for _ in range(rank+1)]
    for k in range(rank-1,-1,-1):
        for i in range(n):
            z=coef[i][k]*free_bounds[k]
            lower[k][i]=lower[k+1][i]+min(0,z)
            upper[k][i]=upper[k+1][i]+max(0,z)
    center_free=[Fraction(center[i]) for i in selected]
    inverses=[None]+[[[Fraction(x) for x in row] for row in inverse[k].tolist()]
                     for k in range(1,rank+1)]
    nodes,complete,out=0,True,[]
    class Budget(Exception):
        pass
    def dfs(k,free,current):
        nonlocal nodes
        nodes+=1
        if nodes>node_limit or (nodes%512==1 and time.monotonic()-started>time_limit):
            raise Budget()
        if any(z+upper[k][i]<0 or z+lower[k][i]>den[i]*bounds[i]
               for i,z in enumerate(current)):
            return
        if k:
            shifted=[Fraction(free[j])-center_free[j] for j in range(k)]
            qi=inverses[k]
            value=sum(shifted[i]*qi[i][j]*shifted[j] for i in range(k) for j in range(k))
            if value>radius:
                return
        if k==rank:
            if any(z%den[i] for i,z in enumerate(current)):
                return
            x=[z//den[i] for i,z in enumerate(current)]
            if all(x[i]*x[j]<=G[i,j] for i in range(n) for j in range(i,n)):
                out.append(x)
            return
        for value in range(free_bounds[k]+1):
            if any(value*free[j]>G[selected[k],selected[j]] for j in range(k)):
                continue
            dfs(k+1,free+[value],[z+coef[i][k]*value for i,z in enumerate(current)])
    try:
        dfs(0,[],initial)
    except Budget:
        complete=False
    out.sort()
    return dict(base,rank=rank,nodes=nodes,complete=complete,bounds=bounds,
                free_coordinates=selected,free_bounds=free_bounds,
                candidates=out,budget_reason=None if complete else 'node_or_time_budget')


def joint_coefficient_domains(word_data, *, node_limit=5_000_000, time_limit=60):
    """Whole restriction/word Gram domain, conditioned on each known column."""
    V=word_data['high_columns'];counts=word_data['multiplicities']
    G=word_data['gram'];B=[row[1:] for row in word_data['restriction']]
    if any(x<0 for row in word_data['restriction'] for x in row):
        return dict(complete=True,impossible=True,reason='negative_restriction_remainder',domains=[])
    d=len(V[0]) if V else 0
    Q=[[sum(m*v[i]*v[j] for v,m in zip(V,counts)) for j in range(d)] for i in range(d)]
    domains=[]
    for v,m in zip(V,counts):
        if not m:
            continue
        domain=enumerate_fixed_gram_block(Q,B,G,v,node_limit=node_limit,time_limit=time_limit)
        domains.append(dict(column=[0]+list(v),count=m,domain=domain))
    return dict(complete=all(z['domain']['complete'] for z in domains),
                impossible=any(z['domain']['complete'] and not z['domain']['candidates'] for z in domains),
                restriction_gram=Q,domains=domains)


def count_system(word_data, domains):
    """Return sparse integer equations for the enumerated Gram columns.

    Only complete domains may be used. The equations simultaneously enforce
    type counts, all Gram entries and restriction of every selected word.
    The zero vector appears in each type's count equation as it must.
    """
    if not domains['complete']:
        raise ValueError('incomplete domains cannot define an exclusion system')
    labels = [(tuple(d['column']), tuple(x)) for d in domains['domains']
              for x in d['domain']['candidates']]
    rows, rhs, descriptions = [], [], []
    def add(coef, b, description):
        row = {j:c for j,c in enumerate(coef) if c}
        if row or b:
            rows.append(row); rhs.append(int(b)); descriptions.append(description)
    for d in domains['domains']:
        v = tuple(d['column'])
        add([int(w == v) for w,x in labels], d['count'], ['count', list(v)])
    G = word_data['gram']
    for i in range(len(G)):
        for j in range(i,len(G)):
            add([x[i]*x[j] for v,x in labels], G[i][j], ['Gram',i,j])
    for i, product in enumerate(word_data['restriction']):
        for k, value in enumerate(product):
            add([x[i]*v[k] for v,x in labels], value, ['restriction',i,k])
    return dict(rows=rows, rhs=rhs, descriptions=descriptions,
                labels=[[list(v),list(x)] for v,x in labels],
                integral_variables=list(range(len(labels))),
                categorification_claimed=False)
