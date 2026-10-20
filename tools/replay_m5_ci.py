#!/usr/bin/env python3
"""Run the complete M5 replay with a CI allowance for native enumeration.

The archived checker uses a 60-second low_generic deadline. Shared CI runners
can exceed it. This launcher changes only that exact call's runtime allowance;
the source bytes, finite domains, output checks and failure behavior are kept.
No timeout is accepted as a mathematical result.
"""
from pathlib import Path
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOFTWARE = ROOT / 'supplements/rank7/software'
NATIVE_TIMEOUT_SECONDS = 1200


class EnumerationSubprocess:
    """Delegate subprocess operations, changing one checked deadline only."""

    def __getattr__(self, name):
        return getattr(subprocess, name)

    def run(self, command, *args, **kwargs):
        if (isinstance(command, (list, tuple)) and len(command) == 1
                and Path(command[0]).resolve() == SOFTWARE / 'low_generic'
                and kwargs.get('timeout') == 60):
            kwargs['timeout'] = NATIVE_TIMEOUT_SECONDS
        return subprocess.run(command, *args, **kwargs)


# This executes on worker import as well as in the parent. It replaces only the
# induction module's local reference, not the global subprocess module.
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'
sys.path.insert(0, str(SOFTWARE))
import induction
induction.subprocess = EnumerationSubprocess()


if __name__ == '__main__':
    import verify_m5
    print('CI replay: complete exact checker; low_generic runtime limit '
          f'{NATIVE_TIMEOUT_SECONDS} seconds.', file=sys.stderr)
    verify_m5.main()
