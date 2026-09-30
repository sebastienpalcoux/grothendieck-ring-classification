# Complete finite modular-representation spectrum cone

The proved twist exponent bound for R6_8_1660 makes its canonical center modular representation a representation of `SL2(Z/48)`. By the Chinese remainder theorem this group is the product of `SL2(Z/16)` and `SL2(Z/3)`.

The exact enumeration gives:

| Group | Order | Exponent | Irreducible characters |
|---|---:|---:|---:|
| SL2(Z/16) | 3072 | 48 | 76 |
| SL2(Z/3) | 24 | 12 | 7 |
| SL2(Z/48) | 73728 | 48 | 532 |

The complete irreducible spectra of the upper-unipotent generator `T`, together with the sign of the central element `-I`, yield 504 distinct signed spectrum types. Merging identical types preserves the nonnegative integral spectrum cone.

`finite_spectra48.py` enumerates the matrix groups, conjugacy classes, and class algebras over the integers. Exact simultaneous diagonalization over Q(zeta48) finds the character rows. Verification reconstructs the groups and class algebras, checks every class-algebra character identity, character orthogonality, positive integral degrees and their square sum, the central signs, and all T eigenvalue multiplicities by exact Fourier inversion. The number of distinct character rows equals the number of conjugacy classes, so the list is exhaustive. No numerical eigenvalue recovery or numerical optimizer is used.

`representation_cone.py` forms all tensor-product spectra. Its `append_cone` function adjoins nonnegative integral multiplicity variables and 48 spectrum equations to an actual-root system. It also imposes 48 signed-trace inequalities, encoded with nonnegative slack: because `S^2` acts by duality, its trace within each T eigenspace is the number of self-dual simples there. Any supplied lower bound for known self-dual low simples must be proved by the caller. For this self-dual source ring, the real character labels prove all six low simples are self-dual.

`ising_complement.py` checks all 4740 labelled restriction profiles: every occupied column projects to zero or a single Ising-center simple. The full-center modular intertwiner theorem and positive individual target masses then force nine disjoint nonzero rows, giving an embedded Ising-center representation. Its row Gram matrix is twice the identity. `append_complement` subtracts this known nine-dimensional T spectrum before imposing the finite-group cone. The complement's signed-trace bounds are **3 at 1, −2 at −1, −1 at the four Ising roots, and zero elsewhere**. A complement need not have permutation duality; imposing nonnegative signed trace there would be invalid.

Replay from the package root:

```sh
OPENBLAS_NUM_THREADS=1 python -O research/round5/m8_modrep/finite_spectra48.py --modulus 16 --verify
OPENBLAS_NUM_THREADS=1 python -O research/round5/m8_modrep/finite_spectra48.py --modulus 3 --verify
python -O research/round5/m8_modrep/representation_cone.py --verify
python -O research/round5/m8_modrep/ising_control.py --verify
python -O research/round5/m8_modrep/ising_complement.py --verify
```

The source-bound receipts are `sl2_16_replay.json`, `sl2_3_replay.json`, `representation_cone_replay.json`, and `ising_control_replay.json`. The last control derives the nine-object center twist spectrum from each Ising indicator choice and verifies an explicit nonnegative integral cone decomposition. The first replay takes approximately 50 seconds in the development environment. These files certify the complete finite-group spectrum cone. Ring-specific exclusions require a separate exact system and separating certificate; cone membership itself does not establish categorification.

`ising_projection_rank_replay.json` binds the complete profile support check proving the forced subrepresentation. Bounded applications of the full-spectrum cone and forced-complement cone supplied no further exact exclusions. The final proven profile frontier remains 168 / 798 / 798. The coupled nonnegative integral representation-completion problem is unresolved; numerical solver outcomes are not additional certificates.
