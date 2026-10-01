#!/usr/bin/env python3
"""Replay every frozen certificate, with optional negative controls."""
import argparse,copy,hashlib,json,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
from common import require,fingerprint
from exclusion8200 import certificate as exclude8200,verify as verify8200
from higher_fields import certificate as higher,verify as verify_higher
BASE=Path(__file__).resolve().parent
EXPECTED_IDS={'R6_9_7018','R6_9_8200','R6_9_8785'}
GENERATORS={'quadratic_gauss_even_codegree_parity_exclusion':exclude8200,
            'inert_quadratic_higher_dimension_field_exclusion':higher}
VERIFIERS={'quadratic_gauss_even_codegree_parity_exclusion':verify8200,
           'inert_quadratic_higher_dimension_field_exclusion':verify_higher}

def replay(negative_controls=False):
    fixtures=json.loads((BASE/'tensors.json').read_text())
    certs=json.loads((BASE/'certificates.json').read_text())
    hashes=json.loads((BASE/'tensor_sha256.json').read_text())
    require(len(fixtures)==3 and {r['id'] for r in fixtures}==EXPECTED_IDS,'incomplete tensor fixtures')
    require(set(certs)==set(hashes)==EXPECTED_IDS,'incomplete certificate or hash inventory')
    report=[]
    for row in fixtures:
        rid=row['id'];R=row['N'];c=certs[rid];tick=time.monotonic()
        require(fingerprint(R)==hashes[rid],'frozen tensor SHA-256 differs')
        require(c['kind'] in VERIFIERS,'unknown certificate kind')
        VERIFIERS[c['kind']](R,c)
        rejected=False
        if negative_controls:
            bad=copy.deepcopy(c)
            if c['kind']=='quadratic_gauss_even_codegree_parity_exclusion':
                bad['strengthened_dimension_trace_multiple']=4010
            else:
                bad['conductor_reduction']['biquadratic_radicands']=[]
            try:VERIFIERS[c['kind']](R,bad)
            except ValueError:rejected=True
            require(rejected,'altered certificate was accepted')
        report.append({'id':rid,'verified':True,'kind':c['kind'],
                       'negative_control_rejected':rejected if negative_controls else None,
                       'seconds':round(time.monotonic()-tick,6)})
    return {'optimized_python':not __debug__,'results':report}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--negative-controls',action='store_true')
    args=ap.parse_args()
    print(json.dumps(replay(args.negative_controls),indent=2))
