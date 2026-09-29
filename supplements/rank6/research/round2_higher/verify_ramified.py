"""Check the new complete general certificates, controls and tamper rejection."""
import argparse
import copy
import json
from pathlib import Path
import sys
import time
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'software'))
from exact import require,VerificationError
from new_ramified_signed import arithmetic,certificate,verify
from rings import permute


def run(audit=False):
    by={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
    ids=['R6_7_3812','R6_8_6234','R6_8_6509']
    out={'optimized_python':not __debug__,'verified':[]}
    for rid in ids:
        row=json.load(open(Path(__file__).with_name(rid+'_general.json')))
        start=time.monotonic();verify(by[rid],row['certificate'])
        out['verified'].append({'id':rid,'seconds':round(time.monotonic()-start,3)})
    if audit:
        controls=[r for r in json.load(open(P/'data/decisions.json'))
                  if r['status'] in ('unitarily_realized','spherically_realized_nonpseudounitary')]
        require(len(controls)==54,'positive control list changed')
        require(all(arithmetic(by[r['id']]) is None for r in controls),
                'a positive control unexpectedly satisfies the ramification hypotheses')
        out['positive_controls_preserved']=[r['id'] for r in controls]
        p=[0,5,3,1,4,2];permutations=[]
        for rid in ids:
            R=permute(by[rid],p)
            c=certificate(R);require(c is not None,'permuted general reduction failed');verify(R,c)
            permutations.append({'id':rid,'permutation':p,'verified':True})
        out['tensor_permutations']=permutations
        base=json.load(open(Path(__file__).with_name(ids[0]+'_general.json')))['certificate']
        variants=[]
        c=copy.deepcopy(base);c['arithmetic']['deficit_budget']+=1;variants.append(('trace_budget',c))
        c=copy.deepcopy(base);c['arithmetic']['mod_two_factors'].pop();variants.append(('missing_local_factor',c))
        c=copy.deepcopy(base);c['arithmetic']['mod_two_factors'][-1]['kind']='unramified_field';variants.append(('local_factor_type',c))
        c=copy.deepcopy(base);c['arithmetic']['S_step']=5;variants.append(('dimension_lattice_step',c))
        c=copy.deepcopy(base);c['arithmetic']['rational_formal_codegrees'].remove(15);variants.append(('missing_formal_codegree',c))
        c=copy.deepcopy(base);c['arithmetic']['integrality_matrix'][0][0]='1';variants.append(('integrality_equation',c))
        rejected=[]
        for label,c in variants:
            try:verify(by[ids[0]],c)
            except VerificationError:rejected.append(label)
            else:raise RuntimeError('tampered certificate accepted: '+label)
        out['tampered_certificates_rejected']=rejected
        R=copy.deepcopy(by[ids[0]]);R[1][1][1]+=2
        try:verify(R,base)
        except VerificationError:out['tampered_tensor_rejected']=True
        else:raise RuntimeError('tampered tensor accepted')
    target=Path(__file__).with_name('verification_optimized.json' if not __debug__ else 'verification.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='positive_controls_preserved'}))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--audit',action='store_true');args=ap.parse_args()
    run(args.audit)
