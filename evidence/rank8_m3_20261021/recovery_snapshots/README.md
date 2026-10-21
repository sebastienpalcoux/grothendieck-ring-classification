# Recovery-only oversized JSON snapshots

Two generated JSON snapshots exceeded the connector's 16 MiB request limit.
Their exact raw bytes are preserved here as deterministic gzip files. Run
`python3 evidence/rank8_m3_20261021/recovery_snapshots/restore.py` from a fresh
checkpoint checkout before any validation. The script verifies compressed and
raw SHA-256 hashes before restoring the ordinary paths. These snapshots are
intermediate campaign states, not a final classification or release audit.
The final release may remove this folder after its normal data layout is frozen.
