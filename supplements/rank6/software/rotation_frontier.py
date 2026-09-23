"""Exact feasible points of the tensor-rotation relaxation, not categorifications."""
from tensor_rotation import *
from pathlib import Path

def verify(R,c):
    require(c['kind']=='integer_count_rotation_feasible','wrong feasible-point kind')
    data=quadratic_data(R,gram_prune=True);cs=tuple(map(tuple,c['columns']));require(cs in data['lows'],'low columns not admissible');ep=c['indicators'];require(ep in list(map(list,indicator_choices(R))),'inadmissible second indicators');L=s.Matrix.hstack(*map(s.Matrix,cs));A,b,meta=system_rotation(R,data,L,ep,c['height']);require([len(b),len(A[0])]==c['shape'],'wrong system size');x=[Q(0)]*len(A[0]);seen=set()
    for j,a,d in c['primal']:
        require(type(j) is int and 0<=j<len(x) and j not in seen and type(a) is int and type(d) is int and a>=0 and d>0,'bad primal entry');seen.add(j);x[j]=Q(a,d)
    require(all(sum(Q(a)*z for a,z in zip(row,x))==rhs for row,rhs in zip(A,b)),'exact tensor-rotation primal identity failed')
    h=meta['high_variables'];rv=meta['rotation_variables'];require(all(x[j].denominator==1 for j in list(range(h))+list(range(len(x)-rv,len(x)))),'nonintegral count in integer-count relaxation')
    require(c['center_rank']==L.cols+sum(x[:h]),'wrong formal central rank')
    return {'equations':len(b),'variables':len(x),'nonzero_coordinates':len(seen),'high_count_variables':h,'rotation_count_variables':rv,'center_rank':c['center_rank']}

if __name__=='__main__':
    import argparse
    P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--recover',action='store_true');args=ap.parse_args();R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']=='R6_2_4')
    if args.recover:
        o=json.load(open(P/'research/milp_candidate_R6_2_4.json'));data=quadratic_data(R,gram_prune=True);L=s.Matrix.hstack(*map(s.Matrix,o['columns']));A,b,meta=system_rotation(R,data,L,o['ep'],o['height']);J=set(o['integral_indices']);x=[Q(round(a)) if j in J else Q(0) for j,a in enumerate(o['x'])];res=[Q(rhs)-sum(Q(a)*z for a,z in zip(row,x)) for row,rhs in zip(A,b)]
        for j in range(len(x)):
            if j in J:continue
            inds=[i for i,row in enumerate(A) if row[j]];require(len(inds)==1,'continuous variable is not a single-row slack');i=inds[0];x[j]=res[i]/A[i][j];res[i]=0
        require(not any(res) and all(z>=0 for z in x),'rounded counts fail exact recovery')
        c={'kind':'integer_count_rotation_feasible','height':o['height'],'columns':o['columns'],'indicators':o['ep'],'shape':[len(b),len(x)],'primal':[[j,z.numerator,z.denominator] for j,z in enumerate(x) if z],'center_rank':int(L.cols+sum(x[:meta['high_variables']]))};verify(R,c);(P/'data/frontier_rotation_feasible.json').write_text(json.dumps({'id':'R6_2_4','N':R,'certificate':c},separators=(',',':'))+'\n')
    o=json.load(open(P/'data/frontier_rotation_feasible.json'));require(o['N']==R and o['id']=='R6_2_4','frontier mismatch');print(json.dumps(verify(R,o['certificate']),indent=2));print('EXACT INTEGER-COUNT ROTATION FEASIBILITY VERIFIED')
