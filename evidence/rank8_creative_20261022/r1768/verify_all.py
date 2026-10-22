"""Exact replay of the R1768 saturated prime-sector reduction; no exclusion."""
from pathlib import Path
import argparse,json,sys,hashlib
HERE=Path(__file__).resolve().parent
import verify_arithmetic as arithmetic
import finite_fibres_cone as fibres
import unit_orbit_cone as unit

def run():
 setup=fibres.f.setup(1768)
 result=arithmetic.run(setup)
 fibres.f.require(result==json.loads((HERE/'arithmetic_verification.json').read_text()),'arithmetic receipt changed')
 branches=fibres.run(0,True,setup)
 final=unit.main(True,0,setup)
 return {'id':setup[0]['id'],'tensor_sha256':setup[0]['tensor_sha256'],
 'verification':'PASS','classification_status':'unresolved',
 'scope':'exact necessary restrictions and rational relaxations; no category or exclusion',
 'fibre_indicator_branches':branches['checked'],'exact_infeasible_branches':branches['rejected'],
 'surviving_branch':{'V':4,'U':0,'indicators':[-1,1,1,1,1,1,1]},
 'distinguished_Galois_unit_restriction':[1,0,2,2,2,2,2,2],
 'final_relaxation':final,
 'irrational_ratio_sector_options':result['V4_irrational_ratio_sector_options']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 result=run();path=HERE/'verification.json'
 if a.write:path.write_text(json.dumps(result,indent=2)+'\n')
 else:fibres.f.require(result==json.loads(path.read_text()),'final receipt changed')
 print(json.dumps(result,indent=2),flush=True)
