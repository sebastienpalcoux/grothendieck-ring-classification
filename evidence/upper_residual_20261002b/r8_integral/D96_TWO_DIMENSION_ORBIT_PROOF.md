# A dimension96 two-dimensional orbit obstruction

## The criterion

An integral fusion category C with simple dimensions 1^4,2,4,6^2 cannot have C_ad=C. This excludes the source rings R8_2_404, R8_2_418, R8_2_604 and R8_2_692 from general complex categorification. The proof uses solvability, two small equivariantization descents, and invariant coefficients of squares. It makes no pivotal, braided or unitary assumption.

In the four applications, `verify_d96_pair.py` checks the exact positive dimension character, all 512 source coefficients, all 4096 associativity identities, the full adjoint closure and every candidate central sign. Their groups of invertibles are V4. The universal criterion also permits C4 invertibles, since only the existence of a central order-two sign is used.

## First descent

The dimension of C is96=2^5·3, so C is solvable by Etingof–Nikshych–Ostrik's p^a q^b theorem. In a solvability chain the final step is a prime cyclic extension or equivariantization. A nontrivial extension would give a nontrivial faithful grading, contrary to C_ad=C. Hence C=D^Cp. Its canonical Rep(Cp) consists of invertible objects, and |Inv(C)|=4, so p=2. Thus FPdim(D)=48. The de-equivariantization is solvable: D is a fusion subcategory of a category Morita equivalent to C, and solvability is closed under Morita equivalence and fusion subcategories.

Let epsilon be the canonical sign and tau the outer involution of D. The epsilon action fixes the unique dimension2 and dimension4 C-simples. It either fixes both dimension6 simples or exchanges them. In a C2 equivariantization a tau-fixed simple produces exactly two simple equivariant objects, exchanged by epsilon; a free two-element orbit produces one simple, fixed by epsilon, with twice the original dimension. This remains true for projective stabilizers since H2(C2,C*)=0.

Consequently D has one of two types:

- 1^4,2^2,3^4, when epsilon fixes both dimension6 objects;
- 1^4,2^2,6, when epsilon exchanges them.

In both cases tau exchanges the two dimension2 simples. In the first case it exchanges the dimension3 simples in two pairs; in the second the dimension6 simple is fixed. The four invertibles consist of two fixed invertibles and one free pair. These conclusions come from actual orbit/stabilizer rules, not a guessed center or tensor.

## The proper-adjoint branch is impossible

The adjoint subcategory D_ad is tau-invariant. Its invertibles form a subgroup of Inv(D), so their number a is1,2 or4. Its number b of dimension2 simples is0 or2 because tau exchanges the pair. In the first D type, its number c of dimension3 simples is0,2 or4. In the second, its number e of dimension6 simples is0 or1. The global dimension

a+4b+9c+36e

divides48. Complete enumeration of the proper divisors permits only dimensions1,2,4 (pointed) or12 with type1^4,2^2. The full dimension48 corresponds to all D-simples.

The pointed possibilities cannot contain X X* for a dimension3 or dimension6 object X: every invertible appears in X X* with multiplicity at most1, so at most four dimension-one summands cannot account for dimension9 or36.

For the dimension12 possibility, the neutral component contains all four invertibles and both dimension2 simples. The universal grading would have order4 and every component would have global dimension12. All simples outside the neutral component have dimension3 or6. Thus their squared dimensions sum to9c+36e, which cannot equal12. This excludes the last proper possibility. Therefore D_ad=D in both branches.

## Second descent

Solvability and D_ad=D again force D=E^Cp. Since Inv(D) has order4, p=2. Thus E is integral of dimension24. Counting fixed labels and free orbits in D leaves exactly two possible E types:

- 1^2,2,3^2;
- 1^6,3^2.

Indeed there are exactly two fixed invertibles of E, each supplying two D-invertibles. If r is the number of free invertible orbits and t the number of fixed dimension2 labels, then r+2t=2 counts the D dimension2 objects. There are no free dimension2 orbits, since D has no dimension4 object. Thus (r,t)=(0,1) or(2,0), giving the two types. The two dimension3 labels are either both fixed (yielding D type3^4) or exchanged (yielding its single dimension6 object). A fixed dimension6 label would give two dimension6 D-objects and is therefore impossible. No other E dimension is possible by the same orbit formula.

## Squares obstruct the required exchange

In the first E type, write its invertibles as1,g and its unique dimension2 simple as x. The g action fixes x, and x is self-dual by uniqueness. Frobenius reciprocity forces x² to contain both1 and g once. Dimension then gives

x²=1+g+x.

The second equivariantization has two lifts x+,x-, exchanged by its canonical central sign eta. Since eta²=1 and eta is central, the two lifts have the identical square V: x+²=x-²=V. Forgetting to E shows that V contains exactly one of x+,x-, with multiplicity1, because x occurs exactly once in x². Any tensor auto-equivalence exchanging x+,x- would have to fix V, as their two squares agree. But its action exchanges the unique dimension2 constituent of V. This is impossible.

In the second E type, let K=Inv(E), of order6. The two dimension2 D-objects come from the two free orbits of the second involution sigma on K, whose fixed subgroup has order2. The groups of order6 are C6 and S3. For C6, sigma is inversion, and its two free orbits are {1,5} and {2,4}. For S3, every involutive nontrivial automorphism is conjugation by a transposition; its free orbits are the other two transpositions and the two three-cycles.

For a free orbit O={a,sigma(a)}, the coefficient of its simple object X_O in X_O² is the coefficient at a in (a+sigma(a))² in the pointed group ring. The free stabilizer is trivial, so associator and action coherence cannot change this multiplicity. In C6 the orbit {1,5} has self-square coefficient0 and {2,4} has coefficient1. In S3 the transposition orbit has coefficient0 and the three-cycle orbit has coefficient1. Therefore the two dimension2 objects have distinct self-square coefficients and no tensor auto-equivalence can exchange them.

Both second-descent types contradict the first outer involution tau, which must exchange the two dimension2 D-simples. This proves the criterion and excludes all four source rings.

## Dependencies and exact scope

The proof uses ENO, *Weakly group-theoretical and solvable fusion categories*, arXiv:0809.3031: the p^a q^b solvability theorem and closure of solvability under Morita equivalence and fusion subcategories. It uses the standard classification of simples in an equivariantization by orbits and projective stabilizer representations (for example Burciu–Natale, *Fusion rules of equivariantizations of fusion categories*, arXiv:1206.6625). All other categorical arguments above are elementary adjoint closure, faithful grading dimensions and Frobenius reciprocity. The code supplies the complete finite integer partitions and both group-of-order6 products.

The four decisions were accepted after independent mathematical audits and identical normal and optimized source-bound replays, extending the reconstructed38-decision stage to42 decisions. Their source fingerprints are in the normal and optimized receipts. No purported induction matrix or formal modular data is used as a positive or negative existence argument.
