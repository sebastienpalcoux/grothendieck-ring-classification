"""Whole-domain central-semion integer-core / continuous-phase coupling.

All currently allowed high restriction types and all height4 phase types
are included. Exact outputs are certificates for this necessary system,
not categorical models.
"""
from pathlib import Path
import json,sys,time
from fractions import Fraction
from domain_probe import rows_for
HERE=Path(__file__).resolve().parent
import prepare as p

class Joint:
 def __init__(self,columns,rhs):self.columns=columns;self.rhs=rhs;self.nvars=len(columns);self.nrows=len(rhs)
 def column(self,j):return self.columns[j]

def main():
 start=time.monotonic();fi=2;bi=4
 d,derived,rank=rows_for('central_dual_frame2');rr=derived[len(d['rhs']):len(d['rhs'])+rank]
 dom=json.loads((HERE/'central_dual_frame2_result.json').read_text())['propagation']['domains'];keep=d['metadata']['source_metadata']['retained_indices'];pos={j:k for k,j in enumerate(keep)};low=d['source_lower'];n=len(dom)
 source=p.old.st.load_ring('R8_3_982');C=p.old.cg.cone(source['tensor'],4,'sts_frame');profiles=json.loads((p.OLD/'commutative_integer/R8_3_982_profile.json').read_text());P=profiles['records'][fi]
 vectors={r['index']:(0,)+tuple(r['vector'])for r in P['high_vectors']};orbits=[tuple(vectors[i]for i in o['indices'])for o in P['duality_orbits']]
 lookup={tuple(sorted((0,)+tuple(C.a['high'][i][0])for i in o)):j for j,o in enumerate(C.orbits)}
 highs=[]
 for j,o in enumerate(orbits):
  upper=low[j]+max(dom[pos[j]])if j in pos else low[j]
  if upper:highs.append((j,lookup[tuple(sorted(o))],upper))
 ep=list(p.old.st.old.ht.indicator_choices(C.R))[bi];fixed=C.column(fi)
 rhs=[row[-1]for row in rr]+[low[j]for j,oi,u in highs]+[v-fixed.get(i,0)for i,v in enumerate(C.rhs_for(ep))]
 cols=[{i:row[j]for i,row in enumerate(rr)if row[j]}for j in range(n)];bounds=[(min(v),max(v))for v in dom];labels=[('integer_core',j)for j in range(n)]
 for h,(j,oi,u)in enumerate(highs):
  if j in pos:cols[pos[j]][rank+h]=-1
  for ti in range(C.nt):
   col={rank+len(highs)+i:a for i,a in C.column(C.offset+oi*C.nt+ti).items()};col[rank+h]=1;cols.append(col);bounds.append((0,u));labels.append(('high_phase',j,oi,ti))
 for globalj in range(C.high_end,C.nvars):cols.append({rank+len(highs)+i:a for i,a in C.column(globalj).items()});bounds.append((0,None));labels.append(('phase_auxiliary',globalj))
 # Shift finite lower bounds and introduce nonnegative complement variables.
 originalcount=len(cols)
 for j,(l,u)in enumerate(bounds):
  if l:
   for i,a in cols[j].items():rhs[i]-=a*l
  if u is not None:
   row=len(rhs);rhs.append(u-l);cols[j][row]=1;cols.append({row:1});labels.append(('bound_complement',j))
 record={'tensor_sha256':source['tensor_sha256'],'frame':fi,'indicators':list(ep),'rank':rank,'core_variables':n,'high_orbits':len(highs),'phase_types':C.nt,'columns':cols,'rhs':rhs,'labels':labels,'original_bounds':bounds,'unshifted_variables':originalcount,'scope':'pseudo_unitary_whole_domain_central_semion_phase_relaxation'}
 (HERE/'joint_phase_system.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
 print('joint system',len(rhs),len(cols),'highorbits',len(highs),'seconds',time.monotonic()-start,flush=True)
 J=Joint(cols,rhs);rows=p.old.cg.active_rows(J,range(J.nvars));ans,diag=p.old.cg.phase_one(rows,rhs,J.nvars,120)
 report={'numerical':diag,'status':'no_exact_conclusion'}
 if ans.success:
  if ans.fun<1e-7:
   primal=p.old.cg.exact_feasible(J,list(range(J.nvars)),rhs,ans.x[:J.nvars])
   if primal is not None:
    weights=list(map(Fraction,primal['weights']));total=[Fraction(0)]*J.nrows
    for j,w in zip(primal['indices'],weights):
     if w<0:raise AssertionError('negative phase weight')
     for i,a in cols[j].items():total[i]+=w*a
    if total!=rhs:raise AssertionError('exact joint primal failed')
    report.update(status='exact_bounded_rational_joint_survivor',certificate=primal)
  else:
   y=p.old.cg.reuse_dual(rows,rhs,J.nvars,ans)
   if y is None:y=p.old.st.old.farkas(rows,rhs,J.nvars,True)
   if y is not None:
    if any(sum(y[i]*a for i,a in col.items())<0 for col in cols):raise AssertionError('negative joint dual column')
    value=sum(y[i]*b for i,b in enumerate(rhs))
    if value>=0:raise AssertionError('nonnegative joint dual rhs')
    report.update(status='exact_joint_phase_obstruction',certificate={'covector':y,'rhs_value':value})
 (HERE/'joint_phase_result.json').write_text(json.dumps(report,separators=(',',':'))+'\n');print(report['status'],diag,'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
