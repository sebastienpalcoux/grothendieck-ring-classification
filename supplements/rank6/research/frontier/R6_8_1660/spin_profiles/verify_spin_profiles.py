"""Portable exact refinement of the 1727-profile R6_8_1660 frontier.

Uses the prior portable fermion certificate as a replayed prerequisite.
Adds normal-fiber even parity from alpha and homogeneous-packet AMV mod 3,
combined with the sixteenth-indicator field obstruction. Standard library.

python -O verify_spin_profiles.py --package /path/to/Rank6_Categorification_M8
Use --write to regenerate the adjacent small receipt.
"""
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
from functools import lru_cache
HERE=Path(__file__).resolve().parent

def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load_prior(package):
 folder=package/'research/frontier/R6_8_1660/fermion_profiles'
 script=folder/'verify_fermion_profiles.py'
 spec=importlib.util.spec_from_file_location('prior_fermion_verifier',script)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 certificate=folder/'fermion_profiles_certificate.json'
 stored=json.loads(certificate.read_text())
 require(module.reconstruct(package)==stored,'prior exact frontier replay failed')
 require(stored['surviving_count']==1727,'wrong prerequisite frontier')
 return module,stored,script,certificate

@lru_cache(None)
def residues(gs,fixed):
 if gs is None:return ()
 states={(0,0,0,0,0)};N=A=Q=0
 for n,a,b,asym,nonselfdual,_,sigmaX in gs:
  N+=n*(2 if asym else 1);cap=n if asym else n//2
  if asym:A+=n
  else:Q+=cap
  nxt=set();step=2 if(asym or nonselfdual)else 1
  for x,y,E,Ea,T in states:
   for e in range(0,cap+1,step):
    xx=x+a*e;yy=y+b*e
    if xx>180 or yy>120:break
    nxt.add((xx,yy,E+e,Ea+(e if asym else 0),(T+e*sigmaX*sigmaX)%3))
  states=nxt
 c=2 if fixed else 3
 return tuple(sorted({T for x,y,E,Ea,T in states if(x,y)==(180,120)and N-2*E-2*(N-3*E-c)>=0 and A-Ea<=N-3*E-c<=A+Q-E}))
