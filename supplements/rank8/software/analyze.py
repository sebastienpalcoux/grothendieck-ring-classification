"""Rank-eight categorification audit of the pinned, complete census through m=2.

Run from anywhere: python3 software/analyze.py.  The emitted statuses are
existence of a complex fusion categorification, not counts of fusion rings.
No undecided record is declared categorifiable or impossible.
"""
from __future__ import annotations

import collections
import csv
import functools
import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOWER = ROOT / "data" / "lower_rank_positive_models.json"
RANK6 = ROOT / "data" / "rank6_positive_models.json"
RANK7_NEGATIVE = ROOT / "data" / "rank7_certified_negative_subrings.json"
SIGNED_WITNESSES = ROOT / "experimental_signed" / "certificates"
sys.path.insert(0, str(HERE))

import sympy as sy
from exact import cyclotomic_failure, t, vector
from prepare import key


def read_source():
    p = ROOT / "data" / "rank8_tables.txt.gz"
    raw = gzip.open(p, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == (
        "97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600"
    )
    rings = [json.loads(line.replace("{", "[").replace("}", "]"))
             for line in raw.decode().splitlines() if line.strip()]
    assert len(rings) == 973
    assert collections.Counter(mult(R) for R in rings) == {1: 96, 2: 877}
    return rings


def mult(R):
    return max(x for M in R for row in M for x in row)


def fp(R):
    return hashlib.sha256(json.dumps(R, separators=(",", ":")).encode()).hexdigest()


def dual(R):
    return [next(j for j in range(len(R)) if R[i][j][0]) for i in range(len(R))]


def commutes(R):
    return all(R[i][j] == R[j][i]
               for i in range(len(R)) for j in range(i))


@functools.lru_cache(None)
def canonical(serial):
    return key(json.loads(serial))


def ckey(R):
    return canonical(json.dumps(R, separators=(",", ":")))


def model_basis_map(source, model):
    """Return the full unit-preserving based isomorphism as a list of labels."""
    source_key, source_order = key(source, witness=True)
    model_key, model_order = key(model, witness=True)
    assert source_key == model_key
    result = [None] * len(source)
    for source_i, model_i in zip(source_order, model_order):
        result[source_i] = model_i
    assert result[0] == 0 and sorted(result) == list(range(len(source)))
    assert all(source[i][j][k] == model[result[i]][result[j]][result[k]]
               for i in range(len(source)) for j in range(len(source)) for k in range(len(source)))
    return result


def K3(k, l, m, n):
    return [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 1, 0], [1, m, k], [0, k, l]],
        [[0, 0, 1], [0, k, l], [1, l, n]],
    ]


def group_ring(elements, multiply):
    identity = elements[0]
    assert all(multiply(identity, x) == x == multiply(x, identity) for x in elements)
    index = {x: i for i, x in enumerate(elements)}
    n = len(elements)
    R = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i, x in enumerate(elements):
        for j, y in enumerate(elements):
            R[i][j][index[multiply(x, y)]] = 1
    return R


