# Rank-eleven unitary models: constructions and exact identification

The accepted files in this directory presently give **25 distinct supplied rings** with unitary categorical models. Every record contains the original compact-JSON tensor hash, an explicit model tensor, and a unit-preserving source-to-model basis permutation. All 1,331 fusion coefficients are compared. A model here proves existence, not uniqueness of associators.

The established constructions are applied before new explicit action calculations. The latter are applications of known equivariantization and zesting theorems; no claim that the resulting categories are new to the literature is made. In particular, finding a fusion-ring automorphism is not taken as proof that it lifts to a categorical action.

## Standard families and the finite searches

`standard.py` constructs the following families from their standard fusion formulas. Its `standard_models.json` has 20 different inputs.

| Inputs (prefix R11_1_) | Preferred construction |
|---|---|
| 182 | Vec(C11) |
| 171 | TY(C10), symmetric bicharacter exp(2πiab/10), positive τ |
| 26, 28, 46 | SU(2)_10, PSU(2)_20, PSU(2)_21 |
| 45 | Rep(D38), group order 38 |
| 1 | Rep(D32), group order 32 |
| 112 | Vec(C16)^C2, multiplication by 7 |
| 37, 75 | TY(C15)^C2 under inversion, with the two parity coherences; 37 also has SO(15)_2 fusion rules |
| 10, 72 | TY(C12)^C2 under inversion, with the two parity coherences; 10 also is the indicated half of SO(24)_2 |
| 64, 113 | TY(C3×C2²)^C2, inversion on C3 and a nontrivial orthogonal involution on C2², with the two parity coherences |
| 157, 176 | TY(C3²)^C2, an orthogonal reflection, with the two parity coherences |
| 30 | SO(8)_2 |
| 57, 105 | C2 associative zests of SO(8)_2 |
| 103 | C2 associative zest of SU(2)_10 |

Prime rank 11 excludes a nontrivial Deligne product of fusion categories. Among pointed categories of rank 11 the group is C11. A TY category of rank 11 must have underlying group of order 10, and its categorifiable group is the abelian C10. The rank equations for the A1 categories give exactly SU(2)_10 and the two even subcategories at levels 20 and 21. The rank equations for odd, full-even, and half-even metaplectic families give N=15, 8, and 24, respectively. Dihedral and dicyclic representation families similarly reduce to the parameters in the program.

Strict C2-equivariantizations of a pointed category have rank (|G|+3f)/2, where f is the number of fixed elements. At rank 11, divisibility f | |G| leaves only (|G|,f)=(19,1) or (16,2). The former is the inversion action on C19. `pointed16_complete.py` additionally enumerates all fourteen groups of order 16 as abelian-index-two extensions and all relevant involutive automorphisms. This is a complete search in that **strict, untwisted pointed-action family**, not a classification of all group-theoretical categories. The twisted examples below are consequently checked separately.

The TY search records its actual bicharacter matrix. In particular it does not assume that any based automorphism of a TY ring lifts. For the displayed nondegenerate symmetric bicharacters, orthogonality of the group automorphism preserves every entry of the standard TY associator. Thus the action on the standard skeleton is an actual unitary tensor action. The tensor natural automorphism ε which is +1 on group objects and −1 on the exceptional object is invariant under this action. Multiplying the C2 multiplication coherence by ε supplies the second action. For an equivariant object, its stabilizer generator satisfies U²=ε(X), so the exceptional-object eigenvalues are ±i instead of ±1. These are precisely the Fourier projections implemented in the program. No obstruction is hidden by replacing the coherence with a based permutation.

The `C2^3` coordinate-cycle TY trial was also constructed with its actual invariant bicharacter; its tensor has multiplicity greater than one and therefore contributes no model to this multiplicity-one census. A failed or out-of-scope model attempt is not an exclusion.

## Associative zesting

For a unitary braided category C with grading d in C2 and a neutral order-two invertible h, the new tensor product is

    X ⋆ Y = X ⊗ Y ⊗ h^(d(X)d(Y)).

The braided base supplies a central lift, and the scalar H4(C2,U(1)) obstruction vanishes. For the bosons or fermions here, a normalized scalar 3-cochain equal to 1 or i on (1,1,1), respectively, cancels the sole possibly nontrivial self-braiding value. Thus the construction is unitary and associative; no new braiding is claimed. The program verifies the grading, neutral degree of h, its order, and every product. Standard bases have their indicated actual braiding.

