"""Fresh rank9 replay with independently exhaustive integer solution grids."""
from itertools import product
from functools import lru_cache
import sys,json,importlib.util,time
import numpy as np
from audit_liptrap import HERE,FIRST,need

def main():
    start=time.monotonic();folder=HERE/'d48_quotient_frozen';sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('rank9_reconstruction_frozen',folder/'rank9_reconstruct.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    expected=json.loads((folder/'rank9_reconstruction.json').read_text());original=json.loads((FIRST/'tensors.json').read_text())
    need(all(row['tensor']==original[rid] for rid,row in m.INPUTS['records'].items()),'all actual physical inputs')
    iso=m.common.based_iso;iso_count=0
    def exact_iso(A,B):
        nonlocal iso_count
        p=iso(A,B)
        if p is not None:
            need(sorted(p)==list(range(len(A))) and np.array_equal(np.asarray(A),np.asarray(B)[np.ix_(p,p,p)]),'full isomorphism verification');iso_count+=1
        return p
    m.common.based_iso=exact_iso
    survivor=[r for c in expected['reconstruction_classes'] for r in c['reconstructions']];valid=[]
    def inspect(N):
        N=np.array(N);n=len(N);du=[next(j for j in range(n) if N[i,j,0]) for i in range(n)]
        adj={0}|{k for i in range(n) for k in range(n) if N[i,du[i],k]}
        while True:
            new=adj|{k for i,j in product(adj,repeat=2) for k in range(n) if N[i,j,k]}
            if new==adj:break
            adj=new
        need(len(adj)==9,'survivor has trivial universal grading')
        h=[g for g in range(1,4) if N[g,g,0] and np.array_equal(N[g],N[:,g])]
        need(len(h)==1,'unique central involution')
        need(all(N[h[0],i,i]==1 for i in range(4,9)),'it fixes all five noninvertibles')
        hits=[j for j,r in enumerate(survivor) if exact_iso(N.tolist(),r['tensor']) is not None]
        need(len(hits)==1,'every valid table is one of the two audited survivors');valid.append(hits[0])
    m.independent_bind9=inspect
    old_solver=m.linear_solutions;solver_calls=0;max_grid=0
    @lru_cache(None)
    def brute(At,bt,ut):
        nonlocal max_grid
        need(all(v>=0 for row in At for v in row) and all(u>=0 for u in ut),'nonnegative bounded integer system')
        grid=np.array(list(product(*(range(u+1) for u in ut))),dtype=np.int64);max_grid=max(max_grid,len(grid))
        A=np.array(At,dtype=np.int64);b=np.array(bt,dtype=np.int64)
        return tuple(tuple(int(x) for x in row) for row in grid[np.all(grid@A.T==b,axis=1)])
    def solver(A,b,upper):
        nonlocal solver_calls
        solver_calls+=1;key=tuple(map(tuple,A)),tuple(b),tuple(upper)
        all_values=brute(*key);returned=tuple(sorted(tuple(v) for v in old_solver(A,b,upper)))
        need(returned==tuple(sorted(all_values)),'interval solver equals independent complete Cartesian grid')
        yield from all_values
    m.linear_solutions=solver
    branches=m.source_branches();lookup={(r['id'],b['involution']):(r,b) for r in branches for b in r['branches']}
    for bind in expected['source_binding']:
        r,b=lookup[bind['id'],bind['involution']];c=expected['reconstruction_classes'][bind['reconstruction_class']]['source'];p=bind['class_basis_map']
        need(r['sha256']==bind['source_hash'] and b['case']=='rank9_dimension24_type_1_4_2_5','source-to-class binding')
        need(np.array_equal(np.array(b['quotient_tensor']),np.array(c['tensor'])[np.ix_(p,p,p)]),'all orbit-ring coefficients in source binding')
    need(len(expected['source_binding'])==sum(b['case']=='rank9_dimension24_type_1_4_2_5' for r in branches for b in r['branches']),'all rank9 branches covered')
    out=[]
    for c in expected['reconstruction_classes']:
        source=c['source'];found,stats=m.reconstruct9(source['tensor'],source['dimensions'])
        need(stats==c['statistics'] and len(found)==len(c['reconstructions']),'exact exhaustive class counts')
        for r in found:inspect(r['tensor'])
        out.append(dict(first_source=source['first_source'],survivors=len(found),statistics=stats))
    result=dict(status='PASS',source_bindings=len(expected['source_binding']),classes=out,integer_system_calls=solver_calls,distinct_integer_systems=brute.cache_info().currsize,maximum_full_integer_grid=max_grid,valid_table_property_checks=len(valid),full_isomorphisms_checked=iso_count,scope='Exact exhaustive rank9 quotient reconstruction; categorical closure uses solvable equivariantization and unique central lift, not a guessed C3 grading',seconds=time.monotonic()-start)
    (HERE/'rank9_quotient_reconstruction_independent.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='classes'})

if __name__=='__main__':main()
