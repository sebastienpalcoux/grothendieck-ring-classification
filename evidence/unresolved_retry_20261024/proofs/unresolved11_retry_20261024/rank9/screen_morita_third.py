"""Add the proved Morita total third-rotation bound to existing center systems."""
from pathlib import Path
from fractions import Fraction as Q
import inspect, sys, json, math, hashlib, time, itertools, gzip

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
OLD = WORK / "unresolved11_20261024"
rid = sys.argv[1]
tau = int(sys.argv[2])
height = int(sys.argv[3]) if len(sys.argv) > 3 else 4
local_clifford = "--local-clifford" in sys.argv
discrete = "--discrete" in sys.argv
sys.path.insert(0, str(WORK / "rank9_m2_research/phase3/quadratic_s_symmetry"))
sys.path.insert(0, str(WORK / "rank9_m2_research/phase3/noncomm1975"))
import quadratic_s_symmetry as qs
import symmetry as sy
qc = qs.qc
R = json.loads((OLD / "inputs" / f"{rid}.json").read_text())["fusion_tensor"]
noncomm = rid == "R9_2_1975"
builder = sy if noncomm else qs
data = sy.base(R) if noncomm else qc.base(R)
g = {"R9_2_137": 1, "R9_2_1607": 5, "R9_2_1975": 5, "R9_2_1976": 8}[rid]
Y = {"R9_2_137": 8, "R9_2_1607": 3, "R9_2_1975": 8, "R9_2_1976": 5}[rid]
data["cols"] = [(v, z) for v, z in data["cols"] if z[1] or
                (tuple(v) == (1,0,0,0,0,0,0,0,0) if noncomm
                 else z[0] == 1 and not v[g])]
fermions = {v for v, z in data["cols"] if z == (1,0) and not v[0]}
source = inspect.getsource(builder.build).replace("return AA,bb,meta", "return AA,bb,meta,keys")
namespace = dict(vars(builder))
if noncomm:
    namespace["base"] = lambda _: data
exec(source, namespace)
oldbase = qc.base
qc.base = lambda _: data
try:
    A, b, meta, keys = namespace["build"](R, height, False)
finally:
    qc.base = oldbase
types, bound = qc.trace_types(2, [2,3], height)
costs = [(Q(1),Q(0)),(Q(0),Q(1,2)),(Q(0),Q(0)),(Q(0),Q(-1,2)),
         (Q(-1),Q(0)),(Q(0),Q(-1,2)),(Q(0),Q(0)),(Q(0),Q(1,2))]
