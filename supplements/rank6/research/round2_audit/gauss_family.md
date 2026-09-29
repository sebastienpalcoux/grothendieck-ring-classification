# Independent audit of the quadratic Gauss family

The theorem and tensor-parametric verifier in
`papers/chapters/gauss_family.tex` and `software/new_gauss_family.py` were
independently reviewed. No mathematical gap was found in the exclusion of
R6_8_6520.

## Exhaustive low and high columns

For U=(5m+sqrt(25m²+4))/2, put z=U² and t=z+1. A codegree-five low
column has dimension t and therefore its quadratic-conjugate character
value is t'=t/z. Low S-matrix reciprocity gives
`z*t'=t*chi(v_z)`, hence all four small character values of the z-column
are one. Along with its FP and conjugate FP values, the complete character
table forces that column to be (1,mj). This does not select a restriction
column without justification.

The other four low columns have deviations w satisfying j·w=0,
delta·w=1, and sum(w)=delta. Projection to the space perpendicular to
j and delta gives sum(||w||²-1/4)<=15. Each integral w has squared norm
at least two, so every individual squared norm is at most ten. The box
[-3,3]^5 and every subsequent low enumeration are consequently exhaustive.
The 32 deviations, 59 initial multisets, 11 reciprocity-compatible
multisets and three positive-semidefinite residuals are reconstructed.

For high columns the diagonal and difference bounds follow directly from
Q-vvᵀ being positive semidefinite. Its kernel also contains the common
vector (1,1,-4,1,1), which determines the third coordinate from the other
four. The verifier uses the exact inverse of a full-rank principal block
and all kernel equations. Thus its finite high-column box is complete.
Integrality of D/dim(Y) follows from integrality of its square, a modular
formal codegree; a root of a monic polynomial over algebraic integers is
integral. The quadratic trace/norm test used in the code is exact.

## Multiplicities and first twist moment

For R6_8_6520 the outer branches have residual rank two but permit only
uniform high columns, which span rank one. The middle branch has exactly
the nine recorded high types.

The more general accepted list may contain 2j and doubled cross columns.
The delta-square and delta-j Gram equations force exactly eight cross
columns and force all of them to have coefficient m, so doubled cross
columns cannot occur. Those eight columns exhaust the u-square and
v-square Gram budgets and eliminate all offset types. The three mixed
Gram equations then force each of the four cross columns to occur twice.
This justifies the code's recorded multiplicities without an unperformed
integer search.

The remaining Gram matrix is (12m²+2)jjᵀ. A uniform column kj has
dimension k(5U), so its contribution to the first twist moment is weighted
by k². Its twist can therefore be counted k² times in a sum of exactly
L=12m²+2 roots of unity. The delta moment gives the total cross twist sum
-2; the j moment then gives

`Lambda=-(m*z+2m*t)/(5U)=-(m²+m*sqrt(25m²+4))/2`.

Both the root budget and this first-moment equation are valid independently
of any higher Frobenius–Schur indicators or finite conductor assumption.

## Arbitrary root orders

Let K=Q(sqrt(q)) have positive fundamental discriminant f and write
sqrt(f)=c*sqrt(q). For a root of exact order N, the normalized relative
trace from K(root) to K is rational when K is not contained in Q(zeta_N).
Otherwise f divides N. Averaging over the kernel of the primitive
quadratic character shows that the irrational part is its induced Gauss
sum divided by phi(N). The Gauss sum vanishes unless N/f is squarefree
and coprime to f; in the nonzero case Chinese remaindering gives magnitude
sqrt(f). Extra prime powers at conductor primes cancel under summation
over their lifts. Hence the coefficient of sqrt(q) has absolute value at
most c/phi(N), and therefore at most c/phi(f).

This argument includes every N, with no bound on its size or prime
support. Averaging a sum already in K fixes that sum, so the triangle
inequality gives L>=phi(f)*|coefficient of sqrt(q)|/c. For m=7 this is
L>=1228*(7/2)=4298, contradicting the exact budget L=590.

The separate trace-ideal argument was also independently audited: its
saturation enumeration forces the original signed gauge and its only
nonzero dimension-character orbit is the FP orbit. Thus the PU exclusion
does combine to a general categorification exclusion, rather than merely
excluding a preferred pivotal structure.

The complete combined certificate is independently replayed under
`python -O` with SciPy optimizer entry points disabled. The machine-readable
result is `gauss_family_replay.json` in this directory.
