"""Full fusion-data hypothesis checks for three published classifications."""
from rings import *

def rank_two(R):
    for i in range(1,4):
        a=R[i][i][i]
        if a>=2 and R[i][i]==[int(j==0)+a*int(j==i) for j in range(4)]:
            return {'kind':'rank_two','object':i,'parameter':a}
    return None

def small_families(R):
    for p in PERMS:
        A=permute(R,p)
        if dual(A)==[0,1,2,3]:
            a,b=A[2][2][2],A[2][2][3]
            if (a,b) not in ((0,0),(0,1),(1,0),(1,1),(2,2)) and A==sd_tensor((0,0,0,0,1,0,a,b,a,b)):
                return {'kind':'EIP','basis':list(p),'a':a,'b':b}
        if dual(A)==[0,1,3,2]:
            m=A[2][2][2]
            if m>=3 and A==ns_tensor((0,0,0,1,m,m)):
                return {'kind':'Larson_transitive','basis':list(p),'parameter':m}
            m=A[1][1][1]
            if m not in (0,2,3,6) and A==ns_tensor((m,1,0,0,0,1)):
                return {'kind':'Larson_near_group','basis':list(p),'parameter':m}
    return None

def check_rank_two(R,c):
    i=c.get('object');a=c.get('parameter')
    require(c.get('kind')=='rank_two' and type(i) is int and 1<=i<4
            and type(a) is int and a>=2,'rank-two theorem hypotheses not met')
    require(R[i][i]==[int(j==0)+a*int(j==i) for j in range(4)],
            'rank-two theorem hypotheses not met')

def check_small_families(R,c):
    p=c.get('basis')
    require(p in [list(q) for q in PERMS],'published family basis is invalid')
    A=permute(R,p);kind=c.get('kind')
    if kind=='EIP':
        a,b=c['a'],c['b']
        require((a,b) not in ((0,0),(0,1),(1,0),(1,1),(2,2))
                and A==sd_tensor((0,0,0,0,1,0,a,b,a,b)),
                'published family theorem hypotheses not met')
    elif kind=='Larson_transitive':
        m=c['parameter']
        require(m>=3 and A==ns_tensor((0,0,0,1,m,m)),
                'published family theorem hypotheses not met')
    elif kind=='Larson_near_group':
        m=c['parameter']
        require(m not in (0,2,3,6) and A==ns_tensor((m,1,0,0,0,1)),
                'published family theorem hypotheses not met')
    else:raise VerificationError('unknown published family')
