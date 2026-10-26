from all_graph_twists import candidate,second_cocycle,ROOT,monomial
import common,itertools,json,time
import numpy as np

def main():
 start=time.monotonic();sources=json.load(open(ROOT/'source_tensors.json'));meta=json.load(open(ROOT/'source_meta.json'));saved=json.load(open(ROOT/'all_graph_twists.json'))
 common.require(len(sources)==16,'sixteen dimension120 inputs')
 premises=[]
 for rid,R in sources.items():
  common.validate(R);common.require(common.sha(R)==meta[rid]['tensor_sha256'],'source hash')
  N=np.array(R,dtype=int);d=np.array(meta[rid]['dimensions'],dtype=int)
  common.require(sorted(d)==[1]*4+[2]*4+[5]*4 and int(d@d)==120,'exact dimension120 type')
  common.require(all(np.array_equal(N[i]@d,d[i]*d)for i in range(12)),'exact positive dimension character')
  I=[i for i in range(12)if d[i]==1];T=[i for i in range(12)if d[i]==2];F=[i for i in range(12)if d[i]==5];D=I+T
  common.require(all(not N[i,j,k]for i,j in itertools.product(D,repeat=2)for k in F),'dimension20 fusion subring')
  bs=[g for g in I if g and N[g,g,0]and all(N[g,t,t]and N[t,g,t]for t in T)]
  common.require(len(bs)==1,'unique common cyclic stabilizer');b=bs[0]
  common.require(all(not N[b,f,f]and np.array_equal(N[b,f],N[f,b])for f in F),'equalfreeleft/right involutions on5s')
  premises.append(dict(id=rid,common_involution=b,dimension20_basis=D,dimension5_basis=F))
 G,H,lam=candidate();W,cert=second_cocycle(G,H);found={};records=[]
 for row in saved:
  a,b=row['parameters'];common.require(row['group_table']==G and row['subgroup']==H and row['schur_cocycle']==lam and row['transfer_cocycle']==W.tolist()and row['transfer_certificate']==cert,'reconstructed categorical parameters')
  w=lambda x,y,z:10*((a*(int(W[x//2,y//2,z//2])+(x%2)*(y%2)*(z%2))+b*(lam[x//2][y//2]+(x%2)*(y%2))*(z%2))%2)
  common.require(all(w(x,y,z)==0 for x,y,z in itertools.product(H,repeat=3)),'subgroup algebra1 actually associative')
  R,info=monomial.construct(G,H,w);common.require(R==row['model_tensor']and json.loads(json.dumps(info))==row['info'],'replayed exact balanced tensor calculation')
  common.validate(R);hits=[]
  for rid,S in sources.items():
   p=common.based_iso(S,R)
   if p is not None:hits.append(rid);found[rid]=list(row['parameters'])
  common.require(hits==[x['id']for x in row['matches']],'exhaustive16source match')
  for bind in row['matches']:
   p=bind['basis_map_source_to_model'];S=sources[bind['id']];common.require(common.sha(S)==bind['tensor_sha256']and all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all1728 recorded coefficients')
  records.append(dict(parameters=[a,b],matches=hits));print('PASS',a,b,hits,flush=True)
 expected={'R12_1_25','R12_1_142','R12_1_361','R12_1_444'};common.require(set(found)==expected,'four realized models')
 excluded=sorted(set(sources)-expected,key=lambda x:int(x.rsplit('_',1)[1]));common.require(len(excluded)==12,'twelve exclusion consequences')
 receipt=dict(status='PASS',normal_python=__debug__,new_modeled=sorted(expected-{'R12_1_25'}),new_excluded=excluded,remaining_unresolved=[],source_premises=premises,finite_cohomological_outputs=records,scope='General complex exclusion uses the categorical converse and exhaustive cohomology proof in theory.md, not a classification of all dimension120 categories.',seconds=time.monotonic()-start)
 (ROOT/('verification.json'if __debug__ else'verification_optimized.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items()if k not in ['source_premises','finite_cohomological_outputs']},indent=2))
if __name__=='__main__':main()
