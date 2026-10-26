# Fresh audit: D144 affine H3 origin by a Galois fixed point

Conclusion: the proposed Galois anchor is sound, given the marked BrPic maps
and the Morita reductions already proved in d144/new_morita_reduction.md.
This audit concerns the new affine-origin step and the resulting identification
of the common integral restriction; it is not a replacement for those earlier
structural proofs or the final tensor binding to a rank12 target.

## Why the marked torsor has a well-defined Galois action

The neutral category is the specifically marked untwisted Vec_V4. Its invertible
bimodule classes have models specified by subgroups of V4 x V4 and cocycles
with values in{±1}. Therefore a Galois automorphism fixing Q(zeta8) fixes the
marked BrPic map and the coefficient module M=Inv Z(Vec_V4). The fact that
M is F2^4 is not, on its own, a justification; these rational/±1 models are.
The normal N=C3² has M^N=0. Averaging on this odd-order subgroup annihilates
higher cohomology with 2-primary coefficients, so H²(N,M)=0. Thus the marked
N-extensions with the fixed map constitute one affine torsor under
H³(N,C*)=F3{x²,xy,y²}.

Choose an automorphism sigma of Qbar fixing zeta8 and sending zeta3 to its
inverse. Such an automorphism exists because the cyclotomic fields of orders8
and3 are linearly disjoint. Its linear action on this H³ group is multiplication
by−1. An affine map with that linear part on an F3-vector-space torsor has a
unique fixed point: in any chosen temporary coordinate it is t -> b-t and
2t=b has one solution. No distinguished zero of the torsor has been assumed.
One must NOT require sigma to have order two on Qbar while fixing i. No such
requirement is needed; its induced action on this finite torsor is the stated
affine involution.

## The actual reference source is the fixed point

The reference is the actual crossed product F semidirect S3 of a three-fermion
S3-crossed category. Cui-Galindo-Plavnik-Wang construct the S3 gauging, and
standard H³(S3,C*) twisting supplies the available associator classes. Its
restriction to the C3 defect axis can therefore be chosen to be the m=0
intrinsic triality category. This is a choice among actual extensions, not a
formal modular-data assignment.

The primary formulas in Teo-Hughes-Fradkin TableVI and Lu-Sun Section6.2/Table4
were checked. At alpha=1 the complete C3 fusion associators belong to
Q(i,sqrt2). The apparent exponential in the formulas equals

    exp((pi/3)(A1+A2+A3)/sqrt3) = (I+A1+A2+A3)/2,

because the three quaternionic Pauli matrices anticommute and square to−I.
The remaining coefficients are signs, powers of i, and1/sqrt2. Thus sigma
fixes that MARKED C3 fusion restriction. This conclusion does not say that all
S3-crossed action tensorators, R-symbols, or the whole source are defined over
that field. THF explicitly do not print all full-S3 F-symbols; the argument
correctly avoids needing them.

For U_base=S3 x S3, restrictions of H³ differences to N lie in the invariant
plane span{x²,y²}; the xy term changes sign under either independent reflection.
The first-axis restriction has zero sigma-difference, so the x² coefficient is
zero. The diagonal reverse S3 is the actual pointed subgroup of objects(1,h)
in the crossed product; its associator is trivial by the crossed-product unit
coherence. Its diagonal C3 restriction therefore also has zero difference.
On the remaining y² term this restriction is injective, so that coefficient
vanishes too. The reference N-extension is sigma-fixed and hence is the unique
fixed point of the marked N torsor.

## The alternate admissible source is the same fixed point

For U_alt the quotient generator acts on N as a quarter-turn. Its invariant
line in H³(N,C*) is span{x²+y²}; xy changes sign and the two squares exchange.
The sigma-difference of an admissible alternate extension must lie on that
line, since both the original and its Galois conjugate extend to U_alt with
the same marked BrPic map. Restriction to the reverse diagonal C3 sends this
line's generator to2x², a nonzero class over F3. Since that actual reverse
pointed algebra has trivial associator, the difference restricts to zero.
Thus it is zero. The alternate N-extension is also sigma-fixed and must equal
the reference m=0 restriction as a marked extension.

This is the essential affine-origin repair. Merely saying a restriction
parameter vanishes would not identify the literature's m=0 origin; uniqueness
of the sigma-fixed point does.

## Extending the comparison to the integral order18 subgroup

The common subgroup U18 contains N with quotient C2. The same averaging
argument gives H²(U18,M)=0. Two extensions with the already-identified N
restriction can differ only by the 2-primary part of H³(U18,C*), inflated from
H³(C2,C*)=C2. Restriction to the reverse H's C2 is an isomorphism on this part.
Both actual reverse S3 subcategories have trivial associator, so this last
difference vanishes. The marked integral extensions are consequently equivalent.

For transport of the reverse algebra, keep track of the subgroup marking.
The point-stabilizer S3 complements in S4 are conjugate; any such residual
choice can be aligned by conjugation. H²(S3,C*)=0 makes the regular algebra
cochain unique up to isomorphism. This gives equality of the resulting integral
Morita-dual fusion tensors, provided the previously checked marking and actual
reverse-algebra data are carried along. It does not by itself identify every
full rank12 dual ring without that final tensor comparison.

## Sources directly checked in this audit

- Teo-Hughes-Fradkin, TableVI and its qualification concerning full S3 data:
  https://arxiv.org/pdf/1503.06812
- Lu-Sun, Section6.2 and Table4, including alpha=1 and sigma_sym:
  https://arxiv.org/pdf/2208.06077
- Cui-Galindo-Plavnik-Wang, existence of three-fermion S3 gauging and the H³
  torsor for actual crossed extensions:
  https://arxiv.org/pdf/1510.03475

The tiny F3 invariant-space and affine-fixed-point calculation is independently
replayed in audit_d144_galois_anchor.json. No modular-data coincidence or
unpublished full F-symbol table is used as a categorical equivalence premise.
