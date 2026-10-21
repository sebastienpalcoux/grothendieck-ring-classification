"""Read-only proof replay, with no numerical optimization."""
import json
import central_support as c
import rotation_search as base
import full_rotation as full
import certified_lp as lp
import character_modular as modular
import spectral_filter
import integral_gram
import central_fusion
import verlinde_low
import central_integral_filters
import cubic_tensor
import sys
from verify_independent import central_columns
from matricial_structure import structure

def main():
    C={r['id']:r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())}
    for r in json.loads((c.HERE/'central_support_results.json').read_text()):
        row=C[r['id']];c.require(r['tensor_sha256']==row['tensor_sha256'],'tensor binding')
        result=json.loads(json.dumps(c.scan(row['tensor']),default=int))
        c.require(result=={k:v for k,v in r.items() if k not in ('id','tensor_sha256')},'central support replay')
    for r in json.loads((c.HERE/'matricial_structure.json').read_text()):
        row=C[r['id']];c.require(r['tensor_sha256']==row['tensor_sha256'],'structure tensor binding')
        c.require(structure(row['tensor'])=={k:v for k,v in r.items() if k not in ('id','tensor_sha256')},'matricial replay')
    old_system=base.h.build_system;dual=primal=undecided=0
    for p in sorted(c.HERE.glob('rotation_*.json')):
        r=json.loads(p.read_text());R=C[r['id']]['tensor'];c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'rotation tensor binding')
        joint=any(x.get('systems') and x['systems'][0]['metadata'].get('joint_rotation') for x in r['result']['branches'])
        base.h.build_system=full.system if joint else old_system
        base.verify(R,r['result']);dual+=sum(x['ray'] is not None for y in r['result']['branches'] for x in y.get('systems',[]))
    base.h.build_system=old_system;base.install()
    for p in sorted(c.HERE.glob('certified_*.json')):
        r=json.loads(p.read_text());R=C[r['id']]['tensor'];quartic=c.w.spectral(R)['factor'].degree()==4
        c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'certified tensor binding')
        a=base.bq.data(R) if quartic else c.w.data(R);cols=a['lows'][r['low_index']];L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));ep=tuple(r['indicators'])
        c.require(ep in base.h.indicator_choices(R),'allowed indicators')
        if quartic:A,b,meta=base.bq.system(R,a,cols,ep,r['height'])
        elif r['metadata'].get('joint_rotation'):A,b,meta=full.system(R,a,L,ep,r['height'])
        else:A,b,meta=old_system(R,a,L,ep,r['height'])
        c.require(meta==r['metadata'],'certified system metadata');lp.verify(A,b,r['decision'])
        primal+=r['decision']['status']=='exact_feasible_relaxation';dual+=r['decision']['status']=='exact_infeasible_relaxation';undecided+=r['decision']['status'] not in ('exact_feasible_relaxation','exact_infeasible_relaxation')
    for p in sorted([*c.HERE.glob('modular_*.json'),*c.HERE.glob('spectral_modular_*.json')]):
        r=json.loads(p.read_text());R=C[r['id']]['tensor'];quartic=c.w.spectral(R)['factor'].degree()==4
        c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'modular tensor binding')
        a=base.bq.data(R) if quartic else c.w.data(R)
        for case in r['cases']:
            cols=a['lows'][case.get('low_index',r.get('low_index'))];L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));ep=tuple(case.get('indicators',r.get('indicators')))
            A,b,meta=base.bq.system(R,a,cols,ep,r['height']) if quartic else full.system(R,a,L,ep,r['height'])
            A,b,meta=modular.append_sts(R,a,cols,tuple(case['permutation']),A,b,meta,r['height'])
            if p.name.startswith('spectral_'):A,b,meta=spectral_filter.append_filter(R,a,cols,A,b,meta)
            c.require(meta==case['metadata'],'modular system metadata');lp.verify(A,b,case['decision'])
            primal+=case['decision']['status']=='exact_feasible_relaxation';dual+=case['decision']['status']=='exact_infeasible_relaxation';undecided+=case['decision']['status'] not in ('exact_feasible_relaxation','exact_infeasible_relaxation')
    p=c.HERE/'integral_gram_721_rotations.json';r=json.loads(p.read_text());R=C[r['id']]['tensor'];a=c.w.data(R);cols=a['lows'][r['low_index']];L=c.s.Matrix.hstack(*map(c.s.Matrix,cols))
    c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'integral Gram tensor binding')
    counts,receipt=integral_gram.completions(a,cols)
    c.require(sorted(tuple(case['multiplicities']) for case in r['cases'])==counts,'all integral Gram completions')
    A,b,meta=full.system(R,a,L,tuple(r['indicators']),r['height']);c.require(meta==r['metadata'],'integral rotation system')
    c.require(tuple(r['indicators']) in base.h.indicator_choices(R),'integral rotation allowed indicators')
    for case in r['cases']:
        AA,bb=integral_gram.append_multiplicities(A,b,case['multiplicities'],meta['trace_types']);lp.verify(AA,bb,case['decision']);primal+=case['decision']['status']=='exact_feasible_relaxation'
    p=c.HERE/'central_fusion_721.json';r=json.loads(p.read_text());R=C[r['id']]['tensor'];a=c.w.data(R);cols=a['lows'][r['low_index']]
    c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'central fusion tensor binding')
    counts,receipt=integral_gram.completions(a,cols)
    c.require(receipt==r['domain'],'central fusion exhaustive domain')
    c.require(sorted(tuple(case['multiplicities']) for case in r['cases'])==counts,'central fusion complete Gram coverage')
    chs=modular.characters(R,a)
    c.require(all(all(ch[i]==ch[a['du'][i]] for i in range(8)) for ch in chs),'distinguished central selfduality')
    for case in r['cases']:
        A,b,meta=central_fusion.system(R,a,cols,case['multiplicities']);c.require(meta==case['metadata'],'central fusion metadata')
        lp.verify(A,b,case['decision']);primal+=case['decision']['status']=='exact_feasible_relaxation'
    p=c.HERE/'verlinde_low_721.json';r=json.loads(p.read_text())
    c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'],'Verlinde tensor binding')
    c.require(r['domain']==receipt,'Verlinde complete Gram domain')
    permutations=modular.assignments(a,modular.characters(R,a),cols)
    c.require(sorted((tuple(case['permutation']),tuple(case['multiplicities'])) for case in r['cases'])==sorted((perm,co) for perm in permutations for co in counts),'complete low Verlinde domain')
    for case in r['cases']:
        A,b,meta,co=verlinde_low.system(R,a,cols,case['multiplicities'],tuple(case['permutation']))
        c.require(co==case['coefficients'] and meta==case['metadata'],'exact low Verlinde coefficients')
        lp.verify(A,b,case['decision']);primal+=case['decision']['status']=='exact_feasible_relaxation'
    p=c.HERE/'integral_modular_721_h6.json';r=json.loads(p.read_text())
    c.require(r['tensor_sha256']==C[r['id']]['tensor_sha256'] and r['domain']==receipt,'integral modular domain')
    c.require(sorted(tuple(case['multiplicities']) for case in r['cases'])==counts,'complete integral modular domain')
    c.require(tuple(r['indicators']) in base.h.indicator_choices(R),'integral modular allowed indicators')
    A,b,meta=full.system(R,a,L,tuple(r['indicators']),r['height'])
    A,b,meta=modular.append_sts(R,a,cols,tuple(r['permutation']),A,b,meta,r['height'])
    c.require(meta==r['metadata'],'integral modular metadata')
    for case in r['cases']:
        AA,bb=integral_gram.append_multiplicities(A,b,case['multiplicities'],meta['trace_types']);lp.verify(AA,bb,case['decision'])
        primal+=case['decision']['status']=='exact_feasible_relaxation';dual+=case['decision']['status']=='exact_infeasible_relaxation';undecided+=case['decision']['status'] not in ('exact_feasible_relaxation','exact_infeasible_relaxation')
    sys.path.insert(0,str(c.HERE.parent/'central_integrality'))
    import integer_gram_1154
    gram1154=integer_gram_1154.compute()
    c.require(gram1154==json.loads((c.HERE.parent/'central_integrality/integer_gram_1154.json').read_text()),'complete R1154 integral Gram domain')
    filtered=central_integral_filters.compute_1154()
    c.require(filtered==json.loads((c.HERE/'central_integral_filters_1154.json').read_text()),'complete R1154 cubic/spectral filters')
    tensor=cubic_tensor.compute_1154()
    c.require(tensor==json.loads((c.HERE/'cubic_tensor_1154.json').read_text()),'complete R1154 tensor cones')
    tensor_witnesses=sum(x is not None for case in tensor['cases'] for x in case['witnesses'])
    print(f'PASS: central support, matricial structure, {dual} exact dual rays, {primal} exact primal witnesses, {undecided} explicitly undecided attempts; R1154 complete 14211 -> 1238 Gram filter and {tensor_witnesses} exact tensor cones')

if __name__=='__main__':main()
