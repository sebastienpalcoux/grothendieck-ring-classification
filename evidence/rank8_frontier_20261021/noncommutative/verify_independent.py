"""Independent positive central-coordinate enumeration and exact replay."""
import itertools,json,math,sys
import central_support as c
s=c.s

def central_columns(R,a,beta,m):
    # Derive the center from multiplication commutators, not the Gram kernel.
    N=a['N'];eq=[]
    for j in range(8):
        M=s.Matrix.hstack(*(s.Matrix(list(N[i]*N[j]-N[j]*N[i])) for i in range(8)))
        eq.extend(list(M.tolist()))
    A=s.Matrix(eq+[[1]+[0]*7]);rhs=s.Matrix([0]*len(eq)+[m])
    rr,piv=A.row_join(rhs).rref();c.require(8 not in piv,'center coordinate consistency')
    free=[j for j in range(8) if j not in piv]
    bounds=[m]+[min(int(a['Gram'][0,i])//m,math.isqrt(int(a['Gram'][i,i]))) for i in range(1,8)]
    out=[];tested=0
    for values in itertools.product(*(range(bounds[j]+1) for j in free)):
        tested+=1;v=[s.S.Zero]*8
        for j,z in zip(free,values):v[j]=s.Integer(z)
        for row,j in enumerate(piv):v[j]=rr[row,8]-sum(rr[row,k]*v[k] for k in free)
        if any(x.q!=1 or x<0 or x>bounds[i] for i,x in enumerate(v)):continue
        if sum((a['K'](int(v[i]))*a['ds'][i] for i in range(8)),a['K'].zero)==beta:out.append(tuple(map(int,v)))
    return sorted(out),tested

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    C=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text());records=[]
    # Three published noncommutative unitary models are positive controls.
    for rid in (448,458,715,721,928,941,1154):
        R=next(x['tensor'] for x in C if x['id']==f'R8_3_{rid}');a=c.data(R);counts=[]
        for cs,fc,m in zip(a['columns'],a['codegrees'][1:],a['multiplicities'][1:]):
            independent,tested=central_columns(R,a,a['D']/fc,m)
            c.require(cs==independent,'independent central coordinate enumeration mismatch');counts.append(tested)
        passing=sum(c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du']) is None for cols in a['lows'])
        c.require(passing>0,'positive control/frontier unexpectedly rejected')
        records.append({'id':f'R8_3_{rid}','independent_boxes':counts,'column_counts':list(map(len,a['columns'])),'passing_low_count':passing})
        print(rid,'PASS',flush=True)
    p=c.HERE/'independent_validation.json'
    if args.write:p.write_text(json.dumps(records,indent=2)+'\n')
    else:c.require(json.loads(p.read_text())==records,'independent receipt differs')

if __name__=='__main__':main()
