# Independent audit of the Fibonacci character-parity exclusion

**Conclusion: PASS.** The argument excludes both `R8_2_190` and `R8_2_489` over the complex numbers. I checked the primary categorical input, independently recomputed the three characters and their formal codegrees from the original tensors, and verified the dimension and parity argument. This is a general exclusion, using the separately audited spherical/Galois-pseudo-unitarity reduction; it assumes no braiding or unitarity on a hypothetical category.

## 1. The character labels are canonical

I independently opened the primary PDF of Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822, and read Example 2.9, the definition immediately preceding Theorem 2.13, and Theorem 2.13 on printed pages 5--6.

For a character chi of K(C), the center character in that definition is exactly chi composed with the forgetful map F. Example 2.9 assigns it the unique simple Z_chi whose normalized S-row equals this character. Theorem 2.13 then gives dimension D/f_chi and multiplicity one in I(1). Therefore

    S(Z_chi,W) = (D/f_chi) chi(FW)

holds with the actual character label chi, not with a label chosen by matching dimensions. This remains valid when two formal codegrees coincide. Symmetry is the ordinary symmetry of the unnormalized modular S-matrix, with no complex conjugation on one side. The center is modular because the ambient category has been made spherical; the ambient category itself need not be braided.

## 2. Independent source and field calculation

I used a separate polynomial-reduction implementation, importing no code from the author's verifier. It uses the exact quotient

    Q(i)[phi,d]/(phi^2-phi-1, d^2-2 phi d-1)

and checks every ordered character-product equation directly on each original census tensor. The source hashes agree with the decision ledger:

- R190: `ef368ba29ddc183f215145eb6a50ead0655e91afff2d3e844f918c6d2a91d867`;
- R489: `23cae0639e4ce7e54428705a66098747319e26d5f29ad8dff05914a6d43caef1`.

In the independent order `(1,g,tau,g tau,x,gx,y,gy)`, the source maps are respectively `(0,7,5,6,1,2,3,4)` and `(0,1,7,2,3,6,4,5)`.

For chi_+, chi_- and psi, I obtain exactly

    f_+=f_-=4(phi+2),
    f_psi=2(3-phi)(1+z^2),  z=(phi-1)d-phi,
    D/f_+=D/f_-=1+phi d,
    D/f_psi=1+phi+2d+3phi d.

In particular, for R190 the formal codegree computation uses chi(b)chi(b*) and its actual nontrivial dual permutation. It does not replace this by a sum of ordinary squares. The two imaginary x-values therefore cause no sign error.

The claimed rational independence is also correct: adjoining d to Q(phi) adjoins sqrt(phi+2), and Norm(phi+2)=5 cannot be the norm of a square. Thus the four dimension coordinates are independent. All positive source dimensions and the global dimension were checked against the actual fusion products.

The independent arithmetic report is `fib_character_parity_independent.json`. I also replayed the author's portable verifier under optimized Python, with PASS, in `fib_character_parity_author_O.json`.

## 3. Restriction dimensions and the contradiction

Because [FZ_chi:1]=1 and restriction multiplicities are nonnegative integers, dimension 1+phi d forces each of FZ_+ and FZ_- to be exactly 1+y or 1+gy. The coefficient of g is zero: the combined dimension-one multiplicity is one and the unit already occupies it. Likewise there is no tau term and no x term.

Since psi(g)=1, psi takes the same value on these two possible restrictions. The two S-symmetry identities with B=Z_psi therefore have equal right sides and the same nonzero prefactor D/f_+ on their left sides. They imply chi_+(FB)=chi_-(FB), regardless of which restriction is assigned to either repeated-codegree character.

The independently checked dimension of FB forces x/gx multiplicity sum two and y/gy multiplicity sum three. Their character difference is exactly

    2 omega (Delta_x + phi Delta_y),

where omega is 1 for R489 and i for R190. Rational independence of 1 and phi forces both integer differences to vanish. But Delta_y cannot vanish when its two multiplicities sum to three. This is the required contradiction.

As an independent finite check of the last step, I enumerated the 24 dimension-compatible restrictions of B (two tau distributions, three x distributions, four y distributions). All have nonzero character difference, for both tensors. This enumeration is supplementary: the proof itself is the single odd-sum argument.

No issue was found with the general-complex scope, equal-codegree labels, forgetful dimensions, duality, or modular symmetry. Both exclusions are justified.
