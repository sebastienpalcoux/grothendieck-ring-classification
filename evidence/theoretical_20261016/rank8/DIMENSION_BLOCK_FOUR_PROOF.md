# Four general exclusions from the dimension-block conductor bound

The four source tensors R8_2_35, R8_2_38, R8_2_346, R8_2_406 each have exactly four invertibles and four other simples of FP dimension d=3+sqrt(10). This is checked against all64 products, with the precise source tensor hashes, by `verify_dimension_block_four.py`.

Suppose one has a complex categorification. By the published Lemma3.1 of A.Schopieray, *Categorification of integral group rings extended by one dimension*, J.LondonMath.Soc.108(2023),1617–1641, DOI10.1112/jlms.12789, every two-FP-dimension categorification is Galois conjugate to a pseudo-unitary categorification. Therefore existence would give a spherical category with simple dimensions1,d and global dimension

    D=4(1+d²)=80+24sqrt(10).

Both the simple-dimension field and the global-dimension field are Q(sqrt(10)), so e=1. Let χ be its nontrivial quadratic character, of conductor40. Theorem5.1 of A.Schopieray, *The dimension block of a spherical fusion category*, arXiv:2609.35287v1, requires

    |1/D − 1/D'|² ≤ 1/40.

But DD'=640 and D−D'=48sqrt(10), so the left side is9/160, greater than1/40 by1/32. Contradiction.

The Galois reduction concerns existence; it is not the false assertion that every categorification is itself pseudo-unitary. The inequality is applied to the pseudo-unitary Galois conjugate. No unitary classification is used. The bound is from the explicitly pinned recent preprint v1; this dependency should be retained transparently.

Primary sources inspected:
- https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms.12789 (published corrected Lemma3.1).
- https://arxiv.org/pdf/2609.35287v1 (Theorem5.1; posted28September2026).
