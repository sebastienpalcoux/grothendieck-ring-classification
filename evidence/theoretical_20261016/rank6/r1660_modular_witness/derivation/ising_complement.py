"""A forced Ising-center subrepresentation and its signed spectrum complement.

The profile check proves every occupied central projection is zero or one
simple of Z(Ising). Positive individual target masses make every row
nonzero, so the projection is surjective. Its nine-dimensional row space
is an actual modular subrepresentation by the full-center intertwiner
lemma. Complement central-sign traces are allowed to be negative.
"""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import require
from round4_m8_ising import ising_labels
from representation_cone import append_cone
HERE=Path(__file__).parent

def profile_control():
 R=next(x['N'] for x in json.loads((ROOT/'data/census.json').read_text()) if x['id']=='R6_8_1660')
 labels=ising_labels(R);require(labels==[(1,4)],'Ising labels changed');g,ss=labels[0]
 permitted={(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1)};branches=[]
 for low in (0,1):
  data=json.loads((ROOT/f'research/round5/m8_1660/low{low}_profiles.json').read_text());br=data['branches'][0]
  lowproj=[(v[0],v[g],v[ss]) for v in br['columns']]
  require(all(v in ((1,0,0),(1,1,0)) for v in lowproj),'low projection not a single twist-one simple')
  V=[(0,)+tuple(v) for v in br['high_vectors']];bad=[i for i,v in enumerate(V) if (v[0],v[g],v[ss]) not in permitted]
  for case in br['cases']:
   keep=case['gram_filter']['survivor_indices']
   for ix in keep:
    p=case['profiles'][ix]
    require(all(not p[i] for i in bad),'occupied column can project to several Ising-center simples')
    require(sum(p[i]*V[i][ss] for i in range(len(V)))==8,'wrong number of sigma objects')
    require(sum(p[i]*V[i][g] for i in range(len(V)))==4,'wrong number of g objects')
   branches.append({'low':low,'labelling':case['labelling'],'profiles_checked':len(keep),'zero_occupied_columns_required':bad})
 return {'id':'R6_8_1660','passed':True,'scope':'every retained profile has only zero or single-simple Ising-center projections','Ising_labels':[g,ss],'target_rank':9,'forced_row_gram_scalar':2,'branches':branches}

def ising_spectrum(sigma_roots):
 require(len(sigma_roots)==4 and len(set(sigma_roots))==4,'wrong Ising root set')
 spectrum=[0]*48;spectrum[0]=3;spectrum[24]=2
 for k in sigma_roots:
  require(0<=k<48 and k%3==0 and k%2==1,'not a primitive sixteenth root');spectrum[k]=1
 return spectrum

def append_complement(A,b,high_labels,sigma_roots,low_count=6):
 """Use only after profile_control applies and low self-duality is proved.

 Full T counts are high_counts + six twist-one low objects. Subtract the
 known Ising-center spectrum. Its central element is +I, so subtract that
 same spectrum from the full signed-trace lower bounds. In particular the
 lower bounds at sigma roots and -1 become -1 and -2, respectively.
 """
 low=[low_count]+[0]*47;AA,bb,meta=append_cone(A,b,high_labels,low,low)
 known=ising_spectrum(sigma_roots);start=len(bb)-96
 for k in range(48):
  bb[start+2*k]+=known[k]
  bb[start+2*k+1]-=known[k]
 meta.update(known_subrepresentation='Z(Ising)',subrepresentation_rank=9,subtracted_T_spectrum=known,complement_T_offset=[a-b for a,b in zip(low,known)],complement_signed_trace_lower_bounds=[a-b for a,b in zip(low,known)])
 return AA,bb,meta

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();out=profile_control();p=HERE/'ising_projection_rank.json'
 if args.verify:require(out==json.loads(p.read_text()),'Ising projection rank-control mismatch')
 else:p.write_text(json.dumps(out,indent=2)+'\n')
 paths={Path(__file__).resolve(),p,ROOT/'data/census.json',HERE/'representation_cone.py'}|{ROOT/f'research/round5/m8_1660/low{i}_profiles.json' for i in (0,1)}
 for mod in list(sys.modules.values()):
  name=getattr(mod,'__file__',None)
  if name:
   q=Path(name).resolve()
   if q.is_relative_to(ROOT) and q.suffix=='.py':paths.add(q)
 receipt={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'profiles_checked':sum(b['profiles_checked'] for b in out['branches']),'files_sha256':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(paths)}};(HERE/'ising_projection_rank_replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='files_sha256'},sort_keys=True))
