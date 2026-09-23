"""Exact verification of a modular-induction relaxation, not a category."""
from pathlib import Path
from fractions import Fraction as Q
import json
from exact import require
from modular_character_induction import reciprocity_data,equation_system,high_columns,system_rotation,s
from augmented_spectrum import AugmentedSpectrum
P=Path(__file__).resolve().parents[1]

def verify_record(R,c):
    require(c['kind']=='modular_frontier_feasible' and c['height']==6,'wrong frontier witness')
    data,tab=reciprocity_data(R);cols=list(map(tuple,c['columns']))
    require(cols in [list(map(tuple,x)) for x in data['lows']],'frontier frame not an admissible low frame')
    lab=tuple(c['labelling']);require(lab in tab.assignments(cols),'invalid character labelling')
    from higher_traces import indicator_choices
    require(tuple(c['indicators']) in indicator_choices(R),'invalid second indicators')
    L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=AugmentedSpectrum(tab,cols,high)
    require(not sp.missing_low and c['spectrum']==sp.metadata(),'wrong joint-dimension Galois pruning')
    A,b,meta=equation_system(R,data,tab,cols,c['indicators'],c['height'],lab,sp)
    require(meta==c['system'],'incorrect frontier equation/variable counts')
    z=[Q(x) for x in c['solution']]
    require(len(z)==len(A[0]) and min(z)>=0,'wrong or negative frontier variables')
    require(all(sum(Q(a)*v for a,v in zip(row,z))==bb for row,bb in zip(A,b)),'frontier point violates an exact equation')
    A0,b0,m0=system_rotation(R,data,L,c['indicators'],c['height']);labs=m0['labels']
    keep=[j for j in range(len(A0[0])) if j>=len(labs) or list(labs[j][0]) not in sp.forbidden]
    require(all(z[j].denominator==1 for j,k in enumerate(keep) if k<len(labs)),'high-object multiplicities not integral')
    require(all(x.denominator==1 for x in z),'the released frontier witness must have all coordinates integral')
    rank=len(cols)+sum(z[j] for j,k in enumerate(keep) if k<len(labs))
    require(str(rank)==c['formal_central_rank'],'wrong formal central rank')
    return {'passed':True,'equations':len(A),'variables':len(z),'formal_central_rank':int(rank),
            'all_variables_integral':True,'integral_high_object_counts':True,'scope':'Necessary central-induction constraints only; no modular datum, complete fusion ring, or category is asserted.'}

def verify():
    c=json.load(open(P/'systems/integral_frontier_215.json'));R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']==c['id'])
    return verify_record(R,c)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
