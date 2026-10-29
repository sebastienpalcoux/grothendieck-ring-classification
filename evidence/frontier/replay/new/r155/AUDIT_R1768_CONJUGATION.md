# Independent audit of the R1768 conjugation-pairing exclusion

Date: 29 October 2026. **Accepted**, conditional on the previously established
spherical/Galois reduction and positive second-indicator theorem, which are
separate inherited premises.

The pivotal sign calculation is direct and requires no Morita equivalence,
module-trace normalization, braiding, or unitarity.

Let j:Id→(**) be the pivotal structure. For an ε-symmetric nondegenerate
selfduality f:Y→Y*, the transpose convention is f^t=f*∘j_Y=εf. For arbitrary
X, put U=X⊗Y⊗X*. Under the standard coherent identifications

    U*=X**⊗Y*⊗X*,

its selfduality is the isomorphism

    f_U=j_X⊗f⊗id_{X*}:U→U*.

Its transpose is

    f_U* j_U
      = j_X⊗(f* j_Y)⊗(j_X* j_{X*})
      = ε(j_X⊗f⊗id_{X*})
      = ε f_U.

The penultimate equality is precisely pivotal compatibility with duals:
j_{X*}=(j_X*)^{-1}. Thus conjugation preserves the actual pairing sign.
This statement concerns a chosen nondegenerate selfduality, not functoriality
of numerical indicators under a nonmonoidal operation.

In a semisimple pivotal category, decomposing an ε-paired object into simple
isotypic blocks gives an alternating nondegenerate multiplicity-space form
whenever a selfdual constituent has indicator −ε. Such a constituent has
even multiplicity. This follows immediately by tensoring its chosen simple
selfduality with the multiplicity-space form and applying pivotal transpose.

For the frozen tensor R8_3_1768, all basis simples are selfdual. The accepted
positive pivotal indicator vector is (1,−1,1,1,1,1,1,1). A direct independent
multiplication in data/current_remaining_cases.py gives

    X_2 ⊗ g ⊗ X_2
      = g + 2X_2 + 2X_3 + 2X_4 + 2X_5 + X_6 + X_7.

Since g has indicator −1, the conjugated object has a negative nondegenerate
pairing. X_6 and X_7 have indicator +1 but occur once. This contradicts
isotypic parity and excludes the positive representative. The inherited
existence reduction then excludes general complex categorification.

I independently evaluated the displayed product as
Σ_k N[2][1][k]N[k][2][j] for every j, obtaining
[0,1,2,2,2,2,1,1]. The contradiction uses no numerical computation and no
associator search. The previous all-GH6 route result is superseded by this
general obstruction once the inherited gate and indicator theorem are retained.
