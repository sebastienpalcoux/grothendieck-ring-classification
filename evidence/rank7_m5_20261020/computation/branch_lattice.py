"""Exact per-branch Gram pruning and stronger inactive lattice tests."""
import argparse,hashlib,itertools,json,math,time
from fractions import Fraction as Q
from pathlib import Path
from inactive_lattice import EchelonLattice,hermite_basis,prepare,check_counts,require
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'
PAIRS=[(i,j) for i in range(6) for j in range(i+1)]


def matrix(values):
    out=[[0]*6 for _ in range(6)]
    for (i,j),value in zip(PAIRS,values):out[i][j]=out[j][i]=value
    return out


def negative_vector(M):
    """An exact negative quadratic-form witness, or None if PSD."""
    n=len(M);S=[list(map(Q,row)) for row in M]
    basis=[[Q(int(i==j)) for i in range(n)] for j in range(n)]
    def primitive(v):
        den=math.lcm(*(x.denominator for x in v));out=[int(x*den) for x in v]
        g=math.gcd(*out) or 1;out=[x//g for x in out]
        require(sum(out[i]*M[i][j]*out[j] for i in range(n) for j in range(n))<0,'invalid negative Gram witness')
        return out
    while S:
        for i in range(len(S)):
            if S[i][i]<0:return primitive(basis[i])
        for i in range(len(S)):
            if S[i][i]==0:
                for j in range(len(S)):
                    if S[i][j]:return primitive([(S[j][j]+1)*x-S[i][j]*y for x,y in zip(basis[i],basis[j])])
        pivot=next((i for i in range(len(S)) if S[i][i]>0),None)
        if pivot is None:return None
        indices=[i for i in range(len(S)) if i!=pivot];value=S[pivot][pivot]
        new_basis=[[x-S[j][pivot]/value*y for x,y in zip(basis[j],basis[pivot])] for j in indices]
        S=[[S[i][j]-S[i][pivot]*S[pivot][j]/value for j in indices] for i in indices]
        basis=new_basis
    return None


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--frame',type=int,choices=(6,8),required=True);args=ap.parse_args()
    frame=args.frame;records=json.loads((HERE/'inactive_branch_replay_normal.json').read_text())['results']
    branches=json.loads((INPUT/f'R7_5_3895_active_{frame}.json').read_text())['branches']
    systems={case:json.loads((INPUT/f'R7_5_3895_system_{frame}_{case}.json').read_text()) for case in (0,2,4,6)}
    original=systems[0];active=set(original['active_variables'])
    for system in systems.values():require([c[:21] for c in system['columns']]==[c[:21] for c in original['columns']] and system['active_variables']==original['active_variables'],'shared Gram and active variables')
    remaining=sorted(set(ix for r in records if r['low_index']==frame for ix in r['remaining_branch_indices']))
    output={'id':'R7_5_3895','low_index':frame,'branches':[],'status':'partial'}
    target=HERE/f'R7_5_3895_branch_lattice_{frame}.json'
    for ix in remaining:
        start=time.monotonic();counts=dict(branches[ix]);rhs=[b-sum(original['columns'][j][i]*c for j,c in counts.items()) for i,b in enumerate(original['rhs'])]
        residual=matrix(rhs[:21]);require(negative_vector(residual) is None,'active branch fails PSD')
        kept=[];excluded=[];forms={}
        for j,col in enumerate(original['columns']):
            if j in active:continue
            key=tuple(col[:21])
            if key not in forms:
                # A nonnegative integer variable >=1 consumes this entire Gram column.
                if any(c>b for c,b in zip(key,rhs[:21])):
                    entry=next(i for i,(c,b) in enumerate(zip(key,rhs[:21])) if c>b)
                    forms[key]={'entry':entry}
                else:
                    difference=matrix([b-c for c,b in zip(key,rhs[:21])]);witness=negative_vector(difference)
                    forms[key]={'negative_vector':witness} if witness is not None else None
            reason=forms[key]
            if reason is None:kept.append(j)
            else:excluded.append({'column':j,**reason})
        columns=[original['columns'][j] for j in kept];basis=hermite_basis(columns)
        lattice=EchelonLattice(basis,len(rhs));lattice.require_contains_generators(columns)
        cases=[]
        for case,system in systems.items():
            require([system['columns'][j] for j in kept]==columns,'shared inactive columns')
            residual_rhs=[b-sum(system['columns'][j][i]*c for j,c in counts.items()) for i,b in enumerate(system['rhs'])]
            prepared=prepare(columns,residual_rhs,[],basis=basis)
            okay,why=check_counts(prepared,[],return_failure=True)
            cases.append({'case':case,'lattice_pass':okay,'failure':why,'prepared':prepared})
        item={'index':ix,'active_counts':branches[ix],'kept_columns':kept,'excluded_columns':excluded,'cases':cases,'seconds':time.monotonic()-start}
        output['branches'].append(item);target.write_text(json.dumps(output,separators=(',',':'))+'\n')
        print(json.dumps({'frame':frame,'branch':ix,'kept':len(kept),'rank':len(basis),'lattice_survivors':[c['case'] for c in cases if c['lattice_pass']],'seconds':item['seconds']}),flush=True)
    output['status']='complete';target.write_text(json.dumps(output,separators=(',',':'))+'\n')


if __name__=='__main__':main()
