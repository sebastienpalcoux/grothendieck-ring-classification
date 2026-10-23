"""New actual-twist Galois-orbit / cyclic Fourier campaign for R928 and R941.

All coefficients are exact. Integer phase variables count actual simple objects
per root in a squared-Galois orbit. Endpoint mixtures stay continuous.
See cases/R928_R941_THEORY.md for the finite-domain proof and limitations.
"""
from functools import lru_cache
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import os
import sympy as sp

DEPENDENCIES = [
    "evidence/rank8_frontier_20261021/quartic_integer_center/source.json",
    "evidence/rank8_frontier_20261021/quartic_integer_center/gram_cubic.json",
    "evidence/rank8_frontier_20261021/quartic_integer_center/r941_charges.json",
    "evidence/rank8_creative_20261022/unified/composite_verification.json",
]
BRANCHES = {
    "R8_3_928": [40, 49, 186, 191],
    "R8_3_941": [8, 19, 21, 31, 34, 43, 45, 56, 60, 72, 73, 77, 79, 85],
}
TENSOR_HASHES = {
    "R8_3_928": "94dfb90235dbb3ba95864a1be23437943ea3b1316ec82ca44baf419262890614",
    "R8_3_941": "8ae4007492dee167ab8b3f4f16310ee368482da03696e20ed7cceea34bec64e6",
}
DEFAULT_ORDERS = (3, 4, 6, 8, 9, 12, 16)
N = 1152
TRANSLATED = (40, 41, 42, 43, 57)


def need(value, message):
    if not value:
        raise ValueError(message)


