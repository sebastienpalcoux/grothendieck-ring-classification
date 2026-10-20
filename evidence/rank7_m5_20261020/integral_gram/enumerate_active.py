"""Exhaust the small saturated conductor-five row multiplicity budget."""
import collections
import json
import pathlib
import sys
import time

HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_center_trace as q


def run(low,write=True):
    start=time.monotonic()
    path=HERE/('R7_5_3895_system_'+str(low)+'_0.json')
    system=json.loads(path.read_text());cols=system['columns'];rhs=system['rhs']
    active=system['active_variables'];weights={int(i):v for i,v in system['active_weights'].items()}
    budget=system['active_budget'];branches=[];counts=collections.Counter()
    pair_index={tuple(sorted((i,j))):k for k,(i,j) in enumerate(q.base.PAIRS)}
    def inspect(chosen,gram):
        counts['raw']+=1
        residual=[b-a for a,b in zip(gram,rhs[:21])]
        if any(x<0 for x in residual):counts['negative_gram']+=1;return
        R=[[residual[pair_index[tuple(sorted((i,j)))]] for j in range(6)] for i in range(6)]
        if any(R[i][3]!=R[i][4] for i in range(6)):counts['difference_kernel']+=1;return
        if any(R[i][i]*R[j][j]<R[i][j]**2 for i in range(6) for j in range(i)):counts['minor2']+=1;return
        if not q.base.psd(R):counts['psd']+=1;return
        count=collections.Counter(chosen)
        branches.append([[j,n] for j,n in sorted(count.items())]);counts['remaining']+=1
    def rec(first,left,chosen,gram):
        if left==0:inspect(chosen,gram);return
        for ai in range(first,len(active)):
            j=active[ai];w=weights[j]
            if w<=left:rec(ai,left-w,chosen+[j],[x+y for x,y in zip(gram,cols[j][:21])])
    rec(0,budget,[],[0]*21)
    out={'id':'R7_5_3895','low_index':low,'system_sha256':q.hashlib.sha256(path.read_bytes()).hexdigest(),
         'active_budget':budget,'statistics':dict(counts),'branches':branches,'seconds':time.monotonic()-start}
    if write:
        (HERE/('R7_5_3895_active_'+str(low)+'.json')).write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({k:v for k,v in out.items() if k!='branches'}),flush=True)
    return out


if __name__=='__main__':
    for low in map(int,sys.argv[1:] or ['6','8']):run(low)
