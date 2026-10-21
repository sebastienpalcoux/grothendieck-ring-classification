"""Replay accepted M3 evidence and bind its immutable publication ledger.

An optimized invocation explicitly starts an assertion-enabled child for
inherited proof routines. It never silently disables their checks.
"""
from __future__ import annotations
import argparse,concurrent.futures,gzip,hashlib,json,os,subprocess,sys,tempfile,time
from pathlib import Path
from m3_campaign import REPO,P,OUT,require,RAW_SHA,OLD_SHA,sha,read_tables
from finalize_m3 import reconcile,digest,validate_receipts
EVIDENCE=OUT.parent

def source_inventory():
    paths={OUT/name for name in ('census_m3.json','decisions_m3.json','survivors_m3.json','survivor_profiles.json','source_manifest.json','input_manifest.json','residual_attempts.json','residual_audit.json','one_spectrum_m3.json','frobenius_results.json','graded_extensions_attempt.json','dimension42_group_types.json','dimension84_obstruction.json','source_transport.json','unified_scope_attempts.json') if (OUT/name).exists()}
    paths.update(P/'data'/name for name in ('decisions.json','rank8_tables.txt.gz','rank8_m3_tables.txt.gz','lower_rank_positive_models.json','rank6_positive_models.json','rank7_certified_negative_subrings.json') if (P/'data'/name).exists())
    paths.update(REPO/name for name in ('supplements/rank6/data/census.json','supplements/rank6/data/decisions.json','supplements/rank7/output/rank7_ledger.json'))
    for folder in ('criteria','models','noncommutative','performance','publication'):
        for path in (EVIDENCE/folder).rglob('*.json'):
            if any(word in path.name for word in ('progress','replay')):continue
            paths.add(path)
    paths.update(OUT.glob('attempts*.jsonl'))
    paths.update((OUT/'literature').glob('*'))
    paths.update((EVIDENCE/'performance/group_scan').glob('*.jsonl'))
    paths.update((EVIDENCE/'performance/group_scan').glob('*.g'))
    return {str(p.relative_to(REPO)):sha(p) for p in sorted(paths) if p.is_file()}

def code_inventory():
    roots=[P/'software',P/'experimental_signed',EVIDENCE,REPO/'supplements/rank6/software',REPO/'supplements/rank7/software']
    paths={p for base in roots for p in base.rglob('*') if p.is_file() and p.suffix in ('.py','.cpp','.h','.hpp','.sage','.md','.tex')}
    return {str(p.relative_to(REPO)):sha(p) for p in sorted(paths)}

def commands():
    normal=sys.executable
    required=[('baseline',[normal,str(P/'software/verify_m3.py')]),
              ('criteria',[normal,str(EVIDENCE/'criteria/accepted.py'),'--verify','--workers','2']),
              ('models',[normal,str(EVIDENCE/'models/verify_models.py')])]
    for name,relative,arguments in [
        ('noncommutative_scalar','noncommutative/scalar_sieve.py',[]),
        ('noncommutative_weighted','noncommutative/weighted_rank8.py',[]),
        ('unitary_only_primary_three','noncommutative/unitary_primary3.py',[]),
        ('weak_group_unitarity_lifts','noncommutative/weak_group_positivity.py',[]),
        ('general_biquadratic_trace_validation','noncommutative/verify_general_biquadratic_traces.py',[]),
        ('general_global_polynomial_validation','noncommutative/verify_general_global_polynomial.py',[]),
        ('global_duality_contraction_validation','criteria/verify_global_duality.py',[]),
        ('global_phase_one_exact_ray_validation','criteria/verify_global_phase_one.py',[]),
        ('pseudo_unitary_central_twist_moments','noncommutative/central_moments.py',[]),
        ('central_twist_moment_independent_validation','noncommutative/verify_central_moments.py',[]),
        ('split_module_independent','noncommutative/verify_split_module_independent.py',[]),
        ('dimension84_structural_obstruction','pipeline/dimension84_obstruction.py',[]),
        ('model_search_attempts','models/model_search_audit.py',[]),
        ('quantum_model_family_attempts','models/quantum_model_attempts.py',[]),
        ('exact_f4_model_family_attempt','models/psl2_11/f4_level3_attempt.py',[]),
        ('izumi_xu_inversion_unitary_obstruction','models/r436_inversion_attempt.py',[]),
        ('haagerup_extension_unitary_obstruction','models/r455_haagerup_extension.py',[]),
        ('odd_hi_near_group_Morita_model_filter','models/fresh_202609/verify_odd_hi_dimension_filter.py',[]),
        ('asaeda_haagerup_model_family_filter','models/asaeda_haagerup_attempt.py',[]),
        ('literature_f660_identity','pipeline/literature/f660_match.py',['--verify']),
        ('native_enumeration_validation','performance/verify_native.py',[]),
        ('native_bottleneck_validation','performance/verify_benchmarks.py',[]),
        ('exact_low_failure_validation','performance/verify_low_failure.py',['--real-fixtures',str(EVIDENCE/'performance/low_failure_real_fixtures.json')]),
        ('group_scan_transcript_audit','performance/group_scan/summarize_scan.py',['--check'])]:
        script=EVIDENCE/relative
        required.append((name,[normal,str(script),*arguments]))
    for name,script,args in [('one_spectrum_attempts','one_spectrum_m3.py',['--verify']),('strong_frobenius_attempts','m3_frobenius.py',['--verify']),('unified_scoped_attempts','m3_unified_scope_audit.py',[]),('residual_effort_audit','m3_residual_audit.py',[])]:
        path=P/'software'/script
        required.append((name,[normal,str(path),*args]))
    return required

