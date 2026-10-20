"""Exact conditional C4-character splitting of the four surviving c0 packets.

The surrounding active/phase enumeration is a separate proof obligation.
This verifier binds and exhausts all five integral C4 choices in each input
phase assignment. Discovery can use HNF/LP; replay uses neither.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'computation'))
import inactive_lattice as lat
import q5_cyclic_eight_search as s
q=s.q


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run(case,replay=False):
    start=time.monotonic()
    systempath=HERE/f'R7_5_5039_c8_case{case}_chi8_0_system.json'
    branchespath=HERE.parent/'integral_gram'/f'R7_5_5039_c8_case{case}_chi8_0_phase_gram.json'
    outputpath=HERE/f'R7_5_5039_c8_case{case}_chi8_0_rotation_split.json'
    system=json.loads(systempath.read_text());branches=json.loads(branchespath.read_text())
    old=json.loads(outputpath.read_text()) if replay else None
    if replay:q.require(old['system_sha256']==sha(systempath) and old['branches_sha256']==sha(branchespath),'bound split inputs')
    cols=system['columns'];rhs=system['rhs'];labels=system['phase_labels'];orbits=system['orbits']
    active={j for j,label in enumerate(labels) if any(v[0]!=v[1] for v,g,z in orbits[label['orbit']])}
    ob=system['cyclic_four'][0]
    q.require(ob['source_object']==1 and ob['A']==4 and ob['B']==0,'C4-X1 has exactly five integer possibilities')
    r,rb,t,tb=ob['variables'];fixed={r,rb,t,tb};results=[];pool=[];basis_cache={}
    for k,branch in enumerate(branches):
        support=dict(branch['support'])
        q.require(set(support)<=active and all(type(n)is int and n>=0 for n in support.values()),'integral active phase assignment')
        remainder=[b-sum(cols[j][i]*n for j,n in support.items()) for i,b in enumerate(rhs)]
        q.require(all(b>=0 for b in remainder[:21]),'nonnegative residual Gram entries')
        pair_index={tuple(sorted(pair)):k for k,pair in enumerate(q.base.PAIRS)}
        gram_cache={}
        def admissible(col):
            key=tuple(col[:21])
            if key not in gram_cache:
                residual=[remainder[i]-col[i] for i in range(21)]
                R=[[residual[pair_index[tuple(sorted((a,b)))]] for b in range(6)] for a in range(6)]
                gram_cache[key]=not any(x<0 for x in residual) and q.base.psd(R)
            return gram_cache[key]
        keep=[j for j,col in enumerate(cols) if j not in active and admissible(col)]
        q.require(keep==branch['kept'],'complete exact unit Gram pruning')
        q.require(fixed<=set(keep),'all C4 variables are present')
        keep=[j for j in keep if j not in fixed]
        inactive=[cols[j] for j in keep]
        target=[b-4*cols[rb][i] for i,b in enumerate(remainder)]
        delta=[a-b for a,b in zip(cols[r],cols[rb])]
        if replay:
            record=old['branches'][k]
            q.require(record['phase_case']==branch['phase_case'] and record['support']==branch['support'],'exact branch order')
            prepared=lat.verify_prepared(record['prepared'],inactive,target,[delta])
        else:
            key=tuple(keep)
            basis=basis_cache.get(key)
            prepared=lat.prepare(inactive,target,[delta],basis=basis)
            basis_cache[key]=prepared['basis']
            record={'phase_case':branch['phase_case'],'support':branch['support'],'kept_after_rotation':len(keep),'prepared':prepared,'choices':[]}
        choices=[]
        for value in range(5):
            passes,why=lat.check_counts(prepared,[value],return_failure=True)
            choice={'r':value,'lattice_pass':passes,'failure':why}
            if passes:
                residual=[b-value*a for b,a in zip(target,delta)]
                if replay:
                    saved=record['choices'][value]
                    index=saved.get('separator')
                    if index is not None:
                        ray=old['separators'][index]
                        q.require(len(ray)==len(rhs) and all(type(x)is int for x in ray),'integral Farkas covector')
                        q.require(q.base.dot(residual,ray)<0 and all(q.base.dot(c,ray)>=0 for c in inactive),'exact conditional Farkas contradiction')
                    choice['separator']=index
                else:choice['separator']=q.separate(inactive,residual,pool)
            if replay:q.require(choice==record['choices'][value],'same exact branch verdict')
            choices.append(choice)
            print(json.dumps({'phase_case':branch['phase_case'],**choice}),flush=True)
        record['choices']=choices;results.append(record)
    unresolved=[{'phase_case':record['phase_case'],'r':choice['r']} for record in results for choice in record['choices'] if choice['lattice_pass'] and choice.get('separator') is None]
    out={'status':'conditional_exclusion' if not unresolved else 'incomplete','scope':'Only the supplied phase assignments; their exhaustiveness is verified separately.',
         'system_sha256':sha(systempath),'branches_sha256':sha(branchespath),'case':case,'branches':results,'separators':old['separators'] if replay else pool,'unresolved':unresolved}
    if not replay:outputpath.write_text(json.dumps(out)+'\n')
    else:q.require(out==old,'exact replay output')
    receipt={'status':'PASS' if replay else 'COMPLETE','case':case,'conditional_closed':not unresolved,'unresolved':unresolved,'integer_choices':5*len(branches),'seconds':time.monotonic()-start,'optimized_python':not __debug__}
    if replay:(HERE/f'R7_5_5039_c8_case{case}_chi8_0_rotation_replay_{"normal" if __debug__ else "optimized"}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',type=int,choices=[0,1],required=True);parser.add_argument('--replay',action='store_true');a=parser.parse_args();run(a.case,a.replay)
