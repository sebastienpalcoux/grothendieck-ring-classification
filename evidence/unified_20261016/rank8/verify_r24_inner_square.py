#!/usr/bin/env python3
"""Source-bound R24 -> label-fixing square root of Ad(g); no exclusion assumed."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path
SHA='2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738'
def req(x,m):
 if not x:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path);a=ap.parse_args();rr=[]
 for line in gzip.open(a.repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
  if not line.strip():continue
  N=json.loads(line.replace('{','[').replace('}',']'))
  if max(v for aa in N for b in aa for v in b)==2:rr.append(N)
 N=sorted(rr)[23];sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest();req(sha==SHA,'source binding')
 dual=[next(j for j in range(8)if N[i][j][0])for i in range(8)]
 for i,j,k in itertools.product(range(8),repeat=3):
  req(N[i][j]==N[j][i],'commutative source');req(N[i][j][k]==N[dual[i]][k][j]==N[k][dual[j]][i],'Frobenius reciprocity')
  for l in range(8):req(sum(N[i][j][u]*N[u][k][l]for u in range(8))==sum(N[j][k][u]*N[i][u][l]for u in range(8)),'associativity')
 basis=[0,7,5,6];outside=set(range(8))-set(basis)
 for i,j in itertools.product(range(4),repeat=2):
  expected=[0]*4
  if i<2 and j<2:expected[i^j]=1
  elif i<2:expected[2+(i^(j-2))]=1
  elif j<2:expected[2+((i-2)^j)]=1
  else:expected[(i-2)^(j-2)]=1;expected[2]=expected[3]=2
  req([N[basis[i]][basis[j]][k]for k in basis]==expected,'all64 neutral coefficients')
  req(all(N[basis[i]][basis[j]][k]==0 for k in outside),'closed subcategory')
 req(all(dual[x]==x for x in basis),'neutral simples self-dual')
 A,AD,G=1,2,7;req(dual[A]==AD and N[A][AD]==[1]+[0]*7,'actual invertible generator')
 req(N[A][A]==[int(k==G)for k in range(8)]and N[G][G]==[1]+[0]*7,'a²=g and g²=1')
 ad=[]
 for x in basis:
  product=[sum(N[A][x][u]*N[u][AD][k]for u in range(8))for k in range(8)]
  req(product==[int(k==x)for k in range(8)],'Ad(a) fixes every neutral label');ad.append(x)
 out={'status':'PASS','source_id':'R8_2_24','tensor_sha256':sha,'neutral_basis_1_g_r_gr':basis,'invertible_a':A,'inverse_a':AD,'a_squared':G,'neutral_ad_a_permutation':ad,'neutral_coefficients_checked':64,'source_associativity_checked':True,'scope':'categorification supplies label-fixing tensor F=Ad(a)|D with F² tensor-isomorphic to Ad(g); no standalone exclusion','optimizer_used':False}
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
