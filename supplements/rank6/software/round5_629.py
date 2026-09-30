"""Exact bounded twist-profile reduction for R6_4_629.

The public enumeration helper is independent of numerical optimization.
The complete proof chain, including modular completion, is replayed by
research/round5/m4_629/replay_modular_chain.py.
"""
import itertools,json,math,time,argparse
from pathlib import Path
from fractions import Fraction
import sympy as s
from exact import require
from spectral_induction import Spectrum
import round3_m4 as ambient

ROOT=Path(__file__).resolve().parents[1]

def enumerate_with_large_bounds_first(A,b,bounds,node_limit=30000000):
    """Exact bounded enumeration, eliminating expensive coordinates first.

    Column permutation changes neither the integer lattice nor completeness.
    The inherited enumerator chooses the surviving free coordinates in the
    opposite order, trying small domains first. No numerical solver is used.
    """
    from round4_quartic_profiles import enumerate_affine
    permutation=sorted(range(len(bounds)),key=lambda j:-bounds[j])
    AA=[[row[j] for j in permutation] for row in A]
    sols,stats=enumerate_affine(AA,b,[bounds[j] for j in permutation],node_limit)
    originals=[]
    for x in sols:
        y=[0]*len(x)
        for j,k in enumerate(permutation):y[k]=x[j]
        originals.append(y)
    return originals,dict(stats,permutation=permutation)