class Field:
    """Exact rational power-basis arithmetic in Q(zeta_n)."""
    def __init__(self, n):
        self.n = n
        x = sp.Symbol("x")
        self.mod = sp.Poly(sp.cyclotomic_poly(n, x), x)
        self.co = tuple(reversed([int(v) for v in self.mod.all_coeffs()]))
        self.degree = len(self.co) - 1
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)
        roots = [self.one]
        for j in range(1, n):
            old = roots[-1]
            lead = old[-1]
            roots.append(tuple((old[t - 1] if t else 0) -
                               lead * self.co[t] for t in range(self.degree)))
        self.roots = tuple(roots)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, a, q):
        return tuple(x * q for x in a)

    def sum(self, seq):
        result = list(self.zero)
        for a in seq:
            for j, x in enumerate(a):
                result[j] += x
        return tuple(result)

    def mul(self, a, b):
        out = [0] * (2 * self.degree - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        out[i + j] += x * y
        for i in range(len(out) - 1, self.degree - 1, -1):
            if out[i]:
                v = out[i]
                for j, c in enumerate(self.co[:-1]):
                    if c:
                        out[i - self.degree + j] -= v * c
        return tuple(out[:self.degree])

    def inv(self, a):
        x = self.mod.gen
        p = sp.Poly(sum(sp.Rational(v.numerator, v.denominator) * x**i
                        for i, v in enumerate(map(Q, a))), x)
        v = sp.invert(p, self.mod)
        return tuple(Q(int(v.nth(i).p), int(v.nth(i).q))
                     for i in range(self.degree))

    def auto(self, a, u):
        need(math.gcd(u, self.n) == 1, "Galois automorphism unit")
        return self.sum(self.scale(self.roots[(j * u) % self.n], v)
                        for j, v in enumerate(a) if v)

    def embed(self, a, target):
        need(target.n % self.n == 0, "cyclotomic field inclusion")
        return target.sum(target.scale(target.roots[j * (target.n // self.n)], v)
                          for j, v in enumerate(a) if v)


@lru_cache(None)
def field(n):
    return Field(n)


def kembed(v):
    f = field(48)
    r2 = f.add(f.roots[6], f.roots[42])
    r3 = f.add(f.roots[4], f.roots[44])
    return f.sum(f.scale(b, Q(q)) for b, q in
                 zip((f.one, r2, r3, f.mul(r2, r3)), v))


def masks(d):
    a, b, c, e = map(Q, d)
    return {12: 3*c-a-b, 24: 6*e-a-2*b}


def evaluate(chars, column):
    return [tuple(sum(Q(ch[i][j]) * column[i] for i in range(8))
                  for j in range(4)) for ch in chars]


@lru_cache(None)
def actual_orbits():
    """Squared-H orbits, H={u in (Z/N)^*: u=1 mod24}."""
    squares = sorted({u*u % N for u in range(1, N, 24)
                      if math.gcd(u, N) == 1})
    seen = set()
    result = []
    for e in range(N):
        if e in seen:
            continue
        orbit = tuple(sorted({e*u % N for u in squares}))
        seen.update(orbit)
        result.append(orbit)
        order = N // math.gcd(e, N)
        a = b = 0
        while order % 2 == 0:
            a += 1
            order //= 2
        while order % 3 == 0:
            b += 1
            order //= 3
        need(order == 1 and len(orbit) ==
             2**max(a-4, 0)*3**max(b-1, 0),
             "actual squared-H orbit formula")
    need(len(seen) == N, "complete actual-root partition")
    return tuple(result)


@lru_cache(None)
def moment(exponents, power):
    big = field(N)
    small = field(48)
    total = big.sum(big.roots[(e*power) % N] for e in exponents)
    # Phi_1152(x)=Phi_48(x^24); the orbit sum lies in Q(zeta48).
    need(big.degree == 24*small.degree, "cyclotomic degree ratio")
    need(all(not x for j, x in enumerate(total) if j % 24),
         "actual Galois-orbit sum in Q(zeta48)")
    return tuple(total[24*j] for j in range(small.degree))


class Model:
    def __init__(self):
        self.lo = []
        self.up = []
        self.integrality = []
        self.labels = []
        self.rows = []
        self.rhs = []
        self.row_labels = []
        self._seen = set()

    def var(self, label, lo, up, integer=True):
        need(Q(lo).denominator == Q(up).denominator == 1,
             "integer variable bounds")
        j = len(self.lo)
        self.lo.append(int(lo))
        self.up.append(int(up))
        self.integrality.append(int(integer))
        self.labels.append(label)
        return j

    def row(self, coeff, rhs, label):
        coeff = {int(j): Q(v) for j, v in coeff.items() if v}
        rhs = Q(rhs)
        den = math.lcm(rhs.denominator, *(v.denominator for v in coeff.values()))
        ints = {j: int(v*den) for j, v in coeff.items()}
        b = int(rhs*den)
        g = math.gcd(abs(b), *(abs(v) for v in ints.values())) or 1
        ints = {j: v//g for j, v in ints.items()}
        b //= g
        if ints:
            lead = ints[min(ints)]
            if lead < 0:
                ints = {j: -v for j, v in ints.items()}
                b = -b
        if not ints and not b:
            return
        key = (tuple(sorted(ints.items())), b)
        if key not in self._seen:
            self._seen.add(key)
            self.rows.append(ints)
            self.rhs.append(b)
            self.row_labels.append(label)

    def vector_row(self, linear, constant, target, label, f=None):
        f = f or field(48)
        for coordinate in range(f.degree):
            self.row({j: v[coordinate] for j, v in linear.items()
                      if v[coordinate]},
                     target[coordinate]-constant[coordinate],
                     [label, coordinate])


def load_data(vendor_root, case):
    files = [Path(vendor_root)/p for p in DEPENDENCIES]
    data = [json.loads(p.read_text()) for p in files]
    row = next(v for v in data[0]["records"] if v["id"] == case)
    need(row["tensor_sha256"] == TENSOR_HASHES[case], "source tensor binding")
    tensor_bytes = json.dumps(row["tensor"], separators=(",", ":")).encode()
    need(hashlib.sha256(tensor_bytes).hexdigest() == row["tensor_sha256"],
         "canonical tensor hash")
    need(len(data[1]["patterns"]) == 343, "complete Gram/cubic pattern domain")
    need(len(data[2]["solutions"]) == 93, "complete fermion charge domain")
    need(len(row["all_low_frames"]) == 1 and
         row["all_low_frames"][0]["symmetric_S_assignments"] == [[0,1,2,3,4]],
         "unique low frame and distinguished S assignment")
    return row, data[1], data[2], data[3], {
        p: hashlib.sha256(q.read_bytes()).hexdigest()
        for p, q in zip(DEPENDENCIES, files)
    }


def build_one(vendor_root, case, branch, orders=DEFAULT_ORDERS):
    row, gram, charges, composite, dependencies = load_data(vendor_root, case)
    f = field(48)
    chars = row["full_characters"]
    lows = row["low_columns"]
    highs = [[0]+v for v in row["canonical_high_vectors"]]
    columns = lows+highs
    values_k = [evaluate(chars, v) for v in columns]
    need(len(values_k) == 70 and len({tuple(v) for v in values_k}) == 70,
         "all restriction types distinguished by complete character evaluations")
    values = [[kembed(v) for v in ev] for ev in values_k]
    dims = [ev[0] for ev in values]
    D = kembed(row["formal_codegrees"][0])
    invD = f.inv(D)
    need(f.mul(D, invD) == f.one, "exact global dimension inversion")
    norm = f.one
    for conjugate in row["formal_codegrees"][:4]:
        norm = f.mul(norm,kembed(conjugate))
    need(all(v == 0 for v in norm[1:]) and Q(norm[0]).denominator == 1,
         "quartic dimension norm is a rational integer")
    prime_tail = abs(int(norm[0]))
    need(prime_tail > 0, "nonzero dimension norm")
    for prime in (2,3):
        while prime_tail % prime == 0:
            prime_tail //= prime
    need(prime_tail == 1, "categorical Cauchy twist prime support is only 2,3")
    for E in range(5):
        d = f.mul(D, f.inv(kembed(row["formal_codegrees"][E])))
        need(d == dims[E], "low dimension D/f_E")
        betaE = f.scale(d, Q(1, row["irreducible_dimensions"][E]))
        for H in range(5):
            dH = dims[H]
            betaH = f.scale(dH, Q(1, row["irreducible_dimensions"][H]))
            need(f.mul(betaE, values[H][E]) ==
                 f.mul(betaH, values[E][H]), "distinguished S normalization")
    need({c for c in range(40) if not any(masks(values_k[5+c][0]).values())}
         == {12,23}, "only two unbounded saturated dimension types")
    for conductor in (12,24):
        need(sum(masks(values_k[t][0])[conductor]**2 for t in range(5)) == 4,
             "low twist-one objects exhaust saturated mask capacity")
        control = next(c for c in composite["quartic_controls"]
                       if c["conductor"] == conductor)
        need(4*conductor*Q(control["epsilon_minus_weights"][0]) ==
             4*conductor*Q(control["epsilon_plus_weights"][0]) == 4,
             "exact twist-one spectral capacity")
    qlow = [1,1,1,1,-1]
    g = 7 if case.endswith("928") else 3
    for E in range(5):
        need(tuple(map(Q, chars[E][g])) ==
             (Q(qlow[E]*row["irreducible_dimensions"][E]),0,0,0),
             "invertible-row character normalization")
    semion = case.endswith("928")
    need(lows[0] == [1,0,0,0,0,0,0,0] and
         highs[40] == [int(j == g) for j in range(8)],
         "vacuum and forced central invertible restrictions")
    for c,v in zip(TRANSLATED,lows):
        translated = [sum(v[a]*row["tensor"][g][a][b] for a in range(8))
                      for b in range(8)]
        need(highs[c] == translated, "fixed central translates bind source tensor")
    theta_g = N//4 if semion else N//2
    fixed = [(i, 0, q) for i, q in enumerate(qlow)]
    fixed += [(5+c, theta_g if q == 1 else (-theta_g) % N,
               -q if semion else q) for c, q in zip(TRANSLATED, qlow)]
    if semion:
        counts = gram["patterns"][branch]
        need(all(counts[c] % 2 == 0 for c in range(40)), "semion pair counts")
        charge_counts = [(c, 1, counts[c]//2, "semion_pair")
                         for c in range(40) if counts[c]]
        pattern_index = branch
    else:
        allocation = charges["solutions"][branch]
        pattern_index = allocation["pattern_index"]
        counts = gram["patterns"][pattern_index]
        p = allocation["plus_pairs"]
        q = allocation["minus_individuals"]
        need(all(2*p[c]+q[c] == counts[c] for c in range(40)),
             "fermion charge/pattern consistency")
        charge_counts = [(c, 1, p[c], "fermion_pair") for c in range(40) if p[c]]
        charge_counts += [(c,-1,q[c],"individual") for c in range(40) if q[c]]
    need(all(counts[c] == (1 if c in TRANSLATED else 0)
             for c in range(40,65)), "complete fixed translated-high domain")
    need(counts[12] <= 8 and counts[23] <= 8, "finite unrestricted-type bound")
    model = Model()
    packets = []
    for c, charge, required, kind in charge_counts:
        L = masks(values_k[5+c][0])
        bound = 12 if L[12] else 24 if L[24] else 0
        seen = set()
        block = []
        for orbit in actual_orbits():
            positive = orbit
            if kind == "semion_pair":
                actual = tuple(orbit)+tuple((e+N//4) % N for e in orbit)
                weighted = tuple((e,1) for e in orbit) + tuple(
                    ((e+N//4) % N,-1) for e in orbit)
                cost = len(orbit)
                key = orbit
            elif kind == "fermion_pair":
                actual = tuple(sorted(set(orbit) | {(e+N//2) % N for e in orbit}))
                weighted = tuple((e,1) for e in actual)
                cost = len(actual)//2
                key = actual
            else:
                actual = orbit
                weighted = tuple((e,-1) for e in orbit)
                cost = len(orbit)
                key = orbit
            if key in seen:
                continue
            seen.add(key)
            if cost > required:
                continue
            if bound and any((e*bound) % N for e in actual):
                continue
            if c not in (12,23) and 0 in actual:
                continue
            j = model.var(["phase",c,charge,kind,list(key)], 0, required//cost)
            packets.append({"j":j, "c":c, "actual":tuple(actual),
                            "weighted":weighted, "count":cost,
                            "kind":kind, "charge":charge})
            block.append((j,cost))
        model.row(dict(block), required, ["restriction_charge_count",c,charge,kind])
    mixes = {control["conductor"]:
             model.var(["continuous_spectral_endpoint",control["conductor"]],
                       0,1,False) for control in composite["quartic_controls"]}

    @lru_cache(None)
    def pm(j, power, charged=False):
        packet = packets[j]
        need(packet["j"] == j, "phase variable contiguous indexing")
        if charged:
            plus = tuple(e for e,q in packet["weighted"] if q == 1)
            minus = tuple(e for e,q in packet["weighted"] if q == -1)
            return f.add(moment(plus,power), f.scale(moment(minus,power),-1))
        return moment(packet["actual"],power)

    def fixed_sum(power, weight, charged=False):
        terms = []
        for t,e,q in fixed:
            terms.append(f.scale(f.mul(moment((e,),power),weight(t)),q if charged else 1))
        return f.sum(terms)

    # Full complex distinguished-row STS.
    for E in range(5):
        for H in range(E,5):
            weight = lambda t: f.mul(values[t][E],values[t][H])
            linear = {p["j"]:f.mul(pm(p["j"],1),weight(5+p["c"])) for p in packets}
            const = fixed_sum(1,weight)
            target = f.scale(f.mul(kembed(row["formal_codegrees"][H]),values[H][E]),
                             row["irreducible_dimensions"][H])
            model.vector_row(linear,const,target,["STS",E,H])
    # The forced central invertible row; divided by beta_E, not beta_E*n_E.
    for E in range(5):
        weight = lambda t: f.mul(dims[t],values[t][E])
        linear = {p["j"]:f.mul(pm(p["j"],1,True),weight(5+p["c"])) for p in packets}
        const = fixed_sum(1,weight,True)
        target = f.mul(f.mul(D,kembed(chars[E][g])),
                       moment(((-theta_g)%N,),1))
        model.vector_row(linear,const,target,["central_STS",E])

    # All signed spectral fibres; mixtures are continuous endpoint coordinates.
    for control in composite["quartic_controls"]:
        conductor = control["conductor"]
        minus = list(map(Q,control["epsilon_minus_weights"]))
        plus = list(map(Q,control["epsilon_plus_weights"]))
        for exponent in range(conductor):
            coeff = {}
            for p in packets:
                L = masks(values_k[5+p["c"]][0])[conductor]
                if not L:
                    continue
                need(all(e*conductor % N == 0 for e in p["actual"]),
                     "saturated actual-root support")
                multiplicity = sum(e*conductor//N % conductor == exponent
                                   for e in p["actual"])
                if multiplicity:
                    coeff[p["j"]] = L*L*multiplicity
            coeff[mixes[conductor]] = -4*conductor*(minus[exponent]-plus[exponent])
            rhs = 4*conductor*plus[exponent]
            for t,e,q in fixed:
                L = masks(values_k[t][0])[conductor]
                if L:
                    need(e*conductor % N == 0,"fixed saturated phase support")
                    if e*conductor//N % conductor == exponent:
                        rhs -= L*L
            model.row(coeff,rhs,["signed_spectral_fibre",conductor,exponent])

    # Source tensor powers, with the source multiplication order fixed explicitly.
    R = row["tensor"]
    max_order = max(orders+(2,))
    powers = {}
    for i in range(8):
        seq = [(1,0,0,0,0,0,0,0)]
        for power in range(1,max_order+1):
            old = seq[-1]
            seq.append(tuple(sum(old[a]*R[a][i][b] for a in range(8))
                             for b in range(8)))
        powers[i] = seq

    @lru_cache(None)
    def indicator(m, source_coefficients):
        weights = [sum(source_coefficients[i]*v[i] for i in range(8))
                   for v in columns]
        linear = {p["j"]:f.scale(f.mul(f.mul(pm(p["j"],m),
                                  dims[5+p["c"]]),invD),weights[5+p["c"]])
                  for p in packets}
        constant = f.mul(fixed_sum(m,lambda t:f.scale(dims[t],weights[t])),invD)
        return linear, constant

    indicators2 = [1,0,0,0,0,0,0,-1] if semion else [1,0,0,1,1,1,1,1]
    for i in range(8):
        unit = tuple(int(i == j) for j in range(8))
        for m,target in [(1,int(i == 0)),(2,indicators2[i])]:
            linear,const = indicator(m,unit)
            model.vector_row(linear,const,f.scale(f.one,target),["indicator",m,i])

    # Needed indicators must belong to Q(zeta_m), before extending automorphisms.
    needed = {n//math.gcd(n,k) for n in orders for k in range(1,n)}
    units48 = [u for u in range(48) if math.gcd(u,48) == 1]
    for m in sorted(needed):
        d = math.gcd(m,48)
        fixing = [u for u in units48 if (u-1) % d == 0]
        for i in range(8):
            unit = tuple(int(i == j) for j in range(8))
            linear,const = indicator(m,unit)
            for u in fixing:
                if u == 1:
                    continue
                difference = {j:f.add(f.auto(v,u),f.scale(v,-1))
                              for j,v in linear.items()}
                dc = f.add(f.auto(const,u),f.scale(const,-1))
                model.vector_row(difference,dc,f.zero,["indicator_field",m,i,u])

    # Exact Fourier integrality of cyclic rotation on Hom(1,X_i^n).
    for n in orders:
        large = field(math.lcm(48,n))
        for i in range(8):
            # Coefficientwise positive FP upper bound; no floating algebraic comparison.
            ds = list(map(Q,chars[0][i]))
            need(all(v >= 0 for v in ds), "positive FP coordinates for safe trace bound")
            upper = sum(v*w for v,w in zip(ds,(1,2,2,3)))
            upper = math.ceil(upper)
            homdim = powers[i][n][0]
            quotient,remainder = divmod(homdim,n)
            trace_bound = sum(upper**math.gcd(n,k) for k in range(1,n))
            B = (trace_bound+n-1)//n+1
            traces = []
            for k in range(1,n):
                divisor = math.gcd(n,k)
                m = n//divisor
                d = math.gcd(m,48)
                coprime_power = k//divisor
                u = next(u for u in units48 if (u-coprime_power) % d == 0)
                linear,const = indicator(m,powers[i][divisor])
                traces.append(({j:f.embed(f.auto(v,u),large)
                                 for j,v in linear.items()},
                               f.embed(f.auto(const,u),large)))
            for eigen in range(n):
                j = model.var(["rotation_shift",n,i,eigen,quotient],
                              max(-B,-quotient),min(B,homdim-quotient),True)
                linear = {j:large.scale(large.one,-n)}
                constant = large.scale(large.one,remainder)
                for k,(tk,tc) in enumerate(traces,1):
                    root = large.roots[(-eigen*k*(large.n//n)) % large.n]
                    constant = large.add(constant,large.mul(root,tc))
                    for v,co in tk.items():
                        linear[v] = large.add(linear.get(v,large.zero),
                                              large.mul(root,co))
                model.vector_row(linear,constant,large.zero,
                                 ["cyclic_Fourier",n,i,eigen],large)
    branch_kind = "pattern" if semion else "charge_allocation"
    model_id = case+"_"+branch_kind+"_"+str(branch)+"_orbits1152_fourier_"+"_".join(map(str,orders))
    return {
        "id":model_id,"case":case,"n":len(model.lo),
        "rows":model.rows,"rhs":model.rhs,"lo":model.lo,"up":model.up,
        "integrality":model.integrality,"variable_labels":model.labels,
        "row_labels":model.row_labels,
        "branch":branch,"branch_kind":branch_kind,"pattern_index":pattern_index,
        "complete_branch_set":BRANCHES[case],"selected_rotation_orders":list(orders),
        "phase_variables":len(packets),"continuous_variables":list(mixes.values()),
        "source_dependencies":dependencies,"tensor_sha256":row["tensor_sha256"],
        "coverage":{
            "parent_domain":"published exact surviving reductions",
            "complete_branches":BRANCHES[case],
            "actual_root_conductor_bound":N,
            "bound_scope":"all actual twists after squared-Galois orbit and saturated support",
            "unrestricted_actual_type_counts":{"12":counts[12],"23":counts[23]},
            "full_cyclic_fourier_orders":list(orders),
            "all_bounds_exact_and_finite":True,
        },
        "theory_scope":(
            "Necessary finite actual-twist orbit model for the entire inherited branch. "
            "Infeasibility requires exact rational/integer certification. Feasibility "
            "does not construct a fusion category. Higher rotation orders may strengthen "
            "the model; the conductor bound is complete, not a numerical cutoff."
        ),
    }


def selected_orders():
    text = os.environ.get("RANK8_FOURIER_ORDERS")
    result = DEFAULT_ORDERS if not text else tuple(sorted(set(map(int,text.split(",")))))
    need(result and all(2 <= n <= 48 for n in result), "rotation orders within 2..48")
    return tuple(result)


def build_models(vendor_root: Path, case: str, out: Path, limit=None):
    need(case in BRANCHES,"supported quartic case")
    orders = selected_orders()
    branches = BRANCHES[case] if limit is None else BRANCHES[case][:int(limit)]
    for branch in branches:
        model = build_one(vendor_root,case,branch,orders)
        model["coverage"]["selected_branches"] = branches
        model["coverage"]["complete_branch_campaign"] = branches == BRANCHES[case]
        yield model


def self_test(vendor_root):
    f = field(48)
    need(f.mul(kembed((0,1,0,0)),kembed((0,1,0,0))) == f.scale(f.one,2),
         "sqrt2 embedding")
    need(f.mul(kembed((0,0,1,0)),kembed((0,0,1,0))) == f.scale(f.one,3),
         "sqrt3 embedding")
    need(f.mul(kembed((0,1,0,0)),kembed((0,0,1,0))) == kembed((0,0,0,1)),
         "sqrt6 embedding")
    need(moment((0,),1) == f.one,"unit actual phase")
    need(moment((N//4,),2) == f.scale(f.one,-1),"central semion square")
    need(f.add(moment((N//4,),1),moment((3*N//4,),1)) == f.zero,
         "opposite imaginary phases")
    actual_orbits()
    models = [build_one(vendor_root,case,BRANCHES[case][0],(3,4))
              for case in BRANCHES]
    for model in models:
        need(model["n"] == len(model["lo"]) == len(model["integrality"]),
             "model dimensions")
        need(len(model["rows"]) == len(model["rhs"]),"row/rhs dimensions")
        need(all(model["lo"][j] <= model["up"][j] for j in range(model["n"])),
             "finite bounds")
        need(all(model["integrality"][j] == 0 for j in model["continuous_variables"]),
             "spectral endpoint mixtures stay continuous")
        need(all(isinstance(v,int) for r in model["rows"] for v in r.values()),
             "exact integer rows")
    return {"status":"PASS","orbits":len(actual_orbits()),
            "representatives":[{"id":m["id"],"n":m["n"],"rows":len(m["rows"])}
                               for m in models]}
