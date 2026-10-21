#!/usr/bin/env python3
"""Evaluate the R925 frame rays against the frozen published matrix builder.

Does not import or call the frontier streaming cone or oracle. Complete low
frames use the frozen native enumeration, compiled outside its frozen root.
The full high/rotation matrix comes from the frozen unstreamed builder.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,itertools,json,math,os,subprocess,sys
HERE=Path(__file__).resolve().parent
STAGE=HERE.parent
BASE=STAGE.parent/'rank8_m3_20261021'
sys.path.insert(0,str(BASE/'criteria'))
import global_induction as old
import global_duality as frozen

def need(ok,message):
    if not ok:raise ValueError(message)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run():
    source=next(x for x in json.loads((BASE/'pipeline/census_m3.json').read_text()) if x['id']=='R8_3_925')
    R=source['tensor'];saved=json.loads((STAGE/'global_induction/frame_results/R8_3_925_h4.json').read_text())
    need(digest(R)==source['tensor_sha256']==saved['tensor_sha256'],'source binding')
    a=old.setup(R);width=a['width'];D=a['global_dimension'];types,bound=a['traces'](4)
    low=[]
    for group,cs in enumerate(a['columns']):
        for c in cs:
            z=tuple(sum(Q(c[i])*a['dimensions'][i][k] for i in range(8)) for k in range(width))
            low.append((group,tuple(map(int,c)),z))
    offset=len(low);labels=[(v,z,ti) for v,z in a['high'] for ti in range(len(types))]
    high_end=offset+len(labels);rotations=[];powers={};specs=[]
    for obj in range(1,8):
        powers[obj]=[[1]+[0]*7]
        for order in range(1,5):powers[obj].append([sum(powers[obj][-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
        for order in (3,4):
            rs=[r for r in old.s.divisors(order) if r<order]
            ts=a['rotations'](order,rs);start=high_end+len(rotations)
            specs.append((obj,order,rs,ts,start))
            rotations.extend((obj,order,tt) for tt in ts)
    def raw_column(j):
        """Separate unnormalized formula, used only to recover row units."""
        out=[]
        if j<offset:g,c,z=low[j];v=None;ti=None
        elif j<high_end:v,z,ti=labels[j-offset];c=None;g=None
        else:c=v=z=ti=g=None
        out.extend(Q(int(g==k)) for k in range(7))
        for i,k in itertools.combinations_with_replacement(range(8),2):
            out.append(Q(c[i]*c[k] if c else v[i-1]*v[k-1] if v and i and k else 0))
        for power in (1,2):
            mom=a['mul'](z,types[ti][power-1]) if v else z
            for i in range(1,8):
                for coord in range(width):out.append(Q(c[i]*z[coord] if c else v[i-1]*mom[coord] if v else 0))
        for obj,order,rs,ts,start in specs:
            out.append(Q(int(start<=j<start+len(ts))))
            for at,r in enumerate(rs):
                for coord in range(width):
                    if c:value=-sum(powers[obj][r][i]*c[i] for i in range(8))*z[coord]
                    elif v:value=-sum(powers[obj][r][i]*v[i-1] for i in range(1,8))*a['mul'](z,types[ti][order//r-1])[coord]
                    elif start<=j<start+len(ts):value=a['mul'](D,ts[j-start][at])[coord]
                    else:value=0
                    out.append(Q(value))
        return out
    print('building frozen full uncontracted matrix',flush=True)
    A,b,indicators,meta=frozen.ORIGINAL_BUILD(R,a,4)
    need(len(A)==saved['metadata']['rows']==197,'row count')
    scales=saved['metadata']['row_scales'];ratios=[];cache={}
    for i,row in enumerate(A):
        if not row:
            need(not b[i],'nonzero empty row');ratios.append(Q(1));continue
        j=next(iter(row))
        if j not in cache:cache[j]=raw_column(j)
        raw=cache[j][i];need(raw!=0,'raw coefficient support')
        old_scale=Q(row[j])/raw
        need(old_scale>0,'positive row normalization')
        ratios.append(Q(scales[i])/old_scale)
    mapping,pairs,nvars=frozen.duality_map(R,a,meta)
    print('full frozen matrix built',meta['variables'],sum(map(len,A)),flush=True)
    import low_frames_rank8 as native
    exe=STAGE/'global_induction/low_frames_frontier'
    cpp=BASE/'performance/low_frames_rank8.cpp'
    if not exe.exists() or exe.stat().st_mtime_ns<cpp.stat().st_mtime_ns:
        temporary=exe.with_name(exe.name+'_review_'+str(os.getpid()))
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(temporary)],check=True,capture_output=True)
        os.replace(temporary,exe)
    native.executable=lambda:exe
    frames=native.low_matrices(a['columns'],a['B'],gram_prune=True)
    lookup={(g,c):i for i,(g,c,z) in enumerate(low)}
    frames=tuple(tuple(lookup[g,tuple(c)] for g,c in enumerate(frame[1:])) for frame in frames)
    need(len(frames)==76984 and digest(frames)==saved['metadata']['frame_domain_sha256'],'complete low frame domain')
    native._cached.cache_clear()
    cases=[]
    for case in saved['pseudo_certificate']['cases']:
        y=case['y'];need(len(y)==len(A) and all(type(x)is int for x in y),'integer full ray')
        transferred=[Q(x)*r for x,r in zip(y,ratios)]
        denominator=math.lcm(*(v.denominator for v in transferred))
        yy=[int(v*denominator) for v in transferred]
        scores=[0]*nvars
        for row,yi in zip(A,yy):
            if yi:
                for j,x in row.items():scores[mapping[j]]+=x*yi
        _,rhs=old.integers(A,b,indicators,D,case['indicators'])
        bty=sum(x*z for x,z in zip(rhs,yy))
        need(bty==case['bTy']*denominator and bty<0,'right-side separation')
        frame_scores=[sum(scores[k] for k in frame) for frame in frames]
        need(min(frame_scores)>=0 and min(scores[offset:])>=0,'full frozen operator ray fails')
        cases.append({'indicators':case['indicators'],'ray_transfer_denominator':denominator,'minimum_frame_pairing':min(frame_scores),'minimum_high_or_aux_pairing':min(scores[offset:]),'rhs_pairing':bty})
        print('frozen operator ray PASS',case['indicators'],flush=True)
    return {'result':'PASS','id':source['id'],'tensor_sha256':source['tensor_sha256'],'matrix_builder':'frozen published global_induction._build','streaming_oracle_used':False,'complete_frames':len(frames),'low_atomic_columns':offset,'uncontracted_columns':meta['variables'],'contracted_high_and_aux_columns':nvars-offset,'rows':len(A),'cases':cases}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    out=run();path=HERE/'r925_independent.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(json.loads(path.read_text())==out,'receipt changed')
    print('PASS: R925 complete frozen-operator replay')