def rank30_system():
    """Rebuild the complete retained rank-30 height-six twist branch."""
    from round4_629_orbits import orbit_domain
    old=ROOT/'research/round4/m4_629'
    R,data,cols,lab,src=source_data();data=ambient.data_for(R,6,15)
    cols=data['lows'][3];lab=data['tab'].assignments(cols)[0]
    saved=json.load(open(old/'fixed_twist_h6.json'))
    require(list(lab)==saved['lab'] and saved['ep']==[1]*5,'changed original branch')
    candidates=[(pi,cs) for pi,cs in zip(src['surviving_indices'],src['counts']) if 6+sum(cs)==30]
    require(len(candidates)==1,'rank30 profile not unique')
    pi,cs=candidates[0];A,b,meta=ambient.system(R,data,cols,saved['ep'],lab)
    G,vectors=ambient.high_vectors(data,cols);sp=Spectrum(data['tab'],cols,[(v,None) for v in vectors]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vectors if v not in bad]
    require(list(map(list,vs))==src['vectors'],'wrong source vectors')
    labels=[(v,ti) for v in vs for ti in range(len(data['phases']))];nh=len(labels);weights=dict(zip(vs,cs))
    domains={B:orbit_domain(data,B) for B in set(cs) if B};keep=[]
    for j in range(len(A[0])):
        if j>=nh:keep.append((j,1));continue
        v,ti=labels[j]
        if weights[v]:keep.extend((j,e) for e in domains[weights[v]].get(ti,[]))
    oldbranch=next(br for br in saved['branches'] if br['rank']==30)
    require(list(map(list,keep))==oldbranch['columns'],'changed complete orbit domain')
    AA=[[row[j]*e for j,e in keep] for row in A];bb=list(b)
    for v,cc in zip(vs,cs):
        if cc:AA.append([int(j<nh and labels[j][0]==v)*e for j,e in keep]);bb.append(cc)
    bounds=[]
    for j,e in keep:
        if j<nh:bounds.append(weights[labels[j][0]]//e)
        else:
            obj,order,_,_=next(block for block in meta['rotation_blocks'] if block[2]<=j<block[2]+block[3]);p=[1]+[0]*5
            for _ in range(order):p=[sum(p[a]*R[a][obj][z] for a in range(6)) for z in range(6)]
            bounds.append(p[0])
    return AA,bb,bounds,{'profile':pi,'rank':30,'height':6,'rows':len(AA),'variables':len(keep),'lab':list(lab),'ep':saved['ep']}

def rank30_certificate():
    A,b,bounds,meta=rank30_system();sols,stats=enumerate_with_large_bounds_first(A,b,bounds)
    require(not sols,'rank30 necessary system has an integer witness')
    return {'id':'R6_4_629','kind':'exact_rank30_twist_profile_obstruction','version':1,'scope':'specified_induction_profile_only','metadata':meta,'bounds':bounds,'enumeration':stats,'solutions':[],'optimizer_used':False}

def verify_rank30(certificate):
    require(certificate==rank30_certificate(),'rank30 exact certificate differs')
    return {'passed':True,'optimizer_used':False,'rank30_profile_excluded':True,'remaining_profile_ranks':[35,38],'ring_status':'unresolved','nodes':certificate['enumeration']['nodes']}

def fixed_twist_system(height,rank):
    """Restrict the universal moment system to one exact column profile.

    Removing zero-multiplicity column classes is substitution of zero in the
    complete domain. Every still occurring class and every relative twist
    orbit permitted by its multiplicity is reconstructed exactly.
    """
    from round4_629_orbits import orbit_domain
    R,_,_,_,src=source_data();data=ambient.data_for(R,height,15);cols=data['lows'][3];lab=data['tab'].assignments(cols)[0];ep=(1,1,1,1,1)
    candidates=[(pi,cs) for pi,cs in zip(src['surviving_indices'],src['counts']) if 6+sum(cs)==rank];require(len(candidates)==1,'profile rank is not unique')
    pi,cs=candidates[0];weights={tuple(v):c for v,c in zip(src['vectors'],cs) if c};vs=list(weights)
    G,_=ambient.high_vectors(data,cols);sp=Spectrum(data['tab'],cols,[(v,None) for v in vs]);require(not sp.forbidden and not sp.missing_low,'invalid retained profile')
    data['_branch_cache']={tuple(map(tuple,cols)):(G,vs,sp)}
    A,b,meta=ambient.system(R,data,cols,ep,lab);labels=[(v,ti) for v in vs for ti in range(len(data['phases']))];nh=len(labels);domains={B:orbit_domain(data,B) for B in set(weights.values())};keep=[]
    for j in range(len(A[0])):
        if j>=nh:keep.append((j,1));continue
        v,ti=labels[j];keep.extend((j,e) for e in domains[weights[v]].get(ti,[]))
    AA=[[row[j]*e for j,e in keep] for row in A];bb=list(b)
    for v,cc in weights.items():AA.append([int(j<nh and labels[j][0]==v)*e for j,e in keep]);bb.append(cc)
    bounds=[]
    for j,e in keep:
        if j<nh:bounds.append(weights[labels[j][0]]//e)
        else:
            obj,order,_,_=next(block for block in meta['rotation_blocks'] if block[2]<=j<block[2]+block[3]);p=[1]+[0]*5
            for _ in range(order):p=[sum(p[a]*R[a][obj][z] for a in range(6)) for z in range(6)]
            bounds.append(p[0])
    return AA,bb,bounds,{'profile':pi,'rank':rank,'height':height,'rows':len(AA),'variables':len(keep),'lab':list(lab),'ep':list(ep),'columns':list(map(list,keep))}

def fixed_profile_certificate(height,rank,node_limit=30000000,progress=None):
    A,b,bounds,meta=fixed_twist_system(height,rank)
    if progress:progress('built',meta)
    sols,stats=enumerate_with_large_bounds_first(A,b,bounds,node_limit)
    return {'id':'R6_4_629','kind':'exact_fixed_twist_profile_enumeration','version':1,'scope':'specified_induction_profile_only','metadata':meta,'bounds':bounds,'enumeration':stats,'solutions':sols,'optimizer_used':False}

def verify_fixed_profile(certificate):
    md=certificate['metadata'];rebuilt=fixed_profile_certificate(md['height'],md['rank'])
    require(certificate==rebuilt,'fixed-profile exact certificate differs')
    return {'passed':True,'optimizer_used':False,'profile_excluded':not rebuilt['solutions'],'rank':md['rank'],'nodes':rebuilt['enumeration']['nodes']}

def integer(z):
    a=z.to_list()
    require(len(a)<=1,'nonrational low Verlinde coefficient')
    q=Fraction(str(a[0])) if a else Fraction(0)
    require(q.denominator==1 and q>=0,'nonintegral/negative low fusion coefficient')
    return int(q)

def source_data():
    R=next(r['N'] for r in json.load(open(ROOT/'data/unresolved_tensors.json')) if r['id']=='R6_4_629')
    profile=json.load(open(ROOT/'research/round4/m4_629/filtered_profiles.json'))
    data=ambient.data_for(R,3,15);cols=data['lows'][3];lab=data['tab'].assignments(cols)[0]
    return R,data,cols,lab,profile

