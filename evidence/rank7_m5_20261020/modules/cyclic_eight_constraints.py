"""Exact C8 rotation character constraints for the complete eighth moment.

Appends linear equalities and eight NONNEGATIVE INTEGER multiplicities per
nonunit source object. The caller must retain the prior C4 variables.
"""
from fractions import Fraction as F


def require(condition,message):
    if not condition:raise RuntimeError(message)


def quad_mul(x,y):
    return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])


def field_times_quad(z,coords):
    return [x for j in range(0,8,2) for x in quad_mul(z,coords[j:j+2])]


def eighth_roots():
    # Basis1,sqrt5,sqrt2,sqrt10,i,i*sqrt5,i*sqrt2,i*sqrt10.
    h=F(1,2)
    return [(1,0,0,0,0,0,0,0),(0,0,h,0,0,0,h,0),
            (0,0,0,0,1,0,0,0),(0,0,-h,0,0,0,h,0),
            (-1,0,0,0,0,0,0,0),(0,0,-h,0,0,0,-h,0),
            (0,0,0,0,-1,0,0,0),(0,0,h,0,0,0,-h,0)]


def append_cyclic_eight(columns,rhs,labels,orbits,records,low,ds,D,N,sign,cyclic_four):
    """Return columns,rhs,labels,metadata; input lists are mutated in place.

    Column labels identify only the leading center-phase variables.
    cyclic_four is fourth_cyclic_constraints() metadata, with `variables`
    in eigenvalue order1,-1,i,-i and constants A=(m4+t2)/2,B=(m4-t2)/2.
    records must contain eighth_scaled8 in the displayed eight-coordinate
    field basis. The source unit is omitted from `low`, as in the wrapper.
    """
    rank=len(N);require(len(ds)==rank and len(sign)==rank,'Source size mismatch.')
    require(all(len(c)==len(rhs) for c in columns),'Input column lengths differ.')
    require(all(len(r['eighth_scaled8'])==8 for r in records),'Missing eighth phase field coordinates.')
    c4={r['source_object']:r for r in cyclic_four}
    require(set(c4)==set(range(1,rank)),'Incomplete source fourth-rotation variables.')
    roots=eighth_roots();metadata=[]
    source_unit=tuple(int(i==0) for i in range(rank));all_low=[source_unit]+list(low)
    for i in range(1,rank):
        power=[int(k==0) for k in range(rank)];power4=None
        for exponent in range(1,9):
            power=[sum(power[j]*N[j][i][k] for j in range(rank)) for k in range(rank)]
            if exponent==4:power4=power[:]
        m8=power[0];t4=sum(power4[k]*sign[k] for k in range(rank))
        require(m8>=abs(t4) and (m8+t4)%2==0,'Impossible order-two restriction of C8 character.')
        known=tuple(sum(v[i]*sum(v[k]*ds[k][h] for k in range(rank)) for v in all_low) for h in range(2))
        real_target=N[i][i][0]-sum(N[i][i][k]*c4[k]['A'] for k in range(1,rank))
        imag_target=-sum(N[i][i][k]*c4[k]['B'] for k in range(1,rank))
        start=len(rhs)
        target=[-known[0],-known[1],0,0,0,0,0,0,real_target,imag_target,t4,m8]
        for j,col in enumerate(columns):
            coeff=[F(0)]*12
            if j<len(labels):
                label=labels[j];moment=[F(x,8) for x in records[label['phase']]['eighth_scaled8']]
                for v,gram,z in orbits[label['orbit']]:
                    values=field_times_quad(z,moment)
                    for h in range(8):coeff[h]+=label['multiplicity_unit']*v[i-1]*values[h]
            for k in range(1,rank):
                if j==c4[k]['variables'][0]:coeff[8]-=2*N[i][i][k]
                if j==c4[k]['variables'][2]:coeff[9]-=2*N[i][i][k]
            col.extend(coeff)
        rhs.extend(target);variables=[]
        for exponent,root in enumerate(roots):
            col=[F(0)]*len(rhs)
            for h,z in enumerate(field_times_quad(D,root)):col[start+h]=-z
            col[start+8]=(1,0,-1,0,1,0,-1,0)[exponent]
            col[start+9]=(0,1,0,-1,0,1,0,-1)[exponent]
            col[start+10]=(-1)**exponent;col[start+11]=1
            variables.append(len(columns));columns.append(col)
        metadata.append({'source_object':i,'hom_eight':m8,'nu2_fourth_power':t4,
                         'nu4_square_source_coefficients':N[i][i],
                         'variables':variables,'eigenvalue_exponents':list(range(8))})
    require(all(len(c)==len(rhs) for c in columns),'Output column lengths differ.')
    return columns,rhs,labels,metadata


def multiplicities_from_traces(m,q,s,t,alpha,beta,gamma,delta):
    """Exact inverse Fourier expression, returned in eigenvalue order ζ8^j."""
    A0=F(m+q+2*s,4);A2=F(m+q-2*s,4)
    A1=F(m-q+2*t,4);A3=F(m-q-2*t,4)
    return ((A0+alpha)/2,(A1+beta)/2,(A2+gamma)/2,(A3+delta)/2,
            (A0-alpha)/2,(A1-beta)/2,(A2-gamma)/2,(A3-delta)/2)


def verify_fourier():
    import itertools
    count=0
    for n in itertools.product(range(3),repeat=8):
        m=sum(n);q=sum((-1)**j*n[j] for j in range(8))
        s=n[0]+n[4]-n[2]-n[6];t=n[1]+n[5]-n[3]-n[7]
        coeff=[n[j]-n[j+4] for j in range(4)]
        require(multiplicities_from_traces(m,q,s,t,*coeff)==n,'C8 inverse Fourier identity failed.')
        count+=1
    return count

def verify_pointed_c2():
    N=[[[1,0],[0,1]],[[0,1],[1,0]]]
    columns=[[] for _ in range(6)];rhs=[]
    labels=[{'orbit':0,'phase':j,'multiplicity_unit':1} for j in range(2)]
    orbits=[[((1,),(),(1,0))]]
    records=[{'eighth_scaled8':(8,0,0,0,0,0,0,0)} for _ in range(2)]
    c4=[{'source_object':1,'variables':[2,3,4,5],'A':1,'B':0}]
    columns,rhs,labels,metadata=append_cyclic_eight(columns,rhs,labels,orbits,records,
                [(1,0)],[(1,0),(1,0)],(2,0),N,[1,1],c4)
    assignment=[1,1,1,0,0,0]+[1,0,0,0,0,0,0,0]
    require([sum(c[k]*n for c,n in zip(columns,assignment)) for k in range(len(rhs))]==rhs,
            'Pointed C2 center control failed.')
    return True

if __name__=='__main__':
    import json
    print(json.dumps({'status':'PASS','exact_fourier_checks':verify_fourier(),'pointed_c2_control':verify_pointed_c2(),
                      'scope':'C8 character equations and complete field-coordinate parity, not domain infeasibility.'}))
