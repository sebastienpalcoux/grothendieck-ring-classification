#!/usr/bin/env python3
"""Independent bounded checks of the global signed table enumeration.

The bound-two reference traverses all 5^10 integer tensors without using
any elimination. A separate Python elimination is compared on mixed-parity,
nonuniform coordinate boxes. The comparisons use the full signed-permutation
orbits and retain the original positivity gauge.
"""
import argparse,hashlib,itertools,json,random,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from signed import python_sd,gauges,sd_equations
TRIPLES=((0,0,0),(0,0,1),(0,0,2),(0,1,1),(0,1,2),(0,2,2),(1,1,1),(1,1,2),(1,2,2),(2,2,2))
MASKS=(1,2,4,1,7,1,2,4,2,4)
MAPS=tuple(tuple(TRIPLES.index(tuple(sorted(p[k] for k in t))) for t in TRIPLES) for p in itertools.permutations(range(3)))
ACTIONS=tuple((m,tuple(-1 if (s&k).bit_count()%2 else 1 for k in MASKS)) for m in MAPS for s in range(8))
def orbit(p):return {tuple(p[j]*s for j,s in zip(m,signs)) for m,signs in ACTIONS}
def canonical(p):return min(orbit(p))
def read_output(output):
 rows=[tuple(map(int,line.split()[1:])) for line in output.splitlines()]
 assert all(len(p)==10 and not any(sd_equations(p)) for p in rows)
 assert len(rows)==len(set(rows))
 assert len(rows)==len({canonical(p) for p in rows})
 return rows

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'verification/global_signed_tests.json');args=parser.parse_args();start=time.monotonic()
 src=ROOT/'software/enumerate_global_signed.cpp';ref=ROOT/'software/enumerate_global_signed_reference.cpp'
 with tempfile.TemporaryDirectory() as tmp:
  exe=Path(tmp)/'global';reference=Path(tmp)/'reference'
  subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(src),'-o',str(exe)],check=True)
  subprocess.run(['g++','-O3','-std=c++17',str(ref),'-o',str(reference)],check=True)
  rows=read_output(subprocess.check_output([str(exe),'2','1'],text=True))
  brute=[tuple(map(int,l.split()[1:])) for l in subprocess.check_output([str(reference),'2'],text=True).splitlines()]
  assert {canonical(p) for p in rows}=={canonical(p) for p in brute}
  rows4=read_output(subprocess.check_output([str(exe),'4','1'],text=True))
  parallel4=read_output(subprocess.check_output([str(exe),'4','4'],text=True));assert set(rows4)==set(parallel4)
  universe=set().union(*(orbit(p) for p in rows4))
  rng=random.Random(690128)
  boxes=[(4,)*10,(3,)*10,(2,)*10,(1,)*10]+[tuple(rng.randrange(5) for _ in range(10)) for _ in range(20)]
  checks=[]
  for N in boxes:
   positive=gauges(N)
   expected=set(python_sd(N,positive))
   actual={p for p in universe if all(abs(v)<=N[k] and (v-N[k])%2==0 for k,v in enumerate(p)) and all(p[k]>0 for k in positive)}
   assert expected==actual,(N,len(expected-actual),len(actual-expected))
   checks.append({'bounds':N,'solutions':len(actual)})
 report={'all_passed':True,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'reference_source_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'exhaustive_bound':2,'exhaustive_integer_tensors':5**10,'exhaustive_valid_tensors':len(brute),'exhaustive_signed_permutation_orbits':len(rows),'mixed_box_bound':4,'mixed_box_orbits':len(rows4),'parallel_set_agreement':True,'python_reference_boxes':checks,'elapsed_seconds':round(time.monotonic()-start,3)}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
