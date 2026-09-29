"""Exact higher-dimensional stabilizer Clifford rotation sieve.

For a forced anti-commuting stabilizer on Hom(1,Y^3) of dimension n,
nu_3(Y)=-(a+b*w+c*w^2), a+b+c=n/2. In a real quadratic relative
trace field its average is n/4-3*a/2. If 3 is absent from the exponent,
nu_3 is rational and belongs to {-n/2+3*b:0<=b<=floor(n/4)}.
No ring is excluded unless every involution-module and central branch fails.
"""
import itertools,json,time
from fractions import Fraction as Q
from exact import require
import stabilizer_rotation as C
from augmented_spectrum import AugmentedSpectrum
from module_dual_gram import anti_representations
from involution_module import invs
from rings import dual
from higher_traces import trace_types,check_farkas,farkas
I=C.I

class Ineligible(Exception):pass
class Survives(Exception):pass

def cubic(R,y):return R[y][y][dual(R)[y]]

_RAYS={}
def cached_farkas(A,b):
 key=(len(A),len(A[0]));rays=_RAYS.setdefault(key,[])
 for y in rays:
  support=[(i,v) for i,v in enumerate(y) if v]
  if sum(b[i]*v for i,v in support)>=0:continue
  if all(sum(A[i][j]*v for i,v in support)>=0 for j in range(len(A[0]))):return y
 y=farkas(A,b)
 if y is not None:
  check_farkas(A,b,y)
  if len(rays)<64:rays.append(y)
 return y

