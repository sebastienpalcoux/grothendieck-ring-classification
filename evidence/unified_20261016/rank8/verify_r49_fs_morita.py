"""Exact source hypotheses for R49's pivotal odd-isotypic/Morita exclusion."""
import argparse,gzip,hashlib,itertools,json,subprocess,sys
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)
def flat(r):return tuple(x for m in r for row in m for x in row)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);root=ap.parse_args().repo.resolve()
 with gzip.open(root/'supplements/rank8/data/rank8_tables.txt.gz','rt')as f:rows=[json.loads(s.replace('{','[').replace('}',']'))for s in f]
 r=sorted((r for r in rows if max(flat(r))==1),key=flat)[48];digest=hashlib.sha256(json.dumps(r,separators=(',',':')).encode()).hexdigest();need(digest=='a5cefbf544001818e1e5c6e5bde951601eaf35f3d71034a252df1b7de751ea85','immutable source hash')
 ledger={x['id']:x for x in json.loads((root/'supplements/rank8/data/decisions.json').read_text())};need(digest==ledger['R8_1_49']['tensor_sha256'],'ledger identity')
 need(all(sum(r[i][j][k]*r[k][a][b]for k in range(8))==sum(r[j][a][k]*r[i][k][b]for k in range(8))for i,j,a,b in itertools.product(range(8),repeat=4)),'source associativity')
 dual=[next(j for j in range(8)if r[i][j][0])for i in range(8)];inv=[0,3,4,5];noninv=[1,2,6,7];rho=6;u=3;g=5
 def prod(i,j):
  need(sum(r[i][j])==1,'simple product');return r[i][j].index(1)
 need(all(prod(i,j)in inv for i in inv for j in inv)and all(prod(i,i)==0 for i in inv),'pointed V4')
 need(dual[rho]==rho and all(dual[i]==i for i in inv),'FS selfduality hypotheses')
 need(r[rho][rho]==[1,1,1,0,0,0,1,1],'rho square')
 # Exact positive dimension character in Z[d]/(d^2-4d-1).
 ds=[(1,0)if i in inv else(0,1)for i in range(8)]
 def mul(x,y):return(x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+4*x[1]*y[1])
 need(all(mul(ds[i],ds[j])==tuple(sum(r[i][j][k]*ds[k][a]for k in range(8))for a in range(2))for i,j in itertools.product(range(8),repeat=2)),'two FP dimensions, d=2+sqrt5')
 cube=[sum(r[rho][rho][k]*r[k][rho][j]for k in range(8))for j in range(8)];need(all(cube[j]==1 for j in inv),'all pointed isotypic multiplicities in rho cubed are one')
 sign_solutions=[]
 for epsilon in[-1,1]:
  for signs in itertools.product([-1,1],repeat=3):
   nu={0:1,3:signs[0],4:signs[1],5:signs[2]}
   if all(nu[j]==epsilon**3 for j in inv if cube[j]%2):sign_solutions.append({'rho':epsilon,'pointed':[nu[j]for j in inv]})
 need(sign_solutions==[{'rho':1,'pointed':[1,1,1,1]}],'pivotal parity has the unique positive sign assignment')
 need(prod(prod(u,rho),u)==prod(g,rho),'moved involution conjugation')
 H=[0,u];unseen=set(range(8));orbits=[]
 while unseen:
  y=min(unseen);orbit=sorted({prod(prod(h,y),k)for h in H for k in H});stab=[(h,k)for h in H for k in H if prod(prod(h,y),k)==y];orbits.append({'representative':y,'orbit':orbit,'free_bimodule_end_dimension':len(stab)});unseen-=set(orbit)
 need(sorted((len(o['orbit']),o['free_bimodule_end_dimension'])for o in orbits)==[(2,2),(2,2),(4,1)],'bimodule double orbit coverage')
 need(sorted(len(o['orbit'])for o in orbits if o['representative']in inv)==[2,2],'both short orbits pointed')
 terminal_script=Path(__file__).with_name('rank5_cyclic')/'verify.py';process=subprocess.run([sys.executable,str(terminal_script)],check=True,capture_output=True,text=True);terminal=json.loads(process.stdout);need(terminal['result']=='PASS'and len(terminal['branches'])==6,'cyclic order-four level-eight terminal exclusion')
 print(json.dumps({'status':'PASS','id':'R8_1_49','tensor_sha256':digest,'dual_labels':dual,'invertible_labels':inv,'selfdual_generator':rho,'rho_cubed':cube,'unique_FS_signs':sign_solutions[0],'associator_trivial_involution':u,'H_double_orbits':orbits,'Morita_dual_type':'near-group, group order4, level8','cyclic_terminal_replay':terminal,'Klein_terminal':'Schopieray JLMS2023 Theorem1.1: levels0 or4 only','scope':'General complex exclusion via Schopieray Lemma3.1, pivotal palindromic odd-isotypic lemma, and inverse Morita reduction'},indent=2))
if __name__=='__main__':main()
