"""Replay finite necessary-data witnesses without an optimizer.

This is a feasibility audit of necessary conditions, not a construction of
a fusion category or a modular tensor category.
"""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import full_field_verlinde as w

q=w.q;m=w.m;e=w.e


def verify(path):
    data=json.loads(path.read_text());rid=data['id']
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    q.require(q.tensor_hash(N)==data['source_sha256'],'witness source tensor hash')
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5)
    records=w.phase_records(field='F8')
    q.require(json.loads(json.dumps(records))==data['phase_records'],'complete exact phase inventory')
    dom=next(a for a in e.domains(rid) if a['low']==data['low'])
    low=[tuple(a) for a in data['low']]
    orbits=[[(tuple(a),tuple(b),tuple(c)) for a,b,c in orb] for orb in dom['orbits']]
    spectrum=w.Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(a,c) for orb in orbits for a,b,c in orb])
    q.require(not spectrum.missing_low,'complete low central spectrum')
    forbidden=set(map(tuple,spectrum.forbidden))
    orbits=[orb for orb in orbits if all(a not in forbidden for a,b,c in orb)]
    q.require(json.loads(json.dumps(orbits))==data['orbits'],'complete spectrally integral source-row domain')
    V=w.v.coefficients(table,{'id':rid,'low_index':dom['low_index'],'low':low,'orbits':orbits},use_cache=False)
    branch=data.get('chi8_branch')
    if branch is None and '_chi8_' in path.name:branch=int(path.name.split('_chi8_')[1].split('_')[0].split('.')[0])
    results=[]
    for result in data['results']:
        if not result.get('exact_feasible'):continue
        case=dom['cases'][result['case']]
        columns,rhs,labels=w.f.build_system(table,low,case['label'],orbits,dom['bound'],D,zs,case['sign'],T,records,rid,chi8_branch=branch)
        if data.get('fifth_primary_refinement'):
            columns,rhs,labels=w.fifth_primary_refinement(columns,rhs,labels,orbits,records,rid)
        if data.get('norm_cut_records'):
            import integer_norm_cuts as nc
            cutdom={'id':rid,'low':low,'orbits':orbits}
            cuts=[nc.coefficient_cut(table,cutdom,case['label'],N,T.dual,V,record) for record in data['norm_cut_records']]
            q.require(cuts==data['norm_cut_coefficients'],'exact integer-norm cut coefficients')
            columns,rhs,labels=nc.append_cuts(columns,rhs,labels,cuts)
        key=lambda label:tuple(sorted(label.items()))
        counts={}
        for item in result['support']:
            label={k:v for k,v in item.items() if k!='count'};count=item['count']
            q.require(type(count)==int and count>0,'positive integer multiplicity')
            q.require(key(label) not in counts,'support labels are unique')
            counts[key(label)]=count
        allowed=set(map(key,labels));q.require(set(counts)<=allowed,'every phase multiplicity has valid provenance')
        x=[counts.get(key(label),0) for label in labels]
        remainder=[F(b)-sum(c[i]*n for c,n in zip(columns,x)) for i,b in enumerate(rhs)]
        slacks=[]
        for c in columns[len(labels):]:
            nz=[i for i,a in enumerate(c) if a]
            q.require(len(nz)==1,'ordinary inequality slack')
            i=nz[0];n=remainder[i]/c[i]
            q.require(n.denominator==1 and n>=0,'nonnegative integer budget slack')
            slacks.append(int(n));remainder[i]=0
        q.require(not any(remainder),'all exact Gram, moment, STS and primary-order equations')
        orbitcounts=[0]*len(orbits)
        for label,n in zip(labels,x):orbitcounts[label['orbit']]+=n*label['multiplicity_unit']
        values=[F(a)+sum(n*F(c[i]) for n,c in zip(orbitcounts,V['orbits'])) for i,a in enumerate(V['known'])]
        q.require(all(a==0 for a in values[1::2]),'all low Verlinde irrational components vanish')
        q.require(all(a.denominator==1 and a>=0 for a in values[::2]),'all low Verlinde coefficients are nonnegative integers')
        q.require(list(map(int,values[::2]))==result['verlinde_coefficients'],'stored low Verlinde values')
        if data.get('words'):
            sys.path.insert(0,str(e.HERE.parent/'computation'))
            from word_coefficients import coefficients
            C=coefficients(table,{'low':low,'orbits':orbits},data['words'])
            values=[F(a)+sum(n*F(c[i]) for n,c in zip(orbitcounts,C['orbits'])) for i,a in enumerate(C['known'])]
            q.require(all(a==0 for a in values[1::2]) and all(a.denominator==1 and a>=0 for a in values[::2]),'all supplied word multiplicities are nonnegative integers')
            q.require(list(map(int,values[::2]))==result['word_multiplicities'],'stored word multiplicities')
        rank=7+sum(n*len(orb) for n,orb in zip(orbitcounts,orbits))
        results.append({'case':result['case'],'rank':rank,'phase_variables':len(labels),'exact_equations':len(rhs),'low_verlinde_triples':len(V['triples']),'word_tests':len(data.get('words',[])),'integer_norm_cuts':len(data.get('norm_cut_records',[])),'status':'PASS_necessary_data_only'})
    q.require(bool(results),'at least one claimed feasible witness')
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_sha256':data['source_sha256'],'results':results,'optimized_python':not __debug__}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('files',nargs='+');args=p.parse_args()
    for name in args.files:print(json.dumps(verify(Path(name))),flush=True)
