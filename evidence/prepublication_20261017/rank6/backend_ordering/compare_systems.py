"""Compare exact systems up to signed row permutation, including right sides."""
import argparse,json,hashlib
from collections import defaultdict,deque
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('first',type=Path);p.add_argument('second',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
f=json.loads(a.first.read_text());q=json.loads(a.second.read_text())
def require(v,s):
 if not v:raise ValueError(s)
require(len(f['A'])==len(q['A']) and len(f['A'][0])==len(q['A'][0]),'matrix shape differs')
index=defaultdict(deque)
def form(row,b):
 support=[(j,v)for j,v in enumerate(row)if v]
 if b:support.append((len(row),b))
 sign=-1 if support and support[0][1]<0 else 1
 key=hashlib.sha256(json.dumps([(j,v*sign)for j,v in support],separators=(',',':')).encode()).hexdigest()
 return key,sign
for i,(row,b)in enumerate(zip(f['A'],f['b'])):
 k,s=form(row,b);index[k].append((i,s))
mapping=[];unmatched=[]
for i,(row,b)in enumerate(zip(q['A'],q['b'])):
 k,ss=form(row,b)
 if not index[k]:unmatched.append(i);continue
 j,fs=index[k].popleft();sg=ss*fs
 require(b==sg*f['b'][j] and all(x==sg*y for x,y in zip(row,f['A'][j])),'digest collision or incorrect entry map')
 mapping.append([i,j,sg])
y=q['y'];support=[(i,v)for i,v in enumerate(y)if v]
vals=[sum(q['A'][i][j]*v for i,v in support)for j in range(len(q['A'][0]))]
r={'status':'PASS' if not unmatched else 'UNMATCHED','rows':len(f['A']),'columns':len(f['A'][0]),'same_saved_ray':f['y']==y,'signed_row_permutation_complete':not unmatched,'unmatched_second_rows':unmatched,'changed_rows':[r for r in mapping if r[0]!=r[1]or r[2]!=1],'old_bTy':sum(x*v for x,v in zip(f['b'],y)),'new_bTy':sum(x*v for x,v in zip(q['b'],y)),'new_min_ATy':min(vals),'new_negative_columns':sum(x<0 for x in vals),'permutation_convention':'[second_row, first_row, multiplier]; includes right side; each matched integer entry compared exactly, no column permutation','input_sha256':{str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in [a.first,a.second]}}
a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in ['changed_rows','unmatched_second_rows','input_sha256']},indent=2))
