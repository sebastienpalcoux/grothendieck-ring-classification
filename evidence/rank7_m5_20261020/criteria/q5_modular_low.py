"""Full twist-one low-block STS equations with exact paired moment columns."""
import argparse
import itertools
import json
import math
import time
from fractions import Fraction as F

import sympy as s

import q5_center_trace as q
from exact_quadratic_characters import ExactQuadraticCharacterTable


def phases():
    return q.phase_vertices()


def quadratic_coeff(value,K):
    value=s.expand(K.to_sympy(value));b=value.coeff(s.sqrt(5));a=s.simplify(value-b*s.sqrt(5))
    if not (a.is_Rational and b.is_Rational):return None
    return F(a),F(b)


def char_data(table):
    rows={h:list(row) for h,row in enumerate(table.rows)}
    return rows,{h:table.codegrees[h] for h in rows},list(itertools.combinations_with_replacement(rows,2))


def evaluate_character(row,v,K):
    return sum((K(c)*x for c,x in zip(v,row)),K.zero)


def trace_coeff(value,K):
    expression=s.expand(K.to_sympy(value))
    real=s.simplify((expression+s.conjugate(expression))/2)
    b=s.expand(real).coeff(s.sqrt(5));a=s.simplify(real-b*s.sqrt(5))
    q.require(a.is_Rational and b.is_Rational,'relative trace lands in dimension field')
    return F(a),F(b)


def augmented_columns(orbits,D,characters,pairs,K,phase_map=None):
    cols=q.trace_columns(orbits,D,phase_map=phase_map)
    idx=0
    for orbit_index,orbit in enumerate(orbits):
        values=[{h:evaluate_character(row,(0,)+v,K) for h,row in characters.items()} for v,_,_ in orbit]
        products={pair:sum((data[pair[0]]*data[pair[1]] for data in values),K.zero) for pair in pairs}
        coefficients={pair:quadratic_coeff(value,K) for pair,value in products.items()}
        q.require(all(value is not None for value in coefficients.values()), 'dual orbit cancels nonreal character coefficients')
        for ph in (phases() if phase_map is None else phase_map[orbit_index]):
            for pair in pairs:cols[idx].extend(q.base.mul(coefficients[pair],ph[:2],5))
            idx+=1
    q.require(idx==len(cols),'phase column correspondence')
    return cols


def augmented_rhs(bound,known,D,sign,low,label,characters,codegrees,pairs,K):
    rhs=[8*x for x in bound]+[-8*x for z in known for x in z]+[8*(D[k]*sign[i+1]-known[i][k]) for i in range(6) for k in range(2)]
    all_low=[(1,0,0,0,0,0,0)]+low
    assigned={h:v for h,v in zip(label,all_low)}
    vals=[{h:evaluate_character(row,v,K) for h,row in characters.items()} for v in all_low]
    for E,G in pairs:
        right=codegrees[G]*evaluate_character(characters[E],assigned[G],K)
        value=right-sum((row[E]*row[G] for row in vals),K.zero)
        rhs.extend(8*z for z in trace_coeff(value,K))
    return rhs


def saturated_phase_map(table,low,label,orbits,rid):
    K=table.K;sqrt5=K.from_sympy(s.sqrt(5))
    indices=[h for h,f in enumerate(table.codegrees) if f==K(5)]
    q.require(len(indices)==2,'two formal-codegree-five characters')
    E,G=indices
    assigned={h:v for h,v in zip(label,[(1,0,0,0,0,0,0)]+low)}
    column=[(evaluate_character(row,assigned[E],K)-evaluate_character(row,assigned[G],K))/table.codegrees[h]
            for h,row in enumerate(table.rows)]
    delta=column[E]*sqrt5
    q.require(delta in (K.one,-K.one),'saturated conductor-five eigenvalue')
    q.require(all(value==delta/sqrt5*K(int(h==E)-int(h==G)) for h,value in enumerate(column)), 'full induced-unit compression saturation')
    delta=1 if delta==K.one else -1
    differing=[i for i in range(7) if table.rows[E][i]!=table.rows[G][i]]
    q.require(differing==([4,5] if rid=='R7_5_3895' else [3,4]), 'nonzero saturated S-coordinate support')
    a,b=differing
    q.require(table.rows[E][a]-table.rows[G][a]==-(table.rows[E][b]-table.rows[G][b]), 'difference coordinate')
    phase_map=[]
    for orbit in orbits:
        active=[v[a-1]!=v[b-1] for v,_,_ in orbit]
        q.require(len(set(active))==1,'saturation support invariant under row orbit')
        phase_map.append([(-2,2*delta,-2,-2*delta)] if active[0] else phases())
    return delta,phase_map


def integral_system(columns,rhs):
    scales=[math.lcm(F(b).denominator,*(F(c[i]).denominator for c in columns)) for i,b in enumerate(rhs)]
    cols=[[int(F(v)*scales[i]) for i,v in enumerate(c)] for c in columns]
    target=[int(F(v)*scales[i]) for i,v in enumerate(rhs)]
    return cols,target


