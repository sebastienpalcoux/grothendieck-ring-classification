"""Lift fixed F8 necessary data to coupled Q(zeta_40) phases.

Only a fixed witness is tested. No failure here excludes a source tensor.
The phase inventory is averaged over source-field-fixing square actions;
the nontrivial source Galois action changes BOTH row and phase.
"""
import argparse
import collections
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import sympy as s
import q5_modular_low as m

q=m.q
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'integral_gram'))
import explore as e


class Cyclotomic40:
    def __init__(self):
        self.x=s.Symbol('x')
        self.modulus=s.Poly(s.cyclotomic_poly(40,self.x),self.x,domain=s.QQ)
        self.powers=[self.vector(self.x**k) for k in range(40)]
        self.root5=self.vector(1+2*self.x**8+2*self.x**32)
        self.root5_powers=[self.vector((1+2*self.x**8+2*self.x**32)*self.x**k) for k in range(40)]
        root2=self.x**5+self.x**35
        root5=1+2*self.x**8+2*self.x**32
        self.f8_basis=[self.vector(a) for a in (1,root5,root2,root5*root2,
            self.x**10,self.x**10*root5,self.x**10*root2,self.x**10*root5*root2)]
        q.require(self.vector(root5**2)==tuple([F(5)]+[F(0)]*15),'sqrt-five embedding')
        q.require(self.vector(root2**2)==tuple([F(2)]+[F(0)]*15),'sqrt-two embedding')

    def vector(self,expression):
        p=s.Poly(expression,self.x,domain=s.QQ).rem(self.modulus)
        return tuple(F(p.nth(i)) for i in range(16))

    def from_f8(self,coefficients):
        return tuple(sum(F(c,8)*b[i] for c,b in zip(coefficients,self.f8_basis)) for i in range(16))

    def quad_times_power(self,ab,k):
        if k is None:return (F(0),)*16
        return tuple(F(ab[0])*a+F(ab[1])*b for a,b in zip(self.powers[k%40],self.root5_powers[k%40]))

    def phase(self,key):
        kind,k=key
        return (self.powers[k],self.powers[2*k%40]) if kind=='root' else ((F(0),)*16,self.powers[k]) if kind=='half' else ((F(0),)*16,)*2

    def phases(self):
        return [('root',k) for k in range(40)]+[('half',k) for k in range(1,40,2)]+[('zero',0)]

    @staticmethod
    def tau(key):return (key[0],9*key[1]%40)

    def inventory(self,records):
        groups=collections.defaultdict(list)
        projections={self.from_f8(r['scaled8'][:8])+self.from_f8(r['scaled8'][8:]):i for i,r in enumerate(records)}
        q.require(len(projections)==37,'distinct complete F8 phase inventory')
        for key in self.phases():
            p=self.phase(key);t=self.phase(self.tau(key))
            averaged=tuple((a+b)/2 for a,b in zip(p[0]+p[1],t[0]+t[1]))
            q.require(averaged in projections,'cyclotomic phase projects to recorded F8 phase')
            groups[projections[averaged]].append(key)
        q.require(len(groups)==37 and sum(map(len,groups.values()))==61,'complete 61 to 37 phase projection')
        return dict(groups)


def positive_transport(v,T):
    out=tuple(T(v))
    if all(a<=0 for a in out):out=tuple(-a for a in out)
    q.require(all(a>=0 and int(a)==a for a in out),'positive signed Galois transport')
    return tuple(map(int,out))


def diagonal_orbits(rows,phases,T):
    universe={(tuple(v),tuple(ph)) for v in rows for ph in phases}
    found=[]
    while universe:
        todo=[min(universe)];orbit=set()
        while todo:
            state=todo.pop()
            if state in orbit:continue
            v,ph=state;orbit.add(state)
            nexts=[(positive_transport(v,T),Cyclotomic40.tau(ph)),
                   (tuple(v[i] for i in T.dual),ph)]
            q.require(all(a in universe or a in orbit for a in nexts),'diagonal orbit stays in source domain')
            todo.extend(a for a in nexts if a not in orbit)
        universe-=orbit;found.append(sorted(orbit))
    return found


