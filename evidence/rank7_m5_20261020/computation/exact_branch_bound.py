"""Discovery of finite integer-split trees with exact Farkas leaves."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,math,sys,time
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];INPUT=HERE.parent/'integral_gram'
sys.path.insert(0,str(ROOT/'supplements/rank7/software'))
from higher_traces import farkas,check_farkas
from inactive_lattice import require


def exact_ray(A,b):
    ray=farkas(A,b)
    if ray is not None:return ray
    # Alternative proposals are still accepted only by the complete integer check.
    aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);m=len(b)
    scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)))
    matrix=aa/scale[:,None];rhs=bb/scale
    solved=linprog(np.ones(2*m),A_ub=np.r_[np.c_[-matrix.T,matrix.T],np.r_[rhs,-rhs][None,:]],
                   b_ub=np.r_[np.zeros(aa.shape[1]),-1.],bounds=(0,None),method='highs',
                   options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    if not solved.success:return None
    values=(solved.x[:m]-solved.x[m:])/scale;values/=max(abs(values))
    for denominator in (8,32,128,1024,10000,1000000):
        proposed=[Fraction(float(x)).limit_denominator(denominator) if abs(x)>1e-10 else Fraction(0) for x in values]
        common=math.lcm(*(x.denominator for x in proposed));candidate=[int(x*common) for x in proposed]
        if check_farkas(A,b,candidate,raise_error=False):return candidate
    import sympy as s
    support=np.flatnonzero(abs(values)>1e-10).tolist()
    for threshold in (1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4):
        active=np.flatnonzero(abs(aa.T@values)<threshold).tolist()
        C=s.Matrix([[A[i][j] for i in support] for j in active]+[[b[i] for i in support]])
        target=s.zeros(C.rows,1);target[-1]=-1;reduced,pivots=C.row_join(target).rref()
        if pivots and pivots[-1]>=len(support):continue
        vector=[s.Rational(0)]*len(support)
        for row,pivot in enumerate(pivots):vector[pivot]=reduced[row,-1]
        common=math.lcm(*(int(x.q) for x in vector));candidate=[0]*m
        for i,x in zip(support,vector):candidate[i]=int(x*common)
        if check_farkas(A,b,candidate,raise_error=False):return candidate
    return None


def bound_system(A,b,bounds):
    inequalities=[]
    for j,(low,high) in sorted(bounds.items()):
        if low>0:inequalities.append((j,-1,low))
        if high is not None:inequalities.append((j,1,high))
    width=len(A[0]);extra=len(inequalities)
    matrix=[row+[0]*extra for row in A];rhs=b[:]
    for k,(j,sign,value) in enumerate(inequalities):
        row=[0]*(width+extra);row[j]=1;row[width+k]=sign;matrix.append(row);rhs.append(value)
    return matrix,rhs


def replay(A,b,node,bounds=None):
    bounds={} if bounds is None else bounds
    if 'y' in node:
        matrix,rhs=bound_system(A,b,bounds);check_farkas(matrix,rhs,node['y']);return 1
    j=node['variable'];k=node['floor'];require(type(j)is int and 0<=j<len(A[0]) and type(k)is int,'integer split')
    low,high=bounds.get(j,(0,None));require(k>=low and (high is None or k<high),'nontrivial complete integer split')
    left=dict(bounds);left[j]=(low,k);right=dict(bounds);right[j]=(k+1,high)
    return replay(A,b,node['left'],left)+replay(A,b,node['right'],right)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--frame',type=int,default=6);ap.add_argument('--branch',type=int,default=0)
    ap.add_argument('--case',type=int,default=0);ap.add_argument('--budget',type=int,default=600);ap.add_argument('--nodes',type=int,default=2000)
    ap.add_argument('--replay',type=Path);args=ap.parse_args();start=time.monotonic()
    system_path=INPUT/f'R7_5_3895_system_{args.frame}_{args.case}.json';system_raw=system_path.read_bytes();system=json.loads(system_raw)
    inventory_path=HERE/f'R7_5_3895_branch_lattice_{args.frame}.json';inventory_raw=inventory_path.read_bytes();inventory=json.loads(inventory_raw)
    entry=next(r for r in inventory['branches'] if r['index']==args.branch);kept=entry['kept_columns'];active=dict(entry['active_counts'])
    b=[v-sum(system['columns'][j][i]*c for j,c in active.items()) for i,v in enumerate(system['rhs'])]
    A=[[system['columns'][j][i] for j in kept] for i in range(len(b))]
    hashes={'system':hashlib.sha256(system_raw).hexdigest(),'inventory':hashlib.sha256(inventory_raw).hexdigest()}
    if args.replay:
        certificate=json.loads(args.replay.read_text());require(certificate['source_hashes']==hashes,'source binding')
        leaves=replay(A,b,certificate['tree']);print(json.dumps({'status':'PASS','leaves':leaves,'optimized_python':not __debug__}));return
    aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)))
    primalA=aa/scale[:,None];primalb=bb/scale
    phase_count=len(system['phase_selection']);stats={'nodes':0,'leaves':0,'depth':0}
    path=HERE/f'R7_5_3895_bnb_{args.frame}_{args.branch}_{args.case}.json';partial=path.with_suffix('.progress.json')
    def solve(bounds,depth):
        stats['nodes']+=1;stats['depth']=max(stats['depth'],depth)
        if stats['nodes']>args.nodes or time.monotonic()-start>args.budget:raise TimeoutError('finite-tree discovery budget exhausted')
        options=[bounds.get(j,(0,None)) for j in range(len(kept))]
        result=linprog(np.zeros(len(kept)),A_eq=primalA,b_eq=primalb,bounds=options,method='highs')
        if not result.success:
            matrix,rhs=bound_system(A,b,bounds);ray=exact_ray(matrix,rhs)
            if ray is None:raise RuntimeError('unsuccessful numerical LP lacked an exact Farkas ray: '+result.message)
            check_farkas(matrix,rhs,ray);stats['leaves']+=1
            partial.write_text(json.dumps({'status':'partial','statistics':stats,'seconds':time.monotonic()-start})+'\n')
            print(json.dumps({'event':'exact_leaf',**stats,'seconds':time.monotonic()-start}),flush=True)
            return {'y':ray}
        if not result.success:raise RuntimeError('LP proposal failed: '+result.message)
        fractions=[(min(x-math.floor(x),math.ceil(x)-x),j,x) for j,x in enumerate(result.x) if abs(x-round(x))>1e-6]
        if not fractions:
            integers=[round(float(x)) for x in result.x]
            if all(sum(a*x for a,x in zip(row,integers))==rhs for row,rhs in zip(A,b)):
                raise RuntimeError('exact feasible integer point; no exclusion')
            raise RuntimeError('near-integer proposal failed exact equations')
        slack=[item for item in fractions if kept[item[1]]>=phase_count]
        _,j,x=max(slack or fractions);k=math.floor(x);low,high=bounds.get(j,(0,None))
        require(k>=low and (high is None or k<high),'valid split proposal')
        left=dict(bounds);left[j]=(low,k);right=dict(bounds);right[j]=(k+1,high)
        return {'variable':j,'floor':k,'left':solve(left,depth+1),'right':solve(right,depth+1)}
    try:tree=solve({},0)
    except (RuntimeError,TimeoutError) as exc:
        partial.write_text(json.dumps({'status':'no_complete_certificate','reason':str(exc),'statistics':stats,'seconds':time.monotonic()-start})+'\n')
        print(partial.read_text(),flush=True);return
    leaves=replay(A,b,tree)
    output={'id':'R7_5_3895','low_index':args.frame,'active_branch':args.branch,'case':args.case,'source_hashes':hashes,
            'scope':'Finite integer infeasibility for this recorded necessary-data branch only.','tree':tree,'leaves':leaves,'statistics':stats,'seconds':time.monotonic()-start}
    path.write_text(json.dumps(output,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in output.items() if k!='tree'}),flush=True)


if __name__=='__main__':main()
