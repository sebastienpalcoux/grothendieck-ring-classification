# A categorical obstruction for the supplied cyclic-eight restriction data

This result concerns the **actual** Grossman–Izumi cyclic-eight quotient
category D and the particular restriction matrix F in
`../center_continuation/cyclic8_center_tensor.json`. Although F is a positive
based-ring homomorphism and satisfies the indicator tests recorded there,
it cannot be the central forgetful functor of a category with fusion ring
R6_3_215 after a braided equivalence of its center with Z(D).

This does **not** exclude all categorifications of R6_3_215, identify a modular
datum with a braided category, or assert that every possible restriction map
from this actual center has already been enumerated. The hypothesis includes
the supplied induction vector and g-column of F; dimension- and
twist-preserving permutations of the central labels do not change either.

## The forced six-object module

Put d=4+sqrt(17), so d²=8d+1. The ring of D has invertibles alpha^j,
j in Z/4, and noninvertibles alpha^j rho of dimension d, with

    rho alpha = alpha^(-1) rho,
    rho² = 1 + 2 sum_j alpha^j rho.

Suppose the proposed central functor exists, with target C. Its associated
D–C Morita bimodule M has six simples: the inner product of the two
canonical induction vectors is 6. The cross Gram matrix F_D^t F determines
traces of the commuting actions. In particular,

    Tr(L_alpha)=0, Tr(L_alpha²)=2,
    Tr(L_(alpha^j rho))=8 for all j,
    Tr(R_g)=2.

Consequently L_alpha is one four-cycle and one two-cycle. Write its first
orbit as m_0,...,m_3 and its second as kappa_0,kappa_1. Symmetry of L_rho and
the relation L_rho L_alpha=L_alpha^(-1)L_rho give a reverse-circulant upper
block, an alternating cross block, and a lower block [[u,v],[v,u]]. The two
trace equations give u=4-r_0-r_2 and v=4-r_1-r_3. The identity
Tr(L_rho²)=70 bounds the remaining integer entries.

`cyclic8_rank6_modules.py` checks all 2,025 bounded parameter assignments
using integers. Exactly eight matrices remain: four with upper row sum s=1,
and four with s=7. Their cross-block entries are all 1. The squared Morita
dimensions, normalized to sum to FPdim(D)=8+32d, are

| Type | Four-cycle objects | Two-cycle objects |
|---|---:|---:|
| s=1 | 1+d | 2+14d |
| s=7 | 1+7d | 2+2d |

Moreover the only involutory permutation with trace 2 commuting with
L_alpha is (m_0 m_2)(m_1 m_3), fixing both kappa objects. Thus it is R_g.

## Reduction of s=7 to s=1

The invertible g in C fixes a simple object, so the associator on its
order-two pointed subcategory is trivial: that fixed object gives a
one-object module category over the pointed subcategory. Therefore the
connected separable algebra A=1+g exists.

The independent exact calculation
`frontier_full_morita.json` / `verify_frontier_full_morita.py` proves that
the fusion ring of C' = A-bimod(C) is again R6_3_215. This is a based-ring
conclusion, not a categorical identification of C and C'.

Form right A-modules in M. Each g-fixed kappa has two inequivalent module
structures: the stabilizer is C2 and its projective representations over
C are the two one-dimensional representations. Each such structure has
the same underlying object kappa. Morita dimensions divide underlying
dimensions by sqrt(FPdim(A))=sqrt(2). Hence in the s=7 case these four
new simples have squared dimension (2+2d)/2=1+d. The two free g-orbits
give two more simples, each with squared dimension
4(1+7d)/2=2+14d.

Thus M_A is a D–C' Morita bimodule containing a simple iota whose internal
end in D has dimension 1+d. Since D has only dimensions 1 and d, and a
simple object's internal end is connected, that end must be
1+alpha^h rho. The s=1 case already contains such an iota. Replacing rho
by alpha^h rho reduces both cases to an algebra of that form.

