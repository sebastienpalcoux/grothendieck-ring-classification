"""Exact primal/dual certification for finite trace relaxations."""
import math,sys
from fractions import Fraction
import central_support as c
sys.path.insert(0,str(c.OLD.parent/'criteria'))
import global_induction as global_engine

def decide(A,b):
    import numpy as np
    from scipy.optimize import linprog
    AA=np.asarray(A,dtype=float);bb=np.asarray(b,dtype=float)
    # Natural positive-row bounds normalize large tensor-power eigenspaces.
    # Without this, order12 counts can exceed small coefficients by 1e12.
    limits=[None]*len(A[0])
    for row,bb0 in zip(A,b):
        if bb0<0 or any(v<0 for v in row):continue
        for j,v in enumerate(row):
            if v>0:
                bound=Fraction(bb0,v)
                if bound>0 and (limits[j] is None or bound<limits[j]):limits[j]=bound
    column_scale=np.asarray([float(v) if v else 1. for v in limits]); AA=AA*column_scale[None,:]
    scale=np.maximum(1,np.maximum(np.max(np.abs(AA),axis=1),np.abs(bb)))
    sol=linprog(np.zeros(len(A[0])),A_eq=AA/scale[:,None],b_eq=bb/scale,bounds=(0,None),method='highs',options={'time_limit':45})
    report={'numeric_status':int(sol.status),'numeric_message':sol.message}
    if sol.success:
        for threshold in (1e-7,1e-9,1e-11):
            support=np.flatnonzero(sol.x>threshold).tolist()
            C=c.s.Matrix([[row[j] for j in support] for row in A]);rhs=c.s.Matrix(b)
            try:z,params=C.gauss_jordan_solve(rhs)
            except ValueError:continue
            if params.rows:continue
            if any(v<0 for v in z):continue
            c.require(C*z==rhs,'primal equation exact')
            report.update(status='exact_feasible_relaxation',primal=[[j,str(v)] for j,v in zip(support,z) if v])
            return report
        report['status']='numerically_feasible_no_exact_reconstruction';return report
    sparse=[{j:v for j,v in enumerate(row) if v} for row in A]
    for phase_one in (True,False):
        ray=global_engine.farkas(sparse,b,len(A[0]),phase_one)
        if ray is not None:
            c.w.core.check_farkas(A,b,ray)
            report.update(status='exact_infeasible_relaxation',ray=ray);return report
    report['status']='undecided_numeric';return report

def verify(A,b,result):
    if result['status']=='exact_infeasible_relaxation':c.w.core.check_farkas(A,b,result['ray'])
    elif result['status']=='exact_feasible_relaxation':
        p={j:c.s.Rational(v) for j,v in result['primal']}
        c.require(len(p)==len(result['primal']) and all(v>=0 for v in p.values()),'valid primal entries')
        c.require(all(sum(row[j]*v for j,v in p.items())==bb for row,bb in zip(A,b)),'exact feasible relaxation replay')
