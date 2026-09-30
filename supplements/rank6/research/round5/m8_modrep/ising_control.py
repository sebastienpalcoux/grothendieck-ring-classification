"""Exact positive controls: the two Ising-center actual-twist spectra."""
import hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import require
from representation_cone import records
HERE=Path(__file__).parent

def control():
 cone=records()['cone'];out=[]
 for z in (3,9):
  twists=[0,24,z];target=[0]*48
  for a in twists:
   for b in twists:target[(a-b)%48]+=1
  allowed=[(i,r) for i,r in enumerate(cone) if r['central_sign']==1 and all(x<=y for x,y in zip(r['spectrum'],target))]
  solution=None;nodes=0
  def dfs(k,remaining,chosen):
   nonlocal solution,nodes
   nodes+=1
   if not any(remaining):solution=list(chosen);return True
   if k==len(allowed):return False
   ix,r=allowed[k];spec=r['spectrum'];bound=min(b//a for a,b in zip(spec,remaining) if a)
   for m in range(bound+1):
    if dfs(k+1,[b-m*a for a,b in zip(spec,remaining)],chosen+([[ix,m]] if m else [])):return True
   return False
  require(dfs(0,target,[]),'Ising-center cone control failed')
  require(all(sum(m*cone[i]['spectrum'][k] for i,m in solution)==target[k] for k in range(48)),'control spectrum decomposition failed')
  out.append({'Ising_sigma_exponent_mod48':z,'center_T_spectrum':target,'central_sign':1,'cone_decomposition':solution,'nodes':nodes})
 return {'passed':True,'scope':'positive controls for the complete signed finite-representation spectrum cone','controls':out}
if __name__=='__main__':
 out=control();p=HERE/'ising_control.json'
 if '--verify' in sys.argv:require(out==json.loads(p.read_text()),'Ising control replay mismatch')
 else:p.write_text(json.dumps(out,indent=2)+'\n')
 files=[Path(__file__).resolve(),p,HERE/'representation_cone.py',HERE/'sl2_16.json',HERE/'sl2_3.json',ROOT/'software/exact.py'];receipt={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'controls':2,'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}};(HERE/'ising_control_replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print('two exact Ising-center spectrum controls passed')