Here is why the transformed module has the required s=1 action, rather
than another possible action of a 1+rho algebra. The four iota objects
form a free alpha-orbit, because their internal ends contain no nontrivial
invertible. The upper rho block is fixed by iota iota*=1+rho; the diagonal
rho² equation forces the two cross entries to have squares summing to 2,
so both are 1. The lower rho block then has u+v=7 and |u-v|=1. If u=4,
the object iota* kappa in C' would have dimension 4d and endomorphism
dimension 5. It has no invertible summands, since iota and kappa have
unequal dimensions. Writing its other multiplicities as a,b,c,e gives
e=c, a+b+2c=4, and squared norm a²+b²+2c². The possible norms are
4,6,8,10,16, never 5. Thus u=3 and v=4, exactly the s=1 action used below.

## The second small algebra gives a contradiction

The actual category D has connected separable algebras 1+alpha^j rho for
every j. Their existence is part of the Grossman–Izumi generalized
Haagerup construction and survives its quotient tensor functor. Choose a
simple Morita object lambda with left internal end 1+alpha rho. Let E be
the corresponding dual category. Compose its E–D bimodule with the
D–C bimodule just obtained (replace C by C' when necessary).

Normalize iota so iota iota*=1+rho. The s=1 module matrices, or direct
Frobenius reciprocity, give two distinct simple objects

    beta_0 = lambda* iota,    beta_2 = lambda* alpha² iota,

both of dimension d+1. For a suitable kappa in the two-cycle, the object
Gamma=lambda* kappa has dimension 4d, its endomorphism space has
dimension 5, and each beta occurs once. Indeed the diagonal rho-entry
at kappa is 3 and the diagonal alpha rho-entry is 4; the cross entries
are 1. Its remaining three summands are distinct simples with total
dimension 2(d-1). One of them, gamma, therefore has dimension at most
2(d-1)/3.

All simple dimensions of this composed bimodule lie in K=Q(sqrt(17)).
To see this without a choice of associator, take the Perron eigenvector
of the sum of its C-action matrices. The simple Perron eigenvalue lies
in K, hence the eigenvector has ratios in K. The known entry
dim(beta_0)=d+1 fixes its normalization in K.

The connected internal end B=gamma* gamma in C now has dimension a square
in K, at most

    L = 4(d-1)²/9 = (8+24d)/9.

It is not the unit algebra. Otherwise gamma is an invertible Morita
object and identifies this bimodule with the regular C-module; that
would place the two distinct simples beta_0,beta_2 of dimension d+1
in C, whereas R6_3_215 has only one such simple.

In a connected internal end the unit occurs once and g occurs at most
once. Using the simple dimensions (1,1,d,d,d-1,d+1), the exhaustive list
of possible dimensions at most L is

    1, 2, d, d+1, d+2, d+3,
    2d-1, 2d, 2d+1, 2d+2, 2d+3, 2d+4, 3d-2.

The value 2 is not a square in K. The field norms of the remaining
nontrivial entries are, in order,

    -1, 8, 19, 32, -19, -4, 13, 32, 53, 76, -53.

None is a nonnegative rational square. This contradicts the existence
of B. `cyclic8_small_algebra_dimensions.py` verifies both the exhaustive
bound and these norms using exact arithmetic.

This last argument extends the mechanism of Grossman–Izumi–Snyder,
Lemma 4.16, to every algebra structure compatible with the displayed
module matrices. Its printed small-dimension list omits 3d-2; including
that value (norm -53) preserves the contradiction.

## Sources and replay

The actual D and its central restriction data come from Grossman–Izumi,
*Drinfeld centers of fusion categories arising from generalized Haagerup
subfactors*, Quantum Topology 13 (2022), Examples 4.4 and 6.10 and
Section 2.4: <https://ems.press/content/serial-article-files/36923>.
The second-algebra obstruction is motivated by Grossman–Izumi–Snyder,
*The Asaeda–Haagerup fusion categories*, Lemmas 4.15–4.16:
<https://arxiv.org/abs/1501.07324>.

Run from the package root:

```sh
python research/new_frontier/cyclic8_rank6_modules.py
python research/new_frontier/cyclic8_small_algebra_dimensions.py
python research/new_frontier/verify_frontier_full_morita.py
```

These are necessary categorical arguments with the source-category and
induction-data hypothesis above. The compatible modular datum alone
does not supply that hypothesis.
