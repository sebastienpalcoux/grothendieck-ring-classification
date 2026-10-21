# A central fermion need not admit a negative scalar dimension character

The proposed implication is false even for a unitary fusion category with a free
fermion action and an all-M-type fermionic quotient. This observation closes a
potential obstruction route for R8_3_941; it makes no model claim for that ring.

Write an element of V=C2×C2 as g=(g1,g2), encoded by g1+2g2, and set

    b(g,h)=g1*h1+g2*h2+g2*h1 mod 2.

The extension H=V×C2 with multiplication
(g,a)(h,b)=(g+h,a+b+b(g,h)) is Q8. Its central involution f=(0,1)
acts freely on all eight group elements and is a commutator: if x=(1,0)
and y=(2,0), then xy=f yx. Consequently every one-dimensional complex
representation of the fusion ring Z[Q8] sends f to +1.

The exact script supplies a normalized function A:V³→Z/4 satisfying

    A(g,h,k)+A(g,h+k,l)+A(h,k,l)
    -A(g+h,k,l)-A(g,h,k+l)=2 b(g,h)b(k,l) mod 4.

It defines the unitary associator on H by

    omega((g,a),(h,b),(k,c))=i^[A(g,h,k)+2c b(g,h)].

This is the pointed specialization of Usher, *Fermionic 6j-symbols in
superfusion categories*, arXiv:1606.03466, Theorem 5.4 and Corollary 5.8.
The verifier independently checks the ordinary pentagon on all 8^4 quadruples,
so the construction does not rely on a cohomology-existence inference.

Give f the half-braiding c(f,(g,a))=(-1)^a. The script checks every central
hexagon. The half-braiding of f with itself is −1, while f² is the central
unit with trivial half-braiding. The associator restricted to {1,f} is trivial.
Thus this is a fully faithful central sVect inside Z(Vec^omega(Q8)). Its
underlying object action is free, so the associated superfusion quotient has
four M-type simple orbits and no Q-type simple. All associator and half-braiding
scalars have modulus one; the pointed category has its positive spherical
structure and the central f has twist −1.

The absence of a scalar character f↦−1 therefore cannot be used to exclude a
category over sVect, even when the fermion action is free. A super pivotal
structure is not an ordinary pivotal structure whose dimension is the
specialization π↦−1 of the π-Grothendieck ring. In particular, the super
double-dual convention acts by parity on odd morphisms; see Aasen–Lake–Walker,
arXiv:1709.01941, §8.3, equation (320). Existence of a different ordinary
pivotal structure with dimension(f)=−1 is an additional condition.

Replay: `python review/fermion_no_negative_character.py` (relative to this
evidence root), and likewise with `python -O`. Both pass. All required data
are in the script and its exact JSON receipt; no numerical solver is used.
