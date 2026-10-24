# Independent audit of the Gelaki-Hopf model for R9_2_965

The model is approved, with the Davydov-Runkel dual convention made explicit
as below. This review checked the primary theorem and its diagrams, the
ordinary Hopf pairing and copairing, the normalized cointegral, the compact
involution, and the unitarity argument. The source fusion tensor was rebuilt
from the independently reconstructed A1 characters rather than imported from
the model agent's constructor.

## A convention correction that must be retained

Davydov-Runkel use H^vee=(H*)^(op,cop) in ordinary vector-space notation;
their footnote 2 explicitly reverses multiplication in the dual coproduct.
Let P be the ordinary symmetric Hopf pairing in the proposed construction,
Gamma0 its inverse H*->H, and gamma0 the corresponding inverse-pairing
tensor. The theorem's Hopf map is Gamma_DR=S Gamma0, not Gamma0.

Their equation (2.28), however, inserts S^-1 after Gamma when forming the
associator copairing. Thus their actual gamma equals gamma0, not
(S tensor id)gamma0. This cancellation is important: replacing the
associator copairing too would introduce a second, unwanted antipode.

An entirely unambiguous route is Corollary 3.19, applied directly to gamma0.
The diagrams P-3 and P-4 read, in vector-space notation,

  (Delta tensor id)gamma0=gamma0_13 gamma0_23,
  (id tensor Delta)gamma0=gamma0_12 gamma0_13.

Both were independently checked over Q(zeta20). The tensor is symmetric;
(S tensor id)gamma0=(id tensor S)gamma0; and S²=id, g=1. The Haar functional
h is two-sided and satisfies

  (h tensor h)(id tensor S)gamma0=1/20.

Consequently lambda=sqrt(20)h has the normalization required by Corollary
3.19. All its hypotheses hold. The theorem gives the coherent extension and
Section 3.6 supplies rigidity. No assertion that arbitrary self-dual Hopf
algebras extend is used.

## Unitarity

With the compact involution in the construction, the twenty displayed basis
vectors are orthogonal for the positive Haar inner product, each of squared
norm 1/2. This is a finite-dimensional Kac Hopf algebra, so its representation
category is a unitary fusion category.

The associator copairing gamma0 is unitary: each idempotent block is a Fourier
bicharacter element multiplied by a unitary g power and a unit scalar. The
odd associator operator has the original, unmodified formula

  phi(b(a,e,b)) = i^(-t e b)/sqrt(5)
                 sum_u zeta5^(-(-1)^e u a) b(u,b,e).

I independently derived this formula using
S(b(a,e,b))=(-1)^(t e b)b(-(-1)^(e+b)a,e,b).
It is a permutation of four normalized Fourier blocks with unit phases, and
is therefore unitary for the Haar inner product.

The two-even-one-odd associator is the representation of unitary gamma0.
The even-odd-odd and odd-odd-even associators are the usual Hopf transport
maps and their inverses. For example W(h tensor v)=h_(1) tensor h_(2)v is
an isometry because (h_Haar tensor id)Delta(a*b)=h_Haar(a*b)1; its antipode
formula is its inverse. The odd-even-odd case is the representation of
gamma0 via right multiplication composed with S in the regular leg and
the ordinary action in the other leg. Right multiplication composed with S
is a star representation, so this is also unitary. Equivalently, the
relevant antipode-modified copairing is viewed in H^op tensor H, not inferred
unitary from a partially antimultiplicative map without accounting for the
opposite algebra. These are the five nontrivial associator cases in Section
2.2; the other three are identities. This proves unitarity of the extension.

## Exact replay and references

`audit_965.py` checks the two copairing equations, symmetry, antipode balance,
cointegral normalization, fusion axioms and all 729 source structure constants
for both the new R965 model and the R21 positive control. The result is in
`audit_965.json`.

Primary references:

- Andruskiewitsch-Natale, Examples of Self-Dual Hopf Algebras, Proposition
  2.2.4 and Sections 3-4:
  https://www.ms.u-tokyo.ac.jp/journal/pdf/jms060108.pdf
- Davydov-Runkel, Z/2Z-extensions of Hopf algebra module categories by their
  base categories, Theorem 2.5, equation (2.28), Corollary 3.19 and Section 3.6:
  https://www.math.uni-hamburg.de/home/runkel/PDF/hext.pdf
