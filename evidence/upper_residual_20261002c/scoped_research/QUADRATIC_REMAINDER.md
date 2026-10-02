# Exact reduction for R7_4_1212 and R7_4_1213

This is a necessary-conditions reduction, **not a general exclusion**. The two rings remain unresolved for arbitrary complex fusion categories. Their pivotal exclusions remain valid.

Both have pointed groupC2 fixing all five noninvertibles, all basis objects self-dual, integer formal-codegree lcm180, and quadratic formal codegrees450±198sqrt(5). Their Casimir traces are1036 and1020. The relative-trace proof gives a totally real dimension-character fieldK containingF=Q(sqrt(5)), with Tr_K/Q(delta) bounded by these traces. Choose the lift of the nontrivial invertible with dimension+1. Its signed action on every noninvertible is then+1. Thus the signed ring also has the zero-on-noninvertibles character(1,-1,0,0,0,0,0), whose codegree is2. The actual nonzero dimension character has degree e≤6 and e is even.

The totally positive algebraic integer beta=delta/180 has Tr_K/Q(beta)≥e. This excludes e=6 since1080+2 exceeds both trace bounds. It is essential not to assume K=Q(delta).

## Degree four is impossible

If e=4, write r=[Q(beta):Q], which divides4.

- If r=4, its trace is at mostfloor(1034/180)=5. No irreducible totally positive quartic has trace at most5. An exact finite check suffices: its elementary symmetric coefficients are positive integers; Maclaurin gives e2≤floor(3a²/8), e3≤floor(a³/16), e4≤floor(a⁴/256) for tracea≤5. Irreducibility and exact Sturm root counts exclude every polynomial in this complete box.
- If r=2, its trace is at mostfloor(1034/360)=2. A totally positive irreducible quadratic has trace at least3: trace2 would force norm1 and both roots1.
- Therefore r=1 and delta is a positive integer divisible by180. Since4delta+2≤1036, necessarily delta=180.

There are then four Casimir eigenvalues180, one eigenvalue2, and two remaining positive rootsu,v. The formal-codegree reciprocal identity gives

    4/180+1/2+1/u+1/v=1,

so90(u+v)=43uv. Their residual quadratic has integral coefficients, hence it is

    z²-43kz+90k

with positive integerk≤7, from the Casimir trace bound. Each of these seven polynomials is irreducible overQ. Its roots fail the d-number criterion because(43k)²/(90k)=1849k/90 is not an integer. But twice each signed codegree is a formal codegree of the sphericalization and must be a d-number; rational scaling does not change this property. This contradiction excludes the entire degree-four branch.

## The precise remaining dimension branch

Consequently e=2 and K=F. Write the five noninvertible dimensions as d_i=(a_i+b_i sqrt(5))/2, with a_i,b_i integers of the same parity. Orthogonality of the two signed dimension characters gives

    sum a_i²-5 sum b_i²=-8.

Putting B=sum b_i² and A=sum a_i b_i then yields

    delta=(5B+A sqrt(5))/2.

Integrality of delta/180 implies B=36a and A=180b, with a,b integers of the same parity. Total positivity and the trace bound give1≤a≤5 and |b|sqrt(5)<a. The complete surviving global-dimension list is therefore

    180,
    270+90sqrt(5), 270-90sqrt(5),
    360,
    450+90sqrt(5), 450-90sqrt(5).

These pass the elementary global-divisibility and d-number tests. An exclusion must still rule out dimension vectors and associative signed tensors realizing one of these six values. The bounded oriented and propagation searches in this directory all timed out and establish no negative result. `verify_quadratic_remainder.py` replays the source invariants, the complete quartic polynomial box, the seven residual d-number failures, and this finite global-dimension list.
