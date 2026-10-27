# R9_2_1975: duality and Galois-unit parity exclude every Morita branch

Status: **excluded over C**, using the existing audited general-scope and
TY/Morita reductions. This report proves that the reflection-duality branch
is impossible. The accompanying `GALOIS_PARITY_EXCLUSION.md` proves that the
rotation-duality branch is also impossible: every central restriction must
have even multiplicity at one large simple, whereas the distinguished
Galois-unit object has multiplicity one there. No categorical model is asserted.

The argument is over arbitrary complex scalars. It is an obstruction to a
duality equivalence of pointed bimodule categories, not a numerical search for
pentagon solutions. An initial fourth-root cochain search was deliberately
discarded: a surviving rotation branch requires eighth roots. The final
reflection obstruction uses a gauge-invariant product of commutators and
therefore is not subject to a root-of-unity search bound.

## 1. Frozen inputs and prior reductions

Source snapshot: classification commit
`6a426acf6465dd674351be92dcca41b72f371521`.
Source tensor SHA-256:
`8b30652d59e868a120b6c423e46a99ab51f6032af752dc0082a3d80fd9e61323`.

Prior categorical arguments in
`evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank9_noncommutative/NEW_RESTRICTIONS.md`
give a rank-twelve Morita dual whose invertibles are (G=D_8), whose four other
objects (X_q) are indexed by (Q=G/Z(G)), and whose dimension is

\[
d=4+3\sqrt2,\qquad d^2=2+8d.
\]

Writing (H=Z(G)), its surviving fusion rules are

\[
gX_q=X_qg=X_{q+gH},\quad
X_pX_q=\sum_{gH=p+q+\alpha}g+2\sum_{t\in Q}X_t,
\quad X_q^*=X_{q+\alpha}.
\]

The two surviving choices have \(\alpha\) a reflection coset or the rotation
coset. Positive TY sign and the earlier extreme Morita tensor were already
excluded; these are not new results here. The integral TY subcategory has
negative sign. The existing all-cochain pairing theorem in the sibling retry
file `rank9/POINTED_BIMODULE.md` says the four-object component is an invertible
\(\operatorname{Vec}_G^\omega\)-bimodule and fixes the pointed associator class.

The new argument uses that component's actual categorical duality. It does
**not** assume that the full rank-twelve category is group graded: its displayed
products plainly contain both pointed and nonpointed terms.

## 2. Explicit conventions and the duality condition

Use (G=\{(x,y,n):x,y,n\in\mathbb F_2\}\) with

\[
(x,y,n)(u,v,m)=(\operatorname{swap}^{m}(x,y)+(u,v),n+m).
\]

Put (p=(1,0,0)), (s=(0,0,1)), (z=(ps)^2=(1,1,0)).
Let (K=G\times G) act by \((g,k)X=gXk^{-1}\). The stabilizer of (X_0) is

\[
L=G\times_QG\simeq G\times C_2,
\qquad (g,e)\longmapsto(g,gz^e).
\]

Write (P=(p,0)), (S=(s,0)), (Z=(z,0)), and (E=(1,1)) in this copy of
(G\times C_2). The opposite operation is the factor interchange

\[
T(g,e)=(gz^e,e).
\]

These are exactly the pointed bimodule conventions of Vainerman--Vallin,
*On Z/2Z-extensions of pointed fusion categories*, arXiv:1210.1732,
§2.2.2 (printed p.11) and §3.1.1 (printed p.14): their right coordinate is
inverted to obtain our second coordinate. Thus the acting cocycle is
\(\Omega=p_1^*\omega/p_2^*\omega\), and the opposite stabilizer cochain is
\((\beta\circ(T\times T))^{-1}\). No additional opposite tensorator has been
omitted in this convention. Their §2.2.1 (printed p.10) supplies the conjugation
correction used below. Only the bimodule classification and opposite operation
are used, not their classification of group-graded extensions.

Choose a lift (q\in G) of the required duality shift \(\alpha\). Conjugation
by \((q,1)\in K\) induces

