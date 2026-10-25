#!/usr/bin/env python3
"""Publish verified realized based-ring representatives and reproducible invariants.

The input catalogues assert categorical models. This script checks their ring
tensors, derives algebraic invariants, and never infers existence from a tensor.
"""
import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent

R5_LABELS = {
    "Vec(C5)": (1, 16), "TY(C4)": (1, 11), "TY(C2xC2)": (1, 1),
    "SU(2)_4": (1, 3), "Rep(D14)": (1, 4), "Rep(S4)": (1, 6),
    "PSU(2)_8": (1, 7), "PSU(2)_9": (1, 10), "LPR-12": (1, 13),
    "LPR-24": (1, 14), "Rep(A5)": (2, 27),
    "Rep(C7 semidirect C3)": (2, 37), "PSU(3)_4": (2, 36),
    "Rep(AGL(1,5))": (3, 75), "Izumi C3+6 equivariantization": (3, 40),
    "Izumi V4+4": (4, 55), "Izumi C4+4": (4, 123),
}


def r3(k, l, m, n):
    result = np.zeros((3, 3, 3), dtype=int)
    result[0] = np.eye(3, dtype=int)
    result[:, 0, :] = np.eye(3, dtype=int)
    result[1, 1] = [1, m, k]
    result[2, 2] = [1, l, n]
    result[1, 2] = result[2, 1] = [0, k, l]
    return result.tolist()


def identify_pointed_order_eight(tensor):
    """Recognize the five groups of order eight by multiplication and orders."""
    n=len(tensor)
    if n!=8 or any(sum(tensor[i][j])!=1 for i in range(n) for j in range(n)):
        raise ValueError("Expected pointed ring of rank eight")
    product=lambda i,j:tensor[i][j].index(1)
    orders=[]
    for i in range(n):
        value=0
        for k in range(1,9):
            value=product(value,i)
            if value==0:orders.append(k);break
        else:raise ValueError("Element order exceeds group size")
    summary=Counter(orders)
    commutative=all(product(i,j)==product(j,i) for i in range(n) for j in range(n))
    cases={(True,((1,1),(2,1),(4,2),(8,4))):"C8",
           (True,((1,1),(2,3),(4,4))):"C4×C2",
           (True,((1,1),(2,7))):"C2×C2×C2",
           (False,((1,1),(2,5),(4,2))):"D8",
           (False,((1,1),(2,1),(4,6))):"Q8"}
    result=cases.get((commutative,tuple(sorted(summary.items()))))
    if not result:raise ValueError(f"Unrecognized group of order eight: {summary}")
    return result


def rank8_source_tensor(record):
    """Convert the sourced model basis to the pinned census basis, and hash it."""
    n=8
    sources=[]
    for ctor in record["constructors"]:
        model=ctor["tensor"]
        perm=ctor["basis_map_source_to_model"]
        if sorted(perm)!=list(range(n)) or perm[0]!=0:
            raise ValueError(f"Invalid source-to-model permutation for {record['id']}")
        source=[[[model[perm[i]][perm[j]][perm[k]] for k in range(n)]
                 for j in range(n)] for i in range(n)]
        if sha_tensor(source)!=record["tensor_sha256"]:
            raise ValueError(f"Rank-eight source hash mismatch for {record['id']}")
        sources.append(source)
    if not sources or any(s!=sources[0] for s in sources[1:]):
        raise ValueError(f"Rank-eight constructors disagree on the source tensor: {record['id']}")
    return sources[0]


