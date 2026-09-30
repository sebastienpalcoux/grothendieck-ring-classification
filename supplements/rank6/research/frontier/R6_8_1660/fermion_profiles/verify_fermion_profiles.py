"""Portable, exact R6_8_1660 frontier reduction. Standard library only.

Reconstructs the conservative fermion orbit sieve and the weighted-FS
congruence; independently rechecks every rejected orbit branch by recursion.
No optimization, floating point, twist search, or stored feasible witnesses.

  python -O verify_fermion_profiles.py --package /path/to/Rank6_Categorification_M8
Use --write once to regenerate the small adjacent certificate.
"""
import argparse
import hashlib
import json
import math
import time
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise RuntimeError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def field_add(x,y):return tuple(a+b for a,b in zip(x,y))
def field_scale(c,x):return tuple(c*a for a in x)
def field_mul(x,y):
    z=[0]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            z[i^j]+=a*b*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
    return tuple(z)

ONE=(1,0,0,0);SQ2=(0,1,0,0);DX=(3,2,2,1)
DX2=field_mul(DX,DX)
D=field_scale(4,field_add(ONE,DX2))
DIMS=(ONE,ONE,DX,DX,SQ2,field_mul(SQ2,DX))

def dimension(v):
    z=(0,0,0,0)
    for a,d in zip(v,DIMS):z=field_add(z,field_scale(a,d))
    return z

def validate_constants(columns):
    lowdims=[dimension(v)for v in columns]
    q=(0,0,0,0)
    for d in lowdims[:4]:q=field_add(q,field_mul(d,d))
    require(field_add(field_mul(D,D),field_scale(-4,q))==field_scale(4,field_mul(DX2,(180,120,0,0))),'even dimension constant failed')
    u=(0,0,0,0)
    for sign,d in zip((1,1,1,1,-1,1),DIMS):u=field_add(u,field_scale(sign,d))
    low_fs=(0,0,0,0)
    for d in lowdims[:4]:low_fs=field_add(low_fs,field_scale(2,d))
    low_fs=field_add(low_fs,field_add(lowdims[4],lowdims[5]))
    require(field_add(field_mul(u,u),field_scale(-1,low_fs))==field_mul(DX,(36,24,0,0)),'FS dimension constant failed')
    require(field_add(lowdims[4],lowdims[5])==field_mul(DX,(0,0,8,4)),'complex-low alternative constant failed')

@lru_cache(None)
def orbit_groups(columns,vectors,profile):
    counts=list(profile);lookup={v:i for i,v in enumerate(vectors)}
    for v in columns[:4]:
        require(v[1]==0,'unexpected even low restriction')
        partner=(v[0],v[3],v[2],v[4],v[5]);i=lookup.get(partner)
        if i is None or counts[i]<1:return None
        counts[i]-=1
    groups=[];seen=set()
    for i,v in enumerate(vectors):
        if not counts[i]or i in seen:continue
        if v[0]:return None
        j=lookup.get((v[0],v[2],v[1],v[3],v[4]))
        if j is None or counts[j]!=counts[i]:return None
        seen.update((i,j));n=counts[i]
        nonselfdual=bool(v[3]%2 and any(v[k]%2 for k in (0,1,2,4)))
        if nonselfdual and n%2:return None
        a=v[1]+v[2];b=v[4]
        if v[3]:
            require((a,b,v[3])==(4,3,1)and nonselfdual,'unexpected sigma type')
            weight=(36,24)
        else:weight=(a*a+2*b*b,2*a*b)
        dv=dimension((0,)+v)
        require(field_mul(dv,dv)==field_mul(DX2,weight+(0,0)),'high dimension square failed')
        groups.append((n,weight[0],weight[1],i!=j,nonselfdual,a,b))
    return tuple(groups)

@lru_cache(None)
def orbit_feasible(groups,fixed_low):
    if groups is None:return False
    # Dimensions A+B sqrt2, number of even orbits E, and number Ea of
    # even orbits joining distinct restriction types.
    states={(0,0,0,0)};N=0;asymmetric=0;symmetric_capacity=0
    for n,a,b,asym,nonselfdual,_,_ in groups:
        N+=n*(2 if asym else 1)
        cap=n if asym else n//2
        asymmetric+=n if asym else 0
        symmetric_capacity+=0 if asym else cap
        step=2 if nonselfdual else 1
        nxt=set()
        for x,y,E,Ea in states:
            for e in range(0,cap+1,step):
                xx=x+a*e;yy=y+b*e
                if xx>180 or yy>120:break
                nxt.add((xx,yy,E+e,Ea+(e if asym else 0)))
        states=nxt
    c=2 if fixed_low else 3
    for x,y,E,Ea in states:
        if (x,y)!=(180,120):continue
        O=N-3*E-c;F=N-2*E-2*O
        if F>=0 and asymmetric-Ea<=O<=asymmetric+symmetric_capacity-E:
            return True
    return False