def build(path,result):
    data=json.loads(path.read_text());rid=data['id']
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    q.require(q.tensor_hash(N)==data['source_sha256'],'witness source hash')
    d,D,B,zs,T,signs=q.source_data(N,rid)
    table=m.ExactQuadraticCharacterTable(N,d,5);K=table.K
    low=[tuple(v) for v in data['low']];all_low=[(1,0,0,0,0,0,0)]+low
    dom=next(a for a in e.domains(rid) if a['low']==data['low'])
    case=dom['cases'][result['case']];label=case['label'];sign=case['sign']
    chars,codegrees,pairs=m.char_data(table)
    assigned=dict(zip(label,all_low))
    known=[tuple(sum(v[i]*sum(v[j]*d[j][k] for j in range(7)) for v in low) for k in range(2)) for i in range(1,7)]
    c=Cyclotomic40();lifts=c.inventory(data['phase_records'])
    rhs=[]
    for ab in known:rhs.extend(c.quad_times_power((-ab[0],-ab[1]),0))
    for i,ab in enumerate(known):rhs.extend(c.quad_times_power((D[0]*sign[i+1]-ab[0],D[1]*sign[i+1]-ab[1]),0))
    lowvals=[{h:m.evaluate_character(row,v,K) for h,row in chars.items()} for v in all_low]
    for E,G in pairs:
        remainder=codegrees[G]*m.evaluate_character(chars[E],assigned[G],K)-sum((r[E]*r[G] for r in lowvals),K.zero)
        ab=m.quadratic_coeff(remainder,K)
        q.require(ab is not None,'low STS right side is quadratic')
        rhs.extend(c.quad_times_power(ab,0))
    group_counts=collections.Counter()
    for item in result['support']:
        group_counts[item['orbit'],item['phase']]+=item['multiplicity_unit']*item['count']
    columns=[];labels=[];group_constraints=[]
    for (oi,pi),count in sorted(group_counts.items()):
        if not data['phase_records'][pi]['orders']:continue
        rows=[(0,)+tuple(row[0]) for row in data['orbits'][oi]]
        orbits=diagonal_orbits(rows,lifts[pi],T)
        positions=[]
        for states in orbits:
            kinds={ph[0] for _,ph in states};q.require(len(kinds)==1,'constant packet type')
            factor=2 if next(iter(kinds))=='half' else 1
            perrow=collections.Counter(v for v,ph in states)
            q.require(set(perrow)==set(rows) and len(set(perrow.values()))==1,'uniform projected row multiplicity')
            unit=factor*next(iter(perrow.values()))
            if unit>count:continue
            column=[F(0)]*len(rhs)
            byphase=collections.defaultdict(list)
            for v,ph in states:byphase[ph].append(v)
            for ph,vs in byphase.items():
                weighted=[tuple(sum(v[i]*sum(v[j]*d[j][k] for j in range(7)) for v in vs) for k in range(2)) for i in range(1,7)]
                values=[{h:m.evaluate_character(row,v,K) for h,row in chars.items()} for v in vs]
                products=[]
                for E,G in pairs:
                    ab=m.quadratic_coeff(sum((v[E]*v[G] for v in values),K.zero),K)
                    q.require(ab is not None,'duality-closed phase fiber makes STS coefficient quadratic')
                    products.append(ab)
                kind,k=ph
                exponents=(k,2*k%40) if kind=='root' else (None,k)
                addition=[v for ab in weighted for v in c.quad_times_power(ab,exponents[0])]
                addition += [v for ab in weighted for v in c.quad_times_power(ab,exponents[1])]
                addition += [v for ab in products for v in c.quad_times_power(ab,exponents[0])]
                column=[a+factor*b for a,b in zip(column,addition)]
            positions.append((len(columns),unit));columns.append(column)
            labels.append({'source_orbit':oi,'F8_phase':pi,'packet_size':factor,'per_row_unit':unit,
                'states':[{'row':v,'phase':ph} for v,ph in states]})
        group_constraints.append({'orbit':oi,'phase':pi,'target_per_row':count,'positions':positions})
    for group in group_constraints:
        coeff=dict(group['positions'])
        for j,col in enumerate(columns):col.append(F(coeff.get(j,0)))
        rhs.append(F(group['target_per_row']))
    cols,target=m.integral_system(columns,rhs)
    return cols,target,labels,group_constraints


