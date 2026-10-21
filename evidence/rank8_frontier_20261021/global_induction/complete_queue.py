"""Serial finite-domain completion; no mathematical result is inferred from exit status."""
from pathlib import Path
import json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
TARGETS=((1768,'atomic_real_sts'),(1795,'atomic_real_sts'),(1615,'sts_frame'),(1617,'sts_frame'),(1660,'sts_frame'),(1661,'sts_frame'),(903,'sts_frame'))
def main():
    start=time.monotonic();out={'status':'running','targets':[[f'R8_3_{n}',v] for n,v in TARGETS],'records':[]};dest=HERE/'complete_queue.json'
    def save():
        out['seconds']=round(time.monotonic()-start,3);tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(out,separators=(',',':'))+'\n');tmp.replace(dest)
    save()
    for n,variant in TARGETS:
        rid=f'R8_3_{n}';path=HERE/'complete_results'/f'{rid}_{variant}_h4.json';record={'id':rid,'variant':variant,'status':'running'};out['records'].append(record);save()
        existing=json.loads(path.read_text()) if path.exists() else None
        if not existing or existing.get('status') not in ('excluded','exact_feasible_relaxation'):
            answer=subprocess.run([sys.executable,str(HERE/'complete_phase_one.py'),'--ring',rid,'--variant',variant]);record['discovery_exit_code']=answer.returncode
        if path.exists():
            result=json.loads(path.read_text());record.update(status=result['status'],result_path=str(path.relative_to(HERE)),tensor_sha256=result['tensor_sha256'])
            if result['status'] in ('excluded','exact_feasible_relaxation'):
                replay=subprocess.run([sys.executable,'-O',str(HERE/'complete_phase_one.py'),'--verify',str(path)]);record['optimized_exact_replay']='PASS' if replay.returncode==0 else 'FAIL';record['replay_exit_code']=replay.returncode
        else:record['status']='missing_result'
        save();print('QUEUE',rid,record['status'],record.get('optimized_exact_replay'),flush=True)
    out['status']='all_serial_attempts_finished';save()
if __name__=='__main__':main()
