# Verify the current publication

> **AI-generated research; independent human verification pending.** Exact checks establish only their stated computational scope.

After cloning the classification repository:

~~~sh
python3 -m pip install sympy==1.14.0 numpy==2.3.5 pypdf==6.10.0
python3 tools/restore_data.py
python3 tools/verify_current_publication.py
python3 tools/verify_current_publication.py --metadata-only
python3 evidence/frontier/replay/run_checks.py
~~~

The first command installs the verification dependencies; the second restores checksummed data. The next two validate the current ledgers, documents, website copies, profile scopes and tensors; full mode also recomputes structural ring properties. The last command replays twelve current exact checks, including the six complete-domain R1768 separators and both strengthened R137 witnesses. It performs no optimization or associator search. Run it with ordinary Python, since some short matrix verifiers use assertions.

For runtime dependencies and the explicit inherited mathematical premises, read [the current proof index](../evidence/frontier/README.md) and [R1768 replay instructions](../evidence/frontier/replay/new/r1768/REPLAY_README.md).

Earlier categorical certificates stay in their frozen rank-specific contexts. The current replay does not claim to repeat every previous exclusion or establish external hypotheses by arithmetic alone. [Manuscripts](../manuscripts/README.md) identify the corresponding proof for each rank.
