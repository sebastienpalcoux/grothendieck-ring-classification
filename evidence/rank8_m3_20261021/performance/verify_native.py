#!/usr/bin/env python3
"""Independent exact regression comparisons for the recovered native kernels."""
from pathlib import Path
from fractions import Fraction as F
from types import SimpleNamespace
import argparse,hashlib,importlib.util,itertools,json,random,sys,tempfile,time
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];FROZEN=ROOT/'supplements/rank6/software'
sys.path.insert(0,str(FROZEN));sys.path.insert(0,str(HERE))
import induction,higher_traces
import low_frames_rank8 as low
import gram_vectors_rank8 as gram
def require(p,msg):
 if not p:raise ValueError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def psd_reference(Q):
 return all(Q.extract(ix,ix).det()>=0 for m in range(1,Q.rows+1)for ix in itertools.combinations(range(Q.rows),m))
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();rng=random.Random(20261021);checks=[]
 # Unmodified frozen Python Cartesian/MITM enumeration on bounded fixtures.
 for n in range(2,9):
  for trial in range(5):
   sets=[];chosen=[]
   for j in range(n-1):
    cs=sorted({(1,)+tuple(rng.randrange(2)for _ in range(n-1))for _ in range(3)})
    if j and trial==0:cs=sets[-1]
    sets.append(cs);chosen.append(rng.choice(cs))
   L=s.Matrix.hstack(s.Matrix([1]+[0]*(n-1)),*(s.Matrix(c)for c in chosen));B=L*L.T
   u=s.Matrix([0]+[rng.randrange(2)for _ in range(n-1)]);B+=u*u.T
   if trial==4 and B[n-1,n-1]>0:B[n-1,n-1]-=1
   reference=sorted(induction.low_matrices(sets,B,False));actual=low.low_matrices(sets,B,False)
   require(actual==reference,'complete low row sums '+str((n,trial)))
   expected=[]
   for cs in reference:
    L=s.Matrix.hstack(*(s.Matrix(c)for c in cs));Q=B-L*L.T
    if min(Q)>=0 and psd_reference(Q):expected.append(cs)
   require(low.low_matrices(sets,B,True)==expected,'exact low Gram filter '+str((n,trial)))
   if n<=6:require(sorted(induction.low_matrices(sets,B,True))==expected,'frozen native Gram '+str((n,trial)))
   checks.append(dict(kind='low',n=n,trial=trial,complete=len(actual),pruned=len(expected),sha256=digest(expected)))
 # The frozen Gram program's sole extension is its declared n<=5 guard to8.
 # Its exhaustive free-coordinate box and leaf tests are otherwise unchanged.
 with tempfile.TemporaryDirectory()as tmp:
  tmp=Path(tmp);py=(FROZEN/'gram_vectors_general.py').read_text();cpp=(FROZEN/'gram_vectors_general.cpp').read_text()
  require(cpp.count('n>5')==1,'frozen Gram bound source changed');(tmp/'reference.py').write_text(py);(tmp/'reference.cpp').write_text(cpp.replace('n>5','n>8'))
  spec=importlib.util.spec_from_file_location('rank8_gram_frozen_reference',tmp/'reference.py');ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
  matrices=[]
  for n in range(1,9):
   matrices += [s.eye(n),s.ones(n),s.diag(*range(1,n+1))]
   for trial in range(3):
    C=s.Matrix(n,2,[rng.randrange(2)for _ in range(2*n)]);matrices.append(C*C.T)
  for i,Q in enumerate(matrices):
   expected=ref.native(Q);actual=gram.native(Q);require(actual==expected,'complete Gram vectors '+str(i))
   checks.append(dict(kind='Gram',n=Q.rows,fixture=i,count=len(actual),sha256=digest(actual)))
  census={r['id']:r['tensor']for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
  a=induction.Characters(census['R8_3_731']);Q=a.C.extract(range(1,8),range(1,8));actual=gram.native(Q);expected=ref.native(Q)
  require(actual==expected and len(actual)==24970,'real R731 complete Gram reference')
  checks.append(dict(kind='Gram',id='R8_3_731',count=len(actual),sha256=digest(actual)))
 # Rank8 arithmetic-filter dispatch agrees with the frozen full Cartesian
 # implementation, independently of both native range implementations.
 for n in (4,8):
  B=s.zeros(n);B[0,0]=1
  for i in range(1,n):
   for j in range(1,n):B[i,j]=2 if i==j else 1
  L=s.Matrix([1]+[0]*(n-1));data=dict(ch=SimpleNamespace(n=n,C=B),q=5,dimensions=[(F(1),F(0))]+[(F(1,2),F(1,2))]*(n-1),global_dimension=(F(10),F(2)))
  expected=higher_traces.high_columns(data,L);actual=gram.high_columns(data,L);require(actual==expected,'high-column arithmetic filter '+str(n))
  checks.append(dict(kind='high_columns',n=n,count=len(actual[1])))
 out=dict(schema='rank8-native-exact-reference-validation-v1',checks=checks,frozen_gram_extension='only C++ input rank guard n>5 to n>8; all enumeration and tests unchanged')
 target=HERE/'native_validation.json'
 if args.write:target.write_text(json.dumps(out,indent=2)+'\n')
 else:require(out==json.loads(target.read_text()),'native validation receipt differs')
 print('PASS:',len(checks),'fresh exact comparisons, including all24970 R731 Gram vectors.')
if __name__=='__main__':main()
