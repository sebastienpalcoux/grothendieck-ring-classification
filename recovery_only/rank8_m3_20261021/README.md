# Recovery-only oversized snapshots

These lossless snapshots are stored outside the live proof inventory. They
represent the current checkpoint, not a final classification release. In a
fresh checkpoint checkout only, run `python3 recovery_only/rank8_m3_20261021/restore.py`
to restore exact oversized data paths after verifying compressed and raw hashes.
Do not run this over newer live campaign files.
