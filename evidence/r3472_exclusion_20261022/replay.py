#!/usr/bin/env python3
"""Replay the source-derived exclusion. All child checks run with assertions on."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tempfile,time
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--quick',action='store_true',help='Only both exact terminal checkers and their data linkage.')
parser.add_argument('--skip-spherical',action='store_true',help='Skip the separately certified complete sphericalization search.')
parser.add_argument('--write',action='store_true',help='Refresh verification.json and proof_manifest.json after a complete replay.')
a=parser.parse_args()
if a.write and (a.quick or a.skip_spherical):raise SystemExit('--write requires the complete replay.')
if (P/'proof_manifest.json').exists() and not a.write:
    manifest=json.loads((P/'proof_manifest.json').read_text())
    for relative,expected in manifest['files'].items():
        path=ROOT/relative
        if not path.is_file()or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise SystemExit('Proof-source hash mismatch: '+relative)
stages=[]
if not a.quick:
    if not a.skip_spherical:stages.append(('general_spherical_gate',ROOT/'evidence/rank8_research_20261022/pivotality/verify_general_spherical_gates.py',['--ring','R8_3_3472']))
    stages += [(name,P/path,[])for name,path in [('complete_high_domain','domain/replay.py'),('complete_low_frames','domain/enumerate_low.py'),('phase_trace_atoms','frames/first_trace_atoms.py'),('all_frame_coverage','frames/replay.py'),('surviving_frame_gram','frames/frame42_gram.py'),('surviving_frame_twists','frames/frame42_sts_coeffs.py'),('source_derived_terminal_model','model/check.py')]]
stages += [(name,P/path,[])for name,path in [('independent_certificate_link','independent/link.py'),('terminal_rational_checker','terminal/check.py'),('independent_rational_checker','independent/verify.py')]]
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
dependencies={};results=[]
with tempfile.TemporaryDirectory(prefix='r3472-exclusion-replay-')as tmp:
    for name,script,args in stages:
        print('REPLAY',name,flush=True);start=time.monotonic();out=Path(tmp)/(name+'.json')
        subprocess.run([sys.executable,'-B','-u',str(P/'provenance/run_stage.py'),str(out),str(script),*args],cwd=ROOT,env=env,check=True)
        dependencies.update(json.loads(out.read_text()));results.append({'stage':name,'status':'PASS','seconds':round(time.monotonic()-start,3)})
summary={'schema':'r3472-exclusion-verification-v1','id':'R8_3_3472','status':'verified','conclusion':'no_complex_fusion_categorification','complete_general_categorification_exclusion':not(a.quick or a.skip_spherical),'canonical_tensor':'site/dist/downloads/fusion-tensors/R8_3_3472.txt','tensor_sha256':'33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a','complete_low_frames':372,'exact_span_exclusions':276,'source_automorphisms':9,'remaining_phase_orbits':12,'exact_phase_orbit_exclusions':11,'last_equivalent_frames':[42,117,304],'twist_orbit_types':424,'terminal_equations':628,'terminal_integer_variables':572,'exact_integer_bound_cuts':1648,'exact_positive_separation':'2717541156573712541191977062303/359103652930042901916159999600','independent_terminal_checker':'PASS','assertions_enabled_in_child_checks':True,'solver_used':False,'stages':results}
if a.write:
    (P/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    own=[]
    for directory in ['terminal','independent','domain','frames','model','provenance','optional_vipr']:
        own += [q for q in(P/directory).rglob('*')if q.is_file()and'__pycache__'not in q.parts]
    own += [P/'README.md',P/'replay.py',P/'verification.json']
    for q in own:dependencies[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
    ownnames={str(q.relative_to(ROOT))for q in own}
    manifest={'schema':'r3472-exclusion-proof-closure-v1','repository_relative_paths':True,'files':dict(sorted(dependencies.items())),'external_dependencies':sorted(set(dependencies)-ownnames),'proof_files':sorted(ownnames),'scope':'Complete replay input and code closure; publication overlays and manuscript files are owned separately.'}
    (P/'proof_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: complete exclusion replay.'if summary['complete_general_categorification_exclusion']else'PASS: requested replay subset.',flush=True)
