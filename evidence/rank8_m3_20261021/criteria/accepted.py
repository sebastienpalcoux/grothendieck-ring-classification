"""Assemble and independently replay completed general-scope certificates.

Search errors, partial certificates and pseudo-unitary-only certificates are
never accepted. Historical source decisions remain hash bound.
"""
from pathlib import Path
import argparse,concurrent.futures,functools,hashlib,importlib.util,json,os,subprocess,sys
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(BASE/'noncommutative'),str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software')]
from exact import require
SCOPE='general_complex_fusion_category'
STRUCTURAL={
 'solvable_dimension80_rigidity':('models/psl2_11/r275/certificate.json','models/psl2_11/r275/verify_dimension80.py','models/psl2_11/r275/proof.md'),
 'solvable_dimension216_obstruction':('models/psl2_11/r216/certificate.json','models/psl2_11/r216/verify_dimension216.py','models/psl2_11/r216/proof.md'),
 'split_module_dimension280_obstruction':('models/psl2_11/r280/certificate.json','models/psl2_11/r280/verify_split_module.py','models/psl2_11/r280/proof.md'),
 'solvable_dimension90_pointed_base_obstruction':('models/d90_structural.json','models/d90_structural.py','models/D90_STRUCTURAL_PROOF.md'),
}
MODULES={
 'certified_negative_subring_transfer':('criteria/negative_subring.py','verify'),
 'quadratic_casimir_compression':('criteria/quadratic_compression.py','verify'),
 'dimension84_adjoint_rigidity':('pipeline/dimension84_obstruction.py','verify'),
 'rep_a5_module_rank':('publication/r307_module_review.py','verify'),
 'nonsolvable_dimension60_extension':('publication/r2132_morita_extension.py','verify'),
 'rank8_scalar_oriented':('noncommutative/scalar_sieve.py','verify'),
 'rank8_split_module_polynomial':('noncommutative/split_module_polynomial.py','verify'),
 'weak_group_theoretical_primary_three':('noncommutative/weak_group_positivity.py','verify'),
 'weak_group_unitarity_lift':('noncommutative/weak_group_positivity.py','verify'),
 'weighted_induction':('noncommutative/weighted_rank8.py','verify'),
 'global_convex_induction_lift':('criteria/global_induction.py','verify'),
}

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def file_digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read_records(path):
    data=json.loads(path.read_text())
    if isinstance(data,list):return data
    for key in ('records','witnesses','exclusions'):
        if key in data:return data[key]
    if 'id' in data:return [data]
    return []

@functools.lru_cache(None)
def module(relative):
    path=BASE/relative;sys.path.insert(0,str(path.parent));spec=importlib.util.spec_from_file_location('m3_accepted_'+hashlib.sha256(relative.encode()).hexdigest()[:16],path)
    value=importlib.util.module_from_spec(spec);sys.modules[spec.name]=value;spec.loader.exec_module(value);return value

@functools.lru_cache(None)
def structural_replay(kind,sha):
    relative,script,proof=STRUCTURAL[kind];path=BASE/relative
    require(file_digest(path)==sha,'structural certificate source changed')
    result=subprocess.run([sys.executable,str(BASE/script)],cwd=ROOT,text=True,capture_output=True)
    require(result.returncode==0,'structural exact replay failed: '+result.stdout[-2000:]+result.stderr[-2000:])
    return json.loads(path.read_text())

