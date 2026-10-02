# R7_2_240 is the unitary modular D12 even part

The D12 subfactor planar algebra is unitary, and its even part is modular.
Existence and modularization are established by Morrison--Peters--Snyder,
*Knot polynomial identities and quantum group coincidences*,
[arXiv:1003.0022](https://arxiv.org/abs/1003.0022), Theorem 2.2 and Proposition
2.4. Its fusion formulas appear in their *Skein theory for the D2n planar
algebras*, [arXiv:0808.0764](https://arxiv.org/abs/0808.0764), Theorem 4.14.
Here 2n=12, so n=6.

Use the ordered basis

    f0, f2, f4, f6, f8, P, Q.

Write f10=P+Q, and fold f_(20-a) to f_a. Bulk products follow the SU(2)_20
truncated Clebsch--Gordan rule under this fold. For 0 <= j <= 4,

    P f_(2j) = sum_(k=5-j)^4 f_(2k) + (P if j even, Q if j odd),

and the rule for Q interchanges P and Q. The remaining products are

    P^2=Q+f2+f6,    Q^2=P+f2+f6,    PQ=f0+f4+f8.

These formulas determine every structure constant. They also show that P*=Q;
all five bulk simples are self-dual.

Equivalently, take the standard unitary SU(2)_20 modular category and the
bosonic algebra A=1+V20. The twist of V20 is
exp(pi i*20*22/(2*22))=1. Its local modules form the modularization of the even
subcategory PSU(2)_20. The free objects V0,V2,V4,V6,V8 give five simples, while
the fixed object V10 splits into P and Q. This is the cited D12 even category.

The bijection from the displayed model basis to the census basis is

    [0, 5, 3, 6, 4, 1, 2].

`verify_d12.py` constructs the model tensor directly from the formulas,
compares all 343 coefficients with the pinned census, and checks all 2401
associativity equalities independently in integer lists. The tensor also
passes the baseline symbolic based-ring validator. The source binding is
`r7_2_240_source.json`; its census tensor SHA256 is
`b367ba34247e0bac11d8dc4c92abc19a79d3898a1438e2f33aab5dc4c812a9a3`.

Consequently R7_2_240 has a unitary modular categorification, hence also a
general complex fusion-category categorification.
