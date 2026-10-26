# Independent final package audit

PASS. The 632-record ledger differs from the frozen baseline in exactly R12_1_561, R12_1_623, and R12_1_628, all previously unresolved. The other 629 full record objects are identical. Summary, CSV, and new-decisions files agree: 480 excluded, 151 previously unitary models, one additional pseudo-unitary model, and no unresolved entries. R623 is explicitly marked `pseudo_unitarily_realized`, with unitarity not established.

All new proof/replay links exist. The full 1728-entry R623 model tensor matches the frozen census under the recorded map. The independent verifier's portability change only replaces its former workspace input path with the identical adjacent frozen tensor; mathematical logic is unchanged.

All four new exact replays passed with Python -O from a freshly copied, renamed temporary evidence directory and cwd `/`, without PYTHONPATH. No full baseline replay was repeated. This audit is separate from the package's integrated verification receipt and from the earlier categorical proof reviews.
