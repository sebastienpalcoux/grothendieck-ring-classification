"""Classification by exact checks of proved or explicitly cited hypotheses."""
from applications import *


def check(R,c,models,search):
    reject_legacy(c)
    k=c['kind']
    require(k in {'model','rank_two_moment','diagonal_involution_moments',
                  'involution_propagation_42','subring','weak_integral',
                  'two_dimensions','automatic_spherical','signed'},
            'certificate type outside the minimal proof stream')
    if k=='model':
        matches=[m for m in models if m['model']==c['model']]
        require(len(matches)==1 and canonical(R)==canonical(matches[0]['matrices']),'unverified model matching')
    elif k=='rank_two_moment':check_rank_two(R,c)
    elif k=='diagonal_involution_moments':check_diagonal(R,c)
    elif k=='involution_propagation_42':check_type42(R,c)
    elif k=='subring':check_subring(R,c)
    elif k in ('weak_integral','two_dimensions'):
        f,K,ds,D,pD,emb=Characters(R).fp()
        if k=='weak_integral':
            require(len(key(D))==1 and key(D)[0].q==1,'not weakly integral')
            if 'dimension' in c:require(str(key(D)[0])==c['dimension'],'dimension mismatch')
        else:require(len(set(map(key,ds)))==2,'not two distinct FP dimensions')
        check_pseudo(R,c['pseudo'])
    elif k=='automatic_spherical':
        require(tuple(c['basis']) in PERMS,'invalid automatic-spherical basis')
        A=permute(R,c['basis'])
        if c['criterion']=='invertible':
            i=c['object']
            require(type(i) is int and 1<=i<4 and A[i][dual(A)[i]]==[1,0,0,0],
                    'no stated nontrivial invertible object')
        elif c['criterion']=='multiplicity_one':
            require(dual(A)==[0,1,2,3] and max(flat(A))==1,
                    'not self-dual multiplicity one')
        else:raise VerificationError('unknown automatic-spherical theorem')
        check_sphere(A,c['spherical'])
    elif k=='signed':check_signed(R,c,search)
    else:raise VerificationError('unknown proof type: '+str(k))
