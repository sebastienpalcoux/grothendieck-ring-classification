"""Replay the multiplicity-five continuation without changing historical bands.

--metadata-only checks source, identifier, status, and recorded-file bindings;
it does not replay mathematical certificates. Full replay independently checks
all new exclusions and the positive model, and preserves the earlier ledger.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import argparse,collections,concurrent.futures,gzip,hashlib,importlib.util,itertools,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'output/m5'
sys.path.insert(0,str(P));sys.path.insert(0,str(P/'software'))
OLD_SHA='00edf884caa59384a1f7b9a91d7273539306443035db5144c02f9bda5bda3d2b'
INPUT_SHA='9018f6f195339fb153ea326ec308c955bb1adf9afe1ffc9423be1bef6818e073'
def require(v,m):
    if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load_module(name,relative):
    path=ROOT/relative
    if str(path.parent) not in sys.path:sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def verify_new(record):
    # Independent replay may rebuild finite domains, never invoke an optimizer.
    def forbidden(*args,**kwargs):raise RuntimeError('numerical optimization forbidden during exact certificate replay')
    try:
        import scipy.optimize
    except ModuleNotFoundError as exc:
        if exc.name not in ('scipy','scipy.optimize'):raise
    else:
        scipy.optimize.linprog=scipy.optimize.milp=forbidden
    from analyze import verify_own
    c=record['certificate'];R=record['tensor'];kind=c['kind']
    if kind=='noncyclic_maximal_near_group':
        load_module('maximal_near_group','evidence/rank7_m5_20261019/models/maximal_near_group.py').verify(R,c)
    elif kind=='certified_rank6_subring':
        load_module('rank6_subring_descent','evidence/rank7_m5_20261019/theory/rank6_subring_descent.py').verify(R,c)
    elif kind=='integral_formal_codegree':
        load_module('integral_codegrees','evidence/rank7_m5_20261019/models/integral_codegrees.py').verify(R,c)
    elif kind=='cyclic_stabilizer_divisibility':
        load_module('cyclic_divisibility','evidence/rank7_m5_20261019/review/cyclic_divisibility.py').verify(R,c)
    elif kind=='cyclic_isotypic_integrality':
        load_module('cyclic_isotypic','evidence/rank7_m5_20261019/review/cyclic_isotypic.py').verify(R,c)
    elif kind=='cyclic3_spectral_module':
        load_module('cyclic3_spectral','evidence/rank7_m5_20261019/theory/cyclic3_spectral.py').verify(R,c)
    elif kind=='spectral_involution_module':
        import new_module_spectral
        new_module_spectral.verify(R,c)
    else:verify_own(R,c)
    return record['id']
def verify_model(record):
    m=load_module('frobenius42','evidence/rank7_m5_20261019/models/verify_frobenius42.py')
    receipt=json.loads((ROOT/'evidence/rank7_m5_20261019/models/frobenius42_match.json').read_text())
    T=m.exact_character_tensor();p=receipt['match']['basis_permutation_model_to_census'];R=record['tensor']
    require(record['id']==receipt['match']['id']=='R7_5_5678','wrong model identifier')
    require(sorted(p)==list(range(7)) and p[0]==0,'invalid model permutation')
    require(all(T[i][j][k]==R[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(7),repeat=3)),'positive tensor transport failed')
    require(record['existence']=={k:'yes' for k in ('general','pivotal','spherical','pseudo_unitary','unitary')},'positive existence claims')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--metadata-only',action='store_true');ap.add_argument('--jobs',type=int,default=4);ap.add_argument('--output',type=Path);args=ap.parse_args();start=time.monotonic()
    oldpath=P/'output/rank7_ledger_through_m4.json';require(sha(oldpath)==OLD_SHA,'historical ledger checksum')
    old=json.loads(oldpath.read_text());ledger_digest=sha(P/'output/rank7_ledger.json');allrows=json.loads((P/'output/rank7_ledger.json').read_text());new=[r for r in allrows if r['multiplicity']==5]
    require([r for r in allrows if r['multiplicity']<=4]==old,'historical records changed')
    require(len(allrows)==10006 and len(new)==5805,'ledger cardinality')
    catalogue=json.loads((P/'data/model_catalog.json').read_text())
    require((P/'data/model_catalog.json').read_bytes()==(P/'output/rank7_model_catalog.json').read_bytes(),'catalogue aliases differ')
    require({r['id'] for r in catalogue}=={r['id'] for r in allrows if r['status']=='unitarily_realized'},'model catalogue omits a realized ring or includes an unverified ring')
    census=json.loads((OUT/'census.json').read_text());require(len(census)==5805,'new source census cardinality')
    require([r['id'] for r in new]==[f'R7_5_{i}' for i in range(1,5806)],'new identifier order')
    source=P/'provenance/rank7_M5_verified/FusionRingMultiplicationTables.txt.gz';require(sha(source)==INPUT_SHA,'new source checksum')
    raw=[json.loads(s.replace('{','[').replace('}',']')) for s in gzip.open(source,'rt') if s.strip()]
    flat=lambda R:tuple(v for A in R for row in A for v in row)
    rawnew=[(line,R) for line,R in enumerate(raw,1) if max(flat(R))==5]
    require(collections.Counter(max(flat(R)) for R in raw)=={1:43,2:319,3:1059,4:2780,5:5805},'input band counts')
    require(collections.Counter(flat(R) for R in raw)==collections.Counter(flat(r['tensor']) for r in allrows),'full source coverage')
    for i,(source_row,record,(line,R)) in enumerate(zip(census,new,rawnew),4202):
        require(record['tensor']==source_row['tensor']==R and record['id']==source_row['id'],'new record binding')
        require(record['source_line']==i and record['input_source_line']==line,'source transport binding')
        require(record['status'] in ('excluded','unitarily_realized','unresolved'),'invalid status')
        if record['status']=='excluded':require(isinstance(record['certificate'],dict) and record['criterion'] and not record['model_names'],'invalid exclusion record')
        elif record['status']=='unresolved':require(record['certificate'] is None and record['criterion'] is None and not record['model_names'],'unsupported unresolved record')
        else:require(record['certificate'] is None and record['model_names'],'invalid model record')
    summary=json.loads((P/'output/rank7_summary.json').read_text());counts=dict(collections.Counter(r['status'] for r in new))
    require(summary['max_multiplicity']==5 and summary['ring_counts']['5']==5805 and summary['status_counts']['5']==counts,'summary does not match ledger')
    canonical=P/'data/rank7_tables.txt.gz'
    require(sha(canonical)==summary['source_sha256'],'canonical source checksum')
    canonical_rows=[json.loads(s.replace('{','[').replace('}',']')) for s in gzip.open(canonical,'rt') if s.strip()]
    require(canonical_rows==[r['tensor'] for r in allrows],'canonical source order differs from ledger')
    commitment=OUT/'commitments.json'
    if commitment.exists():
        for relative,digest in json.loads(commitment.read_text()).items():require(sha(ROOT/relative)==digest,'changed committed input '+relative)
    if not args.metadata_only:
        targets=[r for r in new if r['status']=='excluded']
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
            checked=list(pool.map(verify_new,targets,chunksize=8))
        require(len(set(checked))==len(targets),'incomplete exact replay')
        for record in new:
            if record['status']=='unitarily_realized':verify_model(record)
    require(sha(P/'output/rank7_ledger.json')==ledger_digest,'ledger changed during replay')
    report={'status':'PASS','mode':'metadata_only' if args.metadata_only else 'full_exact_replay','optimized_python':not __debug__,'new_band':5,'new_rings':5805,'new_status_counts':counts,'old_records_preserved':4201,'total_rings':10006,'input_sha256':INPUT_SHA,'ledger_sha256':sha(P/'output/rank7_ledger.json'),'new_exclusions_replayed':0 if args.metadata_only else counts.get('excluded',0),'old_certificates_replayed':0,'scope':'New-band proof certificates and positive character tensor replayed; old records preserved, with historical proof replays separately archived.' if not args.metadata_only else 'Source coverage, identifiers, statuses, and file bindings only; no mathematical certificate replay.','seconds':time.monotonic()-start}
    target=args.output or OUT/('metadata.json' if args.metadata_only else 'replay_optimized.json' if not __debug__ else 'replay_normal.json');target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
