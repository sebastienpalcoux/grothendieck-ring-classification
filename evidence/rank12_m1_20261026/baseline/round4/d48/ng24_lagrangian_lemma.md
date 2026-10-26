# An odd-Lagrangian criterion for the dimension-24 near-group branch

## Lemma

Let pi:S4->S3 be the quotient by the normal Klein four group V, and let omega=pi*nu for a normalized complex 3-cocycle nu of S3. The center of Vec_(S4)^omega has exactly three Lagrangian subcategories. Consequently, if a fusion category D is Morita equivalent to Vec_(S4)^omega, every genuine C2 action on D has group-theoretical equivariantization.

## Proof

The only normal abelian subgroups of S4 are 1 and V. Naidu–Nikshych, Theorem 4.12, parameterizes the Lagrangians by such a subgroup K and an invariant alternating omega-bicharacter on K.

Since nu is normalized, omega(a,b,c)=1 whenever at least one argument lies in V. For a in V and arbitrary h,g in S4, formula (19) of that paper gives

\[
 \beta_a(h,g)=\omega(a,h,g)\,
 \omega(h,h^{-1}ah,g)^{-1}\,
 \omega(h,g,(hg)^{-1}ahg)=1.
\]

Indeed, each of the three factors has an argument in V, because V is normal. Thus both the twisted multiplicativity condition (26) and the twisted conjugation condition (27) reduce exactly to ordinary bicharacter multiplicativity and ordinary S4-invariance on V.

Identify V with F2². Its alternating bicharacters are precisely

\[
 B_0(u,v)=1,\qquad
 B_1(u,v)=(-1)^{u_1v_2+u_2v_1}.
\]

Conjugation by S4 induces GL2(F2). Every matrix in this group has determinant one in F2, so both forms are invariant. Hence K=V contributes exactly two Lagrangians. K=1 contributes exactly the canonical third Lagrangian, and there are no other possible subgroups. This proves the count.

Morita equivalent fusion categories have braided-equivalent centers, so Z(D) has the same three Lagrangians. A tensor action of C2 on D induces an action on this finite set. An involution on a set of odd cardinality fixes an element. By Gelaki–Naidu–Nikshych, Corollary 3.11, a stable Lagrangian is exactly the criterion for D^C2 to be group-theoretical. This uses a setwise stable fusion subcategory, not a choice of equivariant algebra structure; the quoted criterion supplies the required categorical implication.

## Application to arbitrary complex near-group categories

To apply the lemma to an arbitrary complex category of near-group type (D8,2) or (Q8,2), first establish the classification premise. Its dimension is 24=2³·3, hence ENO's prime-power-product theorem makes it solvable, and therefore weakly group-theoretical. The unitarizability theorem of Galindo–Hong–Rowell then permits the complete unitary near-group classification to be used. Izumi–Tucker Theorem 1.2 (quoting Izumi, Theorem 6.1) states that each extraspecial group has exactly three unitary near-group categories. Their Theorem 3.2 constructs three for D8 and three for Q8, distinguished by the third Frobenius–Schur indicator, exhausting that classification. Section 3.2 and the subsequent cochain adaptation show that their associator classes are inflated from S3; the adapted representative need not itself be literally inflated, but it is cohomologous to an inflated one, which is sufficient for the center argument. Thus the arbitrary original near-group category is Morita equivalent to one of the pointed categories in the lemma.

The unitarity bridge and the complete classification must both be cited; merely producing the Izumi–Tucker models would not establish this premise for an arbitrary original category. Once that premise is verified, every C2-equivariantization of either near-group type is group-theoretical. This corrects the earlier invalid blanket dismissal of near-group (G8,2): these categories do exist, but their equivariantizations admit the group-theoretical reduction proved here.

For completeness, an abelian group of order8 cannot occur in the dimension24 near-group branch. The integral abelian near-group classification (Etingof–Gelaki–Ostrik, as explicitly recalled in Izumi–Tucker, Introduction) makes such a category Morita equivalent to the affine group F_q semidirect F_q^times, with |G|=q-1. Here q=9, which would force global dimension q(q-1)=72, whereas the proposed near-group ring has dimension8+4²=24. Thus the only categorifiable groups of order8 in this branch are D8 and Q8, already covered above. This is a categorical dimension contradiction, not the invalid earlier blanket dismissal of nonabelian near-group rings.

No census ring is excluded by this lemma alone. All categorical branches and the complete group-theoretical fusion-rule classification must still be combined before a general-complex exclusion is valid.

## Primary references

- D. Naidu and D. Nikshych, *Lagrangian subcategories and braided tensor equivalences of twisted quantum doubles of finite groups*, arXiv:0705.0665v2, definitions 4.5–4.6, equations (19), (26), (27), theorem 4.12. https://arxiv.org/pdf/0705.0665
- S. Gelaki, D. Naidu and D. Nikshych, *Centers of graded fusion categories*, Algebra & Number Theory 3 (2009), Corollary 3.11. https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf

- M. Izumi and H. Tucker, *Algebraic realization of noncommutative near-group fusion categories*, arXiv:1908.01655, Theorems 1.2 and 3.2, Sections 3.2–3.3. https://arxiv.org/html/1908.01655
- P. Etingof, D. Nikshych and V. Ostrik, *Weakly group-theoretical and solvable fusion categories*, Theorem 1.6 (prime-power-product dimension). https://arxiv.org/abs/0809.3031
- C. Galindo, S.-M. Hong and E. C. Rowell, *Generalized and quasi-localizations of braid group representations*, Theorem 5.20 (weakly group-theoretical categories are completely unitary). https://people.tamu.edu/~rowell/GHRarx1.pdf
