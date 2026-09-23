"""Independent controls for source identifications and categorical recipes."""
import copy,itertools,json,time
from pathlib import Path
from unittest.mock import patch
from exact import require,VerificationError
from rings import permute
from prepare import key
from oriented_signed import validate_general
from residual_models import (verify,examples,extended_haagerup,
                             sign_swap_equivariantization,sign_swap_scalar_check)
from relative_fibonacci_models import reconstruct,forced_gram_columns,verify_controls
from positive_models import rank2,tt3
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)

def rejected(fn):
    try:fn()
    except (VerificationError,ValueError,KeyError,IndexError):return True
    raise RuntimeError('corrupted input was accepted')

def run():
    start=time.monotonic();models=verify();controls=verify_controls()
    idx={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
    records=json.load(open(P/'data/residual_positive_models.json'))
    relabel=0
    for rec in records:
        source=rec['N'];expected=key(idx[rec['id']])
        # Every relabelled output is a valid based ring and has the same class.
        for tail in itertools.permutations(range(1,6)):
            R=permute(source,(0,)+tail);validate_general(R)
            require(key(R)==expected,'relabelled model changed isomorphism class');relabel+=1
    source=copy.deepcopy(extended_haagerup());source[4][4][2]-=1
    rejected(lambda:validate_general(source))
    bad=tt3();bad=copy.deepcopy(bad);bad[2][2][2]=2
    rejected(lambda:reconstruct(bad,2))
    rejected(lambda:sign_swap_equivariantization(-1))
    require(forced_gram_columns([[2,0],[0,2]]) is None,'ambiguous/no-pivot Gram promoted to a result')
    # The integral formulas are not an existence theorem for unspecified inputs.
    names={r['name'] for r in records}
    require({n for n in names if n.startswith('Sign-swap')}=={
        'Sign-swap equivariantization from Ising','Sign-swap equivariantization from half-E6'},
        'an unsupplied categorical parameter was registered')
    now={r['id']:r for r in json.load(open(P/'data/decisions.json'))}
    require(all(now[r['id']]['existence']==r['existence'] for r in records),'model existence does not match current ledger')
    sch=now['R6_2_124'];require(sch['existence']['pseudo_unitary']=='no' and sch['existence']['spherical']=='yes','Schopieray status')
    return {'passed':True,'optimized_python':not __debug__,'seconds':time.monotonic()-start,
            'models':models,'relative_center_controls':controls,'relabelled_tensors':relabel,
            'source_and_parameter_mutations_rejected':3,'no_pivot_not_an_exclusion':True}

if __name__=='__main__':
    result=run();name='reconstruction_controls_optimized.json' if not __debug__ else 'reconstruction_controls_normal.json'
    (P/'verification/current').mkdir(parents=True,exist_ok=True)
    (P/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
