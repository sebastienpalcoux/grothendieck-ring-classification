"""Cheap spherical-character screen of unresolved commutative m=2 rings.

This identifies only candidates for the full oriented signed verifier;
neither a failed spherical character nor a timed-out screen is an exclusion.
"""
import collections
import json
import signal
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
sys.path.insert(1,str(ROOT/'software'))
import analyze
import dimension_order
import proofs
from rings import Characters

class Budget(Exception): pass
def alarm(*_):raise Budget()

def screen(R):
    a=Characters(R)
    counts=collections.Counter()
    for f,m in a.components:
        K,ds,delta,pD=a.component(f)
        if any(not x for x in ds):kind='zero'
        elif any(ds[i]!=ds[a.du[i]] for i in range(8)):kind='duality'
        else:
            w=proofs.norm_failure(pD,a.cf) or proofs.field_failure(f,a.cf) or \
              dimension_order.certificate(a,f) or proofs.spherical_global_moment(a,f)
            kind=w['kind'] if w else 'needs_pseudo'
        counts[kind]+=1
    return dict(counts)

if __name__=='__main__':
    limit=int(sys.argv[1]) if len(sys.argv)>1 else 149
    rows=json.load(open(ROOT/'data/decisions.json'))
    group=sorted((R for R in analyze.read_source() if analyze.mult(R)==2),
      key=lambda R:tuple(x for M in R for row in M for x in row))
    targets=[d for d in rows if d['multiplicity']==2 and d['status']=='unresolved'
       and d['commutative']][:limit]
    signal.signal(signal.SIGALRM,alarm)
    result=[]
    for d in targets:
        started=time.monotonic()
        try:
            signal.alarm(3)
            R=group[d['index']-1]
            assert d['tensor_sha256']==analyze.fp(R)
            counts=screen(R)
            status='complete_spherical_obstruction' if not counts.get('needs_pseudo') else 'needs_pseudo'
        except Budget:
            counts={};status='timeout'
        except Exception as e:
            counts={};status='error:'+type(e).__name__+':'+str(e)
        finally:signal.alarm(0)
        result.append({'id':d['id'],'status':status,'components':counts,
           'seconds':round(time.monotonic()-started,2)})
        print(d['id'],status,counts,result[-1]['seconds'],flush=True)
    (HERE/'screen_m2.json').write_text(json.dumps(result,indent=2)+'\n')
