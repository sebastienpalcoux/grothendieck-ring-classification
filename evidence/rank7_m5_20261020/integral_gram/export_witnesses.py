"""Replay and export feasible integer necessary-data witnesses, not models."""
import hashlib
import json
import pathlib
import sys
import itertools

HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as m
q=m.q


def run(rid):
    domains=json.loads((HERE/(rid+'_domains.json')).read_text())
    records=[]
    if rid=='R7_5_5039':
        for r in json.loads((HERE/(rid+'_verlinde_discovery.json')).read_text())['results']:
            if r.get('exact_feasible') and not any(w['index']==r['index'] for w in records):records.append(r)
    else:
        data=json.loads((HERE/(rid+'_branch_mip_8.json')).read_text())
        allocations=json.loads((HERE/(rid+'_active_8.json')).read_text())['branches']
        for r in data:
            if not r.get('exact_feasible'):continue
            system=json.loads((HERE/(rid+'_system_8_'+str(r['case'])+'.json')).read_text())
            support={j:n for j,n in r['support']}
            support.update({j:n for j,n in allocations[r['branch']]})
            selection=system['phase_selection'];multipliers=system['multipliers']
            actual=[(selection[j],n*multipliers[selection[j]]) for j,n in sorted(support.items()) if j<len(selection)]
            records.append({'index':8,'case':r['case'],'branch':r['branch'],'actual_support':actual})
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid)
    table=m.ExactQuadraticCharacterTable(N,d,5)
    characters,codegrees,pairs=m.char_data(table)
    witnesses=[]
    for rec in records:
        dom=next(dom for dom in domains if dom['low_index']==rec['index'])
        low=[tuple(v) for v in dom['low']];case=dom['cases'][rec['case']]
        label=case['label'];sign=case['sign']
        q.require(tuple(label) in table.assignments([(1,0,0,0,0,0,0)]+low),'exact character labelling')
        orbits=[[(tuple(v),tuple(g),tuple(z)) for v,g,z in orb] for orb in dom['orbits']]
        delta,phase_map=m.saturated_phase_map(table,low,label,orbits,rid)
        bound=[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in low) for i,j in q.base.PAIRS]
        known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        rhs=m.augmented_rhs(bound,known,D,sign,low,label,characters,codegrees,pairs,table.K)
        cols=m.augmented_columns(orbits,D,characters,pairs,table.K)
        total=[0]*len(rhs);objects=[]
        for ix,count in rec['actual_support']:
            oi,pi=divmod(ix,10);orbit=orbits[oi];phase=q.phase_vertices()[pi]
            q.require(phase in phase_map[oi],'saturated phase support')
            v=(0,)+tuple(orbit[0][0]);tv=T(v)
            if all(x<=0 for x in tv):tv=tuple(-x for x in tv)
            dv=tuple(v[i] for i in T.dual)
            q.require(pi<4 or (tv!=v and tv!=dv) or count%2==0,'Galois phase parity')
            q.require(type(count)is int and count>0,'positive integer multiplicity')
            rowset={(0,)+tuple(v) for v,_,z in orbit}
            for row in rowset:
                q.require(all(type(x)is int and x>=0 for x in row),'nonnegative integral restriction row')
                transformed=T(row)
                if all(x<=0 for x in transformed):transformed=tuple(-x for x in transformed)
                q.require(transformed in rowset and tuple(row[i] for i in T.dual) in rowset,'complete Galois and dual row orbit')
            total=[a+count*b for a,b in zip(total,cols[ix])]
            objects.append({'restriction_rows':[(0,)+tuple(row[0]) for row in orbit],
                            'multiplicity_per_row':count,'relative_traces_scaled_by_8':phase,
                            'dimensions':[row[2] for row in orbit]})
        q.require(total==rhs,'all exact Gram, two-indicator and STS equations')
        source_rows=[(v,1) for v in [(1,0,0,0,0,0,0)]+low]
        for obj in objects:
            source_rows.extend((tuple(v),obj['multiplicity_per_row']) for v in obj['restriction_rows'])
        K=table.K
        for v,count in source_rows:table.prepare(v)
        from spectral_induction import Spectrum
        high=[(v[1:],tuple(sum(v[i]*d[i][j] for i in range(7)) for j in (0,1))) for v,count in source_rows if v[0]==0]
        spectrum=Spectrum(table,[(1,0,0,0,0,0,0)]+low,high)
        q.require(not spectrum.forbidden and not spectrum.missing_low,'all central fusion eigenvalues are integral with complete Galois spectrum')
        triples=list(itertools.combinations_with_replacement([h for h in range(7) if h!=table.fp],3))
        fusion=[]
        for E,F,G in triples:
            value=table.D/(table.codegrees[E]*table.codegrees[F]*table.codegrees[G])*sum((K(count)*table.values[E,v]*table.values[F,v]*table.values[G,v]/table.dims[v] for v,count in source_rows),K.zero)
            scalar=K.to_sympy(value)
            q.require(scalar.is_Integer and scalar>=0,'nonnegative integer low Verlinde coefficient')
            fusion.append(int(scalar))
        phase_budget={}
        if rid=='R7_5_5039':
            for name,phases,limit in [('odd',{0,4,7},2),('twice_odd',{1,5,8},2),('four_times_odd',{2,6,9},4)]:
                value=sum(n*sum((v[0]-v[1])**2 for v,_,z in orbits[k//10]) for k,n in rec['actual_support'] if k%10 in phases)
                q.require(value<=limit,'conductor-eight phase budget')
                phase_budget[name]={'value':value,'upper_bound':limit}
        payload={'id':rid,'status':'feasible_necessary_data_only','source_sha256':q.tensor_hash(N),
                 'low_index':rec['index'],'low_rows':[(1,0,0,0,0,0,0)]+low,
                 'character_labelling':label,'second_indicators':sign,'saturation_sign':delta,
                 'high_row_orbit_phase_multiplicities':objects,
                 'low_verlinde_triples':triples,'low_verlinde_coefficients':fusion,'conductor_eight_phase_budgets':phase_budget,
                 'total_center_rank':7+sum(x['multiplicity_per_row']*len(x['restriction_rows']) for x in objects),
                 'equations_checked':len(rhs),'optimizer_used_in_replay':False,'branch':rec.get('branch')}
        serialized=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
        payload['witness_sha256']=hashlib.sha256(serialized).hexdigest()
        witnesses.append(payload)
    target=HERE/(rid+'_integer_witnesses.json')
    target.write_text(json.dumps(witnesses,indent=2)+'\n')
    print(json.dumps({'id':rid,'status':'PASS','witnesses':len(witnesses),'ranks':[w['total_center_rank'] for w in witnesses],'optimized_python':not __debug__}))


if __name__=='__main__':
    for rid in q.CONFIG:run(rid)
