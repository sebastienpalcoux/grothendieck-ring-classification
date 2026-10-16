# Independent unsigned rank-four recount

These unchanged archived sources reproduce the additional prepublication census check. They enumerate fusion rings and do not decide categorifiability. The archive identity and each source hash are recorded in `SOURCE_MANIFEST.json`; the accompanying census-source license and notice are preserved.

Run `python3 count_rings.py --bound 128 --threads 2` here, with Python 3 and g++ supporting C++17 and OpenMP. The command imports no census, sets no default timeout, and writes the full results to `oeis/counts_128.json`. Compare its `counts` object with `by_m` in `supplements/rank4/data/census_128_manifest.json`. Both must contain precisely the 128 multiplicities 1 through 128.

The fresh prepublication run completed with 889,530 classes: 889,157 self-dual and 373 with one dual pair. Every exact-multiplicity count agreed. The corresponding receipt is `../rank4_unsigned_recount_comparison.json`, with raw counts in `../rank4_fresh_unsigned_counts_128.json`.

This is AI-generated research and an AI-performed audit. Independent expert human verification and Lean formalization remain pending.
