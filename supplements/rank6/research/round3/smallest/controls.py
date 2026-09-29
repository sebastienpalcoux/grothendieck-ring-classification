import sys,json,copy,time,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_smallest as C
from exact import require
from rings import permute
R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_4_6');c=json.load(open(Path(__file__).with_name('R6_4_6_certificate.json')))['certificate']
# No census identity participates in applicability. Check every based relabelling.
import itertools
count=0
for tail in itertools.permutations(range(1,6)):
 T=permute(R,(0,)+tail);f=C.family(T);require(f is not None and f['multiplicity']==4,'family recognition depends on basis labelling');count+=1
mutations={}
z=copy.deepcopy(c);z['family']['pointed_associator_class']=0;mutations['wrong_associator_class']=z
z=copy.deepcopy(c);z['modules']['representations']=[];mutations['omitted_module_branch']=z
z=copy.deepcopy(c);z['branches'].pop();mutations['omitted_low_frame']=z
z=copy.deepcopy(c);z['branches'][0]['cases'].pop();mutations['omitted_FS2_assignment']=z
z=copy.deepcopy(c);z['branches'][0]['cases'][0]['ray']=[0]*len(z['branches'][0]['cases'][0]['ray']);mutations['zero_separator']=z
z=copy.deepcopy(c);z['branches'][0]['cases'][0]['system']['forced_twist_removed']+=1;mutations['altered_twist_metadata']=z
records=[]
for name,z in mutations.items():
 start=time.time()
 try:C.verify(R,z)
 except Exception as e:records.append(dict(mutation=name,rejected=True,error=type(e).__name__+': '+str(e),seconds=time.time()-start))
 else:raise RuntimeError('mutation accepted: '+name)
print(json.dumps({'all120_based_relabellings':count,'mutations':records,'optimized':not __debug__}),flush=True)
Path(__file__).with_name('controls_optimized.json' if not __debug__ else 'controls_normal.json').write_text(json.dumps({'all120_based_relabellings':count,'mutations':records,'optimized':not __debug__},indent=2)+'\n')
