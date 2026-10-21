"""Canonical read-only exact replay of completed frontier research results.

Each subprocess isolates field adapters/caches. No numerical discovery or
SciPy is needed. Feasible relaxations and single-frame negatives retain
their explicitly limited scopes.
"""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent
VALIDATIONS=('verify_streaming.py','verify_frames.py','verify_sts.py','verify_generic.py')
RESULTS=(
 ('column_generation.py','results/R8_3_334_h4.json'),
 ('column_generation.py','results/R8_3_1453_h4.json'),
 ('column_generation.py','results/R8_3_1739_h4.json'),
 ('frame_generation.py','frame_results/R8_3_334_h4.json'),
 ('frame_generation.py','frame_results/R8_3_903_h4.json'),
 ('frame_generation.py','frame_results/R8_3_1739_h4.json'),
 ('spectral_generation.py','spectral_results/R8_3_334_h4.json'),
 ('sts_generation.py','sts_results/R8_3_334_h4.json'),
 ('fixed_frame.py','fixed_results/R8_3_334_frame39_h4.json'),
 ('fixed_frame.py','fixed_results/R8_3_1739_frame3445_h4.json'),
 ('fixed_frame.py','fixed_results/R8_3_1739_frame3445_h6.json'),
)
def run(script,*args):
    command=[sys.executable]+(['-O'] if not __debug__ else [])+[str(HERE/script),*map(str,args)]
    subprocess.run(command,check=True)
def main():
    for script in VALIDATIONS:run(script)
    for script,result in RESULTS:run(script,'--verify',HERE/result)
    for rid in ('R8_3_1739','R8_3_1768'):run('partial_s.py','--ring',rid)
    print('PASS all named completed global-induction research certificates',flush=True)
if __name__=='__main__':main()
