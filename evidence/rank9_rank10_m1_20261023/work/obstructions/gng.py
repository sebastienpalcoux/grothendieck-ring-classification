from arithmetic import *
import math

def certificate(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 G=[i for i in range(n) if sum(R[i][du[i]])==1];X=[i for i in range(n) if i not in G]
 if not X:return None
 x=X[0]
 if set(next(k for k in range(n) if R[g][x][k]) for g in G)!=set(X):return None
 H=[g for g in G if R[g][x][x]];r=sum(R[x][du[x]][j] for j in X);st=len(H);disc=r*r+4*st
 if math.isqrt(disc)**2!=disc and r%st:
  return dict(kind='generalized_near_group_divisibility',invertibles=G,noninvertibles=X,object=x,stabilizer=H,r=r,s=st,discriminant=disc,scope='general_complex_fusion_category',reference='Schopieray, Categorification of integral group rings extended by one dimension, Proposition 3.3 (2023)')
 if r==0 and len(X)==1:
  bad=next(((g,h) for g in G for h in G if R[g][h]!=R[h][g]),None)
  if bad:return dict(kind='nonabelian_tambara_yamagami',invertibles=G,object=x,noncommuting_pair=list(bad),scope='general_complex_fusion_category',reference='Tambara--Yamagami 1998; Liptrap arXiv:1002.3166v2 Corollary 4.10')
 return None

def verify(R,c):
 actual=certificate(R)
 if actual!=c:raise ValueError('generalized near-group certificate mismatch')
 return True

def main():
 out=[]
 for r in read():
  c=certificate(r['tensor'])
  if c:verify(r['tensor'],c);print(r['id'],c['kind'],flush=True)
  out.append(dict(id=r['id'],rank=r['rank'],tensor_sha256=r['tensor_sha256'],certificate=c))
 (HERE/'gng.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TOTAL',sum(x['certificate'] is not None for x in out))
if __name__=='__main__':main()
