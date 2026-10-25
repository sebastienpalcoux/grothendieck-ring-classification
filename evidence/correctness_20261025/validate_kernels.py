"""Fresh, isolated controls for the corrected active native kernels."""
from pathlib import Path
import hashlib, importlib.util, itertools, json, math, random, re, subprocess, sys, time
import sympy as s
import argparse,tempfile,shutil
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True);ARGS=parser.parse_args()
OUT=ARGS.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=False)
TEMP=tempfile.TemporaryDirectory(prefix='corrected-kernel-controls-');TREE=Path(TEMP.name)
ROOT_FILES = [
    'supplements/rank6/software/gram_vectors_general.cpp',
    'supplements/rank6/software/round5_1204.cpp',
    'supplements/rank6/research/exclusions/m9_completion/free_involution/gram_vectors_general.cpp',
    'supplements/rank6/research/exclusions/m9_completion/involution_pair/gram_vectors_general.cpp',
    'evidence/correctness_20261025/source_overrides/supplements/rank8/experimental_signed/gram_vectors_general.cpp',
    'evidence/correctness_20261025/source_overrides/evidence/rank7_m5_20261020/computation/gram_vectors_fast.cpp',
]
FRAME_FILES = [f'supplements/rank{r}/{folder}/gram_frames.cpp'
               for r, folder in [(6, 'software'), (7, 'software'), (8, 'experimental_signed')]]
FRAME_FILES=[('evidence/correctness_20261025/source_overrides/'+p) if p.startswith('supplements/rank8/') else p for p in FRAME_FILES]
GUARD_FILE = 'supplements/rank6/software/check.py'

for rel in ROOT_FILES+FRAME_FILES+[GUARD_FILE]:
    p=TREE/'corrected'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(REPO/rel,p)
for rel in [ROOT_FILES[1],FRAME_FILES[0]]:
    p=TREE/'original'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/'kernel_inputs/original'/rel,p)
CURRENT={rel:hashlib.sha256((REPO/rel).read_bytes()).hexdigest() for rel in ROOT_FILES+FRAME_FILES+[GUARD_FILE]}


START=time.monotonic()
BIN=TREE/'validation-build';BIN.mkdir(exist_ok=True)
RNG=random.Random(20261025)
RECEIPT={'applied':True,'optimized_python':not __debug__,'seed':20261025,'checks':{}}

def require(ok, message):
    if not ok:raise RuntimeError(message)

def compile_cpp(source, name, sanitize=False):
    exe=BIN/name
    flags=['-O1','-fsanitize=undefined','-fno-sanitize-recover=undefined'] if sanitize else ['-O2']
    subprocess.run(['g++','-std=c++17',*flags,str(source),'-o',str(exe)],capture_output=True,check=True,timeout=60)
    return exe

def run(exe, values, success=True):
    proc=subprocess.run([str(exe)],input=' '.join(map(str,values)),text=True,capture_output=True,timeout=20)
    if success:require(proc.returncode==0, str(exe)+': '+proc.stderr)
    return proc

def rows(proc):return sorted(tuple(map(int,line.split())) for line in proc.stdout.splitlines())

def psd(H):
    return all(H.extract(ix,ix).det()>=0 for k in range(1,H.rows+1) for ix in itertools.combinations(range(H.rows),k))

def generic_input(G):
    n=G.rows;r=G.rank()
    ix=next(ix for ix in itertools.combinations(range(n),r) if G.extract(ix,ix).det())
    S=G.extract(ix,ix);adj=S.adjugate();det=int(S.det());M=G.extract(range(n),ix)*adj
    return [n,r]+list(map(int,G))+list(ix)+list(map(int,adj))+[det]+list(map(int,M))

def frame_input(A,b):return [len(b),len(A),10]+list(b)+[x for col in A for x in col]

def completed_frames(proc):
    require(bool(re.fullmatch(r'complete 1 nodes \d+ frames \d+\s*',proc.stderr)), 'frame completion missing: '+proc.stderr)
    return rows(proc)

