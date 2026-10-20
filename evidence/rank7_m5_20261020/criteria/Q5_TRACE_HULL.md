# Unrestricted quadratic relative-trace hull for Q(sqrt(5))

This is a necessary-condition lemma, independent of compression saturation.
Write s=sqrt(5), and let t be normalized relative trace to K=Q(s) from
any cyclotomic extension containing the root of unity in question and K.
Use `(a,b,c,d)` to represent `(a+b*s,c+d*s)`.

Every pair `(t(theta),t(theta²))` belongs to a hull with seventeen vertices:

* the five rational vertices `(1,0,1,0)`, `(-1,0,1,0)`,
  `(1/2,0,-1/2,0)`, `(-1/2,0,-1/2,0)`, `(0,0,-1,0)`;
* `P_+`, `P_-`, `-P_+/2`, `-P_-/2`, where
  `P_±=(-1/4,±1/4,-1/4,∓1/4)`;
* `Q_+`, `Q_-`, `-Q_+/2`, `-Q_-/2`, where
  `Q_±=(1/4,±1/4,-1/4,±1/4)`;
* `R_+`, `R_-`, `-R_+/2`, `-R_-/2`, where
  `R_±=(0,0,1/4,±1/4)`.

To prove this, first suppose the order n is not divisible by five. The
relative trace is then the rational Ramanujan value `mu(n)/phi(n)`, also
for the second moment; the familiar rational five-vertex hull contains
all these pairs. If n has five-adic valuation at least two, both the
rational Ramanujan sums and the induced conductor-five Gauss sums vanish,
so both coordinates are zero.

It remains to write `n=2^b*5*m`, with m odd and coprime to ten. A repeated
prime in m again makes both coordinates vanish. For squarefree m, set
`r_m=mu(m)/phi(m)`. The normalized quadratic Gauss sum gives, up to the
choice of sign:

| b | Relative-trace pair |
| --- | --- |
| 0 | `r_m P_±` |
| 1 | `r_m Q_±` |
| 2 | `r_m R_±` |
| at least 3 | zero |

The signs absorb the quadratic character of the exponent and of m. Since
`-1/2 <= r_m <= 1` (the smallest possible odd prime in m is three), each
listed pair is on one of the six displayed endpoint segments. This proves
the all-orders hull without assuming any bound on twist orders.

For a quadratic dimension-field automorphism, modular Galois symmetry
sends theta to `theta^(u²)`. The square automorphism fixes K. Therefore
the first and second normalized relative traces are unchanged. This
allows paired restriction-row types to share a hull vertex even if the
individual twists differ.

In the rank-seven sqrt(5) applications, `D=80*(9+4*s)` with the factor in
parentheses an algebraic unit. For a possible central dimension `z=a+b*s`,
the necessary integrality of D/z is equivalent to that of 80/z. Because
the full ring of integers is `Z[(1+s)/2]`, the exact test is

`a²-5b² divides 160a and 160b`,

with the two integer quotients having the same parity. Requiring both
80a and 80b to be divisible would be unjustifiably stronger and is not
used by the implementation.
