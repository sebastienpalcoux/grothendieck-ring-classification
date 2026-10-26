"""Exact input audit; floats are hints only and never classify a ring."""
from pathlib import Path
import collections, gzip, hashlib, itertools, json, sys, time
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import audit_input as old
import common

def main():
    start=time.monotonic()
    raw=gzip.decompress((ROOT/'input/rank12_M1_verified/FusionRingMultiplicationTables.txt.gz').read_bytes())
    rows=raw.decode().splitlines()
    common.require(len(rows)==632,'632 physical input lines')
    records=[];buckets=collections.defaultdict(list);tensor={};tests=0
    for line,row in enumerate(rows,1):
        R=json.loads(row.replace('{','[').replace('}',']'));n=len(R)
        common.require(n==12 and all(len(A)==12 and all(len(B)==12 for B in A)for A in R),'rank twelve shape')
        common.require(all(type(x)is int and x in (0,1)for A in R for B in A for x in B),'exact multiplicity one')
        common.validate(R)
        N=np.array(R,dtype=np.int64);du=common.dual(R)
        vals,V=np.linalg.eigh(N.sum(0));d=V[:,-1]/V[0,-1]
        common.require(min(d)>0,'positive FP hint')
        common.require(max(np.max(abs(N[i]@d-d[i]*d))for i in range(n))<1e-7,'FP hint residual')
        inv=[i for i in range(n)if sum(R[i][du[i]])==1]
        subs=old.subrings(N,du);key=common.coarse(R)
        for prev,S in buckets[key]:
            tests+=1
            common.require(common.based_iso(R,S)is None,f'duplicate lines {prev},{line}')
        buckets[key].append((line,R))
        rid=f'R12_1_{line}';tensor[rid]=R
        records.append(dict(id=rid,line=line,tensor_sha256=common.sha(R),dual=du,
            commutative=bool(np.array_equal(N,N.swapaxes(0,1))),invertibles=inv,
            subrings=subs,simple=len(subs)==2,
            fp_hint=d.tolist(),global_fp_hint=float(d@d),
            squared_dimensions=old.radical_dimension_certificate(N,d)))
    out=dict(status='PASS',records=records,count=len(rows),
        input_sha256=hashlib.sha256(raw).hexdigest(),exact_pairwise_isomorphism_tests=tests,
        commutative=sum(r['commutative']for r in records),
        weakly_integral=sum(r['squared_dimensions']is not None for r in records),
        pointed=sum(len(r['invertibles'])==12 for r in records),
        simple=sum(r['simple']for r in records),
        invertible_ranks=dict(collections.Counter(len(r['invertibles'])for r in records)),
        elapsed_seconds=time.monotonic()-start)
    (ROOT/'profile.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'tensors.json').write_text(json.dumps(tensor,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='records'},indent=2))

if __name__=='__main__':main()
