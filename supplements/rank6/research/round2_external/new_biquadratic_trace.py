"""Run the authoritative tensor-only verifier in software/."""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[2] / 'software/new_biquadratic_trace.py'), run_name='__main__')
