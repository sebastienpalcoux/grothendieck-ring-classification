"""Exact replay of a finite-domain certificate and its final bounded separator.

The pruning checker deliberately does not call the discovery propagator.
Optional --rebuild reconstructs each necessary system from the fusion tensor.
"""
from pathlib import Path
import argparse,hashlib,json,math,sys
from domain_probe import rows_for
HERE=Path(__file__).resolve().parent

def require(p,msg):
 if not p:raise AssertionError(msg)

def independent_prune_check(rows,bounds,proof,initial_domains=None):
 domains=[set(range(u+1))for u in bounds] if initial_domains is None else[set(v)for v in initial_domains]
 deleted=0
 for number,(i,j,removed) in enumerate(proof['steps']):
  row=rows[i];a=row[j];b=row[-1];require(a!=0,'zero deletion coefficient')
  require(removed and set(removed)<=domains[j],'invalid deletion list')
  choices=[sorted(c*x for x in domains[k])for k,c in enumerate(row[:-1])if c and k!=j]
  low=sum(v[0]for v in choices);high=sum(v[-1]for v in choices)
  modulus=0
  for values in choices:
   for v in values[1:]:modulus=math.gcd(modulus,v-values[0])
  unresolved=[x for x in removed if low<=b-a*x<=high and (modulus==0 or (b-a*x-low)%modulus==0)]
  if unresolved:
   require(high-low<=30000,'discovery convolution range exceeded')
   reachable=1
   for values in choices:
    shifts={v-values[0]for v in values};new=0
    for shift in shifts:new |= reachable<<shift
    reachable=new
   require(all(((reachable>>(b-a*x-low))&1)==0 for x in unresolved),'a removed value has an exact row completion')
  domains[j].difference_update(removed);deleted+=len(removed)
  require(domains[j],'empty surviving domain in consistent proof')
 require([sorted(d)for d in domains]==proof['domains'],'final domains differ')
 require(deleted==proof['deletions'],'deletion total differs')
 require(hashlib.sha256(repr([tuple((i,j,r))for i,j,r in proof['steps']]).encode()).hexdigest()==proof['step_sha256'],'step digest differs')
 return domains

def main(rebuild=False):
 d,rows,rank=rows_for('frame0')
 proof=json.loads((HERE/'frame0_domains.json').read_text())
 require(hashlib.sha256(repr(rows).encode()).hexdigest()==proof['matrix_sha256'],'row matrix differs')
 domains=independent_prune_check(rows,d['bounds'],proof)
 certificate=json.loads((HERE/'frame0_branch.json').read_text())
 require(certificate['nodes']==1 and certificate['status']=='exact_bounded_integer_obstruction','not a complete one-leaf proof')
 leaf=certificate['tree'];require(leaf['status']=='exact_bounded_linear_obstruction','missing bounded separator')
 rr=rows[len(d['rhs']):len(d['rhs'])+rank];y=leaf['covector'];require(len(y)==len(rr),'dual size mismatch')
 target=sum(v*row[-1]for v,row in zip(y,rr));cs=[sum(v*row[j]for v,row in zip(y,rr))for j in range(len(domains))]
 upper=sum(max(c*min(domain),c*max(domain))for c,domain in zip(cs,domains))
 require(target==leaf['rhs_value'] and upper==leaf['box_upper'] and target>upper,'strict exact separator fails')
 frames=[0]
 path=HERE/'frame1_system.json'
 if path.exists():
  d1=json.loads(path.read_text())
  for k in('columns','rhs','bounds','labels'):require(d[k]==d1[k],'frame1 mathematical system differs: '+k)
  frames.append(1)
 if rebuild:
  import prepare as p
  ring=p.old.st.load_ring('R8_3_982');C=p.old.cg.cone(ring['tensor'],4,'sts_frame');T=p.old.character_table(ring['tensor'],C.a)
  require(len(C.frames)==4,'complete distinguished-frame count differs')
  for fi in frames:
   saved=json.loads((HERE/f'frame{fi}_system.json').read_text())
   D,_=p.old.filtered(C,fi);S=p.old.f.build(D,T,frame_index=fi)
   S=p.old.append_galois_balance(S,D,T);S=p.tighten_fusion_bounds(S,D,T);S=p.append_unit_pair_constraints(S,D,T)
   box=p.old.box.propagate(S);Q=p.old.equations.compact(p.old.box.reduced(S,box))
   require(saved['tensor_sha256']==ring['tensor_sha256'],'source tensor differs')
   for key,value in [('columns',Q.columns),('rhs',Q.rhs),('bounds',Q.bounds),('labels',Q.column_labels),('metadata',Q.metadata),('source_lower',box['lower_bounds']),('source_upper',box['upper_bounds'])]:
    require(saved[key]==json.loads(json.dumps(value)),'rebuilt source differs '+str(fi)+' '+key)
   print('PASS full tensor-to-necessary-system source reconstruction',fi,flush=True)
 out={'id':'R8_3_982','tensor_sha256':d['tensor_sha256'],'scope':'pseudo_unitary_fixed_frame_integer_center_necessary_system','frames_excluded':frames,'complete_low_frames':4,'source_system_rows':len(d['rhs']),'source_system_variables':len(d['bounds']),'rational_augmented_rank':rank,'domain_deletions':proof['deletions'],'deletion_steps':len(proof['steps']),'fixed_variables_after_domain_propagation':sum(len(v)==1 for v in domains),'dual_rhs':target,'dual_box_upper':upper,'strict_gap':target-upper,'full_source_rebuilt':rebuild,'conclusion':'these_fixed_frames_have_no_integer_center_completion; other_frames_unresolved'}
 (HERE/'verified_frame01.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rebuild',action='store_true');args=ap.parse_args();main(args.rebuild)
