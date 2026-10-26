# A general-complex exclusion of R12_1_332

## Statement

R12_1_332 has no categorification by a fusion category over C. The proof uses
conjugation by an existing invertible, equivariantization, and formal-codegree
integrality. It does not classify Haagerup categories, assume unitarity, require
a trivial pointed associator, or assume a crossed-product splitting.

## 1. Reduction and the exact input

By the published Schopieray two-FP-value theorem (Lemma 3.1), any complex
categorification has a pseudo-unitary Galois conjugate. Work with that conjugate
and its canonical spherical structure. Its neutral fusion subcategory D has
simples

    1, alpha, alpha^2, rho, alpha rho, alpha^2 rho,

with alpha^3=1, rho alpha=alpha^-1 rho, and

    rho^2 = 1 + rho + alpha rho + alpha^2 rho,
    d = FPdim(rho) = (3+sqrt(13))/2.

An invertible b in the other graded component has b^2=1, and conjugation by b
inverts alpha and fixes rho. This is a statement about the full input tensor,
not an inferred presentation. One checked choice is alpha=input3, b=input5,
rho=input9; neutral labels are {0,3,4,9,10,11}. All tensor identities, closure,
and the complete forgetful-ring map are checked by verify_R332.py.

## 2. Why the conjugation action is coherent even for a twisted pointed part

Here is the useful general lemma. Let H be a subgroup of invertible isomorphism
classes in a fusion category C, and let D be a fusion subcategory preserved by
conjugation by H. Choose representatives u_h, normalized multiplication
isomorphisms m_{h,k}:u_h tensor u_k -> u_{hk}, and duals. Then conjugation gives
a genuine categorical H action on D, irrespective of the associator of C_pt.

For an invertible object u write A_u(X)=u tensor X tensor u*. Its tensorator
contracts the middle u* tensor u by evaluation. For an isomorphism f:u->v the
induced monoidal natural isomorphism is

    A_f(X)= f tensor id_X tensor (f^-1)*.

Associativity and rigidity provide canonical monoidal isomorphisms
A_u A_v -> A_{u tensor v}. Compose these with A_{m_{h,k}} to get
mu_{h,k}:A_{u_h} A_{u_k} -> A_{u_{hk}}.

There are two composite multiplication maps u_h tensor u_k tensor u_l -> u_hkl.
Their discrepancy, including the ambient associator, is a scalar omega(h,k,l),
because the target is simple. Under A this discrepancy acts as omega on the
left and omega^-1 on the right, hence as the identity. Thus the two composites
of mu agree. This proves the action pentagon. Unit coherence follows from the
normalized multiplication maps. The tensorator and naturality identities follow
from evaluation/coevaluation coherence. Equivalently, conjugation sends every
scalar automorphism of an invertible object to the identity transformation.

Apply this with H=<b>=C2. In particular the possible value omega(b,b,b)=-1
cancels in precisely this way. No associative algebra 1+b is asserted or used.
The action preserves the canonical pseudo-unitary pivotal structure (its
uniqueness), so E=D^C2 is pseudo-unitary with its induced positive spherical
structure.

## 3. All action-dependent fusion ambiguities are covered

For a C2 action, a fixed simple has two equivariant lifts: its stabilizer
2-cocycle is a coboundary over C. An orbit of length two gives one simple.
Consequently E has simples (1,g,U,X,Y,V), with forgetful images

    1, 1, alpha+alpha^2, rho, rho, alpha rho+alpha^2 rho.

Here g is the sign representation in the canonical central Rep(C2), Y=gX,
gU=U and gV=V. Their FP dimensions are (1,1,2,d,d,2d). These statements allow
arbitrary tensorators and action coherence; no equivariant structure has been
fixed in advance.

The images, duality, and associativity force

    g^2=1; U^2=1+g+U; UX=UY=V; UV=X+Y+V.

The only initial ambiguity is

    X^2=a+W+V,   a in {1,g}, W in {X,Y}.

If a=g, then X*=Y. Centrality of g gives Y^2=X^2, whereas duality would exchange
the unique X/Y summand of X^2. This is impossible. Hence a=1. Relabeling X,Y if
necessary gives W=X. It follows that both X and Y are selfdual and

    X^2=Y^2=1+X+V;
    XY=g+Y+V;
    XV=YV=U+X+Y+2V;
    V^2=1+g+U+2X+2Y+4V.

The ring is commutative: g is central, the products with U have the unique
forgetful images just described, Y=gX, and V=UX. These are all 36 products.
The full tensor is isomorphic to the project's R6_4_260, under permutation
(0,1,4,3,2,5). The exclusion below is independent of that earlier certificate.

## 4. An elementary exact norm contradiction

The positive global dimension of E is

    D = 1+1+4+d^2+d^2+(2d)^2 = 39+9sqrt(13).

The displayed fusion ring has a one-dimensional character

    chi(1,g,U,X,Y,V)=(1,-1,0,phi,-phi,0),
    phi=(1+sqrt(5))/2.

All objects are selfdual, so its formal codegree is

    f=sum_Z chi(Z)chi(Z*)=2+2phi^2=5+sqrt(5).

For any spherical fusion category, central induction produces a simple object
of categorical dimension D/f for this character (Ostrik, Theorem 2.13). Such a
dimension is an algebraic integer. But in Q(sqrt(13),sqrt(5)),

    Norm(D/f) = Norm_Q(sqrt13)(D)^2 / Norm_Q(sqrt5)(f)^2
              = 468^2/20^2 = 13689/25,

which is not an integer. This contradiction excludes E and therefore the
putative categorification of R12_1_332. The argument applies to every original
complex category through the initial Galois reduction.

## Sources and reproducibility

- A. Schopieray, *Categorification of integral group rings extended by one
  dimension*, published Lemma 3.1: https://doi.org/10.1112/jlms.12789
- S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion
  categories*, especially the orbit/stabilizer description of simples:
  https://arxiv.org/abs/1206.6625
- V. Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13, whose central
  induction statement holds at arbitrary rank:
  https://arxiv.org/abs/1309.4822

Run `PYTHONDONTWRITEBYTECODE=1 python -O verify_R332.py` in this folder.
It uses frozen tensors and standard-library rational arithmetic, checks full
source/target associativity, the source action, all 216 target products, the
forgetful map, both excluded duality branches, both characters, and the norm.
There are no optimizers, repository imports, or Python assertions in the replay.
