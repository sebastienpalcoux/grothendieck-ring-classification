"""Exact general-to-Galois-pseudo-unitary reduction for R6_3_215.

No nonexistence conclusion: all categorifications are shown to admit a
spherical structure and a pseudo-unitary Galois conjugate. Uses the existing
exhaustive oriented signed-sphericalization engine with unrestricted parity
domains, complete sign orbits, and exact norm tests.
"""
import argparse,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
from oriented_signed import enumerate_all,validate_general
from signed import from_values,gauge_original
from proofs import Characters,signed_component_certificate,check_signed_component
from exact import require,pc,ec

PATH=Path(__file__).with_suffix('.json')
R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_3_215')

def enumeration():
 vals,p,stats=enumerate_all(R,timeout=60,normalized=False)
 signs=[(1,)+z for z in itertools.product((-1,1),repeat=5)]
 factors=[tuple(eta[a]*eta[b]*eta[c] for orb in p['active'] for a,b,c in [orb[0]]) for eta in signs]
 groups={};allvalues=set(vals)
 for v in vals:
  orbit={tuple(x*y for x,y in zip(v,f)) for f in factors}
  require(orbit<=allvalues,'sign orbit leaves exhaustive signed solutions')
  rep=min(orbit);groups.setdefault(rep,[]).append(v)
 return vals,p,stats,groups

def produce():
 vals,p,stats,groups=enumeration();branches=[]
 for v,orbit in sorted(groups.items()):
  T=from_values(R,p,v);validate_general(T);g=gauge_original(T,R)
  b={'values':list(v),'orbit_size':len(orbit)}
  if g:b['gauge_original']=g
  else:
   require(all(T[i][j]==T[j][i] for i in range(6) for j in range(6)),'unexpected noncommutative signed branch')
   a=Characters(T);b['generator']=a.k;b['characters']=[]
   for f,m in a.components:
    w=signed_component_certificate(R,T,a,f,{})
    require(w is not None and w['kind'] in ('zero','norm'),'not an elementary arithmetic rejection')
    if w['kind']=='norm':w={'kind':'norm','polynomial':['1','-272','1088'],'prime':17}
    K,ds,delta,pD=a.component(f)
    b['characters'].append({'factor':pc(f),'global_dimension_polynomial':pc(pD),'obstruction':w})
  branches.append(b)
 a=Characters(R);chars=[]
 for f,m in a.components:
  K,ds,delta,pD=a.component(f);zero=next((i for i,d in enumerate(ds) if not d),None)
  chars.append({'factor':pc(f),'dimensions':[ec(d) for d in ds],'zero_object':zero})
 return {'id':'R6_3_215','claim':'Every complex fusion categorification admits a spherical structure and a pseudo-unitary Galois conjugate; existence remains unresolved.',
         'normalized_indicator_restrictions_used':False,'enumeration_statistics':stats,'all_values':[list(v) for v in vals],'branches':branches,'original_character_generator':a.k,'original_characters':chars}

def verify(c):
 vals,p,stats,groups=enumeration()
 require(c['normalized_indicator_restrictions_used'] is False,'unexpected normalization')
 require([list(v) for v in vals]==c['all_values'],'incomplete signed value domain')
 require(stats==c['enumeration_statistics'],'wrong signed enumeration statistics')
 require([list(v) for v in sorted(groups)]==[b['values'] for b in c['branches']],'incomplete signed orbit enumeration')
 gauges=0;zero=0;norm=0
 for v,b in zip(sorted(groups),c['branches']):
  require(b['orbit_size']==len(groups[v]),'wrong sign orbit size')
  T=from_values(R,p,v);validate_general(T)
  if 'gauge_original' in b:
   require(gauge_original(T,R)==b['gauge_original'],'incorrect sign gauge');gauges+=1
  else:
   a=Characters(T,b['generator'])
   require(len(a.components)==len(b['characters']),'missing signed character')
   for (f,m),cc in zip(a.components,b['characters']):
    K,ds,delta,pD=a.component(f)
    require(pc(f)==cc['factor'] and pc(pD)==cc['global_dimension_polynomial'],'wrong signed character field or dimension')
    w=cc['obstruction'];require(w['kind'] in ('zero','norm'),'unexpected arithmetic obstruction')
    check_signed_component(R,T,a,f,w)
    if w['kind']=='zero':zero+=1
    else:norm+=1
 a=Characters(R,c['original_character_generator'])
 require(len(a.components)==len(c['original_characters']),'incomplete original character list')
 good=[]
 for (f,m),cc in zip(a.components,c['original_characters']):
  K,ds,delta,pD=a.component(f)
  require(pc(f)==cc['factor'] and [ec(d) for d in ds]==cc['dimensions'],'wrong original character')
  z=cc['zero_object']
  if z is not None:require(not ds[z],'nonzero original character entry')
  else:
   require(all(ds),'zero entry in claimed spherical character')
   # This is exactly the FP quadratic orbit (1,1,d,d,d-1,d+1).
   d=ds[2]
   require(f.degree()==2 and ds==[K.one,K.one,d,d,d-K.one,d+K.one],'unexpected nonzero dimension character')
   require(d*d==8*d+K.one,'wrong quadratic relation')
   require(f==a.fp()[0],'not the FP component');good.append(f)
 require(len(good)==1,'more than one nonzero dimension orbit')
 require((gauges,zero,norm)==(1,228,43),'wrong signed branch tally')
 require(sum(b['orbit_size'] for b in c['branches'] if 'gauge_original' in b)==32,'wrong original gauge count')
 return {'id':'R6_3_215','signed_quotients':len(vals),'sign_orbits':len(groups),'gauge_original_orbits':gauges,'gauge_original_tables':32,
         'nongauge_zero_character_rejections':zero,'nongauge_norm_character_rejections':norm,
         'categorifications_spherical':True,'galois_pseudo_unitary':True,'categorification_asserted':False}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--generate',action='store_true');args=parser.parse_args()
 if args.generate:
  c=produce();report=verify(c);PATH.write_text(json.dumps(c,indent=2)+'\n')
 else:report=verify(json.load(open(PATH)))
 print(json.dumps(report))