def product(A, B):
    a, b = len(A), len(B)
    return [[[A[i // b][j // b][k // b] * B[i % b][j % b][k % b]
              for k in range(a * b)] for j in range(a * b)] for i in range(a * b)]


def ty_c7():
    R = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i in range(7):
        for j in range(7):
            R[i][j][(i + j) % 7] = 1
        R[i][7][7] = R[7][i][7] = R[7][7][i] = 1
    return R


def dihedral_character_ring(n):
    """Rep(D_{2n}) with D_{2n} of group order 2n (n=10 or 13)."""
    assert n in (10, 13)
    # Linear characters are indexed by bits (rotation sign, reflection sign).
    l = 4 if n % 2 == 0 else 2
    kmax = n // 2 - 1 if l == 4 else (n - 1) // 2
    size = l + kmax
    assert size == 8
    R = [[[0] * size for _ in range(size)] for _ in range(size)]
    for x in range(l):
        for y in range(l):
            R[x][y][x ^ y] = 1
        for k in range(1, kmax + 1):
            rotate = (x >> 1) & 1 if l == 4 else 0
            kk = n // 2 - k if rotate else k
            R[x][l + k - 1][l + kk - 1] = 1
            R[l + k - 1][x][l + kk - 1] = 1
    for k in range(1, kmax + 1):
        for j in range(1, kmax + 1):
            for t in (k + j, abs(k - j)):
                t %= n
                if t == 0:
                    R[l + k - 1][l + j - 1][0] += 1
                    R[l + k - 1][l + j - 1][1] += 1
                elif l == 4 and t == n // 2:
                    R[l + k - 1][l + j - 1][2] += 1
                    R[l + k - 1][l + j - 1][3] += 1
                else:
                    idx = l + min(t, n - t) - 1
                    assert l <= idx < size
                    R[l + k - 1][l + j - 1][idx] += 1
    return R


def dicyclic_character_ring():
    """Irreducible character ring of Dic_5, the dicyclic group of order 20.

    The four linear characters form C4 and the other four have degree two.
    For the latter, rho_i rho_j=rho_{i+j}+rho_{|i-j|},
    rho_0=1+chi_2, rho_5=chi_1+chi_3, rho_{10-i}=rho_i.
    """
    R = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for x in range(4):
        for y in range(4):
            R[x][y][(x+y)%4]=1
        for k in range(1,5):
            kk=5-k if x%2 else k
            R[x][4+k-1][4+kk-1]=R[4+k-1][x][4+kk-1]=1
    for k in range(1,5):
        for j in range(1,5):
            for t in (k+j,abs(k-j)):
                if t==0:
                    R[4+k-1][4+j-1][0]+=1
                    R[4+k-1][4+j-1][2]+=1
                elif t==5:
                    R[4+k-1][4+j-1][1]+=1
                    R[4+k-1][4+j-1][3]+=1
                else:
                    R[4+k-1][4+j-1][4+min(t,10-t)-1]+=1
    return R


def su2_ring(level, even=False):
    """Standard level-k integrable SU(2) Verlinde multiplication."""
    labels = list(range(0, level+1, 2 if even else 1))
    assert len(labels) == 8
    R = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,a in enumerate(labels):
        for j,b in enumerate(labels):
            for h,c in enumerate(labels):
                if abs(a-b) <= c <= min(a+b,2*level-a-b) and (a+b-c)%2 == 0:
                    R[i][j][h]=1
    return R


def model_registry():
    rank2 = [
        ("Vec(C2)", [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],
         "Pointed category Vec(C2)"),
        ("Fib", [[[1, 0], [0, 1]], [[0, 1], [1, 1]]],
         "Ostrik, Fusion categories of rank 2; Fibonacci category"),
    ]
    rank3 = [("Vec(C3)", group_ring(list(range(3)), lambda i, j: (i+j) % 3),
              "Rank-three sphericality and classification, Corollary 1; pointed model")]
    for name, pars, model in [
            ("Ising", (1, 0, 0, 0), "Ising category"),
            ("Rep(S3)", (1, 0, 1, 0), "Representation category of S3"),
            ("Even(E6)", (1, 0, 2, 0), "E6 subfactor even part"),
            ("PSU(2)5", (1, 1, 1, 0), "SU(2)5 even subcategory")]:
        rank3.append((name, K3(*pars),
                      "Rank-three sphericality and classification, Corollary 1; " + model))
    rest = [(x["name"], x["tensor"], x["reference"])
            for x in json.loads(LOWER.read_text())]
    r6 = [(x["name"], x["tensor"], x["reference"])
          for x in json.loads(RANK6.read_text())]
    assert collections.Counter(len(R) for _, R, _ in rest) == {4: 15, 5: 17}
    assert len(r6) == 43 and all(len(R) == 6 and mult(R) <= 2 for _, R, _ in r6)
    reg = collections.defaultdict(dict)
    for name, R, ref in rank2 + rank3 + rest + r6:
        kk = ckey(R)
        assert kk not in reg[len(R)], ("duplicate positive registry", len(R), name)
        reg[len(R)][kk] = (name, ref)
    assert [len(reg[i]) for i in (2, 3, 4, 5, 6)] == [2, 5, 15, 17, 43]

    rank8 = collections.defaultdict(list)
    for name, A, ref in rest:
        if len(A) != 4 or mult(A) > 2:
            continue
        for nm, B, bref in rank2:
            X = product(A, B)
            if mult(X) <= 2:
                rank8[ckey(X)].append({"model": f"{name} x {nm}",
                    "reference": ref.replace("DP4 Table 1", "Rank-four Grothendieck rings through multiplicity 128 (2026), Table 1")
                                  + "; " + bref + "; Deligne tensor product", "tensor": X})
    for n in (10, 13):
        A = dihedral_character_ring(n)
        rank8[ckey(A)].append({"model": f"Rep(D_{{{2*n}}})",
            "reference": "This manuscript, Proposition 4.1 (explicit dihedral character multiplication); "
                         "Serre, Linear Representations of Finite Groups, Chapter 5",
            "tensor": A})
    A=dicyclic_character_ring()
    rank8[ckey(A)].append({"model":"Rep(Dic5)",
        "reference":"This manuscript, Proposition 4.1 (explicit dicyclic character multiplication); "
                    "Serre, Linear Representations of Finite Groups, Chapter 5",
        "tensor":A})
    A = ty_c7()
    rank8[ckey(A)].append({"model": "TY(C7)",
        "reference": "Tambara and Yamagami, Tensor categories with fusion rules of self-duality "
                     "for finite abelian groups, Journal of Algebra 209 (1998), 692--707, Theorem 1",
        "tensor": A})
    for level, even in ((7,False),(14,True),(15,True)):
        A=su2_ring(level,even)
        rank8[ckey(A)].append({
            "model": f"{'PSU' if even else 'SU'}(2)_{level}",
            "reference": "Kirillov--Ostrik, On a q-analogue of the McKay correspondence, 2002; "
                         "standard integrable SU(2) level-k category and its even subcategory",
            "tensor":A})
    appendix=json.loads((ROOT/'experimental_signed/appendix_c3_2_item3.json').read_text())
    assert appendix['claimed_FP_dimension']==20 and len(appendix['source_tensor'])==8
    for name in appendix['claimed_models']:
        rank8[ckey(appendix['source_tensor'])].append({
            'model':name,
            'reference':appendix['source'],
            'tensor':appendix['source_tensor']})
    archive=json.loads((ROOT/'experimental_signed/appendix_mle2_tensors.json').read_text())
    item6=next(x for x in archive['entries'] if x['appendix_item']==6)
    assert 'C(S4, 1, A4, 1), C(S4, 1, S3, 1)' in item6['categorification_line']
    for name in ('C(S4,1,A4,1)','C(S4,1,S3,1)'):
        rank8[ckey(item6['source_tensor'])].append({
            'model':name,
            'reference':archive['source']+'; Appendix C.3.2(6), Lemma-free group-theoretical construction',
            'tensor':item6['source_tensor']})
    item11=json.loads((ROOT/'experimental_signed/appendix_c3_2_item11.json').read_text())
    rank8[ckey(item11['source_tensor'])].append({
        'model':item11['categorification'],
        'reference':item11['source'],
        'tensor':item11['source_tensor']})
    return reg, rank8


def proper_closed_subrings(R, max_rank=6):
    n = len(R)
    d = dual(R)
    for mask in range(1, 1 << (n - 1)):
        J = (0,) + tuple(i for i in range(1, n) if mask >> (i-1) & 1)
        if len(J) == n or len(J) > max_rank:
            continue
        I = set(J)
        if any(d[i] not in I for i in J):
            continue
        if any(h not in I and R[i][j][h]
               for i in J for j in J for h in range(n)):
            continue
        S = [[[R[i][j][k] for k in J] for j in J] for i in J]
        yield J, S


def near_group_certificate(R):
    """Schopieray 2023 Proposition 3.2, in its near-group specialization."""
    d = dual(R)
    G = [i for i in range(8) if sum(R[i][d[i]]) == 1]
    if len(G) != 7 or not commutes(R):
        return None
    x = next(i for i in range(8) if i not in G)
    k = R[x][x][x]
    if 0 < k < 6 and all(R[x][x][g] == 1 for g in G) and all(
            R[x][g][x] == R[g][x][x] == 1 for g in G):
        return {"kind": "near_group", "object": x, "invertibles": G,
                "kappa": k, "criterion": "Schopieray 2023, Proposition 3.2"}
    return None


def rank2_certificate(R):
    for i in range(1, 8):
        k = R[i][i][i]
        if R[i][i][0] == 1 and k >= 2 and sum(R[i][i]) == 1 + k:
            return {"kind": "rank_two", "object": i, "kappa": k,
                    "criterion": "Rank-two complex classification, Theorem 1"}
    return None


def lower_subring_certificate(R, reg):
    for J, S in proper_closed_subrings(R):
        n, m = len(S), mult(S)
        bound = {2: 10000, 3: 10000, 4: 128, 5: 20, 6: 2}.get(n, -1)
        if m <= bound and ckey(S) not in reg[n]:
            return {"kind": "lower_rank_subring", "subset": J,
                    "subrank": n, "submultiplicity": m,
                    "subring_sha256": fp(S), "criterion":
                    {2: "rank-two complex classification", 3: "rank-three complex classification",
                     4: "rank-four through m=128", 5: "rank-five through m=20",
                     6: "rank-six through m=2"}[n]}
    return None


def rank7_negative_registry():
    rows=json.loads(RANK7_NEGATIVE.read_text())
    assert len(rows)==4 and len({x['id'] for x in rows})==4
    assert all(len(x['tensor'])==7 and x['multiplicity']==2
               and x['tensor_sha256']==fp(x['tensor']) for x in rows)
    return {ckey(x['tensor']):x for x in rows}


def rank7_certified_subring_certificate(R,negative):
    for J,S in proper_closed_subrings(R,max_rank=7):
        if len(J)!=7:
            continue
        match=negative.get(ckey(S))
        if match is not None:
            return {'kind':'rank7_certified_subring','subset':list(J),
                    'subring_sha256':fp(S),'rank7_id':match['id'],
                    'criterion':match['source_reference']}
    return None


def signed_witness_registry():
    allowed=json.loads((ROOT/'data/signed_certified_witness_ids.json').read_text())
    assert len(allowed)==len(set(allowed)) and all(x.startswith('R8_') for x in allowed)
    manifest=json.loads((ROOT/'experimental_signed/signed_certified_campaign.json').read_text())
    assert [x['id'] for x in manifest['entries']]==allowed
    rows=[]
    for entry in manifest['entries']:
        path=SIGNED_WITNESSES/(entry['id']+'.json')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['certificate_sha256']
        row=json.loads(path.read_text())
        assert row['tensor_sha256']==entry['source_tensor_sha256']
        rows.append(row)
    assert all(x['id']==id for x,id in zip(rows,allowed))
    assert len(rows)==len({x['tensor_sha256'] for x in rows})
    return {x['tensor_sha256']:x for x in rows}


def oriented_signed_certificate(R,witnesses):
    row=witnesses.get(fp(R))
    if row is None:
        return None
    return {'kind':'oriented_signed_sphericalization',
            'witness_id':row['id'],'signed_certificate_sha256':
            hashlib.sha256(json.dumps(row['certificate'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'criterion':'Rank-six oriented sphericalization and dimension-order theorem; rank-seven exact lifting'}


def published_negative_registry():
    archive=json.loads((ROOT/'experimental_signed/appendix_mle2_tensors.json').read_text())
    selected=[z for z in archive['entries'] if z['appendix_item'] in (5,7)]
    assert len(selected)==2
    assert all((f"excluded by Lemma 4.{3 if z['appendix_item']==5 else 2}." in z['categorification_line'])
               and len(z['source_tensor'])==8 for z in selected)
    return {ckey(z['source_tensor']):z for z in selected}


def published_appendix_certificate(R,negative):
    record=negative.get(ckey(R))
    if record is None:
        return None
    return {'kind':'published_induction_exclusion',
            'appendix_item':record['appendix_item'],
            'lemma':f"4.{3 if record['appendix_item']==5 else 2}",
            'appendix_tensor_sha256':fp(record['source_tensor']),
            'basis_map_source_to_appendix':model_basis_map(R,record['source_tensor']),
            'criterion':'Alekseyev--Bruns--Dong--Palcoux, accepted in Letters in Mathematical Physics, Appendix C.3.2'}


def casimir_poly(R):
    N = [sy.Matrix(A) for A in R]
    C = sum((A * A.T for A in N), sy.zeros(len(R)))
    return C.charpoly().as_poly()


def greedy_certificate(p):
    if all(p.eval(a) == 0 for a in (2, 3, 7)):
        return {"kind": "greedy_237", "codegrees": [2, 3, 7],
                "criterion": "Schopieray 2026, Corollary 2"}
    return None


def dnumber_certificate(p):
    for q, e in p.factor_list()[1]:
        co = list(map(int, q.all_coeffs()))
        d, norm = q.degree(), abs(co[-1])
        for j in range(1, d + 1):
            if pow(co[j], d, norm ** j) != 0:
                return {"kind": "dnumber", "factor": co, "index": j,
                        "criterion": "Ostrik, On formal codegrees, Lemma 2.7"}
    return None


def noncomm_dnumber_certificate(R,p):
    """Rank-eight Wedderburn refinement of Ostrik's d-number test.

    A noncommutative complex semisimple algebra of dimension eight with a
    positive one-dimensional character has precisely four one-dimensional
    simple representations and one two-dimensional simple representation.
    The latter is unique and hence Galois-fixed; its formal codegree is an
    integer.  Thus every nonlinear factor of the regular Casimir polynomial
    belongs exclusively to the one-dimensional codegrees.
    """
    assert len(R)==8 and not commutes(R)
    for q,e in p.factor_list()[1]:
        if q.degree()<2:
            continue
        co=list(map(int,q.all_coeffs()));d=q.degree();norm=abs(co[-1])
        for j in range(1,d+1):
            if pow(co[j],d,norm**j)!=0:
                return {"kind":"rank8_noncomm_dnumber", "factor":co,
                        "index":j,"criterion":
                        "Wedderburn 1^4+2^2 and Ostrik formal-codegree d-number"}
    return None


def integral_drinfeld_certificate(R,casimir=None):
    """Use integer FP dimensions and integral codegree divisibility [Integral].

    For a commutative based ring, every Casimir root is a formal codegree.
    If its FP character is rational, it is integral.  Every formal codegree
    of an integral complex fusion category is an integer divisor of the
    total FP dimension.  All arithmetic and the FP vector are exact.
    """
    if not commutes(R):
        return None
    n=len(R)
    P=sum((sy.Matrix(A) for A in R),sy.zeros(n))
    assert all(P[i,j]>0 for i in range(n) for j in range(n))
    dims=None
    for q,e in P.charpoly().as_poly().factor_list()[1]:
        if q.degree()!=1:
            continue
        eig=-int(q.TC())
        V=(P-eig*sy.eye(n)).nullspace()
        if len(V)!=1 or not V[0][0]:
            continue
        vv=[sy.cancel(v/V[0][0]) for v in V[0]]
        if not all(v>0 and v.q==1 for v in vv):
            continue
        dims=list(map(int,vv))
        assert dims[0]==1 and all(sum(R[i][j][k]*dims[k] for k in range(n))==dims[i]*dims[j]
                                  for i in range(n) for j in range(n))
        break
    if dims is None:
        return None
    D=sum(v*v for v in dims)
    p=casimir if casimir is not None else casimir_poly(R)
    for q,e in p.factor_list()[1]:
        if q.degree()!=1:
            return {'kind':'integral_drinfeld','dims':dims,'global_dimension':D,
                    'failed_factor':list(map(int,q.all_coeffs())),
                    'criterion':'Alekseyev--Bruns--Dong--Palcoux, integral Drinfeld necessary condition'}
        codegree=-int(q.TC())
        assert codegree>0
        if D%codegree:
            return {'kind':'integral_drinfeld','dims':dims,'global_dimension':D,
                    'failed_codegree':codegree,
                    'criterion':'Alekseyev--Bruns--Dong--Palcoux, integral Drinfeld necessary condition'}
    return None


def subring_dimension_certificate(R):
    """Exact FPdim(C)/FPdim(D) algebraic-integer test for a closed subring."""
    from rings import Characters
    a=Characters(R)
    f,K,ds,D,_,_=a.fp()
    u=K(sy.Poly(t,t).rem(f).all_coeffs())
    for J,_ in proper_closed_subrings(R,max_rank=7):
        S=sum((ds[i]*ds[a.du[i]] for i in J),K.zero)
        q=D/S
        mat=sy.Matrix.hstack(*(vector(q*u**i,f.degree()) for i in range(f.degree())))
        p=mat.charpoly(t).as_poly()
        if any(x.q!=1 for x in p.all_coeffs()):
            return {"kind":"subring_dimension","subset":J,
                    "quotient_polynomial":[str(x) for x in p.all_coeffs()],
                    "criterion":"ENO algebraic-integer index of fusion subcategory"}
    return None


def primitive_certificate(p):
    for q, e in p.factor_list()[1]:
        d, norm = q.degree(), abs(int(q.TC()))
        if norm == 0:
            raise ValueError("Codegree must be nonzero")
        # Prime norm valuation less than d is equivalent to indivisibility
        # by all rational integers for a cyclotomic d-number.
        if all(v < d for v in sy.factorint(norm).values()):
            if q.degree() != 8 or e != 1 or p != q:
                return {"kind": "primitive_codegree", "factor": list(map(int, q.all_coeffs())),
                        "degree": d, "norm": norm,
                        "criterion": "Schopieray 2021, Theorem 4.4 and Corollary 4.3"}
    return None


def main():
    rings = read_source()
    reg, positive = model_registry()
    rank7_negative=rank7_negative_registry()
    signed_witnesses=signed_witness_registry()
    published_negative=published_negative_registry()
    grouped = {m: sorted([R for R in rings if mult(R) == m], key=lambda R: tuple(
        x for M in R for row in M for x in row)) for m in (1, 2)}
    assert [len(grouped[i]) for i in (1,2)] == [96,877]
    stages = ("near_group", "rank_two", "zero_spectrum", "lower_rank_subring",
              "rank7_certified_subring",
              "dnumber", "noncomm_dnumber", "integral_drinfeld", "published_appendix_transfer",
              "involution_module", "field_automorphisms",
              "subring_dimension", "primitive_codegree", "cyclotomic", "oriented_signed_sphericalization")
    remaining = {(m,j): R for m in (1,2) for j,R in enumerate(grouped[m],1)}
    excluded, stage_rows = {}, []
    polys = {}
    for stage in stages:
        print("START", stage, "remaining", len(remaining), flush=True)
        assigned = collections.Counter()
        spectrum = {}
        if stage == "zero_spectrum":
            import zero_spectrum
            positions=list(remaining)
            spectrum=dict(zip(positions,zero_spectrum.batch([remaining[k] for k in positions])))
        for ij, R in list(remaining.items()):
            cert = None
            if stage == "near_group": cert = near_group_certificate(R)
            elif stage == "rank_two": cert = rank2_certificate(R)
            elif stage == "zero_spectrum": cert = spectrum[ij]
            elif stage == "lower_rank_subring": cert = lower_subring_certificate(R, reg)
            elif stage == "rank7_certified_subring":
                cert=rank7_certified_subring_certificate(R,rank7_negative)
            elif stage == "oriented_signed_sphericalization" and commutes(R):
                cert=oriented_signed_certificate(R,signed_witnesses)
            elif stage == "published_appendix_transfer":
                cert=published_appendix_certificate(R,published_negative)
            elif stage == "involution_module" and commutes(R):
                import involution_module
                cert=involution_module.certificate(R)
            elif stage == "field_automorphisms" and commutes(R):
                import field_automorphisms
                cert=field_automorphisms.certificate(R)
            elif stage == "subring_dimension" and commutes(R):
                from itertools import islice
                if next(proper_closed_subrings(R,max_rank=7),None) is not None:
                    cert=subring_dimension_certificate(R)
            elif commutes(R):
                if stage in ("dnumber", "noncomm_dnumber", "primitive_codegree"):
                    if ij not in polys:
                        polys[ij] = casimir_poly(R)
                    p = polys[ij]
                elif stage == "integral_drinfeld":
                    if ij not in polys:
                        polys[ij] = casimir_poly(R)
                    p = polys[ij]
                else:
                    p = None
                if stage == "dnumber": cert = dnumber_certificate(p)
                elif stage == "integral_drinfeld": cert=integral_drinfeld_certificate(R,p)
                elif stage == "primitive_codegree": cert = primitive_certificate(p)
                elif stage == "cyclotomic":
                    from rings import matrices
                    c = cyclotomic_failure([A.charpoly(t).as_poly() for A in matrices(R)])
                    if c: cert = {"kind": "cyclotomic", **c,
                       "criterion": "ENO cyclotomicity of based-ring characters"}
            elif stage=="noncomm_dnumber" and not commutes(R):
                if ij not in polys:
                    polys[ij]=casimir_poly(R)
                cert=noncomm_dnumber_certificate(R,polys[ij])
            if cert:
                excluded[ij] = cert
                del remaining[ij]
                polys.pop(ij, None)
                assigned[ij[0]] += 1
        for m in (1,2):
            stage_rows.append({"stage":stage,"multiplicity":m,
                               "new_exclusions":assigned[m],
                               "remaining_after":sum(ij[0] == m for ij in remaining)})
        print("DONE",stage,dict(assigned),"remaining",len(remaining),flush=True)

    models = []
    decisions = []
    for m in (1,2):
        for j, R in enumerate(grouped[m],1):
            k = (m,j)
            status = "excluded" if k in excluded else "unresolved"
            row = {"id": f"R8_{m}_{j}", "multiplicity":m,"index":j,
                   "tensor_sha256":fp(R), "commutative":commutes(R),
                   "status":status}
            if k in excluded:
                row["certificate"] = excluded[k]
            else:
                candidates = positive.get(ckey(R), [])
                if all(sum(R[i][j]) == 1 for i in range(8) for j in range(8)):
                    candidates = [{"model": "Vec(G), |G|=8",
                      "reference": "This manuscript, Section 4 (explicit based group ring); "
                                   "EGNO, Tensor Categories, Chapter 2 (pointed fusion categories)",
                      "tensor": R}] + candidates
                if candidates:
                    candidates=[
                        dict(x,basis_map_source_to_model=model_basis_map(R,x['tensor']),
                             **({'source_url':'https://bimsa.net/doc/publication/14753.pdf'}
                                if 'https://bimsa.net/doc/publication/14753.pdf' in x['reference']
                                else {})) for x in candidates]
                    status=row["status"]="unitarily_realized"
                    row["models"]=[x["model"] for x in candidates]
                    models.append({"id":row["id"],"multiplicity":m,
                                   "tensor_sha256":fp(R),"tensor":R,
                                   "constructors":candidates})
            decisions.append(row)
    assert len(decisions)==973
    assert len({x["tensor_sha256"] for x in decisions})==973
    assert not any(x["status"]=="excluded" and x.get("models") for x in decisions)
    (ROOT/"data"/"decisions.json").write_text(json.dumps(decisions,indent=2)+"\n")
    (ROOT/"data"/"realized_models.json").write_text(json.dumps(models,indent=2)+"\n")
    with (ROOT/"data"/"exclusion_stages.csv").open("w", newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(stage_rows[0]));w.writeheader();w.writerows(stage_rows)
    counts=[]
    for m in (1,2):
        a=collections.Counter(x["status"] for x in decisions if x["multiplicity"]==m)
        counts.append({"multiplicity":m,"fusion_rings":len(grouped[m]),
                       "excluded":a["excluded"],"realized":a["unitarily_realized"],
                       "unresolved":a["unresolved"]})
    (ROOT/"data"/"classification_counts.json").write_text(json.dumps(counts,indent=2)+"\n")
    print("CLASSIFICATION",counts)


if __name__ == "__main__": main()
