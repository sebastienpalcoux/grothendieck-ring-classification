# Focused review of the complete R1154 fixed-Gram calculation

The new height-six calculation correctly covers all 1,238 integral Gram
patterns surviving the preceding cubic and spectral filters. Eight patterns
have exact Farkas separators and 1,230 have exact nonnegative rational
primal solutions. This leaves the categorification problem open. The result
is survival of necessary equations, not a constructed center or category.
This is separate AI review, not human or formal proof-assistant review.

The previous complete rotation receipt leaves only low frames 30 and 31
with indicator tuple (0,0,-1,1,1,1,1); the distinguished-character modular
receipt excludes frame 30. Thus the new calculation uses the only previously
surviving low frame and indicator tuple. Those earlier full receipts remain
prerequisites of the complete statement. The new wrapper checks its unique
character assignment and explicitly matches the recomputed ordered high
restriction list to the saved integer-Gram domain.

All patterns have one common matrix A and a right side affine in seven
coordinates t. If B describes that affine right side and M gives proposed
affine primal weights on a fixed support C, it is enough to check

    (C M - B) (1,t_i) = 0,   M (1,t_i) >= 0

at every pattern i assigned to that family. The implementation does exactly
this. It does not require, or claim, feasibility on the entire ambient
affine span. There are 311 affine families covering 1,111 patterns and
119 individual exact primals. Four full-matrix integer rays cover the
eight rejected patterns. Case domains are checked for disjointness and
their union is compared exactly to the complete filtered index list.

The reviewer inspected the affine parametrization, all three verification
paths, and coverage accounting, and freshly replayed the final strengthened
verifier with Python optimization. It passed with 1,238 certified patterns
and zero unprocessed patterns. The earlier integer enumeration and filter
receipts are separately replayed by the existing noncommutative verifier;
this focused review does not claim a fresh independent rewrite of them.

The accepted general Galois-pseudo-unitarity gate makes the pseudo-unitary
constraints necessary for general complex existence after transport. The
rotation height is six, not a bound on possible categorical exponents.
