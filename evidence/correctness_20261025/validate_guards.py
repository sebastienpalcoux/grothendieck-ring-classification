#!/usr/bin/env python3
"""Focused mutation controls for current native caching and replay outcomes."""
from pathlib import Path
import argparse,contextlib,copy,hashlib,importlib.util,io,json,os,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=False);out=a.output_dir.resolve()
    path=ROOT/'supplements/rank6/software/native_build.py';spec=importlib.util.spec_from_file_location('current_native_build_control',path);native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    helpers=list((ROOT/'supplements').rglob('native_build.py'))+list((HERE/'source_overrides').rglob('native_build.py'))
    need(all(p.read_bytes()==path.read_bytes()for p in helpers),'native cache helper copies differ')
    import subprocess
    with tempfile.TemporaryDirectory(prefix='native-binding-controls-')as tmp:
        work=Path(tmp);source=work/'probe.cpp';exe=work/'probe';source.write_text('#include <iostream>\n#ifndef VALUE\n#define VALUE 1\n#endif\nint main(){std::cout<<VALUE;}\n')
        def value(flags=('-O2','-std=c++17')):return subprocess.check_output([str(native.ensure_native(source,exe,flags))],text=True)
        need(value()=='1','initial fresh build');receipt=exe.with_name('probe.build.json');first=receipt.read_bytes();need(value()=='1'and receipt.read_bytes()==first,'bound cache reuse')
        exe.write_bytes(b'broken cache');need(value()=='1','corrupted native artifact reused')
        t=source.stat().st_mtime_ns;source.write_text(source.read_text().replace('VALUE 1','VALUE 2'));os.utime(source,ns=(t,t));need(value()=='2','source content ignored when timestamp unchanged')
        need(value(('-O2','-std=c++17','-DVALUE=3'))=='3','changed build flags ignored')
        receipt.unlink();exe.unlink()
        with ThreadPoolExecutor(max_workers=2)as pool:values=list(pool.map(lambda _:value(),range(2)))
        need(values==['2','2'],'concurrent source-bound build failed')
    st=ROOT/'evidence/rank8_frontier_20261021';sys.path.insert(0,str(st/'quadratic'));spec=importlib.util.spec_from_file_location('corrected_atomic_integer_control',HERE/'replay_atomic_integer.py');J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
    from features import System
    S=System(columns=((1,),(1,)),rhs=(1,),bounds=(1,1),row_labels=(('control',),),column_labels=(('x',),('y',)),metadata={'kind':'exact_two_variable_control'})
    source={'id':'CONTROL','tensor_sha256':'explicit_control_not_a_census_tensor'};pins={'control':'x+y=1; x,y in {0,1}'}
    b=J.box.propagate(S);compact=J.equations.compact(J.box.reduced(S,b))
    base={'source_sha256':pins,'tensor_sha256':source['tensor_sha256'],'support_filter':{},'system_metadata':S.metadata,'modular_tests':[J.modular(S,p)for p in(2,3)],'box':b,'compact_metadata':compact.metadata,'Hermite':J.hermite(compact),'original_integer_witness':[1,0],'outcome':'exact_nonnegative_integer_witness','completed_exact_scopes':['complete_source_domain','missing_conjugate_support_closure','joint_Galois_support_and_balance','modulo_2_and_3','finite_box_propagation','signed_integer_lattice_membership']}
    tests=[('valid_positive',{},True),('false_obstruction',{'outcome':'pseudo_unitary_integer_obstruction'},False),('omitted_modular',{'modular_tests':[]},False),('wrong_scope',{'completed_exact_scopes':[]},False),('bad_witness',{'original_integer_witness':[0,0]},False)]
    old=(J.HERE,J.construct,J.source_pins);results=[]
    try:
        with tempfile.TemporaryDirectory(prefix='atomic-guard-controls-')as tmp:
            J.HERE=Path(tmp);J.construct=lambda index:(source,{},S);J.source_pins=lambda:pins
            for name,updates,expected in tests+[(name,{},False)for name in('missing_Hermite','missing_outcome')]:
                changed=copy.deepcopy(base);changed.update(updates)
                if name=='missing_Hermite':changed.pop('Hermite')
                if name=='missing_outcome':changed.pop('outcome')
                (J.HERE/'joint_atomic_integer_65_results.json').write_text(json.dumps(J.st.encode(changed)))
                try:
                    with contextlib.redirect_stdout(io.StringIO()):J.run(65)
                    accepted=True;reason=None
                except (ValueError,RuntimeError,KeyError)as exc:accepted=False;reason=str(exc)
                need(accepted==expected,'terminal validation control failed: '+name);results.append({'case':name,'accepted':accepted,'expected':expected,'reason':reason})
    finally:J.HERE,J.construct,J.source_pins=old
    receipt={'status':'PASS','native_cache':{'helper_copies':len(helpers),'sources':{str(p.relative_to(ROOT)):sha(p)for p in helpers},'fresh_build_reuse_corruption_content_flags_concurrency':'PASS'},'atomic_terminal_guard':{'source_sha256':sha(HERE/'replay_atomic_integer.py'),'controls':results},'scope':'Focused exact acceptance-logic and cache-binding controls; toy system does not claim a new ring exclusion.'}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
