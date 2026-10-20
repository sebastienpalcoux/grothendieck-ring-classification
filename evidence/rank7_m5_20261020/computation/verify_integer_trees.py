"""Independent integer-only replay of finite split trees; no optimizer imports."""
import argparse,copy,hashlib,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'


def require(value,message):
    if not value:raise ValueError(message)


def verify_tree(columns,rhs,node,bounds=None):
    bounds={} if bounds is None else bounds
    if 'y' in node:
        constraints=[]
        for variable,(low,high) in sorted(bounds.items()):
            if low>0:constraints.append((variable,-1,low))
            if high is not None:constraints.append((variable,1,high))
        ray=node['y'];n=len(rhs)
        require(len(ray)==n+len(constraints) and all(type(x)is int for x in ray),'complete integer ray')
        scores=[sum(x*y for x,y in zip(column,ray[:n])) for column in columns]
        scalar=sum(x*y for x,y in zip(rhs,ray[:n]))
        for (variable,slack_sign,bound),value in zip(constraints,ray[n:]):
            require(slack_sign*value>=0,'negative bound slack coefficient')
            scores[variable]+=value;scalar+=bound*value
        require(scalar<0 and all(x>=0 for x in scores),'invalid exact leaf inequality')
        return 1
    variable=node['variable'];floor=node['floor']
    require(type(variable)is int and 0<=variable<len(columns) and type(floor)is int,'integer split variable')
    low,high=bounds.get(variable,(0,None))
    require(floor>=low and (high is None or floor<high),'split does not cover the integer domain')
    left=dict(bounds);left[variable]=(low,floor);right=dict(bounds);right[variable]=(floor+1,high)
    return verify_tree(columns,rhs,node['left'],left)+verify_tree(columns,rhs,node['right'],right)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--frame',type=int,choices=(6,8),default=6);args=ap.parse_args()
    start=time.monotonic();results=[];sources={};controls=0
    for branch in ([0,14,122,125] if args.frame==6 else [19]):
        for case in (0,2,4,6):
            candidate=HERE/f'R7_5_3895_bnb_{args.frame}_{branch}_{case}.json';record=json.loads(candidate.read_text())
            system_path=INPUT/f'R7_5_3895_system_{args.frame}_{case}.json';system_bytes=system_path.read_bytes();system=json.loads(system_bytes)
            inventory_path=HERE/f'R7_5_3895_branch_lattice_{args.frame}.json';inventory_bytes=inventory_path.read_bytes();inventory=json.loads(inventory_bytes)
            require(record['source_hashes']=={'system':hashlib.sha256(system_bytes).hexdigest(),'inventory':hashlib.sha256(inventory_bytes).hexdigest()},'tree/source binding')
            entry=next(b for b in inventory['branches'] if b['index']==branch);active=dict(entry['active_counts'])
            rhs=[b-sum(system['columns'][j][i]*c for j,c in active.items()) for i,b in enumerate(system['rhs'])]
            columns=[system['columns'][j] for j in entry['kept_columns']]
            leaves=verify_tree(columns,rhs,record['tree']);require(leaves==record['leaves'],'leaf count')
            altered=copy.deepcopy(record['tree']);leaf=altered
            while 'left' in leaf:leaf=leaf['left']
            leaf['y']=[0]*len(leaf['y'])
            try:verify_tree(columns,rhs,altered)
            except ValueError:controls+=1
            else:raise ValueError('zero separating ray accepted')
            results.append({'low_index':args.frame,'branch':branch,'case':case,'leaves':leaves})
            sources[candidate.name]=hashlib.sha256(candidate.read_bytes()).hexdigest()
    output={'status':'PASS','scope':'Exact infeasibility of the listed integer necessary-data branches; source/domain derivation and pruning separately replayed.',
            'optimized_python':not __debug__,'results':results,'source_hashes':sources,
            'corrupted_leaf_controls_rejected':controls,'optimizer_imports':False,'seconds':time.monotonic()-start}
    path=HERE/f'integer_trees_{args.frame}_{"optimized" if not __debug__ else "normal"}.json'
    path.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='source_hashes'},indent=2))


if __name__=='__main__':main()