def main():
    # Compile every proposed C++ file independently, without stale cached binaries.
    native={rel:compile_cpp(TREE/'corrected'/rel,'corrected-'+str(i)) for i,rel in enumerate(ROOT_FILES+FRAME_FILES)}
    RECEIPT['checks']['fresh_cpp_compilations']=len(native)

    # Expose the actual root function by renaming main; do not enumerate huge boxes.
    # This source includes the proposed file rather than reimplementing its function.
    probe=BIN/'root-probe.cpp'
    probe.write_text('#define main enumerator_main\n#include "'+str(TREE/'corrected'/ROOT_FILES[0])+'"\n#undef main\nint main(){I a;while(std::cin>>a)std::cout<<root(a)<<"\\n";}\n')
    rootexe=compile_cpp(probe,'root-probe',sanitize=True)
    max64=2**63-1
    values=set(range(2917))|{max64,max64-1,2**60-1}
    for b in [0,1,2,46340,999999999,1000000000,1000000001,1073741823,1073741824,3037000499]:
        values.update(a for a in (b*b-1,b*b,b*b+1) if 0<=a<=max64)
    for k in range(63):values.update(a for a in (2**k-1,2**k,2**k+1) if a<=max64)
    values.update(RNG.randrange(max64+1) for _ in range(2048));values=sorted(values)
    got=list(map(int,run(rootexe,values).stdout.split()))
    require(got==[math.isqrt(a) for a in values],'integer square root mismatch')
    roots=[]
    for rel in ROOT_FILES:
        source=(TREE/'corrected'/rel).read_text()
        roots.append(next(line for line in source.splitlines() if line.startswith('I root(')))
    require(len(set(roots))==1,'copied root fixes disagree')
    RECEIPT['checks']['root_exact_controls']={'inputs':len(values),'maximum':max64,'all_six_function_bodies_identical':True,'undefined_behavior_sanitizer':True,'method':'included corrected root(), compared with Python math.isqrt'}

    # Forced joint coordinate: one native leaf suffices to reproduce/fix the defect.
    jointrel='supplements/rank6/software/round5_1204.cpp'
    oldjoint=compile_cpp(TREE/'original'/jointrel,'original-joint')
    boundary=1000000001;G=boundary*boundary
    inp=[1,1,G,0,G,1,G,boundary]
    require(rows(run(oldjoint,inp))==[],'old boundary counterexample did not reproduce')
    require(rows(run(native[jointrel],inp))==[(boundary,)],'fixed joint boundary omitted')
    RECEIPT['checks']['forced_joint_boundary']={'Q':G,'fixed_v':boundary,'old_output':[],'corrected_output':[[boundary]],'enumerated_leaves':1}

    # Independent current-size Gram controls, including singular matrices.
    gramcases=[]
    for n in range(1,6):
        for k in (1,n):
            for trial in range(2):
                X=s.Matrix(n,k,[RNG.randrange(3) for _ in range(n*k)]);G=X*X.T
                if not G.rank():continue
                expected=[]
                for v in itertools.product(*(range(math.isqrt(int(G[i,i]))+1) for i in range(n))):
                    if not any(v):continue
                    H=G-s.Matrix(v)*s.Matrix([v])
                    if all(x>=0 for x in H) and psd(H):expected.append(v)
                expected.sort();inp=generic_input(G)
                for rel in ROOT_FILES:
                    if rel==jointrel:continue
                    require(rows(run(native[rel],inp))==expected,'generic Gram regression '+rel)
                gramcases.append({'size':n,'rank':G.rank(),'vectors':len(expected)})
    RECEIPT['checks']['generic_gram_regressions']={'matrices':len(gramcases),'kernels':5,'comparisons':5*len(gramcases),'method':'all coordinate vectors plus all principal minors','cases':gramcases}

    # Joint-prefix kernel controls use the existing serializer, exact full inverse
    # as independent oracle, and newly compiled corrected source as backend.
    sys.path.insert(0,str(REPO/'supplements/rank6/software'))
    from round5_1204 import prepare
    for case in range(18):
        n=5+case%3
        X=s.eye(n).row_join(s.Matrix([[RNG.randrange(2) for _ in range(2)] for _ in range(n)]));G=X*X.T
        dim,rank,ix,vals=prepare(G);fixed=list(X[:5,case%(n+2)])
        nativefixed=[fixed[i] if i<5 else -1 for i in ix]
        got=rows(run(native[jointrel],[dim,rank]+vals+nativefixed));expected=[];inv=G.inv()
        for tail in itertools.product(*(range(math.isqrt(int(G[i,i]))+1) for i in range(5,n))):
            v=fixed+list(tail);vec=s.Matrix(v)
            if (vec.T*inv*vec)[0]<=1 and all(v[i]*v[j]<=G[i,j] for i in range(n) for j in range(n)):expected.append(tuple(v))
        require(got==sorted(expected),'joint small-domain regression')
    RECEIPT['checks']['joint_current_size_regressions']=18

    # The frame sentinel counterexamples are forced single-variable equations;
    # even the signed-int maximum requires only two search nodes.
    frame_boundaries=[0,1,2916,999999,1000000,1000001,2**31-1]
    oldframe=compile_cpp(TREE/'original'/FRAME_FILES[0],'original-frame')
    require(completed_frames(run(oldframe,frame_input([[1]],[1000000])))==[],'old frame sentinel defect did not reproduce')
    for rel in FRAME_FILES:
        for b in frame_boundaries:
            p=run(native[rel],frame_input([[1]],[b]))
            require(completed_frames(p)==[(b,)],'forced frame boundary '+rel)
            require('nodes 2 ' in p.stderr,'forced frame unexpectedly enumerates')
        # Unsupported zero columns and integer-overflow inputs must fail closed.
        for inp in [frame_input([[0]],[0]),frame_input([[1]],[-1]),frame_input([[1]],[2**31]),frame_input([[1000001]],[1]),[1,1,10,1]]:
            p=run(native[rel],inp,success=False)
            require(p.returncode!=0 and not p.stdout,'invalid frame input did not fail closed')
    # Endpoint regression under UBSan catches overflow in ++m at INT_MAX.
    sanitizedframe=compile_cpp(TREE/'corrected'/FRAME_FILES[0],'sanitized-frame',sanitize=True)
    require(completed_frames(run(sanitizedframe,frame_input([[1]],[2**31-1])))==[(2**31-1,)],'sanitized int endpoint')
    RECEIPT['checks']['forced_frame_boundaries']={'rhs_values':frame_boundaries,'kernels':3,'comparisons':3*len(frame_boundaries),'nodes_per_case':2,'old_1000000_output':[],'invalid_inputs_rejected':15,'endpoint_undefined_behavior_sanitizer':True}

    # Complete independent Ax=b controls use all coordinate count combinations.
    for case in range(50):
        n=1+case%3;k=1+(case//3)%4
        A=[]
        for j in range(k):
            col=[RNG.randrange(3) for _ in range(n)]
            if not any(col):col[j%n]=1
            A.append(col)
        b=[RNG.randrange(7) for _ in range(n)]
        bounds=[min(b[i]//a for i,a in enumerate(col) if a) for col in A]
        expected=sorted(x for x in itertools.product(*(range(v+1) for v in bounds)) if all(sum(A[j][i]*x[j] for j in range(k))==b[i] for i in range(n)))
        for rel in FRAME_FILES:
            require(completed_frames(run(native[rel],frame_input(A,b)))==expected,'small frame exhaustive comparison')
    # Empty finite set has exactly the zero frame iff RHS vanishes.
    for rel in FRAME_FILES:
        require(completed_frames(run(native[rel],frame_input([], [0])))==[()], 'empty zero frame')
        require(completed_frames(run(native[rel],frame_input([], [1])))==[], 'empty infeasible frame')
    RECEIPT['checks']['small_frame_regressions']={'systems':50,'kernels':3,'comparisons':150,'empty_column_set_controls':6}

    # Exercise the actual proposed dispatch, with inherited imports from checkout.
    # All checks remain active under Python -O.
    spec=importlib.util.spec_from_file_location('audit_proposed_check',TREE/'corrected'/GUARD_FILE)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    census=json.loads((REPO/'supplements/rank6/data/census.json').read_text());by={r['id']:r['N'] for r in census}
    ledger=json.loads((REPO/'supplements/rank6/data/decisions.json').read_text())
    noncomm=next(r for r in census if any(r['N'][i][j]!=r['N'][j][i] for i in range(6) for j in range(6)))
    try:module.verify(noncomm['N'],{'kind':'cyclotomic'})
    except module.VerificationError as exc:
        require(str(exc)=='cyclotomic criterion requires commutative input','wrong guard rejection')
    else:raise RuntimeError('noncommutative tensor accepted')
    ids=[]
    for rec in ledger:
        if rec.get('certificate',{}).get('kind')=='cyclotomic':
            module.verify(by[rec['id']],rec['certificate']);ids.append(rec['id'])
    require(len(ids)==16,'unexpected allocated cyclotomic count')
    RECEIPT['checks']['cyclotomic_dispatch']={'noncommutative_input_rejected':noncomm['id'],'existing_certificates_passed':ids,'count':len(ids)}

    require(all(hashlib.sha256((REPO/rel).read_bytes()).hexdigest()==h for rel,h in CURRENT.items()),'active kernel source changed during validation')
    RECEIPT.update(passed=True,status='PASS',seconds=time.monotonic()-START,current_sources_unchanged=True,source_sha256=CURRENT,
        scope='Targeted exact current-kernel regressions, including independent complete small domains and supported-domain boundary checks; not another full census classification replay.')
    (OUT/'receipt.json').write_text(json.dumps(RECEIPT,indent=2)+'\n')
    print(json.dumps({k:v for k,v in RECEIPT.items() if k!='checks'},indent=2))
    print(json.dumps({k:v if not isinstance(v,dict) else {a:b for a,b in v.items() if a not in ['cases','existing_certificates_passed','rhs_values']} for k,v in RECEIPT['checks'].items()},indent=2))

if __name__=='__main__':main()
