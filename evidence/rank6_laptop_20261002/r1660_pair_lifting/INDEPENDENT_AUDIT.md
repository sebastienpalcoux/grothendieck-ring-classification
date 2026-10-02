# Independent audit of the R1660 laptop package

Audit date: 2026-10-02. **Approved as a bounded necessary-condition search.** This approval does not assert that R6_8_1660 is excluded or realized, and no complete profile scan was performed.

The audited runner has SHA256 `2dc1d8c9296847e6c6cc8c5ee1e001eb76af2503845f844788b68b876befbe50`; the input has SHA256 `b7f262afdb4d4345d653b42399830faa6e2842d874ddc3da4e96778fcf0162d4`.

## Mathematical review

The forgetful-functor product equation and all three coordinatewise Frobenius-reciprocity bounds are necessary over the complex numbers. The selfduality of the six base simples identifies restriction vectors of dual central simples; it does not identify the central simples themselves. Repeated restriction vectors retain their full simple-object multiplicities. Aggregate caps are the individual cap multiplied by that multiplicity, with safe additional coordinate bounds.

The distinguished central unit is removed exactly once. Equal restriction types of multiplicity at least two require separate feasibility tests with unit coefficients zero and one, because both actual-dual pairs and nondual pairs exist. Different restriction types require unit coefficient zero. These quantifiers are valid without selecting a central duality permutation. Skipped low–low and invertible-input pairs only weaken the test.

The ungraded input avoids conditioning a claimed obstruction on one arbitrarily retained charge assignment. The method is new here for low–high and high–high products; no strict reduction of the existing frontier has yet been demonstrated. Any eventual ring exclusion still requires all surviving profiles to fail, independent verification of those failures, and validation of the preceding profile reduction's hypotheses and completeness.

## Implementation and source review

The bounded depth-first solver was reviewed for every pruning inequality, signed coordinate-difference bound, gcd condition, and memoization step. Incomplete branches cannot enter the impossible-state cache. Node and time limits produce `unknown_budget`, distinct from complete infeasibility. Feasible witnesses are verified against all exact equations and caps.

The checkpoint binds the input, algorithm, and runner hashes. Completed pair results are committed individually; larger limits or explicit retry can revisit unknowns. Profile and alias accounting survives resume and summary generation. Changed checkpoint identities and modified input bytes are rejected.

Independent reconstruction from the frozen source profiles checked all 1,136 original aliases, their exact bijection with the retained list, all 628 distinct ungraded multisets, and every recorded source-file hash. See `source_input_audit.json`.

`README.md` and `PROOF.md` accurately distinguish feasible individual products, unresolved searches, candidate profile obstructions, and categorification. `verify_returned.py` reconstructs each claimed system from the pinned source rather than trusting the returned coefficients or caps. It is a source-bound replay with the same solver, not a second independent solver or a proof of profile completeness.

## Reproducible checks

`audit_independent.py` compares 2,400 small systems against independent exhaustive Cartesian-product enumeration. It also checks 11 known-positive Rep(D(S3)) jobs, repeated-fibre unit quantifiers, zero-node unknown results, checkpoint retry and summary, and input/checkpoint mutation rejection. It passes both normally and under `python -O`; essential checks are explicit exceptions. Its package-relative adaptation was compared byte-for-byte with the audited original except for the two intended path changes.

The supplied controls add the multiple-unit-restriction example Z(Vec(C2)), integer-semigroup holes, wrong-witness rejection, zero-time budgets, and 120 further independent small systems. The input generator was checked under `-O` to reconstruct the identical input bytes.

Additional `-O` checks of `verify_returned.py` confirmed that the no-obstruction pilot is handled, a falsely claimed obstruction with a feasible witness is rejected, and a modified bounded system is rejected before solving.

The bounded pilot touched one profile: 93 feasible pair tests, three budget-limited tests, and no obstruction. Passing these controls validates the implementation to the stated scope; it predicts neither the outcome nor the runtime of the full laptop scan.
