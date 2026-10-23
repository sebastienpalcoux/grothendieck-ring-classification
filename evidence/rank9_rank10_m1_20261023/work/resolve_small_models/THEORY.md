# Eight small integral unitary realizations

This directory resolves R9_1_47, R9_1_92, R9_1_98, R9_1_117 and
R10_1_61, R10_1_84, R10_1_109, R10_1_158. The certificate data contain
complete tensors and exact source-to-model basis permutations. The independent
verifiers in `work/audit_new_models` check the categorical diagrams as well as
all fusion coefficients. No floating-point acceptance criterion is used.

## Coherent pointed equivariantizations

Let A be a finite group and let a finite group K act on A. Write the
associator of Vec(A,omega) as exp(2 pi i w(a,b,c)/8). For each g in K,
the functor F_g permutes homogeneous degrees by g. Its forward tensorator
F_g(a) tensor F_g(b) -> F_g(ab) has exponent J_g(a,b). The compositor
F_g F_h -> F_gh has exponent mu(g,h,a). All entries in the certificates
are integers modulo 8. They satisfy normalization and the following equations:

- The usual group 3-cocycle equation for w.
- J_g(a,b)+J_g(ab,c)+w(a,b,c)
  =w(ga,gb,gc)+J_g(b,c)+J_g(a,bc).
- mu(g,h,ab)+J_g(ha,hb)+J_h(a,b)
  =J_gh(a,b)+mu(g,h,a)+mu(g,h,b).
- mu(g,h,ka)+mu(gh,k,a)=mu(h,k,a)+mu(g,hk,a).

These are precisely the pointed pentagon, monoidal-functor pentagon,
monoidality of the compositor, and action coherence. Therefore the data
specify an actual coherent unitary action, not merely a permutation of a ring.
Its equivariantization is a unitary fusion category.

An equivariant object has fibre maps U_g(a):V_a -> V_ga with
U_g(ha) U_h(a)=exp(2 pi i mu(g,h,a)/8) U_gh(a).
On a tensor product the fibre map has the additional factor
exp(-2 pi i J_g(a,b)/8). The minus sign is required by the forward
convention for J. Simples correspond to orbits and projective irreducible
representations of their stabilizers. The verifiers explicitly construct
these fibre maps, check every projective action identity, and recover the
fusion multiplicities by the invariant Hom-space character formula.

### R9_1_47 and R9_1_98

The certificate is `coherent_c2_models.json`; its other two entries are
previously known control models. For R47, A=C12 and the involution is a -> -a.
An associator representative has exponent
2 a floor((b+c)/12) modulo 8. The stored J and mu supply its coherent lift.
For R98, A=C3 x C2 x C2 and the involution is
(a,b,c) -> (-a,c,b). The stored associator is the nontrivial mixed C2 x C2
class with exponent 4 a_2 b_1 c_1, where subscripts refer to the two
binary coordinates. In both cases there are two fixed degrees and five
free orbits. Thus there are four invertibles and five dimension-2 simples.
Character arithmetic takes place exactly in Q(zeta_16).

Run `python work/audit_new_models/verify_c2.py`.

### R10_1_61, R10_1_84, R10_1_109, R10_1_158

Here A=F2^3 and K=S3 permutes the three coordinates. The certificate is
`coherent_s3_models.json`, which also includes four control rings.
The normalized associator is (-1) raised to a binary combination of
seven cocycles: a_i b_i c_i (three choices), a_j b_i c_i for i<j
(three choices), and a_0 b_1 c_2. The seven coefficients, all tensorators,
and all compositors are stored in each entry. The four S3-orbits have
sizes 1,3,3,1. Fixed orbits contribute dimensions 1,1,2 each; size-3
orbits contribute dimensions 3,3 each. Hence the profile is 1^4,2^2,3^4.
Stabilizer projective representations are explicitly trivialized over
48th roots of unity, and exact character arithmetic is reduced using
Phi_48(x)=x^16-x^8+1.

Run `python work/audit_new_models/verify_s3.py`.

## R9_1_92: homogeneous bimodules over a pointed category

Let V be the even-parity subgroup of F2^3 and G=V semidirect S3, which is
isomorphic to S4. Restrict the coherent action stored in the R10_1_133
control model to V. For x=(a,g), y=(b,h), z=(c,k), define

Omega(x,y,z)=w(a,gb,ghc)+J_g(b,hc)-mu(g,h,c) modulo 8.

