"""Independent exact replay of whole-domain phase and central-semion follow-up.

--rebuild additionally reconstructs sources and every full-domain phase
minimum from the tensor. No numerical solver is called by this verifier.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,sys
from domain_probe import rows_for
from verify_frame01 import independent_prune_check,require
HERE=Path(__file__).resolve().parent

def read(name):return json.loads((HERE/name).read_text())
def check_dual(rows,ineq,domains,cert):
 y=cert['equality_covector'];z=cert['inequality_covector'];require(len(y)==len(rows)and len(z)==len(ineq)and all(a<=0 for a in z),'invalid hybrid covector')
 c=[sum(a*r[j]for a,r in zip(y,rows))+sum(a*r[j]for a,r in zip(z,ineq))for j in range(len(domains))]
 b=sum(a*r[-1]for a,r in zip(y,rows))+sum(a*r[-1]for a,r in zip(z,ineq));upper=sum(max(a*min(d),a*max(d))for a,d in zip(c,domains))
 require(b==cert['rhs_value']and upper==cert['box_upper']and b>upper,'hybrid separator fails')
 return b-upper

def main(rebuild=False):
 d,rows,rank=rows_for('frame2');d3=read('frame3_system.json')
 for k in('columns','rhs','bounds','labels','source_lower','source_upper'):require(d[k]==d3[k],'frame2/3 system differs '+k)
 baseproof=read('frame2_domains.json');base=independent_prune_check(rows,d['bounds'],baseproof)
 phase=read('phasecut_frame2.json');lo=d['source_lower'];keep=d['metadata']['source_metadata']['retained_indices'];pos={j:k for k,j in enumerate(keep)}
 for exact,divisor,rounded in zip(phase['exact_minima'],phase['divisors'],phase['rounded_coefficients']):require(divisor>0 and [x//divisor for x in exact]==rounded,'invalid downward cut rounding')
 for b in phase['branches']:require([a//q for a,q in zip(b['exact_rhs'],phase['divisors'])]==b['rounded_rhs'],'invalid downward rhs rounding')
 # Cached compact phase-cut systems certify six entire indicator branches.
 sys.path.insert(0,str(HERE.parents[2]/'evidence/rank8_frontier_20261021/commutative_integer'))
 from features import System
 import linear
 excluded=[]
 for bi,b in enumerate(phase['branches']):
  if b.get('linear',{}).get('conclusion')=='exact_bounded_linear_obstruction':
   c=read(f'phasecut_f2_b{bi}_system.json');S=System(tuple(map(tuple,c['columns'])),tuple(c['rhs']),tuple(c['bounds']),(),tuple(map(tuple,c['labels'])),c['metadata']);linear.verify(S,b['linear']['certificate']);excluded.append(bi)
 require(excluded==[1,2,3,5,6,7],'expected whole-domain indicator coverage differs')
 central,cr,rrank=rows_for('central_dual_frame2');require(central['central_action_source']['central_g_domain']==[1],'unique central lift missing')
 gi=central['central_action_source']['central_g_original_index'];require([lo[gi]+v for v in base[pos[gi]]]==[1],'central lift not forced by independently checked domains')
 dom=[set(v)for v in base];parities=central['central_action_parities']
 for j,residue,_ in parities:dom[j]={v for v in dom[j]if v%2==residue};require(dom[j],'parity empties domain')
 cp=read('central_dual_frame2_result.json');final=independent_prune_check(cr,central['bounds'],cp['propagation'],dom)
 crr=cr[len(central['rhs']):len(central['rhs'])+rrank];b0=cp['branches'][0];require(b0['branch']==0 and b0['domain_propagation']['stages']==[],'unexpected hybrid pruning requires additional replay')
 inequalities=[[c[j]for j in keep]+[b-sum(a*v for a,v in zip(c,lo))]for c,b in zip(phase['rounded_coefficients'],phase['branches'][0]['rounded_rhs'])]
 gap=check_dual(crr,inequalities,final,b0['linear'])
 # Replay the complete residual whole-domain rational phase witness.
 J=read('joint_phase_system.json');jr=read('joint_phase_result.json');cols=[{int(i):a for i,a in c.items()}for c in J['columns']];rhs=J['rhs'];total=[Q(0)]*len(rhs)
 for j,w in zip(jr['certificate']['indices'],map(Q,jr['certificate']['weights'])):
  require(0<=j<len(cols)and w>=0,'invalid joint rational support')
  for i,a in cols[j].items():total[i]+=a*w
 require(total==rhs and jr['status']=='exact_bounded_rational_joint_survivor','exact full-phase rational witness fails')
 integer_status=None
 if(HERE/'joint_integer_result.json').exists():
  ji=read('joint_integer_result.json');integer_status=ji['status']
  if ji['status']=='exact_integer_core_and_rational_full_phase_survivor':
   x=ji['integer_core_values'];sx=ji['shifted_integer_core_values'];require(len(x)==J['core_variables']and all(isinstance(v,int)and v in final[j]for j,v in enumerate(x)),'invalid integral joint core')
   require(all(x[j]%2==r for j,r,_ in parities),'joint core parity fails')
   require([v+J['original_bounds'][j][0]for j,v in enumerate(sx)]==x,'joint core shift fails')
   total=[Q(0)]*len(rhs)
   for j,w in enumerate(sx):
    for i,a in cols[j].items():total[i]+=a*w
   for j,w in zip(ji['phase_certificate']['indices'],map(Q,ji['phase_certificate']['weights'])):
    require(w>=0,'negative conditional phase weight')
    for i,a in cols[j+J['core_variables']].items():total[i]+=a*w
   require(total==rhs,'joint integer/full-phase witness fails exact equality')
 if rebuild:
  sys.path.insert(0,str(HERE))
  import prepare as p
  from lift_phase_cuts import add_cuts
  ring=p.old.st.load_ring('R8_3_982');C=p.old.cg.cone(ring['tensor'],4,'sts_frame');T=p.old.character_table(ring['tensor'],C.a)
  require(len(C.frames)==4 and C.column(2)==C.column(3),'full phase-frame transfer fails')
  systems={}
  for fi in(2,3):
   D,_=p.old.filtered(C,fi);S=p.old.f.build(D,T,frame_index=fi);S=p.old.append_galois_balance(S,D,T);S=p.tighten_fusion_bounds(S,D,T);S=p.append_unit_pair_constraints(S,D,T);systems[fi]=S
   box=p.old.box.propagate(S);V=p.old.equations.compact(p.old.box.reduced(S,box));saved=read(f'frame{fi}_system.json')
   for key,value in [('columns',V.columns),('rhs',V.rhs),('bounds',V.bounds),('labels',V.column_labels),('metadata',V.metadata),('source_lower',box['lower_bounds']),('source_upper',box['upper_bounds'])]:require(saved[key]==json.loads(json.dumps(value)),'source rebuild mismatch '+str(fi)+' '+key)
   print('PASS full source reconstruction',fi,flush=True)
  S=systems[2];oldfile=p.OLD/'commutative_integer/R8_3_982_frame2_phases_h4.json';old=json.loads(oldfile.read_text());rays=[a['certificate']['covector'][:C.nrows]for a in old['attempts']]
  require(rays==phase['global_covectors'],'phase covector source differs')
  dot=lambda y,col:sum(y[i]*a for i,a in col.items())
  for y in rays:require(all(dot(y,C.column(j))>=0 for j in range(C.high_end,C.nvars)),'negative phase auxiliary pairing')
  lookup={tuple(sorted((0,)+tuple(C.a['high'][j][0])for j in orbit)):oi for oi,orbit in enumerate(C.orbits)}
  for j,label in enumerate(S.column_labels):
   if label[0]=='high_orbit':
    oi=lookup[tuple(sorted(label[2]))];columns=[C.column(C.offset+oi*C.nt+ti)for ti in range(C.nt)]
    for k,y in enumerate(rays):require(min(dot(y,col)for col in columns)==phase['exact_minima'][k][j],'full phase minimum differs')
   else:require(all(row[j]==0 for row in phase['exact_minima']),'nonmass column in phase cut')
  choices=list(map(list,p.old.st.old.ht.indicator_choices(C.R)));fixed=C.column(2)
  for bi,(ep,b)in enumerate(zip(choices,phase['branches'])):
   require(ep==b['indicators'],'indicator coverage differs');rhs0=[v-fixed.get(i,0)for i,v in enumerate(C.rhs_for(ep))]
   require([sum(a*v for a,v in zip(y,rhs0))for y in rays]==b['exact_rhs'],'phase cut rhs differs')
   cuts=[{'coefficients':c,'rhs':r}for c,r in zip(phase['rounded_coefficients'],b['rounded_rhs'])];U=add_cuts(S,cuts);box=p.old.box.propagate(U);require(box==b['box'],'phase cut source box differs');V=p.old.equations.compact(p.old.box.reduced(U,box));saved=read(f'phasecut_f2_b{bi}_system.json')
   for key,value in [('columns',V.columns),('rhs',V.rhs),('bounds',V.bounds),('labels',V.column_labels),('metadata',V.metadata)]:require(saved[key]==json.loads(json.dumps(value)),'whole cut compact rebuild differs '+str(bi)+' '+key)
  print('PASS all whole-domain phase minima and all eight source cut systems',flush=True)
  from verify_joint_source import verify as verify_joint_source
  joint_source=verify_joint_source(C,ring,central,final)
  print('PASS independent central action and full joint domain source',joint_source,flush=True)
 out={'id':'R8_3_982','tensor_sha256':d['tensor_sha256'],'frames_2_3_identical_necessary_systems':True,'core_domain_deletions':baseproof['deletions'],'whole_pattern_indicator_branches_excluded':excluded,'additional_semion_branch_excluded':0,'semion_branch_separator_gap':gap,'remaining_indicator_branch':4,'remaining_indicators':phase['branches'][4]['indicators'],'unique_central_g_multiplicity':1,'semion_and_duality_parity_variables':len(parities),'full_phase_high_orbits':J['high_orbits'],'full_phase_types':J['phase_types'],'full_phase_rows':len(J['rhs']),'full_phase_variables':len(J['columns']),'full_phase_rational_witness':'exactly_verified','joint_integer_status':integer_status,'source_and_all_phase_minima_rebuilt':rebuild,'scope':'pseudo_unitary_necessary_systems_only_not_a_model_or_ring_exclusion'}
 (HERE/'verified_followup.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rebuild',action='store_true');a=ap.parse_args();main(a.rebuild)
