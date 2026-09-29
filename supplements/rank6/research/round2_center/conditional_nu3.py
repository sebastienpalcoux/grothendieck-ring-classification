"""Conditional exact test: impose nu3(b4)=nu3(b5)=-1 on every low frame.
The numerical optimizer only discovers exact Farkas witnesses; survivors are
reported honestly and the categorical reason for the added hypothesis is NOT
asserted by this script.
"""
import json,sys,time,math,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import modular_character_induction as I
from augmented_spectrum import AugmentedSpectrum
from higher_traces import trace_types
from frontier_feasibility import rational_feasible
from exact import require
ap=argparse.ArgumentParser();ap.add_argument('--height',type=int,default=3);ap.add_argument('--nu3',type=int,default=-1);ap.add_argument('--objects',type=int,nargs='+',default=[4,5]);args=ap.parse_args();tag=f"conditional_nu3_{args.nu3}_h{args.height}_objects{''.join(map(str,args.objects))}"
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')
d,tab=I.reciprocity_data(R);K=tab.K
src=json.loads(Path(__file__).with_name('all_frames.json').read_text());out=[];start=time.monotonic()
types,_=trace_types(d['q'],d['primes'],args.height);sq=K.from_sympy(I.s.sqrt(d['q']));third=[K(t[2][0])+K(t[2][1])*sq for t in types]
for branch in src['branches']:
 if not branch.get('labellings'):continue
 low=list(map(tuple,branch['low']));L=I.s.Matrix.hstack(*map(I.s.Matrix,low));_,hi=I.high_columns(d,L);sp=AugmentedSpectrum(tab,low,hi);forbidden=set(map(tuple,sp.forbidden))
 for lab in branch['labellings']:
  for ep in I.indicator_choices(R):
   A,b,meta=I.equation_system(R,d,tab,low,ep,args.height,lab,sp)
   _,_,rot=I.system_rotation(R,d,L,ep,args.height);labels=rot['labels'];keep=[j for j in range(len(A[0])+sum(tuple(v) in forbidden for v,ti in labels)) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
   require(len(keep)==len(A[0]),'keep mismatch')
   for obj in args.objects:
    rhs=K(args.nu3)*tab.D-sum((K(v[obj])*tab.dims[v] for v in low),K.zero)
    coeff=[K(labels[j][0][obj-1])*tab.dims[(0,)+tuple(labels[j][0])]*third[labels[j][1]] if j<len(labels) else K.zero for j in keep]
    for row,val in I.rational_rows(coeff,rhs,K):A.append(row);b.append(val)
   rec={'index':branch['index'],'labelling':lab,'indicators':list(ep)}
   y=I.farkas(A,b)
   if y is not None:rec['common_y']=y;rec['bTy']=sum(a*z for a,z in zip(b,y));print(branch['index'],lab,ep,'ALL EXCLUDED',flush=True)
   else:
    cases=[]
    for fi,frame in enumerate(branch['gram_frames']):
     count=dict(zip(map(tuple,branch['high']),frame));used=[p for p,j in enumerate(keep) if j>=len(labels) or count[tuple(labels[j][0])]>0];AA=[[row[p] for p in used] for row in A];bb=list(b)
     for v,c in count.items():
      if c:AA.append([int(keep[p]<len(labels) and tuple(labels[keep[p]][0])==v) for p in used]);bb.append(c)
     yy=I.farkas(AA,bb)
     if yy is not None:cases.append({'frame':fi,'y':yy})
     else:
      xx=rational_feasible(AA,bb);cases.append({'frame':fi,'primal':xx});print('SURVIVOR',branch['index'],lab,ep,fi,'rank',6+sum(frame),'exact primal',xx is not None,flush=True)
    rec['cases']=cases
   out.append(rec);Path(__file__).with_name(tag+'_partial.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
Path(__file__).with_name(tag+'.json').write_text(json.dumps({'complete':True,'conditional_nu3':args.nu3,'height':args.height,'objects':args.objects,'cases':out,'seconds':time.monotonic()-start},separators=(',',':'))+'\n')
print('COMPLETE',time.monotonic()-start,flush=True)
