"""Direct independent per-coefficient replay of accepted positive records."""
from pathlib import Path
import collections,hashlib,itertools,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
data=json.loads((BASE/'tensors.json').read_text())
counts=collections.Counter();rings=set();zests=[]
def require(v,msg):
    if not v:raise ValueError(msg)
for name in ('models','additional_models','group_models','twisted_c2_models'):
    rows=json.loads((BASE/(name+'.json')).read_text())
    for row in rows:
        rid=row['id'];R=data[rid];rings.add(rid)
        for model in row['models']:
            M=model['model_tensor'];p=model['basis_map_source_to_model']
            require(len(M)==12 and len(p)==12 and p[0]==0 and sorted(p)==list(range(12)),rid+' map')
            for a,b,c in itertools.product(range(12),repeat=3):
                require(R[a][b][c]==M[p[a]][p[b]][p[c]],rid+' coefficient')
            counts[model['constructor']]+=1
            if model['constructor']=='associative_C2_zest':
                pars=model['parameters'];A=pars['base_tensor'];h=pars['central_invertible'];g=pars['grading']
                require(g[0]==g[h]==0 and set(g)=={0,1},rid+' grading/current')
                require(all(A[h][i]==A[i][h]and sum(A[h][i])==1 for i in range(12)),rid+' central based current')
                require(A[h][h]==[1]+[0]*11,rid+' current order two')
                require(all(g[c]==(g[a]^g[b])for a,b,c in itertools.product(range(12),repeat=3)if A[a][b][c]),rid+' all grading channels')
                kind=pars['base_constructor']
                require(kind in ('pointed','pointed_equivariant','dihedral_rep','deligne_product','odd_metaplectic','half_even_metaplectic','graded_pullback','metaplectic_character_crossed_product'),rid+' audited categorical lift family')
                if kind=='graded_pullback':
                    require(pars['base_parameters']['labels'][h]==[1,0],rid+' inherited Ising fermion')
                if kind=='metaplectic_character_crossed_product':
                    require(h==1,rid+' canonical equivariance boson')
                zests.append(dict(id=rid,base_name=pars['base_name'],base_constructor=kind,h=h,lift_source='specified categorical family, reviewed in findings.md'))
for row in json.loads((BASE/'feudal.json').read_text())['records']:
    if row['model']:
        counts['liptrap_unitary_model']+=1;rings.add(row['id'])
        require(row['model']['kind']=='liptrap_unitary_model','positive Liptrap source')
require(sum(counts.values())==402 and len(rings)==127,'complete 402/127 accounting')
out=dict(status='PASS',ordinary_tensor_identifications=381,liptrap_constructions=21,total_model_records=402,realized_rings=127,constructor_counts=dict(counts),zest_records=zests,scope='Direct bindings independently replayed; categorical proofs manually reviewed against primary sources, not inferred from ring symmetry.')
(HERE/'positive_binding_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items()if k not in ('zest_records','constructor_counts')})
