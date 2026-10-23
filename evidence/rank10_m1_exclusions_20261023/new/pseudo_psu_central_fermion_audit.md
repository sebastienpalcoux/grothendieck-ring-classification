# Independent audit: the pseudo-PSU(2)_6 ring cannot have a central fermion

23 October 2026.

## Conclusion and precise dependency

Let C be any complex fusion category with simples 1,f,x,y and rules

\[
f^2=1,\quad fx=xf=y,\quad x^*=y,\quad
x^2=y^2=f+x+y,\quad xy=1+x+y.
\]

Then f cannot admit a central lift generating sVec. This follows from the **finite super-pentagon exclusion of the odd-evaluation rank-two super fusion rule (1,1)** reported in Chang–Chen–Xu, Section 3, rather than from their conjectural classification at arbitrary multiplicity. The reduction to that exact finite case uses only the standard construction of a superfusion category from a fusion category over sVec; it requires neither a braiding on C nor a unitary structure on C.

The cited finite nonexistence result is a published computer algebra result. This audit checks its exact scope and the categorical reduction. It does not independently reproduce their Gröbner basis calculation.

## Exact quotient calculation

Assume (f,beta) generates sVec in Z(C). The associated superfusion category has

\[
\operatorname{Hom}_{\widehat C}(a,b)_{\bar0}
=\operatorname{Hom}_C(a,b),\qquad
\operatorname{Hom}_{\widehat C}(a,b)_{\bar1}
=\operatorname{Hom}_C(a,f\otimes b).
\]

See Robert Usher, *Fermionic 6j-symbols in superfusion categories*, Journal of Algebra **503** (2018), 453–473, DOI [10.1016/j.jalgebra.2018.02.015](https://doi.org/10.1016/j.jalgebra.2018.02.015), Section 4.2, construction following Lemma 4.6 in the published version. The earlier [arXiv:1606.03466v1](https://arxiv.org/pdf/1606.03466) gives the same construction explicitly as Definition 4.9 on printed pages 11–13. Its hypotheses are a fusion category over sVect, over an algebraically closed field of characteristic zero; pivotal, spherical and unitary hypotheses are absent.

The f-action has two free orbits {1,f} and {x,y}. Choose representatives I=1 and W=x. Both are m-type: their odd endomorphism spaces vanish. The graded fusion spaces are

| Space | Even dimension | Odd dimension |
|---|---:|---:|
| Hom(W tensor W,I) | 0 | 1 |
| Hom(W tensor W,W) | 1 | 1 |
| Hom(I tensor W,W) | 1 | 0 |
| Hom(W tensor I,W) | 1 | 0 |
| End(I), End(W) | 1 | 0 |

Indeed, the first row is Hom_C(x^2,1)=0 and Hom_C(x^2,f)=C; the second row is Hom_C(x^2,x)=C and Hom_C(x^2,fx=y)=C. Thus the quotient rule is exactly

\[
W^2=1_f I+(1_b+1_f)W.
\]

In the notation of Chang–Chen–Xu this is \(\widehat{\mathcal C}^{(1,1)}_m\), their equation (3.2), not the even-evaluation family \(\mathcal C^{(1,1)}_m\). The latter exists and comes from ordinary PSU(2)_6; it must not be confused with the excluded former.

## Precise primary source and scope

Chi-Ming Chang, Jin Chen, Fengjun Xu, *Topological defect lines in two dimensional fermionic CFTs*, **SciPost Physics 15**, 216 (2023), DOI [10.21468/SciPostPhys.15.5.216](https://doi.org/10.21468/SciPostPhys.15.5.216).

Primary PDF locations:

- [Published PDF](https://scipost.org/SciPostPhys.15.5.216/pdf).
- [Author preprint, arXiv:2208.02757v4](https://arxiv.org/pdf/2208.02757v4).

The accessible arXiv v4 has Section 3 on printed page 25; published pagination places it on printed page 20. Equation (3.2) in the preprint, **equation (73) in the published paper**, defines the odd-evaluation family. The next paragraph states that the super-pentagon identity was solved, via Mathematica polynomial generation and Magma Gröbner bases, for an explicit finite list of pairs containing (1,1). The resulting list includes only \(\widehat{\mathcal C}^{(0,0)}_m\) among the odd-evaluation families. Consequently the particular \(\widehat{\mathcal C}^{(1,1)}_m\) rule has no solutions. The published primary PDF's indexed text independently confirms the family definitions, the finite list containing (1,1), and the locality discussion in Section 3.2.4.

The following sentence conjectures that the displayed examples exhaust *all* rank-two superfusion categories. That broader conjecture is unnecessary here, since the required pair (1,1) lies in the explicitly solved finite list.

## Audit for hidden physical or unitary assumptions

1. Section 3 describes the actual exclusion as solving the super-pentagon identity, not as filtering solutions by conformal spin selection, unitarity, or a CFT realization.
2. Section 3.1 permits arbitrary nonzero complex changes of bases. The solutions displayed elsewhere include negative loop dimensions; Table 2 separately records both signs. No positivity or unitarity restriction is imposed on this algebraic calculation.
3. Most decisively, Section 3.2.4 explicitly retains the odd-evaluation (0,0) solutions as consistent super fusion categories while explaining that they violate the physical locality condition discussed earlier. Thus those physical locality/rotation assumptions are not silently used to reject all odd-evaluation rules. The odd (1,1) exclusion is an algebraic super-pentagon assertion.
4. The standard sVec-to-superfusion construction above provides exactly such algebraic super-pentagon data. It does not require transferring a particular spherical or superpivotal convention to the quotient. Therefore the sign of the original categorical dimension of f is irrelevant to this use of Section 3.

This establishes the central-fermion obstruction for all complex categorifications of the indicated rank-four ring, conditional only on the cited finite published super-pentagon result in the ordinary sense of relying on a literature theorem/computation.

## Why the 2026 census is not the needed completeness source

Vercleyen–Slingerland, *On Low-Rank Multiplicity-Free Complex Fusion Categories*, DOI [10.1007/s00220-026-05705-2](https://doi.org/10.1007/s00220-026-05705-2), explicitly describes its data as a census, not a proved classification. Its discussion of correctness, completeness and uniqueness says no formal proof of the three properties is known, and documents a missing rank-seven family found during review. Its pseudo-PSU(2)_6 entries and the later center computations are valuable examples, but should not be used alone to infer that every complex categorification has semionic central f. The finite rank-two obstruction above avoids that completeness issue.
