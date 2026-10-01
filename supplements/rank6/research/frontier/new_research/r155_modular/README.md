# R6_4_155: determinant, Galois blocks, and a new duality obstruction

Status: the complete rank-26 modular S and fusion rules are now uniquely forced
(up to the frozen label/Galois conventions), and the unique candidate passes
all tests listed below. This is not yet a categorical construction or an exclusion.
The frozen M9 release is unchanged.

Let z=exp(2πi/24), d=4+3√2, and B be the forced rank-26 semion centralizer.
Its multiplicative central charge is z^(-3), sqrt(dim B)=12d. Therefore

    s=S_B/(12d),   t=z T_B

is a genuine representation of SL2(Z/24), with s²=C (duality), (st)³=C.
The normalization and finite-level assertion follow from Dong–Lin–Ng,
*Congruence Property in Conformal Field Theory*, Theorem II and §4:
https://arxiv.org/abs/1201.6644
https://arxiv.org/pdf/1201.6644
The modular representation reconstruction framework is in Ng–Rowell–Wang–Wen,
https://arxiv.org/abs/2203.14829 .

## 1. A one-line theoretical determinant cut

In every representation of SL2(Z), determinants satisfy det(s)=det(t)^(-3),
hence det(C)=det(t)^(-6). The frozen twist exponents sum to 258.
Thus det(t)=z^(258+26)=z^20, det(s)=-1, and det(C)=1.
A duality involution on 26 labels with r fixed labels has sign (-1)^((26-r)/2).
Consequently r≡26 (mod 4). Among the previously retained r=10,12,14,
the value 12 is excluded. The two odd 2d twist-pairs must therefore have
the same duality type.

This argument needs neither finite character enumeration nor unitarity.

## 2. Exact finite representation reduction

All a coprime to 24 satisfy a²=1 mod24. Dong–Lin–Ng's signed Galois matrix is

    G_a=σ_a(s)s^(-1)=ρ(diag(a,a^(-1)))=ρ(a I).

It is central, commutes with s,t, and is an involutory signed permutation.
The rational simple-object basis therefore decomposes into simultaneous
Galois character spaces. Denote by χ_i, χ_2, χ_3 the characters describing
the action on i, √2, √3, respectively.

Dimensions and equal twists determine the possible signed permutations.
For example the unit/A and f/fA pairs have signed transposition when √2
changes sign, while pure kd dimensions have positive signs. The known
nonreal-character rows give the M-pair permutation character χ_i χ_2:
normalized M rows have the form (√2/8)φ(F(-)), and φ(X)=±i√2.

`exact_enumeration.py` reconstructs SL2(Z/8), SL2(Z/3), verifies their exact
character tables (class algebra, orthogonality, degrees, T multiplicities,
central signs), tensors all 210 irreducibles, and enumerates all 718
rank-26 T-spectrum decompositions. There are exactly eight decompositions
consistent with the signed Galois permutation constraints. It then uses
the fully known χ_2 six-dimensional block to leave four. The job takes
about four seconds, uses integer/cyclotomic arithmetic, and uses no optimizer.
The receipt is `exact_enumeration.json`. The exploratory scipy files are
not required for the exact replay.

The resulting Galois permutation characters are forced:

| Equal-dimension pair | Pair permutation character |
|---|---|
| even d pairs (twists ±1) | χ_i |
| odd d pair | χ_i |
| odd 3d pair | χ_i |
| M pairs (dimension 1+2d) | χ_i χ_2 |
| odd 2d pairs, both nonselfdual | χ_i for both |
| odd 2d pairs, both selfdual | χ_3 for both |

The representation splits into Galois spaces as follows:

* A rational-character space of dimension 12, of representation type 3+9
  or 3+3+3+3.
* A χ_2 space of dimension 6, fully determined by the known low S rows;
  its representation type is 4+2.
* A mandatory χ_i space of dimension 6, one irreducible representation,
  with distinct t exponents {1,7,10,13,19,22}.
* An additional two-dimensional space: χ_i with two one-dimensional
  constituents if both odd 2d pairs are nonselfdual, or χ_3 with a single
  irreducible constituent if both pairs are selfdual.

Local irrep indices in the receipt refer to the verified JSON tables.
The local SL2(Z/3) index0 is the character t↦ζ3², not the trivial character.
The known χ_2 block has Tr(st)=0. The discarded 2+2+2 choice would have
Tr(st)=-3ζ3²; the retained 4+2 choice has trace zero.

## 3. A second theoretical cut: selfdual odd 2d objects are impossible

In the selfdual branch, take the rational pair-difference basis

    e12-e13, e14-e15

in frozen labels. It spans the χ_3 Galois space, of dimension two, with

    t=diag(i,i w),  w=ζ3,    s=[[a,b],[b,c]].

The two basis vectors have the same squared norm 2, so symmetry of the
original s makes this block symmetric. Since σ(s)=χ_3(σ)s on this rational
space, every entry lies in √3·Q. One has b≠0 even without character classification: if b=0, s²=I makes its
first diagonal entry ±1, and (st)³=I would require (±i)³=1, impossible.
Because C is the identity here, s²=I implies c=-a. The off-diagonal entry
of sts=t^(-1)st^(-1) gives

    a=1/(i·iw·(i-iw))=1/√3.

