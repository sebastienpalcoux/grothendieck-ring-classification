"""Published general rank-three quadratic descent (Ostrik Theorems5.1,1.1)."""
import json,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'supplements/rank7/software'))
from subring_descent import closed_subrings
from rings import codegree_poly
from exact import require

def certificate(R):
 for J,S in closed_subrings(R):
  if len(J)!=3 or any(S[i][i][0]!=1 for i in range(3)):continue
  if max(v for M in S for row in M for v in row)<=2:continue
  p=codegree_poly(S)
  if not any(f.degree()==2 for f,m in p.factor_list()[1]):continue
  return {'kind':'quadratic_rank3_subring','subset':list(J),'subring_tensor':S,'formal_codegree_polynomial':list(map(int,p.all_coeffs())),'maximum_structure_coefficient':max(v for M in S for row in M for v in row),'source_url':'https://arxiv.org/pdf/1309.4822','source_theorems':['5.1','1.1'],'scope':'general_complex'}
 return None

def verify(R,c):
 require(c['kind']=='quadratic_rank3_subring','kind');J=c['subset'];S=None
 for JJ,SS in closed_subrings(R):
  if list(JJ)==J:S=SS;break
 require(S is not None and len(S)==3 and all(S[i][i][0]==1 for i in range(3)),'closed selfdual rank3 subring')
 p=codegree_poly(S);m=max(v for M in S for row in M for v in row)
 require(any(f.degree()==2 for f,z in p.factor_list()[1]),'not quadratic')
 require(m>2 and c['subring_tensor']==S and c['formal_codegree_polynomial']==list(map(int,p.all_coeffs())) and c['maximum_structure_coefficient']==m,'wrong data')
 require(c['source_theorems']==['5.1','1.1'] and c['scope']=='general_complex','scope')
if __name__=='__main__':
 out=[]
 for r in json.load(open(P/'supplements/rank7/output/m5/survivors.json')):
  c=certificate(r['tensor'])
  if c:verify(r['tensor'],c);out.append({'id':r['id'],'certificate':c,'replayed':True})
 Path(__file__).with_name('quadratic_rank3_certificates.json').write_text(json.dumps(out,indent=2)+'\n');print('excluded',len(out),[r['id'] for r in out])