def tensor_checks(tensor):
    a = np.asarray(tensor, dtype=np.int64)
    rank = a.shape[0]
    if a.shape != (rank, rank, rank) or np.min(a) < 0:
        raise ValueError("Invalid fusion tensor shape or negative coefficient")
    eye = np.eye(rank, dtype=np.int64)
    if not np.array_equal(a[0], eye) or not np.array_equal(a[:, 0, :], eye):
        raise ValueError("Basis unit is not indexed zero")
    dual = []
    for i in range(rank):
        js = [j for j in range(rank) if a[i, j, 0] == 1]
        if len(js) != 1 or any(a[i, j, 0] not in (0, 1) for j in range(rank)):
            raise ValueError("Malformed duality")
        dual.append(js[0])
    for i in range(rank):
        for j in range(rank):
            for k in range(rank):
                if not np.array_equal(a[i, j] @ a[:, k, :], a[j, k] @ a[i, :, :]):
                    raise ValueError(f"Associativity failure {i},{j},{k}")
    return a, dual


def clean_float(value):
    value = float(value)
    if abs(value) < 1e-10:
        return 0.0
    return round(value, 10)


def display_complex(z):
    z = complex(z)
    x, y = clean_float(z.real), clean_float(z.imag)
    if abs(y) <= 1e-9:
        return x
    return {"re": x, "im": y}


def invariants(tensor):
    a, dual = tensor_checks(tensor)
    n = len(dual)
    commutative = bool(np.array_equal(a, a.transpose(1, 0, 2)))
    matrices = [a[i].astype(float) for i in range(n)]
    weights = np.arange(1, n + 1)
    operator = sum((w * mat for w, mat in zip(weights, matrices)), np.zeros((n, n)))
    values, vectors = np.linalg.eig(operator)
    fp_idx = int(np.argmax(np.real(values)))
    d = np.real(vectors[:, fp_idx] / vectors[0, fp_idx])
    if any(x <= 0 for x in d) or any(np.linalg.norm(m @ d - d[i] * d) > 1e-6 for i, m in enumerate(matrices)):
        raise ValueError("Positive common dimension character not certified numerically")
    inv = {
        "dual_indices": dual,
        "invertible_indices": [i for i in range(n) if int(np.sum(a[i, dual[i]])) == 1],
        "commutative": commutative,
        "frobenius_perron_dimensions_approx": [clean_float(v) for v in d],
        "global_fp_dimension_approx": clean_float(np.dot(d, d)),
        "dimensions_method": "Numerical Perron eigenvector, normalized at the tensor unit; approximate values.",
    }
    omega = sp.zeros(n)
    for i in range(n):
        omega += sp.Matrix(a[i].tolist()) * sp.Matrix(a[dual[i]].tolist())
    t = sp.Symbol("t")
    inv["central_casimir_polynomial"] = str(sp.factor(omega.charpoly(t).as_expr()))
    if commutative:
        # The codegree polynomial is exact; each row of the character table
        # is a numerical simultaneous eigencharacter, checked against every N_i.
        inv["formal_codegree_polynomial"] = inv["central_casimir_polynomial"]
        chars = None
        rng = np.random.default_rng(760121 + n)
        for trial in range(40):
            if trial:
                other = sum((w * mat for w, mat in zip(rng.integers(1, 10000, n), matrices)),
                            np.zeros((n,n)))
                _, eigenvectors = np.linalg.eig(other)
            else:
                eigenvectors = vectors
            trial_chars = []
            for column in range(n):
                vec = eigenvectors[:, column]
                row = [complex(np.vdot(vec, m @ vec) / np.vdot(vec, vec)) for m in matrices]
                error = max(float(np.linalg.norm(m @ vec - x * vec)) for m, x in zip(matrices, row))
                if error > 1e-6:
                    break
                codegree = sum(row[i] * row[dual[i]] for i in range(n))
                trial_chars.append({"values_approx": [display_complex(z) for z in row],
                                    "formal_codegree_approx": display_complex(codegree)})
            if len(trial_chars)==n and np.linalg.matrix_rank(eigenvectors)==n:
                chars=trial_chars
                break
        if chars is None:
            raise ValueError("Could not stably separate simultaneous eigencharacters")
        chars.sort(key=lambda c: (
            -float(c["formal_codegree_approx"] if isinstance(c["formal_codegree_approx"], float)
                   else c["formal_codegree_approx"]["re"]),
            str(c["values_approx"])))
        inv["irreducible_characters_approx"] = chars
        inv["character_method"] = "Numerical simultaneous eigencharacters of the integral fusion matrices; approximate values."
        inv["exact_character_presentation"] = primitive_presentation(a,dual)
    else:
        try:
            inv.update(noncommutative_characters(a, dual, omega.charpoly(t).as_expr()))
        except (ValueError, np.linalg.LinAlgError):
            inv["character_method"] = "Noncommutative algebra: numerical irreducible-character decomposition could not be validated."
    return inv


