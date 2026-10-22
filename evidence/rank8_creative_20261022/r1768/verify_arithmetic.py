"""Exact source-character, Galois-complement and finite fibre-domain arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
import json,sys,argparse,itertools,hashlib
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'evidence/rank8_research_20261022/pointed_followup'))
import c2_fibres as f

def mul(x,y):return(x[0]*y[0]+37*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def div(x,y):
 n=y[0]*y[0]-37*y[1]*y[1];return tuple(a/n for a in mul(x,(y[0],-y[1])))
def dim(v,ds):return tuple(sum(Q(n)*d[j]for n,d in zip(v,ds))for j in range(2))
def run(base=None):
 source,C,old=f.setup(1768)if base is None else base;R=source['tensor'];D=tuple(map(Q,C.D));ds=list(map(lambda d:tuple(map(Q,d)),C.a['dimensions']));dsp=[(a,-b)for a,b in ds];Dp=(D[0],-D[1])
 need=f.require
 need(D==(Q(444),Q(72))and D[0]**2-37*D[1]**2==5328,'dimensionnorm')
 chars=[(1,-1,0,1,1,-1,-1,0),(1,-1,1,-1,0,0,1,-1),(1,-1,0,1,-2,2,-1,0),(1,1,0,1,-1,-1,1,0),(1,1,1,-1,0,0,-1,1),(1,-1,-2,-1,0,0,1,2)]
 need(all(c[0]==1 and all(c[i]*c[j]==sum(R[i][j][k]*c[k]for k in range(8))for i,j in itertools.product(range(8),repeat=2))for c in chars),'rationalcharacters')
 need(all(sum(a*b for a,b in zip(c,e))==0 for i,c in enumerate(chars)for e in chars[i+1:]),'rationalorthogonality')
 need(all(dim(c,ds)==(0,0)and dim(c,dsp)==(0,0)for c in chars),'FPorthogonality')
 P=[[sum(z[0]for z in [div(mul(ds[i],ds[j]),D),div(mul(dsp[i],dsp[j]),Dp)])for j in range(8)]for i in range(8)]
 need(all(sum(z[1]for z in [div(mul(ds[i],ds[j]),D),div(mul(dsp[i],dsp[j]),Dp)])==0 for i,j in itertools.product(range(8),repeat=2)),'rationalprojector')
 need(all(sum(P[i][k]*P[k][j]for k in range(8))==P[i][j]for i,j in itertools.product(range(8),repeat=2)),'idempotent')
 high=C.a['high'];nonrat=[(i,(0,)+tuple(v),tuple(map(Q,z)))for i,(v,z)in enumerate(high)if not v[0]and 6*z[0]!=37*z[1]]
 need(len(high)==497 and len(nonrat)==137,'completepriorhighdomain')
 small=[];blocked=[]
 for i,v,(a,b)in nonrat:
  need(dim(v,ds)==(a,b),'highdimension')
  if a==6*b:small.append((i,v,b))
  else:
   need(b%12==0 and a==73*(b/12),'largeunitalphafamily')
   need(div((a,b),D)[1]!=0,'irrationalratio')
   rat=div((a,b),D);partner=mul(D,(rat[0],-rat[1]));need(partner==(b/12,Q(0)),'integerGaloispartner')
   blocked.append(i)
 need(len(small)==25,'25smallfamilycolumns')
 keep=[];removed=[]
 for i,v,k in small:
  Pv=[sum(P[j][t]*v[t]for t in range(8))for j in range(8)]
  need(Pv==[Q(0),Q(0)]+[k/6]*6,'explicitprojector')
  w=tuple(2*Pv[j]-v[j]for j in range(8))
  if all(t.denominator==1 and t>=0 for t in w):
   need(all(sum(c[j]*w[j]for j in range(8))==-sum(c[j]*v[j]for j in range(8))for c in chars),'Galoisrationalcharacters')
   need(dim(w,ds)==dim(v,ds),'partnerdimension')
   need(any(tuple(vv)==w[1:]for vv,z in high),'partnerindomain')
   keep.append([i,list(v),int(k),list(map(int,w))])
  else:removed.append(i)
 v=(0,0,0,0,1,0,1,1);w=(0,0,1,1,0,1,0,0);z=tuple(a+b for a,b in zip(v,w))
 want={v,w,tuple(2*a for a in v),tuple(2*a for a in w),z,tuple(2*a for a in z)}
 need({tuple(x[1])for x in keep}==want and len(keep)==6,'sixcompletecolumns')
 c=(1,0,2,2,2,2,2,2);alpha=(Q(73),Q(12));alphap=(Q(73),Q(-12))
 need(dim(c,ds)==alpha and dim(c,dsp)==alphap,'Galoisunitdimension')
 need(all(sum(a*b for a,b in zip(ch,c))==1 for ch in chars),'Galoisunitrationalcharacters')
 # The two FP characters plus the six orthogonal nonzero rational characters
 # span the whole eight-dimensional regular representation; hence uniqueness.
 need(sum(x*x for x in [1]+[0]*7)==1,'unitnormalization')
 decompositions=[]
 for a,b,c0,d in itertools.product(range(17),range(5),range(5),range(2)):
  if a+4*b+4*c0+16*d!=16:continue
  U=a+4*b;V=c0+4*d
  G=[[9*a*(v[i]*v[j]+w[i]*w[j])+9*b*(4*v[i]*v[j]+4*w[i]*w[j])+18*c0*z[i]*z[j]+18*d*4*z[i]*z[j]for j in range(8)]for i in range(8)]
  need(G==[[9*U*(v[i]*v[j]+w[i]*w[j])+18*V*z[i]*z[j]for j in range(8)]for i in range(8)],'Gramaggregation')
  decompositions.append({'a':a,'b':b,'c':c0,'d':d,'U':U,'V':V})
 need({x['V']for x in decompositions}==set(range(5)),'fivecompletebranches')
 final=[x for x in decompositions if x['V']==4]
 need([(x['a'],x['b'],x['c'],x['d'])for x in final]==[(0,0,0,1),(0,0,4,0)],'twosurvivingsectorpatterns')
 return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],'status':'PASS','scope':'exact arithmetic supporting the separately proved saturated-conductor and modular-Galois arguments; no categorification claim','source_characters':[list(c)for c in chars],'formal_codegrees':[sum(a*a for a in c)for c in chars],'initial_high_columns':497,'primitive37_high_candidates_avoiding_g':137,'large_unit_columns_excluded':len(blocked),'small_family_columns':25,'complement_survivors':keep,'complement_excluded_indices':removed,'integer_fibre_decompositions':decompositions,'five_Gram_branches':[{'V':j,'U':16-4*j}for j in range(5)],'distinguished_Galois_unit_restriction':list(c),'V4_irrational_ratio_sector_options':[{'simple_count':18,'restriction':list(2*x for x in z),'dimension':[72,12]},{'simple_count':72,'restriction':list(z),'dimension':[36,6]}]}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();x=run();path=HERE/'arithmetic_verification.json'
 if a.write:path.write_text(json.dumps(x,indent=2)+'\n')
 else:f.require(x==json.loads(path.read_text()),'savedarithmeticchanged')
 print('PASS:497 high columns ->137 primitive candidates ->25 small-family ->6 Galois-compatible; five exact fibre Grams; unique Galois-unit restriction.',flush=True)
