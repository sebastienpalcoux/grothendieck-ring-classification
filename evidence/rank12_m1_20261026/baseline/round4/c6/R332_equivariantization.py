import json,sys,itertools
from pathlib import Path
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'grothendieck-revision/supplements/rank6/software'))
from prepare import key
from rings import validate
cen=json.load(open(root/'grothendieck-revision/supplements/rank6/data/census.json'));dec={r['id']:r for r in json.load(open(root/'grothendieck-revision/supplements/rank6/data/decisions.json'))}
rows=[]
for a,s in itertools.product(range(2),repeat=2):
 R=[[[0]*6 for j in range(6)]for i in range(6)]
 def put(i,j,terms):
  for k,v in terms.items():R[i][j][k]=R[j][i][k]=v
 for i in range(6):put(0,i,{i:1})
 put(1,1,{0:1});put(1,2,{2:1});put(1,3,{4:1});put(1,4,{3:1});put(1,5,{5:1})
 put(2,2,{0:1,1:1,2:1});put(2,3,{5:1});put(2,4,{5:1});put(2,5,{3:1,4:1,5:1})
 put(3,3,{a:1,3+s:1,5:1});put(4,4,{a:1,3+s:1,5:1});put(3,4,{1-a:1,4-s:1,5:1})
 put(3,5,{2:1,3:1,4:1,5:2});put(4,5,{2:1,3:1,4:1,5:2});put(5,5,{0:1,1:1,2:1,3:2,4:2,5:4})
 try:validate(R)
 except Exception as e:print(a,s,'invalid',str(e));continue
 k=key(R);hits=[r for r in cen if r['m']==4 and key(r['N'])==k];print(a,s,[(h['id'],dec[h['id']]['status'],dec[h['id']].get('certificate',{}).get('kind'))for h in hits],flush=True)
 rows.append(dict(a=a,s=s,N=R,hits=[dec[h['id']] for h in hits]))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n')
