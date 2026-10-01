"""Exact, source-bound dispatch for the eleven general M9 completion proofs.

Each proof is replayed once per process in a fresh temporary bundle. This prevents
reuse of an unbound native executable and keeps the published bundles read-only.
The cache never replaces tensor/certificate/source validation.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = 'research/exclusions/m9_completion'
MANIFEST = 'verification/m9/completion/proof_manifest.json'
CASES = {
 'R6_9_529': ('involution_pair', ['involution_pair'], '84f6db29c364e47a967ce6bf7da26bf37239fde9ac6480785e9d639814fa6c65'),
 'R6_9_1060': ('free_involution', ['free_involution'], '3d6747c2494cb99ed76d977a7025d3ef2d399371a2069a67a6ce2964cad7b353'),
 'R6_9_2455': ('involution_pair', ['involution_pair'], '02083204d03d8084f4e82fd397d1c6545936092ffe4074774901eb8201785440'),
 'R6_9_3748': ('relative_center', ['psu25'], '4b6a48b814338c03193a6b8a7916d403d1045ef2ed3db62aaa7890343420d6ca'),
 'R6_9_7018': ('dimension_fields', ['gauss8200','pivotal_gap'], '334eb4f6a9fd8af9c202e65c6900aa3348b17ac1425f826c4f49b12846056d64'),
 'R6_9_7741': ('triangle_saturation', ['triangle'], '02dde73bf8dd7f5247153f391734e56d0540a50cd7e7c04fc37334887010fbd5'),
 'R6_9_7742': ('triangle_saturation', ['triangle'], '1954c96b8d9264aedd4cd183b7396fcd457a8c8c9b619db5d8f236559ee4c649'),
 'R6_9_8099': ('quartic_trace', ['pivotal_gap'], '1695a35fedef9357d39f45630ad83b4eacd2682337b957d0dfbdf33803c2f879'),
 'R6_9_8101': ('quartic_trace', ['pivotal_gap'], '4f0fc9adabbf99f6b4ebe5808c786548671d47a6e4138155ee075e72163fe679'),
 'R6_9_8200': ('gauss_parity', ['gauss8200'], '2bb1330fb68a4ed1adaf6a9e11e6136348e074d5b7bb606ba6fb53899fe16103'),
 'R6_9_8785': ('signed_spectrum', ['gauss8200','case8785'], '7897af45c48cb1d416710f37ea9c4c11226490421317d193c85e3cc5022b3da8'),
}
BUNDLES = sorted({b for _,bs,_ in CASES.values() for b in bs})
_CACHE = {}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def object_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def source_closure(root=ROOT):
    """Bind all local Python imports, including imports inside checker functions."""
    software=Path(root)/'software'
    pending=['check','m9_completion','replay_m9_completion','replay_m9_structure','m9_completion_controls']
    for name in BUNDLES:
        for path in (Path(root)/BASE/name).rglob('*.py'):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node,ast.Import):pending.extend(x.name.split('.')[0] for x in node.names)
                elif isinstance(node,ast.ImportFrom) and node.module:pending.append(node.module.split('.')[0])
    seen=set()
    while pending:
        name=pending.pop();path=software/(name+'.py')
        if name in seen or not path.is_file():continue
        seen.add(name)
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node,ast.Import):pending.extend(x.name.split('.')[0] for x in node.names)
            elif isinstance(node,ast.ImportFrom) and node.module:pending.append(node.module.split('.')[0])
    return sorted('software/'+name+'.py' for name in seen)

def make_manifest(root=ROOT):
    root=Path(root);trees={}
    for name in BUNDLES:
        directory=root/BASE/name
        require(directory.is_dir(),'missing completed proof bundle: '+name)
        files={str(p.relative_to(root)):file_sha(p) for p in sorted(directory.rglob('*'))
               if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
        require(bool(files),'empty proof bundle: '+name)
        trees[name]={'files':files,'sha256':object_sha(files)}
    checkers={name:file_sha(root/name) for name in source_closure(root)}
    return {'schema':'m9-completion-proof-manifest-v1','scope':'general',
            'cases':{rid:{'mechanism':mech,'bundles':bs,'tensor_sha256':sha} for rid,(mech,bs,sha) in CASES.items()},
            'bundles':trees,'checker_files':checkers,'checker_sha256':object_sha(checkers)}

def validate_manifest(root=ROOT):
    root=Path(root);manifest=json.loads((root/MANIFEST).read_text())
    expected_cases={rid:{'mechanism':mech,'bundles':bs,'tensor_sha256':sha} for rid,(mech,bs,sha) in CASES.items()}
    require(manifest.get('schema')=='m9-completion-proof-manifest-v1' and manifest.get('scope')=='general','invalid completion manifest scope')
    require(manifest.get('cases')==expected_cases,'completion proof dependency or tensor inventory changed')
    require(set(manifest.get('bundles',{}))==set(BUNDLES),'completion bundle inventory changed')
    require(set(manifest.get('checker_files',{}))==set(source_closure(root)),'completion checker closure changed')
    require(manifest['checker_sha256']==object_sha(manifest['checker_files']),'completion checker digest invalid')
    files=dict(manifest['checker_files'])
    for name,tree in manifest['bundles'].items():
        require(tree.get('sha256')==object_sha(tree.get('files',{})),'completion proof tree digest invalid: '+name)
        expected={str(p.relative_to(root)) for p in (root/BASE/name).rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
        require(set(tree['files'])==expected,'completion proof tree inventory changed: '+name)
        files.update(tree['files'])
    for name,digest in files.items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe manifest path')
        require(file_sha(root/name)==digest,'completion proof/checker bytes changed: '+name)
    return manifest

def certificate(rid, manifest, root=ROOT):
    mechanism,bundles,digest=CASES[rid]
    return {'kind':'m9_completion_'+mechanism,'scope':'general','tensor_sha256':digest,
            'proof_manifest_sha256':file_sha(Path(root)/MANIFEST),
            'checker_sha256':manifest['checker_sha256'],
            'bundles':{b:manifest['bundles'][b]['sha256'] for b in bundles}}

def validate_certificate(R, cert, root=ROOT):
    manifest=validate_manifest(root);digest=object_sha(R)
    matches=[rid for rid,(_,_,d) in CASES.items() if d==digest]
    require(len(matches)==1,'tensor is not one of the bound completion proof inputs')
    rid=matches[0]
    require(cert==certificate(rid,manifest,root),'completion certificate/proof/tensor binding mismatch')
    return rid,manifest

def commands(name, directory, root):
    if name=='free_involution':return [['verify.py','--source-root',str(root)]]
    if name=='involution_pair':return [['verify.py','--source',str(root)]]
    if name=='pivotal_gap':return [['verify_bundle.py','--source-root',str(root)]]
    if name=='triangle':return [['verify.py','--source-root',str(root)]]
    if name=='gauss8200':return [['verify_bundle.py','--negative-controls']]
    if name=='psu25':return [[script,'--verify'] for script in ['verify_sphericality.py','verify_relative_center.py','verify_center_exclusion.py']]
    if name=='case8785':return [[script] for script in ['verify_8785.py','verify_quadratic_8785.py','verify_signed_8785.py']]
    raise ValueError('unsupported completion bundle')

# All child entry points run with numerical optimizer entry points disabled.
BOOTSTRAP="""import runpy,sys
from pathlib import Path
import scipy.optimize as opt
def denied(*a,**kw): raise RuntimeError('numerical optimizer forbidden in exact completion replay')
opt.linprog=opt.milp=denied
script=Path(sys.argv[1]);sys.argv=sys.argv[1:];sys.path.insert(0,str(script.parent))
runpy.run_path(str(script),run_name='__main__')
"""

def replay_bundle(name, manifest, root=ROOT):
    root=Path(root).resolve()
    key=(str(root),name,manifest['bundles'][name]['sha256'],manifest['checker_sha256'],sys.flags.optimize)
    if key in _CACHE:return _CACHE[key]
    start=time.monotonic();runs=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='m9_completion_'+name+'_') as temporary:
        destination=Path(temporary)/name
        shutil.copytree(root/BASE/name,destination,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for args in commands(name,destination,root):
            command=[sys.executable,*(['-O'] if not __debug__ else []),'-c',BOOTSTRAP,str(destination/args[0]),*args[1:]]
            run=subprocess.run(command,cwd=destination,env=env,capture_output=True,text=True,timeout=840)
            require(run.returncode==0,'completion replay failed '+name+'/'+args[0]+': '+(run.stdout+run.stderr)[-6000:])
            runs.append({'script':args[0],'passed':True,'stdout':run.stdout,'stderr':run.stderr})
    receipt={'bundle':name,'passed':True,'bundle_sha256':manifest['bundles'][name]['sha256'],
             'checker_sha256':manifest['checker_sha256'],'optimized_python':not __debug__,
             'optimizer_disabled':True,'seconds':time.monotonic()-start,'runs':runs}
    _CACHE[key]=receipt
    return receipt

def verify(R, cert):
    rid,manifest=validate_certificate(R,cert)
    for name in CASES[rid][1]:replay_bundle(name,manifest)

def cached_receipts():
    return {r['bundle']:r for r in _CACHE.values()}

def validate_receipt(rows, records, receipt, root=ROOT, optimized=True):
    root=Path(root);manifest=validate_manifest(root)
    require(receipt.get('complete') is True and receipt.get('passed') is True,'completion receipt is incomplete')
    require(receipt.get('optimized_python') is optimized and receipt.get('optimizer_disabled') is True,'completion receipt mode/optimizer mismatch')
    require(receipt.get('census_sha256')==file_sha(root/'data/census.json'),'completion receipt census changed')
    require(receipt.get('certificates_sha256')==file_sha(root/'certificates/m9_completion.jsonl'),'completion certificate file changed')
    require(receipt.get('proof_manifest_sha256')==file_sha(root/MANIFEST) and receipt.get('checker_sha256')==manifest['checker_sha256'],'completion receipt proof/checker binding changed')
    by_id={r['id']:r for r in rows};rec_by={r['id']:r for r in records}
    require(len(rec_by)==len(records)==len(CASES) and set(rec_by)==set(CASES),'completion certificate coverage differs')
    results=receipt.get('results',[]);result_by={r['id']:r for r in results}
    require(len(result_by)==len(results)==receipt.get('count')==len(CASES) and set(result_by)==set(CASES),'completion replay case coverage differs')
    bundle_receipts=receipt.get('bundles',{})
    require(set(bundle_receipts)==set(BUNDLES),'completion replay bundle coverage differs')
    for name,br in bundle_receipts.items():
        require(br.get('bundle')==name and br.get('passed') is True and br.get('bundle_sha256')==manifest['bundles'][name]['sha256']
                and br.get('checker_sha256')==manifest['checker_sha256'] and br.get('optimized_python') is optimized
                and br.get('optimizer_disabled') is True,'completion replay bundle binding mismatch: '+name)
        require([r.get('script') for r in br.get('runs',[])]==[a[0] for a in commands(name,Path(),root)]
                and all(r.get('passed') is True for r in br['runs']),'completion child replay coverage differs: '+name)
    for rid,rec in rec_by.items():
        require(rid in by_id and object_sha(by_id[rid]['N'])==CASES[rid][2],'completion canonical tensor changed')
        require(rec.get('certificate')==certificate(rid,manifest,root),'completion accepted certificate binding changed')
        result=result_by[rid]
        require(result.get('passed') is True and result.get('m')==9 and result.get('tensor_sha256')==CASES[rid][2]
                and result.get('certificate_sha256')==object_sha(rec['certificate']) and result.get('optimized_python') is optimized
                and result.get('optimizer_used') is False and result.get('bundles')==CASES[rid][1],
                'completion per-case replay binding mismatch: '+rid)
    return {'proof_manifest':MANIFEST,'proof_manifest_sha256':file_sha(root/MANIFEST),'checker_sha256':manifest['checker_sha256'],
            'bundles':{name:manifest['bundles'][name]['sha256'] for name in BUNDLES}}
