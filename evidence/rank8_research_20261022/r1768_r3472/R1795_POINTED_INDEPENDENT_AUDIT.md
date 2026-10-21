# Independent review of the R1795 pointed-associator restriction

The argument in `../pointed_followup/PROOF.md` proves a necessary condition:
every complex categorification of `R8_3_1795` has trivial associator on its
pointed `C2` subcategory. It does not exclude the fusion ring or construct
a categorification. In particular, it makes the separable algebra `1+g`
available in a hypothetical categorification; it does not identify that
algebra's complete categorical Morita dual.

## Mathematical review

In a pseudo-unitary categorification, write `I(g)=sum m_Z Z` and let
`z_Z` be the positive dimension of `Z`. The central-induction trace formula
gives `sum m_Z z_Z theta_Z^2=epsilon D`, where `epsilon=nu_2(g)` is `+1`
or `-1`. Its absolute value equals the positive sum `D`; equality in the
triangle inequality forces `theta_Z^2=epsilon` for every constituent.
The first trace is zero because `g` is nontrivial, so the two possible
twist fibres have equal dimension mass `D/2`.

The source tensor directly gives `B[0,g]=0` and `B[g,g]=8`. Thus an
induction constituent with multiplicity `m` and dimension coordinates
`(z_0,z_1)` contributes `(m^2,m z_0,m z_1)` to the Gram and fibre mass.
For this ring `D/2=(270,120)` in the basis `(1,sqrt(5))`. All relevant
coordinates are nonnegative integers. Hence the coordinatewise bounded
integer packing search is complete for this necessary relaxation. It
allows arbitrarily many different central simples with the same column,
so it imposes no unwarranted distinctness condition. The complementary
fibre must have Gram value `8-q`. A deleted column could occur in no
actual pair of fibres; iterating deletion preserves this implication.

For `epsilon=-1`, all the relevant twists are `+i` or `-i`; their first
four relative trace powers over the real FP field are `(0,-1,0,1)`.
The phase restriction is applied only to columns supporting `g`. All
unaffected columns and all inherited rotation constraints remain in the
relaxation. No bound on the actual twist order is introduced.

The eight exact separating certificates cover all admissible assignments
with `nu_2(g)=-1`. The nonzero class in `H^3(C2,C*)=C2` has precisely
this canonical indicator in a pseudo-unitary category. The previously
accepted general-to-Galois-pseudo-unitary gate applies to this fusion
ring, and Galois conjugation fixes that unique nonzero cohomology class.
Consequently the restriction transfers to arbitrary complex
categorifications. This transfer does not assume that the original
category was pivotal, spherical or pseudo-unitary.

## Independent executable checks

The read-only script `r1795_pointed_independent_audit.py` imports the frozen
base cone and the stable odd-parity snapshot; it uses no optimizer and
does not read the mutable discovery result. It checks:

- the source identity and the directly expanded induction Gram matrix;
- all inherited metadata against the frozen complete cone;
- the Fourier packing domain by a separate constituent-addition closure,
  obtaining exactly 1,187 retained pointed columns;
- an independently reconstructed phase mask of exactly 58,074 columns;
- complete coverage of all eight odd-indicator assignments;
- every exact right-hand-side separation and factored score oracle;
- all 58,074 explicit sparse columns against all eight rays.

Replay with:

```sh
python3 evidence/rank8_research_20261022/r1768_r3472/r1795_pointed_independent_audit.py
```

The script uses active checks, so optimization does not disable its
verification. Primary mathematical references and the inherited all-order
trace-domain argument are given in the producer proof and its referenced
R65 proof. This audit adds no new categorification assumption.
