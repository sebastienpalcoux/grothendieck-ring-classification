#!/usr/bin/env python3
"""Standard-library-only replay of the exact positive even-Clifford witnesses."""
from collections import Counter
from pathlib import Path
import argparse, hashlib, json

PIN='b76cdb3fbc8c4cc6c23d3e177be26d0a74d1adab114069b9e40b04b62678fca7'

def require(test,message):
    if not test: raise ValueError(message)

def spin_characters(n):
    require(n>=4 and n%2==0,'even order')
    m=n//2; out=[]
    for parity in (0,1):
        c=Counter()
        for mask in range(2**m):
            if mask.bit_count()%2!=parity:continue
            s=sum(2*a+1 for a in range(m) if mask&(1<<a))
            c[((parity-s)//2)%n]+=1
        out.append([c[j] for j in range(n)])
    c=Counter()
    for mask in range(2**(m-1)):
        s=sum(a for a in range(1,m) if mask&(1<<(a-1)))
        c[-s%n]+=1;c[(m-s)%n]+=1
    out.append([c[j] for j in range(n)])
    return out

def verify_row(source,row):
    n=source['n'];chars=spin_characters(n)
    require(row['status']=='exact_positive_witness','missing exact witness')
    u=row['uniform'];w=row['witness']
    require(type(u)is int and u>=0,'uniform multiplicity')
    require(len(w)==3*n and all(type(a)is int and a>=0 for a in w),'nonnegative multiplicities')
    values=list(map(int,source['multiplicities']))
    require(sum(values)==source['dimension']==row['dimension'],'dimension')
    reconstructed=[u*sum(chars[0])+sum(w[t*n+k]*chars[t][(j-k)%n] for t in range(3) for k in range(n)) for j in range(n)]
    require(reconstructed==values,'integer character identity')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('receipt',type=Path)
    a=p.parse_args();raw=a.source.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,'source hash')
    source=json.loads(raw)['rows'];receipt=json.loads(a.receipt.read_text())
    wanted={(n,x,z) for n in range(4,25,2) for x in (1,2) for z in range(52)}
    key=lambda r:(r['n'],r['base_simple'],r['central_simple'])
    inputs={key(r):r for r in source if key(r) in wanted}
    outputs={key(r):r for r in receipt['rows']}
    require(set(inputs)==set(outputs)==wanted and len(receipt['rows'])==1144,'complete domain')
    for k in sorted(wanted):verify_row(inputs[k],outputs[k])
    k=next(k for k in sorted(wanted) if inputs[k]['dimension']>0)
    bad=dict(outputs[k]);bad['witness']=bad['witness'][:];bad['witness'][0]+=1
    try:verify_row(inputs[k],bad)
    except ValueError:pass
    else:raise ValueError('mutation negative control accepted')
    print('PASS: 1144 exact positive even cyclic Clifford witnesses; mutation rejected; no categorification conclusion.')

if __name__=='__main__':main()
