"""Independent integer controls for fixed/lower-bound elimination and ray lifts."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
PATH=HERE.parents[1]/'computation/r3895_sparse_terminal.py'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify():
    spec=importlib.util.spec_from_file_location('_audited_sparse_terminal',PATH)
    helper=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rng=random.Random(38952026)
    bound_types=((0,None),(1,None),(0,3),(1,3),(0,0),(2,2))
    checked=0
    strict=0
    fixed_zero=0
    all_fixed=0
    for trial in range(1800):
        n=1+trial%4
        A=[[rng.randrange(-4,5) for j in range(n)] for i in range(2)]
        b=[rng.randrange(-6,7) for i in range(2)]
        bounds={j:bound_types[rng.randrange(len(bound_types))] for j in range(n)}
        M,rhs,meta=helper.reduce_bounds(A,b,bounds)
        keep=[j for j in range(n) if bounds[j][1]!=bounds[j][0]]
        upper=[j for j in range(n) if bounds[j][1] is not None and j in keep]
        require(meta['keep']==keep and meta['upper_order']==upper,'exact kept and upper-bound inventories')
        # Independent substitution check on sample feasible shifted vectors.
        shifted=[min(rng.randrange(3),bounds[j][1]-bounds[j][0]) if bounds[j][1] is not None else rng.randrange(3) for j in keep]
        original=[bounds[j][0] for j in range(n)]
        for j,x in zip(keep,shifted):original[j]+=x
        augmented=shifted+[bounds[j][1]-original[j] for j in upper]
        for i,row in enumerate(A):
            require(sum(x*y for x,y in zip(M[i],augmented))-rhs[i]==sum(x*y for x,y in zip(row,original))-b[i],
                    'original and shifted affine residuals agree')
        require(all(sum(x*y for x,y in zip(row,augmented))==value for row,value in zip(M[2:],rhs[2:])),
                'all reduced upper-bound slack equations')
        for base in itertools.product(range(-2,3),repeat=2):
            weights=[rng.randrange(4) for j in upper]
            y=list(base)+weights
            if any(sum(M[i][j]*y[i] for i in range(len(M)))<0 for j in range(len(M[0]))):
                continue
            lifted=helper.lift_ray(A,b,bounds,y,meta)
            # Reconstruct the original bound rows independently: lower rows
            # x_j - s_j = l_j; upper rows x_j + s_j = h_j.
            original_scores=[sum(A[i][j]*lifted[i] for i in range(2)) for j in range(n)]
            target=sum(b[i]*lifted[i] for i in range(2))
            offset=2
            for j,(lo,hi) in sorted(bounds.items()):
                if lo:
                    value=lifted[offset];offset+=1
                    require(value<=0,'lower slack coefficient has correct sign')
                    original_scores[j]+=value;target+=lo*value
                if hi is not None:
                    value=lifted[offset];offset+=1
                    require(value>=0,'upper slack coefficient has correct sign')
                    original_scores[j]+=value;target+=hi*value
            require(offset==len(lifted) and min(original_scores)>=0,'all original columns are nonnegative')
            require(target==sum(x*v for x,v in zip(rhs,y)),'exact preservation of the Farkas target')
            checked+=1
            strict+=target<0
            fixed_zero+=any(lo==hi==0 for lo,hi in bounds.values())
            all_fixed+=len(keep)==0
    require(checked>1000 and strict>100 and fixed_zero>100 and all_fixed>100,'nonvacuous boundary controls')
    return {'status':'PASS','optimized_python':not __debug__,'trials':1800,
            'nonnegative_reduced_covectors':checked,'strict_negative_target_controls':strict,
            'fixed_zero_controls':fixed_zero,'all_variables_fixed_controls':all_fixed,
            'helper_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),
            'scope':'Exact arithmetic controls and algebraic audit of elimination/lifting; no ring exclusion follows.'}


if __name__=='__main__':
    result=verify()
    (HERE/f'sparse_terminal_audit_{"normal" if __debug__ else "optimized"}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