def primitive_presentation(a,dual):
    """Exact Q[θ] presentation of all one-dimensional characters.

    For an integral combination H with squarefree P=charpoly(H), the
    regular algebra is Q[H]. Express every basis multiplication matrix as
    a rational polynomial in H and verify its matrix identity exactly.
    """
    n=len(dual);mats=[sp.Matrix(a[i].tolist()) for i in range(n)]
    theta=sp.Symbol("theta")
    rng=np.random.default_rng(27403+n)
    for attempt in range(60):
        weights=[int(x) for x in rng.integers(1,51,n)] if attempt else list(range(1,n+1))
        H=sum((w*m for w,m in zip(weights,mats)),sp.zeros(n))
        polynomial=H.charpoly(theta).as_expr()
        if sp.gcd(polynomial,sp.diff(polynomial,theta))!=1:
            continue
        powers=[H**j for j in range(n)]
        columns=sp.Matrix.hstack(*(sp.Matrix(list(p)) for p in powers))
        if columns.rank()!=n:continue
        polys=[]
        for mat in mats:
            coefficients=columns.gauss_jordan_solve(sp.Matrix(list(mat)))[0]
            if any(x.free_symbols for x in coefficients):raise ValueError("Nonunique primitive expression")
            expr=sp.expand(sum(coefficients[j]*theta**j for j in range(n)))
            assert sum((coefficients[j]*powers[j] for j in range(n)),sp.zeros(n))==mat
            polys.append(expr)
        codegree=sp.rem(sum(polys[i]*polys[dual[i]] for i in range(n)),polynomial,theta)
        return {
            "exact_generator":"theta = Σ_i w_i X_i (character value at a root of P)",
            "generator_weights":weights,
            "primitive_polynomial":str(sp.factor(polynomial)),
            "basis_values": [str(p) for p in polys],
            "codegree_value":str(sp.factor(codegree)),
            "instruction":"For each complex root θ of P(θ)=0, substitute θ into the displayed polynomials to obtain one exact irreducible character and its formal codegree. All matrix identities N_i=p_i(H) were checked over Q."
        }
    raise ValueError("No separating integral central generator in 60 tries")


