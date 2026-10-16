"""Uniform categorical applications, including explicit literature hypotheses."""
from proofs import *

BANNED={'EIP','ranktwo','near_group','integral42'}

def reject_legacy(c):
    if isinstance(c,dict):
        require(c.get('kind') not in BANNED,'legacy exclusion classification present')
        for v in c.values():reject_legacy(v)
    elif isinstance(c,list):
        for v in c:reject_legacy(v)

def diagonal_recognizer(R):
    for p in PERMS:
        A=permute(R,p);m=A[2][2][2]
        if m>=3 and A==sd_tensor((0,0,0,0,1,0,m,m,m,m)):
            return {'kind':'diagonal_involution_moments','basis':list(p),'m':m}
    return None

def ranktwo_recognizer(R):
    for i in range(1,4):
        a=R[i][i][i]
        if a>=2 and R[i][i]==[int(j==0)+a*int(j==i) for j in range(4)]:
            return {'kind':'rank_two_moment','object':i,'a':a}
    return None

def near_recognizer(R):
    for p in PERMS:
        A=permute(R,p);m=A[3][3][3]
        if m<=0 or m%3:continue
        target=[[[int(j==l) for l in range(4)] for j in range(4)],
                [[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]],
                [[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],
                [[0,0,0,1],[0,0,0,1],[0,0,0,1],[1,1,1,m]]]
        if A!=target:continue
        k=m//3;delta=9*k*k+12;fac=s.factorint(delta)
        q=math.prod(int(v) for v,e in fac.items() if e%2)
        u=math.prod(int(v)**(int(e)//2) for v,e in fac.items())
        require(q>1,'rational near-group dimension not treated')
        conductor=q if q%4==1 else 4*q
        lam=s.Rational(int(s.totient(conductor))-abs(int(s.mobius(conductor))),math.isqrt(conductor//q))
        length=4*k*k+6;lower=s.Rational(k*k+k*u*lam,2)
        if lower<=length:continue
        return {'kind':'near_group_root_length','basis':list(p),'k':k,'squarefree':q,
                'square_factor':u,'conductor':conductor,'lambda':str(lam),
                'required_length':length,'lower_bound':str(lower)}
    return None

def literature_near_recognizer(R):
    """Larson, arXiv:1401.1879v2, Theorem 1.1; then the two-dimension reduction.

    Check the entire near-group multiplication tensor, never a catalogue label.
    The allowed multiplicities of the noninvertible are exactly 0,2,3,6.
    """
    for p in PERMS:
        A=permute(R,p);m=A[3][3][3]
        if m in (0,2,3,6):continue
        target=[[[int(j==l) for l in range(4)] for j in range(4)],
                [[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]],
                [[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]],
                [[0,0,0,1],[0,0,0,1],[0,0,0,1],[1,1,1,m]]]
        if A==target:
            return {'kind':'literature_near_group','basis':list(p),'m':m,
                    'reference':'Larson, Theorem 1.1, arXiv:1401.1879v2'}
    return None

def check_literature_near(R,c):
    require(literature_near_recognizer(R)==c,'Larson near-group hypotheses fail')
    f,K,ds,D,pD,emb=Characters(R).fp()
    require(len(set(map(key,ds)))==2,'two-dimension Galois reduction fails')

def involution_propagation_recognizer(proof):
    """Recognize a complete low-induction proof using the uniform
    residual-involution criterion, with no comparison to a named tensor.
    The historical certificate kind is retained for ledger compatibility.
    """
    if (proof is not None and proof.get('kind')=='induction'
            and proof.get('low_count',0)>0
            and all(branch['obstruction']['kind']=='involution_moment'
                    for branch in proof['failures'])):
        return {'kind':'involution_propagation_42','basis':[0,1,2,3]}
    return None

def check_rank_two(R,c):
    """Exact hypotheses of Ostrik's rank-two classification; no pivotal input."""
    i=c['object'];a=c['a']
    require(type(i) is int and i in range(1,4) and type(a) is int and a>=2,
            'rank-two parameters')
    require(R[i][i]==[int(j==0)+a*int(j==i) for j in range(4)],
            'rank-two closure')


def check_diagonal(R,c):
    p=c['basis'];m=c['m'];A=permute(R,p)
    require(tuple(p) in PERMS and m>=3,'diagonal hypotheses')
    require(A==sd_tensor((0,0,0,0,1,0,m,m,m,m)),'diagonal fusion rules')
    d=s.symbols('d');rel=d*d-2*m*d-1;D=4+4*m*d
    expected=s.Matrix([[4,0,2*m,2*m],[0,4,2*m,2*m],
                       [2*m,2*m,4+4*m*m,4*m*m],[2*m,2*m,4*m*m,4+4*m*m]])
    require(casimir(A)==expected,'diagonal Casimir')
    fp=s.Matrix([1,1,d,d])
    for i,N in enumerate(matrices(A)):
        require(all(s.rem(x,rel,d)==0 for x in N*fp-fp[i]*fp),'diagonal FP character')
    W=4*m+6*m*m*d;H=4*m+4*m*m*d;M=s.rem(2*D*d,rel,d)
    plus=s.rem((3*d+1)*(6*m+8*m*m*d)-2*D*d*(d+1),rel,d)
    expected_plus=2*(4*m*m-m-4)+2*(8*m**3-4*m*m-3*m-4)*d
    minus=s.rem(W*W-(M-W-H)*(M/2+D-W),rel,d)
    expected_minus=8*(m-2)*(3*m**3+3*m*m+3*m+2)+8*(m-2)*(6*m**4+6*m**3+8*m*m+5*m+2)*d
    require(s.expand(plus-expected_plus)==0 and s.expand(minus-expected_minus)==0,'diagonal moment identities')
    require(all(x>0 for x in s.Poly(plus,d).all_coeffs()) and all(x>0 for x in s.Poly(minus,d).all_coeffs()),'diagonal strict gaps')

def check_near(R,c):
    require(near_recognizer(R)==c,'near-group recognition or root-length arithmetic')
    A=permute(R,c['basis']);k=c['k'];d,w,z=s.symbols('d w z');rel=d*d-3*k*d-3
    D=6+3*k*d
    fp=s.Matrix([1,1,1,d])
    for i,N in enumerate(matrices(A)):
        require(all(s.rem(x,rel,d)==0 for x in N*fp-fp[i]*fp),'near-group FP character')
    low=s.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1],[0,k,k,k]])
    expected=s.Matrix([[0,0,0,0],[0,3,1,2*k],[0,1,3,2*k],[0,2*k,2*k,6*k*k+6]])
    require(casimir(A)-low*low.T==expected,'near-group residual Gram')
    W=5*k+3*k*k*d;one=2*k+k*k*d;other=2*k+(k*k+z)*d
    theta_sum=k*k-k*d-z*w*w
    expr=s.rem(s.rem(W+one*w+other*w*w+d*theta_sum,w*w+w+1,w),rel,d)
    require(s.expand(expr)==0,'near-group root-sum identity')
    require(c['square_factor']**2*c['squarefree']==9*k*k+12,'near-group squarefree part')
    require(s.Rational(c['lower_bound'])>c['required_length'],'no root-length contradiction')

def check_type42(R,c):
    f,K,ds,D,pD,emb=Characters(R).fp()
    require(len(key(D))==1 and key(D)[0].q==1,'weak integrality not established')
    # Reconstruct all low parts and test Proposition 5.3 on each branch.
    # In particular, this verifier does not recognize a named ring tensor.
    proof=pseudo_certificate(R)
    require(involution_propagation_recognizer(proof)==c,
            'not a uniform residual-involution certificate')
    check_pseudo(R,proof)
