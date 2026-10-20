"""Exact source/low-row label symmetry audit for the two frontier rings.

Equal restriction rows give identical character-to-row assignments. Source
basis automorphisms are exhaustively enumerated, rather than assumed to
identify the two conductor-five signs.
"""
import hashlib,itertools,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'criteria'))
import q5_modular_low as m
q=m.q

def run(rid,index):
    raw=(q.ROOT/'supplements/rank7/output/m5/census.json').read_bytes()
    N=next(r['tensor'] for r in json.loads(raw) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5)
    path=BASE/'integral_gram'/(rid+'_domains.json');domain_raw=path.read_bytes()
    dom=next(z for z in json.loads(domain_raw) if z['low_index']==index)
    low=[(1,0,0,0,0,0,0)]+list(map(tuple,dom['low']))
    assigned=lambda label:tuple(sorted(zip(label,low)))
    classes={}
    for ci,c in enumerate(dom['cases']):
        if -1 in c['sign']:continue
        key=assigned(c['label']);classes.setdefault(key,[]).append(ci)
    q.require(len(classes)==2,'Exactly two distinct character-to-row assignments.')
    automorphisms=[]
    for tail in itertools.permutations(range(1,7)):
        perm=(0,)+tail
        if any(d[i]!=d[perm[i]] for i in range(7)):continue
        if any(N[i][j][k]!=N[perm[i]][perm[j]][perm[k]] for i in range(7) for j in range(7) for k in range(7)):continue
        cp=[next(h for h,r in enumerate(table.rows) if all(r[i]==row[perm[i]] for i in range(7))) for row in table.rows]
        images=[]
        for key in classes:
            transformed=tuple(sorted((cp[h],tuple(v[perm[i]] for i in range(7))) for h,v in key))
            q.require(transformed in classes,'Based automorphism preserves eligible low frame.')
            images.append(classes[transformed])
        automorphisms.append({'basis_permutation':perm,'character_permutation':cp,'class_images':images})
    q.require(len(automorphisms)==4,'Exhaustive source automorphism group has four elements.')
    groups=list(classes.values())
    q.require(all(a['class_images']==groups for a in automorphisms),'Source automorphisms preserve each delta-sign class.')
    return {'id':rid,'source_sha256':q.tensor_hash(N),'domain_sha256':hashlib.sha256(domain_raw).hexdigest(),
            'low_index':index,'positive_indicator_case_classes':groups,'automorphisms':automorphisms,
            'scope':'Equal low rows yield identical assignments; based source symmetries do not equate the two conductor-five signs.'}

if __name__=='__main__':
    results=[run('R7_5_3895',8),run('R7_5_5039',3)]
    out={'status':'PASS','optimized_python':not __debug__,'results':results}
    (HERE/('label_symmetry_'+('optimized' if not __debug__ else 'normal')+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','optimized_python':not __debug__,'classes':{r['id']:r['positive_indicator_case_classes'] for r in results}}))
