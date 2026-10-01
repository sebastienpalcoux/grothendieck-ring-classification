R6_9_8785: complete nonexistence over C, including nonpivotal categorifications.

Replay from this directory (Python 3, SymPy, g++ C++17):
  python -O verify_8785.py
  python -O verify_quadratic_8785.py
  python -O verify_signed_8785.py
Each defaults to sibling tensor_8785.json; an alternate tensor JSON path may be passed.
All runtime checks remain active with Python optimization.
The signed search completes in approximately 30 seconds on the tested machine.
A timeout is an error, not an exclusion.

Dependencies of the complete mathematical proof:
  general_proof_8785.tex: complete argument, including the FS-normalized domain proof.
  proof_8785.tex: pseudo-unitary character-reciprocity and twist-moment obstruction.
  Shared higher_fields_proof.tex and verify_higher_fields.py: excludes signed
  dimension-field degrees four and six. Obtain these from the gauss8200 bundle.

The standalone signed engine imports no repository code. Its exact successful
completion has 2247571340 nodes, 55 equations and zero solutions. A second agent
independently reviewed the engine and reproduced that report under python -O.

Exploratory scripts, compiled binaries, time-limited searches and numerical
relaxations are deliberately absent from this publication bundle.
