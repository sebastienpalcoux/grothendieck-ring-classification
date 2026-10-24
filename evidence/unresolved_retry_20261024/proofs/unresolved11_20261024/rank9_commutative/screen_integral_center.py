"""Necessary center screen with the new integral-center theorem.

Numerical discovery only: status changes require an exact separating ray and
an independent audit of the reconstructed system. No numerical pass is a model.
"""
import inspect,json,sys,time,math,hashlib
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
sys.path.insert(0,str(WORK/'rank9_m2_research/phase3/quadratic_s_symmetry'))
import quadratic_s_symmetry as qs
qc=qs.qc

rid=sys.argv[1]
height=int(sys.argv[2]) if len(sys.argv)>2 else 3
limit=int(sys.argv[3]) if len(sys.argv)>3 else 180
tau=int(sys.argv[4]) if len(sys.argv)>4 else None
verify='--verify' in sys.argv
start=time.monotonic()
profile=json.loads((HERE.parent/'inputs'/f'{rid}.json').read_text())
R=profile['fusion_tensor'];data=qc.base(R)
g={'R9_2_137':1,'R9_2_1607':5,'R9_2_1976':8}[rid]
oldcols=data['cols']
data['cols']=[(v,z) for v,z in oldcols if z[1] or (z[0]==1 and not v[g])]
fermions={v for v,z in data['cols'] if z==(1,0) and not v[0]}
# Expose the labelled variable keys already constructed by the existing builder.
# Duality is disabled, so keys and variable columns remain in one-to-one order.
source=inspect.getsource(qs.build).replace('return AA,bb,meta','return AA,bb,meta,keys')
namespace=dict(vars(qs));exec(source,namespace)
oldbase=qc.base;qc.base=lambda _:data
try:A,b,meta,keys=namespace['build'](R,height,False)
finally:qc.base=oldbase
types,bound=qc.trace_types(data['q'],data['primes'],height)
fermiontrace=tuple(((-1)**k,0) for k in range(1,height+1))
keep=[j for j,(kind,v,ti) in enumerate(keys)
      if kind!='high' or v not in fermions or tuple(types[ti])==fermiontrace]
if tau is not None:
    if height!=4 or tau not in [-1,1]:raise ValueError('TY screen requires height4 and tau sign')
    Y={'R9_2_137':8,'R9_2_1607':3,'R9_2_1976':5}[rid]
    eigths=[((0,Q(1,2)),(0,0),(0,Q(-1,2)),(-1,0)),
            ((0,Q(-1,2)),(0,0),(0,Q(1,2)),(-1,0))]
    allowed=eigths+([((1,0),(1,0),(1,0),(1,0)),
                    ((-1,0),(1,0),(-1,0),(1,0))] if tau==1 else
                   [((0,0),(-1,0),(0,0),(1,0))])
    keep=[j for j in keep if keys[j][0]!='high' or not keys[j][1][Y] or tuple(types[keys[j][2]]) in allowed]
A=[[row[j] for j in keep] for row in A];keys=[keys[j] for j in keep]
# At most one nonunit central invertible: its image must be one anisotropic h.
limitrow=[int(kind=='high' and v in fermions) for kind,v,ti in keys]
for row in A:row.append(0)
A.append(limitrow+[1]);b.append(1)
if tau is not None:
    col_dims={v:z for v,z in data['cols']}
    for k,value in [(2,tau),(4,0)]:
        values=[qc.scale(qc.mul(col_dims[v],types[ti][k-1],data['q']),v[Y])
                if kind=='high' and v[Y] else (Q(0),Q(0)) for kind,v,ti in keys]+[(Q(0),Q(0))]
        rhs=qc.scale(data['D'],value)
        for c in range(2):
            row=[z[c] for z in values];den=math.lcm(*(Q(z).denominator for z in row+[rhs[c]]))
            A.append([int(z*den) for z in row]);b.append(int(rhs[c]*den))
print(rid,'built',len(A),len(A[0]),'removed integral restrictions',len(oldcols)-len(data['cols']),flush=True)
name=f'{rid}_integral_center_h{height}{"_tau"+str(tau) if tau is not None else ""}'
system_sha=hashlib.sha256(json.dumps({'A':A,'b':b},separators=(',',':')).encode()).hexdigest()
tensor_sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
if verify:
    previous=json.loads((HERE/f'{name}.json').read_text())
    if previous.get('system_sha256',system_sha)!=system_sha:raise ValueError('Reconstructed system hash mismatch')
    ray=previous['ray'];why={'mode':'exact_replay_no_optimizer'}
    if ray is None:raise ValueError('No exact separator recorded')
else:
    ray,why=qc.exact_separator(A,b,timeout=limit)
out={'id':rid,'height':height,'tau_sign':tau,'classification_change':False,
     'outcome':'candidate_exclusion_pending_independent_audit' if ray else 'no_conclusion',
     'theoretical_constraint':'NO_CENTRAL_BOSON.md: integral center Vec or sVec; only h1/h2 fermionic lifts allowed',
     'removed_restrictions':[list(v) for v,z in oldcols if (v,z) not in data['cols']],
     'rows':len(A),'variables':len(A[0]),'system_sha256':system_sha,'tensor_sha256':tensor_sha,
     'ray':ray,'solver_report':why,
     'seconds':time.monotonic()-start}
if ray:
    out['bTy']=sum(x*y for x,y in zip(b,ray))
    out['minimum_ATy']=min(sum(row[j]*y for row,y in zip(A,ray)) for j in range(len(A[0])))
    if not(out['bTy']<0 and out['minimum_ATy']>=0):raise ValueError('Invalid separator')
(HERE/f'{name}{"_replay" if verify else ""}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['ray','removed_restrictions']}),flush=True)
