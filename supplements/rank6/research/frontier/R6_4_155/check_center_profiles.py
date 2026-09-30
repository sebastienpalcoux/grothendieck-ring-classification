"""Optimizer-free reconstruction of the six inherited centralizer profiles.
Reads only the certified high-column profiles, not packet/charge conclusions.
"""
from pathlib import Path
import sys,json,collections,argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('package',nargs='?',type=Path)
parser.add_argument('--verify',action='store_true',help='verify without writing a receipt')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[2]
nearby=next((p for p in Path(__file__).resolve().parents if (p/'data/unresolved_tensors.json').exists()),None)
P=(args.package or nearby or ROOT/'work_round6/Rank6_Categorification_M8').resolve()
sys.path.insert(0,str(P/'software'))
import round3_m4 as M
from exact import require
from round5_155 import semion_packet_frontier,split_centralizer_adjoint,verify_labelling_quotient
R=next(x['N']for x in json.load(open(P/'data/unresolved_tensors.json'))if x['id']=='R6_4_155')
cert=json.load(open(P/'research/round5/m4_155/frontier_certificate.json'))
d=M.data_for(R,3,8);cols=d['lows'][6];labs=d['tab'].assignments(cols)
verify_labelling_quotient(cols,labs);lab=labs[0]
expected={275:(30,16,14,2),277:(27,16,11,5),279:(24,16,8,8),296:(26,16,10,6),298:(23,16,7,9),306:(22,16,6,10)}
out=[]
for pi in expected:
 packet=semion_packet_frontier(R,d,cols,lab,cert['high_columns'],cert['profiles'][pi],4)
 require(packet['complete'],'incomplete semion packet domain')
 survivors=[]
 for oi,p in enumerate(packet['survivors']):
  split=split_centralizer_adjoint(R,d,cols,lab,p,4,3,-1)
  require(split['complete'],'incomplete charge split domain')
  for q in split['survivors']:
   eps=q['charges'];odd=[v for v,e in zip(p['W'],eps)if e==-1]
   nums=(len(eps),eps.count(1),eps.count(-1),sum(eps))
   require(nums==expected[pi],f'profile {pi}: unexpected ranks {nums}')
   ds=collections.Counter((sum(v[3:])+v[0],v[1]+v[2])for v in odd)
   survivors.append(dict(orientation=oi,rank=nums[0],even=nums[1],odd=nums[2],required_fixed=nums[3],odd_dimensions=[[list(k),v]for k,v in sorted(ds.items())],odd_restrictions=odd,trace_contradiction=nums[3]>nums[2]))
 require(len(survivors)==1,'unexpected centralizer survivors')
 out.append(dict(profile=pi,semion_orientations=len(packet['survivors']),survivors=survivors))
print(json.dumps(dict(verified=True,profiles=[dict(profile=x['profile'],**{k:v for k,v in x['survivors'][0].items()if k in ('rank','even','odd','required_fixed','trace_contradiction')})for x in out]),indent=2))
target=args.output or (None if args.verify else Path(__file__).with_name('center_profiles_exact.json'))
if target:target.write_text(json.dumps(out,indent=2)+'\n')