def noncommutative_characters(a, dual, casimir_polynomial):
    """Numerical block traces from an exact center basis of the regular algebra.

    If a central eigenspace has dimension d², it is d copies of a degree-d
    irreducible; its regular trace divided by d gives that character. We
    validate center commutation, square block sizes and character orthogonality.
    """
    n=len(dual)
    exact=[sp.Matrix(a[i].tolist()) for i in range(n)]
    columns=[]
    for j in range(n):
        entries=[]
        for mat in exact:
            comm=exact[j]*mat-mat*exact[j]
            entries.extend(comm)
        columns.append(sp.Matrix(entries))
    basis=sp.Matrix.hstack(*columns).nullspace()
    centers=[]
    for vec in basis:
        z=sum((float(vec[i])*np.asarray(a[i],dtype=float) for i in range(n)),np.zeros((n,n)))
        if max(np.linalg.norm(z@np.asarray(mat,dtype=float)-np.asarray(mat,dtype=float)@z)
               for mat in a)>1e-9:
            raise ValueError("Exact center kernel fails numeric commutator")
        centers.append(z)
    rng=np.random.default_rng(164103+n)
    for trial in range(100):
        weights=rng.integers(1,300, len(centers))
        z=sum((float(w)*mat for w,mat in zip(weights,centers)),np.zeros((n,n)))
        values,vectors=np.linalg.eig(z)
        clusters=[]
        for i,v in enumerate(values):
            matching=next((cluster for cluster in clusters if abs(v-values[cluster[0]])<1e-6),None)
            if matching is None:clusters.append([i])
            else:matching.append(i)
        if len(clusters)!=len(centers):
            continue
        degrees=[math.isqrt(len(cluster)) for cluster in clusters]
        if any(d*d!=len(cluster) for d,cluster in zip(degrees,clusters)) or np.linalg.cond(vectors)>1e9:
            continue
        inverse=np.linalg.inv(vectors)
        chars=[]
        for cluster,d in zip(clusters,degrees):
            projector=vectors[:,cluster]@inverse[cluster,:]
            row=[complex(np.trace(projector@np.asarray(mat,dtype=float))/d) for mat in a]
            # Nonreal characters are valid; only χ(1) must equal the degree.
            if abs(row[0]-d)>1e-6:
                raise ValueError("Irreducible character degree mismatch")
            codegree=sum(row[i]*row[dual[i]] for i in range(n))/d
            chars.append((row,d,codegree))
        if any(abs(sum(row[i]*other[dual[i]] for i in range(n)))>1e-5
               for j,(row,_,_) in enumerate(chars) for k,(other,_,_) in enumerate(chars) if j!=k):
            continue
        if any(abs(codegree.imag)>1e-5 or codegree.real<=0 for _,_,codegree in chars):
            continue
        if abs(sum(d/codegree.real for _,d,codegree in chars)-1)>1e-5:
            continue
        # A central Casimir eigenvalue on the degree-d block equals d*f_E.
        # Exact irreducible factors of its characteristic polynomial give
        # defining polynomials for the individual formal codegrees. Assign
        # factors only when the numerically validated eigenvalue matches a
        # unique exact factor to the stated tolerance.
        t,u=sp.symbols("t u")
        factors=sp.factor_list(casimir_polynomial,t)[1]
        root_groups=[(sp.Poly(poly,t),[complex(z) for z in sp.nroots(poly,n=30,maxsteps=200)])
                     for poly,_ in factors]
        listed=[]
        for row,d,codegree in chars:
            target=d*codegree
            matches=sorted(((min(abs(target-root) for root in roots),poly)
                            for poly,roots in root_groups),key=lambda pair:pair[0])
            error,poly=matches[0]
            if error>1e-5*max(1,abs(target)):
                raise ValueError("Irreducible Casimir eigenvalue has no exact polynomial match")
            if len(matches)>1 and matches[1][0]<1e-5*max(1,abs(target)):
                raise ValueError("Irreducible Casimir eigenvalue matches multiple exact factors")
            degree=poly.degree()
            codegree_poly=sp.Poly(poly.as_expr().subs(t,d*u)/d**degree,u).monic()
            entry={"degree":d,"values_approx":[display_complex(x) for x in row],
                   "formal_codegree_approx":display_complex(codegree),
                   "formal_codegree_minimal_polynomial":str(sp.factor(codegree_poly.as_expr()))}
            if degree==1:
                entry["formal_codegree_exact"]=str(-codegree_poly.all_coeffs()[1])
            listed.append(entry)
        listed.sort(key=lambda c:(-c["degree"],str(c["values_approx"])))
        return {"irreducible_characters_approx":listed,
                "character_method":"Numerical regular-algebra block traces after exact rational center-kernel computation; χ_E(X_i) and f_E=(Σ_i χ_E(X_i)χ_E(X_i*)) / dim(E) are approximate. The displayed codegree minimal polynomials are exact factors of the rational central-Casimir polynomial rescaled by each irreducible degree; factor association uses the validated numerical eigenvalues. Orthogonality and block dimensions validated."}
    raise ValueError("Could not separate exact center into square-dimensional regular blocks")