\[
\phi_q(g,e)=(qgq^{-1},e+c_q(g)),
\qquad qgq^{-1}=gz^{c_q(g)}.
\]

If \(\omega=i^w\), write the normalizer correction additively as

\[
\kappa_q(a,b)=w(q,a,b)+w(qaq^{-1},qbq^{-1},q)
             -w(qaq^{-1},q,b)\pmod4.
\]

It satisfies \(\delta\kappa_q=w-\operatorname{Ad}_q^*w\). For any stabilizer
cochain \(\beta=i^b\) with \(\delta b=p_1^*w-p_2^*w\), a duality equivalence
with shift (qH) therefore requires the ordinary two-cocycle

\[
c_q(A,B)=b(\phi_qA,\phi_qB)+\kappa_q(p_1A,p_1B)+b(TA,TB)
\tag{1}
\]

to be a coboundary (in multiplicative notation use \(i^{c_q}\)). This is a
necessary condition on the object-level duality in any such fusion category.

## 3. A commutator invariant valid for every complex cochain

For an ordinary multiplicative two-cocycle (c), write

\[
C_c(a,b)=c(a,b)c(b,a)^{-1}\quad\text{when }ab=ba,
\qquad J(c)=C_c(P,E)C_c(S,E).
\]

Every coboundary has (J=1). The key point is that (J) of (1) is independent
of the choice of the stabilizer cochain, not merely of the eight convenient
finite-valued representatives.

Indeed, another cochain is \(\beta\gamma\), where \(\gamma\) is an arbitrary
complex two-cocycle on (L). Its contribution to (1) is
\(\phi_q^*\gamma\,T^*\gamma\). Since (E) is central,
\(C_\gamma(-,E)\) is a character of (L); it kills (Z=[P,S]) and has square
one on (P,S). Moreover

\[
TP=P,\quad TS=S,\quad TE=ZE,
\qquad \phi_qP=P(ZE)^a,\quad\phi_qS=S(ZE)^b,\quad\phi_qE=E
\]

for some (a,b\in\mathbb F_2). Consequently the changes in the two factors of
(J) are respectively \(C_\gamma(P,Z)\) and \(C_\gamma(S,Z)\). Their product
is one: it is \(C_\gamma(PS,Z)\), and (Z=(PS)^2), so lifts of (PS) and (Z)
commute in the central extension defined by \(\gamma\). This proves
independence for **all** complex two-cocycles. Coboundary changes of the
cochains are included.

It remains to calculate (J) for one cochain, which is the previously checked
cochain in `POINTED_BIMODULE.md`. For (A=(x,y,n,e)), (B=(u,v,m,f)), it is

\[
\begin{split}
b(A,B)={}&2nf+2nm+2yf+3ym+2ymf+2yu+yem\\
         &+xm+2xmf+2xu+3xem+2xym\pmod4.
\end{split}
\]

The fixed pointed cocycle is

