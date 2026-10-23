#!/usr/bin/env python3
"""Compile one case in an isolated interpreter, preserving exact source domains."""
import argparse, gzip, hashlib, importlib, json, re, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
MODULES={"R8_3_928":"cases.r928_r941","R8_3_941":"cases.r928_r941","R8_3_1154":"cases.r1154","R8_3_1768":"cases.r1768"}
def save(path,model):
    data=(json.dumps(model,sort_keys=True,separators=(",",":"),default=str)+"\n").encode()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(data,compresslevel=6,mtime=0))
def main():
    p=argparse.ArgumentParser();p.add_argument("--case",choices=MODULES,required=True);p.add_argument("--limit",type=int);p.add_argument("--controls",action="store_true");args=p.parse_args()
    import engine
    start=time.monotonic();adapter=importlib.import_module(MODULES[args.case])
    scratch=ROOT/"build-work"/args.case;scratch.mkdir(parents=True,exist_ok=True)
    controls=adapter.self_test(ROOT/"vendor") if args.controls else {"not_rerun":True}
    target=ROOT/"models";target.mkdir(exist_ok=True)
    tasks=[]
    for original in adapter.build_models(ROOT/"vendor",args.case,scratch,limit=args.limit):
        if original.get("case")!=args.case:raise ValueError("Wrong case identity")
        name=original["id"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+",name):raise ValueError("Unsafe model identifier")
        model=original
        original_path=None
        if hasattr(adapter,"project_fixed"):
            original_path=target/"originals"/(name+".json.gz")
            save(original_path,original)
            model={**original,**adapter.project_fixed(original)};model["id"]=name
            model["coverage_branch_id"]=name
            for key in ("coverage_group","source_closure","source_closure_sha256","tensor_sha256","prerequisites","novelty","statistics","all_branches_exported"):
                if key in original:model[key]=original[key]
            model["original_model_path"]=original_path.relative_to(ROOT).as_posix()
        engine.normalize_model(model)
        path=target/(name+".json.gz");save(path,model)
        task={"case":args.case,"id":name,"path":path.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"variables":int(model["n"]),"rows":len(model["rows"]),"integer_variables":sum(bool(x) for x in model["integrality"]),"metadata":model.get("metadata",{}),"theory_scope":model.get("theory_scope",model.get("scope","Necessary system only"))}
        if original_path:task["original_model_path"]=original_path.relative_to(ROOT).as_posix()
        tasks.append(task)
        print("Compiled",name,"variables",task["variables"],"rows",task["rows"],flush=True)
    if not tasks:raise ValueError("Case builder emitted no tasks")
    receipt={"case":args.case,"tasks":tasks,"controls":controls,"compile_seconds":time.monotonic()-start,"limited":args.limit is not None}
    (target/(args.case+".index.json")).write_text(json.dumps(receipt,indent=2,default=str)+"\n")
if __name__=="__main__":main()
