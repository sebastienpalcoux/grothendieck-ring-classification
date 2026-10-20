"""Independent standard-library replay of a complete R3895 probing chain.

The raw induction Gram, active-row mapping, one-unit pruning, C4 choice and
every orbit capacity are rebuilt without the producer's domain helpers.
Completeness of the global C8/low/phi/C4 domain is a separate obligation.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=HERE.parents[2]
SOURCE='590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0'


def require(ok,why):
    if not ok:raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def psd(A):
    A=[[F(v) for v in row] for row in A]
    for k in range(len(A)):
        if A[k][k]<0:return False
        if not A[k][k]:
            if any(A[k][j] for j in range(k+1,len(A))):return False
            continue
        for i in range(k+1,len(A)):
            for j in range(k+1,len(A)):
                A[i][j]-=A[i][k]*A[k][j]/A[k][k]
    return True


def subtract(A,G,count=1):return [[x-count*G[i][j] for j,x in enumerate(row)] for i,row in enumerate(A)]
def admissible(A):return all(x>=0 for row in A for x in row) and psd(A)


def reconstruct(case,branch,r,s):
    source=next(row['tensor'] for row in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if row['id']=='R7_5_3895')
    require(digest(source)==SOURCE,'canonical source tensor')
    path=HERE/f'R7_5_3895_c8_case{case}_system.json';system=json.loads(path.read_text())
    require(system['source_sha256']==SOURCE,'full C8 source binding')
    N=source
    B=[[sum(N[k][i][j]*N[k][h][j] for k in range(7) for j in range(7)) for h in range(7)] for i in range(7)]
    dompath=BASE/'integral_gram/R7_5_3895_domains.json'
    oldpath=BASE/'integral_gram/R7_5_3895_system_8_0.json'
    apath=BASE/'integral_gram/R7_5_3895_active_8.json'
    dom=next(x for x in json.loads(dompath.read_text()) if x['low_index']==8)
    old=json.loads(oldpath.read_text());allocation=json.loads(apath.read_text())['branches'][branch]
    require(system['low']==dom['low'],'same complete low frame')
    key=lambda orb:tuple(tuple(v) for v,g,z in orb)
    wanted={}
    for j,count in allocation:
        original=old['phase_selection'][j];k=key(dom['orbits'][original//10])
        require(k not in wanted,'unique old saturated orbit')
        wanted[k]=count*old['multipliers'][original]
    labels=system['phase_labels'];orbits=system['orbits'];active=set();support=[];seen=set()
    grams=[[[sum(v[i]*v[j] for v,g,z in orb) for j in range(6)] for i in range(6)] for orb in orbits]
    bound=[[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in system['low']) for j in range(6)] for i in range(6)]
    for j,lab in enumerate(labels):
        orb=orbits[lab['orbit']]
        if not any(v[3]!=v[4] for v,g,z in orb):continue
        k=key(orb);require(k not in seen,'unique complete saturated C8 phase');seen.add(k);active.add(j)
        count=wanted.get(k,0);require(count%lab['multiplicity_unit']==0,'integer C8 packet count')
        if count:
            support.append([j,count//lab['multiplicity_unit']])
            bound=subtract(bound,grams[lab['orbit']],count)
    require(set(wanted)<=seen and admissible(bound),'complete positive active mapping and Gram')
    rhs=[b-sum(n*system['columns'][j][i] for j,n in support) for i,b in enumerate(system['rhs'])]
    kept=[];removed=[]
    for j in range(len(system['columns'])):
        if j in active:continue
        if j<len(labels):
            lab=labels[j]
            if not admissible(subtract(bound,grams[lab['orbit']],lab['multiplicity_unit'])):
                removed.append(j);continue
        kept.append(j)
    obj=system['cyclic_four'][0]
    require(obj['source_object']==1 and obj['A']==9 and obj['B']==2,'complete source C4 character domain')
    require(type(r)is int and 0<=r<=9 and type(s)is int and 0<=s<=2,'integer C4 choice')
    fixed=dict(zip(obj['variables'],(r,9-r,s,2-s)))
    rhs=[b-sum(n*system['columns'][j][i] for j,n in fixed.items()) for i,b in enumerate(rhs)]
    kept=[j for j in kept if j not in fixed]
    columns=[system['columns'][j][:] for j in kept]
    groups={}
    for pos,j in enumerate(kept):
        if j<len(labels):groups.setdefault(labels[j]['orbit'],[]).append((pos,labels[j]['multiplicity_unit']))
    capacities=[]
    for oi,variables in sorted(groups.items()):
        gram=grams[oi];upper=min(bound[i][j]//gram[i][j] for i in range(6) for j in range(6) if gram[i][j])
        possible=[n for n in range(upper+1) if psd(subtract(bound,gram,n))]
        require(possible==list(range(max(possible)+1)),'exact PSD capacity initial interval')
        maximum=max(possible);divisor=math.gcd(*(u for j,u in variables));capacity=maximum-maximum%divisor
        for col in columns:col.append(0)
        for pos,unit in variables:columns[pos][-1]=unit
        rhs.append(capacity);slack=[0]*len(rhs);slack[-1]=1;columns.append(slack)
        capacities.append({'orbit':oi,'integer_psd_capacity':maximum,'packet_gcd':divisor,'capacity':capacity})
    return [list(row) for row in zip(*columns)],rhs,kept,capacities,{'support':support,'gram_removed':len(removed),'system_sha256':sha(path)}


def branch_bounds(bounds,j,k,side,width):
    require(type(j)is int and 0<=j<width and type(k)is int and side in (0,1),'integer branch data')
    low,high=bounds.get(j,(0,None))
    require(low<=k and (high is None or k<high),'complete nontrivial integer partition')
    result=dict(bounds);result[j]=(low,k) if side==0 else (k+1,high)
    return result


def leaf(A,b,bounds,y):
    constraints=[]
    for j,(low,high) in sorted(bounds.items()):
        if low>0:constraints.append((j,-1,low))
        if high is not None:constraints.append((j,1,high))
    require(len(y)==len(b)+len(constraints) and all(type(v)is int for v in y),'exact integral leaf covector')
    # Zero entries of an exact covector make no contribution. Keeping only
    # its support accelerates long chains without omitting any column check.
    support=[(row,v) for row,v in zip(A,y) if v]
    coeff=[sum(row[j]*v for row,v in support) for j in range(len(A[0]))]
    target=sum(x*v for x,v in zip(b,y) if v)
    for (j,sign,value),v in zip(constraints,y[len(b):]):
        coeff[j]+=v;target+=value*v
        require(sign*v>=0,'nonnegative bound-slack coefficient')
    require(min(coeff)>=0 and target<0,'exact Farkas contradiction on every column')


def verify(case,branch,r,s,*,check_tree=True):
    A,b,kept,caps,meta=reconstruct(case,branch,r,s)
    prefix=f'R7_5_3895_c8_case{case}_phi{branch}_r{r}_s{s}'
    path=BASE/'computation'/(prefix+'_exact_probing.json');record=json.loads(path.read_text())
    require(record['id']=='R7_5_3895' and [record[k] for k in ('case','branch','r','s')]==[case,branch,r,s],'exact conditional branch')
    require(record['status']=='complete_conditional_exclusion' and 'terminal_y'in record,'only a complete chain proves exclusion')
    require(digest([A,b])==record['matrix_sha256'] and caps==record['capacities'],'independently reconstructed entire matrix and capacities')
    require(all(sha(ROOT/p)==h for p,h in record['source_hashes'].items()),'all recorded inputs match bytes')
    bounds={}
    for step in record['steps']:
        j,k,bad=(step[x] for x in ('variable','floor','discarded_side'))
        require(step['original']==(kept[j] if j<len(kept) else None),'original variable identity')
        leaf(A,b,branch_bounds(bounds,j,k,bad,len(A[0])),step['y'])
        bounds=branch_bounds(bounds,j,k,1-bad,len(A[0]))
    leaf(A,b,bounds,record['terminal_y'])
    require({str(k):list(v) for k,v in sorted(bounds.items())}==record['forced_bounds'],'complete final forced bounds')
    treepath=BASE/'computation'/(prefix+'_probed_tree.json')
    if check_tree and treepath.exists():
        tree_record=json.loads(treepath.read_text());tree={'y':record['terminal_y']}
        for step in reversed(record['steps']):
            bad={'y':step['y']}
            tree={'variable':step['variable'],'floor':step['floor'],
                  'left':bad if step['discarded_side']==0 else tree,
                  'right':tree if step['discarded_side']==0 else bad}
        require(tree==tree_record['tree'] and tree_record['leaves']==len(record['steps'])+1,'exact exhaustive standard-tree conversion')
        require(tree_record['probing_sha256']==sha(path),'tree bound to this probing chain')
    return {'status':'PASS','case':case,'branch':branch,'r':r,'s':s,
            'source_sha256':SOURCE,'matrix_sha256':digest([A,b]),'steps':len(record['steps']),
            'leaves':len(record['steps'])+1,'variables':len(A[0]),'equations':len(b),'capacities':len(caps),
            'source_reconstruction':meta,'certificate_sha256':sha(path),
            'scope':'Exact conditional exclusion; full remaining-branch coverage is separate.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,default=0);p.add_argument('--branch',type=int,default=0)
    p.add_argument('--r',type=int,default=5);p.add_argument('--s',type=int,default=1);a=p.parse_args()
    out=verify(a.case,a.branch,a.r,a.s);out['optimized_python']=not __debug__
    path=HERE/f'R7_5_3895_case{a.case}_phi{a.branch}_r{a.r}_s{a.s}_probing_independent_{"optimized" if not __debug__ else "normal"}.json'
    path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))


if __name__=='__main__':main()
