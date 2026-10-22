# Independent audit of the R1768 nineteen-dimensional Weil block

**Verdict: PASS, with the stated conditional scope.** The normalized block and
all coefficients in the full displayed product of two forced irrational-ratio
objects are correct. Rational-ratio objects with primitive-37 twists remain
allowed and do not invalidate the argument. Neither this theorem nor its
verification excludes or constructs a categorification.

Audited inputs:

* `../unified/R1768_WEIL_BLOCK.md`, SHA256
  `ceb3f2c697840c25ee28b7f07686e61460fef4314468d0f86b6fd4c1c16f8600`;
* `../unified/verify_r1768_weil.py`, SHA256
  `36fbbaa5dc2e19a2fe56f975969aab4642e0428aa861710f20409d821dd8bbbf`.

This review assumes the separately proved saturated-conductor/signed-support
reduction and the accepted R1768 five-branch reduction. It checks the new
consequence rather than reproving those prerequisites.

## Normalization and signs

Put p=37 and s=sqrt(p). In the nonzero-column model, v=F-sH has squared
norm 2p(p-1). With the action T f(x,y)=f(x-y,y), the displayed vector

    v_k(x,y)=-chi(y) zeta^(-kx/y)/sqrt(p(p-1))   (y nonzero)

has T eigenvalue zeta^k and norm one. On the big cell x=ty,

    (S v)(ty,y)=chi(y)(chi(t)-s [t=0]).

Its Fourier coefficient at a nonsquare k is -2s/p. Dividing by the norm
of v and using the normalization of v_k gives the positive overlap
sqrt(2/p), as claimed. The T-fixed overlap is -1/sqrt(p).

Direct substitution, with x=uy and y nonzero, gives

    (v_k,S v_l)=(1/p) sum_(u nonzero) chi(u) zeta^(ku+l/u).

For k=2b^2 and l=2c^2, the negative Salié sign gives

    sqrt(p) S_kl = -(zeta^(4bc)+zeta^(-4bc)).

This agrees with the positive mixed entries and negative fixed entry;
there is no omitted conjugation or reciprocal phase in the specified T
convention. The cyclotomic verifier checks this sum for all324 pairs.
The usual canonical Gauss evaluation uses the positive sqrt(37).

For completeness, the fixed/fixed entry of S squared is
(1+18*2)/37=1. Each mixed entry vanishes because every row of the
unscaled primitive block B sums to1. The remaining324 entries are exactly
those checked by the verifier. Thus the entire displayed19-by-19 block,
not merely its primitive corner, is real symmetric and orthogonal.

## Why additional rational-ratio objects cause no problem

The saturated compression eigenspace in the universal induced model is a
single line. Every irreducible constituent supporting the cyclic vector maps
into that line. Distinct irreducible types could not both contain it; repeated
copies generate the diagonal copy selected by the original vector. The
explicit invariant span of the fixed vector and its eighteen nonzero T
spectral projections consequently identifies the cyclic representation.

In the eighteen-object branch, at each allowed twist the spectral projection
of S(e_1-e_alpha) has only one nonzero simple coordinate, of value2/sqrt(37).
Every rational-ratio simple in the same twist fibre has coefficient zero.
Therefore its normalized spectral vector is exactly e_Zk. The invariant
cyclic subspace is span{(e_1-e_alpha)/sqrt(2), e_Zk}. Invariance and unitarity
force every S entry between a Z_k and its orthogonal complement to vanish.
This includes all rational-ratio simples regardless of their twists.
The conclusion does not assume that a whole T eigenspace is one-dimensional.

## Full product coefficients

Let a=73+12sqrt(37), q=D/12, and dim(Y)=t_Y q for each remaining
rational-ratio simple. The dimension-orbit identity gives

    S_Y,1 = S_Y,alpha = t_Y/12.

All contributions from columns other than1,alpha and the eighteen Z objects
vanish in a product with two Z inputs. The target Y coefficient therefore is

    N_(Zk,Zl)^Y = t_Y(D+D')/(12*37) = 2t_Y.

For target alpha, orthogonality of the primitive rows gives

    N_(Zk,Zl)^alpha = (a+a^(-1)+2)/37 - [k=l] = 4-[k=l].

The Z objects are self-dual, and the unit coefficient is[k=l]. For target Z_n,
the two distinguished columns contribute144/37, and the remaining contribution
is (1/37) times the cubic sum of B. Its exact value4-37*epsilon yields
4-epsilon after including the distinguished columns. This verifies every
term of the full displayed product, with every rational-ratio simple counted
once, including those of primitive-37 twist.

The four signed additive relations defining epsilon are permuted, up to
negation, when a parameter changes sign. Two cannot hold simultaneously
because each parameter is nonzero and2 is invertible modulo37. Thus epsilon
is well-defined on sign classes and belongs to{0,1}.

As an additional independent check, for a fixed ordered input pair there is
one target sign class with epsilon=1 if the inputs coincide, and two if they
are distinct. The primitive coefficient sum is therefore71 or70. Using the
accepted rational-sector identity sum t_Y^2=70, the full FP-dimension identity
is, respectively,

    d^2 = 1+3a+140q+71d = 4a+140q+70d,
    d = 72+12sqrt(37)=a-1.

Both identities hold exactly in Z[sqrt(37)].

## Executed checks

The supplied verifier passed normally and under Python `-O`. Both runs gave
324 exact Salié checks,324 primitive S-square checks and1140 unordered exact
cubic checks. An independent enumeration of all5832 ordered target triples
confirmed sign invariance, epsilon in{0,1}, and the totals630 coefficients3
and5202 coefficients4. An independent quadratic-integer calculation verified
the full product dimension identity for all324 ordered input pairs.

The result is a forced part of hypothetical modular data in the eighteen-object
branch. Products within the remaining rational sector and the remaining
modular and categorical consistency equations are still unresolved. The
seventy-two-object branch determines the same block only on normalized
four-object sums, not on individual simple coordinates.
