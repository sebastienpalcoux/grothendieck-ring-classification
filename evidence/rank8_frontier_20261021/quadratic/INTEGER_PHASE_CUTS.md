# Global phase-separation cuts on integer central restrictions

Fix one allowed indicator branch and the complete source-bound phase
operator C. Let x_l be the integer selected low restrictions and n_o the
integer counts of complete high duality orbits. The high phase variables
w_(o,t) are nonnegative rationals with sum_t w_(o,t)=n_o. Auxiliary
rotation variables are also nonnegative. The fixed central unit is
already incorporated into the original right-hand side b.

Take any integer covector y on the original phase rows with nonnegative
pairing on every auxiliary rotation column. Define

    a_l = y·C_l,       m_o = min_t y·C_(o,t).

Every phase-compatible integer restriction pattern necessarily obeys

    sum_l a_l x_l + sum_o m_o n_o <= y·b.

Indeed, apply y to the complete phase equation and lower-bound each
high fiber by its minimum times its total mass. The rotation contribution
is nonnegative. The minima must include every complete trace type for
every original high orbit, even an orbit absent from the particular
integer pattern that led to y. Lows retain their full character labels.
Different indicator branches have different right-hand sides and must
be treated separately.

A Farkas separator for a fixed pattern supplies such a y after discarding
the appended mass-row coordinates. The code verifies every original
auxiliary sign and high-fiber minimum, and separately checks that the
resulting inequality strictly rejects that originating integer pattern.
The inequality becomes an integer equation by adding a nonnegative slack.
Its finite upper bound is the right-hand side minus the minimum of the
left side over the existing finite variable box.

The exact adapter retains an actual Fib tensor Vec(C4) integer center
under two signed STS row projections. Each new slack and all original
equations are checked; normal and assertion-disabled controls pass.
R65 has one indicator branch. Its finite campaign adds at most ten global
cuts, exactly verifies each proposed integer pattern and each complete
phase test, and distinguishes a checked obstruction or compatible witness
from an inconclusive numerical search. A rejected integer pattern alone
is never called an exclusion of the ring.
