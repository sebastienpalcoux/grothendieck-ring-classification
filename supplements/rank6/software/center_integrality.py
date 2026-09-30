"""General exclusion by complete center profiles and integral rotation counts.

The verifier reconstructs the inherited finite domain and checks the 72
structural obstructions and 99 exact integer-bound/Farkas certificates.
No census identifier is passed to the mathematical verification routine.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys,time
from exact import require
ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'research/exclusions/R6_5_1204'
FILES=('research/round5/m5_1204/profile_certificate.json',
       'research/round5/m5_1204/remaining_profiles.json',
       'research/exclusions/R6_5_1204/forced_W.json',
       'research/exclusions/R6_5_1204/exact_trace_h6.json')

def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def certificate(R):
    return {'kind':'general_center_rotation_integrality','version':1,
            'tensor_sha256':digest(R),
            'proof_files_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES},
            'structural_profiles':72,'trace_profiles':99,'rotation_height':6}

def verify(R,c):
    require(c==certificate(R),'Center-integrality certificate or input tensor mismatch')
    spec=importlib.util.spec_from_file_location('rank6_center_integrality_proof',PROOF/'verify_exclusion.py')
    module=importlib.util.module_from_spec(spec)
    sys.path.insert(0,str(PROOF))
    try:
        spec.loader.exec_module(module)
        report=module.verify_exclusion(R)
    finally:
        sys.path.remove(str(PROOF))
    require(report['passed'] is True,'Incomplete center-integrality verification')
    return report

if __name__=='__main__':
    from argparse import ArgumentParser
    ap=ArgumentParser(description=__doc__);ap.add_argument('--register',action='store_true');args=ap.parse_args()
    row=next(r for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_5_1204')
    c=certificate(row['N']);start=time.monotonic();report=verify(row['N'],c)
    report.update(id=row['id'],kind=c['kind'],optimized_python=not __debug__,seconds=time.monotonic()-start)
    target=ROOT/'verification/current/center_integrality.json';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n')
    if args.register:
        record={'id':row['id'],'m':row['m'],'stage':'continuation_center_integrality',
                'status':'excluded','certificate':c,'exact_checked':True,
                'source':'research/exclusions/R6_5_1204/verify_exclusion.py'}
        (ROOT/'certificates/structural_exclusions.jsonl').write_text(json.dumps(record,separators=(',',':'))+'\n')
    print(json.dumps(report,indent=2))
