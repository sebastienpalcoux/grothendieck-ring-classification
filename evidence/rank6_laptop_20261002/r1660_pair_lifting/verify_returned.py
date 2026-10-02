"""Reconstruct and replay candidate profile obstructions in a returned JSON file."""
import argparse,json
from pathlib import Path
import run_r1660 as M

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('report',type=Path);p.add_argument('--seconds-per-pair',type=float,default=60)
 p.add_argument('--nodes-per-pair',type=int,default=2000000)
 p.add_argument('--output',type=Path,default=Path('r1660_replay.json'))
 a=p.parse_args();data=M.load_input(Path(__file__).with_name('r1660_profiles.json'))
 report=json.loads(a.report.read_text())
 M.require(report.get('input_sha256')==M.EXPECTED_INPUT_SHA,'returned input hash differs')
 M.require(report.get('algorithm')==M.ALGORITHM,'returned algorithm differs')
 profiles={p['key']:p for p in data['profiles']};seen=set();results=[]
 for record in report['profiles']:
  key=record['profile_key'];M.require(key in profiles and key not in seen,'unknown or repeated profile key');seen.add(key)
  source=profiles[key];M.require(record['aliases']==source['aliases'],'source profile aliases differ')
  if record['status']!='profile_rejected':continue
  claim=record['obstruction'];matches=[j for j in M.jobs(data['tensor'],source['columns'])if j['u']==claim['u']and j['v']==claim['v']and j['unit_coefficient']==claim['unit_coefficient']]
  M.require(len(matches)==1,'candidate is not a selected necessary problem');job=matches[0]
  M.require(claim['problem_key']==job['problem_key'],'candidate problem key differs')
  M.require(M.encode(claim['bounded_system'])==M.encode(job['problem']),'candidate bounded system differs')
  M.require(claim['restriction_multiplicities']==source['columns'],'candidate multiplicities differ')
  result=M.solve(job['problem'],a.nodes_per_pair,a.seconds_per_pair)
  results.append({'profile_key':key,'aliases':source['aliases'],'status':result['status'],'nodes':result['nodes']})
  M.require(result['status']!='feasible','claimed obstruction has a feasible witness')
 M.require(seen==set(profiles),'returned report does not cover all profile keys')
 answer={'status':'REPLAYED_CANDIDATES'if all(r['status']=='infeasible'for r in results)else'UNKNOWN_BUDGET',
         'candidate_count':len(results),'results':results,
         'scope':'Replays only candidate finite systems; does not certify profile completeness or category exclusion.'}
 a.output.write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps(answer,indent=2))
if __name__=='__main__':main()
