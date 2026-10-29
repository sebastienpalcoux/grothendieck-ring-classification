"""Explicit installation of independently verified additive accelerators."""
from pathlib import Path
import sys
def install():
 sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'performance'))
 import gram_vectors_rank8,low_frames_rank8,low_failure_exact
 gram_vectors_rank8.install();low_frames_rank8.install();low_failure_exact.install()
