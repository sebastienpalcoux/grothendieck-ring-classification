from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def current():
    exclusions={};models={}
    def add(r,source):
        cs=r.get('certificates')or([r['certificate']]if r.get('certificate')else[])
        if cs:exclusions.setdefault(r['id'],[]).extend(dict(source=source,certificate=c)for c in cs)
    for name in ['arithmetic','subrings','cyclic','primary','primary_full','field_checks','more_criteria','induction']:
        p=ROOT/(name+'.json')
        if not p.exists():continue
        q=json.loads(p.read_text());rs=q['records']if isinstance(q,dict)else q
        for r in rs:add(r,name+'.json')
    p=ROOT/'spectra.json'
    if p.exists():
        for key,z in json.loads(p.read_text()).items():
            for r in z['records']:add(r,'spectra.json:'+key)
    p=ROOT/'modules.json'
    if p.exists():
        rs=json.loads(p.read_text())['records'];classes={int(r['id'].rsplit('_',1)[1]):r for r in rs if r['id'].startswith('subring_class_')and r['certificate']}
        for r in rs:
            if r['id'].startswith('R'):add(r,'modules.json')
        for r in json.loads((ROOT/'subrings.json').read_text())['records']:
            for S in r['subrings']:
                if S['class_index']in classes:
                    add(dict(id=r['id'],certificate=dict(kind='module_excluded_subring',**S)),'modules.json');break
    p=ROOT/'models.json'
    if p.exists():
        for r in json.loads(p.read_text()):models[r['id']]=r['models']
    p=ROOT/'additional_models.json'
    if p.exists():
        for r in json.loads(p.read_text()):models.setdefault(r['id'],[]).extend(r['models'])
    p=ROOT/'twisted_c2_models.json'
    if p.exists():
        for r in json.loads(p.read_text()):models.setdefault(r['id'],[]).extend(r['models'])
    p=ROOT/'group_models.json'
    if p.exists():
        for r in json.loads(p.read_text()):models.setdefault(r['id'],[]).extend(r['models'])
    p=ROOT/'feudal.json'
    if p.exists():
        for r in json.loads(p.read_text())['records']:
            add(r,'feudal.json')
            if r['model']:models.setdefault(r['id'],[]).append(r['model'])
    p=ROOT/'lower_known.json'
    if p.exists():
        classes={r['class_index']:r for r in json.loads(p.read_text())['class_proofs']}
        for r in json.loads((ROOT/'subrings.json').read_text())['records']:
            for S in r['subrings']:
                if S['class_index']in classes:
                    add(dict(id=r['id'],certificate=dict(kind='known_excluded_subring',known_source_id=classes[S['class_index']]['known_source_id'],scope='general_complex_fusion_category',**S)),'lower_known.json');break
    return exclusions,models
if __name__=='__main__':
    ex,mo=current();data=json.loads((ROOT/'tensors.json').read_text());rem=[rid for rid in data if rid not in ex and rid not in mo]
    print('excluded',len(ex),'models',len(mo),'unresolved',len(rem),'conflicts',set(ex)&set(mo))
    (ROOT/'current_remaining.json').write_text(json.dumps(rem,indent=2)+'\n')
