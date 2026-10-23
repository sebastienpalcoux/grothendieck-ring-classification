#!/usr/bin/env python3
"""Offline case-specific exclusion discovery with resumable solver checkpoints."""
import argparse, datetime, gzip, hashlib, importlib, json, math, os, platform, signal, subprocess, sys, time, traceback, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASES=["R8_3_928","R8_3_941","R8_3_1154","R8_3_1768"]
ADAPTERS={"R8_3_928":"cases.r928_r941","R8_3_941":"cases.r928_r941","R8_3_1154":"cases.r1154","R8_3_1768":"cases.r1768"}
DONE={"MODEL_INFEASIBLE_CERTIFIED","CERTIFIED_INFEASIBLE","INFEASIBLE_CERTIFIED","FEASIBLE_EXACT","MODEL_FEASIBLE_EXACT","EXACT_NECESSARY_WITNESS","FEASIBLE_WITNESS"}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read_json(path):
    opener=gzip.open if str(path).endswith(".gz") else open
    with opener(path,"rt",encoding="utf-8") as stream:return json.load(stream)
def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n");os.replace(tmp,path)
def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as stream:
        for part in iter(lambda:stream.read(1048576),b""):h.update(part)
    return h.hexdigest()
def preflight():
    manifest=read_json(ROOT/"PACKAGE_MANIFEST.json")
    for name,entry in manifest["files"].items():
        path=ROOT/name
        if not path.is_file() or path.stat().st_size!=entry["bytes"] or sha(path)!=entry["sha256"]:
            raise ValueError("Package input changed or missing: "+name)
    import engine, independent_check
    engine.self_test();independent_check.self_test()
    index=read_json(ROOT/"models/index.json")
    if sorted(index["cases"])!=sorted(CASES):raise ValueError("Incomplete four-case inventory")
    for item in index["tasks"]:
        model=read_json(ROOT/item["path"])
        if model["case"]!=item["case"] or model["id"]!=item["id"]:raise ValueError("Task identity mismatch")
        engine.normalize_model(model)
    print("Preflight PASS: input hashes, independent exact controls, and all four case inventories.",flush=True)
    return index
def collect():
    results=ROOT/"results";results.mkdir(exist_ok=True)
    environment={"date":now(),"platform":platform.platform(),"python":sys.version,"cpu_count":os.cpu_count(),"source_commit":read_json(ROOT/"vendor_manifest.json")["commit"]}
    try:
        import numpy, scipy, sympy
        environment["dependencies"]={"numpy":numpy.__version__,"scipy":scipy.__version__,"sympy":sympy.__version__}
    except ImportError:pass
    write_json(results/"environment.json",environment)
    archive=ROOT/"RANK8_RESULTS_TO_SEND.zip";temporary=archive.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temporary,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
        for base in [results,ROOT/"models"]:
            if base.exists():
                for path in sorted(base.rglob("*")):
                    if path.is_file() and not path.name.endswith(".tmp") and "__pycache__" not in path.parts and "history" not in path.parts:
                        bundle.write(path,path.relative_to(ROOT).as_posix())
        for name in ["PACKAGE_MANIFEST.json","vendor_manifest.json","build_validation.json","installed_versions.txt","README.md"]:
            if (ROOT/name).is_file():bundle.write(ROOT/name,name)
    os.replace(temporary,archive)
    print("\nSend back: "+str(archive),flush=True)
    return archive
def certificate_audit(task,result,out):
    if "INFEASIBLE" in str(result.get("status","")) and "CERTIFIED" in str(result.get("status","")):
        from verify_results import audit_task
        audit=audit_task(task,out)
        result["exact_replay_audit"]=audit
        result["independent_certificate_check"]="PASS"
        result["closure_policy"]="EXCLUSION_CANDIDATE_REVIEW_REQUIRED"
