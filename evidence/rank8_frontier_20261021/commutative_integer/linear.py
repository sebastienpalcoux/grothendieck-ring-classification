"""Optional bounded phase-I discovery; default certificate replay is exact-only."""
import math
from features import require

def verify(system,certificate):
    y=certificate['covector'];require(len(y)==len(system.rhs)and all(isinstance(v,int)for v in y),'invalid bounded Farkas covector')
    values=[sum(a*b for a,b in zip(y,col))for col in system.columns]
    upper=sum(max(0,v)*u for v,u in zip(values,system.bounds));target=sum(a*b for a,b in zip(y,system.rhs))
    require(target>upper,'bounded Farkas inequality is not strict')
    require(certificate['rhs_value']==target and certificate['box_upper']==upper,'bounded Farkas receipt differs')
    return True


def discover(system):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csc_matrix,hstack,eye
    m=len(system.rhs);n=len(system.columns);scales=[max(1,abs(b))for b in system.rhs]
    for col in system.columns:
        for i,a in enumerate(col):scales[i]=max(scales[i],abs(a))
    values=[];indices=[];starts=[0]
    for col in system.columns:
        for i,a in enumerate(col):
            if a:values.append(float(a/scales[i]));indices.append(i)
        starts.append(len(values))
    A=csc_matrix((np.asarray(values),np.asarray(indices,dtype=np.int32),np.asarray(starts,dtype=np.int32)),shape=(m,n))
    equality=hstack((A,eye(m,format='csc'),-eye(m,format='csc')),format='csc')
    target=np.array([float(b/s)for b,s in zip(system.rhs,scales)])
    answer=linprog(np.r_[np.zeros(n),np.ones(2*m)],A_eq=equality,b_eq=target,bounds=[(0,u)for u in system.bounds]+[(0,None)]*(2*m),method='highs')
    out={'method':'bounded_phase_I_proposal','solver_status':int(answer.status),'solver_message':str(answer.message),'conclusion':'no_exact_bounded_separator'}
    if not answer.success:return out
    out['numerical_phase_I_objective']=float(answer.fun)
    if answer.fun<=0:return out
    raw=[float(v)/s for v,s in zip(answer.eqlin.marginals,scales)];norm=max(map(abs,raw))
    if not norm:return out
    attempts=[]
    for exponent in range(3,19):
        scale=10**exponent;y=[int(round(v/norm*scale))for v in raw]
        vals=[sum(a*b for a,b in zip(y,col))for col in system.columns]
        upper=sum(max(0,v)*u for v,u in zip(vals,system.bounds));b=sum(a*v for a,v in zip(y,system.rhs));gap=b-upper
        attempts.append({'decimal_scale':exponent,'exact_gap':gap})
        if gap>0:
            g=math.gcd(*y)
            if g>1:y=[v//g for v in y];upper//=g;b//=g
            cert={'kind':'exact_bounded_linear_separator','covector':y,'rhs_value':b,'box_upper':upper}
            verify(system,cert);out.update(conclusion='exact_bounded_linear_obstruction',certificate=cert,reconstruction_attempts=attempts);return out
    out['reconstruction_attempts']=attempts;return out
