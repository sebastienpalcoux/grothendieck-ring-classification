"""Exact conditional separation of the 50 by 4 c0/phi packet branches.

The finite active inventories and forced C4 character are separate source-
bound proof inputs. This module rebuilds each residual Gram pruning and
records only integer Farkas covectors; a failed proposal is left unresolved.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time
import q5_cyclic_eight_search as search

HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'
q=search.q
sys.path.insert(0,str(INPUT))
from chi8_phi_cross_allocations import psd, PAIRS


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run(case,replay=False):
    start=time.monotonic()
    source=HERE/f'R7_5_5039_c8_case{case}_chi8_0_system.json'
    phi_path=INPUT/f'R7_5_5039_c8_case{case}_chi8_0_phi_cross_allocations.json'
    chi_path=INPUT/f'R7_5_5039_c8_case{case}_chi8_0_system_phase_lattice.json'
    rotation_path=HERE/f'R7_5_5039_c8_case{case}_chi8_0_rotation_split.json'
    path=HERE/f'R7_5_5039_c8_case{case}_chi8_0_phi_exact_farkas.json'
    hashes={p.name:digest(p) for p in (source,phi_path,chi_path,rotation_path)}
    system=json.loads(source.read_text());phi_data=json.loads(phi_path.read_text());chi_data=json.loads(chi_path.read_text())
    rotation=json.loads(rotation_path.read_text())
    q.require(phi_data['system_sha256']==digest(source),'phi inventory binds exact system')
    q.require(chi_data['hashes']['system']==digest(source),'chi phase inventory binds exact system')
    chi_choices=[c for branch in chi_data['branches'] for c in branch['remaining']]
    q.require(len(chi_choices)==4 and len(phi_data['allocations'])==50,'complete conditional branch dimensions')
    q.require(rotation['system_sha256']==digest(source),'forced C4 proof binds exact system')
    q.require(rotation['unresolved']==[{'phase_case':i,'r':3} for i in range(4)],'all four packets force r=3')
    packet_key=lambda choice:tuple(sorted(tuple(pair) for pair in choice))
    q.require({packet_key(choice) for choice in chi_choices}=={packet_key(branch['support']) for branch in rotation['branches']},'forced C4 proof covers exactly these four chi packets')
    cols=system['columns'];target=system['rhs'];labels=system['phase_labels'];orbits=system['orbits']
    ob=system['cyclic_four'][0];q.require(ob['A']==4 and ob['B']==0,'forced C4 domain')
    fixed_c4=[[j,n] for j,n in zip(ob['variables'],(3,1,0,0)) if n]
    active={j for j,label in enumerate(labels) if any(v[0]!=v[1] or v[2]!=v[3] for v,g,z in orbits[label['orbit']])}|set(ob['variables'])
    inactive=[j for j in range(len(cols)) if j not in active]
    grams=[[label['multiplicity_unit']*sum(v[i]*v[k] for v,g,z in orbits[label['orbit']]) for i,k in PAIRS] for label in labels]
    q.require(all(all(type(j)is int and type(n)is int and 0<=j<len(labels) and n>=0 for j,n in choice) for choice in chi_choices+phi_data['allocations']),'integral phase allocations')
    chi_grams=[[sum(n*grams[j][i] for j,n in choice) for i in range(21)] for choice in chi_choices]
    q.require(all(g==chi_grams[0] for g in chi_grams),'four chi phase choices have identical raw Gram contribution')
    scales=[]
    for i in range(21):
        j=next(j for j in range(len(labels)) if grams[j][i])
        scale=F(cols[j][i],grams[j][i]);scales.append(scale)
        q.require(all(F(col[i])==scale*grams[j][i] for j,col in enumerate(cols[:len(labels)])),'exact Gram equation scale')
    bound=[F(target[i])/scales[i] for i in range(21)]
    old=json.loads(path.read_text()) if replay else None
    if replay:q.require(old['source_hashes']==hashes,'source-bound exact separator pool')
    pool=old['separators'] if replay else [];results=[]
    def write():
        out={'status':'conditional_exclusion' if len(results)==200 and all(r['separator'] is not None for r in results) else 'incomplete',
             'scope':'Only the exact supplied 50 by4 active branches, conditional on their exhaustive inventories and forced C4 proof.',
             'case':case,'source_hashes':hashes,'results':results,'separators':pool,
             'unresolved':[{'phi_allocation':r['phi_allocation'],'chi_choice':r['chi_choice']} for r in results if r['separator'] is None]}
        if not replay:path.write_text(json.dumps(out)+'\n')
        return out
    for ai,phi in enumerate(phi_data['allocations']):
        gram=[b-sum(n*grams[j][i] for j,n in phi+chi_choices[0]) for i,b in enumerate(bound)]
        q.require(min(gram)>=0 and psd(gram),'exact residual Gram')
        cache={}
        def admissible(j):
            if j>=len(labels):return True
            key=tuple(grams[j])
            if key not in cache:
                residual=[a-b for a,b in zip(gram,key)]
                cache[key]=min(residual)>=0 and psd(residual)
            return cache[key]
        keep=[j for j in inactive if admissible(j)]
        columns=[cols[j] for j in keep]
        for ci,chi in enumerate(chi_choices):
            fixed=phi+chi+fixed_c4
            q.require(all(j in active for j,n in fixed),'all fixed variables belong to active block')
            rhs=[b-sum(n*cols[j][i] for j,n in fixed) for i,b in enumerate(target)]
            if replay:
                rec=old['results'][4*ai+ci];sep=rec['separator']
                if sep is not None:
                    y=pool[sep]
                    q.require(len(y)==len(rhs) and all(type(v)is int for v in y),'integer separating functional')
                    q.require(q.base.dot(rhs,y)<0 and all(q.base.dot(c,y)>=0 for c in columns),'exact active-branch separation')
            else:sep=q.separate(columns,rhs,pool)
            rec={'phi_allocation':ai,'chi_choice':ci,'fixed':fixed,'kept':keep,'separator':sep}
            if replay:q.require(rec==old['results'][4*ai+ci],'exact reconstructed branch inventory')
            results.append(rec)
        write()
        print(json.dumps({'case':case,'phi_allocation':ai,'kept':len(keep),'separators':len(pool),'unresolved':sum(r['separator'] is None for r in results),'seconds':time.monotonic()-start}),flush=True)
    out=write()
    if replay:q.require(out==old,'replay matches complete certificate')
    receipt={'status':'PASS' if replay else 'COMPLETE','case':case,'exact_separated':sum(r['separator'] is not None for r in results),'unresolved':out['unresolved'],'separator_count':len(pool),'seconds':time.monotonic()-start,'optimized_python':not __debug__}
    if replay:(HERE/f'R7_5_5039_c8_case{case}_chi8_0_phi_farkas_replay_{"normal" if __debug__ else "optimized"}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--case',type=int,choices=[0,1],required=True);a.add_argument('--replay',action='store_true');arg=a.parse_args();run(arg.case,arg.replay)
