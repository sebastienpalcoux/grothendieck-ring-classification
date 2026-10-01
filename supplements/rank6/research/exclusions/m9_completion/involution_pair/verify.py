"""Portable exact verification. Usage: python -O verify.py --source PACKAGE [--id ID].

The source package supplies audited exact categorical primitives, read-only.
Inputs are frozen full tensors bound to hard-coded canonical SHA-256 hashes.
No unresolved-ledger input, numerical optimization, or assert statement is used.
"""
import argparse, hashlib, itertools, json, math, os, subprocess, sys, tempfile, time
from pathlib import Path
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
default_source=next((p for p in BASE.parents if (p/'software/induction.py').exists()),Path.cwd()/'work_m9/Rank6_Categorification_M9')
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source',type=Path,default=default_source)
ap.add_argument('--id',choices=['R6_9_529','R6_9_2455'])
args=ap.parse_args()
SRC=args.source.resolve()
if not (SRC/'software/induction.py').exists():
    raise SystemExit('Use --source to specify the Rank6_Categorification_M9 package.')
sys.path.insert(0,str(SRC/'software'))
sys.path.insert(0,str(BASE))
import scipy.optimize as opt
def denied(*a,**kw):raise RuntimeError('numerical optimizer forbidden in exact replay')
opt.linprog=opt.milp=denied
import sympy as s
import induction as I
from exact import require
import oriented_signed as O
from signed import from_values,gauge_original
EXPECTED={
 'R6_9_529':'84f6db29c364e47a967ce6bf7da26bf37239fde9ac6480785e9d639814fa6c65',
 'R6_9_2455':'02083204d03d8084f4e82fd397d1c6545936092ffe4074774901eb8201785440'}

original_columns=I.restriction_columns
column_counts=[]
def cauchy_columns(ds,beta,K,B):
    candidates=original_columns(ds,beta,K,B)
    n=B.rows;u=s.eye(n)[:,0];M=B-u*u.T
    require(all(M[:j,:j].det()>0 for j in range(1,n+1)),'M not positive definite')
    Mi=M.inv();q=s.ilcm(*(v.q for v in Mi));A=q*Mi
    require(M*A==q*s.eye(n),'incorrect exact inverse')
    total=B[:,0]-u;keep=[]
    for c in candidates:
        cv=s.Matrix(c);wv=total-cv
        G=s.Matrix([[q-(cv.T*A*cv)[0],-(cv.T*A*wv)[0]],
                    [-(wv.T*A*cv)[0],(n-2)*q-(wv.T*A*wv)[0]]])
        if G[0,0]>=0 and G[1,1]>=0 and G.det()>=0:keep.append(c)
    column_counts.append([len(candidates),len(keep)])
    return keep
def cartesian_frames(sets,B,gram_prune=False):
    n=B.rows;u=(1,)+(0,)*(n-1);total=tuple(int(B[0,j])-u[j] for j in range(n));out=[]
    for cols in itertools.product(*sets):
        if any(sum(c[j] for c in cols)!=total[j] for j in range(n)):continue
        if any(sets[i]==sets[j] and cols[i]>cols[j] for i in range(n-1) for j in range(i+1,n-1)):continue
        out.append((u,)+cols)
    return sorted(out)
I.restriction_columns=cauchy_columns
I.low_matrices=cartesian_frames
import higher_traces as H
import character_induction as C
import proofs as P

