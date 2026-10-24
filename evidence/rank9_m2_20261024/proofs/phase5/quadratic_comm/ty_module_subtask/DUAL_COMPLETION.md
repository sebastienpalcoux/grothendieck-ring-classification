# Complete finite Morita-ring reduction to three uniform D8 rings

## Conclusion

Each of R9_2_137, R9_2_1607 and R9_2_1976 has exactly 28 labelled rank-twelve based-ring completions of the forced six-object Morita module. Twenty fail the pseudo-unitary formal-codegree field condition. Four further completions contain the previously excluded rank-six rings R6_4_6 or R6_4_174 as adjoint fusion subrings. The remaining four labelled completions represent **three based-ring isomorphism types**, all with uniform noninvertible multiplicity two.

This does not construct or exclude any of the three source categories. Using the previously audited general-to-pseudo-unitary existence reductions for the source rings, a general categorification of any source implies a categorification of at least one of these three uniform D8 rings. The field argument is applied after making that existence reduction and taking the Morita dual; it does not assume that an arbitrary original categorification is pseudo-unitary or unitarizable.

## 1. Exact module and full-Gram enumeration

For source involutions b1, b5 and b8 respectively, the existing complete split-involution routine gives precisely one six-object module branch in each case. The full Morita Gram matrix has rank eight and precisely ten admissible commuting right-action matrices. Solving the complete flattened Gram identity gives a unique positive multiplicity vector: each of the eight permutation matrices occurs once and each of the two noninvertible matrices occurs twice. The latter must be retained as four different simples, not merged into two.

| Source | Module rank | Gram rank | Distinct action matrices | Dual rank |
|---|---:|---:|---:|---:|
| R9_2_137 | 6 | 8 | 10 | 12 |
| R9_2_1607 | 6 | 8 | 10 | 12 |
| R9_2_1976 | 6 | 8 | 10 | 12 |

`morita_probe.py` reuses the categorical Gram identity and exhaustive image-candidate domain proved in phase three. Its exact outputs are `R9_2_*_morita_candidates.json`; all three anti-module enumerations report complete. The independently derived TY theorem in `THEOREM.md` explains the same rank-twelve dimension type and identifies the invertible group as D8.

## 2. Why the 28-completion list is exhaustive

Write H=Z(D8), Q=D8/H=V4, and label the four noninvertibles X_q by Q. Fix X=X_0. Standard two-orbit fusion-ring structure gives an automorphism theta of Q, with theta²=id, such that

X_q g = X_{q+theta(gH)}.

There is alpha in Q satisfying theta(alpha)=alpha and

X² = sum_{gH=alpha}g + sum_{q in Q} m_q X_q,

where each m_q is a nonnegative integer and their sum is eight. All products are consequently forced by

X_a X_b = sum_{gH=a+theta(b)+alpha}g + sum_q m_{q+a+theta(b)} X_q.

Duality gives X_q*=X_{theta(q)+alpha}. Associativity and Frobenius reciprocity force invariance of m under theta, translation by alpha, and translation by every element of im(1+theta). These conditions follow respectively from comparing the invertible parts of (X²)X and X(X²), applying duality to X², and comparing (X²)g with X(Xg). Thus they are necessary before any computation is performed.

The two repeated noninvertible action matrices give a nonzero homomorphism pi:Q→C2. Every possible theta, alpha and m satisfying the preceding necessary conditions is enumerated. The program then tests all 144 action-product equations, duality by transpose, all 20,736 associativity equations, and all Frobenius reciprocity equations. No retained multiplication coefficient is inferred solely from a repeated action matrix.

For a conceptual description, put ker(pi)={0,h}, where h is a reflection coset of D8, and write Q={0,h,a,a+h}. The resulting 28 completions are exactly:

1. theta=id, alpha=0, with m=(u,4-u,v,4-v) in this order, for 0≤u,v≤4: 25 cases;
2. theta=id, alpha=h, with m=(2,2,2,2): one case;
3. theta fixing h and interchanging a,a+h, with alpha=0 or h and m=(2,2,2,2): two cases.

The stored label order differs among sources and is recorded in their Q, pi and coset tables. `build_dual_candidates.py` obtains this list exhaustively rather than hard-coding it.

## 3. Uniform field obstruction for twenty cases

Consider the 25 cases in item 1. Each character lambda of Q gives one-dimensional characters of the candidate fusion ring by sending g to lambda(gH) and X to a root x of

x² - M_lambda x - 2 = 0,   M_lambda=sum_q m_q lambda(q).

The corresponding formal codegree is f=8+4x². For a nonzero M, its conjugate pair satisfies

f² -(32+4M²)f +(256+32M²)=0.

For the three nontrivial lambda, the values M are

0,  2(u+v-4),  2(u-v).

