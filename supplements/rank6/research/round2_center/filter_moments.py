"""Exact low-row moment filters on every exhaustive integral Gram frame."""
import json,sys,itertools,math,time
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import modular_character_induction as I
from augmented_spectrum import AugmentedSpectrum
from exact import require
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')
d,tab=I.reciprocity_data(R);K=tab.K
src=json.loads(Path(__file__).with_name('all_frames.json').read_text());output=[];stats={};start=time.monotonic()
def ratcoords(z):
 c=list(reversed(z.to_list()));return [Q(str(x)) for x in c]+[Q(0)]*(K.mod.degree()-len(c))
def linear_row(zs):
 cc=[ratcoords(z) for z in zs];dd=math.lcm(*(x.denominator for z in cc for x in z));return [[int(z[k]*dd) for z in cc] for k in range(K.mod.degree())],dd
def evalrow(row,x):
 aa,den=row;zz=[sum(a*b for a,b in zip(v,x)) for v in aa];return zz,den
for branch in src['branches']:
 ff=branch.get('gram_frames',[])
 if not ff:continue
 ix=branch['index'];low=list(map(tuple,branch['low']));high=[(0,)+tuple(v) for v in branch['high']];vs=low+high
 _,hi=I.high_columns(d,I.s.Matrix.hstack(*map(I.s.Matrix,low)));sp=AugmentedSpectrum(tab,low,hi);tys=dict(zip(sp.vectors,sp.types));weights=[tab.dims[v]**2/tab.D**2 for v in vs]
 gb,gr=sp.balance([(v[1:],0) for v in high],len(high))
 frames=[(i,f) for i,f in enumerate(ff) if all(sum(a*b for a,b in zip(row,f))==rhs for row,rhs in zip(gb,gr))]
 for lab in branch['labellings']:
  moment={}
  def calc(tup):
   tup=tuple(sorted(tup))
   if tup not in moment:moment[tup]=linear_row([weights[i]*math.prod(tys[v][lab[a]] for a in tup) for i,v in enumerate(vs)])
   return moment[tup]
  pairs=list(itertools.combinations_with_replacement(range(6),2));triples=list(itertools.combinations_with_replacement(range(1,6),3));squares=[p+p for p in itertools.combinations_with_replacement(range(1,6),2)]
  for tup in pairs+triples+squares:calc(tup)
  survived=[];why={}
  for fi,f in frames:
   x=[1]*6+f;failure=None
   for a,b in pairs:
    zz,den=evalrow(calc((a,b)),x)
    if zz!=[den*int(a==b),0]:failure='orthogonality';break
   if failure is None:
    for abc in triples:
     zz,den=evalrow(calc(abc),x)
     if zz[1]!=0 or zz[0]<0 or zz[0]%den:failure='cubic_nonnegative_integrality';break
   if failure is None:
    for a,b in itertools.combinations_with_replacement(range(1,6),2):
     zz,den=evalrow(calc((a,b,a,b)),x)
     lp=[int(a==b)]+[evalrow(calc((a,b,c)),x)[0][0]//evalrow(calc((a,b,c)),x)[1] for c in range(1,6)]
     res=zz[0]-den*sum(t*t for t in lp)
     if zz[1]!=0 or res<0 or res%den:failure='fourth_diagonal_nonnegative_integrality';break
   if failure is None:survived.append(fi)
   else:why[failure]=why.get(failure,0)+1
  output.append({'index':ix,'labelling':lab,'galois_frames':[i for i,f in frames],'moment_survivors':survived,'failure_counts':why})
  print(ix,lab,'input',len(ff),'Galois',len(frames),'moment',len(survived),why,flush=True)
  Path(__file__).with_name('moments_partial.json').write_text(json.dumps(output,separators=(',',':'))+'\n')
Path(__file__).with_name('moments.json').write_text(json.dumps({'complete':True,'cases':output,'seconds':time.monotonic()-start},separators=(',',':'))+'\n')
print('COMPLETE',time.monotonic()-start,flush=True)
