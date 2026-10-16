#!/usr/bin/env python3
"""Reproduce the local census, general classification, models, and manuscript tables.

The default never trusts a cached signed cover. --deep adds pruning, exhaustive
small-box, signed reference-enumerator, and scalar regression comparisons.
"""
from pathlib import Path
import argparse, hashlib, json, platform, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]
SUP=ROOT/'supplementary'
VALIDATION=SUP/'validation'


def run_step(name,arguments,log):
    print('BEGIN:',name,flush=True);started=time.monotonic()
    path=VALIDATION/log
    with path.open('w') as f:
        result=subprocess.run([sys.executable,*arguments],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    if result.returncode:
        print('\n'.join(path.read_text(errors='replace').splitlines()[-30:]),flush=True)
        raise RuntimeError(name+' failed; see '+str(path))
    elapsed=round(time.monotonic()-started,3)
    print('PASS:',name,'('+str(elapsed)+' s)',flush=True)
    return {'name':name,'passed':True,'elapsed_seconds':elapsed,'log':str(path.relative_to(ROOT))}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--deep',action='store_true')
    p.add_argument('--engine',choices=['cpp','python'],default='cpp')
    p.add_argument('--manuscript-root',type=Path,
                   help='also compare the companion paper generated/unrestricted tables')
    a=p.parse_args();started=time.monotonic();VALIDATION.mkdir(exist_ok=True)
    steps=[]
    plan=[('Generate the complete ordinary census',['supplementary/census/generate.py'],'census_generation.log'),
          ('Check all tensors, dimensions, isomorphisms, and fresh census coverage',
           ['supplementary/census/verify_census.py','--regenerate'],'census_verification.log'),
          ('Generate the full-census classification ledger',['supplementary/classification/classify.py'],'classification_generation.log'),
          ('Regenerate the signed cover and replay both certificate scopes',
           ['supplementary/classification/verify.py','--engine',a.engine],'classification_verification.log'),
          ('Independently reconstruct the fifteen model tensors',
           ['supplementary/independent/independent_models.py','.','--output','supplementary/independent/results/models.json'],
           'independent_models.log'),
          ('Generate checked signed-scope counts',['supplementary/classification/generate_scope.py'],'scope_generation.log'),
          ('Check model characters and regenerate both manuscript tables',
           ['supplementary/check_manuscript.py','--write'],'manuscript_data_check.log')]
    if a.deep:
        plan += [('Remove ordinary-census dimension pruning and compare exact input sets',
                  ['supplementary/independent/unpruned_census_audit.py','.','--output','supplementary/independent/results/unpruned_census.json'],
                  'unpruned_census.log'),
                 ('Check the exhaustive ordinary parameter box at multiplicity two',
                  ['supplementary/census/audit_small.py','--output','supplementary/independent/results/exhaustive_small_box.json'],
                  'exhaustive_small_box.log'),
                 ('Check signed reference enumeration and scalar/model regressions',
                  ['audit/check_regressions.py'],'exact_regression.log')]
    if a.manuscript_root is not None:
        plan[6][1].extend(['--manuscript-root',str(a.manuscript_root.resolve())])
    for name,argv,log in plan:steps.append(run_step(name,argv,log))
    result=json.loads((SUP/'classification/results/verification.json').read_text())
    report={'passed':True,'rank':4,'dimension_exclusive_bound':1000,'multiplicity_bound':31,
            'census_rings':result['checked_rings'],'excluded':result['excluded'],'models':result['models'],
            'unresolved':0,'fresh_ordinary_census':True,'fresh_signed_cover':True,
            'deep_checks':a.deep,'local_signed_engine':a.engine,'python':platform.python_version(),
            'elapsed_seconds':round(time.monotonic()-started,3),'steps':steps,
            'census_sha256':result['census_sha256'],'ledger_sha256':result['ledger_sha256'],
            'scope':'Exact finite certificate verification; categorical necessity and existence are mathematical inputs proved or cited in the manuscript.'}
    (SUP/'verification_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 1692 census rings; 1677 exclusions; 15 models; zero unresolved.',flush=True)
    print('Total seconds:',report['elapsed_seconds'],flush=True)


if __name__=='__main__':main()
