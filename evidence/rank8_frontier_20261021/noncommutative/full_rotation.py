"""Full joint tensor-rotation equations for quadratic NC fusion rings."""
import itertools,math,sys
from fractions import Fraction as F
import central_support as c
import rotation_search as base
sys.path.insert(0,str(c.OLD.parent/'criteria'))
import tensor_rotation
h=base.h;s=c.s

def system(R,a,L,ep,height):
    Q,high=base.grams.high_columns(a,L);types,bound=h.trace_types(a['q'],a['primes'],height)
    mul=lambda x,y:h.mul(x,y,a['q'])
    labels=[(v,z,ti) for v,z in high for ti in range(len(types))];nvars=len(labels);LL=L*L.T;d=a['dimensions'];D=a['global_dimension']
    low=[tuple(sum((F(int(LL[i,j]))*d[j][k] for j in range(8)),F(0)) for k in range(2)) for i in range(8)]
    c.require(low[0]==D,'weighted unit restriction dimension identity')
    rows=[];rhs=[]
    for i,j in itertools.combinations_with_replacement(range(7),2):
        rows.append({k:F(v[i]*v[j]) for k,(v,z,ti) in enumerate(labels) if v[i]*v[j]});rhs.append(F(int(Q[i,j])))
    moments=[[mul(z,tt) for tt in types[ti]] for v,z,ti in labels]
    for power in (1,2):
        for i in range(7):
            for k in range(2):
                rows.append({j:v[i]*moments[j][power-1][k] for j,(v,z,ti) in enumerate(labels) if v[i]*moments[j][power-1][k]});rhs.append(-low[i+1][k]+(ep[i]*D[k] if power==2 else 0))
    for obj in range(1,8):
        powers=[[1]+[0]*7]
        for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
        for order in range(3,height+1):
            rs=[int(r) for r in s.divisors(order) if r<order];rot=tensor_rotation.rotation_types(a['q'],order,rs);start=nvars;nvars+=len(rot)
            rows.append({start+j:F(1) for j in range(len(rot))});rhs.append(F(powers[order][0]))
            for at,r in enumerate(rs):
                power=order//r
                for k in range(2):
                    row={};constant=sum((F(powers[r][i])*low[i][k] for i in range(8)),F(0))
                    for j,(v,z,ti) in enumerate(labels):
                        coeff=sum(powers[r][i]*v[i-1] for i in range(1,8));value=-coeff*moments[j][power-1][k]
                        if value:row[j]=value
                    for j,tt in enumerate(rot):
                        value=mul(D,tt[at])[k]
                        if value:row[start+j]=value
                    rows.append(row);rhs.append(constant)
    A=[];b=[]
    for sparse,constant in zip(rows,rhs):
        den=math.lcm(constant.denominator,*(x.denominator for x in sparse.values()));row=[0]*nvars
        for j,x in sparse.items():row[j]=int(x*den)
        constant=int(constant*den);g=math.gcd(constant,*row) or 1;A.append([x//g for x in row]);b.append(constant//g)
    return A,b,{'high_columns':len(high),'trace_types':len(types),'order_bound':bound,'rows':len(A),'variables':nvars,'joint_rotation':True}

if __name__=='__main__':
    h.build_system=system
    base.main()
