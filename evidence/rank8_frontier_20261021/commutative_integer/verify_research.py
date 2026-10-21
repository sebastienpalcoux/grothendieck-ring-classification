"""Read-only exact replay of the final five-case commutative integer stage.

Numerical discovery is never invoked. Independent target domains run
sequentially to respect the shared memory limit. The optimized interpreter
flag is passed through to every child.
"""
from pathlib import Path
import os, subprocess, sys
import final_campaign as campaign

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent


def main():
    campaign.main()
    prefix = [sys.executable] + (['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else [])
    env = dict(os.environ)
    env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    for relative in campaign.CONTROLS + campaign.REPLAYS:
        print('EXACT INTEGER REPLAY', relative, flush=True)
        subprocess.run(prefix + [str(STAGE / relative)], check=True, env=env)
    campaign.main()
    print('PASS complete final commutative integer research replay', flush=True)


if __name__ == '__main__': main()
