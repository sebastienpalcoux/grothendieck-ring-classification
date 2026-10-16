"""Exact tensor hypotheses of the R170 inverse-Morita near-group reduction."""
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path

def req(ok,message):
 if not ok:raise ValueError(message)
def flat(r):return tuple(x for m in r for row in m for x in row)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);root=ap.parse_args().repo.resolve()
 with gzip.open(root/'supplements/rank8/data/rank8_tables.txt.gz','rt') as f:rows=[json.loads(l.replace('{','[').replace('}',']')) for l in f]
 r=sorted((r for r in rows if max(flat(r))==2),key=flat)[169];digest=hashlib.sha256(json.dumps(r,separators=(',',':')).encode()).hexdigest();ledger={x['id']:x for x in json.loads((root/'supplements/rank8/data/decisions.json').read_text())};req(digest=='78c260875e85e75fa8689dba58a9c5225942228315e25da354ad3da8b4bbf06d','immutable source hash');req(digest==ledger['R8_2_170']['tensor_sha256'],'ledger source hash')
 neutral={0,5,6,7};degree=[int(i not in neutral) for i in range(8)];req(all(degree[k]==degree[i]^degree[j] for i in range(8) for j in range(8) for k in range(8) if r[i][j][k]),'faithful grading')
 def prod(i,j):
  req(sum(r[i][j])==1,'expected simple product');return r[i][j].index(1)
 inv=[0,3,4,5];req(all(prod(i,j) in inv for i in inv for j in inv),'pointed group closed');req(all(prod(i,i)==0 for i in inv),'V4');u=3;g=5;rho=6;req(degree[u]==1 and prod(u,u)==0,'odd involution');req(prod(prod(u,rho),u)==prod(g,rho),'conjugation')
 # The generator of H^3(C2,C*) is a normalized cocycle.
 gamma=lambda a,b,c: -1 if a*b*c else 1
 req(all(gamma(b,c,d)*gamma(a,b^c,d)*gamma(a,b,c)==gamma(a^b,c,d)*gamma(a,b,c^d) for a in range(2) for b in range(2) for c in range(2) for d in range(2)),'grading cocycle pentagon')
 req(all(gamma(a,b,c)==1 for a in range(2) for b in range(2) for c in range(2) if 0 in (a,b,c)) and gamma(1,1,1)==-1,'normalized nontrivial C2 cocycle')
 H=[0,u];unseen=set(range(8));orbits=[]
 while unseen:
  y=min(unseen);orbit=sorted({prod(prod(h,y),k) for h in H for k in H});stabilizer=[(h,k) for h in H for k in H if prod(prod(h,y),k)==y];orbits.append({'representative':y,'orbit':orbit,'free_bimodule_end_dimension':len(stabilizer)});unseen-=set(orbit)
 req(sorted((len(x['orbit']),x['free_bimodule_end_dimension']) for x in orbits)==[(2,2),(2,2),(4,1)],'bimodule orbit types')
 req(r[rho][rho]==[1,0,0,0,0,0,2,2],'d squared relation');req(prod(g,rho)==7,'neutral partner')
 terminal=[]
 for name in ['C4','V4']:
  t=[[[0]*5 for _ in range(5)] for _ in range(5)]
  for i in range(4):
   for j in range(4):t[i][j][(i+j)%4 if name=='C4' else i^j]=1
   t[i][4][4]=t[4][i][4]=1
  t[4][4]=[1,1,1,1,8]
  terminal.append({'group':name,'level':8,'tensor':t,'tensor_sha256':hashlib.sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest()})
 terminal_script=Path(__file__).resolve().parent/'rank5_cyclic/verify.py'
 process=subprocess.run([sys.executable,str(terminal_script)],check=True,capture_output=True,text=True)
 cyclic_receipt=json.loads(process.stdout);req(cyclic_receipt['result']=='PASS','cyclic terminal certificate failed');req(len(cyclic_receipt['branches'])==6,'cyclic terminal branch coverage')
 print(json.dumps({'status':'PASS','id':'R8_2_170','tensor_sha256':digest,'neutral_labels':sorted(neutral),'odd_involution':u,'H_double_orbits':orbits,'dual_pointed_rank':4,'dual_noninvertible_rank':1,'dual_noninvertible_dimension':'4+2sqrt(5)','terminal_near_group_tensors':terminal,'cyclic_terminal_replay':cyclic_receipt,'klein_terminal_theorem':'Schopieray, Categorification of integral group rings extended by one dimension, Theorem 1.1 (general complex)','scope':'R8_2_170 has no fusion-category categorification over C; source-bound Morita reduction, exact cyclic terminal replay, and cited Klein-four exclusion'},indent=2))
if __name__=='__main__':main()
