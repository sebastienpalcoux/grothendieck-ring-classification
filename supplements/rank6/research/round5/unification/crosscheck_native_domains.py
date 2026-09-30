"""Cross-check selected canonical native domains with the independent Schur engine."""
from pathlib import Path
import hashlib,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from round5_unified import enumerate_fixed_gram_block
source=ROOT/'research/round5/m5_1204/joint_domain_certificate.json'
groups=json.loads(source.read_text());records=[]
for gi in (0,len(groups)//2,len(groups)-1):
 g=groups[gi];H=s.Matrix(g['gram']);Q=H[:5,:5];B=H[5:,:5];G=H[5:,5:]
 for ti in (0,len(g['types'])//2,len(g['types'])-1):
  t=g['types'][ti];a=enumerate_fixed_gram_block(Q.tolist(),B.tolist(),G.tolist(),t['column'],time_limit=30)
  if not a['complete'] or sorted(a['candidates'])!=sorted(t['vectors']):raise ValueError('canonical native/Schur domain mismatch')
  records.append(dict(gram_index=gi,type_index=ti,count=len(a['candidates']),nodes=a['nodes'],rank=a['rank']))
out=dict(passed=True,optimizer_used=False,source='research/round5/m5_1204/joint_domain_certificate.json',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),native_source='software/round5_1204.cpp',native_source_sha256=hashlib.sha256((ROOT/'software/round5_1204.cpp').read_bytes()).hexdigest(),records=records)
p=Path(__file__).with_name('native_1204_domain_crosscheck.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=True,domains=len(records))))
