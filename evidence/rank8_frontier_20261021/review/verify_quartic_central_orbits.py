#!/usr/bin/env python3
"""Exact central order-two orbit and semionic moment bridge for R928/R941."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'noncommutative'))
import rotation_search as rotation

def need(ok,msg):
    if not ok:raise ValueError(msg)

def mul(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
    return tuple(out)

def run():
    sourcepath=BASE/'quartic_integer_center/source.json';grampath=BASE/'quartic_integer_center/gram_cubic.json'
    source=json.loads(sourcepath.read_text());gram=json.loads(grampath.read_text());patterns=gram['patterns']
    need(gram['source_sha256']==hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'joint Gram source binding')
    need(len(patterns)==343 and gram['complete_joint_pattern_count']==343 and gram['independent_Python_nodes']>0,'two independently enumerated complete domains')
    records=[];paths=[sourcepath,grampath,BASE/'quartic_integer_center/source.py',BASE/'quartic_integer_center/gram_cubic.py',
        BASE/'quartic_integer_center/enumerate.cpp',BASE/'noncommutative_followup/verify_scope_gates.py',BASE/'noncommutative_followup/scope_gates.json',
        BASE/'noncommutative_followup/independent_wedderburn.py',BASE/'noncommutative/rotation_search.py',Path(__file__)]
    for rec in source['records']:
        R=rec['tensor'];need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==rec['tensor_sha256'],'source tensor')
        N=len(R);unit=tuple([1]+[0]*(N-1));du=[next(j for j in range(N)if R[i][j][0])for i in range(N)]
        inv=[i for i in range(N)if tuple(R[i][du[i]])==unit]
        need(len(inv)==2 and inv[0]==0,'two source invertibles');g=inv[1]
        need(R[g][g]==list(unit)and all(R[g][i]==R[i][g]for i in range(N)),'central source involution')
        perm=[]
        for i in range(N):
            need(sum(R[g][i])==1,'invertible permutation');perm.append(R[g][i].index(1))
        need(all(perm[perm[i]]==i and perm[i]!=i for i in range(N)),'free source basis action')
        act=lambda v:tuple(sum(v[i]*R[g][i][j]for i in range(N))for j in range(N))
        lows=list(map(tuple,rec['low_columns']));highs=[(0,)+tuple(v)for v in rec['canonical_high_vectors']]
        need(len(lows)==5 and len(highs)==65 and len(set(lows+highs))==70,'distinct complete restriction columns')
        need([v for v in lows if not any(v[1:])]==[unit],'forgetful kernel is Vec by complete I(1) list')
        lower={v:i for i,v in enumerate(lows)};higher={v:i for i,v in enumerate(highs)}
        pure=[i for i,v in enumerate(highs)if v[g]and not any(v[j]for j in range(N)if j!=g)]
        need(pure==[40,45]and highs[40][g]==1 and highs[45][g]==2,'pure-g columns')
        translated=[higher[act(v)]for v in lows];need(translated==[40,41,42,43,57],'complete low translated highs')
        fixed=[];forbidden=[];other=[]
        for i,v in enumerate(highs):
            w=act(v)
            if w in lower:need(translated[lower[w]]==i,'inverse low-high pairing')
            elif w in higher:
                if w==v:fixed.append(i)
                else:other.append((i,higher[w]))
            else:
                need(w[0]>0,'only exhausted low columns prohibit translates');forbidden.append(i)
        need(fixed==list(range(40))and not other,'all high-high orbits fix restriction type')
        need(forbidden==[44,45,46,47,48,49,50,51,52,53,54,55,56,58,59,60,61,62,63,64],'complete forbidden restriction orbits')
        # Verify all listed patterns directly, while the producer's two independent
        # exhaustive algorithms remain a separate prerequisite in the registry.
        vectors=rec['reduced_high_vectors'];Q=rec['reduced_Gram'];cubics=rec['low_cubic_equations']
        for m in patterns:
            need(all(sum(z*v[i]*v[j]for z,v in zip(m,vectors))==Q[i][j]for i,j in itertools.product(range(4),repeat=2)),'every full Gram pattern')
            for c in cubics:
                value=[F(c['constant'][k])+sum(z*F(a[k])for z,a in zip(m,c['coefficients']))for k in range(4)]
                need(not any(value[1:])and value[0].denominator==1 and value[0]>=0,'every full distinguished cubic')
            need(m[40]==1 and all(m[i]==1 for i in translated)and not any(m[i]for i in forbidden),'every pattern forces the same central invertible orbit')
        rotationpath=BASE/f"noncommutative/rotation_{rec['id'].split('_')[-1]}_h6.json"
        prior=json.loads(rotationpath.read_text());need(prior['tensor_sha256']==rec['tensor_sha256'],'indicator source binding')
        rotation.verify(R,prior['result']);branches=prior['result']['branches'];need(len(branches)==1,'complete unique low frame')
        viable=[c['indicators']for c in branches[0]['systems']if c['ray']is None]
        need(viable and len({v[g-1]for v in viable})==1,'one forced pointed indicator sign')
        sign=viable[0][g-1];need(sign==(-1 if rec['id']=='R8_3_928'else 1),'forced pointed sign')
        charges=[]
        for chi,degree in zip(rec['full_characters'],rec['irreducible_dimensions']):
            z=tuple(F(x)/degree for x in chi[g]);need(z[1:]==(0,0,0)and z[0]in(-1,1),'distinguished monodromy character')
            charges.append(int(z[0]))
        need(charges==[1,1,1,1,-1],'full scalar/matrix monodromy normalization')
        allowed=[i for i,m in enumerate(patterns)if all(m[j]%2==0 for j in fixed)]if sign==-1 else None
        if sign==-1:need(allowed==[2,6,40,44,49,58,61,64,186,191,196,199,243,245,248],'complete semionic parity reduction')
        records.append({'id':rec['id'],'tensor_sha256':rec['tensor_sha256'],'source_g':g,'source_g_permutation':perm,
            'complete_joint_patterns':343,'central_g_multiplicity':1,'kernel_pure_unit_only':True,
            'low_translated_high_indices':translated,'fixed_restriction_high_indices':fixed,'forbidden_high_indices':forbidden,
            'forced_source_indicator':sign,'central_twist_squared':sign,'low_monodromy_charges':charges,
            'semion_parity_surviving_pattern_indices':allowed,
            'semion_fixed_restriction_zero_moments':[2,6]if sign==-1 else None,
            'semion_translated_low_trace_moments':[0,-1,0,1,0,-1]if sign==-1 else None})
        paths.append(rotationpath)
    # Actual pointed semion modular category: balancing and absence of fixed
    # points, with both possible signs of its quadratic form.
    gm=lambda a,b:(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def gp(a,k):
        z=(1,0)
        for _ in range(k):z=gm(z,a)
        return z
    for t in((0,1),(0,-1)):
        twists=[(1,0),t];M=[(1,0),(-1,0)]
        for i in range(2):
            need(twists[1-i]==gm(gm(twists[i],t),M[i]),'actual semion balancing control')
            for k in(2,6):need(tuple(a+b for a,b in zip(gp(twists[i],k),gp(twists[1-i],k)))==(0,0),'actual semion moments2,6 control')
    return {'kind':'central_order_two_orbits_and_semion_moments','records':records,
        'known_control':'Both pointed semion quadratic forms; exact values in {0,+1,-1,+i,-i}',
        'scope':'necessary structure of pseudo-unitary Galois conjugates; no tensor factorization of the source and no categorical construction',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=run();path=HERE/'quartic_central_orbits.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'central orbit receipt differs')
    print('PASS928/941 central involution orbits;928 semion parity leaves15 complete patterns.')