def verify(R,c):
    kind=c['kind']
    if kind in STRUCTURAL:
        data=structural_replay(kind,c['source_certificate_sha256']);witness=c['witness']
        require(witness in data['records'],'structural witness absent from replayed certificate')
        require(witness['tensor_sha256']==digest(R) and witness.get('excluded') is True,'wrong structural source tensor or conclusion');return
    if kind=='one_spectrum':
        import one_spectrum_m3
        return one_spectrum_m3.verify(R,c)
    if kind in ('rank8_general_biquadratic_lift','general_global_convex_induction_lift'):
        # Parameterized field adapters mutate their local base module, so every
        # exact replay is isolated rather than leaking into another field.
        name='general_biquadratic' if kind=='rank8_general_biquadratic_lift' else 'general_global_convex'
        code="import json,sys;sys.path[:0]=json.loads(sys.argv[1]);import "+name+" as m;r,c=json.load(sys.stdin);m.verify(r,c)"
        paths=[str(BASE/'noncommutative'),str(HERE),str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software')]
        result=subprocess.run([sys.executable,'-c',code,json.dumps(paths)],input=json.dumps([R,c]),text=True,capture_output=True,cwd=ROOT)
        require(result.returncode==0,'isolated exact field replay failed: '+result.stdout[-2000:]+result.stderr[-2000:]);return
    if kind in ('rank8_biquadratic_rotation_lift','rank8_biquadratic_lift'):
        if all(R[i][j]==R[j][i] for i in range(8) for j in range(8)):
            import biquadratic_commutative
            return biquadratic_commutative.verify(R,c)
        return module('noncommutative/biquadratic_lift.py').verify(R,c)
    if kind in MODULES:
        path,function=MODULES[kind];return getattr(module(path),function)(R,c)
    import rank8_signed_bridge,advanced_criteria
    rank8_signed_bridge.install();return advanced_criteria.verify(R,c)

def build():
    census={r['id']:r for r in json.loads((BASE/'pipeline/census_m3.json').read_text())};accepted={}
    def add(row,c,path,proof=None):
        rid=row['id'];require(rid in census,'certificate ID absent from census')
        require(row.get('tensor_sha256',census[rid]['tensor_sha256'])==census[rid]['tensor_sha256'],'certificate tensor source mismatch')
        if rid in accepted:return
        accepted[rid]={'id':rid,'tensor_sha256':census[rid]['tensor_sha256'],'scope':SCOPE,'certificate':c,'source_proof_path':str((proof or path).relative_to(ROOT)),'source_certificate_path':str(path.relative_to(ROOT)),'source_certificate_sha256':file_digest(path)}
    for relative in ('criteria/subring_transfer.json','criteria/quadratic_compression.json'):
        path=BASE/relative
        if path.exists():
            for row in read_records(path):add(row,row['certificate'],path)
    for kind,(relative,script,proof) in STRUCTURAL.items():
        path=BASE/relative
        if path.exists():
            for row in read_records(path):
                require(row.get('excluded') is True,'structural row lacks exclusion')
                add(row,{'kind':kind,'source_certificate_sha256':file_digest(path),'witness':row},path,BASE/proof)
    for relative in ('pipeline/dimension84_obstruction.json','publication/r307_module_review.json','publication/r2132_morita_extension.json'):
        path=BASE/relative
        if path.exists():
            for row in read_records(path):add(row,row.get('certificate',row),path)
    sources=[BASE/'pipeline/one_spectrum_m3.json',BASE/'noncommutative/split_module_results.json',BASE/'noncommutative/split_module_polynomial_results.json',BASE/'noncommutative/weak_group_results.json',BASE/'noncommutative/lifted_results.json',BASE/'noncommutative/results.json',BASE/'noncommutative/weighted_results.json',BASE/'noncommutative/biquadratic_lifted_results.json',BASE/'noncommutative/general_biquadratic_results.json']
    sources+=sorted((BASE/'noncommutative').glob('biquadratic_R8_*.json'))
    sources+=sorted((BASE/'noncommutative').glob('general_biquadratic_R8_*.json'))
    sources+=sorted((BASE/'noncommutative').glob('general_global_convex_R8_*.json'))
    sources+=sorted((HERE/'advanced').glob('*/*.json'))
    for path in sources:
        if not path.exists():continue
        for row in read_records(path):
            if row.get('status',row.get('outcome'))=='excluded' and row.get('certificate') is not None:add(row,row['certificate'],path)
    out=sorted(accepted.values(),key=lambda r:int(r['id'].split('_')[-1]));dest=HERE/'accepted_exclusions.json';temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(out,separators=(',',':'))+'\n');temp.replace(dest)
    return out

def verify_record(row):
    census={r['id']:r for r in json.loads((BASE/'pipeline/census_m3.json').read_text())};R=census[row['id']]['tensor']
    require(row['scope']==SCOPE,'not a general certificate');require(digest(R)==row['tensor_sha256'],'source tensor mismatch')
    require(file_digest(ROOT/row['source_certificate_path'])==row['source_certificate_sha256'],'accepted source file changed; rebuild manifest')
    verify(R,row['certificate']);return row['id']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');ap.add_argument('--workers',type=int,default=1);ap.add_argument('--id');args=ap.parse_args()
    if not args.verify:
        rows=build();print('ASSEMBLED',len(rows));return
    rows=json.loads((HERE/'accepted_exclusions.json').read_text())
    if args.id:rows=[r for r in rows if r['id']==args.id];require(len(rows)==1,'requested certificate absent')
    if args.workers>1:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
            for rid in pool.map(verify_record,rows):print('PASS',rid,flush=True)
    else:
        for row in rows:print('PASS',verify_record(row),flush=True)
    print('PASS: all accepted general exclusions',len(rows))
if __name__=='__main__':main()