In a pseudo-unitary categorification every formal codegree belongs to the simple FP-dimension field Q(sqrt(2)): the central simple corresponding to the representation has dimension FPdim(C')/f, and its restriction is an integral combination of simples of dimensions 1 and d. For the possible even M between -8 and 8, this field condition requires M=0 or ±8. The other absolute values 2,4,6 give quadratic fields Q(sqrt(3)), Q(sqrt(6)), Q(sqrt(11)), respectively.

It follows directly that the only surviving pairs (u,v) are

(0,0), (0,4), (4,0), (4,4), (2,2).

The exact regular-Casimir calculation independently finds precisely the forbidden irreducible factors

- t²-48t+384;
- t²-96t+768;
- t²-176t+1408.

A regular-Casimir eigenvalue is the formal codegree times the integer dimension of its irreducible representation, so a field violation of this eigenvalue is enough even without resolving noncommutative representation multiplicities. In the present nonuniform cases the displayed factors also arise from the explicit one-dimensional characters above.

## 4. Four extreme cases and the lower-rank dependencies

The four corners u,v in {0,4} have rank-six adjoint subrings. Exact 216-coefficient based transports identify them with R6_4_6 or R6_4_174:

| Candidate index in each stored 28-case list | Adjoint ring | Existing status |
|---:|---|---|
| 0 | R6_4_174 | excluded, general |
| 4 | R6_4_6 | excluded, general |
| 20 | R6_4_6 | excluded, general |
| 24 | R6_4_174 | excluded, general |

The proof dependencies must remain explicit. R6_4_6 uses the project's general C4 associator/stabilizer obstruction (`c4_associator_stabilizer`). R6_4_174 uses its general stabilizer-rotation higher-indicator obstruction (`general_stabilizer_rotation_higher`) together with the two-FP-value existence reduction. This continuation checks exact tensor bindings and preserves the complete prior decision certificates in `lower_rank_dependencies.json`; it does not claim a fresh independent proof of those earlier categorical results.

## 5. The common three-ring frontier

All three source rings have the same four surviving labelled completions, indexed 12,25,26,27 in their stored lists. Every source-to-representative identification is checked on all 1,728 coefficients in `survivor_isomorphisms.json`.

| Representative | theta | alpha | Number of self-dual basis elements |
|---|---|---|---:|
| case 12 | identity | 0 | 10 |
| case 25 | identity | nonzero h | 6 |
| case 26 | interchange a,a+h | 0 | 8 |

Case 27 is isomorphic to case 26 by replacing X with X_a: alpha changes by a+theta(a)=h. Thus there are three isomorphism types. Case 25 is also isomorphic to the uniform `alpha=2,a=2` rank-twelve candidate from the R9_2_1975 continuation; the exact transport is saved. The other two types are distinct from both uniform phase-four 1975 candidates.

**Formal-codegree caution.** All three types have the same regular-Casimir polynomial, but their irreducible representation dimensions differ. The identity-theta cases have eight scalar irreducibles and one irreducible of degree two. Their formal codegrees are D,D_sigma,16 six times, and 4. The nontrivial-theta case has four scalar irreducibles and two irreducibles of degree two; its formal codegrees are D,D_sigma,16 twice,4,8. Consequently I(1) in its center has six distinguished simple summands, with multiplicities 1,1,1,1,2,2, rather than nine. `survivor_formal_codegrees.json` records the exact commutator-kernel calculation.

The remaining problem is therefore a common categorical existence problem for three uniform D8-quadratic based rings. A feasible ring completion is not an associator, and equality of a possible Morita dual ring does not prove that the three original rings are categorified or categorically Morita equivalent.

## Replay

From the research root:

    python phase5/quadratic_comm/ty_module_subtask/verify_structure.py
    python phase5/quadratic_comm/ty_module_subtask/morita_probe.py
    python phase5/quadratic_comm/ty_module_subtask/build_dual_candidates.py
    python phase5/quadratic_comm/ty_module_subtask/filter_dual_candidates.py
    python phase5/quadratic_comm/ty_module_subtask/compare_survivors.py

The field and tensor checks are exact. The full-Gram image enumeration uses the existing exact finite domain, and all three enumerations terminate completely. No bounded moment relaxation or numerical infeasibility is used in this reduction.

## Further categorical pruning

The original exact candidate and field-filter records above preserve the initial
three-isomorphism-type frontier. The later theorem in
`FORCED_D8_ASSOCIATOR.md` excludes the nonidentity quotient-action type (cases
26 and 27 for every source), using the associator forced by the TY-origin
construction. Its cyclic stabilizer obstruction applies to arbitrary complex
fusion categories. The current frontier therefore has **two** isomorphism
types, cases 12 and 25. No original rank-nine source is thereby resolved.
