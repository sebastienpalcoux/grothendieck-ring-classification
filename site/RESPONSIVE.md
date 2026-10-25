# Responsive Atlas

The public Atlas uses the same addresses and records on phones and desktops. CSS viewport queries adapt the layout automatically, including rotation and resizing; there is no user-agent redirect or separate mobile dataset.

Phone layouts have a collapsible navigation menu, readable controls, a single-column reading order, accessible model dialogs and horizontally scrolling exact tables. Selecting a count brings its details into view, with a link back to the table. Without JavaScript, navigation remains visible.

The 25 October browser receipt records 44 layout checks across the Atlas and standalone census page, eight interaction checks, and the tested source hashes. Chromium phone emulation is distinct from physical-device or WebKit testing.

To reproduce the Atlas checks, install Playwright and its Chromium browser, restore the repository data, then run:

```bash
python3 tools/restore_data.py
node site/check_responsive.cjs --output-dir /tmp/atlas-responsive-check
```

Use a new output directory. `BROWSER_EXECUTABLE` can select an installed Chromium executable. Optional `--census-root /path/to/fusion-ring-census` adds the standalone census-page checks. The test starts its own local servers; it does not modify a published website.

Large-range checks verify the fixed row geometry, the final multiplicity-1000 row and both Enter and committed-input jumps. These interface changes leave mathematical source programs, tensors and classification decisions unchanged.
