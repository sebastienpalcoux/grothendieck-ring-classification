"""Rebuild compact ungraded inputs from the frozen1136-profile repository evidence."""
import argparse,collections,hashlib,json
from pathlib import Path

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(value,message):
 if not value:raise ValueError(message)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--output',type=Path,default=Path(__file__).with_name('r1660_profiles.json'));a=p.parse_args()
 root=a.repository;package=root/'supplements/rank6';packetpath=root/'evidence/residual_20261002/rank6/packet_gram_probe_receipt.json';packet=json.loads(packetpath.read_text())
 sources={str(packetpath.relative_to(root)):hashlib.sha256(packetpath.read_bytes()).hexdigest()}
 census=package/'data/census.json';sources[str(census.relative_to(root))]=hashlib.sha256(census.read_bytes()).hexdigest();R=next(r['N']for r in json.loads(census.read_text())if r['id']=='R6_8_1660')
 data={};total=0
 for branch in packet['branches']:
  path=package/f"research/round5/m8_1660/low{branch['low']}_profiles.json";sources[str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest();raw=json.loads(path.read_text())['branches'][0];case=next(c for c in raw['cases']if c['labelling']==branch['labelling'])
  require(len(branch['survivors'])==branch['surviving_count'],'packet survivor count differs')
  for idx in branch['survivors']:
   counts=collections.Counter(map(tuple,raw['columns']))
   for v,m in zip(raw['high_vectors'],case['profiles'][idx]):
    if m:counts[(0,)+tuple(v)]+=m
   cols=[[list(v),m]for v,m in sorted(counts.items())];key=digest(cols)
   rec=data.setdefault(key,{'key':key,'columns':cols,'aliases':[]})
   rec['aliases'].append({'low':branch['low'],'labelling':branch['labelling'],'profile':idx});total+=1
 H=[[6,2,12,12,0,16],[2,6,12,12,0,16],[12,12,142,138,16,192],[12,12,138,142,16,192],[0,0,16,16,8,24],[16,16,192,192,24,280]]
 for rec in data.values():
  require(all(sum(m*v[i]*v[j]for v,m in rec['columns'])==H[i][j]for i in range(6)for j in range(6)),'profile restriction Gram differs')
 require(total==1136,'expected1136 labelled profiles')
 out={'format':1,'ring_id':'R6_8_1660','scope':'necessary ungraded profile test; categorification unresolved','base_order':['1','g','X','gX','sigma','T'],'tensor':R,'profile_count':total,'distinct_ungraded_profiles':len(data),'total_restriction_gram':H,'sources_sha256':sources,'profiles':list(data.values())}
 a.output.write_text(json.dumps(out,separators=(',',':'))+'\n');print(json.dumps({'profiles':total,'distinct_ungraded_profiles':len(data),'bytes':a.output.stat().st_size,'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
