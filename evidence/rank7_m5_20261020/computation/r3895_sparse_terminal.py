"""Recover exact terminal rays after removing fixed variables and lower bounds.

The reduced ray is lifted to every original equation/bound row and accepted
only after exact Farkas verification in the original full integer system.
This discovery helper never mutates the leased probing checkpoint.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,signal,time
from pathlib import Path


def require(c,message):
    if not c:raise ValueError(message)


def reduce_bounds(A,b,bounds):
    m=len(b);n=len(A[0]);lower=[0]*n;fixed={};upper={}
    require(len(A)==m and all(len(row)==n for row in A),'rectangular integer system')
    for j,(lo,hi) in bounds.items():
        require(type(j)is int and 0<=j<n and type(lo)is int and lo>=0 and (hi is None or type(hi)is int and hi>=lo),'valid integer bound')
        lower[j]=lo
        if hi==lo:fixed[j]=lo
        elif hi is not None:upper[j]=hi-lo
    keep=[j for j in range(n) if j not in fixed];position={j:k for k,j in enumerate(keep)};upper_order=sorted(upper)
    rhs=[v-sum(row[j]*lo for j,lo in enumerate(lower) if lo) for row,v in zip(A,b)]
    matrix=[[row[j] for j in keep]+[0]*len(upper_order) for row in A]
    for k,j in enumerate(upper_order):
        row=[0]*(len(keep)+len(upper_order));row[position[j]]=1;row[len(keep)+k]=1;matrix.append(row);rhs.append(upper[j])
    return matrix,rhs,{'keep':keep,'fixed':fixed,'lower':lower,'upper_order':upper_order,'base_equations':m}


def lift_ray(A,b,bounds,reduced_ray,meta):
    m=len(b);n=len(A[0]);require(meta['base_equations']==m and len(reduced_ray)==m+len(meta['upper_order']),'reduced ray dimensions')
    require(all(type(z)is int for z in reduced_ray),'integral reduced covector')
    base=reduced_ray[:m];uppers=dict(zip(meta['upper_order'],reduced_ray[m:]));require(all(z>=0 for z in uppers.values()),'nonnegative reduced upper slack weights')
    rowweights={}
    for j in range(n):
        w=sum(row[j]*y for row,y in zip(A,base));lo,hi=bounds.get(j,(0,None))
        if j in meta['fixed']:
            require(hi==lo==meta['fixed'][j],'fixed-value metadata')
            if lo>0:rowweights[j,-1]=min(0,-w)
            rowweights[j,1]=max(0,-w)
        else:
            u=uppers.get(j,0);require(w+u>=0,'nonnegative reduced variable coefficient')
            if hi is not None:rowweights[j,1]=u
            if lo>0:rowweights[j,-1]=-(w+u)
    lifted=base[:]
    for j,(lo,hi) in sorted(bounds.items()):
        if lo>0:lifted.append(rowweights[j,-1])
        if hi is not None:lifted.append(rowweights[j,1])
    return lifted


def main():
    from r3895_c8_tree import build
    from r3895_exact_probing import replay_steps,digest
    from exact_branch_bound import exact_ray,check_farkas,bound_system
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',type=int,default=2);p.add_argument('--branch',type=int,default=19);p.add_argument('--r',type=int,default=5);p.add_argument('--s',type=int,default=1);p.add_argument('--seconds',type=int,default=300);args=p.parse_args()
    here=Path(__file__).resolve().parent;stem=f'R7_5_3895_c8_case{args.case}_phi{args.branch}_r{args.r}_s{args.s}'
    path=here/(stem+'_exact_probing.json');raw=path.read_bytes();record=json.loads(raw)
    A,b,kept,phase_count,bindings,capacities=build(args.case,args.branch,args.r,args.s)
    require(record['source_hashes']==bindings and record['matrix_sha256']==digest([A,b]) and record['capacities']==capacities,'frozen source/matrix/capacity binding')
    bounds=replay_steps(A,b,record['steps']);full,target=bound_system(A,b,bounds)
    if record.get('terminal_y') is not None:
        check_farkas(full,target,record['terminal_y']);print(json.dumps({'status':'already_complete'}));return
    matrix,rhs,meta=reduce_bounds(A,b,bounds);start=time.monotonic()
    output={'case':args.case,'branch':args.branch,'r':args.r,'s':args.s,'checkpoint_sha256':hashlib.sha256(raw).hexdigest(),'matrix_sha256':record['matrix_sha256'],'steps':len(record['steps']),
            'original_shape':[len(full),len(full[0])],'reduced_shape':[len(matrix),len(matrix[0])],'fixed_variables':len(meta['fixed']),
            'scope':'Exact terminal-ray candidate bound to a read-only probing checkpoint; no checkpoint mutation.'}
    def timeout(signum,frame):raise TimeoutError('bounded sparse exact recovery')
    old=signal.signal(signal.SIGALRM,timeout);signal.alarm(args.seconds)
    try:ray=exact_ray(matrix,rhs)
    except TimeoutError:ray=None;output['timed_out']=True
    finally:signal.alarm(0);signal.signal(signal.SIGALRM,old)
    if ray is None:output['status']='no_exact_ray'
    else:
        check_farkas(matrix,rhs,ray);lifted=lift_ray(A,b,bounds,ray,meta);check_farkas(full,target,lifted)
        require(sum(v*y for v,y in zip(rhs,ray))==sum(v*y for v,y in zip(target,lifted)),'exactly preserved negative Farkas target')
        output.update(status='exact_terminal_candidate',reduced_y=ray,terminal_y=lifted)
    output['seconds']=time.monotonic()-start;(here/(stem+'_sparse_terminal.json')).write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('reduced_y','terminal_y')}),flush=True)
if __name__=='__main__':main()
