"""Finite row enumeration and exact integer quartic completion witnesses.

HiGHS is used only to locate candidates.  Successful answers are rechecked
over the rationals against the FULL restriction and Gram matrices.  A
solver infeasibility report is not accepted as a mathematical exclusion.
"""
from charged_quartic_pair import *
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint

def candidates(x,H):
 piv=list(H.rref()[1]);Hp=H.extract(piv,piv);Hi=Hp.inv();B=Hi*H[piv,:]
 ranges=[]
 for j in piv:
  h=H[j,j];rad=math.isqrt(int(s.ceiling(h)))+1
  ranges.append(range(max(0,int(s.floor(x[j]-rad))),int(s.ceiling(x[j]+rad))+1))
 rows=[]
 for ns in product(*ranges):
  delta=s.Matrix(1,len(piv),[n-x[j] for j,n in zip(piv,ns)])
  if (delta*Hi*delta.T)[0]>1:continue
  row=x+delta*B
  if all(z.q==1 and z>=0 for z in row):rows.append([int(z) for z in row])
 return rows,piv

def main():
 source=read(P/'source.json');domain=read(P/'gram_cubic.json');charged=read(HERE/'charged_quartic_pair.json')
 fermion=read(P/'r941_charges.json')['solutions'];involution=read(HERE/'involution_pair_gram.json');results=[]
 for rec,previous,invresult in zip(source['records'],charged['records'],involution['records']):
  semion=rec['id'].endswith('928');V=s.Matrix.hstack(*(s.Matrix((0,)+tuple(v)) for v in rec['canonical_high_vectors'][:40]));cases=[]
  invcases={c['allocation']:c for c in invresult['cases']}
  for c in previous['cases']:
   if not c.get('survives') or not c['prior_final_survivor']:continue
   a=c['allocation'];ix=c['pattern'];sec=c['sectors'][0];X=matrix(sec['Xtypes']);H=matrix(sec['H']);T=matrix(sec['T']);G=matrix(sec['G'])
   if semion:counts=[n//2 for n in domain['patterns'][ix][:40]]
   else:
    need(invcases[a]['sectors'][0]['antisymmetric_rank']==0,'fermion orbit constancy')
    counts=fermion[a]['plus_pairs'];H/=2;T/=2;G/=2
   active=[k for k,n in enumerate(counts) if n];allrows={};variables=[]
   for k in active:
    rows,piv=candidates(X[k,:],H);allrows[k]=rows
    variables.extend((k,row) for row in rows)
   # Integer linear equations: type counts, selected restriction columns,
   # and the Gram on the independent residual coordinates.
   rp=list((V*s.diag(*counts)*V.T).rref()[1]);gp=list(cwr(piv,2));rhs=[counts[k] for k in active]+[T[t,j] for t in rp for j in piv]+[G[i,j] for i,j in gp]
   A=[]
   for k in active:A.append([int(v==k) for v,row in variables])
   for t in rp:
    for j in piv:A.append([V[t,k]*row[j] for k,row in variables])
   for i,j in gp:A.append([row[i]*row[j] for k,row in variables])
   need(all(v.q==1 for v in map(s.Rational,rhs)),'integral system RHS')
   AA=np.array(A,dtype=float);bb=np.array(rhs,dtype=float)
   opt=milp(np.zeros(len(variables)),integrality=np.ones(len(variables)),bounds=Bounds(np.zeros(len(variables)),np.array([counts[k] for k,row in variables])),constraints=LinearConstraint(AA,bb,bb),options={'time_limit':30})
   case={'allocation':a,'pattern':ix,'residual_rank':len(piv),'rows_by_type':{str(k):rows for k,rows in allrows.items()},'solver_status':int(opt.status),'solver_message':str(opt.message),'variable_count':len(variables),'equation_count':len(rhs)}
   if opt.x is not None:
    ns=[int(round(t)) for t in opt.x]
    if all(n>=0 for n in ns) and s.Matrix(A)*s.Matrix(ns)==s.Matrix(rhs):
     rT=s.zeros(8,T.cols);rG=s.zeros(G.rows,G.cols);cc=[0]*40;witness=[]
     for n,(k,row) in zip(ns,variables):
      if not n:continue
      rr=s.Matrix(1,len(row),row);rT+=n*V[:,k]*rr;rG+=n*rr.T*rr;cc[k]+=n
      witness.append({'type':k,'multiplicity':n,'pair_fusion_coefficients':row})
     need(cc==counts and rT==T and rG==G,'exact full witness')
     case.update(outcome='exact_integer_witness',witness=witness)
    else:case['outcome']='inconclusive_nonexact_solver_output'
   else:case['outcome']='inconclusive_solver_no_witness'
   cases.append(case)
  results.append({'id':rec['id'],'cases':cases})
 files=[P/'source.json',P/'gram_cubic.json',P/'r941_charges.json',HERE/'charged_quartic_pair.json',HERE/'involution_pair_gram.json']
 print(json.dumps({'kind':'exact_integer_pair_completions','records':results,'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in files},'verifier_sha256':digest(Path(__file__)),'scope':'Witnesses satisfy only the stated pair-product constraints; they are not fusion rings or categories. Solver failures are inconclusive.'},indent=2))
if __name__=='__main__':main()
