from pathlib import Path
import sys,json,itertools,time,hashlib,re,subprocess,tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/review'))
import verify_nc_gate_unrestricted as u
def enumerate_gauge(R):
 from oriented_signed import problem
 p=problem(R);du=u.old.dual(R)
 domains=[list(range(-R[a][b][du[c]],R[a][b][du[c]]+1,2)) for orb in p['active'] for a,b,c in [orb[0]]]
 pair_reps=sorted({min(i,du[i]) for i in range(1,len(R))});coordinate={i:pair_reps.index(min(i,du[i])) for i in range(1,len(R))}
 vectors=[]
 for orb in p['active']:
  mask=0
  for i in orb[0]:
   if i:mask^=1<<coordinate[i]
  vectors.append(mask)
 basis={};fixed=[]
 for var in p['order']:
  if domains[var][0]%2==0:continue
  mask=vectors[var]
  while mask:
   pivot=mask.bit_length()-1
   if pivot in basis:mask^=basis[pivot]
   else:basis[pivot]=mask;fixed.append(var);break
 for var in fixed:domains[var]=[x for x in domains[var] if x>0]
 pattern=r'case (\d+):for\(int x:vector<int>\{([^}]*)\}\)\{v\[(\d+)\]=x;'
 def replacement(m):
  level,var=int(m[1]),int(m[3]);u.need(p['order'][level]==var,'enumeration variable order')
  return 'case '+str(level)+':for(int x:vector<int>{'+','.join(map(str,domains[var]))+'}){v['+str(var)+']=x;'
 cpp,count=re.subn(pattern,replacement,p['source']);u.need(count==len(domains),'all domains replaced')
 print('gauge dimensions',len(pair_reps),'fixed',len(fixed),'variables',len(domains),flush=True)
 with tempfile.TemporaryDirectory() as directory:
  source=Path(directory)/'enum.cpp';exe=Path(directory)/'enum';source.write_text(cpp)
  subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True,capture_output=True)
  result=subprocess.run([str(exe)],check=True,capture_output=True,text=True,timeout=240)
 vals=sorted(tuple(map(int,line.split())) for line in result.stdout.splitlines());u.need(len(vals)==len(set(vals)),'duplicate')
 p.update(domains=domains,gauge_fixed_variables=fixed,gauge_dimension=len(pair_reps),gauge_rank=len(fixed))
 return vals,p,result.stderr.strip()

census={r['id']:r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
for rid in sys.argv[1:]:
 start=time.monotonic();R=census[rid]['tensor'];print(rid,'start',flush=True)
 vals,p,stats=enumerate_gauge(R);print(rid,'enumerated',len(vals),stats,'seconds',time.monotonic()-start,flush=True)
 du=u.old.dual(R);signs=[(1,)+tail for tail in itertools.product((-1,1),repeat=7) if all(((1,)+tail)[i]==((1,)+tail)[du[i]] for i in range(8))]
 masks=[tuple(g[x]*g[y]*g[z] for orb in p['active'] for x,y,z in [orb[0]]) for g in signs]
 groups={}
 for v in vals:
  rep=min(tuple(x*y for x,y in zip(v,mask)) for mask in masks);groups.setdefault(rep,[]).append(v)
 print(rid,'classes',len(groups),'sizes',[len(x) for x in groups.values()],flush=True)
 out={'id':rid,'tensor_sha256':census[rid]['tensor_sha256'],'statistics':stats,'gauge_fixed_variables':p['gauge_fixed_variables'],'gauge_dimension':p['gauge_dimension'],'gauge_rank':p['gauge_rank'],'domains':p['domains'],'active':p['active'],'signed_values':vals,'classes':[{'representative':rep,'size':len(members)} for rep,members in groups.items()]}
 (HERE/(rid+'_signed.json')).write_text(json.dumps(out,separators=(',',':'))+'\n')
 a=u.old.ScalarCharacters(R);results=[]
 for rep,members in groups.items():
  T=u.old.from_values(R,p,rep);u.old.validate_general(T);gauge=u.old.proofs.gauge_original(T,R)
  if gauge is not None:report={'kind':'gauge_original','signs':gauge}
  else:
   signed=u.old.ScalarCharacters(T);cc=u.old.character_obstructions(T,a.cf+signed.cf)
   report={'kind':'nongauge','characters':cc,'survivors':sum(c['obstruction'] is None for c in cc)}
  results.append({'representative':rep,'size':len(members),**report});print(rid,'class',len(results),report,flush=True)
 (HERE/(rid+'_character_sieve.json')).write_text(json.dumps(results,indent=2)+'\n')
 print(rid,'done',time.monotonic()-start,flush=True)
