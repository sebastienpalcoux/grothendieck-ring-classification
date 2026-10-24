# Two new general exclusions in dimension 120

**R9_2_12 and R9_2_959 have no complex fusion categorification**, by the
unified argument in `THEORY.md`. This also excludes unitary models. The
proof is ready for independent phase-five audit; the finite verifier passes.
No online files, repositories, earlier phases, or canonical ledgers were
edited by this subtask.

The argument closes the precise gap left in phase four:

1. Both rings force induction dimensions `1,4,4,5,6,20,20,30,30`.
   A new fermion-parity argument using `S[I(1)]=120[I(1)]` forces a
   Tannakian subcategory in the Drinfeld center. Dai's dimension-120
   theorem then forces weak group-theoreticality.
2. Every nonsolvable weakly group-theoretical category of dimension 120
   is group-theoretical: its nilpotent Morita tower can have only an A5
   step and a possible C2 step, and either order gives a pointed category.
   The separately audited phase-four all-cocycle exclusions therefore
   force a hypothetical categorification to be solvable.
3. Trivial universal grading forces its last solvable step to be a
   C2-equivariantization. Exhausting the source involutions gives only
   two dimension-60 types, `(1^2,2,3^2,6)` and `(1^6,3^6)`. Neither can
   be solvable. Their possible cyclic-prime descents reduce to an
   impossible dimension-three simple at dimension 30, or to a C3 action
   on a group of order 20 with too few fixed elements.

The proof treats arbitrary associators, allows a possible central
fermion, and never assumes all categories of dimension 120 are
group-theoretical. The earlier no-GT theorem is used only within its
independently audited scope.

Run the standard-library verifier from any directory:

```
python -S /path/to/rank9_m2_research/phase5/integral120/verify_reductions.py
```

It reads the original compressed census input, checks the two full tensors,
formal codegrees, induction parity, every involution descent, and the
complete grading-dimension bookkeeping. It also checks the phase-four
accepted GT receipt, independent audit, and audited source hashes. It
writes `reductions_certificate.json`. No GAP, local Git checkout, NumPy,
SymPy, or optimization solver is required. Run without Python's `-O` flag.

The dimension-120 literature was checked afresh, including the 2025 Dai
paper and the 2026 publication of Dong's classification below dimension
120. The new argument supplies the missing reduction; it does not claim
that either source already contained these two exclusions. Primary
references and the exact categorical dependencies are listed in `THEORY.md`.
