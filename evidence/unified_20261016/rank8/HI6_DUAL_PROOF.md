# A theoretical identification of the HI(C6) Q-system dual

## Statement

The fusion category dual to the Q-system 1+rho in a known unitary Haagerup–Izumi category for C6 has Grothendieck ring R8_2_535. In particular R8_2_535 admits a unitary categorification.

This identifies the entire ring, not just its dimensions or a module representation. It does not assume a bound on the unknown dual structure constants and does not infer completeness from the census.

## Categorical inputs

Write d=3+sqrt(10), so d^2=1+6d, and D=6+6d^2=120+36sqrt(10).

The required unitary HI(C6) category and Q-system are established in Grossman–Izumi, *Drinfeld centers of fusion categories arising from generalized Haagerup subfactors*, Quantum Topology 13 (2022), 593–668, DOI 10.4171/QT/167, Example 4.5, printed page 632; see also condition (2.24). The known categorical construction supplies its unitary dual category, which we denote E.

Izumi, *The classification of 3^n subfactors and related fusion categories*, Quantum Topology 9 (2018), DOI 10.4171/QT/113, Proposition 7.4 and Theorem 7.5, printed pages 528–529, describe its eight simple objects:

    (1,b,r,rb,e1,e2,s1,s2)

with dimensions

    (1,1,d,d,d+1,d+1,d-1,d-1).

Here b=beta_3, e1=eta_1, e2=eta_2, and s1,s2 are the two sigma objects. The canonical module has seven simple objects (i0,...,i5,tau) with relative dimensions (1,...,1,d-1).

The same known HI(C6) category has center-simple dimensions

    1, d^2, 1+3d, 2+6d, 3d, 6d,

with multiplicities respectively (2,2,4,16,4,18). The complete inventory follows from the **published** Grossman–Izumi Lemma 3.5 (pages 617–618) and Theorem 3.9 (page 624); earlier arXiv versions number the corresponding results differently. Their dimensions squared sum to D^2. Centers are Morita invariant, so this is also the complete dimension inventory for Z(E).

Primary full text:
https://ems.press/content/serial-article-files/36923?nt=1
https://arxiv.org/abs/1609.07604

## 1. The canonical module forces commutativity and five characters

Let P be the cyclic permutation matrix of the six i-labels. The simple action matrices have six-by-six upper-left blocks

    I, P^3, I, P^3, P+P^(-1), P^2+P^(-2), 0, 0.

The matrices of 1 and b have no off-diagonal tau entries and tau diagonal 1. Every other matrix has all six entries in the tau column and row equal to 1. Their tau diagonal entries are, in the same order,

    r:5, rb:5, e1:6, e2:6, s1:4, s2:4.

These formulas follow from the principal graph and the decompositions in Izumi's Proposition 7.4. The bottom diagonal entries also follow immediately from the relative dimension vector. In particular the eta entries are **6**, not 4.

These eight matrices span a five-dimensional commutative algebra. For example their three independent linear relations are

    M_1-M_b-M_r+M_rb=0,
    M_1-M_r+M_s1=0,
    M_1-M_r+M_s2=0.

The fusion algebra K0(E) tensor C is semisimple. Its representation on this module has a three-dimensional kernel and a commutative image. Any noncommutative simple matrix-algebra block would have dimension at least four and would have to lie in the kernel. Therefore K0(E) tensor C is commutative.

Fourier diagonalization on the six cyclic labels, together with the two-dimensional constant/tau block, gives the following five distinct characters. Put d'=3-sqrt(10) and D'=120-36sqrt(10).

| Character | 1 | b | r | rb | e1 | e2 | s1 | s2 | Formal codegree |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| FP | 1 | 1 | d | d | d+1 | d+1 | d-1 | d-1 | D |
| FP conjugate | 1 | 1 | d' | d' | d'+1 | d'+1 | d'-1 | d'-1 | D' |
| u | 1 | -1 | 1 | -1 | 1 | -1 | 0 | 0 | 6 |
| v | 1 | 1 | 1 | 1 | -1 | -1 | 0 | 0 | 6 |
| w | 1 | -1 | 1 | -1 | -2 | 2 | 0 | 0 | 12 |

There are exactly three further one-dimensional characters.

## 2. The missing characters and their possible codegrees

Orthogonality to the five displayed characters forces any missing character to be of the form

    (1,beta,-1,-beta,0,0,s,t),
    beta in {1,-1},  s+t=1+beta.                         (1)

Here beta is a scalar character value, not the object b. To check this directly, subtract the orthogonality equations for u and w to obtain equal e1,e2 values; use v and the FP-conjugate pair to obtain their vanishing, then solve for r and rb.

