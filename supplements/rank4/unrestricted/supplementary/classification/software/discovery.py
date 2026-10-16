"""Witness discovery. This module is not imported by the replay driver."""
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