def values(n,primes):
 require(type(n) is int and n>=0 and n%2==0,'invalid Clifford dimension')
 if 3 not in primes:return [Q(-n,2)+3*b for b in range(n//4+1)]
 return sorted({Q(n,4)-Q(3*a,2) for a in range(n//2+1)})

def objects_for(R,g,fixed,T):
 f=len(fixed)
 return [y for a,y in enumerate(fixed) if cubic(R,y)>0 and T[g][a*f+a]==-1]

def trace_system(R,data,tab,cols,ep,height,lab,sp,objects,targets=None):
 character=lab is not None
 L=I.s.Matrix.hstack(*map(I.s.Matrix,cols))
 base,b,rot=I.system_rotation(R,data,L,ep,height);labels=rot['labels']
 if character:
  K=tab.K;A,b,meta=I.equation_system(R,data,tab,cols,ep,height,lab,sp)
  forbidden=set(map(tuple,sp.forbidden));keep=[j for j in range(len(base[0])) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
  dim=lambda v:tab.dims[tuple(v)]
  D=tab.D
 else:
  K=data['K'];A=base;meta={'variables':len(base[0]),'equations':len(base),'character_refinement':False};keep=list(range(len(base[0])))
  dim=lambda v:sum((K(int(c))*d for c,d in zip(v,data['ds'])),K.zero)
  D=data['D']
 require(len(keep)==len(A[0]),'trace variable mismatch')
 ts,_=trace_types(data['q'],data['primes'],height);sq=K.from_sympy(I.s.sqrt(data['q']))
 phase=[K(t[2][0])+K(t[2][1])*sq for t in ts]
 interval=targets is None;nv=len(A[0]);extra=2*len(objects) if interval else 0
 if extra:A=[row+[0]*extra for row in A]
 added=0
 for k,obj in enumerate(objects):
  n=cubic(R,obj);target=Q(n,4) if interval else targets[k]
  rhs=K(I.s.Rational(target.numerator,target.denominator))*D-sum((K(v[obj])*dim(v) for v in cols),K.zero)
  coeff=[K(labels[j][0][obj-1])*dim((0,)+tuple(labels[j][0]))*phase[labels[j][1]] if j<len(labels) else K.zero for j in keep]
  coeff += [K.zero]*extra
  if interval:coeff[nv+2*k]=D
  for row,rhs1 in I.rational_rows(coeff,rhs,K):A.append(row);b.append(rhs1);added+=1
  if interval:
   # z=upper-average and w=average-lower, both nonnegative.
   row=[0]*(nv+extra);row[nv+2*k]=row[nv+2*k+1]=4;A.append(row);b.append(3*n);added+=1
 return A,b,{**meta,'higher_indicator_equations':added,'variables':nv+extra,'equations':len(A),'interval':interval}

def discover_conditional(R,objects,height=3,progress=None):
 try:data,tab=I.reciprocity_data(R)
 except I.Ineligible as e:raise Ineligible(str(e))
 character=tab.K.mod.degree()<=(1 if data['q']==1 else 2)
 domains=[values(cubic(R,y),data['primes']) for y in objects]
 branches=[]
 for ix,cols in enumerate(data['lows']):
  branch={'columns':list(map(list,cols))}
  why=I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:branch['ordinary']=why;branches.append(branch);continue
  labs=tab.assignments(cols) if character else [None];branch['labellings']=[list(lab) if lab is not None else None for lab in labs]
  sp=None
  if character and labs:
   _,high=I.high_columns(data,I.s.Matrix.hstack(*map(I.s.Matrix,cols)));sp=AugmentedSpectrum(tab,cols,high);branch['spectrum']=sp.metadata()
   if sp.missing_low:branches.append(branch);continue
  cases=[]
  for lab in labs:
   for ep in I.indicator_choices(R):
    A,b,meta=trace_system(R,data,tab,cols,ep,height,lab,sp,objects)
    ray=cached_farkas(A,b);rec={'labelling':list(lab) if lab is not None else None,'indicators':list(ep)}
    if ray is not None:
     check_farkas(A,b,ray);rec.update(method='interval',system=meta,y=ray)
    else:
     sub=[]
     for target in itertools.product(*domains):
      A,b,meta=trace_system(R,data,tab,cols,ep,height,lab,sp,objects,target);ray=cached_farkas(A,b)
      if progress:progress(ix,rec['labelling'],ep,list(map(str,target)),ray is not None)
      if ray is None:raise Survives('a necessary central-indicator branch survives')
      check_farkas(A,b,ray);sub.append({'values':list(map(str,target)),'system':meta,'y':ray})
     rec.update(method='discrete',cases=sub)
    cases.append(rec)
    if progress:progress(ix,rec['labelling'],ep,'interval' if rec['method']=='interval' else 'discrete',True)
  branch['cases']=cases;branches.append(branch)
 return {'kind':'conditional_higher_stabilizer','version':1,'objects':objects,'cubic_dimensions':[cubic(R,y) for y in objects],
         'domains':[[str(z) for z in v] for v in domains],'height':height,'q':data['q'],'prime_support':data['primes'],
         'character_refinement':character,'table':tab.metadata() if character else None,
         'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify_conditional(R,c):
 require(c['kind']=='conditional_higher_stabilizer' and c['version']==1,'bad higher conditional')
 objects=c['objects'];require(objects==sorted(set(objects)) and objects and all(type(j) is int and 0<j<len(R) for j in objects),'invalid higher object set')
 require(type(c['height']) is int and 3<=c['height']<=12,'bad higher trace height')
 data,tab=I.reciprocity_data(R);character=tab.K.mod.degree()<=(1 if data['q']==1 else 2)
 require(c['character_refinement']==character and c['q']==data['q'] and c['prime_support']==data['primes'],'wrong field metadata')
 require(c['table']==(tab.metadata() if character else None),'wrong character metadata')
 domains=[values(cubic(R,y),data['primes']) for y in objects]
 require(c['cubic_dimensions']==[cubic(R,y) for y in objects] and c['domains']==[[str(z) for z in v] for v in domains],'wrong Clifford domains')
 require(c['column_counts']==list(map(len,data['columns'])) and len(c['branches'])==len(data['lows']),'incomplete low-frame domain')
 for cols,branch in zip(data['lows'],c['branches']):
  require(branch['columns']==list(map(list,cols)),'wrong low frame')
  why=I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:require(branch['ordinary']==why,'wrong ordinary obstruction');continue
  labs=tab.assignments(cols) if character else [None]
  require(branch['labellings']==[list(lab) if lab is not None else None for lab in labs],'missing labelling')
  sp=None
  if character and labs:
   _,high=I.high_columns(data,I.s.Matrix.hstack(*map(I.s.Matrix,cols)));sp=AugmentedSpectrum(tab,cols,high)
   require(branch['spectrum']==sp.metadata(),'wrong spectrum')
   if sp.missing_low:continue
  expected=[(list(lab) if lab is not None else None,list(ep)) for lab in labs for ep in I.indicator_choices(R)]
  require([(r['labelling'],r['indicators']) for r in branch['cases']]==expected,'missing indicator branch')
  for rec in branch['cases']:
   if rec['method']=='interval':
    A,b,meta=trace_system(R,data,tab,cols,rec['indicators'],c['height'],rec['labelling'],sp,objects)
    require(meta==rec['system'],'wrong interval system');check_farkas(A,b,rec['y'])
   else:
    require(rec['method']=='discrete','unknown higher method')
    targets=list(itertools.product(*domains));require([v['values'] for v in rec['cases']]==[list(map(str,z)) for z in targets],'missing Clifford value branch')
    for target,r in zip(targets,rec['cases']):
     A,b,meta=trace_system(R,data,tab,cols,rec['indicators'],c['height'],rec['labelling'],sp,objects,target)
     require(meta==r['system'],'wrong discrete system');check_farkas(A,b,r['y'])
 return True

def certificate(R,height=3,progress=None):
 if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):raise Ineligible('commutative input required')
 eligible=False
 for g in invs(R):
  info=anti_representations(R,g)
  if info is None:continue
  fixed,seed,nodes,reps=info;eligible=True;branches=[];conditionals=[];cache={};failed=False
  for ti,T in enumerate(reps):
   objects=objects_for(R,g,fixed,T);branch={'T':list(map(list,T))}
   if any(cubic(R,y)%2 for y in objects):
    branch.update(method='odd_cubic',objects=objects);branches.append(branch);continue
   if objects:
    key=tuple(objects)
    if key not in cache:
     try:cc=discover_conditional(R,objects,height,progress)
     except Survives:cc=None
     if cc is None:cache[key]=None
     else:cache[key]=len(conditionals);conditionals.append(cc)
    if cache[key] is None:
     ab,meta=C.morita_system(R,g,fixed,T)
     if ab is None:branch.update(method='morita_rank',meta=meta)
     else:
      ray=C.zero_column_ray(*ab)
      if ray is None:failed=True;break
      check_farkas(*ab,ray);branch.update(method='morita_gram',meta=meta,y=ray)
    else:branch.update(method='higher_stabilizer',objects=objects,conditional=cache[key])
   else:
    ab,meta=C.morita_system(R,g,fixed,T)
    if ab is None:branch.update(method='morita_rank',meta=meta)
    else:
     ray=C.zero_column_ray(*ab)
     if ray is None:failed=True;break
     check_farkas(*ab,ray);branch.update(method='morita_gram',meta=meta,y=ray)
   branches.append(branch)
  if not failed:return {'kind':'stabilizer_rotation_higher','version':1,'scope':'pseudo_unitary','involution':g,'fixed':fixed,'generators':list(seed),'generator_tuples':nodes,'branches':branches,'conditionals':conditionals}
 if not eligible:raise Ineligible('no eligible forced involution module')
 raise Survives('at least one necessary module/center branch survives')

def verify(R,c):
 require(c['kind']=='stabilizer_rotation_higher' and c['version']==1 and c['scope']=='pseudo_unitary','bad higher certificate')
 g=c['involution'];require(g in invs(R),'bad involution');fixed,seed,nodes,reps=anti_representations(R,g)
 require(c['fixed']==fixed and c['generators']==list(seed) and c['generator_tuples']==nodes,'wrong module domain')
 require([b['T'] for b in c['branches']]==[list(map(list,T)) for T in reps],'missing module branch')
 for cc in c['conditionals']:verify_conditional(R,cc)
 used=set()
 for T,b in zip(reps,c['branches']):
  if b['method']=='odd_cubic':
   objs=objects_for(R,g,fixed,T);require(objs==b['objects'] and any(cubic(R,y)%2 for y in objs),'wrong odd Clifford dimension')
  elif b['method']=='higher_stabilizer':
   objs=objects_for(R,g,fixed,T);i=b['conditional'];require(type(i) is int and 0<=i<len(c['conditionals']),'invalid conditional index');require(objs and b['objects']==objs and c['conditionals'][i]['objects']==objs,'wrong stabilizer objects');used.add(i)
  else:
   ab,meta=C.morita_system(R,g,fixed,T);require(meta==b['meta'],'wrong Morita system')
   if ab is None:require(b['method']=='morita_rank','wrong rank obstruction')
   else:require(b['method']=='morita_gram','wrong Gram obstruction');check_farkas(*ab,b['y'])
 require(used==set(range(len(c['conditionals']))),'unused conditionals');return True

def verify_general(R,c):
 import galois_pseudo_reduction as G
 require(c['kind']=='general_stabilizer_rotation_higher' and c.get('version')==1,'bad general higher stabilizer certificate')
 require(c.get('scope')=='general','wrong general higher scope')
 if c['reduction'].get('kind')=='two_fp_values':
  from rings import Characters
  require(set(c['reduction'])=={'kind'},'unexpected two-FP-value reduction payload')
  require(len(set(Characters(R).fp()[2]))==2,'two-FP-value Galois reduction does not apply')
 else:G.verify(R,c['reduction'])
 verify(R,c['pseudo'])
 return True

if __name__=='__main__':
 import argparse,signal
 from pathlib import Path
 ROOT=Path(__file__).resolve().parents[1]
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('id');p.add_argument('--output',type=Path,required=True);p.add_argument('--seconds',type=int,default=600);p.add_argument('--height',type=int,default=3);p.add_argument('--verify',action='store_true');args=p.parse_args()
 R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==args.id)
 if args.verify:
  c=json.load(open(args.output))['certificate'];(verify_general if c['kind']=='general_stabilizer_rotation_higher' else verify)(R,c);print('EXACT HIGHER STABILIZER VERIFIED',args.id,flush=True)
 else:
  start=time.monotonic();record={'id':args.id};last=[None]
  def budget(*a):raise TimeoutError('explicit per-input discovery budget reached')
  def progress(*a):last[0]=a;print(json.dumps({'id':args.id,'progress':a}),flush=True)
  signal.signal(signal.SIGALRM,budget);signal.alarm(args.seconds)
  try:
   c=certificate(R,height=args.height,progress=progress);signal.alarm(0);verify(R,c);record.update(outcome='pseudo_unitary_excluded',certificate=c)
  except Ineligible as e:record.update(outcome='ineligible',reason=str(e),certificate=None)
  except Survives as e:record.update(outcome='no_exact_obstruction',reason=str(e),certificate=None)
  except TimeoutError as e:record.update(outcome='budget_incomplete',reason=str(e),certificate=None,last_progress=last[0])
  finally:signal.alarm(0)
  record['seconds']=time.monotonic()-start;args.output.write_text(json.dumps(record,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in record.items() if k!='certificate'}),flush=True)
