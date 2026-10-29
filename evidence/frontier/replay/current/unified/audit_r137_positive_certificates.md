# Independent audit of the positive-TY R137 exclusion

**Verdict:** all nine exact linear certificates pass independent reconstruction on every allowed column. Their integer consequences exclude the positive-TY branch, conditional on the inherited theorem forcing its four projected cubic indicators to be 1/2. This is not an exclusion of the negative-TY branch or of R137 altogether.

The archived 264-equation export contains four final equations setting the projected fourth indicators to 2 as a test branch. These are removed. The verifier uses precisely the remaining 260 equations, nine radical-zero Verlinde equations, and the 2,508 full-character Galois pairing equations. It does not import an optimizer. The allowed column list is reconstructed from the independently checked Galois complement metadata, not blindly accepted from the certificate file.

All nine Verlinde functionals are independently rebuilt using rational-pair arithmetic in Q(d), d^2=8d+2, then converted to rational and sqrt(2) components. Every certificate is checked on all 5,996 allowed physical or slack columns. Its exact right-hand side, nonnegative inequality multipliers, and any previously deduced integer equalities are also checked.

Write n_E=N(B,B;A_E), in the nine-character order used by the case researcher. The exact bounds are:

| Stage | Bounds | Integer consequence |
|---|---|---|
| Initial | 1/2 <= n_7 <= 31/18 | n_7=1 |
| With n_7=1 | n_3,n_6 <=17/30 | n_3=n_6=0 |
| With those three equalities | n_1,n_2,n_4,n_5 <=3/4 | all four vanish |
| Same stage | n_0<=1 | n_0 is 0 or 1 |

Every n_E is a nonnegative integer in an actual modular category. The unit is label E=8, and n_8=1 because B is self-dual. Adjunction gives

    sum_E n_E = dim Hom(B^2,I(1))
              = dim Hom(F(B)^2,1)
              = 5,

because F(B)=1+X3+X4+X5+X6 consists of five distinct self-dual source simples, and every distinguished summand of I(1) has multiplicity one in this commutative case. Thus the eight nonunit coefficients must sum to 4. The certified bounds force their sum to be at most 2, a contradiction.

The numerical optimizer was used by the case researcher to discover certificates, but the independent verification is exact and makes no optimizer call. The all-column slack inequalities and the integer argument, rather than an optimization status or a bounded integer search, establish the branch contradiction.

Files: `audit_r137_positive_certificates.py` and `audit_r137_positive_certificates.json`. The inherited positive-TY cubic reduction and finite categorical domain theorem remain explicit prerequisites; they are not proved by these nine arithmetic certificates.
