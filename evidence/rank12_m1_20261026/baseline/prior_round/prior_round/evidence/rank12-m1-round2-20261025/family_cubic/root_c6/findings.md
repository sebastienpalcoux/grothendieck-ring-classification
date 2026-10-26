# Five quadratic C6-type cases: further theoretical investigation

No additional categorification or general exclusion is claimed here for R12_1_332, R12_1_350, R12_1_561, R12_1_623 or R12_1_628. These findings are distinct from the twenty completed cubic exclusions in the parent directory.

## Exact structural distinctions

All five rings have six invertibles acting freely and transitively on six noninvertibles. Thus none has a nontrivial simple-object stabilizer: the paired stabilizer criterion has no direct application. Their transitive two-dimension property gives the established Galois pseudo-unitarity reduction, but does not imply unitarizability.

R332 has dimension d=(3+sqrt(13))/2 and a C2 grading with neutral Haagerup-C3 ring on labels {0,3,4,9,10,11}. Its invertible group is S3. Conjugation by an odd invertible inverts the neutral C3. A crossed-product construction therefore requires an actual tensor autoequivalence of the chosen neutral category inducing that inversion.

The other four have d=3+sqrt(10), with d^2=1+6d. They are not mere basis relabelings of the established generalized-Haagerup C6 model R326:

| Ring | Pointed group | Rule for rho g | Self-dual noninvertibles |
| --- | --- | --- | ---: |
| R326 (known model, control) | C6 | g^-1 rho | 6 |
| R350 | S3 | g rho for the central self-dual representative rho=11 | 4 |
| R561 | C6 | g rho | 2 |
| R623 | C6 | g^-1 rho, with rho^2 having the nontrivial involution as its invertible summand | 0 |
| R628 | C6 | g rho, and no self-dual representative | 0 |

Full primary-3 numerical probes for all five completed in less than one second in total and gave only numerical zero as the least eigenvalue. No exact positivity conclusion or new classification is inferred from these probes; the attempt receipts explicitly retain that scope.

## R332: the twisted neutral categories must be included

The known outer-automorphism calculation for the usual untwisted Haagerup categories is insufficient for arbitrary original categories. In particular, twisted Haagerup-C3 categories really exist. Izumi, *A Cuntz algebra approach to the classification of near-group categories*, arXiv:1512.04288v2, Example 12.14, constructs two such categories by de-equivariantizing the two cyclic C9 near-group categories along their order-three subgroup. The pointed C3 associators have opposite nontrivial classes.

Example 12.13 instead starts with the C3 x C3 near-group category and gives the two untwisted Haagerup categories. These two precursor groups must not be confused. Section 13.3 describes automorphisms of an actual m=|G| near-group category as the group automorphisms preserving its full bicharacter, a and b data. Inversion of the underlying cyclic group by itself does not establish a tensor autoequivalence.

The recent Gannon–Schopieray–Yadav paper arXiv:2609.25185v1 explicitly restricts its completeness statement to untwisted Q-system-type HI categories. It does not establish the premise needed to identify every possible original neutral categorification with one of the usual unitary examples. No unsupported categorical classification is substituted here.

Primary references:

- <https://arxiv.org/pdf/1512.04288>, Examples 12.13–12.14 and Section 13.3.
- <https://arxiv.org/html/2609.25185v1>, introduction, Theorem A and its stated hypotheses.

## R350: a finite conditional Morita reduction

There is a useful conditional route when the associator of the pointed S3 subcategory is trivial. It is not a general exclusion, because the required triviality has not been proved.

With that hypothesis, the regular subgroup algebra A_G exists. The central self-dual representative rho=11 satisfies rho g=g rho and rho^2=1+sum_g g rho. Since H^2(S3,C*)=0, the corresponding pointed bimodule sector has the regular bimodule structure. Its Morita dual has the Rep(S3) sector (1,u,T) and noninvertible sector (S,uS,W=TS), of dimensions d,d,2d. The Rep(S3) action gives uW=W and TW=S+uS+W. Consequently

\[
S^2=\alpha+aS+b\,uS+cW,\qquad a+b+2c=6,
\]

where alpha is 1 or u. If alpha=u, dual reversal requires a=b. Moreover

\[
W^2=1+u+T+(a+b+c)(S+uS)+(a+b+3c)W.
\]

Hence every coefficient is at most nine. The twenty ordered choices are a tiny list; no new census is required. `R350_conditional_Morita_candidates.json` contains their full tensors and exact basis identifications with the existing rank-six classification, together with the retained recorded decisions. Every one is recorded there as excluded. Physical census row ordinals are kept separately from the permanent classification IDs; they must not be conflated.

This inventory is a structural research reduction, not a newly accepted rank-twelve exclusion. It does not replay the full lower-rank categorical certificates, and it does not establish the pointed-associator premise. In particular, the two harder surviving arithmetic types (a=b=1,c=2) match R6_8_1262 and R6_8_200 and require their higher-indicator certificates rather than a d-number shortcut.

## Other routes with explicit remaining premises

For the two commutative C6 cases, a central Tannakian C3 lift would permit de-equivariantization toward a rank-four quadratic category with the large coefficient three. But commutativity of the based ring does not supply a half-braiding, so that lift is not assumed.

Likewise, the regular algebra on an order-two pointed subgroup is not automatic in these freely acting quadratic categories. A nontrivial pointed associator may obstruct it. The successful algebra 1+g in the completed C9 argument was supplied by a fixed dimension-two simple; these five rings have no such fixed simple. That proof cannot be transferred without this categorical premise.

The two all-non-self-dual rings are also not modeled by matching only dimensions or the pointed group with a known C6 generalized-Haagerup category. The duality and right-action data differ, as the table shows. No actual new coherent construction was obtained in these attempts.
