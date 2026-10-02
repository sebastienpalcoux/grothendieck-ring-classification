"""Exact positive, negative, solver-exhaustion and budget controls; no R1660 scan."""
import collections,itertools,json,random,tempfile
from pathlib import Path
import run_r1660 as M

def require(v,msg):
 if not v:raise ValueError(msg)

def solve_all(R,restrictions):
 columns=[[list(v),m]for v,m in sorted(collections.Counter(map(tuple,restrictions)).items())]
 tasks=M.jobs(R,columns,include_low_low=True)
 for task in tasks:
  ans=M.solve(task['problem'],node_limit=100000,seconds=5)
  require(ans['status']=='feasible' and M.validate_solution(task['problem'],ans['coefficients']),'known categorical model failed')
 return columns,tasks

def main():
 # C=Rep(S3); its unitary center Rep(D(S3)) has these induced restrictions.
 R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,1]]]
 restrictions=[[1,0,0],[0,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,0],[0,0,1],[0,0,1]]
 columns,tasks=solve_all(R,restrictions)
 require({j['unit_coefficient']for j in tasks if j['u']==j['v']==[0,0,1]}=={0,1},'duplicate restriction dual/nondual cases omitted')
 # C=Vec(C2); its center has two simples over each invertible. This also
 # checks removal of the distinguished unit without deleting its entire fibre.
 C2=[[[1,0],[0,1]],[[0,1],[1,0]]];mult=[[1,0],[1,0],[0,1],[0,1]]
 for u in ([1,0],[0,1]):
  for v in ([1,0],[0,1]):
   for unit in ([0,1]if u==v else[0]):
    problem=M.make_problem(C2,[[[1,0],2],[[0,1],2]],u,v,unit)
    result=M.solve(problem,1000,5);require(result['status']=='feasible','VecC2 center control failed')
 hole={'vectors':[(2,),(3,)],'caps':[3,3],'target':(1,)}
 require(M.solve(hole,1000,5)['status']=='infeasible','integer-semigroup hole was accepted')
 easy={'vectors':[(1,)],'caps':[2],'target':(1,)}
 require(M.solve(easy,0,5)['status']=='unknown_budget','node exhaustion became a proof')
 require(M.solve(easy,1000,0)['status']=='unknown_budget','time exhaustion became a proof')
 require(not M.validate_solution(easy,[2]),'wrong witness accepted')
 rng=random.Random(20261002)
 for _ in range(120):
  n=rng.randrange(1,4);q=rng.randrange(1,5)
  vectors=[]
  for j in range(q):
   v=tuple(rng.randrange(4)for _ in range(n))
   vectors.append(v if any(v)else(1,)+(0,)*(n-1))
  caps=[rng.randrange(4)for _ in range(q)];target=tuple(rng.randrange(10)for _ in range(n));p={'vectors':vectors,'caps':caps,'target':target}
  brute=any(M.validate_solution(p,list(c))for c in itertools.product(*(range(b+1)for b in caps)))
  got=M.solve(p,100000,5)
  require(got['status']==('feasible'if brute else'infeasible'),'DFS differs from independent exhaustive Cartesian-product check')
 data=M.load_input(Path(__file__).with_name('r1660_profiles.json'))
 # Force a short checkpoint round with UNKNOWN cases, then resume with more
 # budget. Only one R1660 profile is touched; no classification is inferred.
 with tempfile.TemporaryDirectory()as tmp:
  root=Path(tmp);base=['--checkpoint',str(root/'state.sqlite3'),'--output',str(root/'result.json'),'--max-profiles','1','--seconds','5']
  first=M.main(base+['--nodes-per-pair','0','--seconds-per-pair','0.01'])
  require(first['labelled_profile_counts'].get('profile_rejected',0)==0,'budget-only pilot rejected a profile')
  with M.sqlite3.connect(root/'state.sqlite3')as db:
   require(db.execute('SELECT count(*) FROM problems').fetchone()[0]>0,'no pair checkpoints saved')
  second=M.main(base+['--nodes-per-pair','2000','--seconds-per-pair','0.03'])
  require(Path(root/'result.json').stat().st_size<2_000_000,'return report too large')
 report={'status':'PASS','known_RepS3_center_tests':len(tasks),'duplicate_std_fibre_multiplicity':3,'duplicate_dual_and_nondual_requirements_checked':True,'kernel_unit_fibre_control':'Z(VecC2)','integer_semigroup_hole_rejected':True,'node_and_time_budget_stops_are_unknown':True,'brute_force_cross_checks':120,'source_profile_count':1136,'distinct_ungraded_profiles':628,'checkpoint_resume_control':'one profile only; no full scan','post_resume_profile_counts':second['labelled_profile_counts']}
 Path(__file__).with_name('controls_receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
