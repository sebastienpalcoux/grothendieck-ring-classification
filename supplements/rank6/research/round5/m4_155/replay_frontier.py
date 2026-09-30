"""Optimizer-free exhaustive reconstruction of the current R155 frontier."""
import json,sys,time,itertools,copy,importlib.util
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
op.linprog=op.milp=lambda *_a,**_kw:(_ for _ in ()).throw(RuntimeError('optimizer forbidden'))
import round3_m4 as M,round5_155 as V,round5_unified as U,round4_quartic_twists as T
from spectral_induction import Spectrum
from higher_traces import check_farkas
from exact import require
import round5_balancing as CB
h=Path(__file__).parent;cert=json.load(open(h/'frontier_certificate.json'));R=next(x['N']for x in json.load(open(P/'data/census.json'))if x['id']==cert['id']);start=time.monotonic()
def dense_ray(sparse,m):
 y=[0]*m
 for i,x in sparse:require(y[i]==0 and type(x)is int and x!=0,'bad ray encoding');y[i]=x
 return y
pointed=copy.deepcopy(cert['pointed'])
for r in pointed['branches']:
 if r.get('outcome')=='exact_farkas':r['ray']=dense_ray(r['ray'],r['rows'])
pv=V.verify_pointed_reduction(R,pointed);print('pointed',pv['exact_rays'],flush=True)
d=M.data_for(R,6,8);cols=d['lows'][6];labs=d['tab'].assignments(cols);lab=labs[0];perm=V.verify_labelling_quotient(cols,labs);require(len(pv['survivors'])==len(labs)and all(x['low']==6 and x['indicators']==[0,0,1,-1,-1]for x in pv['survivors']),'wrong surviving branch')
expected=[(list(la),z)for la in labs for z in['-2','-1/2']];require([(r['labelling'],r['cubic'])for r in cert['cubic']['cases']]==expected,'incomplete cubic branches')
for r in cert['cubic']['cases']:
 A,b,meta=V.nonselfdual_stabilizer_system(R,d,cols,(0,0,1,-1,-1),r['labelling'],exact_cubic_value=Fraction(r['cubic']));check_farkas(A,b,dense_ray(r['ray'],len(A)))
print('cubic',len(expected),flush=True)
ld=V.profile_lattice(R,d,cols,lab);profiles,nodes=V.enumerate_lattice(ld);require(sorted(cert['profiles'])==profiles and len({tuple(p)for p in cert['profiles']})==len(profiles),'profile domain incomplete');require(cert['high_columns']==ld['high_columns'],'high-column mismatch');high=cert['high_columns'];profiles=cert['profiles'];pc=[ix for ix,p in enumerate(profiles)if V.pointed_profile_reason(R,cols,high,p)[0]is None];require([r['profile']for r in cert['joint']]==pc,'incomplete pointed-profile reduction')
print('profiles',len(profiles),'pointed-compatible',len(pc),flush=True)
sp=Spectrum(d['tab'],cols,[(tuple(v),None)for v in high]);words=[w for k in(2,3)for w in itertools.combinations_with_replacement(range(1,6),k)];cache={};kept=[];empty=0;gram_rays=0
for ix,r in enumerate(cert['joint']):
 pi=r['profile'];p=profiles[pi];wd=U.low_word_data(R,d,cols,high,p,lab,words=words,spectrum=sp)
 if r['outcome']=='exact_empty_domain':
  v=r['empty_column'];require(v[0]==0 and p[high.index(v[1:])]>0,'empty absent type');Q=[[sum(m*x[i]*x[j]for x,m in zip(high,p))for j in range(5)]for i in range(5)];dom=U.enumerate_fixed_gram_block(Q,[x[1:]for x in wd['restriction']],wd['gram'],v[1:],node_limit=1000000,time_limit=30);require(dom['complete']and not dom['candidates'],'empty-domain certificate fails');empty+=1
 else:
  dom=U.joint_coefficient_domains(wd,node_limit=1000000,time_limit=30);require(dom['complete'],'incomplete domain');ss=U.count_system(wd,dom)
  if r['outcome']=='exact_farkas':V.check_sparse_ray(ss['rows'],ss['rhs'],len(ss['labels']),dense_ray(r['ray'],len(ss['rhs'])));gram_rays+=1
  else:require(r['outcome']=='retained','unexpected outcome');cache[pi]=(wd,dom);kept.append(pi)
 if(ix+1)%100==0:print('joint',ix+1,'seconds',time.monotonic()-start,flush=True)
require([r['profile']for r in cert['coupled']]==kept,'incomplete coupled cases');A0,b0,meta=V.nonselfdual_stabilizer_system(R,d,cols,(0,0,1,-1,-1),lab,exact_cubic_value=1);sur=[];rays=0
for r in cert['coupled']:
 pi=r['profile']
 if r['outcome']=='retained':sur.append(pi);continue
 require(r['outcome']=='exact_farkas','unexpected coupled outcome');wd,dom=cache[pi];A,b,kept,integ=T.fixed_profile(A0,b0,meta['labels'],meta['base'],meta['keep'],high,profiles[pi]);ss=CB.build_coupled(R,d,cols,lab,A,b,meta['labels'],kept,[1]*len(A[0]),wd,dom);V.check_sparse_ray(ss['rows'],ss['rhs'],len(ss['labels']),dense_ray(r['ray'],len(ss['rhs'])));rays+=1
require(all(V.pointed_profile_reason(R,cols,high,profiles[pi])[1]==[0,3,4,5]for pi in sur),'full pointed group not forced')
result={str(sign):[pi for pi in sur if not V.pointed_stabilizer_divisibility(R,cols,high,profiles[pi],[0,3,4,5],[0,3]if sign==-1 else[0])]for sign in[-1,1]};require(result==cert['pointed_orbits'],'pointed stabilizer domain mismatch')
out={'passed':True,'optimized_python':not __debug__,'optimizer_used':False,'status':'open','pointed_rays':pv['exact_rays'],'cubic_rays':len(expected),'labelling_permutations':perm,'profiles':len(profiles),'profile_nodes':nodes,'pointed_compatible':len(pc),'empty_domains':empty,'joint_gram_rays':gram_rays,'coupled_rays':rays,'before_pointed_orbits':len(sur),'remaining_by_quadratic_sign':result,'remaining_profiles':len(set().union(*map(set,result.values()))),'seconds':time.monotonic()-start}
(h/'frontier_replay_optimized.json').write_text(json.dumps(out,indent=2));print(out,flush=True)
