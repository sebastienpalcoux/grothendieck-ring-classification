# D144 local source and complete inverse-tensor certificate

Read `theory.md` together with the global extension and exhaustion proof in `../../d144/new_morita_reduction.md`.

Replays (all inputs are frozen locally):

```sh
python -O local_c4.py
python -O nimrep.py
```

The first verifies the actual local Liptrap source, the neutral V4 coboundary, the unique marked order-four Brauer--Picard class, vanishing local H², and the support/duality data. The second reconstructs the full inverse tensor from the theoretically forced NIMrep alternatives, exhibits the exact associativity contradiction for the four impossible label choices, and matches every coefficient of the other four choices to R12_1_320.

`input_manifest.json` records the frozen input hashes. This is an assistance certificate; the final D144 classification is counted in the sibling d144 results, not again in the D32 results.
