# Independent audit: R928 patterns 49 and 191 are impossible

The proposed obstruction is valid under the explicitly inherited positive-spherical existence gate and the established decomposition Z(C)=Sem tensor B. It removes **two center patterns**, not the ring: patterns 40 and 186 are not removed by this argument.

## Categorical premises

Let S denote the symmetric normalized modular matrix of B, with S(0,0)=1/L and L=D/sqrt(2), where

    D = 144 + 96 sqrt(2) + 80 sqrt(3) + 56 sqrt(6).

Its normalization is unitary as a matrix; a unitary associator is not required. The four known Galois-unit simple objects A_0,...,A_3 have dimensions r_sigma=D/sigma(D), and their normalized columns are

    S(X,A_sigma)=r_sigma sigma(d_X)/L.

These are the inherited Galois-column identities already used in the published spectral reduction. They are checked arithmetically here, not rederived from associators.

All four objects A_sigma have twist 1 in **B**, not merely after multiplying by the semion. This placement needs justification and is not a generic assertion that Galois conjugates of the unit always have twist 1. In this case the four objects are the scalar-character summands of the canonical algebra I(1) in Z(C), so their twists there are 1. Their four scalar source characters satisfy chi_sigma(g)=1. The distinguished-center character identity therefore gives monodromy charge

    q(A_sigma)=chi_sigma(g)/dim(E_sigma)=1

against the central semion G. Thus they belong directly to B=Sem', and their twists in B remain 1. The corresponding fifth, two-dimensional-character summand has negative charge; it is deliberately not included in this assertion. The exact source JSON independently confirms the four scalar dimensions, their g-values, and the four unit multiplicities 1.

## Short obstruction

Patterns 49 and 191 each require a simple H of dimension

    d_H=L/2=48+36 sqrt(2)+28 sqrt(3)+20 sqrt(6).

For the four Galois automorphisms (++),(-+),(--),(+-) on (sqrt(2),sqrt(3)), the formula above forces

    (S(H,A_0),...,S(H,A_3))=(1,-1,-1,1)/2.

The squared absolute values of these entries already sum to 1. Unitarity of normalized S forces every other entry of row H to vanish. Since H is not one of A_0,...,A_3, this gives S(H,H)=0. Symmetry gives the same four entries in column H.

Put T=diag(theta_X), using the actual twists. Since theta(A_sigma)=1,

    (S T S)(H,H)=sum_sigma S(H,A_sigma)^2=1.

But the modular identity is

    S T S = xi T^{-1} S T^{-1}

for a nonzero anomaly xi. Its (H,H) entry is xi theta_H^{-2} S(H,H)=0. Contradiction.

No value of theta_H or xi can repair this contradiction. No self-duality assumption on H is needed, no extra assumption on all remaining twists is used, and the more elaborate forced-fusion-matrix/projection argument is unnecessary.

## Independent finite check

`audit_r928_bosonic_row.py` uses SymPy, independently of the earlier quartic-field implementation. It checks all r_sigma sigma(D)=D identities, both occurrences of d_H=L/2, all eight forced S entries, the norm saturation, and the source scalar-character/low-column facts. Output: `audit_r928_bosonic_row.json`.

The inherited complete four-pattern theorem and the general-complex existence gate remain mathematical prerequisites. The independent check proves neither of those categorical theorems. This audit finds no new gap in their **use** by the two-pattern obstruction.

## A slightly broader bound

For possible future use, suppose a row X has real entries in a collection J of twist-one columns, and X is not in J. Write a=sum_{j in J} S(X,j)^2. Matrix unitarity leaves row norm 1-a outside J, so |S(X,X)|<=sqrt(1-a). If the anomaly has absolute value 1, the diagonal modular relation gives

    a <= (1-a)+sqrt(1-a),

and hence a<=3/4. Therefore bosonic real-column mass greater than 3/4 is already impossible, even before exact norm saturation. This broader inequality gives no additional elimination for patterns 40 or 186 in the present data. It is a necessary condition, not a construction test.
