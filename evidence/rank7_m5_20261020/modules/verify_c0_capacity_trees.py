"""Independent raw-Gram reconstruction and complete conditional tree audit.

Pure API: verify_all(require_trees=True). Upstream low/phase/phi/C4 coverage
must also be replayed before this conditional result is a ring exclusion.
"""
import hashlib
import json
import math
from pathlib import Path
import sys
from verify_chi8_allocations import psd, require, digest

HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parents[1]
sys.path.insert(0,str(BASE/'computation'))
sys.path.insert(0,str(BASE/'models/sqrt5'))
import verify_c0_forced_eighth_packet as forced_proof


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def subtract(A,G,n=1):
    return [[x-n*G[i][j] for j,x in enumerate(row)] for i,row in enumerate(A)]


def admissible(A):
    return all(x>=0 for row in A for x in row) and psd(A)


def replay(A,b,node,bounds=None):
    """Standard-library replay, with no optimizer imported or called."""
    bounds={} if bounds is None else bounds
    if 'y' in node:
        inequalities=[]
        for j,(low,high) in sorted(bounds.items()):
            if low>0:inequalities.append((j,-1,low))
            if high is not None:inequalities.append((j,1,high))
        width=len(A[0]);extra=len(inequalities)
        matrix=[row+[0]*extra for row in A];rhs=b[:]
        for k,(j,sign,value) in enumerate(inequalities):
            row=[0]*(width+extra);row[j]=1;row[width+k]=sign
            matrix.append(row);rhs.append(value)
        y=node['y']
        require(len(y)==len(rhs) and all(type(x) is int for x in y),'integer leaf covector')
        require(all(sum(matrix[i][j]*y[i] for i in range(len(rhs)))>=0
                    for j in range(width+extra)),'every nonnegative variable has a nonnegative leaf coefficient')
        require(sum(x*z for x,z in zip(rhs,y))<0,'strict leaf contradiction')
        return 1
    j=node['variable'];k=node['floor']
    require(type(j) is int and 0<=j<len(A[0]) and type(k) is int,'integer split')
    low,high=bounds.get(j,(0,None))
    require(k>=low and (high is None or k<high),'complete nontrivial integer alternatives')
    left=dict(bounds);left[j]=(low,k)
    right=dict(bounds);right[j]=(k+1,high)
    return replay(A,b,node['left'],left)+replay(A,b,node['right'],right)


