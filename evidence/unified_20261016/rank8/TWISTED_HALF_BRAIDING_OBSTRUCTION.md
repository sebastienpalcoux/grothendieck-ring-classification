# A pointed-support obstruction for two regular bimodule products

## General theorem

Neither R8_2_314 nor R8_2_432 is the Grothendieck ring of a fusion category over C. The proof uses no pivotal, spherical, braided, or unitary structure.

Steps 2–4 have passed independent categorical audit. All associators below are retained implicitly by monoidal coherence; no skeletal strictness hypothesis is imposed on the hypothetical category or on its autoequivalence.

## 1. Exact source data

In either hypothetical category C, let D have simples (1,g,r,gr), with

    g²=1, gr=rg, r²=g^epsilon+r+gr,

where epsilon=1 for R314 and epsilon=0 for R432. The complement M is stable under left and right tensoring by D. There is a simple X in M such that the four aX, for a simple in D, are distinct simples and exhaust M, and

    X a = F(a) X,
    F(1)=1, F(g)=g, F(r)=gr, F(gr)=r,
    X²=g^epsilon+X+gX.                                  (1)

These are equalities of isomorphism classes at this stage. The full source data are:

| Ring | D basis (1,g,r,gr) | X | M basis (X,gX,rX,grX) |
|---|---|---|---|
| R8_2_314 | (0,7,1,2) | 3 | (3,4,6,5) |
| R8_2_432 | (0,3,4,5) | 6 | (6,7,1,2) |

Also the internal end of X over D is 1. The source-bound verifier reads the full census tensors, binds their hashes, checks all 64 neutral coefficients and every support assertion above, and verifies the forced permutations used below.

## 2. The right action supplies an actual tensor autoequivalence

The functor L:D→M, a↦a⊗X, is an equivalence of left D-module categories. It maps simples bijectively to simples and is fully faithful on each Hom space: maps between distinct simples vanish, while the identity of a simple maps to the identity of the nonzero simple aX. Semisimplicity extends this to all objects. Its module structure is inherited from the associator of C.

The right action by D on M commutes coherently with this left action. Transporting it through L identifies it with right tensoring on D by a strong monoidal functor F:D→D. Since the source computation shows that F permutes the four simples as in (1), it is a tensor autoequivalence. In particular there are coherent natural isomorphisms

    delta_a: X⊗a → F(a)⊗X.                              (2)

Writing J for F's tensorator, their product compatibility is precisely the one induced by the right D-module associativity constraint. Thus (2) is not an arbitrarily selected collection of objectwise isomorphisms.

## 3. Multiplication produces a twisted half-braiding on 1+g

Apply (2) twice to obtain coherent natural isomorphisms

    X²⊗a → F²(a)⊗X².

The decomposition C=D direct-sum M is a decomposition of D-bimodule categories. Hence its projection to M is a D-bimodule functor, and the preceding isomorphism restricts coherently to the M-part of X². By (1), that part is z⊗X with z=1 direct-sum g. Replacing X⊗a by F(a)⊗X and cancelling the fully faithful functor L gives natural isomorphisms

    eta_a: z⊗F(a) → F²(a)⊗z.                            (3)

For a,b in D, the compatibility of (3), suppressing associators, is

    eta_(a b) (id_z ⊗ J^F_(a,b))
      = (J^(F²)_(a,b) ⊗ id_z)
          (id_(F² a) ⊗ eta_b) (eta_a ⊗ id_(F b)).

This can alternatively be read directly from the D-bimodule functor obtained by projecting multiplication M tensor_D M→C to M: the source has right action F² and the target has right action F.

Apply a monoidal quasi-inverse of F to (3). Since F fixes 1 and g, the object F^(-1)(z) is isomorphic to z. Transporting along this isomorphism gives an F-twisted half-braiding

    theta_a: z⊗a → F(a)⊗z,
    theta_(a b)=(J_(a,b)⊗id_z)
                    (id_(F a)⊗theta_b)(theta_a⊗id_b),   (4)

with the usual associators understood. It is natural in a, including with respect to any inclusion of a simple constituent into a tensor product.

## 4. Pointed support contradicts the r→r² channel

Choose the fixed direct-sum decomposition z=z_0 direct-sum z_1 with z_0=1 and z_1=g. Since r and gr are distinct simples and F(r)=gr, every isomorphism

    theta_r: (1+g)r → (gr)(1+g)

must exchange the two support labels: its source z_i⊗r can map only to F(r)⊗z_(i+1), with indices modulo two. Both such blocks are nonzero isomorphisms. This assertion concerns Hom spaces between distinct simples, so no choice of associators or scalar gauges changes it.

Equation (4) for a=b=r applies two such exchanges. Its remaining maps, the associators and J_(r,r)⊗id_z, preserve the direct-sum label of z by naturality. Thus theta_(r⊗r) sends the entire source summand z_i⊗(r⊗r) into the target summand F(r⊗r)⊗z_i: its support permutation is the identity.

On the other hand, r occurs in r⊗r with multiplicity one in both source rings. Choose a nonzero inclusion v:r→r⊗r. Naturality requires

    theta_(r⊗r) (id_z⊗v)
      = (F(v)⊗id_z) theta_r.                            (5)

Restricted to z_i⊗r, the left side of (5) has image in the target direct summand indexed by i. The right side has image in the target direct summand indexed by i+1. Both maps are nonzero: v and F(v) are split monomorphisms in a semisimple category, tensoring preserves them, and the theta maps are isomorphisms. Distinct direct summands have zero intersection. Equation (5) is impossible.

This proves the general exclusion of both rings. The independent categorical audit confirms Steps 2–3. The finite tensor check identifies the two concrete applications; the contradiction itself is a purely theoretical coherence and naturality argument.

