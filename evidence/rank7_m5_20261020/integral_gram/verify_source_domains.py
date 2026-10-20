"""Optimizer-free canonical-source replay of the q5 integral branch domains."""
import hashlib
import json
import time
from fractions import Fraction as F

import explore as e
import verlinde as v
import enumerate_active as a
from spectral_induction import Spectrum

q=e.q;m=e.m;HERE=e.HERE


def run():
    start=time.monotonic();rid='R7_5_3895'
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5)
    characters,codegrees,pairs=m.char_data(table)
    lows,nodes,forced=q.enumerate_low(B,d,zs,T);rows=q.global_rows(B,d)
    recorded=e.domains(rid);actual=[];systems=[]
    for ix,low in enumerate(lows):
        labels=table.assignments([(1,0,0,0,0,0,0)]+low)
        if not labels:continue
        dom=next((r for r in recorded if r['low_index']==ix),None)
        q.require(dom is not None,'every surviving low frame recorded')
        R,bound,orbits,rank=q.compatible_orbits(rows,B,low,T)
        columns=m.augmented_columns(orbits,D,characters,pairs,table.K)
        known=[tuple(sum(w[i+1]*z[k] for w,z in zip(low,zs)) for k in range(2)) for i in range(6)]
        cases=[]
        for label in labels:
            for sign in signs:
                rhs=m.augmented_rhs(bound,known,D,sign,low,label,characters,codegrees,pairs,table.K)
                cols,target=m.integral_system(columns,rhs)
                cases.append({'label':label,'sign':sign,'rhs':target})
        fresh={'low_index':ix,'low':low,'bound':bound,'orbits':orbits,'columns':cols,'cases':cases}
        q.require(json.loads(json.dumps(fresh))==dom,'all canonical low/high rows and exact STS columns match')
        actual.append(ix)
        V=v.coefficients(table,{'id':rid,'low_index':ix,'low':low,'orbits':orbits},use_cache=False)
        vc=[list(map(F,c)) for c in V['orbits']];vk=list(map(F,V['known']))
        spectrum=Spectrum(table,[(1,0,0,0,0,0,0)]+low,[(w,z) for orb in orbits for w,_,z in orb])
        q.require(not spectrum.missing_low,'low spectra survive necessary condition')
        forbidden=set(map(tuple,spectrum.forbidden));excluded={j for j,orb in enumerate(orbits) if any(w in forbidden for w,_,_ in orb)}
        mult=[]
        for orb in orbits:
            row=(0,)+orb[0][0];tr=T(row)
            if all(z<=0 for z in tr):tr=tuple(-z for z in tr)
            du=tuple(row[i] for i in T.dual)
            mult.extend([1]*4+[2 if tr==row or tr==du else 1]*6)
        for ci,case in enumerate(cases):
            if -1 in case['sign']:continue
            delta,phase_map=m.saturated_phase_map(table,low,case['label'],orbits,rid)
            phase=4 if delta==-1 else 7
            selection=[j for j in range(len(cols)) if j//10 not in excluded and
                       (all(w[3]==w[4] for w,_,z in orbits[j//10]) or j%10==phase)]
            matrix=[[mult[j]*F(x) for x in cols[j]]+[mult[j]*x for x in vc[j//10]] for j in selection]
            rhs=list(map(F,case['rhs']))+[-x for x in vk];old=len(case['rhs'])
            for ti in range(len(V['triples'])):
                col=[F(0)]*len(rhs);col[old+2*ti]=-1;matrix.append(col)
            matrix,rhs=m.integral_system(matrix,rhs)
            active=[j for j,k in enumerate(selection) if any(w[3]!=w[4] for w,_,z in orbits[k//10])]
            weights={j:sum((w[3]-w[4])**2 for w,_,z in orbits[selection[j]//10])*mult[selection[j]] for j in active}
            expected={'id':rid,'low_index':ix,'case':ci,'source_sha256':q.tensor_hash(N),'columns':matrix,'rhs':rhs,
                      'phase_selection':selection,'multipliers':mult,'active_variables':active,'active_weights':weights,'active_budget':8}
            path=HERE/(rid+'_system_'+str(ix)+'_'+str(ci)+'.json')
            q.require(json.loads(json.dumps(expected))==json.loads(path.read_text()),'entire integer system regenerated from source')
            systems.append({'low_index':ix,'case':ci,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        fresh_active=a.run(ix,write=False);old_active=json.loads((HERE/(rid+'_active_'+str(ix)+'.json')).read_text())
        for key in ('id','low_index','system_sha256','active_budget','statistics','branches'):
            q.require(fresh_active[key]==old_active[key],'complete active allocation enumeration')
        print(json.dumps({'event':'frame_verified','low_index':ix,'orbits':len(orbits),'active_branches':len(fresh_active['branches'])}),flush=True)
    q.require(actual==[6,8] and len(recorded)==2,'exact surviving low inventory')
    result={'id':rid,'status':'PASS','source_sha256':q.tensor_hash(N),'optimizer_used':False,'optimized_python':not __debug__,
            'low_frames':len(lows),'global_rows':len(rows),'surviving_frames':actual,'systems':systems,'seconds':time.monotonic()-start}
    path=HERE/('source_domain_replay_'+('normal' if __debug__ else 'optimized')+'.json')
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);return result


if __name__=='__main__':run()
