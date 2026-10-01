"""Exact replay of M9 structure obstructions; no general exclusion is asserted.

A pivotal fusion category with self-dual simples is spherical: pivotal traces
satisfy dim_left(X)=dim_right(X*); equality on simples implies equality on all
endomorphisms by semisimplicity. The wrapper checks the required dual map.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse,hashlib,json,time
from pathlib import Path
from exact import require
from oriented_extension import pseudo_check
from proofs import check_sphere
from rings import dual
ROOT=Path(__file__).resolve().parents[1]
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def verify_record(R,rec):
    require(rec['m']==9 and sha(R)==rec['tensor_sha256'],'structure claim source mismatch')
    c=rec['certificate'];scope=rec['structure']
    if scope=='pseudo_unitary':pseudo_check(R,c)
    elif scope=='spherical':
        require(c['kind']=='spherical','wrong spherical certificate kind')
        check_sphere(R,c,pseudo_check)
    elif scope=='pivotal':
        require(c['kind']=='selfdual_spherical_obstruction' and c['version']==1,'wrong pivotal certificate kind')
        require(c['dual']==dual(R)==list(range(len(R))),'pivotal reduction requires self-dual simples')
        require(c['spherical_certificate']['kind']=='spherical','wrong spherical certificate kind')
        check_sphere(R,c['spherical_certificate'],pseudo_check)
    else:require(False,'unsupported scoped claim')
    return True

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificates',type=Path,default=ROOT/'certificates/m9_structure_only.json')
    ap.add_argument('--output',type=Path,default=ROOT/'verification/m9/structure_replay_optimized.json')
    args=ap.parse_args()
    import scipy.optimize as opt
    def denied(*a,**k):raise RuntimeError('optimizer forbidden in exact structure replay')
    opt.linprog=opt.milp=denied
    rows={r['id']:r for r in json.loads((ROOT/'data/census.json').read_text())}
    records=json.loads(args.certificates.read_text());out=[];seen=set()
    for rec in records:
        require(rec['id'] not in seen,'duplicate scoped claim');seen.add(rec['id'])
        row=rows[rec['id']];require(row['m']==9,'new multiplicity-nine claims only')
        start=time.monotonic();verify_record(row['N'],rec)
        out.append(dict(id=row['id'],m=9,structure=rec['structure'],passed=True,
            certificate_sha256=sha(rec['certificate']),tensor_sha256=sha(row['N']),seconds=time.monotonic()-start))
    result=dict(complete=True,passed=True,optimized_python=not __debug__,optimizer_disabled=True,
        count=len(records),census_sha256=hashlib.sha256((ROOT/'data/census.json').read_bytes()).hexdigest(),
        certificates_sha256=hashlib.sha256(args.certificates.read_bytes()).hexdigest(),results=out,
        scope='The named structure and all stronger structures are excluded. No general categorification nonexistence is asserted.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