def worker(task_path,seconds,attempt):
    task=read_json(Path(task_path))
    out=ROOT/"results"/task["case"]/task["id"];out.mkdir(parents=True,exist_ok=True)
    working=out/"working_model.json"
    base_model=read_json(ROOT/task["path"])
    model=read_json(working) if working.is_file() else base_model
    import engine
    start=time.monotonic()
    try:
        result=engine.solve_model(model,seconds=seconds,output_dir=out,resume=True,seed=attempt)
        if not isinstance(result,dict):raise TypeError("Solver must return a JSON result")
        adapter=importlib.import_module(ADAPTERS[task["case"]])
        if hasattr(adapter,"check_candidate") and isinstance(result.get("values"),list):
            values=result["values"]
            engine.verify_witness(model,values)
            checked=adapter.check_candidate(base_model,values,ROOT/"vendor")
            result["additional_candidate_check"]=checked
            if not checked["valid"]:
                result["status"]="CANDIDATE_REJECTED_EXACTLY"
                cut=adapter.candidate_nogood(base_model,values,ROOT/"vendor")
                replay=adapter.validate_nogood(base_model,values,checked,cut,ROOT/"vendor")
                if not replay["valid"]:raise ValueError("Invalid exact rejection cut: "+str(replay))
                write_json(out/("candidate_rejection_"+str(attempt)+".json"),{"candidate":values,"check":checked,"nogood":cut})
                # Reload before mutation: base_model must keep its equality representation.
                model=read_json(working) if working.is_file() else read_json(ROOT/task["path"])
                if "row_lo" not in model:
                    model["row_lo"]=list(model["rhs"]);model["row_up"]=list(model["rhs"]);model.pop("rhs",None)
                model["rows"].append(cut["row"])
                model["row_lo"].append(cut.get("row_lo"));model["row_up"].append(cut.get("row_up"))
                model["exact_candidate_rejections"]=int(model.get("exact_candidate_rejections",0))+1
                write_json(working,model)
                result["next_step"]="Resume with the exact assignment-blocking row."
        result.update({"task":task["id"],"case":task["case"],"attempt":attempt,"worker_seconds":time.monotonic()-start,"updated":now()})
        write_json(out/"latest.json",result)
        certificate_audit(task,result,out)
        write_json(out/"latest.json",result)
    except BaseException as error:
        write_json(out/"latest.json",{"status":"ERROR","case":task["case"],"task":task["id"],"attempt":attempt,"error":str(error),"traceback":traceback.format_exc(),"updated":now()})
        raise
def memory_gib():
    try:
        data=Path("/proc/meminfo").read_text()
        return next(int(line.split()[1])/1048576 for line in data.splitlines() if line.startswith("MemAvailable:"))
    except Exception:return 6.0
