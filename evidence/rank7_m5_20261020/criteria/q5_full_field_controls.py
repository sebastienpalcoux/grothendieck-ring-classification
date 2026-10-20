"""Exact projection controls for the full multiquadratic moment engine."""
import json
from pathlib import Path
import sys

import q5_full_field as f
m=f.m;q=f.q
from full_source_phases import phase_records


def run():
    directory=Path(__file__).resolve().parent.parent/'integral_gram'
    records=phase_records('F8');outputs=[]
    for rid,index,branch in [('R7_5_3895',8,None),('R7_5_5039',3,None),('R7_5_5039',3,0),('R7_5_5039',3,2)]:
        dom=next(x for x in json.loads((directory/(rid+'_domains.json')).read_text()) if x['low_index']==index)
        N=next(row['tensor'] for row in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if row['id']==rid)
        d,D,B,zs,T,signs=q.source_data(N,rid)
        table=m.ExactQuadraticCharacterTable(N,d,5)
        low=[tuple(v) for v in dom['low']]
        orbits=[[(tuple(v),tuple(g),tuple(z)) for v,g,z in orbit] for orbit in dom['orbits']]
        case=next(c for c in dom['cases'] if -1 not in c['sign'])
        chars,degrees,pairs=m.char_data(table)
        original=m.augmented_columns(orbits,D,chars,pairs,table.K)
        cols,rhs,labels=f.build_system(table,low,case['label'],orbits,dom['bound'],D,zs,case['sign'],T,records,rid,chi8_branch=branch)
        # All exact coefficients in these cases are integral already; row
        # denominator clearing is checked against a projected right side as
        # well as columns, so a hidden scale change cannot silently pass.
        projection=list(range(21))+[21+8*j+k for j in range(6+6+len(pairs)) for k in (0,1)]
        known=[tuple(sum(v[i+1]*z[k] for v,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        oldrhs=m.augmented_rhs(dom['bound'],known,D,case['sign'],low,case['label'],chars,degrees,pairs,table.K)
        expected_columns=[]
        for column,label in zip(cols,labels):
            record=records[label['phase']];phase=record['scaled8']
            if branch is not None:
                weight=sum((v[0]-v[1])**2 for v,_,_ in orbits[label['orbit']])
                orders=record['orders']
                if weight:
                    q.require((orders and 40%orders[0]==0) if branch==2 else (not orders or orders[0] in (16,80)),'sign-safe active twist provenance')
                    if not orders:q.require(label['multiplicity_unit']%4==0,'active zero four-cycle divisibility')
                order=orders[0] if orders else 0
                two_part=order//5 if order and order%5==0 else order
                q.require(column[-6:-2]==[weight*label['multiplicity_unit']*int(two_part==k) for k in (1,2,4,8)],'four exact mass coefficients')
            old_phase=(phase[0],phase[1],phase[8],phase[9])
            pi=q.phase_vertices().index(old_phase)
            expected_columns.append([label['multiplicity_unit']*x for x in original[10*label['orbit']+pi]])
        normalized,normalized_rhs=m.integral_system(expected_columns,oldrhs)
        q.require([rhs[i] for i in projection]==normalized_rhs,'full-field target projects to established real-field target')
        for column,expected in zip(cols,normalized):
            q.require([column[i] for i in projection]==expected,'full-field column projects exactly, including multiplicity factor')
        if branch is not None:
            q.require(len(cols)==len(labels)+2,'only prime-five inequality slacks; none for exact conductor-eight masses')
            q.require(rhs[-6:-2]==[branch,branch,2*branch,4*branch],'four exact mass targets')
        q.require(rhs[-2:]==[24,128],'visible prime-five mass bounds')
        outputs.append({'id':rid,'low_index':index,'chi8_branch':branch,'columns_checked':len(labels),'projected_equations':len(projection)})
    result={'status':'PASS','controls':outputs,'optimized_python':not __debug__}
    (f.HERE/'q5_full_field_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':run()