def verify_all(require_trees=True):
    census=json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text())
    N=next(r['tensor'] for r in census if r['id']=='R7_5_5039')
    dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    B=[[sum(N[a][j][k]*N[k][dual[a]][i] for a in range(7) for k in range(7))
        for j in range(7)] for i in range(7)]
    results=[];missing=[];total_leaves=0
    for case in (0,1):
        stem=f'R7_5_5039_c8_case{case}_chi8_0'
        paths=[BASE/'criteria'/(stem+'_system.json'),
               BASE/'integral_gram'/(stem+'_phase_gram.json'),
               BASE/'integral_gram'/(stem+'_system_phase_lattice.json'),
               BASE/'integral_gram'/(stem+'_phi_cross_allocations.json')]
        system,grams,inventory,phi_inventory=[json.loads(p.read_text()) for p in paths]
        require(system['source_sha256']==digest(N),'canonical source binding')
        bindings={str(p.relative_to(ROOT)):sha(p) for p in paths}
        proof=forced_proof.verify(case)
        require(proof['system_sha256']==sha(paths[0]),'forced-packet source binding')
        require(inventory['hashes']['system']==phi_inventory['system_sha256']==sha(paths[0]),
                'upstream inventory binding')
        exact=json.loads((BASE/'criteria'/(stem+'_phi_exact_farkas.json')).read_text())
        require(exact['source_hashes'][paths[0].name]==sha(paths[0]),'conditional separator source')
        remaining={}
        for row in exact['unresolved']:
            remaining.setdefault(row['phi_allocation'],set()).add(row['chi_choice'])
        expected_phi=(2,14,46,49) if case==0 else (46,49)
        require(tuple(sorted(remaining))==expected_phi and all(x==set(range(4)) for x in remaining.values()),
                'complete remaining phi/chi branch inventory')
        labels=system['phase_labels'];orbits=system['orbits'];records=system['phase_records']
        raw_grams=[[[sum(v[i]*v[j] for v,g,z in orb) for j in range(6)] for i in range(6)] for orb in orbits]
        bound=[[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in system['low']) for j in range(6)] for i in range(6)]
        chi_active={j for j,l in enumerate(labels) if any(v[0]!=v[1] for v,g,z in orbits[l['orbit']])}
        phi_active={j for j,l in enumerate(labels) if any(v[2]!=v[3] for v,g,z in orbits[l['orbit']])}
        high={j for j,l in enumerate(labels) if l['orbit'] in (45,50) and records[l['phase']]['orders']==[320]}
        c4=system['cyclic_four'][0]
        require(c4['source_object']==1 and c4['A']==4 and c4['B']==0,'C4 domain')
        fixed_c4=dict(zip(c4['variables'],(3,1,0,0)))
        forbidden=chi_active|phi_active|high|set(fixed_c4)
        # Reconstruct the packet ordering without using fixed_packets().
        packets=[]
        for branch in grams:
            matched=next(r for r in proof['branches'] if r['phase_case']==branch['phase_case'])
            require(matched['active_support']==branch['support'],'forced proof covers this exact chi support')
            for column in sorted(matched['allowed_forced_columns']):
                packets.append(branch['support']+[[column,1]])
        require(len(packets)==8,'complete eight forced packet choices')
        cache={}
        for packet_index,packet in enumerate(packets):
            for phi_index in expected_phi:
                phi=phi_inventory['allocations'][phi_index];support=packet+phi
                require(len({j for j,n in support})==len(support),'disjoint fixed phase variables')
                R=bound
                for j,n in support:
                    require(type(n) is int and n>=0,'integral fixed packet count')
                    lab=labels[j];R=subtract(R,raw_grams[lab['orbit']],n*lab['multiplicity_unit'])
                require(admissible(R),'fixed packets fit raw source Gram')
                key=json.dumps(R,separators=(',',':'))
                if key not in cache:
                    kept=[]
                    for j in range(len(system['columns'])):
                        if j in forbidden:continue
                        if j<len(labels):
                            lab=labels[j]
                            if not admissible(subtract(R,raw_grams[lab['orbit']],lab['multiplicity_unit'])):continue
                        kept.append(j)
                    groups={}
                    for position,j in enumerate(kept):
                        if j<len(labels):groups.setdefault(labels[j]['orbit'],[]).append((position,labels[j]['multiplicity_unit']))
                    capacities=[]
                    for oi,variables in sorted(groups.items()):
                        G=raw_grams[oi]
                        upper=min(R[i][j]//G[i][j] for i in range(6) for j in range(6) if G[i][j])
                        # Direct finite scan independently checks the producer's
                        # monotone binary-search capacity and gcd rounding.
                        possible=[n for n in range(upper+1) if psd(subtract(R,G,n))]
                        require(possible==list(range(max(possible)+1)),'PSD counts form an initial interval')
                        maximum=max(possible);gcd=math.gcd(*(u for position,u in variables))
                        capacities.append((oi,variables,maximum,gcd,maximum-maximum%gcd))
                    cache[key]=(kept,capacities)
                kept,capacities=cache[key]
                cols=[system['columns'][j][:] for j in kept]
                rhs=[b-sum(n*system['columns'][j][i] for j,n in support)
                       -sum(n*system['columns'][j][i] for j,n in fixed_c4.items())
                     for i,b in enumerate(system['rhs'])]
                for oi,variables,maximum,gcd,capacity in capacities:
                    for col in cols:col.append(0)
                    for position,unit in variables:cols[position][-1]=unit
                    rhs.append(capacity);slack=[0]*len(rhs);slack[-1]=1;cols.append(slack)
                matrix=[list(row) for row in zip(*cols)]
                path=BASE/'computation'/f'R7_5_5039_c8_case{case}_packet{packet_index}_phi{phi_index}_tree.json'
                if not path.exists():
                    missing.append(path.name)
                    if require_trees:raise ValueError('Missing complete conditional tree: '+path.name)
                    continue
                tree=json.loads(path.read_text())
                require(tree['source_hashes']==bindings,'exact tree input binding')
                require((tree['case'],tree['packet'],tree['phi'])==(case,packet_index,phi_index),'exact tree branch identity')
                leaves=replay(matrix,rhs,tree['tree'])
                require(leaves==tree['leaves'],'complete tree leaf count')
                total_leaves+=leaves
                results.append(dict(case=case,packet=packet_index,phi=phi_index,leaves=leaves,
                                    tree_sha256=sha(path),matrix_sha256=digest([matrix,rhs]),
                                    capacity_cuts=len(capacities),columns=len(cols)))
    if require_trees:require(len(results)==48 and not missing,'all forty-eight conditional branches proved')
    return dict(status='PASS' if not missing else 'INCOMPLETE',source_sha256=digest(N),
                scope='Conditional c0 branch proof; preceding domain/phase/C4/phi coverage must also be verified.',
                complete_trees=len(results),total_leaves=total_leaves,missing=missing,trees=results)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--allow-missing',action='store_true');args=parser.parse_args()
    result=verify_all(require_trees=not args.allow_missing)
    (HERE/'c0_capacity_tree_independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='trees'}))
