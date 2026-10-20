"""Independent raw-tensor audit of the seven/eighteen active row allocations."""
import collections,hashlib,json,math
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).parent;BASE=HERE.parent;ROOT=BASE.parents[1]

def require(v,m):
    if not v:raise RuntimeError(m)

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def psd(A):
    A=[list(map(Q,row)) for row in A];n=len(A)
    for k in range(n):
        if A[k][k]<0:return False
        if not A[k][k]:
            if any(A[k][j] for j in range(k+1,n)):return False
            continue
        for i in range(k+1,n):
            for j in range(k+1,n):A[i][j]-=A[i][k]*A[k][j]/A[k][k]
    return True

def run(branch):
    ipath=BASE/'integral_gram'/f'R7_5_5039_chi8_active_{branch}.json';record=json.loads(ipath.read_text())
    c4path=BASE/'integral_gram'/f'R7_5_5039_c4_system_3_0_chi8_{branch}.json';system=json.loads(c4path.read_text())
    census=json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text());N=next(r['tensor'] for r in census if r['id']=='R7_5_5039')
    require(digest(N)==record['source_sha256']==system['source_sha256'],'Canonical source identity.')
    require(hashlib.sha256(c4path.read_bytes()).hexdigest()==record['system_sha256'],'Frozen C4 system identity.')
    require(digest(system['orbits'])==record['orbit_sha256'] and digest(system['low'])==record['low_sha256'],'Orbit and low identity.')
    dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    B=[[sum(N[a][j][k]*N[k][dual[a]][i] for a in range(7) for k in range(7)) for j in range(7)] for i in range(7)]
    low=[(1,0,0,0,0,0,0)]+system['low']
    bound=[[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in low) for j in range(6)] for i in range(6)]
    weights={};units={};orbits=system['orbits']
    for lab in system['phase_labels']:
        k=lab['orbit'];w=sum((v[0]-v[1])**2 for v,g,z in orbits[k])
        if w:weights[k]=w;units[k]=math.gcd(units.get(k,0),lab['multiplicity_unit'])
    require(weights=={int(k):v for k,v in record['weights'].items()},'Reconstructed active weights.')
    require(units=={int(k):v for k,v in record['multiplicity_units'].items()},'Reconstructed packet gcds.')
    active=sorted(weights);require(active==record['active_orbits'],'Complete active set.')
    grams={k:[[sum(v[i]*v[j] for v,g,z in orbits[k]) for j in range(6)] for i in range(6)] for k in active}
    statistics=collections.Counter();branches=[];preg=[]
    small=[k for k in active if weights[k]==2]
    if branch==2:require(len(small)==1,'Unique orbit fitting either two-unit bucket.')
    def visit(pos,left,chosen):
        if pos<len(active):
            k=active[pos];step=weights[k]*units[k]
            for n in range(left//step+1):
                chosen[k]=n*units[k];visit(pos+1,left-n*step,chosen)
            chosen.pop(k,None);return
        if left:return
        statistics['raw']+=1
        if branch==2 and chosen[small[0]]<2:statistics['two_small_buckets']+=1;return
        allocation=[[k,n] for k,n in sorted(chosen.items()) if n];preg.append(allocation)
        R=[[bound[i][j]-sum(chosen[k]*grams[k][i][j] for k in active) for j in range(6)] for i in range(6)]
        if any(x<0 for row in R for x in row):statistics['negative_gram']+=1;return
        if any(row[0]!=row[1] for row in R):statistics['difference_kernel']+=1;return
        if not psd(R):statistics['psd']+=1;return
        branches.append(allocation);statistics['remaining']+=1
    visit(0,16,{})
    require(dict(statistics)==record['statistics'],'Independent allocation statistics.')
    require(preg==record['pre_gram_allocations'] and branches==record['branches'],'Complete allocation list replay.')
    c8checks=[]
    for case in (0,1):
        path=BASE/'criteria'/f'R7_5_5039_c8_case{case}_chi8_{branch}_system.json';c8=json.loads(path.read_text())
        require(c8['orbits']==system['orbits'] and c8['low']==system['low'],'C8 uses the identical orbit order and low frame.')
        for lab in c8['phase_labels']:
            k=lab['orbit'];w=sum((v[0]-v[1])**2 for v,g,z in c8['orbits'][k])
            if w:require(k in active and w==weights[k] and lab['multiplicity_unit']%units[k]==0,'C8 active packet lies in C4 allocation relaxation.')
        c8checks.append({'case':case,'system_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'phase_columns':len(c8['phase_labels'])})
    return {'branch':branch,'raw':statistics['raw'],'allocations':len(branches),'inventory_sha256':hashlib.sha256(ipath.read_bytes()).hexdigest(),
            'source_sha256':digest(N),'orbit_sha256':digest(orbits),'c8_checks':c8checks}

if __name__=='__main__':
    result={'status':'PASS','proof':'Independent raw-tensor Gram and rational Schur-complement enumeration; C8 active packets project into the complete C4 gcd relaxation.',
            'results':[run(0),run(2)]}
    (HERE/'chi8_allocation_independent_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
