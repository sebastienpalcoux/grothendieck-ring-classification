"""Compare discovery accelerations with the previous exact enumerators."""
import hashlib,itertools,json,math,random,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank7/software'))
import sympy as s
from gram_vectors_fast import native

def require(value,message):
    if not value:raise ValueError(message)

def main():
    start=time.monotonic();rng=random.Random(20261020)
    fast=HERE/'low_frames_fast';old=ROOT/'supplements/rank7/software/low_generic'
    subprocess.run(['g++','-O3','-std=c++17',str(fast.with_suffix('.cpp')),'-o',str(fast)],check=True)
    low_count=0
    for dimension in range(1,7):
        for repeat in range(6):
            cols=[sorted(set(tuple(rng.randrange(3) for _ in range(dimension)) for _ in range(5))) for _ in range(dimension)]
            if repeat%2==0:cols[-1]=cols[0]
            chosen=[rng.choice(c) for c in cols]
            target=[sum(v[i] for v in chosen) for i in range(dimension)]
            B=[[sum(v[i]*v[j] for v in chosen)+int(i==j)*rng.randrange(3) for j in range(dimension)] for i in range(dimension)]
            raw=[dimension,dimension]+target+sum(B,[])
            for c in cols:raw+=[len(c)]+[x for v in c for x in v]
            outputs=[]
            for exe in (old,fast):
                result=subprocess.run([str(exe)],input=' '.join(map(str,raw)),text=True,capture_output=True,check=True,timeout=20)
                outputs.append(sorted(result.stdout.splitlines()))
            require(outputs[0]==outputs[1],'low enumeration differs');low_count+=1
    high_count=0
    for dimension in range(1,7):
        for repeat in range(4):
            if repeat==0:Q=s.diag(*[rng.randrange(1,5) for _ in range(dimension)])
            else:
                A=s.Matrix(dimension,min(dimension,repeat),lambda i,j:rng.randrange(2))
                Q=A*A.T
            rank=Q.rank()
            if not rank:require(not native(Q),'zero Gram matrix has a nonzero vector');high_count+=1;continue
            ix=next(I for I in itertools.combinations(range(dimension),rank) if Q.extract(I,I).det()!=0)
            sub=Q.extract(ix,ix);adj=sub.adjugate();det=int(sub.det())
            null=Q.nullspace();expected=[]
            for v in itertools.product(*(range(math.isqrt(int(Q[i,i]))+1) for i in range(dimension))):
                if not any(v):continue
                if any(v[i]*v[j]>Q[i,j] for i in range(dimension) for j in range(i,dimension)):continue
                if any(sum(v[i]*z[i] for i in range(dimension)) for z in null):continue
                if sum(v[ix[i]]*adj[i,j]*v[ix[j]] for i in range(rank) for j in range(rank))>det:continue
                expected.append(v)
            require(sorted(expected)==list(native(Q)),'high enumeration differs');high_count+=1
    files=['low_frames_fast.cpp','gram_vectors_fast.cpp','gram_vectors_fast.py','high_columns_fast.py']
    report={'status':'PASS','low_comparisons':low_count,'high_comparisons':high_count,
            'dimensions_checked':list(range(1,7)),'optimized_python':not __debug__,
            'sources_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files},
            'seconds':time.monotonic()-start,
            'scope':'Discovery acceleration equivalence controls; new exclusions still require inherited exact replay.'}
    (HERE/'acceleration_controls.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
