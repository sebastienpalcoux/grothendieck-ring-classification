# Pattern 40: bounded exact reduction to one phase and one matching

This note records the phase/matching reduction used by the subsequent signed-Galois obstruction in REPORT.md. The latter excludes pattern40, not R928 as a whole; no category is constructed.

In the chosen orientation xi=exp(pi*i/4), all phase exponents below are taken modulo1728, except the initial variable t and B triple in the enumeration, which are modulo144.

## Nine-A phase equation

The full square-Galois orbit condition implies that each A9 multiset is a union of complete square orbits. Every allowed nonsingleton orbit has sum zero. The singleton orbit roots form mu24. To solve the exact equation

    sum_A theta_A = -1 - 2t - 2sqrt(3)*xi,

the checker enumerates singleton multisets of mass at most9 by a meet-in-the-middle split of masses at most4 and5, using exact coefficients modulo Phi24=x8-x4+1. It then fills the remaining mass with complete zero-sum nonsingleton orbits.

For t=60,84,96 modulo144, this produces respectively32,32,120 complete A multisets. Together with the four allowed (t,B) combinations and312 H quartets, the known three-W Vafa equations leave174 phase allocations. The exact modular indicator of W gives

    174 ->12 by nu2(W)=1 ->2 by nu4(W) in Z[i].

The nu3,nu6,nu8,nu9 checks do not further reduce these two. Their common phases are

    t=1152; W=432;
    A=(288,288,864,936,936,936,936,1512,1512);
    B=(720,720,1296).

The H quartet is either(162,594,1026,1458) or(378,810,1242,1674).
Their W indicators are respectively nu4(W)=2 or40, while both have nu3(W)=5, nu6(W)=4, nu8(W)=14-3sqrt(2), and nu9(W)=17.

## Residual matching

The integral projection lemma in REPORT.md gives three disjoint equal-dimension pairs. Here there are5427 such matchings: nine A, three B, four H, with all other dimension fibers singleton.

For each of the two phase assignments, the exact three-C Vafa equations and modular indicators yield

    5427 ->1347 by three-C Vafa ->85 by nu2(C)=1 ->9 by nu3(C)=5.

All nine pass the nu4(C) test, whose value is1 in the H162 branch and39 in the H378 branch. Every surviving matching includes the two H antipodal pairs. Its third pair has equal twists and is one of: the A288 pair, the A1512 pair, any of the six pairs among the four A936 objects, or the B720 pair.

The six-dimensional modular block proved in REPORT.md therefore applies without change. It requires a^4*lambda=i, where a is the first H twist and lambda is the outside-pair twist. H378 would require lambda at phase648, which is unavailable. H162 requires lambda at phase1512, selecting its unique A pair.

Consequently pattern40 has exactly one remaining phase multiset and matching, up to permutations of identical fibers:

    low twists1; W=i; E=F=zeta3^2;
    A=(zeta6,zeta6,-1,zeta24^13,zeta24^13,zeta24^13,zeta24^13,zeta8^7,zeta8^7);
    B=(zeta12^5,zeta12^5,-i);
    H=zeta32^3*(1,i,-1,-i).

The three residual pairs are the two H antipodal pairs and the A pair at zeta8^7. Complex conjugation supplies the opposite semion orientation.

## Replay

Run from the checks directory, in this order:

    python r928/pattern40_singletons.py
    python r928/pattern40_vafa.py
    python r928/pattern40_indicators.py
    python r928/pattern40_matching.py

The scripts use exact arithmetic, their adjacent JSON outputs, cyclotomic_arithmetic.py, vafa_probe.json (for the separately regenerated312 H quartets), prior/spectral_reduction.json, and SymPy. The last matching check ran in about2.3seconds here; none is an associator or unbounded search. The assumptions feeding the inherited spectral data must be audited separately; matching and phase checks do not establish them.
