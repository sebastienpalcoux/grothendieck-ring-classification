# Scope and completeness of the rank-eight involution-module pass

The pass began with the 34 cases remaining after the ten general
exclusions proved earlier in this update. Every involution was inspected
using **right** fixed simples, including in the noncommutative rings.
The eight new exclusions are in `ANTI_MODULE_EIGHT_GENERAL_PROOF.md`.

Among the remaining 26 cases, exactly four admit this module test:

| Case | Involution | Right-fixed labels | Anti-representations up to sign gauge | Dual-module Gram result |
|---|---:|---|---:|---|
| R8_2_342 | 5 | 3,7 | 1 | No exclusion found |
| R8_2_630 | 1 | 6,7 | 1 | No exclusion found |
| R8_2_666 | 1 | 6,7 | 1 | No exclusion found |
| R8_2_671 | 1 | 6,7 | 1 | No exclusion found |

The self-contained portable verifier `verify_frontier_modules.py`
reconstructs all 34 census tensors, checks their current ledger hashes,
and reproduces the complete involution/fixed-simple inventory. For each
of these four cases it exhausts the bounded integral anti-representations
using a generating-word basis and verifies the unique sign-gauge class.
The legacy `module_dual_gram.anti_representations` helper only tries up
to two generators: it skips 342 and 666, which need three. Cases 630 and 671
have two-generator presentations. The portable replacement handles all
four and verifies the original fusion relations directly.

`four_remaining_gram_witnesses.json` supplies nonnegative integral Gram
factors for every one of the six non-unit module simples in each case.
The verifier reconstructs the full module matrices, positive quadratic
FP-dimension character, the dual dimension multiset from I+M_g, and all
24 internal-end Gram matrices. It checks BB^t=Q exactly and checks each
column's weighted FP dimension, including the required multiplicity of
each dual dimension class. It uses no optimizer and no imported legacy
software. These are separate necessary-condition witnesses; they do not
assert simultaneous compatibility of dual fusion actions or construct
categorifications. Normal and optimized receipts are
`frontier_modules_normal.json` and `frontier_modules_optimized.json`.

Every involution in the remaining noncommutative cases R8_1_49,
R8_2_36, R8_2_37, R8_2_170, R8_2_314, R8_2_412, R8_2_432 has no
right-fixed simple. The same is true for every involution in the other
remaining cases; R8_2_820 and R8_2_869 have no nontrivial involution.
Thus there is no omitted positive fixed-count case in the original
34-case frontier.

The general lemma itself does not require commutativity. Normality is
used only for the chosen generator, and `verify_anti_module_eight.py`
checks the exact relation XX*=X*X for that generator. This distinction
is preserved in both the proof and manuscript.

A further exploratory pass enforced the necessary condition
Q-vv^t positive semidefinite for every candidate Gram column. It used
an independent principal block P of Q, requiring v to lie in the range
of Q and v_P^t P^{-1}v_P <= 1. This reduced the column domains to 5--23
columns, without producing a contradiction. Nonnegative integral
solutions of all 24 resulting separate Gram systems were then found
and checked by exact matrix multiplication. These separate solutions
are not claimed to be mutually compatible dual fusion actions.
