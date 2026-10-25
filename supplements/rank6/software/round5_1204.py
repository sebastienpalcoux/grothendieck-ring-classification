"""Exact necessary-profile reduction for the rank-six quadratic frontier.

Canonical proof discovery is separate from replay. Replay performs only exact
arithmetic, bounded exhaustive enumeration, and integer certificates. Survivors
are necessary restriction profiles and are not categorifications.
"""
from native_build import ensure_native
import argparse,hashlib,itertools,json,math,os,subprocess,tempfile,time
from pathlib import Path
from fractions import Fraction
from collections import Counter
import sympy as s
import round3_m4 as M
from spectral_induction import Spectrum
from round4_quartic_profiles import word_forms,enumerate_affine,filter_profiles
from higher_traces import check_farkas
from modular_moments import check_congruence
from exact import require
ROOT=Path(__file__).resolve().parents[1]
PROOF=ROOT/'research/round5/m5_1204'

def digest(value):
 return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def native_executable():
 src=Path(__file__).with_suffix('.cpp');h=hashlib.sha256(src.read_bytes()).hexdigest()[:16];exe=Path(tempfile.gettempdir())/('rank6_joint_'+h)
 ensure_native(src,exe,flags=('-O3', '-std=c++17'))
 return exe
def build(R,d,i):
 cols=d['lows'][i];lab=d['tab'].assignments(cols)[0];G,vs=M.high_vectors(d,cols);sp=Spectrum(d['tab'],cols,[(v,None)for v in vs]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad]
 A=[[v[a]*v[b]for v in vs]for a in range(5)for b in range(a,5)];rhs=[int(G[a,b])for a in range(5)for b in range(a,5)];aa,bb=sp.balance([(v,None)for v in vs],len(vs));A+=aa;rhs+=bb;nv=len(vs)
 for word,forms in word_forms(d,cols,vs,sp,lab,3):
  for den,row in forms[1:]:
   if any(row):A.append(list(row[1:])+[0]*(len(A[0])-nv));rhs.append(-row[0])
  den,row=forms[0];A=[r+[0]for r in A];A.append(list(row[1:])+[0]*(len(A[0])-nv-1)+[-den]);rhs.append(-row[0])
 return A,rhs,vs,cols,lab,sp

def eq(A,b,bounds):
 n=len(A[0]);m=len(bounds);AA=[r+[0]*m for r in A];bb=list(b)
 for j,(v,sg,B) in enumerate(bounds):
  row=[0]*(n+m);row[v]=sg;row[n+j]=1;AA.append(row);bb.append(B)
 return AA,bb

