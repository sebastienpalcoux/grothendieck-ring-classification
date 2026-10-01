"""Source-bound, resumable execution of existing criteria on exact multiplicity nine.

This campaign never changes/replays certificates for multiplicities one to eight.
Run bounded chunks, for example:
  timeout 890 python software/classify_m9.py --jobs 6 --seconds 840 --resume
Every accepted witness is exactly checked by the existing dispatcher. Timeouts,
errors and survival only retain a tensor. Completed stages and partial stages are
bound to the complete imported census and exact input tensor digest.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse, collections, hashlib, json, platform, time
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
import classify
P=Path(__file__).resolve().parents[1]
BASE=P/'verification/m9/classification'
STAGES=classify.STAGES[:11]+[('cheap_arithmetic_early','Early exact arithmetic and Morita continuations',300)]+classify.STAGES[11:-1]+[('module_dual_gram','Dual module Gram continuation',150)]

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def atomic_text(path,value):
    temporary=path.with_name(path.name+'.tmp')
    temporary.write_text(value);os.replace(temporary,path)
def write(path,value):atomic_text(path,json.dumps(value,indent=2)+'\n')

def module_worker(task):
    from continuation_campaign import bounded
    row=task[3]
    return bounded((row,'module_dual_gram'),task[2])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs',type=int,default=6)
    ap.add_argument('--seconds',type=int,default=840)
    ap.add_argument('--resume',action='store_true')
    ap.add_argument('--through',default=None,choices=[x[0] for x in STAGES])
    args=ap.parse_args()
    if args.jobs<1 or not 1<=args.seconds<=840:ap.error('jobs positive and seconds in 1..840 required')
    # Fail before creating a campaign if required mathematical dependencies are missing.
    import sympy,scipy,numpy,flint
    started=time.monotonic();deadline=started+args.seconds
    rows=[r for r in json.loads((P/'data/census.json').read_text()) if r['m']==9]
    if len(rows)!=8809:raise ValueError('M9 requires exactly 8,809 new tensors')
    fingerprint=digest(P/'data/census.json')
    input_hash=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
    BASE.mkdir(parents=True,exist_ok=True)
    identity={'census_sha256':fingerprint,'input_sha256':input_hash,'input_count':len(rows),'multiplicity':9}
    state_path=BASE/'stages.json';ledger=BASE/'attempts.jsonl'
    if state_path.exists():
        if not args.resume:raise ValueError('existing M9 campaign: use --resume')
        state=json.loads(state_path.read_text())
        if state['identity']!=identity:raise ValueError('campaign source changed')
    else:
        from import_repository import verify_source
        source=verify_source()
        state={'identity':identity,'source':source,'python':platform.python_version(),'stages':[]}
        write(state_path,state)
        write(BASE/'input_manifest.json',dict(identity,ids=[r['id'] for r in rows],
              scope='New exact-multiplicity-nine source tensors only. Previous proofs are retained unchanged.'))
        ledger.write_text('')
    completed={x['stage'] for x in state['stages']};exclusions={};remaining={r['id']:r for r in rows}
    existing={}
    for line in ledger.read_text().splitlines():
        record=json.loads(line);existing.setdefault(record['stage'],[]).append(record)
    committed=[]
    # Immutable completed-stage files and their digests prevent a delayed file
    # synchronization from silently dropping an earlier committed stage.
    for position,report in enumerate(state['stages']):
        stage=report['stage']
        if position>=len(STAGES) or stage!=STAGES[position][0]:raise ValueError('completed stage order changed')
        frozen=P/report['attempts_file'] if report.get('attempts_file') else None
        if frozen is not None:
            payload=frozen.read_bytes()
            if hashlib.sha256(payload).hexdigest()!=report['attempts_sha256']:raise ValueError('completed stage checkpoint checksum mismatch')
            records=[json.loads(line) for line in payload.splitlines()]
        else:
            records=existing.get(stage,[])
            payload=''.join(json.dumps(r,separators=(',',':'))+'\n' for r in records).encode()
            if report.get('attempts_sha256') and hashlib.sha256(payload).hexdigest()!=report['attempts_sha256']:raise ValueError('canonical completed-stage checksum mismatch')
        if len(records)!=len(remaining) or {r['id'] for r in records}!=set(remaining):raise ValueError('completed stage coverage mismatch: '+stage)
        for record in records:
            if record.get('stage')!=stage or record.get('census_sha256')!=fingerprint:raise ValueError('completed stage source mismatch')
            if record['status']=='excluded':
                if record.get('exact_checked') is not True or not isinstance(record.get('certificate'),dict):raise ValueError('unchecked completed exclusion')
                exclusions[record['id']]=record;remaining.pop(record['id'])
            committed.append(json.dumps(record,separators=(',',':')))
        removed=sum(r['status']=='excluded' for r in records)
        if (report['entered'],report['removed'],report['remaining'])!=(len(records),removed,len(remaining)):raise ValueError('completed stage count mismatch: '+stage)
    atomic_text(ledger,''.join(line+'\n' for line in committed))
    early_path=P/'verification/m9/early_arithmetic_certificates.jsonl'
    early={}
    if early_path.exists():
        byid={r['id']:r for r in rows}
        for line in early_path.read_text().splitlines():
            record=json.loads(line);rid=record['id']
            if rid in early or rid not in byid or record.get('status')!='excluded' or record.get('exact_checked') is not True:raise ValueError('invalid early arithmetic proof')
            tensor_hash=hashlib.sha256(json.dumps(byid[rid]['N'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if record.get('tensor_sha256')!=tensor_hash:raise ValueError('early arithmetic tensor changed')
            early[rid]=record['certificate']
    cert_path=P/'certificates/m9_classification.jsonl'
    def export():
        atomic_text(cert_path,''.join(json.dumps(exclusions[r['id']],separators=(',',':'))+'\n' for r in rows if r['id'] in exclusions))
        write(BASE/'summary.json',dict(identity,completed_stages=len(completed),
              stages_total=len(STAGES),complete=len(completed)==len(STAGES),excluded=len(exclusions),
              positive=0,unresolved=len(remaining),unresolved_ids=list(remaining),
              certificates_sha256=digest(cert_path),errors=sum(s['errors'] for s in state['stages']),
              budget_exhausted=sum(s['budget_exhausted'] for s in state['stages']),
              interpretation='Only exact checked certificates exclude; unfinished stages, errors, exhausted discovery budgets, and survivors remain unresolved.'))
        write(BASE/'residual_tensors.json',list(remaining.values()))
    for stage_number,(stage,label,budget) in enumerate(STAGES):
        if args.through and stage_number>[x[0] for x in STAGES].index(args.through):break
        if stage in completed:continue
        active=list(remaining.values());progress=BASE/(stage+'.progress.jsonl');outputs={}
        if progress.exists():
            lines=progress.read_text().splitlines()
            for number,line in enumerate(lines):
                try:out=json.loads(line)
                except json.JSONDecodeError:
                    if number!=len(lines)-1:raise ValueError('damaged nonterminal checkpoint line')
                    atomic_text(progress,''.join(x+'\n' for x in lines[:number]));break
                if out.get('census_sha256')!=fingerprint or out.get('stage')!=stage or out.get('id') not in remaining:
                    raise ValueError('partial checkpoint source/stage mismatch')
                if out['status']=='excluded' and not out.get('exact_checked'):raise ValueError('unchecked partial exclusion')
                outputs[out['id']]=out
        tasks=[(stage,label,budget,dict(row,_advanced_repeat=True,_general_discover=True),early.get(row['id']) if stage=='cheap_arithmetic_early' else None,False)
               for row in active if row['id'] not in outputs]
        print('START',stage,'entered',len(active),'checkpoint',len(outputs),'pending',len(tasks),flush=True)
        stage_start=time.monotonic()
        if stage=='zero_spectrum' and tasks:
            if time.monotonic()+130>=deadline:export();return
            import zero_spectrum
            batch_start=time.monotonic();cs=zero_spectrum.batch([t[3]['N'] for t in tasks]);elapsed=time.monotonic()-batch_start
            with progress.open('a') as stream:
                for task,cert in zip(tasks,cs):
                    row=task[3];out=dict(id=row['id'],m=9,stage=stage,status='excluded' if cert else 'survives',seconds=elapsed/len(tasks),census_sha256=fingerprint)
                    if cert:out.update(certificate=cert,exact_checked=True,witness_source='discovered')
                    outputs[row['id']]=out;stream.write(json.dumps(out,separators=(',',':'))+'\n')
                stream.flush()
        elif tasks:
            expensive=stage in ('general_induction','cheap_arithmetic_early','dimension_order','character','tensor_rotation','modular','module_dual_gram')
            executor=ThreadPoolExecutor if expensive else ProcessPoolExecutor
            operation=module_worker if stage=='module_dual_gram' else classify.hard_worker if expensive else classify.worker
            iterator=iter(tasks);done_count=0
            with progress.open('a') as stream,executor(max_workers=args.jobs) as pool:
                pending={}
                def submit():
                    if time.monotonic()+budget+8>=deadline:return False
                    task=next(iterator,None)
                    if task is None:return False
                    pending[pool.submit(operation,task)]=task[3]['id'];return True
                for _ in range(args.jobs):submit()
                while pending:
                    done,_=wait(pending,return_when=FIRST_COMPLETED)
                    for future in done:
                        pending.pop(future);out=future.result();out['census_sha256']=fingerprint
                        outputs[out['id']]=out;stream.write(json.dumps(out,separators=(',',':'))+'\n');stream.flush()
                        done_count+=1
                        if done_count%100==0 or out['status'] in ('error','budget_exhausted'):
                            print(stage,len(outputs),'/',len(active),out['id'],out['status'],out.get('diagnostic',''),flush=True)
                        submit()
        if len(outputs)!=len(active):
            print('CHECKPOINT',stage,len(outputs),'/',len(active),'command allowance nearly exhausted',flush=True)
            export();return
        report=dict(stage=stage,label=label,entered=len(active),removed=sum(x['status']=='excluded' for x in outputs.values()),
            remaining=len(active)-sum(x['status']=='excluded' for x in outputs.values()),
            worker_seconds=sum(x['seconds'] for x in outputs.values()),final_chunk_wall_seconds=time.monotonic()-stage_start,
            errors=sum(x['status']=='error' for x in outputs.values()),budget_exhausted=sum(x['status']=='budget_exhausted' for x in outputs.values()),
            statuses=dict(collections.Counter(x['status'] for x in outputs.values())),jobs=args.jobs)
        additions=[]
        for row in active:
            out=outputs[row['id']];additions.append(json.dumps(out,separators=(',',':'))+'\n')
            if out['status']=='excluded':exclusions[out['id']]=out;remaining.pop(out['id'],None)
        completed_path=BASE/'completed'/(stage+'.jsonl');completed_path.parent.mkdir(exist_ok=True)
        stage_text=''.join(additions);atomic_text(completed_path,stage_text)
        report['attempts_file']=str(completed_path.relative_to(P));report['attempts_sha256']=hashlib.sha256(stage_text.encode()).hexdigest()
        if stage=='cheap_arithmetic_early':report['source_proofs_sha256']=digest(early_path)
        committed.extend(line.rstrip('\n') for line in additions)
        atomic_text(ledger,''.join(line+'\n' for line in committed))
        state['stages'].append(report);write(state_path,state);completed.add(stage);progress.unlink(missing_ok=True)
        print('DONE',json.dumps(report),flush=True);export()
        if args.through==stage:return
    export()
    print(json.dumps(json.loads((BASE/'summary.json').read_text()),indent=2),flush=True)

if __name__=='__main__':main()
