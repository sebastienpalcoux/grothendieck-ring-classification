"""Finite data check for the complete palindromic parity method.

The categorical completeness statement is proved in parity_saturation.md.
No associators, pivotal structures or categories are inferred by this script.
"""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('tensors',ROOT/'current_remaining_cases.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
old=json.loads((Path(__file__).parent/'prior_parity_receipt.json').read_text())
prior={r['id']:r for r in old['cases']}
out=[]
for name,N in m.TENSORS.items():
    n=len(N); dual=m.DUALS[name]; selfdual=[i for i in range(n) if dual[i]==i]
    # Hash source independently, rather than trust only exported metadata.
    sha=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    assert sha==m.METADATA[name]['tensor_sha256']==prior[name]['tensor_sha256']
    assert all(N[i][j][0]==int(dual[i]==j) for i in range(n) for j in range(n))
    assert all(sum(N[i][j][t]*N[t][k][l] for t in range(n))==sum(N[j][k][t]*N[i][t][l] for t in range(n)) for i,j,k,l in itertools.product(range(n),repeat=4))
    def conjugate(x,y,z):return sum(N[x][y][t]*N[t][dual[x]][z] for t in range(n))
    parent=list(range(n))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    for y,z in itertools.product(selfdual,repeat=2):
        if any(conjugate(x,y,z)%2 for x in range(n)):parent[root(y)]=root(z)
    components=sorted(sorted(i for i in selfdual if root(i)==r) for r in set(root(j) for j in selfdual))
    assert components==prior[name]['same_sign_components']
    for record in prior[name]['assignments']:
        signs=record['indicators']
        assert not any(conjugate(x,y,z)%2 and signs[y]!=signs[z] for x in range(n) for y,z in itertools.product(selfdual,repeat=2))
    # Exact Frobenius-duality identity behind the hyperbolic cross-term proof.
    cross_checks=0
    for i,j,y,z in itertools.product(range(n),range(n),selfdual,selfdual):
        left=sum(N[i][y][t]*N[t][dual[j]][z] for t in range(n))
        right=sum(N[j][y][t]*N[t][dual[i]][z] for t in range(n))
        assert left==right
        cross_checks+=1
    out.append({'id':name,'tensor_sha256':sha,'components':components,'unit_fixed_sign_assignments':2**(len(components)-1),'inherited_assignments_pass':len(prior[name]['assignments']),'hyperbolic_cross_term_checks':cross_checks})
result={'theorem':'All further conjugation-parity tests on arbitrary direct sums and nested palindromic tensor words follow from the simple-conjugator graph.','scope':'Pivotal categories only; general complex use needs a separate existence gate.','new_exclusions':0,'new_models':0,'cases':out}
(Path(__file__).parent/'saturation_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
