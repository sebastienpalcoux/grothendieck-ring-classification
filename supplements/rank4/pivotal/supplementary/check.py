#!/usr/bin/env python3
"""Regenerate and verify the bounded census, certificates, and model matches.

All reported classification counts are read from freshly verified outputs.
Use --deep for the unpruned and exhaustive-small-box cross-checks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def require(test, message):
    if not test:
        raise RuntimeError(message)

def load(path):
    return json.loads(path.read_text())

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true',
                        help='Replay the release data without replacing the census or certificate ledger.')
    parser.add_argument('--deep', action='store_true',
                        help='Also rebuild temporary unpruned and exhaustive-small-box censuses (requires g++).')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    require(args.workers >= 1, '--workers must be positive')
    started = time.monotonic()
    evidence = ROOT/'validation'
    independent = ROOT/'independent/results'
    evidence.mkdir(exist_ok=True); independent.mkdir(exist_ok=True)
    report_path = ROOT/'verification_report.json'
    report = {'all_checks_passed':False, 'status':'running',
              'regenerated':not args.verify_only, 'deep_checks_requested':args.deep,
              'workers':args.workers, 'python':platform.python_version(), 'steps':[]}
    write(report_path,report)  # Never leave a stale PASS after a failed rerun.

    def run(label, script, *extra, optimized=False):
        flags = ['-O'] if optimized else []
        cmd = [sys.executable,*flags,str(ROOT/script),*map(str,extra)]
        relative_cmd = ['python3',*flags,str(Path('supplementary')/script),*map(str,extra)]
        step_start = time.monotonic()
        print(f'[{len(report["steps"])+1}] {label}', flush=True)
        logfile=evidence/(label+'.log')
        with logfile.open('w') as out:
            result = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, cwd=ROOT.parent)
        step={'name':label,'command':relative_cmd,'return_code':result.returncode,
              'seconds':round(time.monotonic()-step_start,3),'log':str(logfile.relative_to(ROOT))}
        report['steps'].append(step);write(report_path,report)
        if result.returncode:
            print(logfile.read_text()[-10000:], file=sys.stderr)
            raise RuntimeError(f'{label} failed; see {logfile}')

    try:
        if not args.verify_only or args.deep:
            run('linear_box_regression','tests/linear_box_regression.py')
        if not args.verify_only:
            run('census_regeneration','census/generate.py')
        run('census_verification','census/verify_census.py')
        if not args.verify_only:
            run('certificate_regeneration','classification/classify.py','--workers',args.workers)
        run('certificate_verification','classification/verify.py','--workers',args.workers)
        run('certificate_verification_optimized','classification/verify.py','--workers',args.workers,
            '--report',ROOT/'classification/results/verification_optimized.json',optimized=True)
        run('stage_reproduction','stages.py','--all','--workers',args.workers)
        run('stage_regressions','tests/stages_regression.py')
        run('regression_tests','tests/regression.py','--output',ROOT/'tests/results.json')
        run('regression_tests_optimized','tests/regression.py',
            '--output',ROOT/'tests/results_optimized.json',optimized=True)
        for name in ['independent_central_audit','independent_fourth_audit','independent_models']:
            extra=['--workers',args.workers] if name=='independent_central_audit' else []
            run(name,'independent/'+name+'.py',ROOT.parent,'--output',independent/(name+'.json'),*extra)
        if args.deep:
            run('unpruned_census_audit','independent/unpruned_census_audit.py',ROOT.parent,
                '--output',independent/'unpruned_census_audit.json')
            run('exhaustive_small_box','census/audit_small.py','--output',independent/'exhaustive_small_box.json')
            run('strict_dimension_boundaries','census/audit_boundaries.py',
                '--output',independent/'strict_dimension_boundaries.json')
        run('manuscript_data_check','check_manuscript.py',*(['--write'] if not args.verify_only else []),
            '--output',evidence/'manuscript_data_check.json')
        census=load(ROOT/'census/audit.json')
        classification=load(ROOT/'classification/results/verification.json')
        optimized=load(ROOT/'classification/results/verification_optimized.json')
        summary=load(ROOT/'classification/results/summary.json')
        for result in [census,classification,optimized,load(ROOT/'tests/results.json'),
                       load(ROOT/'tests/results_optimized.json')]:
            require(result['all_checks_passed'], 'a component has not passed')
        require(classification['verified_filters']==optimized['verified_filters'], 'optimization changed outcomes')
        staged=load(evidence/'stages/all.json')
        require(staged['all_checks_passed'] and staged['model_records_replayed']==15, 'staged reproduction failed')
        require(load(ROOT/'tests/stages_results.json')['all_checks_passed'], 'stage regressions failed')
        require(len(staged['model_endpoint']['models'])==15 and len(staged['remaining_ids'])==15,
                'staged endpoint differs from exactly fifteen models')
        require(census['rings_verified']==classification['checked_rings']==summary['census_count'],
                'verified census totals differ')
        require(classification['verified_models']==summary['model_count'], 'verified model totals differ')
        for name in ['independent_central_audit','independent_fourth_audit','independent_models']:
            require(load(independent/(name+'.json'))['passed'], name+' did not pass')
        require(load(independent/'independent_models.json')['models']==classification['verified_models'],
                'independent model count differs')
        if args.deep:
            require(load(independent/'unpruned_census_audit.json')['passed'], 'unpruned comparison did not pass')
            require(load(independent/'exhaustive_small_box.json')['exact_set_equality'], 'small-box comparison differs')
            require(load(independent/'strict_dimension_boundaries.json')['passed'],
                    'strict dimension boundary comparison differs')
        report.update({'all_checks_passed':True,'status':'passed',
                       'rings':classification['checked_rings'],'models':classification['verified_models'],
                       'excluded':classification['checked_rings']-classification['verified_models'],
                       'type_counts':census['type_counts'],
                       'verified_filters':classification['verified_filters'],
                       'arithmetic_backend':classification['arithmetic_backend'],
                       'ordinary_and_optimized_replays':True,
                       'fresh_stage_reproduction':True,
                       'stage_regression_tests':load(ROOT/'tests/stages_results.json')['tests'],
                       'central_survivors':len(staged['model_endpoint']['models']),
                       'independent_central_records':load(independent/'independent_central_audit.json')['central_records'],
                       'independent_arithmetic_records':load(independent/'independent_central_audit.json')['arithmetic_records'],
                       'independent_spherical_records':load(independent/'independent_central_audit.json')['spherical_records'],
                       'regression_tests_per_mode':load(ROOT/'tests/results.json')['tests']})
    except Exception as exc:
        report.update({'all_checks_passed':False,'status':'failed','error':str(exc)})
        raise
    finally:
        report['seconds']=round(time.monotonic()-started,3)
        write(report_path,report)
    print(f'PASS: {report["rings"]:,} rings; {report["excluded"]:,} exclusions; {report["models"]} model rings.')
    print(f'Total time: {report["seconds"]} seconds. Evidence: {report_path}')

if __name__=='__main__':
    main()
