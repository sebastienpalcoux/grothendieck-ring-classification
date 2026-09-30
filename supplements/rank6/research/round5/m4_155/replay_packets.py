import json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
op.linprog=op.milp=lambda *_a,**_kw:(_ for _ in ()).throw(RuntimeError('optimizer forbidden'))
import round3_m4 as M,round5_155 as V
from exact import require
h=Path(__file__).parent;c=json.load(open(h/'frontier_certificate.json'));R=next(x['N']for x in json.load(open(P/'data/census.json'))if x['id']==c['id']);d=M.data_for(R,3,8);cols=d['lows'][6];lab=d['tab'].assignments(cols)[0];start=time.monotonic();ids=sorted(set().union(*map(set,c['pointed_orbits'].values())));out={'id':c['id'],'input_profiles':ids,'cases':[],'complete':False}
for ix in ids:
 result=V.semion_packet_frontier(R,d,cols,lab,c['high_columns'],c['profiles'][ix],4);require(result['complete'],'incomplete semion packet enumeration');out['cases'].append(dict(profile=ix,**result))
semion_profiles=[r['profile']for r in out['cases']if r['survivors']];splittings=[]
for r in out['cases']:
 for orientation,packet in enumerate(r['survivors']):
  for sign in(-1,1):
   if r['profile']not in c['pointed_orbits'][str(sign)]:continue
   result=V.split_centralizer_adjoint(R,d,cols,lab,packet,4,3,sign);require(result['complete'],'incomplete adjoint splitting');splittings.append(dict(profile=r['profile'],orientation=orientation,quadratic_sign=sign,**result))
# Complex conjugation normalizes q(g)=i, preserving the PU structure and
# the explicitly checked equal-column low labelling quotient.
import importlib.util
import round4_quartic_twists as T,round5_unified as U
from spectral_induction import Spectrum
import round5_balancing as CB
# An integral algebraic number has integral field norm.  Compute the norm
# of d(X)/2 exactly in the ambient cyclotomic field to certify the boson
# de-equivariantization obstruction without a hand calculation.
import sympy as sym
from exact import evaluate
C=d['C'];degree=C.mod.degree();half=d['dims'][1]/C(2);basis=[C.unit**j for j in range(degree)]
coord=lambda z:list(reversed(z.to_list()))+[0]*(degree-len(z.to_list()))
half_norm=sym.det(sym.Matrix.hstack(*(sym.Matrix(coord(half*z))for z in basis)));require(sym.denom(half_norm)!=1,'half dimension might be integral')
conjugate_lab=tuple(d['tab'].rows.index(tuple(evaluate(z.to_list(),C.unit**7,C)for z in d['tab'].rows[lab[a]]))for a in range(len(cols)));require(conjugate_lab in d['tab'].assignments(cols),'missing conjugate low labelling');V.verify_labelling_quotient(cols,d['tab'].assignments(cols));out.update(half_dimension_field_norm=str(half_norm),conjugate_labelling=list(conjugate_lab))
d6=M.data_for(R,6,8);A0,b0,meta=V.nonselfdual_stabilizer_system(R,d6,cols,(0,0,1,-1,-1),lab,exact_cubic_value=1);sp=Spectrum(d6['tab'],cols,[(tuple(v),None)for v in c['high_columns']]);words=[w for k in(2,3)for w in __import__('itertools').combinations_with_replacement(range(1,6),k)];same=[r for r in splittings if r['quadratic_sign']==1 and r['survivors']];same_excluded=[]
for r in same:
 ix=r['profile'];record=next(z for z in c['same_form_rays']if z['profile']==ix);p=c['profiles'][ix];wd=U.low_word_data(R,d6,cols,c['high_columns'],p,lab,words=words,spectrum=sp);dom=U.joint_coefficient_domains(wd,time_limit=30,node_limit=1000000);require(dom['complete'],'incomplete same-form word domain');A,b,kept,integ=T.fixed_profile(A0,b0,meta['labels'],meta['base'],meta['keep'],c['high_columns'],p);oldlen=len(A[0]);A,b,am=V.pointed_pair_action(R,d6,cols,lab,A,b,meta['labels'],kept,4,3,sign=1);kept +=[max(max(meta['keep'])+1,len(meta['labels']))+j for j in range(len(A[0])-oldlen)];ss=CB.build_coupled(R,d6,cols,lab,A,b,meta['labels'],kept,[1]*len(A[0]),wd,dom);y=[0]*len(ss['rhs'])
 for i,a in record['ray']:require(y[i]==0,'duplicate ray coefficient');y[i]=a
 V.check_sparse_ray(ss['rows'],ss['rhs'],len(ss['labels']),y);same_excluded.append(ix);r['same_form_exact_ray']=True;r['survivors']=[]
out.update(same_form_excluded=same_excluded)
out.update(complete=True,semion_profiles=semion_profiles,semion_orientations=sum(len(r['survivors'])for r in out['cases']),splittings=splittings,remaining_profiles=sorted({r['profile']for r in splittings if r['survivors']}),low_matrix_pairs=sum(len(r['survivors'])for r in splittings),optimizer_used=False,optimized_python=not __debug__,seconds=time.monotonic()-start);(h/'packet_frontier.json').write_text(json.dumps(out));print({k:v for k,v in out.items()if k not in('cases','splittings')},flush=True)