def output_locations(output,marker):
    canonical=OUT/('continuation_replay_optimized_invocation.json' if marker=='-O' else 'continuation_replay.json')
    output=output or canonical
    reserved={ (OUT/name).resolve() for name in ('continuation_replay.json','continuation_replay_optimized_invocation.json') }
    require(output.resolve() not in reserved or output.resolve()==canonical.resolve(),'receipt path belongs to the other replay lane')
    isolated=output.resolve()!=canonical.resolve()
    logroot=output.resolve().parent/(output.stem+'_logs') if isolated else OUT
    return output,logroot,isolated

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only',action='store_true');parser.add_argument('--output',type=Path)
    parser.add_argument('--jobs',type=int,default=2)
    args=parser.parse_args();ledger,summary=reconcile()
    marker=os.environ.get('M3_REPLAY_REQUESTED_OPTIMIZATION','normal')
    if args.metadata_only:
        if args.output:require(args.output.resolve() not in {(OUT/name).resolve() for name in ('continuation_replay.json','continuation_replay_optimized_invocation.json')},'metadata report cannot overwrite a full mathematical replay receipt')
        published=P/'output/m3/ledger.json';require(published.exists(),'published M3 ledger missing')
        require(json.loads(published.read_text())==ledger,'published M3 ledger differs from accepted evidence')
        normal,optimized=validate_receipts(ledger)
        require(normal['source_manifests_sha256']==source_inventory(),'metadata source inventory differs')
        require(normal['proof_source_sha256']==code_inventory(),'metadata proof inventory differs')
        expected={name for name,_ in commands()}
        require(all({item['section'] for item in report['sections']}==expected for report in (normal,optimized)),'full replay section coverage differs')
        raw=gzip.decompress((P/'data/rank8_m3_tables.txt.gz').read_bytes());require(hashlib.sha256(raw).hexdigest()==RAW_SHA,'source tensor hash mismatch')
        require(sha(P/'data/decisions.json')==OLD_SHA,'historical decisions changed')
        report={'status':'METADATA_PASS','mathematical_replay_performed':False,'ledger_digest':digest(ledger),
                'ledger_sha256':sha(published),'counts':summary['counts'],'historical_decisions_preserved':973,
                'new_band_count':3527,'source_tensor_uncompressed_sha256':RAW_SHA,
                'full_replay_receipt_sha256':sha(OUT/'continuation_replay.json'),
                'optimized_full_replay_receipt_sha256':sha(OUT/'continuation_replay_optimized_invocation.json'),
                'source_manifests_sha256':normal['source_manifests_sha256'],'proof_source_sha256':normal['proof_source_sha256']}
        if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2));return
    sources=source_inventory();code=code_inventory();start=time.monotonic();cmds=commands()
    for name,cmd in cmds:require(Path(cmd[1]).is_file(),'missing required proof implementation: '+name)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    # Custom output locations are isolated validation runs. Their logs must not
    # overwrite the fixed publication logs bound by a previously released receipt.
    output,logroot,isolated=output_locations(args.output,marker)
    logroot.mkdir(parents=True,exist_ok=True)
    def run(item):
        name,cmd=item;print('REPLAY',name,flush=True);tic=time.monotonic()
        result=subprocess.run(cmd,cwd=REPO,env=env,capture_output=True,text=True)
        lane='_optimized_invocation' if marker=='-O' else ''
        log=logroot/('replay_'+name+lane+'.log');log.write_text(result.stdout+result.stderr)
        require(result.returncode==0,'failed exact replay '+name+': '+str(log))
        print('PASS',name,flush=True)
        logref=str(log) if isolated else str(log.relative_to(REPO))
        return {'section':name,'status':'PASS','seconds':round(time.monotonic()-tic,6),'log':logref,'log_sha256':sha(log)}
    sections=[run(cmds[0])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:sections.extend(pool.map(run,cmds[1:]))
    require(source_inventory()==sources,'proof manifests added, removed or changed during replay')
    require(code_inventory()==code,'proof sources added, removed or changed during replay')
    final,_=reconcile();require(final==ledger,'accepted ledger changed during replay')
    report={'status':'PASS','result':'PASS','receipt_scope':'isolated_validation' if isolated else 'publication',
            'ledger_digest':digest(ledger),'counts':summary['counts'],'source_manifests_sha256':sources,
            'proof_source_sha256':code,'sections':sections,'seconds':round(time.monotonic()-start,6),
            'requested_optimization':marker,'invocation_optimization_requested':marker,
            'proof_interpreter_assertions_enabled':__debug__}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    if not __debug__:
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['M3_REPLAY_REQUESTED_OPTIMIZATION']='-O'
        raise SystemExit(subprocess.run([sys.executable,__file__,*sys.argv[1:]],env=env).returncode)
    main()
