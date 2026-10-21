#!/usr/bin/env python3
"""Exact central twist moment relaxation, with explicit pseudo-unitary scope."""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys
import weighted_rank8 as w
from exact import ec,require
HERE=Path(__file__).resolve().parent

def restriction(a,beta,m):
    # Positivity supplies exact coordinate bounds before the inherited RREF
    # enumeration. Tightening these bounds removes no possible column.
    K=a['K'];emb=a['embedding'];remainder=beta-K(m)
    if emb.sign(remainder)<0:return 0,None
    B=a['Gram'].copy()
    for i in range(1,len(a['ds'])):
        alpha=remainder/a['ds'][i];lo=0;hi=1
        while emb.sign(alpha-K(hi))>=0:hi*=2
        while hi-lo>1:
            mid=(lo+hi)//2
            if emb.sign(alpha-K(mid))>=0:lo=mid
            else:hi=mid
        require(emb.sign(alpha-K(lo))>=0 and emb.sign(alpha-K(lo+1))<0,'exact coordinate floor')
        B[0,i]=min(int(B[0,i]),m*lo)
    if K.mod.degree()==1:
        # Exact bounded-knapsack dynamic programming counts every integral
        # column and computes coordinatewise minima without a Cartesian box.
        vals=[w.s.Rational(ec(v)[0]) if v else w.s.Rational(0) for v in [remainder,*a['ds'][1:]]]
        scale=math.lcm(*(int(v.q) for v in vals));target=int(vals[0]*scale);weights=[int(v*scale) for v in vals[1:]]
        require(all(v>0 for v in weights),'positive integralized dimension weights')
        bounds=[min(int(B[0,i])//m,math.isqrt(int(B[i,i]))) for i in range(1,len(a['ds']))]
        states={0:(1,[])}
        for weight,bound in zip(weights,bounds):
            nextstates={}
            for total,(count,mins) in states.items():
                for value in range(min(bound,(target-total)//weight)+1):
                    at=total+value*weight;candidate=mins+[value]
                    if at in nextstates:
                        oldcount,oldmins=nextstates[at]
                        nextstates[at]=(oldcount+count,[min(x,y) for x,y in zip(oldmins,candidate)])
                    else:nextstates[at]=(count,candidate)
            states=nextstates
        count,mins=states.get(target,(0,None))
        return count,None if mins is None else (m,*mins)
    cs=w.core.restriction(a['ds'],beta,m,K,B)
    return len(cs),tuple(min(c[i] for c in cs) for i in range(len(a['ds']))) if cs else None

def scan(R):
    a=w.spectral(R);K=a['K'];D=a['D'];ds=a['ds'];emb=a['embedding'];n=len(R)
    dimensions=[D/f for f in a['codegrees'][1:]]
    require(all(emb.sign(z)>0 for z in dimensions),'positive central constituent dimensions required')
    summaries=[restriction(a,z,m) for z,m in zip(dimensions,a['multiplicities'][1:])]
    counts=[item[0] for item in summaries];minima=[item[1] for item in summaries]
    if not all(counts):return dict(outcome='pseudo_unitary_obstruction',reason='empty required central restriction set',column_counts=counts)
    objects=[];obstructed=[]
    for i in range(1,n):
        lower=sum((K(mins[i])*z for mins,z in zip(minima,dimensions)),K.zero)
        total=D*ds[i];choices=(0,) if a['du'][i]!=i else (-1,1);cases=[]
        for nu in choices:
            # For the positive remaining spectral measure, m0=T-L,
            # m1=-L, m2=nu*D-L. PSD of its 3x3 Toeplitz matrix
            # gives these four distinct principal-minor conditions.
            vals=[total-lower,total*total-2*total*lower,
                  total*total-(K(nu)*D)**2-2*lower*(total-K(nu)*D),
                  (total-K(nu)*D)*(total*(total+K(nu)*D)-lower*(3*total+K(nu)*D))]
            signs=[emb.sign(v) for v in vals];cases.append(dict(second_indicator=nu,principal_minors=[ec(v) for v in vals],signs=signs,passes=all(v>=0 for v in signs)))
        if not any(c['passes'] for c in cases):obstructed.append(i)
        objects.append(dict(object=i,lower_trivial_twist_mass=ec(lower),total_mass=ec(total),cases=cases))
    return dict(outcome='pseudo_unitary_obstruction' if obstructed else 'no_conclusion',column_counts=counts,multiplicities=a['multiplicities'][1:],objects=objects,obstructed_objects=obstructed)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())}
    survivors=json.loads((HERE.parent/'pipeline/survivors_m3.json').read_text())
    models=json.loads((HERE.parent/'models/consolidated_models.json').read_text())
    if isinstance(models,dict):models=models.get('models',models.get('records',[]))
    model_ids={r['id'] for r in models}
    targets={r['id'] for r in survivors if any(r['tensor'][i][j]!=r['tensor'][j][i] for i in range(8) for j in range(8))}|model_ids
    rows=[]
    for rid in sorted(targets,key=lambda x:int(x.split('_')[-1])):
        r=census[rid];out=dict(id=rid,tensor_sha256=r['tensor_sha256'],stage='central_twist_moments',scope='pseudo_unitary_only',completed=True)
        try:out.update(scan(r['tensor']))
        except Exception as exc:out.update(outcome='implementation_ineligible',completed=False,reason=type(exc).__name__+': '+str(exc))
        require(rid not in model_ids or out['outcome']!='pseudo_unitary_obstruction','known model rejected')
        rows.append(out);print(rid,out['outcome'],flush=True)
    result=dict(schema='rank8-central-toeplitz-moments-v1',scope='pseudo_unitary_only; no general exclusion is inferred',records=rows,model_control_ids=sorted(model_ids),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    target=HERE/'central_moments_results.json'
    if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
    else:require(json.loads(target.read_text())==result,'central moment receipt differs')
    print('PASS:',len(rows),'exact central twist moment attempts',flush=True)
if __name__=='__main__':main()
