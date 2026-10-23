"""R8_3_1768: join integer center structure to the saturated phase cone.

This is discovery, not replay of the previously feasible rational cone.
The two tasks exhaust the surviving V=4 irrational-sector alternatives.
Original center-count/fusion/slack variables are integral. Relative trace
weights and rotation compression auxiliaries remain continuous throughout.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import sys

CASE = "R8_3_1768"
TENSOR_SHA256 = "240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0"
DS = ((1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1))
Z = (0,0,1,1,1,1,1,1)
TWO_Z = tuple(2*x for x in Z)
ALPHA = (1,0,2,2,2,2,2,2)
BRANCHES = (("sector18", TWO_Z, 18), ("sector72", Z, 72))
COMPLETE_BRANCH_SET = [CASE + "_" + name for name, _, _ in BRANCHES]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _json_canonical(value):
    # Stable across JSON round trips, including sparse integer column keys.
    if isinstance(value,dict):
        return {str(k):_json_canonical(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [_json_canonical(v) for v in value]
    if isinstance(value,Q):
        return str(value)
    return value


def digest(value):
    return hashlib.sha256(json.dumps(_json_canonical(value), sort_keys=True, separators=(",",":")).encode()).hexdigest()


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "Cannot load " + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _dimension(v):
    return tuple(sum(Q(v[i])*DS[i][k] for i in range(8)) for k in range(2))


def _rational_ratio(v):
    a,b = _dimension(v)
    return 6*a == 37*b


def _canonical_source(vendor_root):
    path = vendor_root / "site/dist/downloads/fusion-tensors" / (CASE + ".txt")
    require(path.is_file(), "Missing canonical tensor: " + str(path))
    tensor = json.loads(path.read_text())
    require(len(tensor)==8 and all(len(M)==8 and all(len(row)==8 for row in M) for M in tensor), "Tensor shape")
    require(all(type(x) is int and x>=0 for M in tensor for row in M for x in row), "Tensor coefficients")
    actual = hashlib.sha256(json.dumps(tensor,separators=(",",":")).encode()).hexdigest()
    require(actual == TENSOR_SHA256, "Canonical R1768 tensor digest differs")
    require(all(tensor[i][i][0]==1 for i in range(8)), "Self-duality prerequisite")
    return {"id":CASE, "tensor":tensor, "tensor_sha256":actual}


def _setup(vendor_root):
    vendor_root = Path(vendor_root).resolve()
    frontier = vendor_root / "evidence/rank8_frontier_20261021"
    latest = vendor_root / "evidence/rank8_creative_20261022/r1768"
    for directory in ("global_induction","commutative_integer","quadratic","quadratic_atomic_integer"):
        sys.path.insert(0,str(frontier/directory))
    sys.path.insert(0,str(latest))
    phase_module = _module("_laptop_r1768_phase", latest/"unit_orbit_cone.py")
    fv = _module("_laptop_r1768_integer", frontier/"quadratic_atomic_integer/final_verify.py")
    canonical = _canonical_source(vendor_root)
    # The original lookup reads the entire 3,527-record census. This equivalent
    # lookup binds the one canonical tensor required by this adapter.
    def lookup(identifier):
        require(identifier==CASE, "R1768 adapter requested another tensor")
        return canonical
    original_lookup = phase_module.f.st.load_ring
    phase_module.f.st.load_ring = lookup
    # setup installs the published exact low-column accelerator and verifies
    # equality of its complete domain with the frozen atomic-cone metadata.
    # Restore the shared loader before another case is built in this process.
    try:
        setup = phase_module.f.setup(1768)
        phase = phase_module.UnitOrbitCone(setup[1])
        source, system, reports = fv.construct(1768)
    finally:
        phase_module.f.st.load_ring = original_lookup
    phase_module._laptop_base_setup = setup
    require(system is not None, "Previously accepted integer support is now empty; retain this as a separate audited result")
    require(source["tensor_sha256"]==TENSOR_SHA256, "Integer and phase tensor mismatch")
    require(tuple(tuple(Q(x) for x in d) for d in phase.a["dimensions"]) == tuple(tuple(Q(x) for x in d) for d in DS), "Dimension basis mismatch")
    require(system.metadata["FP_character"]==phase.meta["FP_character"], "Character label order mismatch")
    integer_table = fv.RealTable(source["tensor"], phase.a)
    require(integer_table.metadata==phase.meta["character_table"], "Complete ordered character-table basis mismatch")
    require(all(len(orbit)==1 for orbit in phase.orbits), "Source self-duality must give singleton high restriction orbits")
    return phase_module, phase, system, reports


def _assemble(system, phase, branch_name, sector_vector, sector_count):
    """Sparse exact mixed-integer intersection; no phase integrality assumed."""
    nr = len(system.rhs)
    n0 = len(system.columns)
    rows = [{} for _ in range(nr)]
    rhs = [int(x) for x in system.rhs]
    for j,col in enumerate(system.columns):
        require(len(col)==nr, "Integer column height")
        for i,a in enumerate(col):
            if a:
                require(type(a) is int, "Integer center row must be exact")
                rows[i][j]=a
    row_labels = [list(label) for label in system.row_labels]
    lo = [0]*n0
    up = [int(x) for x in system.bounds]
    integrality = [1]*n0
    variable_labels = [list(label) for label in system.column_labels]
    lows = {}
    highs = {}
    for j,label in enumerate(system.column_labels):
        if label[0]=="low":
            key=(int(label[1]),tuple(label[2]))
            require(key not in lows,"Duplicate labelled distinguished choice")
            lows[key]=j
        elif label[0]=="high_orbit":
            vectors=tuple(tuple(v) for v in label[2])
            require(len(vectors)==1,"R1768 high counts must count individual self-dual restriction types")
            require(vectors[0] not in highs,"Duplicate high restriction type")
            highs[vectors[0]]=j
    require(lows and highs,"Missing center structural variables")

    # The alpha object and both irrational-sector alternatives are theorem
    # consequences, not guesses selected from the previous rational witness.
    forced_zero_low = 0
    for (character,v),j in lows.items():
        if _dimension(v)==(Q(73),Q(12)) and v!=ALPHA:
            up[j]=0
            forced_zero_low+=1
    target_index=highs.get(tuple(sector_vector))
    irrational=[]
    for v,j in highs.items():
        if not _rational_ratio(v):
            irrational.append(j)
            if v!=tuple(sector_vector):
                up[j]=0
    if target_index is not None and sector_count<=up[target_index]:
        lo[target_index]=up[target_index]=int(sector_count)
    rows.append({target_index:1} if target_index is not None else {})
    rhs.append(int(sector_count))
    row_labels.append(["irrational_ratio_sector_count",branch_name])

    # After unit, alpha and the forced irrational sector are removed, the
    # high rational sector has sum t^2=52, dim(Y)=t*(37+6*sqrt(37)).
    mass_row={}
    for v,j in highs.items():
        if _rational_ratio(v):
            a,b=_dimension(v)
            t=a/Q(37)
            require(t==b/Q(6) and t.denominator==1 and t>0, "Rational-sector dimension is not a positive integral multiple of D/12")
            weight=int(t)**2
            mass_row[j]=weight
            up[j]=min(up[j],52//weight)
    rows.append(mass_row)
    rhs.append(52)
    row_labels.append(["high_rational_dimension_square_mass"])

    phase_rhs=list(phase.rhs_for([-1,1,1,1,1,1,1]))
    phase_start=len(rows)
    rows.extend({} for _ in phase_rhs)
    rhs.extend(int(x) for x in phase_rhs)
    row_labels.extend(["saturated_phase",*label] for label in phase.rows)
    phase_map={}
    low_used=set()
    high_phase={v:[] for v,j in highs.items() if _rational_ratio(v)}
    skipped=0
    for old in sorted(phase.allowed):
        if old<phase.offset:
            group,v,dim=phase.low[old]
            key=(int(phase.meta["low_character_labels"][group]),tuple(v))
            target=lows.get(key)
            if target is None:
                skipped+=1
                continue
            low_used.add(target)
        elif old<phase.high_end:
            orbit,trace=divmod(old-phase.offset,phase.nt)
            members=phase.orbits[orbit]
            require(len(members)==1,"Unexpected high duality compression")
            v=(0,)+tuple(phase.a["high"][members[0]][0])
            require(_rational_ratio(v),"Residual phase cone contains an irrational-ratio variable")
            structural=highs.get(v)
            if structural is None or up[structural]==0:
                skipped+=1
                continue
            target=len(lo)
            lo.append(0)
            up.append(up[structural])
            integrality.append(0)
            variable_labels.append(["continuous_relative_trace",list(v),int(trace)])
            high_phase[v].append(target)
        else:
            # This is a convex compression of rotation eigenvalue data.
            # Its nonnegative weights are bounded by a rotation_sum row.
            col=phase.column(old)
            sums=[int(phase_rhs[i]) for i,a in col.items() if phase.rows[i][0]=="rotation_sum" and a==1]
            require(len(sums)==1 and sums[0]>=0,"Rotation auxiliary lacks a complete finite sum bound")
            target=len(lo)
            lo.append(0)
            up.append(sums[0])
            integrality.append(0)
            variable_labels.append(["continuous_rotation_compression",int(old-phase.high_end)])
        phase_map[old]=target
        for i,a in phase.column(old).items():
            a=Q(a)
            require(a.denominator==1,"Phase coefficient is not integrally scaled")
            row=rows[phase_start+i]
            row[target]=row.get(target,0)+int(a)
            if not row[target]:
                del row[target]
    for j in lows.values():
        if j not in low_used:
            up[j]=0
    # The actual counts must equal the total phase mass at each restriction
    # vector. Both earlier domains use the same source basis and one copy
    # per (self-dual) high restriction type. Irrational fixed contributions
    # were already removed from the phase RHS and are handled above.
    coupling_count=0
    for v,j in sorted(highs.items()):
        if not _rational_ratio(v):
            continue
        row={j:1}
        for target in high_phase.get(v,[]):
            row[target]=-1
        rows.append(row)
        rhs.append(0)
        row_labels.append(["phase_center_count_coupling",list(v)])
        coupling_count+=1

    require(len(lo)==len(up)==len(integrality)==len(variable_labels),"Variable vector lengths")
    require(all(type(u) is int and u>=0 for u in up),"All variables must have finite exact bounds")
    require(all(all(type(j) is int and 0<=j<len(lo) and type(a) is int for j,a in row.items()) for row in rows),"Sparse row index/coefficient invariant")
    require(all(kind==0 for kind,label in zip(integrality,variable_labels) if label[0] in ("continuous_relative_trace","continuous_rotation_compression")),"A compressed phase weight was incorrectly declared integral")
    model = {
        "id":CASE+"_"+branch_name,
        "case":CASE,
        "n":len(lo),
        "rows":rows,
        "rhs":rhs,
        "lo":lo,
        "up":up,
        "integrality":integrality,
        "variable_labels":variable_labels,
        "row_labels":row_labels,
        "theory_scope":"Necessary system for a pseudo-unitary Galois form of any hypothetical complex categorification; relies on the separately recorded general-to-spherical/Galois reduction and the saturated-conductor/five-branch proof. Feasibility is not a categorification.",
        "coverage_group":CASE+"_surviving_V4_two_sector_alternatives",
        "closure_status_policy":"EXCLUSION_CANDIDATE_REVIEW_REQUIRED even if both tasks receive exact contradiction certificates; analytic coverage must be reviewed",
        "complete_branch_set":COMPLETE_BRANCH_SET,
        "prerequisites":[
            "39 of the 40 saturated Gram/second-indicator branches have prior exact certificates",
            "The remaining branch has V=4,U=0 and indicators (-1,1,1,1,1,1,1)",
            "The complete residual irrational sector is either 18 copies of 2z or 72 copies of z",
            "The Galois image of unit restricts to (1,0,2,2,2,2,2,2)"
        ],
        "novelty":"Joint mixed-integer intersection of the prior integer Gram/S/cubic/joint-Galois/source-unit system and the latest saturated phase/rotation/STS cone, with shared low choices and exact per-restriction count coupling. The previous rational witness alone does not solve this system.",
        "tensor_sha256":TENSOR_SHA256,
        "statistics":{
            "original_integer_variables":n0,
            "original_integer_rows":nr,
            "phase_rows":len(phase_rhs),
            "count_coupling_rows":coupling_count,
            "continuous_variables":sum(x==0 for x in integrality),
            "forced_zero_low_choices":forced_zero_low,
            "irrational_sector_count":sector_count,
            "irrational_sector_vector":list(sector_vector),
            "phase_columns_removed_by_exact_integer_support":skipped
        }
    }
    projected=project_fixed(model)
    model["fixed_projection"]=projected["fixed_projection"]
    model["projected_model_sha256"]=projected["projected_model_sha256"]
    return model


def project_fixed(model):
    """Exactly substitute fixed variables; expose any identical branch searches.

    The returned necessary model is equivalent to the input under the explicit
    free-variable index map and fixed assignments. No numerical presolve or
    rounding enters this transformation. A candidate/witness or contradiction
    for this model must retain this projection metadata for full replay.
    """
    fixed_q={j:Q(a) for j,(a,b) in enumerate(zip(model["lo"],model["up"])) if a==b}
    require(all(a.denominator==1 for a in fixed_q.values()),"R1768 fixed bounds must be integral; no truncation permitted")
    fixed={j:int(a) for j,a in fixed_q.items()}
    free=[j for j in range(model["n"]) if j not in fixed]
    mapping={old:new for new,old in enumerate(free)}
    rows=[];rhs=[];labels=[];source_rows=[];zero_rows=[]
    for i,(row,b) in enumerate(zip(model["rows"],model["rhs"])):
        row={int(j):Q(a) for j,a in row.items()}
        require(all(a.denominator==1 for a in row.values()),"R1768 projected coefficients must be integral")
        b=Q(b)-sum(Q(a)*fixed[j] for j,a in row.items() if j in fixed)
        out={mapping[j]:int(a) for j,a in row.items() if j in mapping and a}
        require(b.denominator==1,"Fixed projection RHS must remain integral")
        if not out and not b:
            zero_rows.append(i)
            continue
        rows.append(out);rhs.append(int(b));source_rows.append(i)
        labels.append(model["row_labels"][i])
    canonical={"n":len(free),"rows":rows,"rhs":rhs,
               "lo":[model["lo"][j] for j in free],
               "up":[model["up"][j] for j in free],
               "integrality":[model["integrality"][j] for j in free]}
    original={key:model[key] for key in ("n","rows","rhs","lo","up","integrality")}
    metadata={"original_model_sha256":digest(original),"free_variable_indices":free,
              "fixed_assignments":{str(j):v for j,v in fixed.items()},
              "retained_source_rows":source_rows,"discarded_exact_zero_rows":zero_rows,
              "original_variables":model["n"],"original_rows":len(model["rows"])}
    return {**canonical,"id":model["id"]+"_fixed_projection","case":model["case"],
            "variable_labels":[model["variable_labels"][j] for j in free],
            "row_labels":labels,"fixed_projection":metadata,
            "projected_model_sha256":digest(canonical),
            "complete_branch_set":model["complete_branch_set"],
            "theory_scope":model["theory_scope"],
            "closure_status_policy":model["closure_status_policy"]}


def build_models(vendor_root:Path, case:str=CASE, out:Path|None=None, limit=None):
    require(case==CASE,"This case adapter handles only "+CASE)
    phase_module,phase,system,reports=_setup(vendor_root)
    package_root=Path(vendor_root).resolve()
    loaded={}
    for module in tuple(sys.modules.values()):
        name=getattr(module,"__file__",None)
        if name:
            path=Path(name).resolve()
            if path.suffix==".py" and package_root in path.parents:
                loaded[path.relative_to(package_root).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    if out is not None:
        Path(out).mkdir(parents=True,exist_ok=True)
        (Path(out)/"r1768_source_closure.json").write_text(json.dumps(loaded,sort_keys=True,indent=2)+"\n")
    for number,(branch,vector,count) in enumerate(BRANCHES):
        if limit is not None and number>=int(limit):
            break
        model=_assemble(system,phase,branch,vector,count)
        model["source_closure_sha256"]=digest(loaded)
        model["source_closure"]=loaded
        model["integer_support_reports_sha256"]=digest(reports)
        model["all_branches_exported"]=limit is None or int(limit)>=len(BRANCHES)
        yield model


def _coverage_check(phase_module, vendor_root):
    """Replay all prior branch certificates before treating two tasks as exhaustive.

    This validates the finite arithmetic and exact certificates. The analytic
    saturated-conductor and modular-Galois proofs still require mathematical
    review before any general non-categorifiability claim.
    """
    latest=Path(vendor_root)/"evidence/rank8_creative_20261022/r1768"
    setup=phase_module._laptop_base_setup
    arithmetic=_module("_laptop_r1768_arithmetic",latest/"verify_arithmetic.py")
    arithmetic_result=arithmetic.run(setup)
    require(arithmetic_result==json.loads((latest/"arithmetic_verification.json").read_text()), "Prior finite-sector arithmetic changed")
    fibres=sys.modules["finite_fibres_cone"]
    branch_result=fibres.run(0,True,setup)
    require(branch_result["checked"]==40 and branch_result["rejected"]==39 and branch_result["survivors"]==[(4,[-1,1,1,1,1,1,1])], "Prior branch certificate coverage differs")
    phase_result=phase_module.main(True,0,setup)
    require(phase_result["status"]=="exact_feasible", "Known phase positive control changed")
    return {"status":"PASS","tensor_sha256":TENSOR_SHA256,
            "prior_branch_count":40,"prior_exact_rejections":39,
            "remaining_V4_integer_sector_branches":COMPLETE_BRANCH_SET,
            "finite_arithmetic_sha256":digest(arithmetic_result),
            "new_exclusion":False,
            "analytic_proofs":"Saturated-conductor, signed-prime support, modular Galois, pointed and general-to-Galois reductions remain mathematical prerequisites."}


def coverage_check(vendor_root:Path):
    phase_module,phase,system,reports=_setup(vendor_root)
    return _coverage_check(phase_module,vendor_root)


def self_test(vendor_root:Path):
    phase_module,phase,system,reports=_setup(vendor_root)
    known=Path(vendor_root)/"evidence/rank8_creative_20261022/r1768/unit_orbit_cone.json"
    receipt=json.loads(known.read_text())
    require(receipt["tensor_sha256"]==TENSOR_SHA256 and receipt["status"]=="exact_feasible","Frozen positive phase-cone control")
    phase.check_feasible(receipt["certificate"]["indices"],receipt["certificate"]["weights"],[-1,1,1,1,1,1,1])
    require(system.metadata["rows"]==521 and system.metadata["variables"]==2610,"Prior integer center control changed")
    answers=[];projection_hashes=[]
    for branch,vector,count in BRANCHES:
        model=_assemble(system,phase,branch,vector,count)
        require(model["statistics"]["phase_rows"]==241,"Expected full retained phase equations")
        require(model["statistics"]["count_coupling_rows"]>0,"Missing new count coupling")
        require(model["statistics"]["continuous_variables"]>0,"The phase cone must not become integral")
        require(model["id"] in model["complete_branch_set"],"Branch coverage mismatch")
        rows=[(r,b) for r,b,label in zip(model["rows"],model["rhs"],model["row_labels"]) if label[0]=="irrational_ratio_sector_count"]
        require(len(rows)==1 and rows[0][1]==count,"Sector branch count constraint")
        projected=project_fixed(model)
        require(projected["projected_model_sha256"]==model["projected_model_sha256"],"Fixed projection digest differs")
        projection_hashes.append(model["projected_model_sha256"])
        answers.append({"id":model["id"],"n":model["n"],"rows":len(model["rows"]),"projected_n":projected["n"],"projected_rows":len(projected["rows"]),"projected_model_sha256":model["projected_model_sha256"],"statistics":model["statistics"]})
    prior_coverage=_coverage_check(phase_module,vendor_root)
    return {"status":"PASS","canonical_tensor":TENSOR_SHA256,"known_exact_rational_phase_witness":"rechecked","prior_branch_coverage":prior_coverage,"branches":answers,"both_sector_models_identical_after_exact_fixed_substitution":len(set(projection_hashes))==1,"scope":"Builder/source/positive-phase and prior-certificate controls; not a categorification or a new exclusion"}
