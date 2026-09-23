"""Decision trees extending the prefix by higher relative twist moments."""
from proofs import *
import higher_traces

def extended_pseudo(R,height=6):
    c=pseudo_certificate(R,gram_prune=True)
    if c is not None:return c
    a=Characters(R);f,K,ds,D,pD,e=a.fp();w=field_failure(f,a.cf)
    if w:return {'kind':'fp_dimension_field','generator':a.k,'factor':pc(f),'obstruction':w}
    return higher_traces.certificate(R,height,gram_prune=True)

def check_extended_pseudo(R,c):
    if c['kind']=='finite_indicator_traces':higher_traces.verify(R,c)
    elif c['kind']=='fp_dimension_field':
        a=Characters(R,c['generator']);f=a.fp()[0];require(c['factor']==pc(f),'wrong FP field');check_field(f,a.cf,c['obstruction'])
    else:check_pseudo(R,c)

def general_certificate(R,height=6,timeout=30,adjoint_parity=False,positive_indicators=False):
    a=Characters(R);f,K,ds,D,pD,e=a.fp()
    gate='weak_integrality' if pD.degree()==1 else 'two_FP_values' if len(set(ds))==2 else None
    if gate:
        c=extended_pseudo(R,height)
        return None if c is None else {'kind':'pseudo_gate','gate':gate,'pseudo':c}
    sphere=sphere_certificate(R,lambda R:extended_pseudo(R,height))
    if sphere is None:return None
    vals,p,stats=enumerate_signed(R,timeout=timeout,adjoint_parity=adjoint_parity,positive_indicators=positive_indicators);branches=[]
    for v in vals:
        T=from_values(R,p,v);b={'values':list(v)};why=signed_adjoint_parity(R,T);g=gauge_original(T,R)
        if why:b['obstruction']=why
        elif g:b['obstruction']={'kind':'gauge_original','signs':g}
        else:
            aa=Characters(T);cc=[{'factor':pc(ff),'obstruction':signed_component_certificate(R,T,aa,ff,sphere)} for ff,_ in aa.components]
            if any(c['obstruction'] is None for c in cc):return None
            b['characters']=cc;b['generator']=aa.k
        branches.append(b)
    return {'kind':'signed_extension_positive' if positive_indicators else 'signed_extension_parity' if adjoint_parity else 'signed_extension','sphere':sphere,'branches':branches}

def verify_general(R,c):
    if c['kind']=='pseudo_gate':
        a=Characters(R);f,K,ds,D,pD,e=a.fp()
        require((c['gate']=='weak_integrality' and pD.degree()==1) or (c['gate']=='two_FP_values' and len(set(ds))==2),'invalid pseudo-unitary gate')
        check_extended_pseudo(R,c['pseudo']);return
    require(c['kind'] in ('signed_extension','signed_extension_parity','signed_extension_positive'),'unknown extension certificate')
    check_sphere(R,c['sphere'],check_extended_pseudo)
    vals,p,stats=enumerate_signed(R,timeout=60,adjoint_parity=c['kind']=='signed_extension_parity',positive_indicators=c['kind']=='signed_extension_positive')
    require([list(v) for v in vals]==[b['values'] for b in c['branches']],'incomplete signed enumeration')
    for v,b in zip(vals,c['branches']):
        T=from_values(R,p,v);validate(T,nonnegative=False)
        if 'obstruction' in b:
            why=b['obstruction']
            if why['kind']=='signed_adjoint_parity':require(signed_adjoint_parity(R,T)==why,'invalid signed parity')
            elif why['kind']=='gauge_original':require(gauge_original(T,R)==why['signs'],'invalid original gauge')
            else:raise VerificationError('unknown signed obstruction')
        else:
            aa=Characters(T,b['generator']);require(len(aa.components)==len(b['characters']),'missing signed character')
            for (ff,m),cc in zip(aa.components,b['characters']):require(pc(ff)==cc['factor'],'wrong signed factor');check_signed_component(R,T,aa,ff,cc['obstruction'])
