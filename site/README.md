# Grothendieck Ring Atlas

Private, static research site for exact based-ring census counts and the current categorification classification. The visible count table is generated from the private classification repository's data/counts.json, which pins fusion-ring-census at commit b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726. The separate status ledger distinguishes complete decisions and partial bands with residuals. Multiplicity means the exact maximum structure constant. The site features ranks 2–6; rank 7–8 census-only datasets stay in the underlying census repository. Count bands of rank 4–6 without classification analysis are omitted from the site snapshot.

## Regenerate

Run these commands from this directory in the classification repository:

    python3 build_snapshot.py --classification ..
    npm run check
    npm run dev

For the independent Sites checkout, pass the absolute path to the classification repository. build_snapshot.py rejects missing multiplicities, wrong cumulative totals, mismatched classification counts, and status partitions that do not sum to a cell's census count. The site serves only dist/ and needs no runtime APIs or credentials. Relative asset links make it portable to a repository subpath.

## Contents

- dist/index.html, styles.css, app.js: accessible count explorer, filters, multiplicity jump, source links, status details, local trend plot, and paper shelf.
- dist/data/atlas.json, counts.csv: generated portable count snapshot.
- dist/data/classification_status.json: exact per-band classification ledger, copied from the repository.
- dist/papers/: revised manuscripts and guides.
- dev-preview.mjs: dependency-free local preview for QA.

## Private publication

Keep the GitHub repository private. Do not enable ordinary GitHub Pages for a personal account: its site can be public even when source is private. Private GitHub Pages requires an organization on GitHub Enterprise Cloud. This snapshot is hosted privately through Sites; its .openai/hosting.json is held in the Site checkout, outside this portable repository subtree. Verify access rules before changing hosting.

The rank-three manuscript proves the unrestricted five-ring necessity directly, together with sphericality. Its classification-status ledger can therefore mark every displayed rank-three multiplicity as complete.
