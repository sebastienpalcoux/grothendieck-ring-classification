"""Independent bounded solver and checkpoint audit; no full profile search."""
import collections,contextlib,hashlib,importlib.util,io,itertools,json,random,sqlite3,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
P=HERE
spec=importlib.util.spec_from_file_location('audited_r1660',P/'run_r1660.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
def require(b,msg):
 if not b:raise RuntimeError(msg)
def brute(V,B,t):
 for xs in itertools.product(*(range(c+1)for c in B)):
  if all(sum(xs[j]*V[j][k]for j in range(len(V)))==t[k]for k in range(len(t))):return xs
 return None
start=time.monotonic();rng=random.Random(981_771);passed=0
for unused in range(2400):
 n=rng.randrange(1,5);q=rng.randrange(0,6);V=[]
 for j in range(q):
  v=tuple(rng.randrange(5)for k in range(n));V.append(v if any(v)else(1,)+(0,)*(n-1))
 B=[rng.randrange(4)for j in range(q)]
 if unused%3==0:
  coeff=[rng.randrange(b+1)for b in B];target=tuple(sum(coeff[j]*V[j][k]for j in range(q))for k in range(n))
 else:target=tuple(rng.randrange(-1,16)for k in range(n))
 problem={'vectors':V,'caps':B,'target':target};expected=brute(V,B,target)
 got=M.solve(problem,node_limit=50000,seconds=2,cache_limit=rng.choice([0,1,20,200000]))
 require(got['status']==('feasible'if expected is not None else'infeasible'),'independent brute-force disagreement')
 if expected is not None:
  z=got['coefficients'];require(all(0<=x<=b for x,b in zip(z,B)) and all(sum(z[j]*V[j][k]for j in range(q))==target[k]for k in range(n)),'returned witness wrong')
 passed+=1
# Independently check every generated cap on the positive D(S3) restriction control
# can be distributed among the actual repeated simple labels.
R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,1]]]
restrictions=[(1,0,0),(0,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,0),(0,0,1),(0,0,1)]
cols=[[list(v),m]for v,m in sorted(collections.Counter(restrictions).items())]
positive=M.jobs(R,cols,include_low_low=True)
for job in positive:
 ans=M.solve(job['problem'],node_limit=50000,seconds=2)
 require(ans['status']=='feasible','Rep(D(S3)) positive control failed')
 require(M.validate_solution(job['problem'],ans['coefficients']),'bad positive witness')
require({x['unit_coefficient']for x in positive if x['u']==x['v']==[0,0,1]}=={0,1},'duplicate fibre quantifiers')
data=M.load_input(P/'r1660_profiles.json')
# Check reports without mutating the candidate package. Zero-node work must stay UNKNOWN.
with tempfile.TemporaryDirectory()as tmp:
 root=Path(tmp);dbpath=root/'state.sqlite3';outpath=root/'out.json'
 base=['--input',str(P/'r1660_profiles.json'),'--checkpoint',str(dbpath),'--output',str(outpath),'--max-profiles','1','--seconds','4']
 with contextlib.redirect_stdout(io.StringIO()):
  first=M.main(base+['--nodes-per-pair','0','--seconds-per-pair','0.01'])
 require(first['labelled_profile_counts'].get('profile_rejected',0)==0,'zero-node search rejected a profile')
 with sqlite3.connect(dbpath)as db:
  cached=[json.loads(x[0])for x in db.execute('SELECT result FROM problems')]
 require(cached and all(x['status']=='unknown_budget'for x in cached),'zero-node checkpoint false proof')
 with contextlib.redirect_stdout(io.StringIO()):
  second=M.main(base+['--nodes-per-pair','2000','--seconds-per-pair','0.02'])
 require(sum(second['labelled_profile_counts'].values())==1136,'resumed aliases lost')
 with contextlib.redirect_stdout(io.StringIO()):
  third=M.main(base+['--summarize'])
 require(third['labelled_profile_counts']==second['labelled_profile_counts'],'summary altered statuses')
 with sqlite3.connect(dbpath)as db:
  db.execute("UPDATE metadata SET value='wrong-identity' WHERE key='identity'")
 try:
  with contextlib.redirect_stdout(io.StringIO()):M.main(base+['--summarize'])
 except ValueError as ex:require('different input/script'in str(ex),'wrong identity exception')
 else:raise RuntimeError('checkpoint identity mutation accepted')
 bad=root/'mutated.json';bad.write_bytes((P/'r1660_profiles.json').read_bytes()+b' ')
 try:M.load_input(bad)
 except ValueError as ex:require('SHA256 differs'in str(ex),'wrong input exception')
 else:raise RuntimeError('modified input accepted')
receipt={'status':'PASS','scope':'implementation audit and bounded controls; no complete R1660 scan',
 'script_sha256':hashlib.sha256((P/'run_r1660.py').read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((P/'r1660_profiles.json').read_bytes()).hexdigest(),
 'independent_cartesian_product_comparisons':passed,'Rep_D_S3_positive_jobs':len(positive),
 'duplicate_restriction_unit_quantifiers':'both0and1 checked','zero_node_checkpoint':'all unknown, no exclusions',
 'resume_and_summary':'PASS','changed_checkpoint_identity_rejected':True,'changed_input_rejected':True,
 'profile_alias_count':1136,'distinct_ungraded_profiles':628,'bounded_pilot_counts':second['labelled_profile_counts'],
 'seconds':round(time.monotonic()-start,3)}
(HERE/'independent_audit.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