For SO(8)_2 the universal grading is V4. Its pointed subcategory is Tannakian: all four invertibles have twist 1 and centralize one another. Choose a coherent identification with Rep(V4), so both their associator and mutual braiding are trivial. Every bilinear function

    λ : V4 × V4 → V4

is an invertible-object 2-cocycle valued in these neutral invertibles. The associative-zesting obstruction is built from their associator and mutual braiding, so it is identically 1. Taking the scalar correction identically 1 gives a unitary associative zest. `v4_zest.py` enumerates all 4^4 bilinear functions and computes every resulting fusion tensor. They give four isomorphism classes: 30, 57, 105, and **150**, the last of which is additional to the single-C2 trials. A complete model receipt for 150 uses parameters (2,0,0,3) in the program's basis. The integer associativity test is an additional check; the categorical existence follows from this obstruction calculation.

## A coherent spin-current action on SU(2)_6

The involution σ of simple labels 0,...,6 fixes even labels and sends odd a to 6−a. Its equivariantization has rank 11 and the required dimension profile, but that information alone does not identify a category. In fact, the naive tensorator with all coefficients +1 gives a nonassociative proposed fusion tensor and is rejected.

`su2_spin_action.py` instead works with the standard real unitary quantum-Racah associator. Put u=2cos(π/8), with minimal polynomial u⁴−4u²+2 and isolating interval (1847759/10^6,1847760/10^6). Quantum integers satisfy [1]=1, [2]=u, and [n+1]=u[n]−[n−1]. For a tetrahedron of admissible doubled-spin labels, the standard formula is

    F^{abc}_d[e,f] = (−1)^((a+b+c+d)/2) sqrt([e+1][f+1])
                    × Δ(a,b,e)Δ(e,c,d)Δ(b,c,f)Δ(a,f,d)
                    × Σ_z (−1)^z [z+1]! / (Π_i [z−A_i]! Π_j [B_j−z]!),

where Δ(a,b,c)²=[s−a]![s−b]![s−c]!/[s+1]!, s=(a+b+c)/2,
A=((a+b+e)/2,(e+c+d)/2,(b+c+f)/2,(a+f+d)/2), and
B=((a+b+c+d)/2,(a+c+e+f)/2,(b+d+e+f)/2).
The sum has the usual bounds max A ≤ z ≤ min B. Terms containing [8] in the numerator vanish at this level, and no denominator factor vanishes for these admissible sextuples.

The square of each F entry lies in Q(u). The program compares the square of every admissible entry to that of its σ-transform exactly in this field. Its sign is the sign of the Racah sum times the displayed parity. Every such sign is certified by rational interval arithmetic, refining the isolating interval as needed. Consequently the comparison includes the actual signed entries, not just their magnitudes or floating-point approximations.

There are 1,664 nonzero entries and 16 zero entries. Equality of squared magnitudes holds for all of them. The ratios of nonzero entries determine a linear system over F2 for the 71 normalized tensorator signs J_ab^c. The system has rank 65 and the displayed solution satisfies all monoidal-functor equations. These signs have modulus one. For the square action, the program exhaustively finds and checks the two coherent choices

    μ_a = 1,                         and  μ_a = (−1)^a,

satisfying δμ=J·σ(J) and μ_{σ(a)}=μ_a. These are actual C2 actions, including the group-associativity coherence.

The usual orbit/stabilizer construction of equivariantization then gives the fusion rules. If three source labels are fixed, the involution on the one-dimensional fusion space is J_ab^c times the chosen stabilizer eigenvalues; fixed-output multiplicities are (dimension+trace)/2. If either input label belongs to a free orbit, that summand has trace zero. For a free output orbit the coefficient is its underlying multiplicity at a chosen representative. The entire tensor is computed this way and independently matched:

- μ=1 gives **R11_1_68**;
- μ_a=(−1)^a gives **R11_1_24**.

The tensorator, coherence, labels, exact source hash, model tensor, and basis permutation are all in `su2_spin_models.json`. This proof uses the established SU(2)_6 associator; it does not pretend that checking tensor-ring associativity alone verifies pentagons.

## Twisted cyclic pointed actions: 48 and 146

