# Why the frozen R3895 norm slack is integral

The general rational norm inequality does not automatically have an integral
gap. Encoding an arbitrary rational gap with an unscaled integer slack can
therefore be too strong. Future generic inequalities should clear their
coefficient denominators before introducing an integer slack of coefficient
minus one.

For the two frozen R3895 systems, however, the original encoding is justified
by existing necessary congruences. No system or certificate regeneration is
needed.

The source multiplier is

`x=(0,1/2,1/2,0,1,1,0)`.

All low chord weights and the constant in the norm inequality are integers.
The quartic squared norm and the low product coefficients are actual fusion
multiplicities, hence integers in any categorification. It remains to show
that the total high-row contribution

`sum_Y g*(x.v_Y)`, where `g*(t)=max_{k>=0 integer}(tk-k^2)`,

is integral. Set `n=v_1+v_2+2v_4+2v_5`. Completing the square, or checking
the four residues of `n` modulo four, gives

`2 g*(n/2)=floor(n^2/8)`.

Thus only the parity of the sum of these integers matters. There are 26
half-integral orbit costs in each frozen system, so orbitwise integrality
alone would not justify the slack.

Let the system rows have their stored zero-based indices. The sum modulo
two of rows

`346,347,359,362,373,382,385,390`

has, on every phase variable, coefficient

`2 * multiplicity_unit * sum_{v in orbit} g*(x.v) modulo 2`.

It has coefficient zero on every auxiliary variable and target zero modulo
two. These eight rows are necessary all-word congruences. Their moduli are
respectively `6400,320,80,80,8,8,8,8`; they do not use the norm-cut row 345.
Consequently the total high-row cost is an integer. The full norm gap is
therefore a nonnegative integer in every actual categorification, exactly
as required by the frozen slack encoding.

`verify_r3895_norm_parity.py` independently recomputes the orbit costs, binds
the canonical source tensor, reconstructs the eight all-word equations and
checks the parity identity on all 3,925 columns and the target. It imports
no producer norm, lattice or optimizer helper. Normal and optimized Python
replays pass for both label representatives, with receipts
`r3895_norm_parity_normal.json` and `r3895_norm_parity_optimized.json`.

This validates an auxiliary necessary inequality. It is not a general
categorification exclusion of R3895. R5039's corresponding orbit costs are
already integral and its complete exclusion chain is unaffected.
