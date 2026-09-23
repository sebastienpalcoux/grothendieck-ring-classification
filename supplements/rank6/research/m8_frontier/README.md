# First residual: exact stronger conditions and primary-source model audit

The general existence status of `R6_3_215` is **unknown**. Its positive dimensions
are `(1,1,d,d,d-1,d+1)`, `d=4+sqrt(17)`, and its dimension is
`136+32*sqrt(17)`. No ring is excluded by matching or failing to match dimensions.

`low_product_gram.py` adds one joint nonnegative integral Gram matrix for all
15 products of the five nontrivial low central objects. This strengthens
separate third-order Verlinde and product-restriction constraints. The script
first rechecks the inherited exact induction witness, then reconstructs and
checks every fourth-order moment and restriction equation. It does not call a
numerical optimizer or re-enumerate fusion rings.

```bash
python research/m8_frontier/low_product_gram.py --check
python -O research/m8_frontier/low_product_gram.py --check
```

The supplied rank-22 witness survives. Its 15-by-15 residual Gram matrix has
rank 3; the three high restriction types have multiplicities `(4,8,4)` and are
linearly independent. The zero type-variance matrix forces unique constant
product coefficients within each type. All are nonnegative integers, and the
expanded 15-by-16 matrix satisfies both Gram and restriction identities exactly.
This is a stronger **necessary-condition witness**, not a modular datum,
associative center tensor, algebra structure or categorification.

The proof and application are integrated into Section 4 of the paper. Rejection of one
candidate completion would not suffice to exclude its source ring: that would
require exhaustive treatment of all allowed center possibilities. No new general
exclusion is allocated from these experiments.
