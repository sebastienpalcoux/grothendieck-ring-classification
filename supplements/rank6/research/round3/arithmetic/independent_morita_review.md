# Independent review of the integer Morita refinement

Reviewed `software/round3_integral_morita.py`, the underlying
`software/full_morita_gram.py` construction, and
`research/round3/higher/integral_morita_proof.md`.

The new integrality step is valid. Each variable counts simple objects of
the dual fusion category with the same enumerated right-action matrix, so
is a nonnegative integer. The finite candidate construction includes all
matrices allowed by the Gram image, diagonal and entrywise bounds, left/right
commutation, and first-column types. The class-count equations retain
multiplicities. Removing the distinguished unit once is correct; allowing
another simple object to have an identical right-action matrix weakens the
system and does not remove a possible category.

Deduplication uses the complete augmented row (coefficients and right-hand
side), preserving exactly the solution set. A verified integral row vector
with y A=0 modulo q and y b nonzero modulo q contradicts every integral
solution. Primality of q is not needed for verification. The certificate
generator uses prime q=2, where its Gaussian elimination is valid.

The verifier reconstructs the exhaustive involution-module branches,
reconstructs each complete Gram system, and applies the modular witness to
that system. The surviving branches are connected to the existing higher
stabilizer conditional through reconstructed object lists and indices.
No new pivotality or positivity-of-categorical-dimension assumption is
introduced by the integer refinement. General scope depends on the explicit
unrestricted signed reduction checked by `verify_general`, which is present.

This is a mathematical and source review; the normal/optimized execution
reports for the full combined certificates are maintained by the higher
continuation audit.
