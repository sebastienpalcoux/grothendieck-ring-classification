# Locate the enclosing frozen release or the explicitly supplied base.
import os as _task_os
from pathlib import Path as _TaskPath
def _find_release():
    if _task_os.environ.get("RANK6_PACKAGE"):
        return _TaskPath(_task_os.environ["RANK6_PACKAGE"]).resolve()
    for _p in _TaskPath(__file__).resolve().parents:
        for _c in (_p, _p / "Rank6_Categorification_M9"):
            if (_c / "software/round3_m4.py").is_file() and (_c / "data/census.json").is_file():
                return _c
    raise FileNotFoundError("Set RANK6_PACKAGE to the extracted multiplicity-nine package")
_TASK_PACKAGE = _find_release()

"""Exact signed-Galois / fermion-orbit audit of the frozen 1670 profiles.

No optimizer or center fusion enumeration. Writes only outside the package.
Run: python -O two_final/r1660_galois/verify.py --write
"""
import argparse, hashlib, importlib.util, json, time
from pathlib import Path
from functools import lru_cache
from collections import Counter
HERE=Path(__file__).resolve().parent
B5=((1,0,0,0,0,0),(0,1,0,0,0,0),(2,2,-1,-2,-2,2),
    (2,2,-2,-1,-2,2),(0,0,0,0,-1,0),(2,2,-2,-2,-4,3))

def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def jsondigest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def signed_map(v):
 w=tuple(sum(a*b for a,b in zip(row,v))for row in B5)
 if all(x>=0 for x in w):return 1,w
 if all(x<=0 for x in w):return -1,tuple(-x for x in w)
 raise RuntimeError('mixed-sign Galois image: '+str(v))
def swap(v):return(v[0],v[2],v[1],v[3],v[4])
def gal(v):return signed_map((0,)+v)[1][1:]

def validate_signed_matrix(f):
 """All 36 exact equations f_l sigma(chi_l(b))=sigma(f_l) chi_l(B5 b)."""
 zero=(0,0,0,0);one=f.ONE;negative=(-1,0,0,0);chars=[]
 for s in (1,-1):
  for t in (1,-1):
   x=(3,2*s,2*t,s*t);q=(0,s,0,0)
   chars.append((one,one,x,x,q,f.field_mul(q,x)))
 chars.extend(((one,negative,one,negative,zero,zero),(one,negative,negative,one,zero,zero)))
 sg=lambda x:(x[0],-x[1],-x[2],x[3])
 for ch in chars:
  fc=zero
  for x in ch:fc=f.field_add(fc,f.field_mul(x,x))
  for j in range(6):
   value=zero
   for i in range(6):value=f.field_add(value,f.field_scale(B5[i][j],ch[i]))
   require(f.field_mul(value,sg(fc))==f.field_mul(sg(ch[j]),fc),'signed S-row identity failed')
 for i in range(6):
  for j in range(6):require(sum(B5[i][k]*B5[k][j]for k in range(6))==int(i==j),'B5 is not involutive')
 return 36

def groups(L,V,profile):
 counts=list(profile);lookup={v:i for i,v in enumerate(V)}
 for v in L[:4]:
  k=(v[0],v[3],v[2],v[4],v[5]);require(k in lookup,'missing forced partner');counts[lookup[k]]-=1
 require(min(counts)>=0,'negative residual multiplicity')
 d={};seen=set()
 for i,v in enumerate(V):
  if not counts[i]or i in seen:continue
  require(v[0]==0,'unexpected residual g coefficient')
  j=lookup.get(swap(v));require(j is not None and counts[j]==counts[i],'h pairing failed')
  seen.update((i,j));n=counts[i];asym=i!=j;q=v[1]+v[2];t=v[4];non=bool(v[3])
  weight=(36,24)if non else(q*q+2*t*t,2*q*t)
  d[min(v,swap(v))]=(n,weight[0],weight[1],asym,non,q,t)
 return tuple(sorted(d.items()))

