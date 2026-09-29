"""Tensor-parametric unrestricted sphericalization reduction.

A successful certificate proves that every categorification admits a spherical
structure and a Galois conjugate that is pseudo-unitary. It is not by itself a
nonexistence certificate. All signed quotients are enumerated without choosing
second-indicator signs; their complete sign orbits and character obstructions
are checked. No census ID or fixed dimension formula enters the verifier.
"""
import itertools
from oriented_signed import enumerate_all,validate_general
from signed import from_values,gauge_original
from proofs import Characters,signed_component_certificate,check_signed_component
from exact import require,pc,ec
from rings import dual


def enumeration(R,timeout=120):
    vals,p,stats=enumerate_all(R,timeout=timeout,normalized=False);n=len(R);du=dual(R)
    signs=[(1,)+z for z in itertools.product((-1,1),repeat=n-1)
           if all(((1,)+z)[i]==((1,)+z)[du[i]] for i in range(n))]
    factors=[tuple(eta[a]*eta[b]*eta[c] for orb in p['active'] for a,b,c in [orb[0]]) for eta in signs]
    groups={};allvalues=set(vals)
    for v in vals:
        orbit={tuple(x*y for x,y in zip(v,f)) for f in factors}
        require(orbit<=allvalues,'sign orbit leaves exhaustive signed solutions')
        groups.setdefault(min(orbit),[]).append(v)
    return vals,p,stats,groups


def certificate(R,timeout=120):
    vals,p,stats,groups=enumeration(R,timeout);branches=[];n=len(R)
    for v,orbit in sorted(groups.items()):
        T=from_values(R,p,v);validate_general(T);g=gauge_original(T,R)
        b={'values':list(v),'orbit_size':len(orbit)}
        if g:b['gauge_original']=g
        else:
            if any(T[i][j]!=T[j][i] for i in range(n) for j in range(n)):
                if n!=6:return None
                from oriented_extension import nc_certificate
                cc=nc_certificate(R,T)
                if cc is None:return None
                b['noncommutative']=cc;branches.append(b);continue
            a=Characters(T);b['generator']=a.k;b['characters']=[]
            for f,m in a.components:
                w=signed_component_certificate(R,T,a,f,{})
                if w is None:return None
                K,ds,delta,pD=a.component(f)
                b['characters'].append({'factor':pc(f),'global_dimension_polynomial':pc(pD),'obstruction':w})
        branches.append(b)
    a=Characters(R);chars=[];good=0;fp=a.fp()[0]
    for f,m in a.components:
        K,ds,delta,pD=a.component(f);zero=next((i for i,d in enumerate(ds) if not d),None)
        cc={'factor':pc(f),'dimensions':[ec(d) for d in ds],'zero_object':zero}
        if zero is None:
            if f==fp:good+=1
            else:
                obstruction=signed_component_certificate(R,R,a,f,{})
                if obstruction is None:return None
                cc['arithmetic_obstruction']=obstruction
        chars.append(cc)
    if good!=1:return None
    return {'kind':'galois_pseudo_reduction','version':1,'normalized_indicator_restrictions_used':False,
            'enumeration_statistics':stats,'all_values':list(map(list,vals)),'branches':branches,
            'original_character_generator':a.k,'original_characters':chars}


def verify(R,c):
    require(c['kind']=='galois_pseudo_reduction' and c.get('version')==1,'wrong sphericalization reduction kind/version')
    vals,p,stats,groups=enumeration(R);n=len(R)
    require(c['normalized_indicator_restrictions_used'] is False,'unexpected second-indicator normalization')
    require(list(map(list,vals))==c['all_values'],'incomplete unrestricted signed domain')
    require(stats==c['enumeration_statistics'],'wrong signed enumeration statistics')
    require([list(v) for v in sorted(groups)]==[b['values'] for b in c['branches']],'incomplete signed sign-orbit enumeration')
    gauges=0;character_rejections=0
    for v,b in zip(sorted(groups),c['branches']):
        require(b['orbit_size']==len(groups[v]),'wrong sign orbit size')
        T=from_values(R,p,v);validate_general(T)
        if 'gauge_original' in b:
            require(gauge_original(T,R)==b['gauge_original'],'incorrect original sign gauge');gauges+=1
        elif 'noncommutative' in b:
            require(n==6 and any(T[i][j]!=T[j][i] for i in range(n) for j in range(n)),'invalid noncommutative signed branch')
            from oriented_extension import nc_certificate
            cc=nc_certificate(R,T)
            require(cc is not None and cc==b['noncommutative'],'noncommutative signed character rejection failed')
            character_rejections+=len(cc['characters'])
        else:
            require(all(T[i][j]==T[j][i] for i in range(n) for j in range(n)),'commutative character test used on noncommutative quotient')
            a=Characters(T,b['generator'])
            require(len(a.components)==len(b['characters']),'missing signed dimension-character component')
            for (f,m),cc in zip(a.components,b['characters']):
                K,ds,delta,pD=a.component(f)
                require(pc(f)==cc['factor'] and pc(pD)==cc['global_dimension_polynomial'],'wrong signed dimension character')
                check_signed_component(R,T,a,f,cc['obstruction']);character_rejections+=1
    a=Characters(R,c['original_character_generator']);fp=a.fp()[0]
    require(len(a.components)==len(c['original_characters']),'incomplete original dimension-character list')
    good=[]
    for (f,m),cc in zip(a.components,c['original_characters']):
        K,ds,delta,pD=a.component(f)
        require(pc(f)==cc['factor'] and [ec(d) for d in ds]==cc['dimensions'],'wrong original character')
        z=cc['zero_object']
        if z is not None:
            require(type(z) is int and 0<=z<n and not ds[z],'nonzero claimed zero dimension')
        elif 'arithmetic_obstruction' in cc:
            check_signed_component(R,R,a,f,cc['arithmetic_obstruction'])
        else:
            require(all(ds) and f==fp,'nonzero dimension character lies outside FP Galois orbit');good.append(f)
    require(len(good)==1,'FP orbit not the unique nonzero dimension-character component')
    return {'signed_quotients':len(vals),'sign_orbits':len(groups),'gauge_original_orbits':gauges,
            'nongauge_character_rejections':character_rejections,'categorifications_spherical':True,
            'galois_pseudo_unitary':True}
