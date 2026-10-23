# Rank-sixteen Morita-dual structure: independently checked deductions

Assume the rank-ten involution-module reduction of `quadratic_obstructions` has produced a fusion category D whose simple FP dimensions are

    1 (four objects), d=1+sqrt(2) (eight objects), d^2=3+2sqrt(2) (four objects).

This initial note records necessary dimension deductions. The later files `RELATIVE_FACTORIZATION.md` and `PSEUDO_BRANCH_EXCLUSION.md` complete the exclusion of the three pseudo-factor cases. `ORDINARY_DESCENT_AUDIT.md` independently reviews the ordinary-factor exclusion developed by the quadratic-models agent. The caveats below explain why the initial unitary-only route was insufficient and was replaced.

## Elementary dimension rules

Write dimensions in the integral basis (1,d), where d^2=1+2d.

For two simples X,Y of dimension d, XY has dimension d^2. Its possible dimension decompositions are exactly:

1. one invertible and two dimension-d simples, counted with multiplicity;
2. one dimension-d^2 simple.

Indeed if A,B,C count the respective types then A+C=1 and B+2C=2.

For X of dimension d and L of dimension d^2, XL has dimension d^3=2+5d. Frobenius reciprocity excludes invertible summands, since Hom(XL,g)=Hom(L,X* g)=0. Hence its dimension decomposition is one dimension-d simple plus two dimension-d^2 simples (counting multiplicity).

Each XX* contains the unit exactly once, so XX*=1+Y+Z, where Y,Z have dimension d. Thus X has trivial left invertible stabilizer. The four invertibles act freely on the eight small objects; there are two left orbits and two right orbits.

For two small X,Y, XY* contains an invertible if and only if X=gY for some invertible g. In that case the invertible is unique and the remaining summands have total dimension 2d. Otherwise XY* is a simple large object.

## Multiplicity-two branch is impossible categorically

Suppose XX*=1+2Y. Then Y=Y* and Frobenius reciprocity gives N_{YX}^X=2. The dimension rule gives YX=g+2X for an invertible g. Reciprocity gives X=Yg. Substituting and cancelling g gives Y^2=1+2Y. Hence {1,Y} spans the rank-two based ring K_2. Ostrik's classification of complex fusion categories of rank two excludes K_2. Consequently the two summands Y,Z in XX*=1+Y+Z must be distinct.

The same calculation shows that each such Y belongs to the left invertible orbit of X*: since YX contains X, the dimension rule forces an invertible g in YX, and then Y=gX*.

## Why the dimension profile does not force a tensor product

The known rank-ten model R10_1_21 is an essential control. Its Morita dual here can be described as B crossed C2, where B is the rank-eight central product obtained by condensing 1+(f,f) in PSU(2)_6 squared. This dual has a faithful C2 grading, whereas the literal tensor product PSU(2)_6 squared has trivial universal grading. Therefore the shared rank-sixteen profile cannot by itself identify the tensor product ring or category.

## Subfactor classification caveat

Liu--Morrison--Penneys, arXiv:1310.8566, Theorem 1, classifies 1-supertransitive subfactor planar algebras at index 3+2sqrt(2) (inside its stated interval [3+sqrt(5),6+1/5]). The outcomes are the PSU(2)_6 even part and two complex-conjugate pseudo-PSU(2)_6 even parts. For a **unitary** D, a small simple X gives a 1-supertransitive canonical subfactor because XX*=1+Y+Z has three distinct constituents. This theorem therefore strongly constrains the generated even part.

The original problem concerns arbitrary complex fusion categories. The established Galois reduction supplies pseudo-unitarity, not a unitary structure. Applying a subfactor/positive planar-algebra classification directly would leave a unitarizability gap. No such application is asserted here.

Primary references inspected:
- https://arxiv.org/abs/1310.8566 (Liu--Morrison--Penneys).
- https://arxiv.org/html/2406.13438v3 (Maeurer--Thiel, centers of all multiplicity-free categories through rank five; explicitly numerical/algebraic computations of centers rather than a general rank-sixteen classification).
