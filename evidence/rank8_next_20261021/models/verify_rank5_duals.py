"""Replay rank-five dual exclusions against all exact tensor coefficients.

The categorical C2-orbit reduction and hypothesis are documented separately.
"""
from pathlib import Path
import hashlib
import json
import sys
import construction_reductions as cr

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank5/software'))
import unified

def run():
    data=json.loads((HERE/'rank5_dual_exclusions.json').read_text())
    cr.need([(r['m'],r['nonselfdual']) for r in data]==[(0,False),(1,False),(2,False),(2,True)],'complete four dual isomorphism types')
    records=[]
    for row in data:
        N=cr.rank5(row['m'],row['nonselfdual'])
        cr.need(row['tensor']==N,'full candidate tensor mismatch')
        cr.validate(N)
        cr.need(row['certificate']['kind']=='signed_extension_positive','unexpected certificate kind')
        unified.verify(N,row['certificate'])
        records.append({'m':row['m'],'nonselfdual':row['nonselfdual'],'tensor_sha256':cr.digest(N),'all_125_coefficients_checked':True,'exact_certificate_verified':True,'criterion':row['certificate']['kind']})
    files={HERE/'construction_reductions.py',HERE/'rank5_dual_exclusions.json',Path(__file__)}
    for module in tuple(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path:
            path=Path(path)
            if path.is_file() and str(path).startswith(str(ROOT/'supplements/rank5/software')):
                files.add(path)
    out={'kind':'complete_tensor_bound_rank5_dual_exclusion_replay','records':records,
         'hypothesis_for_R1154':'trivial pointed C2 associator, so the algebra 1+g exists',
         'consequence':'the untwisted pointed-associator branch of R1154 is excluded by the exact rank5 dual certificates',
         'limitation':'R1154 itself remains unresolved; its nontrivial pointed-associator branch is not covered',
         'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
    (HERE/'rank5_dual_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS all four rank5 Morita-dual isomorphism types excluded by exact tensor-bound certificates. R1154 twisted branch remains open.')

if __name__=='__main__':
    run()
