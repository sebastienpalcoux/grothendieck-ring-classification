"""Exact dispatch: no discovery routines or floating-point feasibility tests."""
from extension import *
import zero_spectrum,subring_descent,weighted_induction,oriented_extension
_order6_finite_checked=False

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
    global _order6_finite_checked
    k=c['kind']
    if k=='general_stabilizer_rotation':
        import stabilizer_rotation
        stabilizer_rotation.verify_general(R,c)
    elif k=='general_stabilizer_rotation_higher':
        import stabilizer_rotation_higher
        stabilizer_rotation_higher.verify_general(R,c)
    elif k=='general_cyclotomic_stabilizer_trace':
        import cyclotomic_stabilizer_trace
        cyclotomic_stabilizer_trace.verify_general(R,c)
    elif k in ('ramified_signed_pseudo_exclusion','ramified_signed_arithmetic_exclusion','ramified_Casimir_trace_exclusion'):
        import new_ramified_signed
        new_ramified_signed.verify(R,c)
    elif k=='biquadratic_spherical_trace':
        import new_biquadratic_trace
        new_biquadratic_trace.verify(R,c)
    elif k in ('formal_codegree_trace_ideal','trace_ideal_signed_pseudo_exclusion'):
        import new_trace_ideal
        new_trace_ideal.verify(R,c)
    elif k=='rank3_c2_neargroup_subring':
        import new_rank3_subring
        new_rank3_subring.verify(R,c)
    elif k=='spectral_involution_module':
        import new_module_spectral
        new_module_spectral.verify(R,c)
    elif k=='morita_order6':
        import new_morita_order6
        # The finite rank-twelve domain is independent of the input tensor.
        # Replay it once per checking process; each tensor reduction is still
        # reconstructed and verified separately.
        new_morita_order6.verify(R,c,check_finite=not _order6_finite_checked)
        _order6_finite_checked=True
    elif k=='full_morita_gram':
        import full_morita_gram
        full_morita_gram.verify(R,c)
    elif k=='small_dimension_morita':
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
