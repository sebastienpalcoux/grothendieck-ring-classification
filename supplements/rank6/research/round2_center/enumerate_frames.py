"""Exhaust low induction frames and all pruned integral Gram decompositions."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import modular_character_induction as I
from augmented_spectrum import AugmentedSpectrum
from integer_gram import frames
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')
d,tab=I.reciprocity_data(R);out=[];start=time.monotonic()
for ix,cols in enumerate(d['lows']):
 rec={'index':ix,'low':[list(v) for v in cols]}
 why=I.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
 if why:rec['failure']=why;out.append(rec);continue
 aa=tab.assignments(cols);rec['labellings']=[list(v) for v in aa]
 if not aa:out.append(rec);continue
 Q,hi=I.high_columns(d,I.s.Matrix.hstack(*map(I.s.Matrix,cols)));sp=AugmentedSpectrum(tab,cols,hi);rec['spectrum']=sp.metadata()
 if sp.missing_low:out.append(rec);continue
 forbidden=set(map(tuple,sp.forbidden));hh=[(v,z) for v,z in hi if tuple(v) not in forbidden]
 ff=frames(Q,hh,30);rec['high']=[list(v) for v,z in hh];rec['gram_frames']=[list(v) for v in ff];out.append(rec)
 print(ix,'high',len(hh),'frames',len(ff),'lab',len(aa),'ranks',sorted(set(6+sum(f) for f in ff)),flush=True)
 (Path(__file__).with_name('all_frames_partial.json')).write_text(json.dumps(out,separators=(',',':'))+'\n')
(Path(__file__).with_name('all_frames.json')).write_text(json.dumps({'complete':True,'low_frames':len(out),'branches':out,'seconds':time.monotonic()-start},separators=(',',':'))+'\n')
print('COMPLETE',time.monotonic()-start,flush=True)
