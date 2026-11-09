"""Spherical-character arithmetic followed by bounded positive induction."""
from exact import *
from rings import *
from induction import *

@lru_cache(maxsize=None)
def nonabelian_factor(coefficients):
    q=poly(coefficients)
    if q.degree()<=2:return False
    require(q.degree() in (3,4),'cyclotomic factor degree is not three or four')
    group,_=q.galois_group()
    return not group.is_abelian

def cyclotomic_failure(a):
    """All codegree-ratio fields are abelian iff the Casimir splitting field is.

    For any candidate global dimension D, sum_j D/f_j=D. If every D/f_j
    lies in a cyclotomic field, so do D and f_j=D/(D/f_j). The converse
    is immediate. In rank four all irreducible factors have degree at most
    four; only cubic and quartic factors can have a nonabelian Galois group.
    """
    for q,m in a.cf:
        if nonabelian_factor(tuple(pc(q))):
            return {'kind':'nonabelian_codegrees','factor':pc(q)}
    return None

def check_nonabelian_factor(cp,c):
    require(isinstance(c,dict) and c.get('kind')=='nonabelian_codegrees',
            'wrong cyclotomic obstruction')
    coefficients=c.get('factor')
    require(isinstance(coefficients,list) and len(coefficients)>=2
            and all(isinstance(v,str) for v in coefficients),
            'unrelated cyclotomic factor')
    try:q=poly(coefficients)
    except Exception:raise VerificationError('unrelated cyclotomic factor')
    require(q.degree() in (3,4),'cyclotomic factor degree is not three or four')
    require(any(q==f for f,m in cp.set_domain(s.QQ).factor_list()[1]),'unrelated cyclotomic factor')
    require(nonabelian_factor(tuple(pc(q))),'codegree splitting field is abelian')

def check_cyclotomic(a,c):
    check_nonabelian_factor(a.cp,c)

def first_moment_failure(a,f):
    K,ds,D,pD=a.component(f)
    gap=K(2*a.w)*D-D-K.one
    for number,emb in enumerate(embeddings(f)):
        if emb.sign(gap)>0:
            return {'kind':'spherical_first_moment','embedding':number,
                    'inverse_square_sum':str(a.w),'gap':ec(gap)}
    return None

def arithmetic_failure(a,f):
    K,ds,D,pD=a.component(f)
    zero=next((i for i in range(4) if not ds[i]),None)
    unequal=next((i for i in range(4) if ds[i]!=ds[a.du[i]]),None)
    if zero is not None:return {'kind':'zero','object':zero}
    if unequal is not None:return {'kind':'duality','object':unequal}
    why=norm_failure(pD,a.cf)
    if why is not None:return why
    why=first_moment_failure(a,f)
    if why is not None:return why
    return cyclotomic_failure(a)

def sphere_certificate(R,a=None):
    if a is None:a=Characters(R)
    fp=a.fp();p_fp=fp[4]
    branches=[{'factor':pc(f),'obstruction':arithmetic_failure(a,f)} for f,m in a.components]
    unresolved=[(f,b) for (f,m),b in zip(a.components,branches) if b['obstruction'] is None]
    pseudo=None
    if unresolved:
        if any(a.component(f)[3]!=p_fp for f,b in unresolved):return None
        # Equal minimal polynomials of global dimensions suffice; characters may differ.
        pseudo=pseudo_certificate(R,a)
        if pseudo is None:return None
        for f,b in unresolved:b['obstruction']={'kind':'galois_global_dimension'}
    return {'kind':'spherical','generator':a.k,'characters':branches,'pseudo':pseudo}

def check_sphere(R,c):
    require(isinstance(c,dict) and c.get('kind')=='spherical','wrong spherical certificate')
    a=Characters(R,c['generator']);p_fp=a.fp()[4]
    require(len(a.components)==len(c['characters']),'missing character branches')
    pseudo_checked=False
    for (f,m),b in zip(a.components,c['characters']):
        require(pc(f)==b['factor'],'wrong character factor')
        K,ds,D,pD=a.component(f);v=b['obstruction']
        require(isinstance(v,dict),'missing spherical obstruction')
        kind=v.get('kind')
        if kind in ('zero','duality'):
            i=v.get('object');require(type(i) is int and 0<=i<4,'invalid spherical object')
            if kind=='zero':require(not ds[i],'dimension is nonzero')
            else:require(ds[i]!=ds[a.du[i]],'dual dimensions agree')
        elif kind=='norm':check_norm(pD,a.cf,v)
        elif kind=='spherical_first_moment':
            ee=embeddings(f);number=v.get('embedding')
            require(type(number) is int and 0<=number<len(ee),'invalid real embedding')
            require(all(ds[i]==ds[a.du[i]] for i in range(4)),'first-moment branch is not spherical')
            gap=K(2*a.w)*D-D-K.one
            require(v['inverse_square_sum']==str(a.w) and v['gap']==ec(gap)
                    and ee[number].sign(gap)>0,'spherical first-moment bound not violated')
        elif kind=='nonabelian_codegrees':check_cyclotomic(a,v)
        elif kind=='galois_global_dimension':
            require(pD==p_fp,'global dimension is not conjugate to FP dimension')
            if not pseudo_checked:check_pseudo(R,c['pseudo'],a);pseudo_checked=True
        else:raise VerificationError('unknown spherical obstruction')
    require(pseudo_checked or c.get('pseudo') is None,'unused pseudo-unitary proof')
