#!/usr/bin/env python3
"""Build only after exact controls, full branch compilation and solver smoke tests."""
import datetime, gzip, hashlib, json, os, platform, shutil, subprocess, sys, time, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
os.chdir(ROOT)
CASES=["R8_3_928","R8_3_941","R8_3_1154","R8_3_1768"]
COUNTS=dict(zip(CASES,[4,14,25,2]))
LOGS=ROOT/"validation-logs";LOGS.mkdir(exist_ok=True)
stages=[]
def read(path):
    with (gzip.open(path,"rt") if str(path).endswith(".gz") else open(path)) as stream:return json.load(stream)
def write(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n")
def run(name,cmd,timeout=1500):
    start=time.monotonic();print("VALIDATING",name,flush=True)
    with (LOGS/(name+".log")).open("w") as log:
        result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=timeout)
    if result.returncode:
        print((LOGS/(name+".log")).read_text()[-16000:],flush=True)
        raise RuntimeError(name+" failed: "+str(result.returncode))
    stage={"name":name,"status":"PASS","seconds":round(time.monotonic()-start,3)}
    stages.append(stage);print(stage,flush=True)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    start=time.monotonic()
    run("exact_engine_controls",[sys.executable,"engine.py","--self-test"])
    run("independent_checker_controls",[sys.executable,"-c","import independent_check; independent_check.self_test(); print('PASS')"])
    run("rejection_recovery_and_exact_closure",[sys.executable,"tools/control_campaign.py"],timeout=300)
    run("actual_orbit_arithmetic_controls",[sys.executable,"-m","unittest","discover","-s","tests","-v"])
    for case in CASES:
        cmd=[sys.executable,"tools/compile_case.py","--case",case]
        if case!="R8_3_941":cmd.append("--controls")
        run("compile_"+case,cmd)
    import engine
    tasks=[];aliases=[];inventory={}
    for case in CASES:
        receipt=read(ROOT/"models"/(case+".index.json"))
        original=receipt["tasks"];inventory[case]=len(original)
        if receipt["limited"] or len(original)!=COUNTS[case]:raise ValueError("Incomplete branch set "+case)
        seen={}
        for task in original:
            model=read(ROOT/task["path"])
            core=engine.normalize_model(model)
            numeric=engine.model_digest(core)
            if numeric in seen:
                previous=read(ROOT/seen[numeric]["path"])
                if engine.serialized_core(core)!=engine.serialized_core(engine.normalize_model(previous)):raise ValueError("Hash collision; exact arrays differ")
                aliases.append({"case":case,"alias":task["id"],"representative":seen[numeric]["id"],"path":task["path"],"original_model_path":task.get("original_model_path"),"numeric_model_sha256":numeric})
            else:
                tasks.append(task);seen[numeric]=task
    index={"cases":CASES,"tasks":tasks,"complete_branch_counts":inventory,
           "exact_equivalent_branches":aliases,"source_commit":read(ROOT/"vendor_manifest.json")["commit"],
           "closure_policy":"An exact model contradiction still requires mathematical review of all inherited reductions."}
    write(ROOT/"models/index.json",index)
    for case in CASES:
        task=next(t for t in tasks if t["case"]==case)
        taskfile=ROOT/"build-work"/(case+"_smoke_task.json");write(taskfile,task)
        run("solver_smoke_"+case,[sys.executable,"campaign.py","--worker",str(taskfile),"--seconds","2","--attempt","0"],timeout=240)
        latest=read(ROOT/"results"/case/task["id"]/"latest.json")
        if latest["status"]=="ERROR":raise ValueError(latest)
    run("replay_smoke_outputs",[sys.executable,"verify_results.py"],timeout=300)
    shutil.rmtree(ROOT/"results",ignore_errors=True)
    tested=subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True)
    (ROOT/"tested_versions.txt").write_text(tested)
    validation={"status":"PASS","date":datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "platform":platform.platform(),"python":sys.version,"source_commit":index["source_commit"],
                "package_source_commit":os.environ.get("GITHUB_SHA"),"complete_branch_counts":inventory,
                "distinct_search_tasks":len(tasks),"exact_equivalent_branches":aliases,
                "stages":list(stages),"build_seconds":round(time.monotonic()-start,3)}
    write(ROOT/"build_validation.json",validation)
    payload=set()
    for name in ["README.md","METHODS.md","requirements.txt","install.sh","run.sh","collect.sh","campaign.py","verify_results.py","engine.py","independent_check.py","vendor_manifest.json","build_validation.json","tested_versions.txt","tools/compile_case.py","tools/control_campaign.py"]:
        path=ROOT/name
        if not path.is_file():raise ValueError("Missing payload "+name)
        payload.add(path)
    for folder in ["cases","models","tests"]:
        payload.update(p for p in (ROOT/folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc")
    vendor=read(ROOT/"vendor_manifest.json")
    for entry in vendor["files"]:payload.add(ROOT/"vendor"/entry["path"])
    for entry in vendor.get("restored",[]):
        name=entry.get("path") or entry.get("target")
        if not name:raise ValueError("No restored target name")
        payload.add(ROOT/"vendor"/name)
    manifest={"format":1,"files":{p.relative_to(ROOT).as_posix():{"sha256":digest(p),"bytes":p.stat().st_size} for p in sorted(payload)}}
    write(ROOT/"PACKAGE_MANIFEST.json",manifest);payload.add(ROOT/"PACKAGE_MANIFEST.json")
    run("offline_package_preflight",[sys.executable,"campaign.py","--preflight"],timeout=300)
    dist=ROOT/"dist";dist.mkdir(exist_ok=True)
    archive=dist/"Rank8_Exclusion_Campaign.zip"
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
        for path in sorted(payload):
            name="Rank8_Exclusion_Campaign/"+path.relative_to(ROOT).as_posix()
            info=zipfile.ZipInfo(name,date_time=(2026,10,23,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100755 if path.suffix==".sh" else 0o100644)<<16
            bundle.writestr(info,path.read_bytes())
    (dist/"Rank8_Exclusion_Campaign.sha256").write_text(digest(archive)+"  "+archive.name+"\n")
    write(dist/"validation.json",dict(validation,archive_bytes=archive.stat().st_size,archive_sha256=digest(archive),final_preflight="PASS",all_stages=stages))
    print("PACKAGE PASS",archive.stat().st_size,"bytes",len(payload),"files",len(tasks),"distinct tasks",flush=True)
if __name__=="__main__":main()
