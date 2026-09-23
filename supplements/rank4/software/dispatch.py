"""Classification by exact checks of proved or explicitly cited hypotheses."""
from applications import *
_MODEL_KEYS={}

def nonselfdual_recognizer(R):
    for p in PERMS:
        A=permute(R,p)
        if dual(A)!=[0,1,3,2]:continue
        m=A[2][2][2]
        if m>=2 and A==ns_tensor((0,0,0,1,m,m)):
            return {'kind':'Sm','basis':list(p),'m':m}
    return None

def discover(R,models,search):
    canonical_R=canonical(R)
    if not _MODEL_KEYS:
        _MODEL_KEYS.update({canonical(m['matrices']):m['model'] for m in models})
    if canonical_R in _MODEL_KEYS:return {'kind':'model','model':_MODEL_KEYS[canonical_R]},None
    for test in (dnumber,ranktwo_recognizer,nonselfdual_recognizer,
                 diagonal_recognizer,near_recognizer,literature_near_recognizer):
        c=test(R)
        if c:return c,None
    c=cyclotomic_failure([N.charpoly(t).as_poly() for N in matrices(R)])
    if c:return c,None
    c=subring_certificate(R)
    if c:return c,None
    f,K,ds,D,pD,emb=Characters(R).fp()
    weak=len(key(D))==1 and key(D)[0].q==1
    two=len(set(map(key,ds)))==2
    if weak or two:
        c=pseudo_certificate(R)
        if c:
            if weak:
                direct=involution_propagation_recognizer(c)
                if direct:return direct,None
            return {'kind':'weak_integral' if weak else 'two_dimensions','pseudo':c},None
    return signed_certificate(R,search)

def check(R,c,models,search):
    reject_legacy(c)
    k=c['kind']
    if k=='model':
        matches=[m for m in models if m['model']==c['model']]
        require(len(matches)==1 and canonical(R)==canonical(matches[0]['matrices']),'unverified model matching')
    elif k=='dnumber':check_dnumber(R,c)
    elif k=='rank_two_moment':check_rank_two(R,c)
    elif k=='diagonal_involution_moments':check_diagonal(R,c)
    elif k=='involution_propagation_42':check_type42(R,c)
    elif k=='near_group_root_length':check_near(R,c)
    elif k=='literature_near_group':check_literature_near(R,c)
    elif k=='Sm':require(nonselfdual_recognizer(R)==c,'non-self-dual recognition failed')
    elif k=='cyclotomic':check_cyclotomic([N.charpoly(t).as_poly() for N in matrices(R)],c)
    elif k=='subring':check_subring(R,c)
    elif k in ('weak_integral','two_dimensions'):
        f,K,ds,D,pD,emb=Characters(R).fp()
        if k=='weak_integral':
            require(len(key(D))==1 and key(D)[0].q==1,'not weakly integral')
            if 'dimension' in c:require(str(key(D)[0])==c['dimension'],'dimension mismatch')
        else:require(len(set(map(key,ds)))==2,'not two distinct FP dimensions')
        check_pseudo(R,c['pseudo'])
    elif k=='signed':check_signed(R,c,search)
    else:raise VerificationError('unknown proof type: '+str(k))