def blocks_from(gitems):
 d=dict(gitems);seen=set();blocks=[]
 for k,g in gitems:
  if k in seen:continue
  n,a,b,asym,non,q,t=g;kk=min(gal(k),swap(gal(k)))
  require(kk in d,'missing Galois partner')
  keys=tuple(sorted({k,kk}));seen.update(keys);gg=[d[j]for j in keys]
  require(len({(x[0],x[3],x[4])for x in gg})==1,'Galois partners disagree in multiplicity or h-type')
  cap=n if asym else n//2;step=2 if(asym or non)else 1;opts=[]
  for e in range(0,cap+1,step):
   for o in ((n-e,)if asym else range((n-2*e)//2+1)):
    t=0 if asym else n-2*e-2*o
    if non and n%4:continue
    if non and(o%2 or t%4):continue
    option=(sum(x[1]for x in gg)*e,sum(x[2]for x in gg)*e,len(gg)*(e-o-t),sum(x[6]**2 for x in gg)*e%3,e,o,t)
    opts.append(option)
  blocks.append((keys,tuple(opts)))
 return tuple(blocks)

@lru_cache(None)
def witness(gitems,fixed,needres):
 blocks=blocks_from(gitems);states={(0,0,0,0):()}
 for keys,opts in blocks:
  nxt={}
  for (x,y,r,s),path in states.items():
   for j,(a,b,rr,t,e,o,ff)in enumerate(opts):
    if x+a<=180 and y+b<=120:nxt.setdefault((x+a,y+b,r+rr,(s+t)%3),path+(j,))
  states=nxt
 for state,path in states.items():
  x,y,r,s=state
  if(x,y,r)==(180,120,-(2 if fixed else 3))and(not needres or s==1):return path
 return None

def check_witness(gitems,fixed,needres,path):
 """Direct check of the returned individual group counts; no DP replay."""
 blocks=blocks_from(gitems);require(len(path)==len(blocks),'wrong witness length');d=dict(gitems);values={}
 for(keys,opts),j in zip(blocks,path):
  _,_,_,_,e,o,t=opts[j]
  for k in keys:values[k]=(e,o,t)
 A=B=R=residue=0
 for k,(n,a,b,asym,non,q,tt)in gitems:
  e,o,t=values[k]
  require(min(e,o,t)>=0,'negative orbit count')
  require(n==e+o and t==0 if asym else n==2*e+2*o+t,'wrong h count')
  require(not(asym or non)or e%2==0,'fiber parity failed')
  require(not non or(n%4==0 and o%2==0 and t%4==0),'sigma fiber/fixed-set divisibility failed')
  require(values[min(gal(k),swap(gal(k)))]==(e,o,t),'Galois orbit counts disagree')
  A+=e*a;B+=e*b;R+=e-o-t;residue+=e*tt*tt
 require((A,B,R)==(180,120,-(2 if fixed else 3)),'dimension/rank equation failed')
 require(not needres or residue%3==1,'old AMV residue failed')
 return [[list(k),*values[k]]for k in sorted(values)]

def profile133_proof(P):
 """Independent elementary exhaustion: two even-sector choices only."""
 raw=json.loads((P/'research/round5/m8_1660/low0_profiles.json').read_text())['branches'][0]
 case=next(c for c in raw['cases']if c['labelling']==[0,5,4,1,3,2])
 g=dict(groups(tuple(map(tuple,raw['columns'])),tuple(map(tuple,raw['high_vectors'])),case['profiles'][133]))
 expected={(0,0,0,0,1):2,(0,1,1,0,2):2,(0,2,2,0,2):1,(0,2,2,0,3):2,(0,2,2,1,3):8,(0,4,4,0,4):2,(0,4,4,0,8):1}
 require({k:v[0]for k,v in g.items()}==expected,'profile133 residual types changed')
 patterns=[]
 for a in range(2):
  for b in range(2):
   for z in (0,2,4):
    for c in range(2):
     if 3*a+b+3*z+8*c!=15:continue
     ranks=set()
     # a controls both Galois-related multiplicity-two types.
     for oa in range(2-a):
      ta=2-2*a-2*oa
      for ob in range(2-b):
       tb=2-2*b-2*ob
       for oc in range(2-c):
        tc=2-2*c-2*oc
        for oz in range((8-2*z)//2+1):
         tz=8-2*z-2*oz
         if oz%2 or tz%4:continue
         ranks.add(2*(a-oa-ta)+(b-ob-tb)+(c-oc-tc)+(z-oz-tz)-2)
     require(-3 not in ranks,'independent rank contradiction failed')
     patterns.append(dict(e_a=a,e_b=b,e_sigma=z,e_c=c,possible_E_minus_O_minus_T=sorted(ranks)))
 require(len(patterns)==2,'expected exactly two even-sector patterns')
 return dict(low=0,labelling=[0,5,4,1,3,2],profile_index=133,required_E_minus_O_minus_T=-3,even_dimension_equation='3 e_a + e_b + 3 e_sigma + 8 e_c = 15',patterns=patterns)

def reconstruct(P):
 fp=P/'research/frontier/R6_8_1660/fermion_profiles/verify_fermion_profiles.py'
 sp=P/'research/frontier/R6_8_1660/spin_profiles/verify_spin_profiles.py'
 f=load(fp,'galois_prior_f');s=load(sp,'galois_prior_s');eqs=validate_signed_matrix(f)
 ap=P/'research/round5/m8_actual48/certificate.json';fcp=fp.with_name('fermion_profiles_certificate.json');scp=sp.with_name('spin_profiles_certificate.json')
 a=json.loads(ap.read_text());fc=json.loads(fcp.read_text());sc=json.loads(scp.read_text())
 require(s.reconstruct(P)==sc,'prior 1670-frontier replay failed')
 sources={str(p.relative_to(P)):digest(p)for p in(fp,sp,ap,fcp,scp)};out=[]
 for b in sc['branches']:
  old=next(x for x in a['branches']if x['outcome']=='profile_frontier'and x['low']==b['low']and x['labelling']==b['labelling'])
  fb=next(x for x in fc['branches']if x['low']==b['low']and x['labelling']==b['labelling'])
  source=P/old['source'];require(digest(source)==old['source_sha256'],'profile source hash changed');sources[old['source']]=digest(source)
  raw=json.loads(source.read_text())['branches'][0];case=next(x for x in raw['cases']if x['labelling']==b['labelling']);V=tuple(map(tuple,raw['high_vectors']));L=tuple(map(tuple,raw['columns']))
  bad=set(fb['fermion_orbit_rejected']+fb['center_fs_congruence_rejected']+b['alpha_even_rejected']+b['amv_fs16_rejected'])
  inds=[i for i in old['unresolved']if i not in bad]
  require(len(inds)==b['surviving_count']and jsondigest(inds)==b['surviving_indices_sha256'],'input frontier binding differs')
  reject=[];witnesses=[];sigmas=Counter();actions=Counter();signed_checks=0
  for i in inds:
   p=case['profiles'][i];g=groups(L,V,p)
   for v,n in zip(V,p):
    if n:
     sign,w=signed_map((0,)+v);require(signed_map(w)[1]==(0,)+v,'signed map inverse failed');signed_checks+=1
   sigmas[tuple(p[j]for j,v in enumerate(V)if v[3])]+=1
   supplier=any(p[j]and v[0]==0 and v[3]==0 and v[4]>0 and v[4]%3==0 for j,v in enumerate(V))
   found=False
   for fixed in((False,True)if b['low']==1 else(False,)):
    w=witness(g,fixed,not supplier)
    if w is not None:
     ww=check_witness(g,fixed,not supplier,w);witnesses.append([i,fixed,ww]);actions['two_fixed'if fixed else'low_swap']+=1;found=True;break
   if not found:reject.append(i)
  out.append(dict(low=b['low'],labelling=b['labelling'],input_count=len(inds),input_indices_sha256=jsondigest(inds),rejected=reject,surviving_count=len(inds)-len(reject),sigma_multiplicity_distributions=[dict(multiplicities=list(k),count=v)for k,v in sorted(sigmas.items())],witness_low_actions=dict(sorted(actions.items())),directly_checked_witnesses=len(witnesses),witnesses_sha256=jsondigest(witnesses),signed_restriction_checks=signed_checks))
 return dict(status='necessary_reduction_only_original_unresolved',exact=True,optimizer_used=False,center_fusion_enumerated=False,signed_matrix_B5=[list(x)for x in B5],exact_character_basis_identities=eqs,source_sha256=sources,branches=out,input_count=sum(b['input_count']for b in out),excluded_count=sum(len(b['rejected'])for b in out),surviving_count=sum(b['surviving_count']for b in out),criterion='Signed Galois5 restriction map; sigma-fiber and h-fixed-locus 4-divisibility, even sigma odd-pair counts; Galois-equivariant even/odd/fixed h-orbit counts, plus prior dimension, rank, alpha parity, and AMV/FS16 residue conditions.', independent_profile133_proof=profile133_proof(P))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',type=Path,default=_TASK_PACKAGE);p.add_argument('--write',action='store_true');p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');a=p.parse_args();t=time.time();r=reconstruct(a.package.resolve())
 if a.write:a.certificate.write_text(json.dumps(r,indent=2)+'\n')
 else:require(r==json.loads(a.certificate.read_text()),'receipt differs')
 print(json.dumps(dict(passed=True,input_count=r['input_count'],excluded_count=r['excluded_count'],surviving_count=r['surviving_count'],directly_checked_witnesses=sum(b['directly_checked_witnesses']for b in r['branches']),seconds=round(time.time()-t,4))))
if __name__=='__main__':main()