\[
w((x,y,n),(u,v,m),(a,b,\ell))
=\ell\bigl(3m(x+y)+x'u+y'v+2y'u\bigr)+2t nm\ell\pmod4,
\]

where (x+y) inside the first term means addition in \(\mathbb F_2\),
\((x',y')=\operatorname{swap}^{m}(x,y)\), and (t=1) for negative TY sign
((t=0) works as well).

Substitution in (1) gives, for (q=(x,y,n)),

\[
\boxed{\ J(i^{c_q})=(-1)^{x+y+n}.\ }
\tag{2}
\]

The correction \(\kappa_q\) contributes zero on the pairs involving (E),
because (p_1(E)=1\). Thus (2) is independent of the TY sign. Precisely the
two noncentral reflection cosets have (x+y+n=1\). They therefore cannot be
the duality shift. This is the promised categorical obstruction.

## 4. Consequences of the duality test alone

For R9_2_1975 the reflection type \((\alpha,a)=(2,2)\) is excluded. In its
archived tensor, (X_8^*=X_{10}\), and the invertible lifts of that shift are
objects 4 and 5, both of order two. The remaining type is
\((\alpha,a)=(3,2)\); here (X_8^*=X_{11}\), with shift lifts 6 and 7 of order
four. These assertions are direct bindings to `new_results_inputs.json`.

The same theorem eliminates the reflection alternative in the corresponding
uniform Morita reductions of R9_2_137, R9_2_1607 and R9_2_1976, leaving their
zero-shift alternative. It does not exclude any of those source rings.

The rotation shift genuinely passes this duality test: for the displayed
\(\beta\) and (q=ps\), equation (1) has an explicit eighth-root-valued
one-cochain trivialization. The checker records and verifies all 256 equations.
Thus the rotation case cannot be rejected by restricting a search to fourth
roots. A zero-shift witness is obtained by multiplying \(\beta\) by the
Schur-multiplier cocycle of the central extension (D_{16}\to D_8\).

These rotation pointed-bimodule and duality cochains do not solve the
pentagons involving noninvertible multiplication. No vanishing of the
obstruction for a hypothetical Z2-graded extension is inferred: the ring is
not such an extension.

## 5. The second obstruction completes the exclusion

In the rotation case, use the individual commutator at (P,E), rather than only
the product J. Its value for the displayed cochain is one; replacing beta by
beta gamma multiplies it by C_gamma(P,Z). Duality therefore forces
C_gamma(P,Z)=1. Since C_beta(P,Z)=-1, the actual diagonal stabilizer multiplier
has commutator -1 at P,Z.

The even subgroup <p,z> is V4 and its pointed associator is identically trivial
in the chosen gauge. Thus every central half-braiding induces anticommuting
operators on the X_0-isotypic multiplicity space. Its dimension is even. This
argument avoids an unsupported choice of global diagonal D8 tensorator.

Apply the Galois-unit restriction theorem directly to the pseudo-unitary
rank-twelve Morita category. Its eight scalar irreducibles have formal
codegrees D,D',16,16,16,16,16,16; its degree-two irreducible has codegree 4.
The element 1+sum_q X_q acts on each irreducible E by f_E/sigma(f_E), retaining
the degree-two normalization. Consequently the distinguished central simple
associated to sigma(FP) restricts to exactly 1+sum_q X_q. Its X_0 multiplicity
is one, contradicting the preceding evenness.

The full categorical proof, explicit irreducible characters and citations are
in `GALOIS_PARITY_EXCLUSION.md`. The checker `verify_galois_parity.py` binds the
actual original and Morita tensors by SHA-256, verifies the displayed group
and fusion rules, and checks the full exact rational matrix identity for the
Galois-unit restriction. This supplies a whole-ring exclusion, rather than
only the earlier aggregate parity restriction on source-center dimensions.

## 6. Reproduction and scope

`verify_duality_obstruction.py` checks the finite group identities, both pointed
cocycles, the stabilizer cochain, all conjugation corrections, (2), and the
surviving eighth-root witness. Its computations concern a group of order 16
and finish quickly. The all-complex argument in §3 is the mathematical reason
these finite checks do not amount to an incomplete search over associators.

Independent review by the rank-nine commutative and rank-six investigations
confirmed the primary-source conventions and the eighth-root rotation
witness. Both accepted the added all-complex diagonal commutator argument and
the even-V4 relative-center parity proof. The separate rank-six 1660 audit
confirmed the noncommutative formal-codegree and Galois-unit calculation and
freshly replayed the original source's complete signed Galois-to-pseudo-unitary
gate in under a second, including both signed branches and final UNSAT.
The complete original TY/Morita and general-scope reductions remain cited
project dependencies. The outcome is **one new whole-ring exclusion and zero
new models** for R9_2_1975. The independent categorical review is recorded in
`../r6_155/R1975_INDEPENDENT_AUDIT.md`.
The independent general-scope and normalization audit is
`../r6_1660/R1975_GALOIS_AUDIT.md`.

Primary reference: L. Vainerman and J.-M. Vallin,
*On Z/2Z-extensions of pointed fusion categories*, arXiv:1210.1732,
https://arxiv.org/pdf/1210.1732, §§2.2.1, 2.2.2, 3.1.1.