This is the associator of the crossed product and is also checked directly
on every quadruple in G. Let s=(0,t), where t is a transposition, and
H={1,s}. Omega restricts identically to zero on H. Thus the subgroup
algebra 1+s is a separable unitary algebra in Vec(G,Omega).
Its bimodule category, with relative tensor product, is a unitary fusion
category of dimension 24. `s4_twisted_models.json` contains the complete
24-element group table, 24^3 associator exponents, and homogeneous simple
bimodules. The independent verifier constructs the left and right action
matrices, checks their associativity and mixed diagrams, forms balanced
tensor products, checks that both induced actions descend to the quotient,
and reconstructs all 729 multiplicities exactly. The resulting tensor is
R9_1_92 under the stored basis map.

Run `python work/audit_new_models/verify_s4.py`.

## R9_1_117: a triality extension of Rep(D8)

The existence input is Nikshych--Riepel, *Categorical Lagrangian Grassmannians
and Brauer--Picard groups of pointed fusion categories*,
[arXiv:1309.5026](https://arxiv.org/abs/1309.5026), Section 4 and Example 9.3.
They construct a **nontrivial C3 extension of Rep(D8)**; its dimension is 24,
and all noninvertible simples have dimension 2. Their definition of
nontrivial, immediately before Remark 4.2, means that a homogeneous component
is not equivalent to the regular category as a left module category.
The construction uses BrPic(Rep(D8))=S4 and the coprime extension theorem.
This is categorical existence, including associators and coherence.

Write C=D + M + N, with D=Rep(D8). A homogeneous component containing an
invertible object is equivalent to the regular D-module by tensoring with
that object. Since M and N are mutually inverse bimodule categories, either
both are regular as left modules or neither is. Choose the nontrivial
extension above. Both therefore contain no invertibles. Each has dimension
8, so each has exactly two simples, each of dimension 2.

We next identify the fusion ring without assuming multiplicity-freeness.
Write the neutral simples as G=V4 and m, with m^2=sum(G) and gm=mg=m.
The rank-two invertible D-module categories have transitive G action.
Here is a direct check using the classification of indecomposable Rep(D8)
module categories as projective representation categories Rep^psi(H):

- Rank two arises for H=C2, or for H=D8 with its nontrivial Schur class.
- For the central subgroup C2, the dual is C(D8,C2), which is pointed
  (four double cosets, two characters on each). It cannot be D, so this
  module is not an invertible D-bimodule.
- For either conjugacy class of reflection C2 subgroups, restricting the
  four linear characters of D8 gives both C2 characters; their action on
  the two simple modules is transitive.
- For the nontrivial Schur class of D8, use the central cover D16.
  Its two projective irreducibles are the 2-dimensional odd-weight
  representations (weights 1 and 3). A linear character sending the
  rotation to -1 interchanges them. The action is again transitive.

For completeness, the other subgroups cause no omitted rank-two case:
H=1 gives rank one; H=C4 has trivial Schur multiplier and rank four;
H=V4 gives rank four or rank one according to its Schur class; untwisted
D8 has rank five. Thus the list above is exhaustive. The same reasoning
applies to the right module structure.

Label M={X0,X1} and N={Y0,Y1}, with Xi*=Yi. There are nonzero characters
phi,psi:V4 -> C2 such that

  g Xi=X(i+phi(g)),  Xi g=X(i+psi(g)),
  g Yi=Y(i+psi(g)),  Yi g=Y(i+phi(g)).

The matrix for multiplication by m commutes with the transposition and
squares to 2I+2S. Nonnegative integrality therefore forces it to be I+S,
on either side and in either component. Frobenius reciprocity then forces

  Xi Yj = sum_{phi(g)=i+j} g + m,
  Yi Xj = sum_{psi(g)=i+j} g + m.

Only Xi Xj remains undetermined. Write
Xi Xj=a_ij Y0+(2-a_ij)Y1, with a_ij in {0,1,2}; duality determines
Yj Yi=a_ij X0+(2-a_ij)X1. These parameters exhaust every possibility,
including multiplicity two. `triality_ring.py` checks all 3*3*3^4=729
parameter choices by exact integer associativity. Exactly six pass,
one for each distinct pair of nonzero left/right kernel generators.
Every passing case has all a_ij=1 and is based-isomorphic to R9_1_117.
The full tensors and basis maps are in `triality_117_certificate.json`.
This finite argument links the categorical existence theorem to the exact
input tensor; it does not infer existence from a fusion ring alone.

Finally, the realized category is nilpotent: its adjoint category is D,
the next adjoint category is Vec(V4), and the next is Vec. It is therefore
unitarizable by Galindo--Hong--Rowell, *Generalized and quasi-localizations
of braid group representations*, [arXiv:1105.5048](https://arxiv.org/abs/1105.5048),
Theorem 5.20 (weakly group-theoretical categories are completely unitary).

Run `python work/resolve_small_models/triality_ring.py`.
