"""Complete diagonal-algebra/character integrality compatibility by Morita profile."""
import json,itertools,collections,random
import sympy as s
from gram_discovery import HERE,REPO,require
from morita_closure import DATA

def projectors(R,ds):
 x=s.Symbol('x');N=list(map(s.Matrix,R));rng=random.Random(65)
 while True:
  w=[rng.randrange(1,20)for _ in range(8)];T=sum((a*M for a,M in zip(w,N)),s.zeros(8));p=T.charpoly(x).as_poly();ff=s.factor_list(p)[1]
  if all(k==1 for _,k in ff):break
 out=[]
 for f,_ in ff:
  h=p.exquo(f);c=s.invert(h,f);poly=(h*c).rem(p);E=s.zeros(8)
  for coef in poly.all_coeffs():E=E*T+coef*s.eye(8)
  require(E*E==E and E.T==E,'rational orthogonal projector')
  ed=E*s.Matrix([s.Rational(d[0])+s.Rational(d[1])*s.sqrt(DATA[next(k for k,v in DATA.items()if v[1]==ds)][0])for d in ds])
  pf=ed!=s.zeros(8,1)
  out.append({'polynomial':str(f.as_expr()),'degree':f.degree(),'E':E,'coefficients':list(E[:,0]),'PF':pf})
 require(sum(q['PF']for q in out)==1,'one PF rational orbit')
 return out

def run():
 source={x['id']:x for x in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())};old={(x['id'],x['candidate_index']):x for x in json.loads((HERE/'integral_gram.json').read_text())};records=json.loads((HERE/'profile_closure.json').read_text());out={}
 for rid,r in records.items():
  if rid=='R8_3_65':continue
  R=source[rid]['tensor'];ps=projectors(R,DATA[rid][1]);groups=collections.defaultdict(list)
  for f in r['surviving_factors']:groups[tuple(tuple(t)for t in f['profile'])].append(f)
  result=[]
  for profile,fs in groups.items():
   multiplicities=collections.Counter(profile);opts=collections.defaultdict(set)
   for f in fs:opts[tuple(f['root_dimension'])].add(f['candidate_index'])
   group_options=[]
   for t,count in multiplicities.items():
    group_options.append(list(itertools.combinations_with_replacement(sorted(opts[t]),count)))
   valid=[]
   for choice in itertools.product(*group_options):
    indices=[i for c in choice for i in c];trace=[sum(old[(rid,i)]['algebra_object'][j]for i in indices)for j in range(8)];ms=[sum(c*t for c,t in zip(q['coefficients'],trace))/q['degree']for q in ps]
    if any(z.q!=1 or z<0 or(q['PF']and z!=1)for z,q in zip(ms,ps)):continue
    valid.append({'loop_candidate_indices':indices,'trace':trace,'character_orbit_multiplicities':[int(z)for z in ms]})
   ff=[]
   for f in fs:
    B=s.Matrix(f['B']);support=[B*q['E']!=s.zeros(B.rows,8)for q in ps]
    compatible=[j for j,v in enumerate(valid)if f['candidate_index']in v['loop_candidate_indices']and all(not a or b>=1 for a,b in zip(support,v['character_orbit_multiplicities']))]
    ff.append({'candidate_index':f['candidate_index'],'factor_index':f['factor_index'],'compatible_trace_assignment_indices':compatible})
   result.append({'profile':[list(t)for t in profile],'trace_assignments':valid,'factor_checks':ff})
  out[rid]={'rational_character_orbits':[{k:v for k,v in q.items()if k!='E'}for q in ps],'profiles':result}
  print(rid,'profiles',len(result),'surviving profiles',sum(any(f['compatible_trace_assignment_indices']for f in p['factor_checks'])for p in result),'surviving factors',sum(bool(f['compatible_trace_assignment_indices'])for p in result for f in p['factor_checks']),flush=True)
 (HERE/'trace_closure.json').write_text(json.dumps(out,default=str,separators=(',',':'))+'\n')
 return out
if __name__=='__main__':run()