def prepare(G):
 n=G.rows;r=G.rank();ix=[]
 for i in list(range(5))+sorted(range(5,n),key=lambda i:G[i,i]):
  if G.extract(ix+[i],ix+[i]).det():ix.append(i)
  if len(ix)==r:break
 vals=list(map(int,G))+ix
 # common-factor reduction of inverse numerator and denominator is exact.
 for k in range(1,r+1):
  S=G.extract(ix[:k],ix[:k]);det=int(S.det());aa=list(map(int,S.adjugate()));g=math.gcd(det,*aa);vals +=[det//g]+[x//g for x in aa]
 # native final map denominator must equal its final inverse denominator.
 S=G.extract(ix,ix);adj=S.adjugate();det=int(S.det());g=math.gcd(det,*map(int,adj));M=G.extract(range(n),ix)*(adj/g);vals+=list(map(int,M));vmax=math.isqrt(max(map(int,G.diagonal())));bound=max(abs(v)for v in vals)
 if bound>=2**60 or n*n*bound*vmax*vmax>=2**120:raise OverflowError('native integer bounds')
 return n,r,ix,vals

def native(pre,v):
 n,r,ix,vals=pre;fixed=[v[i]if i<5 else -1 for i in ix];st=time.monotonic();run=subprocess.run([str(native_executable())],input=' '.join(map(str,[n,r]+vals+fixed)),text=True,capture_output=True,check=True,timeout=30);out=sorted(tuple(map(int,line.split()))for line in run.stdout.splitlines());return out,time.monotonic()-st

def replay_bounds(A,b,c):
 bounds=[];upper=[None]*len(A[0]);lower=[0]*len(A[0])
 for rec in c['steps']:
  j,sg,B=rec['variable'],rec['sign'],rec['bound'];require(0<=j<len(A[0])and sg in[-1,1]and type(B)is int,'invalid integral bound')
  AA,bb=eq(A,b,bounds);T=[r+[0]for r in AA];row=[0]*(len(AA[0])+1);row[j]=sg;row[-1]=-1;T.append(row);check_farkas(T,bb+[B+1],rec['ray']);bounds.append((j,sg,B))
  if sg==1:upper[j]=B
  else:lower[j]=-B
 require(upper==c['upper']and lower==c['lower'],'incorrect saturated bounds')
 return upper,lower

def profiles(R,d,c):
 A,b,V,cols,lab,sp=build(R,d,21);upper,lower=replay_bounds(A,b,c)
 AA=[r[:len(V)]for r in A if not any(r[len(V):])];bb=[z for r,z in zip(A,b)if not any(r[len(V):])]
 for j in range(len(V)):
  if upper[j]==lower[j]:AA.append([int(k==j)for k in range(len(V))]);bb.append(lower[j])
 pp,stats=enumerate_affine(AA,bb,upper[:len(V)],10000000);require(stats==c['enumeration'],'wrong exhaustive affine domain');require(digest(pp)==c['raw_profiles_sha256'],'wrong complete profile list')
 filtered=filter_profiles(R,d,cols,V,sp,pp,lab,6);require(digest(filtered)==c['filtered_sha256'],'wrong low-word profile filter')
 return V,cols,lab,sp,filtered['survivors'],upper

def product_records(R,d,V,cols,lab,sp,survivors):
 C=d['C'];tab=d['tab'];conj=lambda x:M.evaluate(x.to_list(),C.unit**(d['F']-1),C);star=[lab.index(tab.rows.index(tuple(conj(x)for x in tab.rows[lab[a]])))for a in range(6)];pairs=list(itertools.combinations_with_replacement(range(1,6),2));moments={};pp=[x['counts']for x in survivors]
 for word,forms in word_forms(d,cols,V,sp,lab,4):
  den,row=forms[0];vv=[row[0]+sum(a*b for a,b in zip(row[1:],p))for p in pp];require(all(z%den==0 for z in vv),'nonintegral fourth moment');moments[word]=[z//den for z in vv]
 records=[]
 for ix,x in enumerate(survivors):
  p=x['counts'];t={tuple(z['word']):z['multiplicity']for z in x['low_triples']};lc=[[int(a==star[b])]+[t[tuple(sorted((a,b,star[c])))]for c in range(1,6)]for a,b in pairs]
  G=[[moments[tuple(sorted(tuple(star[a]for a in aa)+bb))][ix]-sum(a*b for a,b in zip(lc[i],lc[j]))for j,bb in enumerate(pairs)]for i,aa in enumerate(pairs)]
  require(all(z>=0 for row in G for z in row),'negative product Gram entry (this record must be excluded separately)')
  prod=[[sum(cols[a][i]*cols[b][j]*R[i][j][k]for i in range(6)for j in range(6))-sum(lc[h][i]*cols[i][k]for i in range(6))for k in range(6)]for h,(a,b)in enumerate(pairs)]
  records.append(dict(profile_index=x['profile_index'],counts=p,rank=x['rank'],gram=G,low_coefficients=lc,restriction=prod))
 return records

def joint_groups(GR,V,records):
 gg={}
 for r in records:
  w=len(r['gram']);H=[list(map(int,GR.row(i)))+[r['restriction'][j][i+1]for j in range(w)]for i in range(5)]+[r['restriction'][i][1:]+r['gram'][i]for i in range(w)];gg.setdefault(tuple(tuple(row)for row in H),[]).append(r)
 out=[]
 for H,rs in gg.items():
  pre=prepare(s.Matrix(H));n,rank,ix,vals=pre;require(ix[:5]==list(range(5)),'restriction Gram must be nonsingular');S=s.Matrix(H).extract(ix,ix);require(S.det()>0 and s.Matrix(H)==s.Matrix(H)[:,ix]*S.inv()*s.Matrix(H)[ix,:],'invalid joint Gram image')
  active=[j for j in range(len(V))if any(r['counts'][j]for r in rs)];types=[]
  for j in active:
   vv,_=native(pre,V[j]);require(all(v[:5]==tuple(V[j])for v in vv),'fixed restriction mismatch');require(len(vv)==len(set(vv)),'duplicate joint column');types.append(dict(index=j,column=list(V[j]),vectors=[list(v[5:])for v in vv]))
  out.append(dict(gram=[list(row)for row in H],profiles=[r['profile_index']for r in rs],rank=rank,types=types))
 return out

def factor_system(group,r):
 w=len(r['gram']);p=r['counts'];domains=[t for t in group['types']if p[t['index']]];labels=[(t['index'],t['column'],x)for t in domains for x in t['vectors']];A=[];b=[]
 for t in domains:A.append([int(j==t['index'])for j,v,x in labels]);b.append(p[t['index']])
 for i in range(w):
  for j in range(i,w):A.append([x[i]*x[j]for k,v,x in labels]);b.append(r['gram'][i][j])
 for i in range(w):
  for j in range(5):A.append([x[i]*v[j]for k,v,x in labels]);b.append(r['restriction'][i][j+1])
 return A,b

def phase_base(R,d,V,cols,lab,upper):
 allowed=[v for v,B in zip(V,upper)if B];G,_=M.high_vectors(d,cols);sp=Spectrum(d['tab'],cols,[(v,None)for v in allowed]);d['_branch_cache']={tuple(map(tuple,cols)):(G,allowed,sp)};A,b,meta=M.system(R,d,cols,[1]*5,lab);bad=set(map(tuple,sp.forbidden));allowed=[v for v in allowed if v not in bad];return A,b,allowed

def phase_system(base,V,profile,nt):
 A,b,allowed=base;vix={v:i for i,v in enumerate(V)};nh=len(allowed)*nt;keep=[j for i,v in enumerate(allowed)if profile[vix[v]]for j in range(i*nt,(i+1)*nt)]+list(range(nh,len(A[0])));ar=[[row[j]for j in keep]for row in A];rb=list(b);active=[(i,v)for i,v in enumerate(allowed)if profile[vix[v]]]
 for row,(i,v)in enumerate(active):ar.append([int(row*nt<=k<(row+1)*nt)for k in range(len(keep))]);rb.append(profile[vix[v]])
 nz=[i for i,row in enumerate(ar)if any(row)or rb[i]];return [ar[i]for i in nz],[rb[i]for i in nz]

def verify(R,c,progress=print,frontier=None):
 require(c['kind']=='exact_joint_center_profile_reduction'and c['version']==1,'wrong profile certificate');st=time.monotonic()
 import galois_pseudo_reduction as reduction
 red=reduction.verify(R,c['general_reduction']);d=M.data_for(R,3,24);require(M.metadata(d)==c['metadata'],'wrong complete low domain');admitted=[]
 for i,cols in enumerate(d['lows']):
  if M.low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du):continue
  labs=d['tab'].assignments(cols)
  if labs:admitted.append((i,labs))
 require([i for i,labs in admitted]==[20,21],'unexpected admitted low frame')
 # The first frame's two distinct labellings have inherited exact ST rays.
 for lab,br in zip(admitted[0][1],c['low20']):
  require(list(lab)==br['labelling'],'wrong low20 labelling');A,b,meta=M.system(R,d,d['lows'][20],[1]*5,lab);check_farkas(A,b,br['ray'])
 require(len(c['low20'])==len(admitted[0][1]),'omitted low20 labelling');progress('low frame20 excluded exactly')
 cols=d['lows'][21];labs=admitted[1][1];lab=labs[0]
 for other in labs:
  perm=[lab.index(x)for x in other];require(all(tuple(cols[i])==tuple(cols[perm[i]])for i in range(6)),'invalid repeated-column labelling quotient')
 V,cols,lab,sp,survivors,upper=profiles(R,d,c['saturation']);progress('complete low frame21 profiles: '+str(len(survivors)))
 records=product_records(R,d,V,cols,lab,sp,survivors);GR,_=M.high_vectors(d,cols);groups=joint_groups(GR,V,records);require(digest(groups)==c['joint_domain_sha256'],'joint domain reconstruction mismatch');progress('complete joint coefficient domains: '+str(len(groups)))
 byprofile={p:g for g in groups for p in g['profiles']};byrecord={r['profile_index']:r for r in records};proofs=c['profile_proofs'];require(set(map(int,proofs))==set(byrecord),'omitted profile proof or survivor');base=None;remaining=[];counts=Counter()
 for pi,r in byrecord.items():
  pr=proofs[str(pi)];kind=pr['kind'];counts[kind]+=1
  if kind in ['joint_farkas','joint_congruence']:
   A,b=factor_system(byprofile[pi],r)
   if kind=='joint_farkas':check_farkas(A,b,pr['ray'])
   else:check_congruence(A,b,[1]*len(A[0]),pr['congruence'])
  elif kind=='cubic_joint_farkas':
   from round5_unified import low_word_data
   words=list(itertools.combinations_with_replacement(range(1,6),2))+list(itertools.combinations_with_replacement(range(3,6),3));wd=low_word_data(R,d,cols,V,r['counts'],lab,words=words,spectrum=sp);cr=dict(profile_index=pi,counts=r['counts'],gram=wd['gram'],restriction=wd['restriction']);cg=joint_groups(GR,V,[cr])[0];A,b=factor_system(cg,cr);require(len(A)==pr['rows']and len(A[0])==pr['variables'],'wrong cubic factor system');check_farkas(A,b,pr['ray'])
  elif kind=='twist_farkas':
   if base is None:base=phase_base(R,d,V,cols,lab,upper)
   A,b=phase_system(base,V,r['counts'],len(d['phases']));check_farkas(A,b,pr['ray'])
  else:require(kind=='retained','unsupported proof kind');remaining.append(pi)
 require(remaining==c['remaining_profile_indices'],'wrong residual profile list');require(not c['categorification_claimed'],'necessary data claimed categorical')
 if frontier is not None:
  require(frontier['low_columns']==[list(v) for v in cols] and frontier['high_columns']==[list(v) for v in V],'frontier restriction columns do not match exact reconstruction')
  expected=[dict(profile_index=pi,rank=byrecord[pi]['rank'],multiplicities=[[i,n] for i,n in enumerate(byrecord[pi]['counts']) if n]) for pi in remaining]
  require(frontier['profiles']==expected,'frontier multiplicities do not match complete exact reconstruction')
 return dict(passed=True,scope='general_necessary_profile_reduction',optimizer_used=False,low_frames=len(d['lows']),raw_profiles=c['raw_profile_count'],low_word_profiles=len(records),joint_forms=len(groups),proof_counts=dict(counts),remaining_profiles=len(remaining),remaining_ranks=sorted({byrecord[i]['rank']for i in remaining}),general_reduction=red,seconds=time.monotonic()-st)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--certificate',type=Path,default=PROOF/'profile_certificate.json');ap.add_argument('--output',type=Path,default=PROOF/'exact_replay.json');args=ap.parse_args()
 import scipy.optimize
 def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during exact replay')
 scipy.optimize.linprog=scipy.optimize.milp=denied
 R=next(r['N']for r in json.load(open(ROOT/'data/census.json'))if r['id']=='R6_5_1204');out=verify(R,json.load(open(args.certificate)),progress=lambda t:print(t,flush=True));args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
