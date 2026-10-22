#!/usr/bin/env python3
"""Refine the complete quartic phase domains by saturated dimension-block masks."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
FRONTIER=ROOT/'evidence/rank8_frontier_20261021'

def need(ok,msg):
 if not ok:raise ValueError(msg)

def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod

def mask(number):
 source=json.loads((FRONTIER/'quartic_integer_center/source.json').read_text())
 row=next(r for r in source['records'] if r['id']==f'R8_3_{number}')
 dims=[];allowed=[]
 for index,v in enumerate(row['canonical_high_vectors']):
  d=tuple(sum(F(c[j])*x for c,x in zip(row['full_characters'][0],[0]+v))for j in range(4))
  a,b,c,e=d;good=(a+b==3*c and a+2*b==6*e)
  dims.append([str(x)for x in d])
  if good:allowed.append(index)
 need(set(allowed)&set(range(40))=={12,23},'twist-one mask')
 return row,allowed,dims

def cosines24():
 # Relative traces from Q(zeta_24) to its real subfield Q(sqrt2,sqrt3).
 # The list is exact cos(m*pi/12), m=0,...,12; complete by symmetry.
 z=F(0);h=F(1,2);q=F(1,4)
 half=[(F(1),z,z,z),(z,q,z,q),(z,z,h,z),(z,h,z,z),(h,z,z,z),(z,-q,z,q),(z,z,z,z),
       (z,q,z,-q),(-h,z,z,z),(z,-h,z,z),(z,z,-h,z),(z,-q,z,-q),(-F(1),z,z,z)]
 cos=half+list(reversed(half[1:12]))
 need(len(cos)==24,'complete relative traces')
 return cos

def conductor_types(height):
 cos=cosines24()
 individual={f:{tuple(cos[(m*k)%24]for k in range(1,height+1))for m in range(0,24,24//f)}for f in (12,24)}
 paired={ratio:{f:{tuple(tuple(x+y for x,y in zip(cos[(m*k)%24],cos[((m+ratio)*k)%24]))for k in range(1,height+1))for m in range(0,24,24//f)}for f in (12,24)}for ratio in (6,12)}
 return individual,paired

def spectral_capacities():
 data=json.loads((HERE.parent/'unified/composite_verification.json').read_text())
 result={}
 for r in data['quartic_controls']:
  f=r['conductor'];minus=list(map(F,r['epsilon_minus_weights']));plus=list(map(F,r['epsilon_plus_weights']))
  for k in range(f//2+1):
   orbit=sorted({k,(-k)%f});a=sum(minus[i]for i in orbit);b=sum(plus[i]for i in orbit)
   need(a==b,'conjugate fibre capacity independent of mixture')
   result[f,k]=4*f*a
 return result

def run(number,write,conductor=False,spectral=False):
 row,allowed,dims=mask(number);path=HERE/f"R{number}_{'spectral'if spectral else 'conductor'if conductor else 'dimension'}_mask.json"
 saved=None if write else json.loads(path.read_text())
 cases=[]
 bounds=[]
 for d in dims:
  a,b,c,e=map(F,d);bounds.append(12 if a+b!=3*c else 24 if a+2*b!=6*e else 0)
 finite,paired=conductor_types(6)
 if number==928:
  sys.path.insert(0,str(FRONTIER/'r928_semion_rotation'))
  mod=load_module('pair_rotation_mask',FRONTIER/'r928_semion_rotation/pair_rotation.py')
  loaded=mod.setup();old=json.loads((FRONTIER/'r928_semion_rotation/pair_rotation.json').read_text())
  badtype=tuple((F(x),F(0),F(0),F(0))for x in (1,0,1,2,1,0))
  need(badtype in loaded[2],'phase pair containing one identified')
  bt=loaded[2].index(badtype)
  ordinary_types=mod.base.rotation.bq.trace_types(6)[0]
  raw_to_canonical={raw:canonical for canonical,raw in enumerate(row['original_high_order'])}
  labels=[]
  for raw in range(65):
   c=raw_to_canonical[raw]
   if c<40:labels.extend(('pair',c,ti)for ti in range(30))
   else:labels.extend(('individual',c,ti)for ti in range(38))
  indices=[c['metadata']['pattern_index']for c in old['cases']]
  build=lambda i:mod.build(loaded,i)
  lp=mod.base.lp
  def remove(label):
   kind,c,ti=label
   if kind=='auxiliary':return False
   if kind=='pair'and c not in allowed and ti==bt:return True
   if not conductor or not bounds[c]:return False
   if kind=='pair':return loaded[2][ti]not in paired[6][bounds[c]]
   return tuple(ordinary_types[ti])not in finite[bounds[c]]
 else:
  sys.path.insert(0,str(FRONTIER/'quartic_integer_center'))
  mod=load_module('r941_paired_mask',FRONTIER/'quartic_integer_center/r941_paired_rotation.py')
  loaded=mod.setup();old=json.loads((FRONTIER/'quartic_integer_center/r941_paired_rotation.json').read_text())
  indices=json.loads((FRONTIER/'review/r941_fusion_traces.json').read_text())['paired_surviving_allocations']
  types=mod.rotation.bq.trace_types(6)[0]
  one=next(i for i,t in enumerate(types)if t==tuple((F(1),F(0),F(0),F(0))for k in range(6)))
  minus=next(i for i,t in enumerate(types)if t==tuple((F((-1)**k),F(0),F(0),F(0))for k in range(1,7)))
  build=lambda i:mod.build(loaded,i)
  lp=mod.lp
  def remove(label):
   kind,c,ti=label
   if kind in ('rotation_auxiliary','auxiliary'):return False
   if c not in allowed and ((kind=='plus_pair'and ti in (one,minus))or(kind=='minus_individual'and ti==one)):return True
   if not conductor or not bounds[c]:return False
   if kind=='minus_individual':return tuple(types[ti])not in finite[bounds[c]]
   pair=tuple(tuple(x+y for x,y in zip(u,v))for u,v in zip(types[ti],types[loaded[4]['negative_phase_indices'][ti]]))
   return pair not in paired[12][bounds[c]]
 result={'id':f'R8_3_{number}','allowed_twist_one_high_indices':allowed,'high_dimensions':dims,'prior_indices':indices,'cases':cases,'saturated_conductor_support_applied':conductor,'all_conjugate_spectral_fibre_capacities_applied':spectral,'twist_order_bounds':bounds if conductor else None}
 for i in indices:
  A,b,meta=build(i)
  if number==941:labels=[loaded[2][j]for j in meta['selected_universal_columns']]
  labels_here=labels+[('auxiliary',-1,-1)]*(len(A[0])-len(labels))
  keep=[j for j,label in enumerate(labels_here)if not remove(label)]
  removed=[j for j in range(len(A[0]))if j not in keep]
  Ap=[[r[j]for j in keep]for r in A]
  if spectral:
   capacities=spectral_capacities();cos=cosines24();newrows=[];newrhs=[]
   lowdims=[tuple(sum(F(ch[k])*v for ch,v in zip(row['full_characters'][0],vec))for k in range(4))for vec in row['low_columns']]
   def masks(d):
    aa,bb,cc,dd=map(F,d);return {12:3*cc-aa-bb,24:6*dd-aa-2*bb}
   fixed=[(d,0)for d in lowdims]
   if number==941:fixed += [(dims[c],12 if at<4 else 0)for at,c in enumerate((40,41,42,43,57))]
   cache={}
   def coefficients(label):
    kind,c,ti=label
    if kind in ('auxiliary','rotation_auxiliary'):return {key:F(0)for key in capacities}
    L=masks(dims[c]);bound=bounds[c]
    if not bound:return {key:F(0)for key in capacities}
    ratio=6 if kind=='pair'else 12 if kind=='plus_pair'else None
    if number==928:typ=loaded[2][ti]if kind=='pair'else tuple(ordinary_types[ti])
    elif kind=='minus_individual':typ=tuple(types[ti])
    else:typ=tuple(tuple(x+y for x,y in zip(u,v))for u,v in zip(types[ti],types[loaded[4]['negative_phase_indices'][ti]]))
    ck=bound,ratio,typ
    if ck not in cache:
     matches=[]
     for m in range(0,24,24//bound):
      es=[m]if ratio is None else[m,(m+ratio)%24]
      tt=tuple(tuple(sum(cos[(e*k)%24][h]for e in es)for h in range(4))for k in range(1,7))
      if tt!=typ:continue
      cc={}
      for f,k in capacities:
       if f==12 and any(e%2 for e in es):cc[f,k]=None
       else:cc[f,k]=sum(min((e*f//24)%f,(-e*f//24)%f)==k for e in es)
      matches.append(cc)
     need(matches and all(x==matches[0]for x in matches),'unique finite conjugate-fibre counts')
     cache[ck]=matches[0]
    return {key:(L[key[0]]**2*cache[ck][key]if L[key[0]]else F(0))for key in capacities}
   co=[coefficients(labels_here[j])for j in keep]
   for key,cap in capacities.items():
    f,k=key;constant=cap
    for d,e in fixed:
     if min((e*f//24)%f,(-e*f//24)%f)==k:constant-=masks(d)[f]**2
    newrows.append([int(c[key])for c in co]);newrhs.append(int(constant))
   Ap+=newrows;b=list(b)+newrhs
  pm={'index':i,'removed':removed,'rows':len(Ap),'columns':len(keep),'matrix_sha256':hashlib.sha256(json.dumps(Ap,separators=(',',':')).encode()).hexdigest(),'rhs_sha256':hashlib.sha256(json.dumps(b,separators=(',',':')).encode()).hexdigest()}
  if write:
   prev=next(c for c in old['cases']if c['metadata'].get('pattern_index'if number==928 else 'allocation_index')==i)['decision']
   pp=[]if spectral else prev.get('primal',[])
   if not spectral and prev['status']=='exact_feasible_relaxation'and all(j in keep for j,v in pp):
    decision={'status':'exact_feasible_relaxation','primal':[[keep.index(j),v]for j,v in pp],'origin':'previous exact witness obeys new mask'}
   else:decision=lp.decide(Ap,b)
  else:
   need(saved['cases'][len(cases)]['metadata']==pm,'mask matrix binding')
   decision=saved['cases'][len(cases)]['decision']
  need(decision['status']in ('exact_feasible_relaxation','exact_infeasible_relaxation'),'exact decision required')
  lp.verify(Ap,b,decision)
  cases.append({'metadata':pm,'decision':decision})
  if write:path.write_text(json.dumps(result,indent=2)+'\n')
  print(number,i,'removed',len(removed),decision['status'],flush=True)
 result['scope']='Necessary twist-one dimension mask, optionally strengthened by saturated conductor support and all conjugate spectral-fibre capacities. Exact rational feasibility is not categorification.'
 if write:path.write_text(json.dumps(result,indent=2)+'\n')
 else:need(result==saved,'deterministic full mask replay')
 print('PASS',number,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--ring',type=int,choices=(928,941),required=True);p.add_argument('--write',action='store_true');p.add_argument('--conductor',action='store_true');p.add_argument('--spectral',action='store_true');a=p.parse_args();run(a.ring,a.write,a.conductor or a.spectral,a.spectral)
