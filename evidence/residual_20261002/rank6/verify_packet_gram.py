"""Exact charge-Gram necessary conditions; the original ring remains unresolved."""
from pathlib import Path
import json, importlib.util, hashlib, time, os, argparse
from functools import lru_cache
import numpy as np

HERE=Path(__file__).resolve().parent
def find_package():
    for p in HERE.parents:
        for q in (p, p/'supplements/rank6', p/'classification-repo/supplements/rank6'):
            if (q/'data/census.json').is_file() and (q/'research/frontier/new_research/r1660_galois/verify.py').is_file():
                return q
    raise FileNotFoundError('Pass --package or set RANK6_PACKAGE to the multiplicity-nine package')

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package', type=Path, default=None)
parser.add_argument('--output', type=Path, default=HERE/'packet_gram_probe_receipt.json')
args=parser.parse_args()
PACKAGE=(args.package or (Path(os.environ['RANK6_PACKAGE']) if os.environ.get('RANK6_PACKAGE') else find_package())).resolve()
SOURCE_HASHES={}


def require(v,msg):
    if not v: raise RuntimeError(msg)

def read(p):
    SOURCE_HASHES[str(p.relative_to(PACKAGE))]=hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text())
def same(a,b):return a['low']==b['low'] and a['labelling']==b['labelling']
def load(p):
    spec=importlib.util.spec_from_file_location('galois_prerequisite',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

module_path=PACKAGE/'research/frontier/new_research/r1660_galois/verify.py'
SOURCE_HASHES[str(module_path.relative_to(PACKAGE))]=hashlib.sha256(module_path.read_bytes()).hexdigest()
module=load(module_path)

@lru_cache(None)
def search(gitems,fixed,delta_target):
    blocks=module.blocks_from(gitems)
    options=[]
    for keys,raw in blocks:
        values={}
        for j,(_,_,rank,_,e,o,t) in enumerate(raw):
            # All asymmetric restriction fibers have one common charge.
            if any(k[1]!=k[2] for k in keys):
                n=dict(gitems)[keys[0]][0]
                if e!=(n if delta_target else 0):continue
            q2=sum(e*(k[1]+k[2])**2 for k in keys)
            qa=sum(e*(k[1]+k[2])*k[4] for k in keys)
            a2=sum(e*k[4]**2 for k in keys)
            z2=sum(e*k[3]**2 for k in keys)
            d2=sum(e*(k[1]-k[2])**2 for k in keys)
            values.setdefault((q2,qa,a2,z2,d2,rank),j)
        options.append(tuple((v,j) for v,j in sorted(values.items())))
    if any(not x for x in options):return None
    order=sorted(range(len(options)),key=lambda i:(len(options[i]),-max(v[0][3] for v in options[i])))
    opts=[options[i] for i in order]
    tails=[]
    for pos in range(len(opts)+1):
        tails.append(tuple((sum(min(v[0][h] for v in op) for op in opts[pos:]),
                            sum(max(v[0][h] for v in op) for op in opts[pos:])) for h in range(6)))
    @lru_cache(None)
    def dfs(pos,target):
        if any(not lo<=x<=hi for x,(lo,hi) in zip(target,tails[pos])):return None
        if pos==len(opts):return () if all(x==0 for x in target) else None
        for vec,j in opts[pos]:
            rest=tuple(x-y for x,y in zip(target,vec))
            path=dfs(pos+1,rest)
            if path is not None:return(j,)+path
        return None
    path=dfs(0,(84,60,46,2,delta_target,-(2 if fixed else 3)))
    if path is None:return None
    answer=[0]*len(blocks)
    for i,j in zip(order,path):answer[i]=j
    return tuple(answer)

def audit_witness(L,gitems,fixed,delta_target,path):
    values=module.check_witness(gitems,fixed,True,path)
    even=list(L[:4]);odd=list(L[4:])
    for v in L[:4]:even.append((v[1],v[0],v[3],v[2],v[4],v[5]))
    for v,e,o,t in values:
        v=tuple(v);asym=v!=module.swap(v)
        for w in ([v,module.swap(v)] if asym else [v]):
            even.extend([(0,)+w]*(e if asym else 2*e))
            odd.extend([(0,)+w]*(o if asym else 2*o+t))
    # Integer matrix replay, independent of moment targets in search.
    R=np.array(even+odd,dtype=np.int64).T
    M=R.T@R
    J=np.diag([1]*len(even)+[-1]*len(odd))
    P=(M+J@M@J)//2;Q=M-P
    require(np.array_equal(P@Q,Q@P),'packet commutator')
    Hp=np.array(even,dtype=np.int64).T@np.array(even,dtype=np.int64)
    A=70+delta_target//2
    expected=np.array([[4,0,6,6,0,8],[0,4,6,6,0,8],[6,6,A,140-A,8,96],[6,6,140-A,A,8,96],[0,0,8,8,4,12],[8,8,96,96,12,140]])
    require(np.array_equal(Hp,expected),'even charge Gram')
    # H acts on restrictions by g; its action on repeated labels is irrelevant:
    # (H P)[r,s] is the corresponding g-translated restriction inner product.
    GR=R[[1,0,3,2,4,5],:]
    HP=(GR.T@R+J@(GR.T@R)@J)//2
    require(np.array_equal(P@P-Q@Q,2*(P-HP)),'packet square identity')
    return values

def main():
    start=time.time()
    old=read(PACKAGE/'research/round5/m8_actual48/certificate.json')
    ferm=read(PACKAGE/'research/frontier/R6_8_1660/fermion_profiles/fermion_profiles_certificate.json')
    spin=read(PACKAGE/'research/frontier/R6_8_1660/spin_profiles/spin_profiles_certificate.json')
    gal=read(PACKAGE/'research/frontier/new_research/r1660_galois/certificate.json')
    results=[]
    for gb in gal['branches']:
        ob=next(b for b in old['branches'] if b['outcome']=='profile_frontier' and same(b,gb))
        fb=next(b for b in ferm['branches'] if same(b,gb));sb=next(b for b in spin['branches'] if same(b,gb))
        bad=set(fb['fermion_orbit_rejected']+fb['center_fs_congruence_rejected']+sb['alpha_even_rejected']+sb['amv_fs16_rejected']+gb['rejected'])
        indices=[i for i in ob['unresolved'] if i not in bad]
        require(len(indices)==gb['surviving_count'],'input count')
        raw=read(PACKAGE/ob['source'])['branches'][0]
        L=tuple(map(tuple,raw['columns']));V=tuple(map(tuple,raw['high_vectors']))
        case=next(c for c in raw['cases'] if c['labelling']==gb['labelling'])
        survivors=[];rejected=[];witnesses=[]
        for idx in indices:
            profile=tuple(case['profiles'][idx]);gitems=module.groups(L,V,profile)
            found=None
            for fixed in ([False,True] if gb['low']==1 else [False]):
                for delta in ([0,4] if gb['low']==1 else [0]):
                    path=search(gitems,fixed,delta)
                    if path is not None:
                        values=audit_witness(L,gitems,fixed,delta,path)
                        found=dict(profile=idx,low_fixed=fixed,delta_moment=delta,groups=values)
                        break
                if found:break
            if found:survivors.append(idx);witnesses.append(found)
            else:rejected.append(idx)
        row=dict(low=gb['low'],labelling=gb['labelling'],input_count=len(indices),rejected=rejected,
                 surviving_count=len(survivors),survivors=survivors,witnesses=witnesses)
        results.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ('survivors','witnesses','rejected')}),flush=True)
    out=dict(status='necessary_charge_gram_reduction_original_ring_unresolved',exact=True,optimizer_used=False,
             source_sha256=SOURCE_HASHES,input_count=sum(r['input_count'] for r in results),excluded_count=sum(len(r['rejected']) for r in results),
             surviving_count=sum(r['surviving_count'] for r in results),branches=results)
    args.output.write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='branches'}),flush=True)

if __name__=='__main__':main()
