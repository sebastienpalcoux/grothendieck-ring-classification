# R6_4_155: reflection refinement of the local braid obstruction

Date: 16 October 2026. **The categorification problem remains unresolved.**

## What was established in this pass

The previously prepared three-strand spectral search was run, and strengthened by exact multiplicative-preprojective reflections. All **226 nonzero blocks of dimension greater than four**, spanning dimensions 6–308 and **80 distinct normalized spectral profiles**, admit partitions satisfying the strengthened necessary conditions. Every input spectrum was recomputed exactly from the source modular data and every partition was checked again. The 70 blocks of dimension at most four had already passed the earlier test.

This result does not construct even the required braid representations: a passing imaginary-root reduction is only a necessary condition. It certainly does not construct associators, braidings, or a categorification. No categorification status changes.

## The additional necessary condition

For a hypothetical irreducible constituent of the tuple `(D^{-1},B,A)`, with `D=BA` and product identity, associate its standard star-shaped quiver. If the ordered eigenvalues on leg i are `xi[i,j]` with multiplicities `m[i,j]`, put

    alpha[0] = r,
    alpha[i,j] = r - sum_{s<=j} m[i,s],
    q[0] = product_i xi[i,1]^{-1},
    q[i,j] = xi[i,j] / xi[i,j+1].

All q parameters are roots of unity, stored as integer exponents modulo 144. Let `(alpha,e_v)=2 alpha[v]-sum_{w~v} alpha[w]`. If this is positive, there are two cases. If `q[v]!=1`, the reflection equivalence replaces `alpha[v]` by `alpha[v]-(alpha,e_v)`, inverts `q[v]`, and multiplies adjacent parameters by the old `q[v]`. If `q[v]=1`, no simple representation exists unless `alpha=e_v`. Indeed the vertex-simple module exists, and the Hom–Ext formula makes a positive pairing impossible between two distinct simples. Negative dimensions or disconnected nonzero support are also impossible. Repetition reduces total dimension until a coordinate-simple vector or the fundamental region is reached; reaching the latter is not an existence test.

The needed references are Crawley-Boevey–Shaw, *Multiplicative preprojective algebras, middle convolution and the Deligne–Simpson problem*, arXiv:math/0404186v2, Theorem 1.7, Lemma 5.1, and Lemma 8.3:
https://arxiv.org/pdf/math/0404186

This filter is applied separately to all candidate Jordan–Hölder constituents. No complete-reducibility or unitarity assumption is made.

## A genuine new local restriction

The full ten-dimensional block `(a,b)=(16,3)` cannot be irreducible, although its original Scott conditions pass. In the normalized exponent convention its spectra are

    A: 0^1,12^1,36^2,60^1,72^2,90^1,108^1,126^1;
    B: 36^2,84^4,132^4;
    D: 54^6,126^4.

Ordering each leg by decreasing multiplicity gives initial star dimension vector

    (10,8,6,5,4,3,2,1,6,2,4)

and parameter exponents

    (78,108,72,132,96,114,126,126,96,96,72).

The edges are the three arms `0-1-2-3-4-5-6-7`, `0-8-9`, `0-10`. Reflections at vertices `0,1,8,0` lead to `alpha[0]=6`, `alpha[10]=4`, and `q[10]=1`. Hence `(alpha,e_10)=8-6=2>0`, contradicting simplicity. Nevertheless a `2+6+2` partition survives, so this is not a categorical obstruction. The symmetry-related blocks have the same restriction.

## Completion of the large blocks

The search budget initially left `(24,24)` and `(25,25)`, both of dimension 308, undecided. They have elementary explicit passing partitions. In normalized modulo-144 exponents, remove respectively the one-dimensional characters

    (A,B,D)=(132,120,108),
    (A,B,D)=(60,120,36).

In each case the remaining dimension-307 triple passes Scott and reflection tests. Thus the final receipt has no `UNKNOWN` entries. This is a verified positive partition, not a negative inference from a timeout.

## Unitary-only exploration

Inspired by Liu–Ding, arXiv:2610.15792v1, rank-one multiplicative Horn inequalities were checked on all 80 normalized profiles, and classical degree-zero rank-two inequalities on profiles of dimension at most 40. No violation was found. Higher-degree/rank Horn inequalities were not exhausted. The exploratory working file `horn_test.py` recorded these limited checks; it is not included in this portable replay and must not be described as a full Horn feasibility test.

Primary source:
https://arxiv.org/html/2610.15792v1

## Reproduction

    python r155_reflection/replay.py

This recomputes all spectra, checks all 226 partitions, and reruns the original positive and negative controls with the reflection refinement active. The compact portable output is `r155_reflection/receipt.json`; exact input spectra and partitions are stored once per normalized profile in `partitions.json`. The source data and inherited Scott implementation retain their upstream bytes; the receipt binds their hashes and the added scripts.

The source datum is the inherited positive-ribbon candidate, not independently reconstructed here. The argument that every categorification of R6_4_155 has the specified positive Galois representative and center candidate remains an upstream prerequisite.

Current primary literature still lists the ring R′(4) as unresolved: Meng–Yu, arXiv:2608.06064v1, Theorem 1.1 and Section 5. The public arXiv record checked on 16 October 2026 lists only version 1.
https://arxiv.org/abs/2608.06064

No model or general, pivotal, spherical, pseudo-unitary, or unitary exclusion was found.

## Coverage check for the expanded involution-module method

The new rank-seven anti-invariant module analysis extends an implementation
previously restricted to at most two fixed labels. This does not expose a
missed original rank-six branch. In the source ordering for R6_4_155, the
three nontrivial invertibles have labels 3, 4 and 5. Their fixed-label sets
are respectively `{1,2}`, the empty set, and the empty set. The existing
rank-six method already treats the only eligible involution, `h=3`, and
the frontier chapter explicitly uses its `1+h` module action and
stabilizer-rotation constraints. The adjacent `involution_coverage.json`
records the exact permutations and source hashes for both rank-six
residuals. Neither has an involution with three or more fixed labels.

This coverage statement concerns the original source rings. The expanded
test was also applied to the separate rank-26 candidate centralizer, as
recorded next.

## The centralizer's six-fixed-label module test passes

In the inherited rank-26 modular datum, the fermion has label 0 and fixes
labels `(4,7,20,21,24,25)`. A natural six-dimensional anti-invariant
representation passes the exact constraints. One generator, the action
of label 16, is

    [[ 0,-1, 0, 0,-1,-1],
     [ 0, 0, 0, 1,-1, 1],
     [ 1, 0, 0, 0,-1, 1],
     [ 0, 0,-1, 0,-1,-1],
     [ 1, 1, 1, 1, 0, 1],
     [ 1,-1,-1, 1,-1, 0]].

Its characteristic polynomial is `(x^2+9)(x^2+1)(x^2-1)`. The complete
26 anti-invariant matrices satisfy every fusion identity, the transpose
duality condition, and all fixed-block entry bounds and parities. The
fermion acts by minus the identity. Resolving each of the six fixed labels
into two module labels reconstructs a nonnegative integer based module
of rank 22. Its complete 676 fusion identities also hold exactly.

The portable data are in `r155_center_module/anti_module_witness.json`.
Run `python r155_center_module/verify_anti_module.py` for a standard-library
replay; `receipt.json` binds the source datum and both matrix collections.
This is a passing necessary condition. It constructs neither a module
category nor a categorification, and yields no exclusion. This route was
stopped after the explicit passing witness was verified.