def state_for(task):
    out=ROOT/"results"/task["case"]/task["id"]
    try:return read_json(out/"latest.json")
    except (OSError,ValueError):return {}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hours",type=float,default=8.0)
    p.add_argument("--jobs",type=int,default=None)
    p.add_argument("--case",dest="cases",action="append",choices=CASES)
    p.add_argument("--slice-seconds",type=float,default=300.0)
    p.add_argument("--preflight",action="store_true")
    p.add_argument("--collect",action="store_true")
    p.add_argument("--worker",type=Path)
    p.add_argument("--seconds",type=float)
    p.add_argument("--attempt",type=int,default=0)
    args=p.parse_args()
    if args.worker:
        worker(args.worker,args.seconds,args.attempt);return
    if args.collect:collect();return
    if args.preflight:preflight();return
    if args.hours<=0 or args.slice_seconds<1: p.error("--hours must be positive; --slice-seconds must be at least 1")
    preflight()
    selected=args.cases or CASES
    index=read_json(ROOT/"models/index.json");all_tasks=[x for x in index["tasks"] if x["case"] in selected]
    jobs=args.jobs or max(1,min(2,(os.cpu_count() or 2)//2,max(1,int(memory_gib()/3))))
    if not 1<=jobs<=16:p.error("--jobs must be between 1 and 16")
    results=ROOT/"results";results.mkdir(exist_ok=True)
    lock=results/"campaign.lock"
    import fcntl
    handle=lock.open("a+")
    try:fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:raise SystemExit("Another campaign is running in this folder.")
    stop={"requested":False}
    def request_stop(*_):stop["requested"]=True
    signal.signal(signal.SIGINT,request_stop);signal.signal(signal.SIGTERM,request_stop)
    deadline=time.monotonic()+args.hours*3600
    attempts={}
    for task in all_tasks:attempts[task["id"]]=int(state_for(task).get("attempt",-1))+1
    active={};last_report=0;case_cursor=0
    print("Cases:",", ".join(selected),"\nWorkers:",jobs,"\nBudget:",args.hours,"wall-clock hours. Existing checkpoints resume automatically.",flush=True)
    print("Ctrl+C requests a checkpointed stop; a return archive is written automatically.",flush=True)
    try:
        while time.monotonic()<deadline and not stop["requested"] and not (ROOT/"STOP").exists():
            for key,entry in list(active.items()):
                process,task,log,start,slice_budget=entry
                if process.poll() is not None:
                    log.close();active.pop(key)
                    current=state_for(task)
                    print(task["id"]+": "+str(current.get("status","worker_exit_"+str(process.returncode))),flush=True)
                elif time.monotonic()-start>slice_budget+120:
                    process.terminate()
                    try:process.wait(timeout=15)
                    except subprocess.TimeoutExpired:process.kill();process.wait()
                    log.close();active.pop(key)
                    write_json(results/task["case"]/task["id"]/"latest.json",{"status":"WORKER_TIME_LIMIT","attempt":attempts[task["id"]]-1,"case":task["case"],"task":task["id"],"updated":now()})
            pending=[t for t in all_tasks if t["id"] not in active and state_for(t).get("status") not in DONE and state_for(t).get("status")!="ERROR"]
            while len(active)<jobs and pending and time.monotonic()<deadline:
                # Fairly alternate cases, then tasks with the fewest attempts.
                eligible_cases=selected[case_cursor%len(selected):]+selected[:case_cursor%len(selected)]
                chosen_case=next((c for c in eligible_cases if any(t["case"]==c for t in pending)),None)
                task=min((t for t in pending if t["case"]==chosen_case),key=lambda t:(attempts[t["id"]],t["id"]))
                case_cursor=(selected.index(chosen_case)+1)%len(selected)
                pending.remove(task)
                out=results/task["case"]/task["id"];out.mkdir(parents=True,exist_ok=True)
                task_file=out/"task.json";write_json(task_file,task)
                attempt=attempts[task["id"]];attempts[task["id"]]+=1
                log=(out/("attempt_"+str(attempt)+".log")).open("a")
                budget=min(args.slice_seconds,max(0.1,deadline-time.monotonic()))
                env=dict(os.environ)
                env.update({"OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1","MKL_NUM_THREADS":"1","NUMEXPR_NUM_THREADS":"1","PYTHONUNBUFFERED":"1"})
                process=subprocess.Popen([sys.executable,str(ROOT/"campaign.py"),"--worker",str(task_file),"--seconds",str(budget),"--attempt",str(attempt)],stdout=log,stderr=subprocess.STDOUT,env=env,cwd=ROOT)
                active[task["id"]]=(process,task,log,time.monotonic(),budget)
                print("Searching "+task["id"]+" · attempt "+str(attempt+1),flush=True)
            if not active and not pending:break
            if time.monotonic()-last_report>30:
                summaries={}
                for task in all_tasks:
                    status=state_for(task).get("status","PENDING");summaries[status]=summaries.get(status,0)+1
                write_json(results/"summary.json",{"updated":now(),"cases":selected,"statuses":summaries,"tasks":len(all_tasks),"active":list(active),"wall_hours_requested":args.hours})
                last_report=time.monotonic()
            time.sleep(0.5)
    finally:
        for process,task,log,start,budget in active.values():process.terminate()
        end=time.monotonic()+20
        for process,task,log,start,budget in active.values():
            try:process.wait(timeout=max(0.1,end-time.monotonic()))
            except subprocess.TimeoutExpired:process.kill();process.wait()
            log.close()
        statuses={task["id"]:state_for(task).get("status","PENDING") for task in all_tasks}
        write_json(results/"summary.json",{"updated":now(),"cases":selected,"tasks":statuses,"stopped":stop["requested"] or (ROOT/"STOP").exists()})
        collect()
    if any(state_for(t).get("status")=="ERROR" for t in all_tasks):
        print("Some tasks reported errors; the archive includes their tracebacks.",file=sys.stderr)
if __name__=="__main__":main()
