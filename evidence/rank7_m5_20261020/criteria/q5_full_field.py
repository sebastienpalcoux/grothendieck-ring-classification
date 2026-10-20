"""Discovery with all two-moment traces in Q(sqrt(5),sqrt(-2)).

The phase source independently verifies the cyclotomic arithmetic. Returned
feasible data are only necessary data, never a construction of a category.
"""
import json
import math
from pathlib import Path
import sys
import time

import q5_modular_low as m
q=m.q
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'models/sqrt5'))


def multiply_real(value,phase):
    return [x for j in range(0,len(phase),2) for x in q.base.mul(value,phase[j:j+2],5)]


def build_system(table,low,label,orbits,bound,D,zs,sign,transport,records,rid='R7_5_5039',chi8_branch=None):
    low=[tuple(v) for v in low]
    orbits=[[(tuple(v),tuple(gram),tuple(z)) for v,gram,z in orbit] for orbit in orbits]
    K=table.K
    characters,codegrees,pairs=m.char_data(table)
    delta,allowed=m.saturated_phase_map(table,low,label,orbits,rid)
    width=len(records[0]['scaled8'])//2
    q.require(width in (4,8) and all(len(rec['scaled8'])==2*width for rec in records),'uniform multiquadratic phase width')
    fourth=all('fourth_scaled8' in rec for rec in records)
    q.require(not fourth or (width==8 and all(len(rec['fourth_scaled8'])==8 for rec in records)),'uniform fourth-moment phase metadata')
    eighth=all('eighth_scaled8' in rec for rec in records)
    q.require(not eighth or (fourth and all(len(rec['eighth_scaled8'])==8 for rec in records)),'uniform eighth-moment phase metadata')
    padding=[0]*(width-2)
    known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
    rhs=[8*x for x in bound]
    rhs += [value for pair in known for value in [-8*pair[0],-8*pair[1]]+padding]
    rhs += [value for i,pair in enumerate(known) for value in [8*(D[0]*sign[i+1]-pair[0]),8*(D[1]*sign[i+1]-pair[1])]+padding]
    all_low=[(1,0,0,0,0,0,0)]+low
    assigned=dict(zip(label,all_low))
    values=[{h:m.evaluate_character(row,v,K) for h,row in characters.items()} for v in all_low]
    for E,F in pairs:
        right=codegrees[F]*m.evaluate_character(characters[E],assigned[F],K)
        remainder=right-sum((v[E]*v[F] for v in values),K.zero)
        pair=m.quadratic_coeff(remainder,K)
        q.require(pair is not None,'surviving low STS right side lies in real dimension field')
        rhs += [8*pair[0],8*pair[1]]+padding
    known_weight=sum((v[1]-v[2])**2 for v in low)
    q.require(chi8_branch is None or (rid=='R7_5_5039' and width==8 and chi8_branch in (0,2)),'valid sign-safe conductor-eight branch')
    chi_budget_count=(4 if chi8_branch is not None else 3) if rid=='R7_5_5039' else 0
    budget_count=chi_budget_count+2
    if chi_budget_count:
        q.require(known_weight<=2,'conductor-eight low compression')
        rhs += ([chi8_branch-known_weight,chi8_branch,2*chi8_branch,4*chi8_branch]
                if chi8_branch is not None else [2-known_weight,2,4])
    fp_weights=([2,1,1,2,-2,-2,0] if rid=='R7_5_3895' else [2,1,1,-2,-2,2,0])
    known_fp_weight=sum(sum(a*b for a,b in zip(fp_weights,v))**2 for v in [(1,0,0,0,0,0,0)]+low)
    q.require(known_fp_weight==8,'exact induced-unit FP-difference weight')
    rhs += [32-known_fp_weight,128]
    Kphases=q.phase_vertices()
    buckets=tuple({Kphases[j] for j in group} for group in ((0,4,7),(1,5,8),(2,6,9)))
    columns=[];labels=[]
    for oi,orbit in enumerate(orbits):
        gram=[sum(row[1][i] for row in orbit) for i in range(21)]
        weighted=[tuple(sum(v[i]*z[k] for v,_,z in orbit) for k in range(2)) for i in range(6)]
        vals=[{h:m.evaluate_character(row,(0,)+v,K) for h,row in characters.items()} for v,_,_ in orbit]
        products=[m.quadratic_coeff(sum((v[E]*v[F] for v in vals),K.zero),K) for E,F in pairs]
        q.require(all(x is not None for x in products),'dual orbit character products lie in real dimension field')
        weight=sum((v[0]-v[1])**2 for v,_,_ in orbit)
        fp_weight=sum(sum(a*b for a,b in zip(fp_weights,(0,)+v))**2 for v,_,_ in orbit)
        v=(0,)+orbit[0][0];tv=transport(v)
        if all(x<=0 for x in tv):tv=tuple(-x for x in tv)
        dv=tuple(v[i] for i in transport.dual)
        fixes=(tv==v or tv==dv)
        for pi,record in enumerate(records):
            phase=tuple(record['scaled8'])
            projection=(phase[0],phase[1],phase[width],phase[width+1])
            orders=record['orders']
            if weight and chi8_branch==2 and (not orders or 40%orders[0]):continue
            if weight and chi8_branch==0:
                active_orders=(16,80,32,160,64,320) if eighth else (16,80,32,160) if fourth else (16,80)
                if orders and orders[0] not in active_orders:continue
                if eighth and not orders:continue
            extra_indices=list(range(2,width))+list(range(width+2,2*width))
            if len(allowed[oi])==1 and (projection!=allowed[oi][0] or any(phase[j] for j in extra_indices)):continue
            factors=([8 if fourth else 4] if weight and chi8_branch==0 and not orders else
                     record.get('zero_semigroup') or [record.get('fixed_row_multiple') or 1])
            for factor in factors:
                # The source-fixed packet and the fifth-part inversion are
                # disjoint: a fixed/dual actual row needs both conjugate
                # Q(zeta_40) phase packets, not just their common lcm.
                # The positive +/-T transport, rather than raw T, is essential.
                if fixes and orders and orders[0]%5==0:
                    factor*=2
                # A hidden fifth-primary packet has a source-fixed 5-cycle;
                # inversion exchanges its two nonzero residues modulo five.
                # Pure high-two-primary packets retain their four-unit bound.
                if fixes and not orders and factor==5:
                    factor=10
                column=[8*x for x in gram]
                column += [x for value in weighted for x in multiply_real(value,phase[:width])]
                column += [x for value in weighted for x in multiply_real(value,phase[width:])]
                column += [x for value in products for x in multiply_real(value,phase[:width])]
                if chi8_branch is not None:
                    two_part=(orders[0]//5 if orders and orders[0]%5==0 else orders[0] if orders else 0)
                    column += [weight*int(two_part==order) for order in (1,2,4,8)]
                elif chi_budget_count:column += [weight*int(projection in bucket) for bucket in buckets]
                column += [fp_weight*int(bool(orders) and orders[0]%5!=0),fp_weight*int(bool(orders) and orders[0]%5==0)]
                column=[factor*x for x in column]
                columns.append(column);labels.append({'orbit':oi,'phase':pi,'multiplicity_unit':factor})
    nonnegative=list(range(21))+list(range(len(rhs)-budget_count,len(rhs)))
    q.require(all(rhs[i]>=0 and all(c[i]>=0 for c in columns) for i in nonnegative),'nonnegative integral budgets')
    keep=[j for j,c in enumerate(columns) if all(c[i]<=rhs[i] for i in nonnegative)]
    columns=[columns[j] for j in keep];labels=[labels[j] for j in keep]
    slack_indices=list(range(len(rhs)-2,len(rhs)))
    if chi8_branch is None:slack_indices=list(range(len(rhs)-budget_count,len(rhs)))
    for j in slack_indices:
        column=[0]*len(rhs);column[j]=1;columns.append(column)
    integer_columns,target=m.integral_system(columns,rhs)
    return integer_columns,target,labels


def run(rid='R7_5_5039',field='L4',chi8_branch=None):
    from full_source_phases import phase_records
    from spectral_induction import Spectrum
    records=phase_records(field=field)
    start=time.monotonic()
    tensor=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(tensor,rid)
    table=m.ExactQuadraticCharacterTable(tensor,d,5)
    lows,nodes,forced=q.enumerate_low(B,d,zs,T)
    rows=q.global_rows(B,d);pool=[];branches=[];unresolved=[]
    print(json.dumps({'event':'domain','lows':len(lows),'rows':len(rows),'phases':len(records),'seconds':time.monotonic()-start}),flush=True)
    for ix,low in enumerate(lows):
        labels=table.assignments([(1,0,0,0,0,0,0)]+low)
        branch={'low':low,'labellings':[list(label) for label in labels]}
        branches.append(branch)
        if not labels:continue
        weight=sum((v[1]-v[2])**2 for v in low)
        if rid=='R7_5_5039' and weight>2:
            branch['low_compression']={'weight':weight,'upper_bound':2};continue
        _,bound,orbits,_=q.compatible_orbits(rows,B,low,T)
        spectrum=Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(v,z) for orbit in orbits for v,_,z in orbit])
        branch['spectrum']=spectrum.metadata()
        if spectrum.missing_low:continue
        forbidden=set(map(tuple,spectrum.forbidden))
        orbits=[orbit for orbit in orbits if all(v not in forbidden for v,_,_ in orbit)]
        cases=[]
        for label in labels:
            for sign in signs:
                cols,rhs,varlabels=build_system(table,low,label,orbits,bound,D,zs,sign,T,records,rid,chi8_branch=chi8_branch)
                separator=q.separate(cols,rhs,pool)
                case={'labelling':list(label),'indicators':sign,'variables':len(cols),'separator':separator}
                cases.append(case)
                if separator is None:unresolved.append({'low_index':ix,**case})
                print(json.dumps({'event':'case','low':ix,**case}),flush=True)
        branch['cases']=cases
    result={'id':rid,'field':field,'chi8_branch':chi8_branch,'status':'candidate_exclusion' if not unresolved else 'no_exclusion','scope':'pseudo_unitary','source_sha256':q.tensor_hash(tensor),'phase_records':records,'low_frames':len(lows),'global_rows':len(rows),'branches':branches,'separators':pool,'unresolved':unresolved,'seconds':time.monotonic()-start}
    suffix='' if chi8_branch is None else '_c'+str(chi8_branch)
    (HERE/(rid+'_'+field+suffix+'_full_field_discovery.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('branches','separators','unresolved','phase_records')}),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('ring',choices=q.CONFIG);parser.add_argument('--field',choices=['L4','F8'],default='L4');parser.add_argument('--chi8-branch',type=int,choices=[0,2]);args=parser.parse_args()
    run(args.ring,args.field,args.chi8_branch)