def rational_consistency(columns,target):
    """Fraction Gaussian reduction with a replayable contradictory row combination."""
    basis={}
    for i,b in enumerate(target):
        row=[F(c[i]) for c in columns]+[F(b)];w={i:F(1)}
        for pivot,(prior,relation) in sorted(basis.items()):
            scale=row[pivot]
            if not scale:continue
            row=[a-scale*b for a,b in zip(row,prior)]
            for j,a in relation.items():
                w[j]=w.get(j,F(0))-scale*a
                if not w[j]:del w[j]
        pivot=next((j for j,a in enumerate(row[:-1]) if a),None)
        if pivot is None:
            if not row[-1]:continue
            q.require(all(sum(a*columns[k][j] for j,a in w.items())==0 for k in range(len(columns))), 'exact contradiction kills all columns')
            value=sum(a*target[j] for j,a in w.items())
            q.require(value!=0,'exact contradiction has nonzero right side')
            return {'consistent':False,'row_combination':[[j,str(a)] for j,a in sorted(w.items())],'contradiction':str(value)}
        scale=row[pivot];basis[pivot]=([a/scale for a in row],{j:a/scale for j,a in w.items()})
    return {'consistent':True,'rank':len(basis),'variables':len(columns)}


def run(path):
    data=json.loads(path.read_text());outputs=[]
    for result in data['results']:
        if not result.get('exact_feasible'):continue
        cols,rhs,labels,groups=build(path,result)
        status=rational_consistency(cols,rhs)
        record={'case':result['case'],'variables':len(cols),'equations':len(rhs),'rational_test':status,'group_constraints':groups}
        if status['consistent']:
            import numpy as np
            from scipy.optimize import Bounds,LinearConstraint,milp
            upper=[math.inf]*len(cols)
            for group in groups:
                for j,unit in group['positions']:upper[j]=group['target_per_row']//unit
            res=milp(np.zeros(len(cols)),integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),upper),
                     constraints=LinearConstraint(np.array(cols,dtype=float).T,rhs,rhs),options={'time_limit':60})
            record['milp_status']=int(res.status)
            if res.x is not None:
                counts=[round(float(z)) for z in res.x]
                q.require(all(z>=0 for z in counts) and all(sum(z*c[i] for z,c in zip(counts,cols))==b for i,b in enumerate(rhs)),'exact coupled-phase lift')
                record['status']='exact_lift_of_necessary_data'
                record['support']=[{**label,'count':z} for label,z in zip(labels,counts) if z]
            else:record['status']='no_lift_found_no_exact_integer_certificate'
        else:record['status']='fixed_witness_has_no_rational_lift'
        outputs.append(record)
        print(json.dumps({k:v for k,v in record.items() if k not in ('group_constraints','support')}),flush=True)
    output={'source_file':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'id':data['id'],
        'scope':'Fixed necessary-data witness lift only; no source-ring exclusion.',
        'phase_inventory':{'root40':40,'half80':20,'zero':1,'Galois_exponent':9},'results':outputs}
    destination=HERE/(path.stem+'_cyclotomic_lift.json')
    destination.write_text(json.dumps(output,indent=2)+'\n')
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('witness',type=Path);args=parser.parse_args();run(args.witness)
