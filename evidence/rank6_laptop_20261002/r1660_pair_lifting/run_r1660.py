"""Resumable exact NEW low/high restriction-product lifting for R6_8_1660.
Python3 standard library only. Passing never constructs a category.
"""
import argparse,collections,hashlib,itertools,json,math,sqlite3,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED_INPUT_SHA='b7f262afdb4d4345d653b42399830faa6e2842d874ddc3da4e96778fcf0162d4'
ALGORITHM='ungraded-restriction-lifting-v1'
class Budget(Exception):pass

def require(v,msg):
 if not v:raise ValueError(msg)
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(encode(x).encode()).hexdigest()

def product(R,a,b):
 n=len(R)
 return tuple(sum(a[i]*b[j]*R[i][j][k]for i in range(n)for j in range(n))for k in range(n))

def make_problem(R,columns,u,v,unit_coefficient):
 """Aggregate only equal restrictions; preserve their simple-object counts."""
 n=len(R);one=(1,)+(0,)*(n-1);u=tuple(u);v=tuple(v)
 require(unit_coefficient in (0,1),'unit coefficient')
 counts={tuple(w):m for w,m in columns};require(counts.get(one,0)>=1,'missing distinguished unit')
 raw=product(R,u,v);target=tuple(raw[k]-unit_coefficient*one[k]for k in range(n))
 vectors=[];caps=[]
 for w,m in sorted(counts.items()):
  # Remove the distinguished central unit, not its entire restriction fibre.
  m-=int(w==one)
  if m==0:continue
  wb=product(R,w,v);aw=product(R,u,w)
  cap=min([raw[k]//w[k]for k in range(n)if w[k]]+
          [wb[k]//u[k]for k in range(n)if u[k]]+
          [aw[k]//v[k]for k in range(n)if v[k]])
  if sum(w)==1:
   k=w.index(1)
   if tuple(R[k][k])==one:cap=min(cap,1) # every such central simple is invertible
  aggregate=m*cap
  if min(target)>=0:aggregate=min(aggregate,min(target[k]//w[k]for k in range(n)if w[k]))
  if aggregate>0:vectors.append(w);caps.append(aggregate)
 return {'vectors':vectors,'caps':caps,'target':target}

def validate_solution(problem,coefficients):
 V=problem['vectors'];B=problem['caps'];target=problem['target']
 return (len(coefficients)==len(V) and all(type(x)is int and 0<=x<=b for x,b in zip(coefficients,B))
         and all(sum(x*v[k]for x,v in zip(coefficients,V))==target[k]for k in range(len(target))))

def solve(problem,node_limit=200000,seconds=15.0,cache_limit=200000):
 """Exhaustive bounded positive-vector DFS. A budget stop is UNKNOWN."""
 start=time.monotonic();deadline=start+seconds;nodes=0
 V=[tuple(v)for v in problem['vectors']];B=list(problem['caps']);target=tuple(problem['target']);n=len(target)
 require(len(V)==len(B) and all(b>=0 for b in B),'invalid bounded system')
 require(all(len(v)==n and all(type(x)is int and x>=0 for x in v) and any(v)for v in V),'invalid columns')
 order=sorted(range(len(V)),key=lambda i:(B[i],-sum(x!=0 for x in V[i]),-sum(V[i]),V[i]))
 VV=[V[i]for i in order];BB=[B[i]for i in order];q=len(V)
 # Coordinate and coordinate-difference bounds/gcds prune only exact necessities.
 forms=[tuple(int(i==j)for i in range(n))for j in range(n)]
 forms += [tuple(int(k==i)-int(k==j)for k in range(n))for i in range(n)for j in range(i+1,n)]
 W=[tuple(sum(f[k]*v[k]for k in range(n))for f in forms)for v in VV]
 lo=[[0]*len(forms)for _ in range(q+1)];hi=[[0]*len(forms)for _ in range(q+1)];gcd=[[0]*len(forms)for _ in range(q+1)]
 for pos in range(q-1,-1,-1):
  for k,z in enumerate(W[pos]):
   lo[pos][k]=lo[pos+1][k]+min(0,z*BB[pos]);hi[pos][k]=hi[pos+1][k]+max(0,z*BB[pos]);gcd[pos][k]=math.gcd(gcd[pos+1][k],z)
 dead=set()
 def dfs(pos,r):
  nonlocal nodes
  if nodes>=node_limit or time.monotonic()>=deadline:raise Budget()
  nodes+=1
  if min(r,default=0)<0:return None
  if not any(r):return (0,)*(q-pos)
  if pos==q:return None
  key=(pos,r)
  if key in dead:return None
  rr=tuple(sum(f[k]*r[k]for k in range(n))for f in forms)
  for k,z in enumerate(rr):
   if z<lo[pos][k]or z>hi[pos][k]or(gcd[pos][k]and z%gcd[pos][k]):
    if len(dead)<cache_limit:dead.add(key)
    return None
  low=0;high=BB[pos]
  for k,z in enumerate(W[pos]):
   if z>0:
    low=max(low,-((hi[pos+1][k]-rr[k])//z));high=min(high,(rr[k]-lo[pos+1][k])//z)
   elif z<0:
    a=-z;low=max(low,-((rr[k]-lo[pos+1][k])//a));high=min(high,(hi[pos+1][k]-rr[k])//a)
  for x in range(high,low-1,-1):
   tail=dfs(pos+1,tuple(r[k]-x*VV[pos][k]for k in range(n)))
   if tail is not None:return (x,)+tail
  if len(dead)<cache_limit:dead.add(key)
  return None
 try:
  path=dfs(0,target)
  if path is None:status='infeasible';answer=None
  else:
   answer=[0]*q
   for i,x in zip(order,path):answer[i]=x
   require(validate_solution(problem,answer),'internal solution check failed');status='feasible'
 except Budget:status='unknown_budget';answer=None
 return {'status':status,'nodes':nodes,'seconds':round(time.monotonic()-start,6),'coefficients':answer}

def jobs(R,columns,include_low_low=False):
 out=[];n=len(R);one=(1,)+(0,)*(n-1)
 def is_invertible(v):return sum(v)==1 and tuple(R[v.index(1)][v.index(1)])==one
 for i,(u,m)in enumerate(columns):
  for v,mm in columns[i:]:
   if not include_low_low and u[0]and v[0]:continue
   if is_invertible(u)or is_invertible(v):continue # already forced permutation products
   for unit in ([1,0]if u==v and m>=2 else [1]if u==v else [0]):
    problem=make_problem(R,columns,u,v,unit)
    out.append({'u':u,'v':v,'unit_coefficient':unit,'problem':problem,'problem_key':digest(problem)})
 return sorted(out,key=lambda j:(sum(j['problem']['target']),len(j['problem']['vectors']),j['u'],j['v'],j['unit_coefficient']))

def load_input(path):
 raw=path.read_bytes();require(hashlib.sha256(raw).hexdigest()==EXPECTED_INPUT_SHA,'input SHA256 differs')
 d=json.loads(raw);R=d['tensor'];n=len(R);require(n==6,'base rank')
 require(all(R[i][j][0]==int(i==j)for i,j in itertools.product(range(n),repeat=2)),'self-dual base required')
 H=d['total_restriction_gram'];aliases=0
 for p in d['profiles']:
  require(digest(p['columns'])==p['key'],'profile key differs');aliases+=len(p['aliases'])
  require(all(sum(m*v[i]*v[j]for v,m in p['columns'])==H[i][j]for i,j in itertools.product(range(n),repeat=2)),'profile restriction Gram differs')
 require(aliases==d['profile_count']==1136 and len(d['profiles'])==628,'profile coverage')
 return d

def save_report(db,data,path,configuration):
 states={r[0]:json.loads(r[1])for r in db.execute('SELECT profile_key,record FROM profiles')};totals=collections.Counter();records=[]
 for p in data['profiles']:
  state=states.get(p['key'],{'status':'not_run','tested':0});totals[state['status']]+=len(p['aliases'])
  records.append({'profile_key':p['key'],'aliases':p['aliases'],**state})
 report={'format':1,'algorithm':ALGORITHM,'input_sha256':EXPECTED_INPUT_SHA,'ring_id':data['ring_id'],
         'categorification_status':'unresolved; returned necessary-test obstructions require independent replay',
         'labelled_profile_counts':dict(totals),'distinct_ungraded_profiles':628,'profiles':records,
         'configuration':configuration,'return_instructions':'Send this JSON file back. Keep the SQLite checkpoint locally for resuming.'}
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(report,indent=2)+'\n');tmp.replace(path)
 return report

def main(argv=None):
 a=argparse.ArgumentParser(description=__doc__)
 a.add_argument('--input',type=Path,default=HERE/'r1660_profiles.json');a.add_argument('--output',type=Path,default=Path('r1660_results.json'));a.add_argument('--checkpoint',type=Path,default=Path('r1660_checkpoint.sqlite3'))
 a.add_argument('--seconds',type=float,default=3600);a.add_argument('--seconds-per-pair',type=float,default=15);a.add_argument('--nodes-per-pair',type=int,default=200000);a.add_argument('--cache-states',type=int,default=200000)
 a.add_argument('--max-profiles',type=int,default=0,help='0 means all; use2 for a short pilot');a.add_argument('--retry-unknown',action='store_true');a.add_argument('--summarize',action='store_true')
 args=a.parse_args(argv);require(args.seconds>=0 and args.seconds_per_pair>=0 and args.nodes_per_pair>=0,'nonnegative budgets required')
 data=load_input(args.input);args.output.parent.mkdir(parents=True,exist_ok=True);args.checkpoint.parent.mkdir(parents=True,exist_ok=True)
 db=sqlite3.connect(args.checkpoint);db.execute('CREATE TABLE IF NOT EXISTS metadata(key TEXT PRIMARY KEY,value TEXT)');db.execute('CREATE TABLE IF NOT EXISTS problems(key TEXT PRIMARY KEY,result TEXT,node_budget INTEGER,time_budget REAL)');db.execute('CREATE TABLE IF NOT EXISTS profiles(profile_key TEXT PRIMARY KEY,record TEXT)')
 identity=encode({'input':EXPECTED_INPUT_SHA,'algorithm':ALGORITHM,'script':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()});old=db.execute("SELECT value FROM metadata WHERE key='identity'").fetchone()
 if old:require(old[0]==identity,'checkpoint belongs to different input/script; choose a new checkpoint')
 else:db.execute("INSERT INTO metadata VALUES('identity',?)",(identity,));db.commit()
 configuration={k:v for k,v in vars(args).items()if not isinstance(v,Path)};deadline=time.monotonic()+args.seconds;processed=0
 try:
  if not args.summarize:
   for profile in data['profiles']:
    if time.monotonic()>=deadline or(args.max_profiles and processed>=args.max_profiles):break
    existing=db.execute('SELECT record FROM profiles WHERE profile_key=?',(profile['key'],)).fetchone()
    if existing and json.loads(existing[0])['status']in ('pairwise_pass','profile_rejected'):continue
    tasks=jobs(data['tensor'],profile['columns']);tested=unknown=0;failure=None;all_visited=True
    for job in tasks:
     if time.monotonic()>=deadline:all_visited=False;break
     budget=min(args.seconds_per_pair,max(0,deadline-time.monotonic()));cached=db.execute('SELECT result,node_budget,time_budget FROM problems WHERE key=?',(job['problem_key'],)).fetchone();result=None
     if cached:
      saved=json.loads(cached[0])
      if saved['status']!='unknown_budget' or(not args.retry_unknown and cached[1]>=args.nodes_per_pair and cached[2]>=budget-0.001):result=saved
     if result is None:
      result=solve(job['problem'],args.nodes_per_pair,budget,args.cache_states)
      db.execute('INSERT OR REPLACE INTO problems VALUES(?,?,?,?)',(job['problem_key'],encode(result),args.nodes_per_pair,budget));db.commit()
     if result['status']=='feasible':require(validate_solution(job['problem'],result['coefficients']),'cached feasible witness failed');tested+=1
     elif result['status']=='infeasible':
      failure={k:job[k]for k in ('u','v','unit_coefficient','problem_key')};failure.update(nodes=result['nodes'],bounded_system=job['problem'],restriction_multiplicities=profile['columns']);tested+=1;break
     else:unknown+=1
    status='profile_rejected'if failure else 'pairwise_pass'if all_visited and unknown==0 else 'partial'
    state={'status':status,'tested':tested,'unknown_budget':unknown,'total_tests':len(tasks)}
    if failure:state['obstruction']=failure
    db.execute('INSERT OR REPLACE INTO profiles VALUES(?,?)',(profile['key'],encode(state)));db.commit();processed+=1
    report=save_report(db,data,args.output,configuration)
    print(json.dumps({'profile':profile['aliases'][0],'status':status,'tested':tested,'unknown_budget':unknown,'labelled_counts':report['labelled_profile_counts']}),flush=True)
 except KeyboardInterrupt:print('Interrupted safely; completed pair tests are saved.',flush=True)
 finally:
  report=save_report(db,data,args.output,configuration);db.close()
 print(json.dumps({'output':str(args.output),'checkpoint':str(args.checkpoint),'counts':report['labelled_profile_counts']}),flush=True)
 return report
if __name__=='__main__':main()
