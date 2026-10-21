"""Canonical read-only exact replay of completed frontier research results.

Each subprocess isolates field adapters/caches. No numerical discovery or
SciPy is needed. Feasible relaxations and single-frame negatives retain
their explicitly limited scopes.
"""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent
VALIDATIONS=('verify_streaming.py','verify_frames.py','verify_sts.py','verify_generic.py','verify_atomic.py','../quadratic/octic_low_s_general.py','../quadratic/review_cm_real_sts.py')
RESULTS=(
 ('column_generation.py','results/R8_3_334_h4.json'),
 ('column_generation.py','results/R8_3_1453_h4.json'),
 ('column_generation.py','results/R8_3_1739_h4.json'),
 ('frame_generation.py','frame_results/R8_3_334_h4.json'),
 ('frame_generation.py','frame_results/R8_3_903_h4.json'),
 ('frame_generation.py','frame_results/R8_3_1739_h4.json'),
 ('spectral_generation.py','spectral_results/R8_3_334_h4.json'),
 ('sts_generation.py','sts_results/R8_3_334_h4.json'),
 ('generic_generation.py','generic_results/R8_3_901_frame_h4.json'),
 ('atomic_spectrum_generation.py','atomic_spectrum_results/R8_3_65_h4.json'),
 ('atomic_spectrum_generation.py','atomic_spectrum_results/R8_3_3472_h4.json'),
 ('generic_generation.py','generic_results/R8_3_1463_sts_frame_h4.json'),
 ('complete_phase_one.py','complete_results/R8_3_334_sts_frame_h4.json'),
 ('complete_phase_one.py','complete_results/R8_3_982_sts_frame_h4.json'),
 ('complete_phase_one.py','complete_results/R8_3_1768_atomic_real_sts_h4.json'),
 ('complete_phase_one.py','complete_results/R8_3_1795_atomic_real_sts_h4.json'),
 ('cm_generation.py','complete_results/R8_3_65_cm_real_sts_h4.json'),
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
    run('final_campaign.py')
    print('PASS all named completed global-induction research certificates',flush=True)
if __name__=='__main__':main()
