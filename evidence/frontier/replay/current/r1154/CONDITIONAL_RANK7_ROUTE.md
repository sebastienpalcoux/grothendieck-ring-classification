# R8_3_1154: a six-vertex module and a conditional rank-seven Morita route

29 October 2026. **R8_3_1154 remains unresolved.** This note does not construct
an algebra, a module category, or a categorification. The conditional rank-seven
conclusion below uses the full-center/module-character identification in
Ostrik, arXiv:1309.4822, Remark 2.19. That premise received a separate
agent review; this is not independent human verification.

Put a=6+3sqrt(5), b=a+1, delta=(a-1)/2=(5+3sqrt(5))/2 and
D=540+240sqrt(5). Use the published basis 1,X1,X2,g,X4,X5,X6,X7.
The positive representative is supplied by the separately established
sphericalization/Galois gate. Its pointed C2 associator is nontrivial.

## 1. A small algebra search reduced theoretically

No connected separable algebra can contain g: its simple regular right module
would then be fixed by g, giving a rank-one module for Vec(C2,omega), contrary
to the nontriviality of omega. More generally g acts freely on the simple
objects of every module category. Thus the smallest possible nontrivial
connected algebra has dimension b, and its object is 1+X4 or 1+X5.
This is only a lower bound, not an existence statement.

Suppose A=1+X4 is a connected separable algebra, and let m be its regular
module. Its free-induction Gram matrix is right multiplication by A. The
rows m and gm are respectively

    (1,0,0,0,1,0,0,0), (0,0,0,1,0,1,0,0).

After subtracting their rank-one Gram contributions, the residual images of
X4 and X5 agree and have squared norm two. Write that common image p+q.
The residual images of X1 and X6 agree, have squared norm three, and inner
product two with p+q; hence each is p+q+r. Likewise X2 and X7 give p+q+s.
Their inner product two forces r and s to differ. All six vertices are
distinct. Every simple module occurs in a free module, so there are exactly
six. Up to permutation the complete induction matrix is

    B = [[1,0,0,0,1,0,0,0],
         [0,0,0,1,0,1,0,0],
         [0,1,1,0,1,1,1,1],
         [0,1,1,0,1,1,1,1],
         [0,1,0,0,0,0,1,0],
         [0,0,1,0,0,0,0,1]].

The relative module dimensions are (1,1,delta,delta,2,2), and g exchanges
the three pairs (m,gm), (p,q), and (r,s).

The matrix B has rank five. If L_i is the source left multiplication
matrix (output-row convention), every module matrix is

    M_i = B L_i B^+ + chi(X_i) zz^t/2,
    z=(0,0,1,-1,0,0)^t.

The missing line must carry a source character with chi(g)=-1. There are
exactly two:

    chi_4  = (1,0,0,-1,1,-1,0,0),
    chi_20 = (1,-2,-2,-1,-1,1,2,2).

Both choices give nonnegative integral module matrices satisfying every
fusion product and duality transpose. Thus neither branch is excluded at
the based-module level. Their module associators remain unconstructed.

## 2. The chi_4 branch has a sharply constrained dual

The module character in this branch has multiplicities 1,1,2,0,1 on the
source irreducible representations FP, its Galois conjugate, chi_4,
chi_20, and the two-dimensional representation, respectively.

Let A0,...,A4 be the published distinguished central simples. The full-center
character identity identifies those multiplicities with their multiplicities
in the Lagrangian algebra of the module category. For an explicit proof,
apply Ostrik's Remark 2.19 to the linking multifusion category of C and its
Morita dual: its cross-corner Grothendieck space is
Hom(L_C,L_M), and a central simple A_E contributes V_E tensor W_E*, where
dim(W_E) is precisely its multiplicity in L_M. They already account for
the full dimension:

    L = A0+A1+2A2+A4,
    dim(L) = 1+(161+72sqrt(5))+2(135+60sqrt(5))
             +(108+48sqrt(5)) = D.

Consequently L has no further central summands. Its squared multiplicity
sum is seven, so the dual fusion category has rank seven. Its action on the
six-vertex module identifies its complex Grothendieck algebra with the full
seven-dimensional commutant. This last assertion uses the same annular
character identification: no central block of the dual lies outside the
support of the original induction of the unit.

As an independent necessary check, the low S block is

    [[3/20-sqrt(5)/15, 3/20+sqrt(5)/15, 1/4, 1/20, 1/5],
     [3/20+sqrt(5)/15, 3/20-sqrt(5)/15, 1/4, 1/20, 1/5],
     [1/4,1/4,3/4,-1/4,0],
     [1/20,1/20,-1/4,7/20,2/5],
     [1/5,1/5,0,2/5,3/5]].

The complete known low columns send (1,1,2,0,1) to itself with zero high
tail in every retained center pattern. This S-invariance alone would not
prove the existence of the Lagrangian algebra.

