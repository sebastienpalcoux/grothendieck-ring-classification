"""Liu--Palcoux--Ren--Vercleyen one-spectrum criterion, exact general scope.

Primary reference: Triangular Prism Equations and Categorification,
arXiv:2203.06522; one-spectrum theorem, equations(6.13)--(6.18).
Theorem numbering differs between versions (6.8/6.9).
Author copy: https://bimsa.net/doc/publication/3416.pdf.
"""
import argparse,json,os,subprocess,tempfile
from pathlib import Path
from m3_campaign import OUT,write,require
from analyze import dual,fp

def verify(R,c):
 require(c['kind']=='one_spectrum','criterion kind');n=len(R);q,a,b,c0,u,v,w,x,y,z=c['indices'];require(all(type(i)is int and 0<=i<n for i in c['indices']),'index bounds');d=dual(R)
 dot=lambda i,j,k,l:sum(R[i][j][h]*R[k][l][h] for h in range(n))
 require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundaries')
 require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==1,'equation6.13')
 require(R[u][x][q]==R[d[v]][y][q]==R[w][d[z]][q]==1,'equation6.14')
 require(R[b][a][c0]==0,'equation6.15')
 require(1 in [dot(v,u,y,d[x]),dot(v,q,b,x),dot(b,d[u],y,d[q])],'equation6.16')
 require(1 in [dot(v,q,c0,d[z]),dot(v,w,y,z),dot(y,d[q],c0,d[w])],'equation6.17')
 require(1 in [dot(u,x,w,d[z]),dot(u,a,q,z),dot(q,d[x],w,d[a])],'equation6.18')
 return True

def batch(rows):
 source=Path(__file__).with_suffix('.cpp')
 with tempfile.TemporaryDirectory(prefix='m3_one_spectrum_') as tmp:
  exe=Path(tmp)/'search';subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True,capture_output=True)
  values=[len(rows)]
  for r in rows:
   R=r['tensor'];values.append(len(R));values.extend(v for M in R for row in M for v in row)
  result=subprocess.run([str(exe)],input=' '.join(map(str,values)),text=True,capture_output=True,check=True,timeout=1800)
 out=[]
 for line in result.stdout.splitlines():
  numbers=list(map(int,line.split()));j,found=numbers[:2];require(j==len(out),'one-spectrum source order');r=rows[j];c={'kind':'one_spectrum','indices':numbers[2:]} if found else None
  if c:verify(r['tensor'],c)
  out.append({'id':r['id'],'tensor_sha256':fp(r['tensor']),'stage':'one_spectrum','scope':'general_complex_fusion_category','outcome':'excluded' if c else 'no_conclusion','certificate':c})
 require(len(out)==len(rows),'complete spectrum pass');return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--verify',action='store_true',help='Read-only exact replay (the default).');args=ap.parse_args();rows=json.loads((OUT/'survivors_m3.json').read_text());result=batch(rows);path=OUT/'one_spectrum_m3.json'
 if args.write:write(path.name,result)
 else:require(json.loads(path.read_text())==result,'stored one-spectrum pass differs')
 print('PASS one-spectrum exact search',len(result),'tensors;',sum(r['outcome']=='excluded' for r in result),'exclusions')
if __name__=='__main__':main()
