# Independent audit of the R1660 profile-133 exclusion

The proposed cut is valid, conditional only on the already established
profile and categorical reductions. It removes zero-based profile 133 in
low frame zero, labelling `[0,5,4,1,3,2]`. The independent arithmetic
checker `audit_galois_cut.py` reads the raw frozen profile and does not
import the new Galois verifier or its dynamic program.

## Signed Galois and the fermion

Write s for the normalized center S matrix. For each low simple Aχ,
the established low-row formula is

\[
s_{A_\chi,Z}=\chi(F(Z))/f_\chi.
\]

The Galois automorphism σ₅ of Q(ζ₄₈) negates √2 and √3 and fixes √6.
Its signed permutation π satisfies
σ₅(sᵢⱼ)=εⱼsᵢ,π(j). Thus the matrix B₅ in the new verifier is characterized by

\[
f_\chi\,\sigma_5(\chi(v))
=\sigma_5(f_\chi)\,\chi(B_5v).
\]

The six characters form an invertible character table, so all 36
basis identities imply B₅v=ε_ZF(πZ). The displayed B₅ passes these exact
identities. In particular, it sends a σ-supported vector
(0,0,b,c,1,3), b+c=4, to minus (0,0,c,b,1,3).

Let h be the central fermion, with monodromy charge ηⱼ∈{±1}.
The normalized-S identity sₕZ,j=ηⱼsZ,j and the rationality of ηⱼ imply,
after applying σ₅, that the rows indexed by π(hZ) and hπ(Z) agree up to
the Galois signs. Invertibility of s forces π(hZ)=hπ(Z), with equal
signs. The column-ratio identity η_Z=sₕZ/s₁Z separately shows that
π preserves charge. Thus π preserves even pairs, odd pairs and odd
h-fixed objects. The coherent α also commutes with h because α(h)=h.

Consequently γ=π₅α preserves each σ-supported restriction fiber and
its h-fixed locus. Galois twist symmetry gives θπ₅Z=θ_Z²⁵; on the
primitive-order-16 σ-supported objects this equals −θ_Z. Since α
preserves twists, γ pairs the θ and −θ strata.

Every σ-supported object is non-self-dual: its restriction has odd
multiplicity of σ (indicator −1) and of σX (indicator +1), so a
nondegenerate self-duality cannot have one transpose sign on both
odd-dimensional multiplicity spaces. Duality preserves the h-fixed
locus and preserves twists. Each twist stratum in that locus therefore
has even cardinality. The γ-bijection equates opposite-twist stratum
cardinalities, proving that the total h-fixed count is divisible by four.
**No commutation of γ with duality is required.**

The same reasoning applies to the whole σ-supported restriction fiber,
so its cardinality is divisible by four. Together with the previously
proved even number e of charge-even h-pairs, this makes the number o
of odd h-pairs even in n=2e+2o+t.

The Galois input is Dong–Lin–Ng, *Congruence property in conformal field
theory*, [arXiv:1201.6644](https://arxiv.org/abs/1201.6644), particularly
the signed S symmetry and Lemma 4.2 for the canonical representation
of a Drinfeld center. That lemma gives the squared Galois action on
the actual center twist, with no anomaly normalization left over.

## Search-free contradiction for profile 133

Remove the four forced high partners of the even low objects. The
remaining seven symmetric restriction types have (x,a), where
x=[X]+[gX] and a=[σX],

| Type | (x,a) | Multiplicity | Even-pair weight |
|---|---|---:|---|
| 1 | (0,1) | 2 | 2 |
| 2 | (2,2) | 2 | 12+8√2 |
| 3 | (4,2) | 1 | 24+16√2 |
| 4 | (4,3) | 2 | 34+24√2 |
| σ | σ-supported | 8 | 36+24√2 |
| 6 | (8,4) | 2 | 96+64√2 |
| 7 | (8,8) | 1 | 192+128√2 |

There are 18 residual objects. The even dimension balance is 180+120√2.
Types 3 and 7 have e=0, types 1,2,4,6 have e∈{0,1}, and eσ∈{0,2,4}.
Subtracting 3/2 times the irrational-coefficient equation from the
rational equation gives e₁=e₄. The remaining equation is

\[
e_2+3e_4+3e_\sigma+8e_6=15.
\]

Its only possibilities are
(e₁,e₂,e₃,e₄,eσ,e₆,e₇)=(1,0,0,1,4,0,0) and (0,1,0,0,2,1,0).
The former has E=6 and hence O=18−3E−3=−3, impossible.
The latter has E=4, O=3 and total fixed count 4.

Only types 1,4,σ can now contribute odd pairs. B₅ exchanges types 1
and 4, so o₁=o₄. Therefore 2o₁+oσ=3. The capacities o₁≤1 and oσ≤2
force o₁=1 and oσ=1. Hence

\[
t_\sigma=8-2e_\sigma-2o_\sigma=8-4-2=2,
\]

contradicting four-divisibility. This contradiction does not need the
AMV/FS16 residue test; the old dimension and rank equations, Galois
orbit matching, and the new h-fixed parity suffice.

The full new verifier was also replayed against all 1670 source-bound
profiles. Its survivor witnesses show that only profile 133 is removed
by the implemented necessary conditions, leaving 163+753+753=1669.
