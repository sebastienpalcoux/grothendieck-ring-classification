# An anticommuting stabilizer obstruction to scalar pivotal rotation

This lemma is categorical and does not identify a hypothetical center with
any known center. It uses the actual action of the forced algebra 1+g.

Let C be a spherical fusion category over C. Let g be an invertible of
order two for which A=1+g is an algebra, and let Y be simple with gY=Y=Yg.
Choose an associative identification g²=1 and isomorphisms

    l: gY -> Y,     r: Yg -> Y.

They can be rescaled to make l(id_g⊗l)=id_Y and
r(r⊗id_g)=id_Y. The two maps gYg -> Y differ by a scalar kappa:

    r(l⊗id_g) = kappa l(id_g⊗r).

The scalar is a sign. More directly, transporting the right A-module
structure on gY by l gives

    r' = l(id_g⊗r)(l^(-1)⊗id_g) = kappa^(-1) r.

The two possible normalized right actions on Y are r and -r. Hence kappa
equals +1 if left multiplication by g fixes both A-module structures and
-1 if it exchanges them. In the anti-invariant module representation this
is exactly T_g[Y,Y].

Assume kappa=-1. Let q^(-1):1->g² be the inverse of the fixed associative
multiplication q:g²->1. Define the invertible endomorphism

    a = (r⊗l)(id_Y⊗q^(-1)⊗id_Y) : Y² -> Y².

On Y³ put P=a⊗id_Y and Q=id_Y⊗a. Both preserve
V=Hom(1,Y³), and their restrictions are invertible. They anticommute.
Indeed expand either composite by inserting the two copies of q^(-1)
before applying the endpoint isomorphisms. The common intermediate word is

    Y g g Y g g Y.

The maps on its outer two Y objects agree. The two maps on its middle
gYg are respectively r(l⊗id_g) and l(id_g⊗r); their ratio is -1. Thus
PQ=-QP, both on Y³ and on V. In particular dim(V) is even.

Let E be the pivotal cyclic rotation that moves the last Y to the first
position. Crucially, cyclic rotation

    Hom(1,B⊗Y) -> Hom(1,Y⊗B)

is natural in the whole object B. Taking B=Y² and the morphism a gives
the exact identity EP=QE on V. This does not involve a braiding, a
self-duality sign of Y, or a choice of bases for trivalent vertices.

If V is nonzero and E were scalar, this identity would give P=Q. But
then PQ=-QP would imply P²=0, contrary to invertibility. Therefore E is
not scalar. When dim(V)=2, E³=1 implies its two eigenvalues are distinct
cube roots of unity, so

    nu_3(Y) in {-1,-zeta_3,-zeta_3²}.

If 3 does not divide the Frobenius–Schur exponent N of C, the indicator
also lies in Q(zeta_N). Its intersection with Q(zeta_3) is Q. Therefore
nu_3(Y)=-1.

For R6_3_215, the two surviving exact full-Morita branches have T_g=-I on
the fixed simples b4,b5, and N_(b4 b4)^b4=N_(b5 b5)^b5=2. The preceding
lemma therefore gives nu_3(b4)=nu_3(b5)=-1 in every pseudo-unitary
categorification: the Cauchy theorem applied to the global-dimension norm
1088=2^6*17 excludes the prime 3 from the FS exponent. The previously
proved sphericalization/Galois reduction transfers a pseudo-unitary
nonexistence result to arbitrary complex categorifications.

Independent checks of the categorical argument were obtained from the
other two theory auditors. The separate exhaustive center certificate
`../../certificates/stabilizer_rotation_215.json` has now been independently
replayed under `python -O`: all 91 low frames, 50 character labellings and
200 exact separating vectors are covered. Together with the 1,480-table
unrestricted sphericalization reduction and 16 complete involution-module
branches, this proves general noncategorifiability of R6_3_215.

The stronger Clifford-algebra argument in the manuscript shows that for
arbitrary m=dim Hom(1,Y³), the third indicator has the form
-(a+b*zeta_3+c*zeta_3²), where a+b+c=m/2. The normalized real-field average
therefore belongs to [-m/2,m/4], without any exponent-coprimality hypothesis.
`clifford_rotation.py` checks the universal algebra identities exactly.