def sha_tensor(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()


def model_link(reference):
    # Prefer a published DOI when the catalogue supplies one.
    doi = re.search(r"(?:https://doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s;,]+)", reference, re.I)
    if doi:
        return "https://doi.org/" + doi.group(1).rstrip(".")
    match=re.search(r"arXiv:(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?",reference,re.I)
    if match:
        return f"https://arxiv.org/abs/{match.group(1)}"
    # These abbreviations identify specific papers in the source catalogues.
    # Only attach an external link when that citation is actually present.
    for marker,arxiv in (
        ("LPR", "2010.10264"),
        ("Liu–Palcoux–Ren", "2010.10264"),
        ("EIP", "2108.01564"),
        ("Grossman--Snyder", "1102.2631"),
        ("Evans--Jones", "2404.14466"),
        ("Hong–Rowell", "0907.1051"),
        ("Izumi,", "1512.04288"),
    ):
        if marker in reference:
            return f"https://arxiv.org/abs/{arxiv}"
    return None


def make_record(rank, label, name, tensor, reference, source_path, source_location, existence="unitary",reference_url=None):
    rank = int(rank)
    tensor = np.asarray(tensor, dtype=int).tolist()
    if len(tensor) != rank:
        raise ValueError(f"Rank mismatch for {label}")
    multiplicity = max(x for mat in tensor for row in mat for x in row)
    ref_url=reference_url or model_link(reference)
    if ref_url and not ref_url.startswith("https://"):
        raise ValueError(f"Model source is not an HTTPS URL: {label}")
    return {
        "rank": rank,
        "multiplicity": multiplicity,
        "id": label,
        "name": name,
        "existence": existence,
        "fusion_tensor": tensor,
        "tensor_sha256": sha_tensor(tensor),
        "basis": [f"X{i}" for i in range(rank)],
        "model_reference": reference,
        "model_reference_url":ref_url,
        "source_file": source_path,
        "source_location": source_location,
        "invariants": invariants(tensor),
    }


def rank_two_and_three():
    result = []
    for name, tensor, reference in [
        ("Vec(C2)", [[[1, 0], [0, 1]], [[0, 1], [1, 0]]], "Rank-two manuscript, classification theorem and final model paragraph: the pointed category Vec(C2); Ostrik, Fusion categories of rank 2 (2003)."),
        ("Fibonacci", [[[1, 0], [0, 1]], [[0, 1], [1, 1]]], "Rank-two manuscript, classification theorem and final model paragraph: Fibonacci as the even part of SU(2)3; Ostrik, Fusion categories of rank 2 (2003)."),
    ]:
        result.append(make_record(2, f"R2_1_{len(result)+1}", name, tensor, reference,
                                  "manuscripts/rank2.tex", "Classification theorem and final model paragraph",
                                  reference_url="https://arxiv.org/abs/math/0203255"))
    c3 = [[[1 if k == (i+j)%3 else 0 for k in range(3)] for j in range(3)] for i in range(3)]
    for name, tensor in [
        ("Vec(C3)", c3), ("Ising", r3(1,0,0,0)), ("Rep(S3)", r3(1,0,1,0)),
        ("E6 even part", r3(1,0,2,0)), ("PSU(2)5", r3(1,1,1,0)),
    ]:
        multiplicity=max(x for matrix in tensor for row in matrix for x in row)
        index=1+sum(r["rank"]==3 and r["multiplicity"]==multiplicity for r in result)
        result.append(make_record(3, f"R3_{multiplicity}_{index}", name, tensor,
                                  "Rank-three manuscript, Corollary on the five rings and its table of standard unitary models; Ostrik, Pivotal fusion categories of rank 3 (2015).",
                                  "manuscripts/rank3.tex", "Corollary on the five rings, model table",
                                  reference_url="https://arxiv.org/abs/1309.4822"))
    return result


def from_catalogues(repo):
    records = rank_two_and_three()
    p4 = "supplements/rank4/data/models.json"
    for model in json.loads((repo/p4).read_text()):
        refs = "; ".join(model.get("references", []))
        m=int(re.search(r"F_\{(\d+),",model["label"]).group(1))
        url=("https://arxiv.org/abs/2010.10264" if m==1 else
             "https://arxiv.org/abs/2108.01564" if model["label"]=="F_{2,2}" else
             "https://arxiv.org/abs/1102.2631" if model["label"]=="F_{2,15}" else
             "https://arxiv.org/abs/2404.14466" if model["label"]=="F_{3,19}" else
             "https://arxiv.org/abs/1512.04288" if model["label"] in ("F_{3,24}","F_{6,81}") else None)
        records.append(make_record(4, model["label"], model["model"].replace("_", " "), model["matrices"],
                                   f"Rank-four manuscript, model catalogue; {refs}.", p4, model["label"],reference_url=url))
    p5 = "supplements/rank5/data/positive_models.json"
    ref5 = "Rank-five manuscript, Section 'Unitary realizations', Table of the seventeen positive rings"
    for model in json.loads((repo/p5).read_text()):
        name = model["name"]
        m, j = R5_LABELS[name]
        ref = ref5
        if name.startswith("LPR-"):
            ref += "; Liu–Palcoux–Ren, Lett. Math. Phys. 112 (2022), article 54, Sections 3.5, 4.2, 4.4"
        elif name.startswith("Izumi"):
            ref += "; Izumi, arXiv:1512.04288v2, " + ("Example 13.10" if "equivariantization" in name else "Examples 9.5–9.6")
        elif name == "PSU(3)_4":
            ref += "; Hong–Rowell, J. Algebra 324 (2010), 1000–1015"
        else:
            ref += "; standard unitary realization as specified in that section"
        url=("https://arxiv.org/abs/2010.10264" if name.startswith("LPR-") else
             "https://arxiv.org/abs/1512.04288" if name.startswith("Izumi") else
             "https://arxiv.org/abs/0907.1051" if name=="PSU(3)_4" else None)
        record = make_record(5, f"R5_{m}_{j}", name, model["tensor"], ref, p5, name,reference_url=url)
        if record["multiplicity"] != m:
            raise ValueError(f"Rank-five model band mismatch: {name}")
        records.append(record)
    p6 = "supplements/rank6/data/model_catalog.json"
    cache = {}
    for model in json.loads((repo/p6).read_text()):
        ctor = model["constructors"][0]
        reg = ctor["registry"]
        if reg not in cache:
            cache[reg] = json.loads((repo/"supplements/rank6/data"/reg).read_text())
        match = next((x for x in cache[reg] if x.get("id")==model["id"]), None)
        if match is None:
            raise ValueError(f"No exact rank-six model tensor for {model['id']} in {reg}")
        tensor = match.get("N") or match.get("tensor")
        rec = make_record(6, model["id"], ctor["name"], tensor,
                          f"Rank-six manuscript, positive model catalogue, {model['id']}; {ctor['reference']}.",
                          f"supplements/rank6/data/{reg}", model["id"],
                          "unitary" if model["existence"].get("unitary")=="yes" else "spherical, non-pseudo-unitary")
        if rec["multiplicity"] != model["multiplicity"]:
            raise ValueError(f"Rank-six model band mismatch: {model['id']}")
        rec["basis_permutation_model_to_census"] = ctor.get("basis_permutation")
        rec["alternative_models"] = [
            {"name":other["name"],"reference":other["reference"],
             "source_url":model_link(other["reference"]),
             "basis_permutation_model_to_census":other.get("basis_permutation")}
            for other in model["constructors"][1:]]
        records.append(rec)
    p7 = "supplements/rank7/data/model_catalog.json"
    if (repo/p7).exists():
        for model in json.loads((repo/p7).read_text()):
            rec=make_record(7,model["id"],model["name"],model["tensor"],
                            f"Rank-seven manuscript, positive model catalogue, {model['id']}; {model['source_reference']}; construction: {model['source_construction']}.",
                            p7,model["id"],"unitary" if model["existence"].get("unitary")=="yes" else "realized",
                            reference_url=model.get("source_url"))
            if rec["multiplicity"]!=model["multiplicity"]:
                raise ValueError(f"Rank-seven model band mismatch: {model['id']}")
            rec["basis_permutation_model_to_census"] = model.get("basis_permutation_model_to_census")
            records.append(rec)
    import sys
    sys.path.insert(0, str(repo / "tools"))
    from rank8_publication import model_path
    p8 = model_path(repo)
    if (repo/p8).exists():
        for model in json.loads((repo/p8).read_text()):
            first=model["constructors"][0]
            source_tensor=rank8_source_tensor(model)
            name=first["model"]
            ref=f"Rank-eight manuscript, positive model catalogue, {model['id']}; {first['reference']}"
            reference_url=first.get("source_url")
            if model['id'] in ('R8_3_331','R8_3_471'):
                ref += '; Calegari–Morrison–Snyder, arXiv:1004.0665, Appendix A by Ostrik, Proposition A.4.1 (C3+3), followed by the stated Deligne product'
                reference_url='https://arxiv.org/abs/1004.0665'
            if model['id'] in ('R8_3_1456','R8_3_3314'):
                ref += '; Kirillov–Ostrik, arXiv:math/0101219, E8 construction and its adjoint category, followed by the stated Deligne product'
                reference_url='https://arxiv.org/abs/math/0101219'
            if name=="Vec(G), |G|=8":
                group=identify_pointed_order_eight(source_tensor)
                name="Vec(dihedral group of order 8)" if group=="D8" else f"Vec({group})"
                ref+="; group identified from the exact multiplication table by element orders and commutativity"
            rec=make_record(8,model["id"],name,source_tensor,ref+".",
                            p8,model["id"],model.get("model_scope", "unitary"),reference_url=reference_url)
            construction=first.get('construction',{})
            rec['construction_notes']=[construction[key] for key in ('kind','cocycle','identification','basis_map_scope','human_review')
                                       if isinstance(construction.get(key),str)]
            if isinstance(construction.get('proof'),str):
                proof=construction['proof']
                if not proof.startswith('evidence/'):
                    certificate=model.get('source_certificate')
                    candidate=(Path(certificate).parent/proof).as_posix() if isinstance(certificate,str) else None
                    proof=candidate if candidate and (repo/candidate).is_file() else 'evidence/rank8_m3_20261021/models/'+proof
                if not (repo/proof).is_file():
                    raise ValueError('Missing construction proof: '+proof)
                rec['construction_proof_file']=proof
            if rec["multiplicity"]!=model["multiplicity"]:
                raise ValueError(f"Rank-eight model band mismatch: {model['id']}")
            rec["basis_permutation_census_to_model"] = first["basis_map_source_to_model"]
            rec["alternative_models"]=[{"name":other["model"],"reference":other["reference"],
                                         "source_url":other.get("source_url") or model_link(other["reference"]),
                                         "basis_permutation_census_to_model":other["basis_map_source_to_model"]}
                                       for other in model["constructors"][1:]]
            records.append(rec)
    from correctness_publication import active,update_models
    if active(repo):update_models(records)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--classification", type=Path, required=True)
    args = parser.parse_args()
    repo = args.classification.resolve()
    records = from_catalogues(repo)
    ids = [r["id"] for r in records]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate identifiers in positive model catalogue")
    expected = {2:2,3:5,4:15,5:17}
    expected[6] = json.loads((repo/"supplements/rank6/verification/release_summary.json").read_text())["positive"]
    if any(Counter(r["rank"] for r in records)[rank]!=n for rank,n in expected.items()):
        raise ValueError("Positive catalogue cardinality mismatch")
    records.sort(key=lambda r:(r["rank"],r["multiplicity"],r["id"]))
    out = HERE/"dist/data/realized_rings.json"
    out.write_text(json.dumps({"schema":"ring-atlas/realized/v1","records":records},ensure_ascii=False,separators=(",", ":"))+"\n")
    print("Wrote",len(records),"realized model records to",out)


if __name__ == "__main__":
    main()