@lru_cache(None)
def independent(gs,fixed,target):
 if gs is None:return False
 opts=[]
 for n,a,b,asym,nonselfdual,_,sigmaX in gs:
  choices=set()
  for e in range((n if asym else n//2)+1):
   if(asym or nonselfdual)and e%2:continue
   if asym:choices.add((e*a,e*b,2*e-n,e*sigmaX*sigmaX%3))
   else:
    for o in range((n-2*e)//2+1):
     f=n-2*e-2*o
     if nonselfdual and f%2:continue
     choices.add((e*a,e*b,e-o-f,e*sigmaX*sigmaX%3))
  opts.append(tuple(choices))
 bounds=[]
 for k in range(len(opts)+1):
  tail=opts[k:];bounds.append((sum(min(z[2]for z in g)for g in tail),sum(max(z[2]for z in g)for g in tail),sum(max(z[0]for z in g)for g in tail),sum(max(z[1]for z in g)for g in tail)))
 @lru_cache(None)
 def search(k,a,b,r,t):
  lo,hi,ma,mb=bounds[k]
  if a<0 or b<0 or a>ma or b>mb or r<lo or r>hi:return False
  if k==len(opts):return(a,b,r)==(0,0,0)and(target is None or t==target)
  return any(search(k+1,a-x,b-y,r-z,(t+tt)%3)for x,y,z,tt in opts[k])
 return search(0,180,120,-(2 if fixed else 3),0)

def validate_packet_constants(module,columns,vectors):
 up=tuple(sum(v[i]for v in columns[:4])for i in range(6))
 um=tuple(sum(v[i]for v in columns[4:])for i in range(6))
 require(up==(4,0,6,6,0,8)and um==(2,2,6,6,0,8),'packet restrictions changed')
 base=[0]*6
 delta=[0]*6
 for v in columns[:4]:
  fv=(v[1],v[0],v[3],v[2],v[4],v[5])
  for w in (v,fv):
   a=sum(x*y for x,y in zip(w,um))
   for i in range(6):base[i]+=a*w[i];delta[i]+=(2*w[0]-2*w[1])*w[i]
 require(tuple(base)==(144,144,648,648,0,848),'base packet cube coefficients changed')
 require(tuple(delta)==(8,-8,0,0,0,0),'packet cube difference changed')
 # Every sigma-containing normal high type has b=3, so its contribution
 # to H_even u_minus vanishes modulo 3 and its known twist order divides16.
 for v in vectors:
  if v[3]:require(v[0]==0 and v[3]==1 and v[4]==3,'unexpected Ising-root type')
 # sigmaX has a nonzero sqrt3 part, hence is not in Q(zeta16).
 d=module.DIMS[5]
 require(d==(4,3,2,2)and d!=(d[0],d[1],-d[2],-d[3]),'FS16 field obstruction failed')

def reconstruct(package):
 module,cut,prior_script,prior_certificate=load_prior(package)
 oldpath=package/'research/round5/m8_actual48/certificate.json'
 old=json.loads(oldpath.read_text());out=[];checks=0
 sources={str(prior_script.relative_to(package)):digest(prior_script),str(prior_certificate.relative_to(package)):digest(prior_certificate),str(oldpath.relative_to(package)):digest(oldpath)}
 for branch in cut['branches']:
  prior=next(z for z in old['branches']if z['outcome']=='profile_frontier'and z['low']==branch['low']and z['labelling']==branch['labelling'])
  path=package/prior['source'];require(digest(path)==prior['source_sha256'],'source profile hash changed');sources[prior['source']]=digest(path)
  raw=json.loads(path.read_text())['branches'][0]
  case=next(c for c in raw['cases']if c['labelling']==branch['labelling'])
  V=tuple(map(tuple,raw['high_vectors']));L=tuple(map(tuple,raw['columns']))
  validate_packet_constants(module,L,V)
  bad=set(branch['fermion_orbit_rejected']+branch['center_fs_congruence_rejected'])
  inputs=[i for i in prior['unresolved']if i not in bad]
  require(len(inputs)==branch['surviving_count'],'prior surviving count differs')
  require(hashlib.sha256(json.dumps(inputs,separators=(',',':')).encode()).hexdigest()==branch['surviving_indices_sha256'],'prior surviving index binding differs')
  alpha_bad=[];amv_bad=[];survivors=[]
  for index in inputs:
   profile=case['profiles'][index];gs=module.orbit_groups(L,V,tuple(profile))
   supplier=any(profile[j]and v[0]==0 and v[3]==0 and v[4]>0 and v[4]%3==0 for j,v in enumerate(V))
   rr=set()
   for fixed in ((False,True)if prior['low']==1 else(False,)):
    r=residues(gs,fixed);rr.update(r)
    passed=bool(r and(supplier or 1 in r))
    if not passed:
     require(not independent(gs,fixed,None if supplier else 1),'independent charge recursion disagrees');checks+=1
   if not rr:alpha_bad.append(index)
   elif not supplier and 1 not in rr:amv_bad.append(index)
   else:survivors.append(index)
  out.append(dict(low=branch['low'],labelling=branch['labelling'],input_count=len(inputs),alpha_even_rejected=alpha_bad,amv_fs16_rejected=amv_bad,surviving_count=len(survivors),surviving_indices_sha256=hashlib.sha256(json.dumps(survivors,separators=(',',':')).encode()).hexdigest()))
 require(len(out)==3,'wrong branch coverage')
 return dict(status='necessary_reduction_only_original_unresolved',exact=True,optimizer_used=False,conservative_low_one_actions=['swap','two_fixed'],source_sha256=sources,branches=out,input_count=sum(b['input_count']for b in out),alpha_even_exclusions=sum(len(b['alpha_even_rejected'])for b in out),amv_fs16_exclusions=sum(len(b['amv_fs16_rejected'])for b in out),surviving_count=sum(b['surviving_count']for b in out),independently_rechecked_rejected_charge_branches=checks)

def locate(explicit):
 if explicit:return Path(explicit).resolve()
 for root in (Path.cwd(),HERE,*HERE.parents,*Path.cwd().parents):
  for p in (root,root/'work_round8/Rank6_Categorification_M8'):
   if(p/'research/frontier/R6_8_1660/fermion_profiles/verify_fermion_profiles.py').is_file():return p
 raise RuntimeError('Supply --package /path/to/Rank6_Categorification_M8')

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--package');parser.add_argument('--certificate',type=Path,default=HERE/'spin_profiles_certificate.json');parser.add_argument('--write',action='store_true');args=parser.parse_args()
 start=time.time();result=reconstruct(locate(args.package))
 if args.write:args.certificate.write_text(json.dumps(result,indent=2)+'\n')
 else:require(result==json.loads(args.certificate.read_text()),'spin certificate differs from exact reconstruction')
 print(json.dumps(dict(passed=True,input_count=result['input_count'],alpha_even_exclusions=result['alpha_even_exclusions'],amv_fs16_exclusions=result['amv_fs16_exclusions'],surviving_count=result['surviving_count'],optimizer_used=False,seconds=round(time.time()-start,4))))
if __name__=='__main__':main()
