# Independent audit of the R1768 algebra lemma

The conditional algebra lemma in `../r8_quadratic/REPORT.md` is valid,
assuming its boundary identity (E(l,l)=1) for nonzero diagonal points and
the previously audited concrete crossed-product category. No positivity or
unitary classification is used. The arithmetic boundary proof and the
identification of the resulting Morita dual are separate obligations.

I checked the actual algebraic formulas in Radchenko–Wheeler,
https://arxiv.org/html/2609.21892v2, §5.4, against the new computation.
With (n=12), (L=L^\perp), (q|_L=1), and (T'_L=\sum_{l\in L}T'_l),
the identity (pT'_L\tau(p)=pT'_L) follows directly from

\[
T'_LU_l=T'_L,\qquad \lambda_lT'_L=T'_L\lambda_l,
\qquad p\lambda_l=p \quad(l\in L).
\]

Thus (t'\tau(t')=n^{-1}pT'_L\rho(T'_L)). In the explicit formula
for \(\rho(T'_l)\), its first term sums to
\(d^{-1/2}pS'_L\), its middle term is zero by \(T'_rS_h=0\), and its
last term is exactly

\[
\frac1{n^2}\sum_{h\in G,r\in L}
\left(\sum_{l\in L}B(l,h)E(-h-l)\right)pT'_{-h}T'_{h+r}.
\]

Likewise direct substitution in \(\rho(S'_l)\) gives equation (3) of
the report. The source projection in equation (2) is legitimately
removed using \(T'_l\tau^2(p)=\tau(p)T'_l\) and the displayed averaging
identity. Comparing the two types of terms gives
\(b^2=(c-1)/\kappa\) and exactly equation (4), with the stated sign.
The normalized Fourier transform has factor \(1/n\), so summing over
\(L\) leaves exactly one copy of the dual sum, as in equation (5).
No extra factor (n) or sign appears.

Both zigzag identities needed for separability can be checked directly,
rather than inferred from only one contraction. The term in (3) with
two primed (T)'s vanishes against (r), giving

\[
p\tau(s)rp=\frac ndp=\frac1c p.
\]

In the other order, substitute \(\rho(S_l)\tau(\lambda_l)\) into
\(\tau(r)\). The (T T) term is killed by (S'_k), and the surviving
sum is

\[
s\tau(r)p=\frac1{nd}\sum_{k,l\in L}\lambda_{l-k}p
=\frac ndp=\frac1c p.
\]

Consequently (1+cr) is a genuine two-sided inverse copairing to
\(\epsilon m\). Associativity implies the usual Frobenius identity,
so the displayed \(\Delta\) is an (A)-bimodule map. Connectedness
gives \(\operatorname{End}_A(A)=\mathbb C\), and evaluating
\(m\Delta\) on the unit gives \(1+c\ne0\). This proves the stated
separability section over (mathbb C).

Finally, the older explicit crossed-product audit proves that the
inclusion from the diagonal untwisted crossed product into the twisted
order-24 crossed product preserves all generating intertwiners and
their tensor products. Its extension to the additive Karoubi envelope
is therefore an actual tensor functor. The same diagonal projector
remains primitive, so it sends the parent simple to the target simple
\(\sigma\); connectedness as well as the explicit separability section
survives. This is a construction from the specified RW category, not a
statement about arbitrary spherical near-group categories.

## Categorical warning: the new algebra is not yet the desired model

The free (A)-bimodule Gram matrix does not have a unique nonnegative
integral factorization. In the order (a_0,\ldots,a_5,b_0,\ldots,b_5), it is

\[
\begin{pmatrix}I+J_{\mathrm{inv}}&I+J_{\mathrm{inv}}+2J\\
I+J_{\mathrm{inv}}+2J&I+J_{\mathrm{inv}}+28J\end{pmatrix},
\]

where (J_{\mathrm{inv}}) is inversion on (C_6), and (J) is the
all-ones matrix. Removing the four columns forced by the unit and the
rows (a_0,a_1,a_2) leaves a Gram matrix on the (b)-rows with every
entry 12 except the (b_3) cross entries 14 and its diagonal entry 18.
Therefore all five other residual row vectors are identical: this
follows from their squared difference being zero. For the two columns
supported at (a_3), write their common non-3 entries (p,2-p) and
their entries at (b_3) as (q,4-q).

Algebraic integrality of their dimensions gives (5p+q\in\{1,7,13\}).
Up to exchanging these columns there are two possibilities:

* (p=0,q=1): their dimensions are (1,u), and the other columns
  are constant on all six (b)-rows, with squares summing to 8.
  The possible partitions are ((2,2),(2,1,1,1,1),(1^8)), giving
  dual ranks 8, 11, 14.
* (p=1,q=2): their dimensions are both ((1+u)/2), and the
  remaining constant columns have squares summing to 10.
  The partitions ((3,1),(2,2,1,1),(2,1^6),(1^{10})) give
  dual ranks 8, 10, 13, 16.

Here (u=6+\sqrt{37}\) is the positive dimension, distinct from the
negative algebraic parameter (c) used above. R1768 would require the
first branch and the partition ((2,2)).

The rank-eight investigator subsequently found a stronger distinction,
which I independently checked. Conjugation by (a_3) in the parent
category carries the old projector (p_0) to (p_6). Its trivalent
space is the one-dimensional line (p_6T'_L). In the twisted target,
the equivalence from this projector back to (p_0) is

\[
Z=\lambda_{(0,6)},\qquad Z\tau(Z)=-U_{(0,6)}.
\]

Transporting the product line consequently gives

\[
Z(p_6T'_L)(Z\tau(Z))^{-1}
=-p_0Z\sum_{l\in L}T'_{l+(0,6)},
\]

the other trivalent line (t'_1), rather than (t'_0). Normalized
algebra isomorphisms act on the simple summand by (+1) or (-1), so
the pure-channel algebras are not isomorphic.

The possible additional invertible in the first Gram branch would have
underlying object (a_3+b_3=a_3A). Its left (A)-action would give an
algebra isomorphism (A\cong a_3Aa_3^{-1}\): connected separable algebras
are simple as bimodules, and the corresponding nonzero algebra map
between these equal-dimensional objects must be an isomorphism. Thus
the two pure-channel algebras cannot yield the first branch. Their
actual Morita duals have only one invertible and cannot be R1768.

There is also a valid finiteness argument excluding a continuous family
of mixed-channel multiplications on this same object. The necessary
conic is (b_0^2-b_1^2=(c-1)/\kappa). As the two pure-channel
solutions exist, all remaining equations on this conic reduce to a
fixed vector times (b_0b_1). If this vector were zero, the conic would
give infinitely many nonisomorphic connected separable algebras
(normalization leaves only the simultaneous sign equivalence).
This contradicts finiteness of indecomposable module categories and of
their simple objects over a fixed fusion category. Hence only the two
axes occur on (1+\sigma_0). This argument does not settle the other,
odd, conjugation orbit of simple noninvertibles in the precursor.

An even shorter check of the invertible count avoids completing the
Gram factorization. The already forced right-module list consists of
six (m_g=a_gA), whose underlying dimension is (1+u), and two
modules with underlying dimension (6u). An invertible (A)-bimodule
acts by an autoequivalence on right (A)-modules, so its value on the
simple regular module (A) is simple; its underlying dimension is
(1+u). Therefore it is one of the six (a_gA). Such a bimodule requires
(A\cong a_gAa_g^{-1}), which at the object level requires (2g=0).
For (g=3) the computed channel interchange forbids the isomorphism;
for (g=0) the algebra automorphism group is trivial because its
nonzero product into the simple summand forces the scalar automorphism
to be one. Thus the dual has exactly one invertible, independently of
its final rank and remaining products.

## Audit of the extension to all six translates

The extension in the rank-eight investigator's dual-obstruction note,
§4, is valid. For its character-weighted maps $r_\eta,s_\eta,t'_\eta$,
directly shifting the diagonal summation variable proves
$p_\eta r_\eta=\tau(p_\eta)r_\eta=r_\eta$.
Similarly $s_\eta\lambda_l=\zeta^{\eta l}s_\eta$, and the diagonal
identity $S'_lU_j=S'_l$ proves
$s_\eta p_\eta=s_\eta\tau(p_\eta)=s_\eta$.
The character factors therefore cancel in the two quadratic expansions
and in both zigzags. In the cubic contraction, the surviving middle
term of $\rho(T'_l)$ forces the two outer $S$-indices to coincide, so
the factors $\zeta^{\eta a}$ and $\zeta^{-\eta a}$ cancel.
Its rotation scalar remains one.

Conjugation by $g^3$ still sends $p_\eta$ to $p_{\eta+6}$, and transport
by $Z$ exchanges the two target trivalent lines exactly as before.
The finiteness argument and the right-module dimension argument do
not depend on the translate. Thus every connected separable algebra
on any $1+g^j\sigma$ in this specific precursor has a Morita dual with
only one invertible. This excludes the whole displayed construction
route, not the general categorifiability of R1768.
