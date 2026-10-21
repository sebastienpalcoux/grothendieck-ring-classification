# A finite Galois obstruction for the remaining R8_3_1154 center data

This note proves an additional **necessary-condition refinement**, from 36 to
25 pair-product histograms. All three remaining central-restriction patterns
survive. It proves neither an exclusion nor a categorification of R8_3_1154.
The argument is in the pseudo-unitary center setting of the existing evidence;
any broader reduction to that setting is inherited from the preceding work.

## 1. A general signed-permutation obstruction

Let C be a pseudo-unitary fusion category, D=dim(C), and let s denote the
canonical normalized modular S matrix of its Drinfeld center: s=S/D. For a
Galois automorphism sigma of the cyclotomic field of modular data, there is a
signed permutation matrix G with

    sigma(s) = G s.

We use the row convention G[i,pi(i)]=epsilon[i], with epsilon[i] in {+1,-1}.
Consequently its vacuum-column equation is

    sigma(d[i]/D) = epsilon[i] d[pi(i)]/D.                 (1)

This is the standard modular Galois symmetry; see Dong–Lin–Ng, *Congruence
property in conformal field theory*, Algebra & Number Theory 9 (2015),
2121–2166, Theorem II(iii), §4 equations (4-3)–(4-4), p. 2145. The canonical
center normalization appears in (1-10), p. 2130, and Lemma 4.2, p. 2146.
[Primary article](https://msp.org/ant/2015/9-9/ant-v9-n9-p03-s.pdf),
[DOI](https://doi.org/10.2140/ant.2015.9.2121).

Suppose a self-dual simple A has integral symmetric fusion matrix N and its
Verlinde eigenvalues lambda[j]=s[A,j]/s[0,j] satisfy

    sigma(lambda[j]) = 1/lambda[j]                     (2)

for every simple j. In particular N is invertible. Applying sigma to
N=s diag(lambda) s^-1 gives

    N = G N^-1 G^-1,       hence       N G N = G.        (3)

If U is any known matrix of vectors and Y=N U is also known, then (3) implies

    Y^T G Y = U^T G U.                                 (4)

Thus arbitrary unknown entries of N can be eliminated from a finite exact
necessary test whenever the right vectors are already known. This statement
requires no assumption that G is symmetric or that G^2=I. Even an involution
on a subfield can have extensions of higher order to the full modular field.

## 2. Application and exact input data

Use A=A1, the unique center simple of dimension 161+72 sqrt(5). Its uniqueness
among all occupied simple dimensions makes it self-dual. The coefficient
field is

    K = Q(t),   t^2 - 1684 t + 28159 = 0,
    t = 842 + 369 sqrt(5),   sigma(t)=1684-t.

Extend this field automorphism to the cyclotomic modular field. Every A1
Verlinde eigenvalue lies in K. The verifier checks (2) exactly for every
occupied type of each of the three patterns.

Take U to be the five coordinate vectors of the known low simples
A0=1,A1,A2,A3,A4. The matrix Y=N[:,0:5] is already fixed by each pair histogram:
its low entries are cubic vacuum moments, and its high entries are the
previously completed pair-product coefficients. These are inherited from
`evidence/rank8_next_20261021/r1154/joint_quartic_fibers.json` and the exact
moment/character definitions; the receipt binds the source files by SHA-256.
The independent verifier recomputes the low coefficients directly from
Verlinde moments and checks their Gram identities.

Only the three patterns retained by the reviewed preceding package are
considered: 6971, 8766, and 8772. Their 9, 11, and 16 pair histograms form the
entire 36-element input domain. Histogram numbers below are zero-based indices
in the corresponding stored `pair11_histogram_solutions_by_high_type` list.

## 3. Exhaustive finite enumeration

Equation (1) assigns every positive dimension class a unique target dimension
class and a forced sign. The exact field embedding determines that sign.
Source and target class cardinalities must agree. The verifier checks that
the assigned target classes are distinct and exhaust all classes.

Within each dimension class, it enumerates **all bijection effects**. Sources
are individually labelled. Targets are grouped only when both their Y rows
and their low coordinate labels agree. Recursive enumeration assigns a
sequence of target classes with exactly the required multiplicities. Every
labelled bijection has such a sequence, and every such sequence can be
expanded to a labelled bijection. Identical target classes do not affect (4),
so this compression loses no possible value of that equation.

For a possible source i to target j assignment, its contribution to the 5-by-5
left side minus right side of (4) is

    epsilon[i] (Y[i,:]^T Y[j,:] - U[i,:]^T U[j,:]).

The program sums these integer matrices within each class, deduplicates equal
matrices, and forms the exact finite sumset over disjoint dimension classes.
A pair histogram is excluded exactly when the zero matrix is absent. This is
complete finite enumeration, with no floating-point infeasibility inference.
The independent implementation instead enumerates integer transportation
tables between equal-row classes and reconstructs signed-permutation
witnesses for the retained cases.

## 4. Result and limits

| Pattern | Input pair histograms | Retained | Excluded histogram numbers |
|---|---:|---:|---|
| 6971 | 9 | 7 | 0, 4 |
| 8766 | 11 | 5 | 0, 4, 5, 6, 8, 9 |
| 8772 | 16 | 13 | 1, 4, 6 |
| Total | 36 | 25 | 11 excluded |

The discovery and independent verifiers agree on every input histogram.
Both are also replayed with Python optimization enabled. The published
manuscript's three-pattern residual domain remains correct; its 36 pair
histograms describe the preceding stage. This follow-up reduces that second
count to 25. A passing signed permutation is a witness only for (1) and (4);
it is not a modular datum, a fusion-matrix completion, or a category model.
