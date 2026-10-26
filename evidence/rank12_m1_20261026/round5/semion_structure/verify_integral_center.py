#!/usr/bin/env python3
"""Exact six-profile reduction; categorical proof in companion note."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
T=[(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,2)]
profiles=[]
def rec(i,a,b,c,cs):
    if min(a,b,c)<0:return
    if i==len(T):
        if a==b==c==0:profiles.append(cs)
        return
    p,t=T[i];bounds=[16]
    if p:bounds.append(a//(p*p))
    if t:bounds.append(c//(t*t))
    if p*t:bounds.append(b//(p*t))
    for k in range(min(bounds)+1):rec(i+1,a-k*p*p,b-k*p*t,c-k*t*t,cs+[k])
rec(0,6,6,15,[])
if len(profiles)!=13:raise ValueError('complete profile count')
survivors=[i for i,cs in enumerate(profiles)if all(not n or t for(p,t),n in zip(T,cs))]
if survivors!=[1,2,7,8,11,12]:raise ValueError('survivor list')
out={'status':'PASS','ring':'R12_1_623','restriction_only':True,'new_exclusion':False,
     'profiles_before':13,'profiles_after':6,'surviving_indices':survivors,
     'surviving_profiles':[profiles[i]for i in survivors],'pair_types':T}
(P/'integral_center_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