For a commutative pseudo-unitary fusion category, each character chi determines a simple constituent of I(1) with dimension D/f_chi (Ostrik's formal-codegree induction theorem). The complete center inventory consequently restricts its formal codegree to

    D, D', 12, 6, 4sqrt(10), 2sqrt(10).

The last two possibilities are impossible: formal codegrees are totally positive, while their nontrivial Galois conjugates are negative. In this commutative setting, positivity is also immediate: a codegree is the squared norm of its character, and every Galois conjugate is the codegree of another character. This argument uses total positivity, not a claim about the constant coefficient of a dimension expression.

We must also rule out additional missing characters of codegree D or D'; uniqueness of the FP character alone would not justify this. For a character of the form (1), the Perron bound gives |s|,|t| <= d-1. Hence

    f_chi=4+|s|^2+|t|^2 <= 4+2(d-1)^2=8+8d < D.

Thus no missing character has codegree D. The five already displayed characters form a Galois-stable set, so the remaining three also form a Galois-stable set. A missing character of codegree D' would have a Galois conjugate of codegree D, which has just been ruled out.

All three missing codegrees are therefore 6 or 12. Formal-codegree reciprocity gives sum_chi 1/f_chi=1. Since

    1/D+1/D'=1/6,

and the other visible codegrees contribute 1/6+1/6+1/12, the three missing reciprocals sum to 5/12. Thus their codegrees are exactly 6,6,12.

## 3. The complete character table is forced

The invertible object b permutes s1,s2. If it fixed them both, any missing character with beta=-1 would have s=t=0 and codegree 4, which is impossible. All three missing characters would then have beta=1. But vectors of the form (1) with beta=1 span a space of dimension at most two; three distinct characters are linearly independent. Consequently b exchanges s1 and s2.

It follows that t=beta s. The vectors with beta=-1 now span a space of dimension at most two, so not all three missing characters can have beta=-1. There must be exactly one with beta=1, since it is uniquely determined as

    x=(1,1,-1,-1,0,0,1,1),  f_x=6.

The other two have beta=-1 and codegrees 6 and 12. Write them as

    y=(1,-1,-1,1,0,0,z,-z),
    zeta=(1,-1,-1,1,0,0,w,-w).

Their norms and mutual orthogonality give

    |z|=1, |w|=2, z conjugate(w)=-2.

Complex conjugation permutes characters, preserving both beta and the formal codegree. Within the missing set, each of these two codegrees is unique among characters with beta=-1. Thus both characters are real. Exchanging the names s1,s2 if needed, z=1 and w=-2.

This determines all eight characters. Since all their values are real and characters separate the fusion algebra, every simple object is self-dual.

## 4. Reconstruction and source identification

For the now completely determined characters and codegrees, every structure constant is forced by

    N_ij^k = sum_chi chi(i) chi(j) chi(k) / f_chi.

For a compact explicit description, put e=e1 and s=s1. The ring is commutative, b^2=1, and e2=be, s2=bs. All products are determined by these six relations:

    r^2 = 1+r+br+e+be+s+bs,
    re  = r+br+2e+be+s+bs,
    rs  = r+br+e+be+bs,
    e^2 = 1+2r+br+e+2be+s+bs,
    es  = r+br+e+be+s+bs,
    s^2 = 1+br+e+be+bs.

Thus the reconstruction gives nonnegative integers throughout, with maximum 2. Under the basis bijection

    (1,b,r,rb,e1,e2,s1,s2) -> (0,1,3,6,4,5,2,7)

it is exactly the source tensor R8_2_535. The maximum multiplicity is a conclusion of the reconstruction; it was not assumed in the uniqueness proof.

The standard-library verifier `verify_hi6_dual.py` carries out all arithmetic in Q(sqrt(10)), verifies character orthogonality, formal-codegree reciprocity, all 512 structure constants against the source tensor, all 4,096 associativity coefficients, and all 3,136 canonical-module multiplication coefficients. The source tensor is independently bound to the existing ledger hash

    bbec9e7a6c9699ef6dde3d09c0387b1ee426ea230c8bd0f94c7c48a4ec501edd.

Both normal and optimized Python runs pass. The categorical existence comes from the known Q-system and its dual category; the calculation identifies that existing category with the census ring. It constructs no category from a mere passing numerical test.

## Scope

This proves unitary existence for R8_2_535. It does **not** prove nonexistence for R8_2_630 or R8_2_671: the center inventory used here belongs to this specific constructed Morita class, and an unrelated categorification could have a different center.
