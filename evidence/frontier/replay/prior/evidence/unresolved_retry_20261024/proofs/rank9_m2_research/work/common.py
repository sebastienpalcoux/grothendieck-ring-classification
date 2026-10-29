from pathlib import Path
import json,gzip,hashlib,sys
import numpy as np
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parent/'grothendieck-ring-classification'
PRIOR=REPO/'evidence/rank9_rank10_m1_20261023'
sys.path.insert(0,str(BASE/'sources'))
from match_models import based_iso,coarse
def digest(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def read():
 out=[];counts={}
 for line,text in enumerate(gzip.open(BASE/'inputs/rank9_M2_verified/FusionRingMultiplicationTables.txt.gz','rt'),1):
  R=json.loads(text.replace('{','[').replace('}',']'));m=max(v for a in R for b in a for v in b)
  counts[m]=counts.get(m,0)+1
  out.append({'id':f'R9_{m}_{counts[m]}','physical_line':line,'multiplicity':m,'tensor':R,'tensor_sha256':digest(R)})
 return out
def save(name,data):
 (BASE/'work'/name).write_text(json.dumps(data,indent=2)+'\n')
def load(name):return json.loads((BASE/'work'/name).read_text())
