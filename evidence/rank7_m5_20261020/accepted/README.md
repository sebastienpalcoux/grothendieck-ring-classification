# Accepted continuation decisions

`decisions.json` contains the reviewed general exclusions admitted to the
rank-seven ledger. `assemble.py` binds them to the frozen initial frontier
in `../computation/source_frontier.json`. For inherited computational
proof trees it additionally requires successful normal and optimized
replay receipts whose hashes match the current candidate files.

The conductor-60 entries bind both the pseudo-unitary trace certificate
and the separate signed/Galois reduction that gives general scope. The
Morita entry contains the complete regenerated R4982 certificate.

`supplements/rank7/software/finalize_m5.py` applies these entries only to
open records and rejects a conflict with an already recorded continuation
decision. `verify_m5.py` replays each accepted mathematical certificate
from its census tensor. It preserves all 4,201 earlier-band records.

R4982's assertion-bearing components run in an isolated temporary tree
with Python optimization disabled, even when the aggregate verifier is
invoked with `-O`. The aggregate receipt explicitly records this mode.
Its regenerated certificate must equal the accepted certificate exactly.
