# R623: thirteen remaining integer central profiles

Assume the forced central-semion lift described in R623_central_semion.md.
Let z denote that order-two central simple and put T(W)=z tensor W* for simples
of Z(C). This involution has no fixed point. Indeed, a fixed point would give
W*=zW. In the braided center, the monodromy scalar M(z,W) is ±1 because z^2=1.
The ribbon identities would imply theta_W=theta_W*=theta_z theta_W M(z,W),
contradicting theta_z=±i. This argument is used ONLY in the braided center.

All noninvertible input simples satisfy X*=zX, so restriction coefficients of
W and T(W) agree on every noninvertible. On the pointed coefficient classes
{1,2} and {9,10}, T exchanges the two coefficients. The remaining classes are
{3,5,7} and {4,6,8}, with coefficients denoted a,b.

The unique-dimension central summand of I(1) is selfdual. This first eliminates
two of the four old PSD branches; the other two have the same multiset of low
columns. Add the six distinct central simples z times those of I(1), with
their forced dimensions and restrictions. Their twists have averaged powers
(0,-1,0,1,0,-1) through height6. Subtracting all twelve known columns leaves
this exact Gram matrix on the four coefficient classes:

    [6,0,6,6]
    [0,6,6,6]
    [6,6,32,30]
    [6,6,30,32].

Its zero (1,2) entry forces each remaining column to have pointed coefficients
(p,0) or(0,p). A T pair therefore consists of

    (p,0,a,b), (0,p,a,b).

Summing its noninvertible Gram contributions gives

    sum a^2=16, sum b^2=16, sum ab=15,
    hence sum(a-b)^2=2.

Duality pairs the T pairs with unequal coefficients, exchanging a,b. Therefore
there is exactly one four-object orbit with a=m+1,b=m, its dual orbit having
these coefficients interchanged. The Gram bounds give p∈{0,1},m∈{0,1,2}.
Its simple-object dimension is beta=2p+3(2m+1)d. The necessary conditions
D/beta algebraically integral and beta a d-number eliminate five of these six
possibilities; the sole survivor is p=m=0. Thus these four center simples have
dimension3d and coefficient columns(0,0,1,0) twice and(0,0,0,1) twice.

Every other T pair has a=b=t. The remaining equations become

    sum p^2=6, sum pt=6, sum t^2=15.

The same dimension integrality filters leave the seven pair types

    (p,t)=(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,2).

There are exactly thirteen nonnegative integer solutions for their counts.
The portable verify_R623_profiles.py reconstructs the Gram matrix from frozen
input, verifies all arithmetic filters, exhausts these tiny equations, and
checks the resulting full Gram matrices. The proof above establishes domain
completeness; the replay is an exact check, not an optimizer search.

A further bounded research probe uses all65 joint relative-trace pairs for
(theta,i theta), including the zero pair for unbounded orders, at height6.
Each of the thirteen integer profiles was imposed separately. One profile has
an exact checked Farkas obstruction; twelve were not separated. This does not
prove their categorical feasibility. Adding exact pointed cocycle indicators
also excludes the class3/noninvertible-third-average−1/2 combination, but the
other branches were not separated. The present work therefore retains R623
as unresolved.

Research scripts semion_*_probe.py and semion_integer_profiles.py use the old
criterion implementation to seek and check rays. Their failed separation
results are recorded only as search history. The portable structural replay
verify_R623_profiles.py requires neither that implementation nor an optimizer.
