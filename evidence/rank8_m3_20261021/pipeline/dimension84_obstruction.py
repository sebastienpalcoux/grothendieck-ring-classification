"""Exact source witnesses for the general dimension84 adjoint-rigidity theorem."""
import argparse,functools,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/'supplements/rank8/software'))
from analyze import fp,dual
from dimension42_group_types import enumerate_all,require
IDS=[f'R8_3_{i}' for i in (76,735,738,1422,1805)]

def generated(R,start):
 S=set(start)|{0}
 while True:
  T=S|{k for i in S for j in S for k,v in enumerate(R[i][j]) if v}
  if T==S:return sorted(S)
  S=T

def witness(row):
 R=row['tensor'];du=dual(R);N=range(8)
 # Use a positive integral character; uniqueness of the positive character
 # makes these dimensions exact, without numerical root selection.
 import itertools
 dims=None
 for g in itertools.combinations(range(1,8),3):
  I={0,*g};rest=[i for i in N if i not in I]
  for twos in itertools.combinations(rest,2):
   ds=[1 if i in I else 2 if i in twos else 6 for i in N]
   if all(sum(R[i][j][k]*ds[k] for k in N)==ds[i]*ds[j] for i in N for j in N):dims=ds;break
  if dims:break
 require(dims is not None,'not exact dimension84type');require(sum(d*d for d in dims)==84,'dimension84')
 adj=generated(R,{k for i in N for k,v in enumerate(R[i][du[i]]) if v});require(adj==list(N),'adjoint not full')
 signs=[]
 for g in range(1,8):
  if dims[g]!=1 or R[g][g]!=[1,0,0,0,0,0,0,0]:continue
  require(all(sum(R[g][i])==1 for i in N),'invertible permutation')
  p=[R[g][i].index(1) for i in N]
  if not all(R[g][i]==R[i][g] for i in N):continue
  fixed=[i for i in N if p[i]==i];n2=sum(dims[i]==2 for i in fixed);n6=sum(dims[i]==6 for i in fixed)
  require(n2 in (0,2) and n6 in (0,2),'baseorbitparity')
  base=sorted([1]*(2+2*n2)+[2]*((2-n2)//2)+[3]*(2*n6)+[6]*((2-n6)//2))
  require(sum(d*d for d in base)==42,'base42dimension')
  signs.append({'object':g,'permutation':p,'fixed_simples':fixed,'base_type':base,'required_fixed_base_invertibles':2})
 return {'id':row['id'],'tensor_sha256':fp(R),'kind':'dimension84_adjoint_rigidity','scope':'general_complex_fusion_category','fp_dimensions':dims,'global_dimension':84,'adjoint_closure':adj,'possible_sign_objects':signs,'theorem':'pipeline/dimension84_obstruction.md'}

def build():
 rows={x['id']:x for x in json.loads((HERE/'census_m3.json').read_text())};enumeration=enumerate_all();stored=json.loads((HERE/'dimension42_group_types.json').read_text());require(enumeration==stored,'dimension42 finite audit differs')
 records=[witness(rows[rid]) for rid in IDS]
 return {'result':'PASS','scope':'general_complex_fusion_category','criterion':'dimension84_adjoint_rigidity','dimension42_enumeration_sha256':hashlib.sha256((HERE/'dimension42_group_types.json').read_bytes()).hexdigest(),'records':records}

@functools.lru_cache(None)
def check_dimension42():
 require(enumerate_all()==json.loads((HERE/'dimension42_group_types.json').read_text()),'dimension42 finite audit differs');return True

def verify(R,c):
 check_dimension42()
 row={'id':c['id'],'tensor':R};require(witness(row)==c,'source witness differs');return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=build();p=HERE/'dimension84_obstruction.json'
 if args.write:p.write_text(json.dumps(result,separators=(',',':'))+'\n')
 else:require(json.loads(p.read_text())==result,'stored dimension84 proof differs')
 print('PASS dimension84',len(result['records']),'general exclusions')
if __name__=='__main__':main()