Here there is a uniform closed formula, which also explains why the untwisted pointed scan missed these inputs. Let n=16, let residues lie in {0,...,15}, and write c(a,b)=floor((a+b)/n). On Vec(C_n) use the unitary cyclic 3-cocycle

    ω_t(a,b,c) = ζ_n^(t a c(b,c)).

For an involutive multiplier u with u²=1 mod n, set p(a)=ua mod n and v=(u²−1)/n. The following tensorator uses exponents modulo n:

    J(a,b) = ζ_n^(−t u a floor(u b/n)).

The carry identity shows δJ = ω_t / p*ω_t. Explicitly,
c(p(b),p(c)) = u c(b,c)+floor(u(b+c mod n)/n)−floor(ub/n)−floor(uc/n),
and the u²−1 term vanishes modulo n. The composite tensorator J(a,b)J(p(a),p(b)) has exponent −tvab modulo n.

Take a natural isomorphism μ:F²→Id with exponent modulo 2n

    μ_a = ζ_(2n)^(tv a²+2ka).

Since n is even, δμ is exactly that composite tensorator. Choose k so that μ_{p(a)}=μ_a for every a; this is precisely the remaining C2-action coherence. For t=1 the choices used here are

| u | v | k | Identified input |
|---:|---:|---:|---|
| 15 | 14 | 0 | R11_1_48 |
| 7 | 3 | 4 | R11_1_146 |

Both actions have fixed points 0 and 8. At 8, μ_8=1 but J(8,8)=−1. Thus the lift of the nonzero fixed point squares to the nontrivial character of C2, producing the C4 group of invertibles. This is the feature absent from the untwisted examples.

`twisted_cyclic.py` verifies 65,536 cocycle equations, 4,096 tensorator equations, 256 square-coherence equations, and 16 action-associativity equations per action. It then constructs all fusion coefficients from the projective stabilizer traces. On fixed labels, the tensor-product equivariance is U_a U_b J(a,b)^(−1), which fixes the sign convention. All 1,331 coefficients match the supplied rings. The construction is unitary because every cocycle, tensorator, and coherence value is a root of unity.

## Primary sources and prior-project dependencies

- D. Tambara and S. Yamagami, *Tensor categories with fusion rules of self-duality for finite abelian groups*, J. Algebra 209 (1998), 692–707, Theorem 1; DOI 10.1006/jabr.1998.7558.
- P. Gustafson, E. C. Rowell and Y. Ruan, *Metaplectic Categories, Gauging and Property F*, Sections 3.1 and 3.3, https://arxiv.org/abs/1808.00698 . The authors' explicit fusion formulas and boson statement determine the SO(8)_2 and half-SO(24)_2 models.
- C. Delaney, C. Galindo, J. Y. Plavnik, E. C. Rowell and Q. Zhang, *Braided zesting and its applications*, https://arxiv.org/abs/2005.05544 , CMP 386 (2021), 1–55; associative zesting and its H4 obstruction. See also their *G-crossed braided zesting*, https://arxiv.org/abs/2212.05336 .
- S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion categories*, https://arxiv.org/abs/1206.6625v2 , J. Math. Phys. 54 (2013), 013511. Use the corrected v2, whose group action is explicitly assumed to be tensor.
- A. N. Kirillov and N. Yu. Reshetikhin, *Representations of the algebra U_q(sl(2)), q-orthogonal polynomials and invariants of links*, in *Infinite-dimensional Lie algebras and groups*, World Scientific (1988), p. 285 onward. The quantum-6j formula is also provided in the authors' implementation cited by E. Ardonne at https://staff.fysik.su.se/~ardonne/mathematica.html .
- C. Edie-Michell, *Auto-equivalences of the modular tensor categories of type A, B, C and G*, https://arxiv.org/abs/2002.03220 . This places the SU(2) simple-current involution among established constructions; our finite calculation additionally supplies and verifies its coherent action and equivariantization.
- The previous rank-nine/rank-ten accepted work supplies the standard tensor constructors in `work/models/match_models.py`, `extra_models.py`, `zest_models.py`, and `work/root_models/construct.py`. The new files are separate and do not modify that accepted release.

Computational proofs have exact finite scope and remain subject to ordinary mathematical review. All accepted existence claims are categorical constructions plus full-table identifications; unsuccessful model searches never imply nonexistence.