allowed = [tuple(costs[(j*k)%8] for k in range(1,height+1)) for j in (1,3)]
allowed += ([tuple((Q(a**k),Q(0)) for k in range(1,height+1)) for a in (1,-1)]
            if tau == 1 else
            [tuple((Q(0) if k%2 else Q((-1)**(k//2)),Q(0))
                   for k in range(1,height+1))])
fermiontrace = tuple((Q((-1)**k),Q(0)) for k in range(1,height+1))
keep = [j for j,(kind,v,t) in enumerate(keys) if kind != "high" or
        ((not v[Y] or tuple(types[t]) in allowed) and
         (v not in fermions or tuple(types[t]) == fermiontrace))]
A = [[row[j] for j in keep] for row in A]
keys = [keys[j] for j in keep]
col_dims = {v:z for v,z in data["cols"]}


def add_equal(row, rhs):
    den = math.lcm(*(Q(x).denominator for x in row + [rhs]))
    A.append([int(x*den) for x in row]); b.append(int(rhs*den))


for k, value in [(k,v) for k,v in [(2,tau),(4,0),(6,tau)] if k <= height]:
    vals = [qc.scale(qc.mul(col_dims[v],types[t][k-1],2),v[Y])
            if kind == "high" and v[Y] else (Q(0),Q(0))
            for kind,v,t in keys]
    rhs = qc.scale(data["D"], value)
    for c in range(2):
        add_equal([z[c] for z in vals], rhs[c])
if not noncomm:
    row = [int(kind == "high" and v in fermions) for kind,v,t in keys]
    for rr in A: rr.append(0)
    A.append(row+[1]); b.append(1)
    keys.append(("slack",(),0))

# Morita invariance of weighted third indicators gives:
# sum_Z dim(Z)^2 Tr_K(theta_Z^3) = D*(1+d*S),
# S=sum_{four source large objects} Tr_K(nu_3), S <= 2.
# The sqrt(2) coefficient is 96 + 816*S <= 1728.
weighted = []
for kind,v,t in keys:
    if kind == "high":
        weighted.append(qc.mul(qc.mul(col_dims[v],col_dims[v],2),types[t][2],2))
    elif kind in ("label","anon","anonymous"):
        weighted.append(qc.mul(col_dims[v],col_dims[v],2))
    else:
        weighted.append((Q(0),Q(0)))
row = [z[1] for z in weighted]
for rr in A: rr.append(0)
den = math.lcm(*(Q(x).denominator for x in row))
A.append([int(x*den) for x in row]+[den]); b.append(1728*den)
keys.append(("slack",(),0))

if local_clifford:
    if noncomm:
        raise ValueError("The direct source argument needs equal left/right stabilizers")
    large = [i for i in range(9) if data["dims"][i][1]]
    for i in large:
        vals = []
        for kind,v,t in keys:
            if kind == "high":
                vals.append(qc.scale(qc.mul(col_dims[v],types[t][2],2),v[i]))
            elif kind in ("label","anon","anonymous"):
                vals.append(qc.scale(col_dims[v],v[i]))
            else:
                vals.append((Q(0),Q(0)))
        row = [z[1] for z in vals]
        for rr in A: rr.append(0)
        den = math.lcm(*(Q(x).denominator for x in row))
        A.append([int(x*den) for x in row]+[den]); b.append(48*den)
        keys.append(("slack",(),0))

def exact_primal(matrix, rhs, floats):
    """Recover a rational basic solution from numerical support by exact RREF."""
    import flint
    for threshold in (1e-7,1e-9,1e-11):
        support = [j for j,x in enumerate(floats) if x > threshold]
        reduced, rank = flint.fmpq_mat([[row[j] for j in support]+[y]
                                      for row,y in zip(matrix,rhs)]).rref()
        k = len(support)
        vals = [Q(0)]*k
        valid = True
        for i in range(rank):
            pivot = next((j for j in range(k+1) if reduced[i,j]),None)
            if pivot == k:
                valid = False; break
            if pivot is not None:
                vals[pivot] = Q(str(reduced[i,k]))
        if valid and all(x >= 0 for x in vals):
            if all(sum(row[j]*x for j,x in zip(support,vals)) == y
                   for row,y in zip(matrix,rhs)):
                return [[j,str(x)] for j,x in zip(support,vals) if x]
    return None


if discrete:
    if not local_clifford:
        raise ValueError("Discrete screen needs the source-local theorem")
    import numpy as np
    from scipy.optimize import linprog
    # Each of the four last rows is its object's projected third moment.
    # Delete their independent nonnegative slacks and prescribe one of the
    # two allowed indicator values exactly. The aggregate slack is retained.
    denoms = [A[-4+k][-4+k] for k in range(4)]
    AA = [row[:-4] for row in A]
    bb = b[:]
    matrix = np.asarray(AA,dtype=float)
    records = []
    for choices in itertools.product((Q(-1),Q(1,2)),repeat=4):
        rhs = bb[:]
        rhs[-4:] = [int(96*x*den) for x,den in zip(choices,denoms)]
        ff = np.asarray(rhs,dtype=float)
        scale = np.maximum(1,np.maximum(abs(matrix).max(axis=1),abs(ff)))
        sol = linprog(np.zeros(len(AA[0])),A_eq=matrix/scale[:,None],
                      b_eq=ff/scale,bounds=(0,None),method="highs",
                      options={"time_limit":30})
        rec = {"projected_indicators":list(map(str,choices)),"numerical_status":sol.status}
        if sol.success:
            witness = exact_primal(AA,rhs,sol.x)
            if witness is not None:
                rec["exact_witness"] = witness
                rec["system_sha256"] = hashlib.sha256(json.dumps([AA,rhs],separators=(',',':')).encode()).hexdigest()
                name = f"{rid}_tau{tau}_h{height}_discrete_clifford"
                with gzip.open(HERE/f"{name}_system.json.gz","wt") as stream:
                    json.dump({"A":AA,"b":rhs,"witness":witness},stream,separators=(',',':'))
                records.append(rec)
                break
        elif sol.status == 2:
            ray, why = qc.exact_separator(AA,rhs,timeout=30)
            rec["separator_report"] = why
            if ray is not None:
                if not qc.verify_ray(AA,rhs,ray):
                    raise ValueError("Invalid discrete separator")
                rec["exact_ray"] = ray
        records.append(rec)
    result = {"source":rid,"tau":tau,"height":height,
              "branch_records":records,"classification_change":False,
              "scope":"Necessary projected-center relaxation with exact source-local Clifford choices. A feasible witness is not a categorical model."}
    (HERE/f"{rid}_tau{tau}_h{height}_discrete_clifford.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"source":rid,"tau":tau,"branches_tried":len(records),
                      "exact_feasible_branch":any("exact_witness" in r for r in records),
                      "exact_excluded_branches":sum("exact_ray" in r for r in records),
                      "classification_change":False}))
    raise SystemExit(0)

start = time.monotonic()
ray, why = qc.exact_separator(A,b,timeout=60)
result = {"source":rid,"tau":tau,"height":height,"rows":len(A),
          "columns":len(A[0]),"ray":ray,"solver_report":why,
          "new_constraint":"projected sum of four large third indicators <= 2",
          "system_sha256":hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest(),
          "seconds":time.monotonic()-start,
          "classification_change":False}
result["local_clifford"] = local_clifford
if ray:
    if not qc.verify_ray(A,b,ray): raise ValueError("Invalid separator")
    result["bTy"] = sum(x*y for x,y in zip(b,ray))
    result["min_ATy"] = min(sum(row[j]*y for row,y in zip(A,ray)) for j in range(len(A[0])))
else:
    import numpy as np
    from scipy.optimize import linprog
    mat = np.asarray(A,dtype=float); rhs = np.asarray(b,dtype=float)
    scale = np.maximum(1,np.maximum(abs(mat).max(axis=1),abs(rhs)))
    # Check exact rational feasibility; this is a necessary-system witness only.
    sol = linprog(np.zeros(len(A[0])),A_eq=mat/scale[:,None],b_eq=rhs/scale,
                  bounds=(0,None),method="highs",options={"time_limit":30})
    result["primal_status"] = sol.status
    if sol.success:
        for limit in (100,10000,1000000):
            xx = [Q(float(x)).limit_denominator(limit) for x in sol.x]
            if all(sum(c*x for c,x in zip(row,xx)) == y for row,y in zip(A,b)):
                result["rational_witness"] = [[i,str(x)] for i,x in enumerate(xx) if x]
                break
(HERE / f"{rid}_tau{tau}_h{height}_{'local_clifford' if local_clifford else 'morita_third'}.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("ray","rational_witness")}))
