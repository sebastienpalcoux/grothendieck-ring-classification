"""Exact continuation for the verified rank-seven multiplicity-five band.

New identifiers follow appearance within the exact-multiplicity-five input band.
Earlier ledger entries are preserved verbatim. Discovery timeouts never exclude.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import argparse,collections,concurrent.futures,gzip,hashlib,json,signal,sys,time,traceback,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P));sys.path.insert(0,str(P/'software'))
OUT=P/'output/m5';OUT.mkdir(exist_ok=True)
def write(name,obj):
    target=OUT/name;tmp=target.with_suffix(target.suffix+'.tmp');tmp.write_text(json.dumps(obj,separators=(',',':'))+'\n');tmp.replace(target)
def ingest(source):
    from prepare import flatten
    old=json.loads((P/'output/rank7_ledger.json').read_text());old=[r for r in old if r['multiplicity']<=4]
    raw=[];transport=[];rows=[];exact={flatten(r['tensor']):r for r in old}
    with gzip.open(source,'rt') as f:
        for line,s in enumerate(f,1):
            R=json.loads(s.replace('{','[').replace('}',']'));v=flatten(R);m=max(v);raw.append(v)
            if m<5:
                if v not in exact:raise ValueError('Old-band representative changed')
                transport.append({'id':exact[v]['id'],'old_source_line':exact[v]['source_line'],'input_source_line':line})
            elif m==5:
                rid=f'R7_5_{len(rows)+1}'
                rows.append({'id':rid,'rank':7,'multiplicity':5,'source_line':4201+len(rows)+1,'input_source_line':line,'commutative':all(R[i][j]==R[j][i] for i in range(7) for j in range(i)),'status':'unresolved','criterion':None,'certificate':None,'model_names':[],'tensor':R})
                transport.append({'id':rid,'input_source_line':line,'source_line':rows[-1]['source_line']})
            else:raise ValueError('unexpected multiplicity')
    if len(rows)!=5805 or len(raw)!=10006 or len(set(raw))!=10006 or len(transport)!=10006:raise ValueError('source counts/duplicates')
    write('census.json',rows);write('source_transport.json',transport)
    write('source.json',{'input_path':'provenance/rank7_M5_verified/FusionRingMultiplicationTables.txt.gz','input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'old_ledger_sha256':hashlib.sha256((P/'output/rank7_ledger_through_m4.json').read_bytes()).hexdigest(),'old_band_records':4201,'new_band_records':5805,'identifier_convention':'R7_5_i follows appearance in exact multiplicity 5 of uploaded input; old records/identifiers retained.'})
    return rows
STAGES=('near_group','rank_two','zero_spectrum','lower_rank_subring','dnumber','subcategory_divisibility','cyclotomic','involution_module','field_automorphisms','oriented_dimension_order','general_induction','character','tensor_rotation','modular')
def worker(task):
    stage,row,budget=task;R=row['tensor'];start=time.monotonic()
    def alarm(*args):raise TimeoutError('finite discovery budget exhausted')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(budget)
    out={'id':row['id'],'stage':stage,'status':'survives'}
    try:
        from analyze import near_group_certificate,verify_own
        from check import verify
        if stage=='near_group':c=near_group_certificate(R)
        elif stage=='rank_two':c=next(({'kind':'rank_two','object':i,'multiplicity':R[i][i][i]} for i in range(1,7) if R[i][i][0]==1 and R[i][i][i]>=2 and sum(R[i][i])==1+R[i][i][i]),None)
        elif stage=='lower_rank_subring':
            from subring_descent import certificate;c=certificate(R)
        elif stage=='dnumber':
            from rings import dnumber;c=dnumber(R)
        elif stage=='subcategory_divisibility':
            from subring_descent import closed_subrings
            from proofs import subring_certificate
            c=subring_certificate(R) if row['commutative'] and next(closed_subrings(R),None) else None
        elif stage=='cyclotomic':
            from proofs import cyclotomic_failure
            from rings import matrices,t
            c=cyclotomic_failure([M.charpoly(t).as_poly() for M in matrices(R)]) if row['commutative'] else None
        elif stage=='involution_module':
            from involution_module import certificate;c=certificate(R) if row['commutative'] else None
        elif stage=='field_automorphisms':
            from field_automorphisms import certificate;c=certificate(R) if row['commutative'] else None
        elif stage=='oriented_dimension_order':
            c=pure_dimension_order(R,budget) if row['commutative'] else None
        elif stage=='general_induction':
            from oriented_extension import certificate;c=certificate(R,height=6,timeout=min(60,budget//2),integral=True) if row['commutative'] else None
        else:
            from advanced_criteria import general_certificate
            c=general_certificate(R,mode='dimension_order' if stage=='oriented_dimension_order' else stage,timeout=min(60,budget//2),height=6) if row['commutative'] else None
        if c:
            verify_own(R,c)
            out.update(status='excluded',certificate=c,exact_checked=True,scope='general_complex_fusion_category')
    except (TimeoutError,subprocess.TimeoutExpired) as e:out.update(status='budget_exhausted',diagnostic=str(e))
    except Exception as e:out.update(status='error',diagnostic=repr(e),traceback=traceback.format_exc())
    finally:signal.alarm(0)
    out['seconds']=time.monotonic()-start
    return out

def hard_worker(task):
    stage,row,budget=task;start=time.monotonic()
    cmd=[sys.executable]+([] if __debug__ else ['-O'])+[str(Path(__file__).resolve()),'--worker']
    with subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True) as proc:
        try:stdout,stderr=proc.communicate(json.dumps(task,separators=(',',':')),timeout=budget)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL);proc.communicate()
            return {'id':row['id'],'stage':stage,'status':'budget_exhausted','diagnostic':'Independent process-group watchdog expired; no exclusion.','seconds':time.monotonic()-start}
        if proc.returncode!=0:return {'id':row['id'],'stage':stage,'status':'error','diagnostic':'Worker exit '+str(proc.returncode),'stderr':stderr[-2000:],'seconds':time.monotonic()-start}
        out=json.loads(stdout)
        if out.get('id')!=row['id'] or out.get('stage')!=stage:raise ValueError('subprocess identity mismatch')
        return out

def pure_dimension_order(R,budget):
    # First test only inexpensive exact spherical-character obstructions.
    # A missing branch returns None; it never implies nonexistence.
    from rings import Characters
    from exact import pc
    import proofs,dimension_order,advanced_criteria
    a=Characters(R);branches=[]
    for f,m in a.components:
        K,ds,D,pD=a.component(f)
        zero=next((i for i,d in enumerate(ds) if not d),None)
        unequal=next((i for i in range(a.n) if ds[i]!=ds[a.du[i]]),None)
        if zero is not None:why={'kind':'zero','object':zero}
        elif unequal is not None:why={'kind':'duality','object':unequal}
        else:why=(proofs.norm_failure(pD,a.cf) or proofs.field_failure(f,a.cf) or dimension_order.certificate(a,f) or proofs.spherical_global_moment(a,f))
        if why is None:return None
        branches.append({'factor':pc(f),'obstruction':why})
    sphere={'kind':'spherical','generator':a.k,'characters':branches,'pseudo':None}
    return advanced_criteria._complete_oriented_lift(R,sphere,min(60,budget//2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--jobs',type=int,default=4);ap.add_argument('--through',choices=STAGES,default='field_automorphisms');ap.add_argument('--budget',type=int,default=120);args=ap.parse_args()
    rows=ingest(args.source) if args.source else json.loads((OUT/'census.json').read_text())
    records={r['id']:r for r in rows};ledger=OUT/'attempts.jsonl';completed=OUT/'stages.json'
    stages=json.loads(completed.read_text()) if completed.exists() else []
    if ledger.exists():
        for s in ledger.read_text().splitlines():
            z=json.loads(s)
            if z['status']=='excluded':records[z['id']].update(status='excluded',criterion=z['stage'],certificate=z['certificate'])
    additions=OUT/'additions.json'
    if additions.exists():
        for addition in json.loads(additions.read_text()):
            if records[addition['id']]['status']=='unresolved':records[addition['id']].update(addition)
    for stage in STAGES[:STAGES.index(args.through)+1]:
        if stage in [x['stage'] for x in stages]:continue
        active=[r for r in records.values() if r['status']=='unresolved'];results=[];start=time.monotonic()
        progress=OUT/(stage+'.progress.jsonl')
        if progress.exists():
            recovered={z['id']:z for z in (json.loads(line) for line in progress.read_text().splitlines())}
            results=[recovered[r['id']] for r in active if r['id'] in recovered]
            active=[r for r in active if r['id'] not in recovered]
        entered=len(active)+len(results)
        print('START',stage,'pending',len(active),'recovered',len(results),flush=True)
        if stage=='zero_spectrum':
            from analyze import spectrum_batch
            results=[{'id':r['id'],'stage':stage,'status':'excluded' if c else 'survives',**({'certificate':c,'exact_checked':True,'scope':'all_characteristics'} if c else {})} for r,c in zip(active,spectrum_batch(active))]
        else:
            expensive=stage in ('oriented_dimension_order','general_induction','character','tensor_rotation','modular')
            executor=concurrent.futures.ThreadPoolExecutor if expensive else concurrent.futures.ProcessPoolExecutor
            operation=hard_worker if expensive else worker
            with executor(max_workers=args.jobs) as pool:
                pending=[pool.submit(operation,(stage,r,args.budget)) for r in active]
                for future in concurrent.futures.as_completed(pending):
                    z=future.result()
                    results.append(z)
                    with (OUT/(stage+'.progress.jsonl')).open('a') as pf:pf.write(json.dumps(z,separators=(',',':'))+'\n')
                    if len(results)%20==0:print('PROGRESS',stage,len(results),'/',len(active),flush=True)
                    if z['status'] in ('error','budget_exhausted'):print(z['id'],z['status'],z.get('diagnostic'),flush=True)
        with ledger.open('a') as f:
            for z in results:
                f.write(json.dumps(z,separators=(',',':'))+'\n')
                if z['status']=='excluded':records[z['id']].update(status='excluded',criterion=stage,certificate=z['certificate'])
        count=collections.Counter(z['status'] for z in results);stageinfo={'stage':stage,'entered':entered,'counts':dict(count),'seconds':time.monotonic()-start};stages.append(stageinfo);write('stages.json',stages);write('ledger.json',list(records.values()));write('survivors.json',[r for r in records.values() if r['status']=='unresolved']);print('DONE',stageinfo,'survivors',sum(r['status']=='unresolved' for r in records.values()),flush=True)
if __name__=='__main__':
    if '--worker' in sys.argv:print(json.dumps(worker(json.load(sys.stdin)),separators=(',',':')))
    else:main()
