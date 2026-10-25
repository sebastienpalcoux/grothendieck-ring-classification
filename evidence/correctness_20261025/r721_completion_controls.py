from pathlib import Path
import importlib.util,itertools,random,json,hashlib
A=Path(__file__).resolve().parent;p=A/'r721_exact_completion.py'
s=importlib.util.spec_from_file_location('completion',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rng=random.Random(20261025)
checks=[]
for case in range(240):
 q=1+case%4;D=rng.randrange(1,6);M=[[rng.randrange(-4,5)for j in range(q)]+[rng.randrange(-10,11)]for r in range(1+case%7)]
 dom=[tuple(v for v in range(4)if rng.randrange(3)!=0)or (rng.randrange(4),)for j in range(q)]
 actual={v for v in itertools.product(*dom)if all(0<=sum(a*x for a,x in zip(row[:-1],v))+row[-1]<=3*D and (sum(a*x for a,x in zip(row[:-1],v))+row[-1])%D==0 for row in M)}
 found=set();nodes=[0]
 def walk(d):
  nodes[0]+=1;got,why=m.propagate(d,M,D)
  if why:return
  free=next((j for j in range(q)if len(d[j])>1),None)
  if free is None:found.add(tuple(x[0]for x in d));return
  for v in d[free]:
   child=d.copy();child[free]=(v,);walk(child)
 walk(dom.copy());m.need(found==actual,'Independent Cartesian control mismatch')
 checks.append(dict(case=case,variables=q,denominator=D,solutions=len(found),nodes=nodes[0]))
receipt=dict(passed=True,optimized_python=not __debug__,independent_cartesian_domains=240,script_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),checks=checks)
(A/'r721-completion-controls.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items()if k!='checks'}))