The diagonal entry of s²=I then gives b²=2/3. But b∈√3·Q would imply
(b/√3)²=2/9, impossible over Q. This excludes the selfdual branch.

Consequently B must have exactly 10 selfdual simples, and its rank-52
center exactly 20. Both odd 2d pairs are dual pairs. This is stronger
than the determinant cut and still does not exclude the fusion ring.

## 4. The six-dimensional χ_i block is completely forced

In the equal-norm pair-difference basis

    (2,5), (3,6), (4,7), (20,21), (16,17), (18,19)

where (a,b) means e_a-e_b, one has s=i Q, with

    2Q = [[ 0, 0, 1,-1,-1,-1],
          [ 0, 0,-1, 1,-1,-1],
          [ 1,-1, 0, 0, 1,-1],
          [-1, 1, 0, 0, 1,-1],
          [-1,-1, 1, 1, 0, 0],
          [-1,-1,-1,-1, 0, 0]].

The known M antisymmetric rows give the last two rows. Their rows of
sts=t^(-1)st^(-1) leave three rational variables, and their rows of
s²=-I force those variables to 0,1/2,0. The remaining extra χ_i two-space
has s=i I. Thus the unresolved S block has dimension 12.

`chi_i_completion.py` records the exact linear derivation and verifies every
modular relation entry of the resulting block, as well as the two-block
rational-square obstruction. Its receipt is `chi_i_completion.json`. The
remaining block and its integral Verlinde coefficients are determined below;
categorical realization remains open.


## 5. The last twelve-dimensional block is uniquely forced

The rational Galois space has the rational basis

    e1-e23, e0-e22, e2+e5, e3+e6, e4+e7, e20+e21,
    e8, e9, e10, e11, e12+e13, e14+e15.

Let P have these vectors as columns, N=PᵀP=diag(2,2,2,2,2,2,1,1,1,1,2,2),
and H=PᵀsP. The action matrix is N⁻¹H, not H itself. Symmetry and modular
relations become

    H=Hᵀ,   H N⁻¹ H=N,   H N⁻¹ tH=t⁻¹Ht⁻¹.

The first two rows are known low rows. Their equations reduce the 55
unknown symmetric entries to ten rational variables. Two further linear
equations set one variable to zero. The remaining equations are 187
quadratics in nine variables. Regard quadratic monomials as temporary
independent columns and row-reduce the equation coefficient matrix over Q.
This produces nine linear equations, forcing the nine variables to

    -1/3, -1/6, 1/3, 1/3, 2/3, -1/6, -1/6, -2/3, -1/6

in the recorded order. Substitution satisfies every original equation.
No Gröbner basis, optimizer, algebraic root enumeration, or numerical
approximation is needed for uniqueness. `trivial12.py` performs this
rational calculation in approximately four seconds; its receipt includes
the original equations, linear consequences, and unique solution.

The scaled symmetric form 6H is the integer matrix in `matrix_blocks.json`.
The block has Tr(s)=-2, selecting the representation type 3+9; the competing
3+3+3+3 type would have trace +2. The final full representation type is

    9 + 6 + 4 + 3 + 2 + 1 + 1.

Its local SL2(Z/8) × SL2(Z/3) constituent indices are

    (13,6), (24,0), (23,0), (10,0), (8,0), (2,1), (2,2).

## 6. Complete modular data, fusion, and checks

`reconstruct.py` combines the four mutually orthogonal rational bases.
For their direct-sum H and basis matrix P, the full normalized matrix is

    s = P N⁻¹ H N⁻¹ Pᵀ.

The resulting `reconstruction.json` records s exactly as coefficients
in Q(ζ24), all 26³ fusion coefficients, the unit label 1, and duality.
The coefficient lists are in descending-power order for ζ24 with minimal
polynomial x⁸-x⁴+1; the empty list represents zero. It verifies every
entry of s²=C and sts=t⁻¹st⁻¹ and all known low rows. The entire Verlinde
table is nonnegative integral, with maximum coefficient 9. The numeric
calculation in this script proposes integers only; every proposed entry
is then certified by exact fusion diagonalization. The complete data
have also been independently checked by the models subagent.

The following further tests pass exactly:

| Test | Scope | Result |
|---|---|---|
| Modular second indicators | all 26 simples | correct 0/±1 values |
| Anderson–Moore–Vafa | all 26⁴=456,976 ordered quadruples | all pass mod 24 |
| Ordinary cyclic rotations | all 26 simples; n=2,3,4,6,8,12,24 | all 182 blocks have nonnegative integer eigenvalue multiplicities |
| Quaternionic multiplicity | [U*⊗U:24] for all 26 U | all zero |

Object 24 is the unique quaternionic selfdual simple: ν₂(24)=-1; every
other selfdual simple has ν₂=+1. Scripts and receipts are `full_checks.*`
and `higher_ordinary.*`. Each job takes less than seven seconds.

Reproduction order, from this directory:

    python exact_enumeration.py
    python chi_i_completion.py
    python trivial12.py
    python reconstruct.py
    python full_checks.py
    python higher_ordinary.py

The three exploratory files `galois_cone.py`, `low_trace_probe.py`, and
`B_modrep24.json` are not needed for these exact conclusions.

Categorification still requires associators/braiding data or an independent
realization theorem. These computations establish a unique fully explicit
candidate modular datum and fusion ring for B; they do not construct B
as a category or construct the original rank-six category.
