"""Replay the research supplement against the frozen multiplicity-nine release.

Set RANK6_PACKAGE or pass --package. Each check runs in a fresh interpreter;
neither the old release nor its mathematical receipts are modified.
"""
from pathlib import Path
import argparse,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--package',type=Path)
ap.add_argument('--optimized',action='store_true')
args=ap.parse_args()
package=args.package
if package is None and os.environ.get('RANK6_PACKAGE'):package=Path(os.environ['RANK6_PACKAGE'])
if package is None:
    package=next((p for a in ROOT.parents for p in (a,a/'Rank6_Categorification_M9')
                  if (p/'software/round3_m4.py').is_file()),None)
if package is None:raise SystemExit('Pass --package /path/to/Rank6_Categorification_M9')
package=package.resolve()
if not (package/'data/census.json').is_file():raise SystemExit('Not a rank-six base package')
env=dict(os.environ,RANK6_PACKAGE=str(package),PYTHONDONTWRITEBYTECODE='1')
rec=ROOT/'r155_modular/reconstruction.json'
jobs=[
 ['r155_modular/exact_enumeration.py'],['r155_modular/chi_i_completion.py'],
 ['r155_modular/trivial12.py'],['r155_modular/reconstruct.py'],
 ['r155_modular/full_checks.py'],['r155_modular/higher_ordinary.py'],
 ['r155_generalized/check.py'],['r155_generalized/check_B.py'],['r155_generalized/summarize.py'],
 ['r155_categorical/check_full_fusion_categorical.py'],
 ['r155_models/verify_order32_bosons.py'],['r155_models/wzw_rank26.py'],
 ['r155_models/modular_audit/independent_full_s_audit.py','--reconstruction',str(rec)],
 ['r155_models/modular_audit/forgetful_ring_audit.py','--package',str(package),'--reconstruction',str(rec)],
 ['r1660_categorical/verify_module_targets.py'],['r1660_categorical/reconstruct_dual_actions.py'],
 ['r1660_categorical/independent_audit.py'],['r1660_indicators/verify.py'],
 ['r1660_galois/verify.py','--package',str(package)],['r1660_indicators/audit_galois_cut.py'],
]
rows=[];start=time.monotonic();logs=ROOT/'verification';logs.mkdir(exist_ok=True)
for n,job in enumerate(jobs,1):
    t=time.monotonic();cmd=[sys.executable]+(['-O'] if args.optimized else [])+[str(ROOT/job[0])]+job[1:]
    result=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True,timeout=180)
    (logs/(job[0].replace('/','__')+'.log')).write_text(result.stdout+result.stderr)
    rows.append({'script':job[0],'returncode':result.returncode,'seconds':round(time.monotonic()-t,3)})
    print(f'{n}/{len(jobs)} {job[0]}: '+('PASS' if result.returncode==0 else 'FAIL'),flush=True)
    if result.returncode:raise SystemExit(result.stderr or result.stdout)
out={'passed':True,'optimized':args.optimized,'jobs':rows,'total_seconds':round(time.monotonic()-start,3),
     'categorification_claimed':False,'remaining_original_rings':['R6_4_155','R6_8_1660'],
     'R155_modular_candidate_rank':26,'R1660_center_profile_count':1669}
(logs/('replay_optimized.json' if args.optimized else 'replay.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='jobs'}))
