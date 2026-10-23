import sys,json,collections,numpy as np,networkx as nx
from pathlib import Path
sys.path.insert(0,str(Path('work/input_audit').resolve()))
from audit import refinement,graph
D=json.load(open('work/literature/anyonwiki_mult1.json'))['data']
I=json.load(open('work/input_audit/tensors.json'))
buckets=collections.defaultdict(list)
for uuid,v in D.items():
 if v['anyonwiki_code'][0] not in (9,10):continue
 N=np.array(v['mult_tab']); key,sigs=refinement(N)
 buckets[key].append((uuid,v,N,sigs))
rows=[]
for id,A in I.items():
 N=np.array(A);key,sigs=refinement(N);matches=[]
 for uuid,v,M,msigs in buckets[key]:
  G,H=graph(N,sigs),graph(M,msigs)
  mt=nx.algorithms.isomorphism.MultiDiGraphMatcher(G,H,node_match=nx.algorithms.isomorphism.categorical_node_match('color',None),edge_match=nx.algorithms.isomorphism.categorical_multiedge_match('role',None))
  if mt.is_isomorphic():
   p=[mt.mapping[('b',i)][1] for i in range(len(N))]
   assert np.array_equal(N,M[np.ix_(p,p,p)])
   matches.append({'input_id':id,'anyonwiki_code':v['anyonwiki_code'],'anyonwiki_uuid':uuid,'input_to_anyonwiki_zero_based':p})
 assert len(matches)==1,(id,matches)
 rows+=matches
 if matches[0]['anyonwiki_code']==[9,1,0,38]:print(matches[0],flush=True)
Path('work/literature/crosswalk.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Matched',len(rows))
