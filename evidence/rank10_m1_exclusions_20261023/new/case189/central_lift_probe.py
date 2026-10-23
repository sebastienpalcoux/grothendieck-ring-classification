from itertools import permutations
from pathlib import Path
__file__=str(Path(__file__).resolve().with_name('verify_structure.py'))
exec(Path(__file__).read_text().split('receipt=')[0])
def hv(row,v):
 ans=cv(0)
 for h,n in zip(row,v):ans=add(ans,mul(h,n))
 return ans
found=[]
# params = trivialtwo then(lambda,uplus),(lambda,uminus).
# independently assignsingleton andtriplemissing indices.
for sing in permutations(range(1,5)):
 for miss in permutations(range(1,5)):
  cols=[[1]+[0]*9,[1]+[0]*4+[0]+[1]*4]
  for j in range(4):
   cols.append([1]+[0]*4+[int(i not in [0,miss[j]]) for i in range(5)])
   cols.append([1]+[0]*4+[int(i==sing[j]) for i in range(5)])
  if any(hv(H[i],cols[j])!=hv(H[j],cols[i]) for i in range(10) for j in range(i)):
   continue
  found.append((sing,miss,cols))
print('reciprocitysolutions',len(found))
for sing,miss,cols in found:
 for t in range(5):
  A=[]
  for i in range(5):
   tot=cv(0)
   for g in range(1,5):
    for (l,w,r),v in zip(params,cols):
     tot=add(tot,mul(v[5+(i-g)%5],zpow[(3*t*g*g+3*l*g)%5]))
   A.append(tot)
  print('sing',sing,'miss',miss,'q',t,'thirdmomentsvanish',all(x==cv(0) for x in A),'A',[[str(c) for c in a] for a in A])
