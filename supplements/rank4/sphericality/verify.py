#!/usr/bin/env python3
"""Replay the ordinary census, the descent to sphericality and the model checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / 'results'


def run(name, script, *arguments, capture=False):
    print(name, flush=True)
    env = dict(os.environ, PYTHONOPTIMIZE='', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, '-B', str(script), *map(str,arguments)],
                            cwd=ROOT,env=env,check=True,text=True,
                            stdout=subprocess.PIPE if capture else None)
    if capture:
        print(result.stdout,end='')
    return result.stdout


def read(filename):
    return json.loads((REPORTS / filename).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path,help='also compare the fifteen printed model rows')
    args = parser.parse_args()
    manuscript = args.manuscript.resolve() if args.manuscript else None
    REPORTS.mkdir(exist_ok=True)
    ordinary = ROOT / 'supplementary/census'
    independent = ROOT / 'supplementary/independent'
    run('Ordinary census and tensor verification',ordinary/'verify_census.py',
        '--regenerate','--report',REPORTS/'ordinary.json')
    run('Ordinary census without dimension pruning',independent/'unpruned_census_audit.py',
        ROOT,'--output',REPORTS/'unpruned.json')
    run('Exhaustive ordinary coefficient box at multiplicity two',ordinary/'audit_small.py',
        '--output',REPORTS/'small_box.json')
    descent = run('Finite signed descent on the ordinary tables',ROOT/'verify_descent.py',capture=True)
    expected = {'self-dual rings':1642,'without nontrivial invertibles':1259,
                'without a forbidden rank-two subring':905,'ordinary d-numbers':71,
                'ordinary field test':41,'proper signed tuples in this gauge':1798,
                'pairs of ordinary rings and signed polynomials':623,'norm-test survivors':2,
                'remaining candidates for nonspherical categorifications':0}
    for key, count in expected.items():
        if descent.splitlines().count(f'{key}: {count}') != 1:
            raise ValueError('descent count differs from the manuscript: '+key)
    (REPORTS/'descent.json').write_text(json.dumps(expected,indent=2)+'\n')
    run('Independent model reconstruction',independent/'independent_models.py',
        ROOT,'--output',REPORTS/'reconstructions.json')
    model_args = ['--output',REPORTS/'models.json']
    if manuscript:
        model_args.extend(['--manuscript',manuscript])
    run('Model dimensions and ordinary census identifications',
        ROOT/'supplementary/models/check_models.py',*model_args)
    for script in [ROOT/'audit/verify_quadratic_intervals.py',ROOT/'quartic_bounds.py']:
        run(script.stem,script)
    counts = read('ordinary.json')
    if counts['type_counts'] != {'S':1642,'N':50} or counts['rings_verified'] != 1692:
        raise ValueError('unexpected ordinary counts')
    summary = {'ordinary_rings':1692,'ordinary_by_duality':counts['type_counts'],
               'unpruned_rings':read('unpruned.json')['unpruned_rings'],
               'models_checked':len(read('models.json')),
               'fresh_descent_passed':True,
               'ordinary_records_sha256':hashlib.sha256((ordinary/'data/rings.jsonl').read_bytes()).hexdigest()}
    (REPORTS/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('PASS: ordinary census, finite descent, analytic scalar checks, and fifteen model identifications.')


if __name__ == '__main__':
    main()
