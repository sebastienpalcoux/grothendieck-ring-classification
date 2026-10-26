"""Complete accepted offline replay and delivered-ledger binding."""
from pathlib import Path
import collections,csv,hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
FIRST=ROOT/"evidence/rank12-m1-offline-20261025"
SECOND=ROOT/"evidence/rank12-m1-round2-20261025"
LOG=ROOT/"verification";LOG.mkdir(exist_ok=True)
def require(c,m):
 if not c:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(R):return hashlib.sha256(json.dumps(R,separators=(",",":")).encode()).hexdigest()
steps=[
 (FIRST,"verify.py"),
 (SECOND/"audit_exclusions","audit_all_exclusions.py"),
 (SECOND/"audit_models","independent_positive_bindings.py"),
 (SECOND/"family_cubic","verify.py"),
 (SECOND/"audit_exclusions","audit_c9_morita.py"),
 (SECOND/"audit_exclusions","audit_quadratic_signed.py"),
 (SECOND/"audit_exclusions","audit_pointed_stabilizers.py"),
 (SECOND/"family_graded","verify.py"),
 (SECOND/"audit_exclusions","audit_d8_cohomology.py"),
 (SECOND/"audit_exclusions","audit_d40_duals.py"),
 (SECOND/"family_quadratic","verify.py"),
 (SECOND/"family_quadratic","audit_graded_models.py"),
 (SECOND/"family_integral","verify.py"),
 (SECOND/"d24_pointed_extensions","verify.py"),
 (SECOND/"audit_exclusions","audit_graph_model.py"),
 (SECOND/"audit_exclusions","audit_sl23_model.py")]
start=time.monotonic();checks=[];mode="optimized"if not __debug__ else"normal"
for number,(directory,script)in enumerate(steps,1):
 t=time.monotonic();r=subprocess.run([sys.executable,*([]if __debug__ else["-O"]),str(directory/script)],cwd=directory,capture_output=True,text=True,env=dict(os.environ,OPENBLAS_NUM_THREADS="1",PYTHONDONTWRITEBYTECODE="1"))
 label=str((directory/script).relative_to(ROOT));(LOG/f"{mode}_{number:02d}.log").write_text(r.stdout+r.stderr)
 if r.returncode:print(r.stdout[-4000:]+r.stderr[-4000:]);raise RuntimeError("Failed: "+label)
 checks.append(dict(script=label,status="PASS",seconds=time.monotonic()-t));print(f"{number:02d}/{len(steps)} PASS {label}",flush=True)
data=read(FIRST/"tensors.json");old=read(FIRST/"ledger.json");ledger=read(ROOT/"ledger.json");summary=read(ROOT/"summary.json");new=read(ROOT/"new_decisions.json")
require(summary==ledger["summary"],"ledger summary binding")
require((summary["excluded"],summary["modeled"],summary["unresolved"])==(425,141,66),"final totals")
require(summary["online_revision_performed"]is False,"offline scope")
negative=set(new["exclusions"]);positive=set(new["models"])
require(len(negative)==32 and len(positive)==14 and not negative&positive,"new disjoint counts")
oldex={r["id"]for r in old["records"]if r["status"]=="excluded"};oldmo={r["id"]for r in old["records"]if r["status"]=="unitarily_realized"};oldun=set(data)-oldex-oldmo
require(negative|positive<=oldun,"only previously unresolved statuses changed")
ids=[r["id"]for r in ledger["records"]];require(len(ids)==len(set(ids))==632 and set(ids)==set(data),"all permanent IDs exactly once")
by={r["id"]:r for r in ledger["records"]}
for rid,R in data.items():
 expected="excluded"if rid in oldex|negative else"unitarily_realized"if rid in oldmo|positive else"unresolved"
 require(by[rid]["status"]==expected and by[rid]["tensor_sha256"]==sha(R),"status and input binding "+rid)
for rid,models in new["models"].items():
 for m in models:
  p=m["basis_map_source_to_model"];T=m["model_tensor"]
  require(p[0]==0 and sorted(p)==list(range(12)),"unit-preserving model bijection")
  require(all(data[rid][i][j][k]==T[p[i]][p[j]][p[k]]for i in range(12)for j in range(12)for k in range(12)),"all new model coefficients")
# Independent elementary reconstruction of the classical R541 representation ring.
M=[[[0]*12 for _ in range(12)]for _ in range(12)]
for a in range(8):
 for b in range(8):M[a][b][(a+b)%8]=1
 for b in range(4):M[a][8+b][8+(a+b)%4]=M[8+b][a][8+(a+b)%4]=1
for a in range(4):
 for b in range(4):
  M[8+a][8+b][(a+b)%8]=1;M[8+a][8+b][(a+b+4)%8]=1;M[8+a][8+b][8+(a+b)%4]=1
require(any(m["model_tensor"]==M for m in new["models"]["R12_1_541"]),"classical R541 reconstruction")
with(ROOT/"ledger.csv").open(newline="")as f:rows=list(csv.DictReader(f))
require(len(rows)==632 and {r["id"]for r in rows}==set(data),"CSV complete IDs")
require(all(r["status"]==by[r["id"]]["status"]and r["tensor_sha256"]==by[r["id"]]["tensor_sha256"]for r in rows),"CSV decisions")
rem=read(ROOT/"unresolved_tensors.json");expected=set(data)-oldex-negative-oldmo-positive
require(len(rem)==66 and {r["id"]for r in rem}==expected,"unresolved list complete")
require(all(r["tensor"]==data[r["id"]]and r["tensor_sha256"]==sha(data[r["id"]])for r in rem),"unresolved tensors")
out=dict(status="PASS",input_count=632,excluded=425,modeled=141,unresolved=66,new_excluded=32,new_modeled=14,optimized_python=not __debug__,steps=checks,elapsed_seconds=time.monotonic()-start)
(LOG/f"{mode}.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps({k:v for k,v in out.items()if k!="steps"},indent=2))
