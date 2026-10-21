"""Lift fixed-mass phase rays to necessary inequalities on every integer pattern.

For a phase covector y nonnegative on auxiliary columns, let c_o=min_t yA_ot.
All phase weights are nonnegative and sum to the integral mass m_o, hence
sum_o c_o*m_o <= y*(b-fixed_low). This uses ALL phase types of every allowed
high orbit. Dividing by q and rounding coefficients/RHS down gives an exact
weaker integer inequality for m>=0. Each ray applies to every indicator branch.
"""
from dataclasses import replace
from pathlib import Path
import hashlib,itertools,json,math,sys,time
HERE=Path(__file__).resolve().parent
import prepare as p

def dot(y,col):return sum(y[i]*a for i,a in col.items())
def add_cuts(S,cuts):
 rows=[c['coefficients'] for c in cuts];rhs=[c['rhs']for c in cuts]
 cols=[tuple(c)+tuple(row[j]for row in rows)for j,c in enumerate(S.columns)]
 bounds=list(S.bounds);labels=list(S.column_labels)
 for i,(row,b)in enumerate(zip(rows,rhs)):
  upper=b-sum(min(0,a*u)for a,u in zip(row,S.bounds))
  if upper<0:raise ArithmeticError('cut alone contradicts original bounds')
  col=[0]*(len(S.rhs)+len(rows));col[len(S.rhs)+i]=1
  cols.append(tuple(col));bounds.append(upper);labels.append(('whole_domain_phase_cut_slack',i))
 return replace(S,columns=tuple(cols),rhs=tuple(S.rhs)+tuple(rhs),bounds=tuple(bounds),column_labels=tuple(labels),row_labels=tuple(S.row_labels)+tuple(('whole_domain_phase_cut',i)for i in range(len(rows))),metadata={**S.metadata,'whole_domain_phase_cuts':len(cuts)})

def main(fi):
 start=time.monotonic();ring=p.old.st.load_ring('R8_3_982');C=p.old.cg.cone(ring['tensor'],4,'sts_frame');T=p.old.character_table(ring['tensor'],C.a)
 D,profile=p.old.filtered(C,fi);print('filtered',fi,flush=True)
 S=p.old.f.build(D,T,frame_index=fi);S=p.old.append_galois_balance(S,D,T);S=p.tighten_fusion_bounds(S,D,T);S=p.append_unit_pair_constraints(S,D,T)
 box=p.old.box.propagate(S);Q=p.old.equations.compact(p.old.box.reduced(S,box))
 out={'frame':fi,'tensor_sha256':ring['tensor_sha256'],'columns':Q.columns,'rhs':Q.rhs,'bounds':Q.bounds,'labels':Q.column_labels,'metadata':Q.metadata,'source_lower':box['lower_bounds'],'source_upper':box['upper_bounds']}
 (HERE/f'frame{fi}_system.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 print('built cached',fi,len(Q.rhs),len(Q.columns),flush=True)
 file=p.OLD/'commutative_integer'/f'R8_3_982_frame{fi}_phases_h4.json';old=json.loads(file.read_text())
 rays=[a['certificate']['covector'][:C.nrows]for a in old['attempts']]
 choices=list(map(list,p.old.st.old.ht.indicator_choices(C.R)));fixed=C.column(fi)
 for y in rays:
  if any(dot(y,C.column(j))<0 for j in range(C.high_end,C.nvars)):raise AssertionError('ray is negative on a phase auxiliary column')
 orbitlookup={tuple(sorted((0,)+tuple(C.a['high'][j][0])for j in orbit)):oi for oi,orbit in enumerate(C.orbits)}
 minima=[[0]*len(S.columns)for _ in rays]
 for j,label in enumerate(S.column_labels):
  if label[0]!='high_orbit':continue
  oi=orbitlookup[tuple(sorted(label[2]))]
  vals=[C.column(C.offset+oi*C.nt+ti)for ti in range(C.nt)]
  for k,y in enumerate(rays):minima[k][j]=min(dot(y,v)for v in vals)
 print('all orbit-phase minima exact',fi,'orbits',sum(l[0]=='high_orbit'for l in S.column_labels),flush=True)
 # Use a common positive integer divisor for each ray; all rounded cuts
 # remain rigorously necessary for every nonnegative integral multiplicity.
 divisors=[max(1,max(map(abs,row))//10000)for row in minima]
 rounded=[[a//q for a in row]for row,q in zip(minima,divisors)]
 report={'frame':fi,'tensor_sha256':ring['tensor_sha256'],'scope':'pseudo_unitary_all_high_integer_patterns_all_phase_types','source_phase_receipt_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'phase_rows':C.nrows,'phase_types':C.nt,'global_covectors':rays,'exact_minima':minima,'divisors':divisors,'rounded_coefficients':rounded,'branches':[]}
 import linear
 for bi,ep in enumerate(choices):
  b=[v-fixed.get(i,0)for i,v in enumerate(C.rhs_for(ep))]
  exactrhs=[sum(a*v for a,v in zip(y,b))for y in rays]
  cuts=[{'coefficients':row,'rhs':rhs//q}for row,rhs,q in zip(rounded,exactrhs,divisors)]
  U=add_cuts(S,cuts);bx=p.old.box.propagate(U)
  rec={'indicators':ep,'exact_rhs':exactrhs,'rounded_rhs':[c['rhs']for c in cuts],'box':bx}
  if bx['outcome']=='integer_box_consistent':
   V=p.old.equations.compact(p.old.box.reduced(U,bx));ans=linear.discover(V);rec.update(linear=ans)
   data={'frame':fi,'branch':bi,'indicators':ep,'tensor_sha256':ring['tensor_sha256'],'columns':V.columns,'rhs':V.rhs,'bounds':V.bounds,'labels':V.column_labels,'metadata':V.metadata,'source_lower':bx['lower_bounds'],'source_upper':bx['upper_bounds']}
   (HERE/f'phasecut_f{fi}_b{bi}_system.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
   print('branch',fi,bi,len(V.rhs),len(V.columns),ans['conclusion'],ans.get('numerical_phase_I_objective'),flush=True)
  else:print('branch',fi,bi,bx['outcome'],flush=True)
  report['branches'].append(rec);(HERE/f'phasecut_frame{fi}.json').write_text(json.dumps(report,separators=(',',':'))+'\n')
 print('finished',fi,'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main(int(sys.argv[1]))
