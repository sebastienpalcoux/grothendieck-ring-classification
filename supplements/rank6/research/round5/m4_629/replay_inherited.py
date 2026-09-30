"""Source-bound optimizer-free replay of the complete inherited R629 reduction.

Historical inputs and receipts are read only. The fixed-twist stage writes
inside an automatically removed temporary directory at the same package depth.
"""
import contextlib,hashlib,io,json,runpy,shutil,signal,sys,tempfile,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
def denied(*a,**k):raise RuntimeError('numerical optimization forbidden in inherited replay')
op.linprog=op.milp=denied
from exact import require
import galois_pseudo_reduction as G
import round4_quartic_profiles as Q

def main():
    start=time.monotonic();old=P/'research/round4/m4_629';here=Path(__file__).parent
    def stop(*a):raise TimeoutError('inherited replay exceeded explicit840second budget')
    signal.signal(signal.SIGALRM,stop);signal.alarm(840)
    inputs=[P/'data/unresolved_tensors.json']+[old/name for name in ('general_reduction.json','R6_4_629_exact_profiles.json','filtered_profiles.json','fixed_twist_h6.json','fixed_twist_h6_lab1.json')]
    original_hashes={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs}
    R=next(r['N'] for r in json.loads(inputs[0].read_text()) if r['id']=='R6_4_629');checks={}
    checks['general_reduction']=G.verify(R,json.loads((old/'general_reduction.json').read_text())['certificate']);print('general reduction verified',flush=True)
    cert=json.loads((old/'R6_4_629_exact_profiles.json').read_text())['certificate'];checks['exact_profiles']=Q.verify(R,cert);print('seven low frames and complete profile enumeration verified',flush=True)
    exploratory=json.loads((old/'filtered_profiles.json').read_text());branch=cert['branches'][exploratory['low_frame']]
    require(branch['high_vectors']==exploratory['vectors'],'canonical/exploratory column domains differ')
    expected={tuple(v) for v in exploratory['counts']};require(len(expected)==len(exploratory['counts'])==5,'exploratory profiles duplicate or missing')
    require(len(branch['gram_galois_profiles'])==784,'wrong complete profile cardinality')
    require(len(branch['cases'])==2,'missing canonical low labelling')
    for case in branch['cases']:require({tuple(v['counts']) for v in case['survivors']}==expected,'canonical/exploratory full-vector bridge failed')
    checks['profile_bridge']=dict(full_count_vectors=5,column_dimension=85,canonical_labellings=len(branch['cases']),passed=True)
    with tempfile.TemporaryDirectory(dir=here.parent,prefix='m4_629_inherited_replay_') as name:
        tmp=Path(name)
        for filename in ('replay_fixed_twists.py','filtered_profiles.json','fixed_twist_h6.json','fixed_twist_h6_lab1.json'):shutil.copy2(old/filename,tmp/filename)
        with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(tmp/'replay_fixed_twists.py'),run_name='__main__')
        report=json.loads((tmp/('fixed_twist_exact_replay_O.json' if not __debug__ else 'fixed_twist_exact_replay.json')).read_text())
        require(report['passed'] and report['optimizer_used'] is False,'fixed-twist replay did not pass')
        actual_labs=[x['lab'] for x in report['reports']];require(actual_labs==branch['labellings'],'fixed-twist stage omits a canonical labelling')
        rays=[p for r in report['reports'] for p in r['profiles'] if p['outcome']=='exact_linear_obstruction'];require(len(rays)==7 and all(p['passed'] for p in rays),'incomplete exact profile/label rejection')
        retained=[p['rank'] for p in report['reports'][0]['profiles'] if p['outcome']!='exact_linear_obstruction'];require(sorted(retained)==[30,35,38],'unexpected inherited frontier')
        checks['fixed_twists']=dict(reports=report['reports'],exact_rays=len(rays),retained_ranks=sorted(retained),passed=True)
    require(all(hashlib.sha256((P/name).read_bytes()).hexdigest()==digest for name,digest in original_hashes.items()),'historical inputs changed during replay')
    sources={Path(__file__).resolve(),old/'replay_fixed_twists.py'}
    for module in sys.modules.values():
        filename=getattr(module,'__file__',None)
        if filename:
            f=Path(filename).resolve()
            if f.is_relative_to(P/'software') and f.suffix=='.py':sources.add(f)
    result=dict(id='R6_4_629',passed=True,optimizer_used=False,optimized_python=not __debug__,scope='general_sphericalization_and_all_inherited_low_frames_profiles_and_labellings',checks=checks,sources={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(sources)},inputs=original_hashes,elapsed_seconds=round(time.monotonic()-start,3))
    (here/'inherited_replay_O.json').write_text(json.dumps(result,indent=2)+'\n');signal.alarm(0);print({'passed':True,'elapsed_seconds':result['elapsed_seconds'],'retained_ranks':retained},flush=True)

if __name__=='__main__':main()
