#!/usr/bin/env python3
"""Compare catalog orbit queries with independent local Python elimination."""
import sys,json,random,time,itertools,functools,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'software'))
from signed import Search,python_sd,gauges,sd_parity_failure,SD_PERM_MAPS,gauge_images
from rings import sd_tensor,casimir_determinant
from rapid import dnumber,cyclotomic_failure
from global_signed import load_catalog
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--catalog',type=Path,default=ROOT/'data/signed_universal_128.jsonl.gz');parser.add_argument('--manifest',type=Path,default=ROOT/'data/signed_universal_128_manifest.json');args=parser.parse_args();rows,manifest=load_catalog(args.catalog,args.manifest,require_bound=None);assert manifest['bound']>=6
search=Search('python',use_global=False);search.global_catalog=(rows,manifest)
rng=random.Random(7612890)
small=[p for p,d in rows if max(map(abs,p))<=4]
bounds=[]
for p in rng.sample(small,20):
 mapping=rng.choice(SD_PERM_MAPS);p=tuple(p[k] for k in mapping);p=rng.choice(sorted(gauge_images(p)))
 N=tuple(rng.choice([n for n in range(abs(v),7) if (n-v)%(2 if k==4 else 4)==0]) for k,v in enumerate(p))
 bounds.append(N)
bounds+= [tuple(rng.randrange(7) for _ in range(10)) for _ in range(4)]
@functools.lru_cache(maxsize=None)
def admissible(p):
 R=sd_tensor(p);return not dnumber(R) and not cyclotomic_failure(R)
@functools.lru_cache(maxsize=None)
def determinant(p):return casimir_determinant(sd_tensor(p))
records=[];start=time.monotonic()
for N in bounds:
 raw=python_sd(N,gauges(N));universal=[p for p in raw if not sd_parity_failure(N,p) and admissible(p)]
 for primes in ([],[2],[3],[5],[2,3]):
  expected={p for p in universal if all(determinant(p)%q==0 for q in primes)}
  got,summary=search.global_selfdual(N,primes)
  assert set(got)==expected,(N,primes,len(expected-set(got)),len(set(got)-expected))
  records.append({'bounds':N,'primes':primes,'local_associative':len(raw),'universal_parity':len(universal),'retained':len(got)})
report={'all_passed':True,'catalog_bound':manifest['bound'],'test_bound':6,'mixed_bounds':len(bounds),'prime_conditions':5,'comparison_count':len(records),'nonempty_comparisons':sum(bool(r['retained']) for r in records),'elapsed_seconds':round(time.monotonic()-start,3),'comparisons':records}
(ROOT/'verification/global_signed_query_independent_tests.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='comparisons'},indent=2))
