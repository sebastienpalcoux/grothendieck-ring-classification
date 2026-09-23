#!/usr/bin/env python3
"""Cross-check small exhaustive searches and reject damaged proof witnesses."""
from pathlib import Path
import sys,json,copy,itertools,time
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'software'))
from dispatch import *
from signed import *
from test_data import certificate_records,source_tensors,historical_rings

def main():
    start=time.monotonic();selected={};small=[]
    for row in certificate_records():
        c=row['certificate'];k=c['kind']
        if k=='dnumber':selected.setdefault('dnumber',row)
        if k=='signed':
            if row['multiplicity']<=6:small.append(row)
            if c.get('tables'):selected.setdefault('signed',row)
            if c.get('duality_type')=='ns' and c.get('tables'):selected.setdefault('ns',row)
            if c.get('enumeration'):selected.setdefault('compact',row)
        if k=='weak_integral' and c.get('pseudo',{}).get('roots') and c['pseudo'].get('failures'):selected.setdefault('weak',row)
    R=source_tensors([r['source_index'] for r in list(selected.values())+small]);models=json.loads((ROOT/'data/models.json').read_text());fast=Search('cpp');slow=Search('python')
    compared=0
    for row in small:
        c=row['certificate'];A=permute(R[row['source_index']],c['basis'])
        if dual(A)==[0,1,2,3]:require(fast.selfdual(sd_tuple(A))==slow.selfdual(sd_tuple(A)),'backend disagreement')
        compared+=1
    bounds=[(2,)*10,(0,0,0,1,0,1,1,0,0,1),(1,)*10]
    bounds += [sd_tuple(r) for r in historical_rings()[:27] if dual(r)==[0,1,2,3]]
    naive_cases=0
    for N in dict.fromkeys(bounds):
        pos=gauges(N);domains=[tuple(v for v in range(-n,n+1,2) if k not in pos or v>0) for k,n in enumerate(N)]
        brute=sorted(p for p in itertools.product(*domains) if not any(sd_equations(p)))
        require(brute==sorted(python_sd(N,pos))==fast.selfdual(N),'brute-force enumeration disagreement')
        for pars in brute:validate(sd_tensor(pars),nonnegative=False)
        naive_cases+=1
    rejected=[]
    def reject(name,row,edit):
        c=copy.deepcopy(row['certificate']);edit(c)
        try:check(R[row['source_index']],c,models,fast)
        except (VerificationError,ValueError,IndexError,KeyError,ZeroDivisionError):rejected.append(name)
        else:raise VerificationError('tampered proof accepted: '+name)
    reject('false d-number divisibility',selected['dnumber'],lambda c:c.update(j=len(c['factor'])-1))
    reject('missing signed table',selected['signed'],lambda c:c['tables'].pop())
    if 'compact' in selected:
        def alter_count(c):
            e=c['enumeration'];k='total' if 'total' in e else 'retained_tables';e[k]+=1
        reject('false compact signed count',selected['compact'],alter_count)
    reject('altered codegree root',selected['weak'],lambda c:c['pseudo']['roots'][0].__setitem__(0,str(s.Rational(c['pseudo']['roots'][0][0])+1)))
    reject('missing induction branch',selected['weak'],lambda c:c['pseudo']['failures'].pop())
    if 'ns' in selected:reject('missing non-self-dual signed branch',selected['ns'],lambda c:c['tables'].pop())
    row=selected['dnumber'];bad=copy.deepcopy(row);bad['certificate']={'kind':'model','model':models[0]['model']}
    reject('false positive model',bad,lambda c:None)
    report={'passed':True,'cross_backend_rings_through_multiplicity_6':compared,'naive_enumeration_bound_cases':naive_cases,'rejected_corruptions':rejected,'elapsed_seconds':round(time.monotonic()-start,3)}
    (ROOT/'verification/tests.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
