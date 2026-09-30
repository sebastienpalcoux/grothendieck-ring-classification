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