def partial_eight_constraints(columns,rhs,orbits,phase_map,low):
    """Audited conductor-eight exact two-primary order budgets 2, 2, 4.

    Zero relative phase is omitted even when its true twist has low 2-part;
    that omission weakens the necessary upper bound and is therefore safe.
    """
    phases0=phases()
    allowed=tuple({phases0[j] for j in group} for group in ((0,4,7),(1,5,8),(2,6,9)))
    result=[]
    index=0
    for orbit,phase_list in zip(orbits,phase_map):
        weight=sum((v[0]-v[1])**2 for v,_,_ in orbit)
        for phase in phase_list:
            result.append(list(columns[index])+[weight*int(phase in group) for group in allowed])
            index+=1
    q.require(index==len(columns),'partial compression phase correspondence')
    known=sum((v[1]-v[2])**2 for v in low)
    target=list(rhs)+[2-known,2,4]
    for j in range(3):
        slack=[0]*len(target);slack[-3+j]=1;result.append(slack)
    # These ten phases are exact Cauchy-restricted relative traces, so an
    # orbit/phase coefficient is an actual nonnegative integer. A coefficient
    # exceeding any nonnegative budget forces its variable to vanish.
    nonnegative=list(range(21))+list(range(len(target)-3,len(target)))
    q.require(all(target[i]>=0 and all(c[i]>=0 for c in result) for i in nonnegative),'nonnegative integer budgets')
    result=[c for c in result if all(c[i]<=target[i] for i in nonnegative)]
    return result,target


def run(rid,partial_eight=False):
    start=time.monotonic()
    N=next(row['tensor'] for row in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if row['id']==rid)
    d,D,B,zs,transport,signs=q.source_data(N,rid)
    table=ExactQuadraticCharacterTable(N,d,5)
    characters,codegrees,epairs=char_data(table)
    lows,nodes,forced=q.enumerate_low(B,d,zs,transport);rows=q.global_rows(B,d)
    pool=[];branches=[];unresolved=[]
    print(json.dumps({'event':'domain','id':rid,'lows':len(lows),'rows':len(rows),'field_characters':list(characters),'seconds':time.monotonic()-start}),flush=True)
    for ix,low in enumerate(lows):
        labels=table.assignments([(1,0,0,0,0,0,0)]+low)
        if not labels:
            branches.append({'low':low,'labellings':[]});continue
        if partial_eight:
            weight=sum((v[1]-v[2])**2 for v in low)
            if weight>2:
                branches.append({'low':low,'labellings':[list(z) for z in labels],'partial_eight_low_budget':{'weight':weight,'upper_bound':2}})
                print(json.dumps({'event':'partial_eight_low_excluded','index':ix,'weight':weight,'upper_bound':2}),flush=True)
                continue
        R,bound,orbits,rank=q.compatible_orbits(rows,B,low,transport)
        from spectral_induction import Spectrum
        spectrum=Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(v,z) for orbit in orbits for v,_,z in orbit])
        if spectrum.missing_low:
            branches.append({'low':low,'labellings':[list(z) for z in labels],'spectrum':spectrum.metadata()})
            print(json.dumps({'event':'spectral_low_excluded','index':ix,'missing_low':spectrum.missing_low}),flush=True)
            continue
        forbidden=set(map(tuple,spectrum.forbidden))
        orbits=[orbit for orbit in orbits if all(v not in forbidden for v,_,_ in orbit)]
        print(json.dumps({'event':'spectral_rows','index':ix,'remaining_orbits':len(orbits),'forbidden_rows':len(forbidden)}),flush=True)
        
        known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        cases=[];columns_by_sign={}
        for label in labels:
            delta,phase_map=saturated_phase_map(table,low,label,orbits,rid)
            if delta not in columns_by_sign:
                columns_by_sign[delta]=augmented_columns(orbits,D,characters,epairs,table.K,phase_map=phase_map)
            columns=columns_by_sign[delta]
            for sign in signs:
                rhs=augmented_rhs(bound,known,D,sign,low,label,characters,codegrees,epairs,table.K)
                augmented,values=partial_eight_constraints(columns,rhs,orbits,phase_map,low) if partial_eight else (columns,rhs)
                cols,target=integral_system(augmented,values)
                sep=q.separate(cols,target,pool)
                cases.append({'labelling':list(label),'indicators':sign,'separator':sep,'saturated_sign':delta})
                if sep is None:unresolved.append({'low_index':ix,'labelling':list(label),'indicators':sign,'orbits':len(orbits)})
        branches.append({'low':low,'labellings':[list(z) for z in labels],'spectrum':spectrum.metadata(),'cases':cases})
        print(json.dumps({'event':'frame','index':ix,'labels':len(labels),'orbits':len(orbits),'pool':len(pool),'unresolved':len(unresolved)}),flush=True)
    result={'id':rid,'scope':'pseudo_unitary','status':'candidate_exclusion' if not unresolved else 'no_exclusion',
            'exponent_prime_restriction':[2,5],'codegree_five_saturation':True,'joint_spectrum_integrality':True,'conductor_eight_exact_order_budgets':([2,2,4] if partial_eight else []),'source_sha256':q.tensor_hash(N),'character_table':table.metadata(),'field_characters':list(characters),
            'low_frames':len(lows),'global_rows':len(rows),'separators':pool,'branches':branches,'unresolved':unresolved,
            'seconds':time.monotonic()-start}
    (q.HERE/(rid+'_q5_modular_low'+('_partial8' if partial_eight else '')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('character_table','separators','branches','unresolved')}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('ring',choices=q.CONFIG);parser.add_argument('--partial-eight',action='store_true');args=parser.parse_args()
    q.require(not args.partial_eight or args.ring=='R7_5_5039','conductor eight applies only to nonreal character pair')
    run(args.ring,args.partial_eight)
