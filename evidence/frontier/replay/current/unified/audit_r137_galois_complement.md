# Independent audit of R137's full-character Galois complement rule

**Verdict:** the categorical rule and its implementation pass this audit. It yields a stronger necessary domain and multiplicity-pairing equations. It is not by itself an exclusion of the ring.

## Exact rule

Let K=Q(sqrt(2)), let sigma restrict nontrivially to K, and choose a lift to the cyclotomic field of the modular data of Z(C). Use the canonical center normalization s=S/D. For each of the nine source characters E, the previously established distinguished-center formula is

    s(A_E,Z)=chi_E(v_Z)/f_E.

The normalized modular Galois column rule gives

    sigma(s(A_E,Z)) = epsilon_Z s(A_E,pi_sigma(Z)),

where epsilon_Z is +1 or -1, independent of E. Therefore, putting v'=v_(pi_sigma Z),

    chi_E(v') = epsilon_Z (f_E/sigma(f_E)) sigma(chi_E(v)).

This derivation does not need a separate assumption about how the distinguished I(1) labels permute. The nine characters separate the commutative source fusion algebra. Direct exact calculation of the resulting linear transformation T gives, with

    a=v0+v1+v2+v7+2v8,

the following formula:

    (Tv)_i=v_i                 for i=0,1,2,7,8,
    (Tv)_i=a-v_i               for i=3,4,5,6,
    v'=epsilon_Z T(v).

The auditor independently checked all 81 character/basis identities and T squared equals the identity, using rational arithmetic in Q(d), d=4+3sqrt(2).

If a>0, at least one of the unchanged integral coordinates is strictly positive. Nonnegativity of v' consequently forces epsilon_Z=+1, and hence v_i<=a for each large coordinate. If a=0, all integral coordinates vanish; a nonzero column has at least one positive large coordinate, so epsilon_Z=-1 is forced and v'=v. Neither case may be silently omitted.

## Pairing the twist types

In the canonical center normalization, the modular Galois twist rule sends theta_Z to sigma squared(theta_Z), up to using the inverse label convention. Since sigma restricted to K has order two, sigma squared fixes K. It follows that every normalized relative trace to K of theta_Z to the n-th power is unchanged. This is exactly the first-four-moment trace type stored by the finite system.

Thus the total number of simples with a given restriction vector v and trace type t equals the total with its physical partner vector and the same t. When several variables encode the same pair (v,t), their multiplicities must first be aggregated. The rule does not equate arbitrary individual duplicate variables.

This reasoning does not require specifically choosing the automorphism with exponent 5 or assuming that 5 is coprime to a proposed conductor: sigma squared fixing K is sufficient.

## Independent implementation check

The positive-TY saved domain has 22,179 physical variable columns. The new negative-complement rule forbids 13,466 of them, including **8,752** not forbidden by the old filter. The complete saved domain also lacks the required partner trace type for 351 otherwise nonnegative columns; 269 of these are newly forbidden. Thus the combined filter removes **9,021 additional variables**, for 16,243 forbidden variables in total, and supplies **2,508 aggregated pairing equations**.

The auditor independently reconstructed these sets and equations and matched them exactly to `complement_metadata.json`. The old 102-support witness uses one newly forbidden variable and violates eleven of the pairing equations. This rejects that particular witness from the strengthened system.

The missing-partner deletion step uses the inherited theorem that the saved finite domain includes every categorical column/trace type. The negative-complement inequality itself does not need finite-domain completeness. The old general-complex existence gate and distinguished-character-row theorem remain explicit categorical prerequisites for applying the rule to general complex categorifiability.

This audit establishes the Galois restriction only. The separate exact positive-sign certificate audit supplies the branch contradiction; the negative-sign witness audit checks its current necessary-data solution. Neither is a categorification.

Replay: `python unified/audit_r137_galois_complement.py`. Receipt: `audit_r137_galois_complement.json`. No optimizer is invoked.