@lru_cache(None)
def independent_orbit_feasible(groups,fixed_low):
    """Separate recursion over e,o,f, summing p-s-t without eliminating O,F."""
    if groups is None:return False
    options=[]
    for n,a,b,asym,nonselfdual,_,_ in groups:
        choices=set()
        for e in range((n if asym else n//2)+1):
            if nonselfdual and e%2:continue
            if asym:choices.add((e*a,e*b,2*e-n))
            else:
                for o in range((n-2*e)//2+1):
                    f=n-2*e-2*o
                    if nonselfdual and f%2:continue
                    choices.add((e*a,e*b,e-o-f))
        options.append(tuple(choices))
    suffix=[]
    for k in range(len(options)+1):
        rem=options[k:]
        suffix.append((sum(min(z[2]for z in c)for c in rem),sum(max(z[2]for z in c)for c in rem),sum(max(z[0]for z in c)for c in rem),sum(max(z[1]for z in c)for c in rem)))
    @lru_cache(None)
    def search(k,a,b,r):
        lo,hi,ma,mb=suffix[k]
        if a<0 or b<0 or a>ma or b>mb or r<lo or r>hi:return False
        if k==len(options):return (a,b,r)==(0,0,0)
        return any(search(k+1,a-x,b-y,r-z)for x,y,z in options[k])
    return search(0,180,120,-(2 if fixed_low else 3))

def fs_congruence(groups):
    if groups is None:return None
    divisor=0;offset=0
    for n,_,_,asym,nonselfdual,a,b in groups:
        if nonselfdual:continue
        coefficient=a*(2 if asym else 1)
        divisor=math.gcd(divisor,2*coefficient)
        offset+=coefficient*n
    residual=36-offset
    if divisor==0:return None if residual==0 else dict(divisor=0,residual=residual)
    if residual%divisor:return dict(divisor=divisor,residue=residual%divisor)
    return None

def locate_package(explicit):
    if explicit:
        result=Path(explicit).resolve()
        require((result/'research/round5/m8_actual48/certificate.json').is_file(),'--package is not the source package')
        return result
    roots=[Path.cwd(),HERE,*HERE.parents,*Path.cwd().parents]
    for root in roots:
        for candidate in (root,root/'work_round6/Rank6_Categorification_M8'):
            if (candidate/'research/round5/m8_actual48/certificate.json').is_file():return candidate
    raise RuntimeError('Supply --package /path/to/Rank6_Categorification_M8')

def reconstruct(package):
    cp=package/'research/round5/m8_actual48/certificate.json';old=json.loads(cp.read_text())
    require(old['id']=='R6_8_1660'and old['complete']is True,'wrong prior certificate')
    source_hashes={'research/round5/m8_actual48/certificate.json':digest(cp)}
    branches=[];checked_rejections=0
    for prior in old['branches']:
        if prior['outcome']!='profile_frontier':continue
        source=package/prior['source'];require(digest(source)==prior['source_sha256'],'old source binding failed')
        source_hashes[prior['source']]=digest(source)
        raw=json.loads(source.read_text())['branches'][0]
        case=next(c for c in raw['cases']if c['labelling']==prior['labelling'])
        columns=tuple(map(tuple,raw['columns']));vectors=tuple(map(tuple,raw['high_vectors']))
        validate_constants(columns)
        require(prior['unresolved']==sorted(set(prior['unresolved'])),'prior frontier repeats indices')
        orbital=[];fs=[];conditions=[];surviving=[]
        for index in prior['unresolved']:
            groups=orbit_groups(columns,vectors,tuple(case['profiles'][index]))
            outcomes=[]
            for fixed in ((False,True)if prior['low']==1 else(False,)):
                passed=orbit_feasible(groups,fixed);outcomes.append(passed)
                if not passed:
                    require(not independent_orbit_feasible(groups,fixed),'independent orbit replay disagrees')
                    checked_rejections+=1
            if not any(outcomes):orbital.append(index)
            condition=fs_congruence(groups)
            if condition is not None:
                fs.append(index);conditions.append(dict(index=index,**condition))
            if any(outcomes)and condition is None:surviving.append(index)
        branches.append(dict(low=prior['low'],labelling=prior['labelling'],input_count=len(prior['unresolved']),fermion_orbit_rejected=orbital,center_fs_congruence_rejected=fs,center_fs_conditions=conditions,surviving_count=len(surviving),surviving_indices_sha256=hashlib.sha256(json.dumps(surviving,separators=(',',':')).encode()).hexdigest()))
    require(len(branches)==3,'unexpected frontier branch count')
    return dict(status='necessary_reduction_only_original_unresolved',exact=True,optimizer_used=False,conservative_low_one_action=['swap','two_fixed'],source_sha256=source_hashes,branches=branches,input_count=sum(b['input_count']for b in branches),fermion_orbit_exclusions=sum(len(b['fermion_orbit_rejected'])for b in branches),center_fs_congruence_exclusions=sum(len(b['center_fs_congruence_rejected'])for b in branches),surviving_count=sum(b['surviving_count']for b in branches),independently_rechecked_rejected_orbit_branches=checked_rejections)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package');parser.add_argument('--certificate',type=Path,default=HERE/'fermion_profiles_certificate.json');parser.add_argument('--write',action='store_true')
    args=parser.parse_args();start=time.time();result=reconstruct(locate_package(args.package))
    if args.write:args.certificate.write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads(args.certificate.read_text()),'small certificate differs from exact reconstruction')
    print(json.dumps(dict(passed=True,input_count=result['input_count'],fermion_exclusions=result['fermion_orbit_exclusions'],center_fs_exclusions=result['center_fs_congruence_exclusions'],surviving_count=result['surviving_count'],optimizer_used=False,seconds=round(time.time()-start,4))))
if __name__=='__main__':main()