def quartic_check():
    t=s.Symbol('t');counts=[0,0];total=0
    def sign(z):return (1 if z>0 else 0)-(1 if z<0 else 0)
    def changes(v):
        v=[z for z in v if z]
        return sum(a!=b for a,b in zip(v,v[1:]))
    for a in (1,2):
        for c in range(1,257*a**3//64+1):
            if 257**2*a**4%c:continue
            for b in range(1,3*257*a*a//8+1):
                if b**4%(c*c):continue
                total+=1;n=257**2*c
                p=t**4-257*a*t**3+257*b*t*t-4*n*t+n
                seq=s.sturm(p,t)
                roots=changes([sign(z.subs(t,0)) for z in seq])-changes([sign(s.Poly(z,t).LC()) for z in seq])
                if roots!=4:counts[0]+=1;continue
                disc=int(s.resultant(p,s.diff(p,t),t))
                require(disc>0,'positive-root discriminant')
                require(math.isqrt(disc)**2!=disc,'biquadratic survivor')
                require(disc%257!=0 or math.isqrt(disc//257)**2!=disc//257,'cyclic quartic survivor')
                counts[1]+=1
    require(total==1057 and counts==[736,321],'quartic completeness counts')
    # Independent residue check of the corrected quadratic trace-parity argument.
    residues=set()
    for x,a,b in itertools.product(range(1,16,2),range(8),range(8)):
        delta=2+2*x*x+4*(a*a+b*b)
        if delta%8==0:residues.add(delta%16)
    require(residues=={8},'quadratic local parity lemma failed')
    return {'quartic_candidates':total,'quartic_rejections':counts,'quadratic_delta_mod16':list(residues)}

def saturation_check(R,rid):
    p=O.problem(R,normalized=False);src=p['source'];du=O.dual(R)
    g=next(i for i in range(1,6) if R[i][i]==[1,0,0,0,0,0] and all(sum(z)==1 for z in R[i]))
    for v,dom in enumerate(p['domains']):
        bound=max(dom)
        if bound==1:require(all(g in tri for tri in p['active'][v]),'bound-one orbit outside g action')
        vals=[1] if bound==1 else [-bound,bound]
        old='for(int x:vector<int>{'+','.join(map(str,dom))+'}){v['+str(v)+']=x;'
        new='for(int x:vector<int>{'+','.join(map(str,vals))+'}){v['+str(v)+']=x;'
        require(old in src,'endpoint domain substitution absent')
        src=src.replace(old,new)
    with tempfile.TemporaryDirectory(dir=BASE) as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(src)
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=120)
    vals=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines())
    frozen=next(z for z in json.loads((BASE/'saturated_signs.json').read_text()) if z['id']==rid)
    require(vals==sorted(tuple(z['values']) for z in frozen['branches']),'saturated solution domain changed')
    require(len(vals)==8,'wrong saturated solution count')
    for v in vals:
        T=from_values(R,p,v);O.validate_general(T)
        require(gauge_original(T,R) is not None,'nongauge saturated quotient')
    return {'saturated_solutions':8,'all_original_gauges':True,'native_statistics':run.stderr.strip()}

def verify_row(row):
    rid=row['id'];R=row['N'];start=time.time()
    sha=hashlib.sha256(json.dumps(R,separators=(',',':'),sort_keys=True).encode()).hexdigest()
    require(sha==EXPECTED[rid],'frozen tensor digest mismatch')
    O.validate_general(R,nonnegative=True)
    require(set(O.flat(R))=={0,1,7,8,9},'unexpected multiplicity support')
    a=I.Characters(R);require(s.trace(a.C)==4136,'Casimir trace changed')
    t=I.t
    require(I.codegree_poly(R)==s.Poly((t-4)**2*(t-8)**2*(t*t-4112*t+16448),t),'formal codegrees changed')
    column_counts.clear()
    data=H.quadratic_data(R);counts=list(column_counts)
    require(counts==[[817,10],[833,9],[833,9],[217,10],[217,10]],'column domain counts')
    require(len(data['lows'])==497,'low frame count')
    cert=json.loads((BASE/(rid+'_pseudo.json')).read_text())
    tab=C.CharacterTable(R,data);require(tab.metadata()==cert['table'],'character table metadata')
    eps=list(itertools.product(*[[-1,1] if a.du[i]==i else [0] for i in range(1,6)]))
    require(list(map(list,eps))==cert['indicator_choices'],'not every FS2 choice included')
    surviving=[]
    for cols in data['lows']:
        why=I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why is None:surviving.append(cols)
    require(len(surviving)==91 and len(cert['branches'])==91,'incomplete surviving frame domain')
    rays=0;labelled=0
    for ix,(cols,branch) in enumerate(zip(surviving,cert['branches'])):
        require(list(map(list,cols))==branch['cols'],'frame ordering mismatch')
        labs=tab.assignments(cols)
        require(list(map(list,labs))==branch['labellings'],'incomplete character assignments')
        if not labs:continue
        labelled+=1
        require([z['ep'] for z in branch['cases']]==list(map(list,eps)),'incomplete FS2 branch domain')
        L=s.Matrix.hstack(*map(s.Matrix,cols))
        for ep,rec in zip(eps,branch['cases']):
            A,b,meta=H.build_system(R,data,L,ep,height=6)
            require(rec['y'] is not None,'missing ray')
            H.check_farkas(A,b,rec['y']);rays+=1
        print(rid,'exact frame',ix,'rays',rays,flush=True)
    require((labelled,rays)==((6,48) if rid=='R6_9_529' else (31,992)),'wrong unrestricted FS2 counts')
    verified_token={'kind':'verified_all_FS2_cauchy_induction','tensor_sha256':sha}
    sphere=P.sphere_certificate(R,lambda _:verified_token)
    require(sphere is not None,'spherical character domain incomplete')
    P.check_sphere(R,sphere,lambda rr,c:require(rr==R and c==verified_token,'wrong checked PU token'))
    sat=saturation_check(R,rid)
    return {'id':rid,'tensor_sha256':sha,'general_excluded':True,'optimizer_disabled':True,
            'optimized_python':not __debug__,'column_counts':counts,'low_frames':497,
            'ordinary_failures':406,'character_labelled_frames':labelled,'all_FS2_rays':rays,
            'spherical_character_components':len(sphere['characters']),**sat,'seconds':time.time()-start}

arithmetic=quartic_check()
rows=json.loads((BASE/'tensors.json').read_text())
require({r['id'] for r in rows}==set(EXPECTED),'frozen fixture incomplete')
reports=[verify_row(r) for r in rows if args.id is None or r['id']==args.id]
print(json.dumps({'arithmetic':arithmetic,'reports':reports},indent=2),flush=True)
