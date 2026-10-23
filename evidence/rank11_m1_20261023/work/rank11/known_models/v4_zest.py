"""Bilinear V4 zesting of the unitary SO(8)_2 category."""
from standard import *

def construct(parameters):
 T=so8_level2();g=[0]*5+[1,1,2,2,3,3];n=11
 a,b,c,d=parameters
 lam=lambda x,y: (a if(x&1)and(y&1)else 0)^(b if(x&1)and(y&2)else 0)^(c if(x&2)and(y&1)else 0)^(d if(x&2)and(y&2)else 0)
 act=[[T[h][k].index(1)for k in range(n)]for h in range(4)]
 S=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,j,k in itertools.product(range(n),repeat=3):S[i][j][act[lam(g[i],g[j])][k]]=T[i][j][k]
 return S,[[lam(x,y)for y in range(4)]for x in range(4)],g

def main():
 data=targets();buckets=collections.defaultdict(list)
 for rid,R in data.items():buckets[coarse(R)].append((rid,R))
 out={};all_attempts=[]
 for pp in itertools.product(range(4),repeat=4):
  T,lam,g=construct(pp);hits=[]
  for rid,R in buckets[coarse(T)]:
   p=based_iso(R,T)
   if p is None:continue
   hits.append(rid)
   if rid not in out:
    validate(T)
    out[rid]={'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[{'name':f'V4-bilinear zest of SO(8)_2, parameters{pp}','constructor':'v4_so8_zest','parameters':{'bilinear_parameters':pp,'cocycle':lam,'grading':g,'base_tensor':so8_level2()},'model_tensor':T,'basis_map_source_to_model':p,'reference':'Gustafson--Rowell--Ruan, Section3.3 (SO8_2 fusion rules and Tannakian invertibles); associative zesting along the V4 grading with coefficients in the neutral Tannakian V4'}]}
   print(pp,rid,flush=True)
  if not hits:raise ValueError(('constructed model absent fromcensus',pp))
  all_attempts.append({'parameters':pp,'matches':hits})
 rows=sorted(out.values(),key=lambda x:int(x['id'].split('_')[-1]));(HERE/'v4_zest_models.json').write_text(json.dumps(rows,indent=2)+'\n');(HERE/'v4_zest_attempts.json').write_text(json.dumps(all_attempts,indent=2)+'\n')
 print('TOTAL',len(rows),list(out),flush=True)
if __name__=='__main__':main()