## 3. The commutant determines one based ring

Every commuting integral nonnegative matrix has the form

    [[t, r-t, b, h-b, q, q],
     [r-t, t, h-b, b, q, q],
     [c, h-c, u, 5h+4q+r-u, h, h],
     [h-c, c, 5h+4q+r-u, u, h, h],
     [q,q,h,h,q+r,2q],
     [q,q,h,h,2q,q+r]],

where h,q,r,t,b,c,u are integers, h,q,r>=0, 0<=t<=r,
0<=b,c<=h, and 0<=u<=5h+4q+r. Its FP eigenvalue is

    delta*h+4q+r.

The coefficient-of-unit trace on the proposed dual algebra is

    tau(K)=(t+u-3h)/2.

Indeed its simple blocks have formal codegrees D,D',4,5; the trace weights
are the reciprocals of these codegrees. For a nonunit simple, u=3h-t.
The squared norm tau(KK^t) then is

    b^2-bh+c^2-ch+h^2-4hq-hr-ht+9q^2+4qr+4qt+r^2+2t^2.

It must equal one. The dimension bound d(K)^2<=D gives h<=5,q<=8,r<=32:
D<1077<33^2 and delta>29/5. This is a finite small domain, without any
associator search. Exact integer enumeration leaves twelve possible nonunit
matrices. Only two six-element sets are pairwise orthonormal. One has
half-integral, sometimes negative multiplication coefficients; the other
has nonnegative integral multiplication throughout.

Thus this branch forces the exact tensor in `rank7_dual_1.json`, with simple
dimensions

    (1,delta,delta,delta+1,delta+1,2delta+1,4delta+4)

and duality (0,1,2,4,3,5,6). Its maximum multiplicity is 19. It is a simple
noncommutative based fusion ring: every nonunit basis element generates it.
This is a necessary alternative ring, not a constructed category.

## 4. Further indicator restrictions on this branch

The Morita-invariant total second indicator of the source is 26+12sqrt(5),
or 8delta+6. Since the dual pair has zero second indicator, coefficient
comparison in

    1+delta(e1+e2)+(2delta+1)e5+(4delta+4)e6 = 8delta+6

forces e1=e2=e5=e6=1. Thus the candidate has no quaternionic selfdual simple.

The source total third indicator is 81+36sqrt(5)=21+24delta. Let t_i be
the candidate's third indicators, with t3=t4 by pivotal duality. The cubic
vacuum dimensions are (1,1,1,1,1,2,19). Comparing coefficients gives

    t1+t2+t5=4,        2t3+t5+4t6=20.

The triangle inequality saturates the first equation, forcing t1=t2=1 and
t5=2. Then t3+2t6=9. Since t3 is a cube root of unity and t6 belongs to
Z[zeta_3], reduction modulo 2 forces t3=1, hence t6=4. Therefore

    nu_3=(1,1,1,1,1,2,4).

These are consistent necessary spectra. For the last simple the cubic
rotation eigenvalue multiplicities are (9,5,5). No pentagon contradiction
follows from these identities alone.

The complete zero-spectrum and one-spectrum tests of Liu--Palcoux--Ren--
Vercleyen, arXiv:2203.06522v5, Theorems 6.7 and 6.8, were also applied to
this tensor. Neither supplies a witness. The short native scan examines
858,857 configurations satisfying the six required nonzero faces; it also
rechecks the original R1154 tensor, with 293,728 eligible configurations
and no witness. This calculation takes less than a second and does not
search associators. `small_spectrum.cpp` supplies the scan.

## 5. What is and is not settled

Neither A=1+X4 nor A=1+X5 has been constructed. The chi_20 based-module
branch also survives; its full-center low contribution is A0+...+A4 and
leaves dimension D/5 to be filled by other central simples. Therefore the
rank-seven ring is not an unconditional Morita partner of R1154.

The new dimension-block bound of Schopieray, arXiv:2609.35287, was checked
at the source dimension. Here the dimensional grading is trivial and the
two inverse-dimension character sums are 3/10 and -2sqrt(5)/15. Their
squares are 9/100<=1 and 4/45<=1/5, respectively. The bound gives no
contradiction. The algebra and matrix work above gives no general exclusion
and no new model of R1154.

Primary background: Ostrik, *Pivotal fusion categories of rank 3*,
arXiv:1309.4822, Theorem 2.13 and Remark 2.19 (distinguished central
simples, codegrees, and the linking multifusion character identity);
Deshpande, *On centers of bimodule categories and induction-restriction
functors*, arXiv:1611.04486 (annular character formalism); Schopieray,
*The dimension block of a spherical fusion category*, arXiv:2609.35287,
Theorem 5.1. The source's positive existence gate, central columns, and
indicator values are inherited, separately documented project premises.
