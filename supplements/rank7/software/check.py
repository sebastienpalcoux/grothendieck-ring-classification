"""Exact dispatch: no discovery routines or floating-point feasibility tests."""
from extension import *
import zero_spectrum,subring_descent,weighted_induction,oriented_extension

def integral_general(R,c):
    require(c['kind']=='signed_integral','wrong integral-general certificate');check_sphere(R,c['sphere'],oriented_extension.pseudo_check)
    vals,p,stats=enumerate_signed(R,timeout=180,positive_indicators=True)
    require([list(v) for v in vals]==[b['values'] for b in c['branches']],'missing integral signed branches')
    for v,b in zip(vals,c['branches']):
        T=from_values(R,p,v);validate(T,nonnegative=False)
        if 'obstruction' in b:
            w=b['obstruction']
            if w['kind']=='gauge_original':require(gauge_original(T,R)==w['signs'],'incorrect original gauge')
            else:require(signed_adjoint_parity(R,T)==w,'incorrect signed parity')
        else:
            aa=Characters(T,b['generator']);require(len(aa.components)==len(b['characters']),'missing signed characters')
            for (ff,m),cc in zip(aa.components,b['characters']):require(pc(ff)==cc['factor'],'wrong signed character');check_signed_component(R,T,aa,ff,cc['obstruction'])

def verify(R,c):
    k=c['kind']
    if k=='small_dimension_morita':
        import small_dimension_morita
        small_dimension_morita.verify(R,c)
    elif k=='involution_module':
        import involution_module
        involution_module.verify(R,c)
    elif k=='noncommuting_field_automorphisms':
        import field_automorphisms
        field_automorphisms.verify(R,c)
    elif k=='dnumber':check_dnumber(R,c)
    elif k=='rank_two':
        i=c['object'];m=c['multiplicity'];require(type(i) is int and 0<i<len(R) and type(m) is int and m>=2,'rank-two parameters');require(R[i][i][0]==1 and R[i][i][i]==m and sum(R[i][i])==1+m,'rank-two subring absent')
    elif k=='zero_spectrum':zero_spectrum.verify(R,c)
    elif k=='lower_rank_subring':subring_descent.verify(R,c)
    elif k=='subring':check_subring(R,c)
    elif k=='cyclotomic':check_cyclotomic([a.charpoly(t).as_poly() for a in matrices(R)],c)
    elif k=='weighted_induction':weighted_induction.verify(R,c)
    elif k=='signed_integral':integral_general(R,c)
    elif k.startswith('oriented_'):oriented_extension.verify(R,c)
    else:verify_general(R,c)
