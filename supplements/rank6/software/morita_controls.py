"""Exact Morita-obstruction tests, positive controls and relabeling invariance."""
import copy, itertools, json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'verification/current').mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'software'))
from exact import require
from prepare import key
from fermionic_products import examples, local_certificate, verify_local_certificate, local_data
from small_dimension_morita import certificate, structural_data, verify



def reject(fn):
    try:fn()
    except Exception:return
    raise RuntimeError('a deliberately invalid certificate was accepted')

def permute(R,p):return [[[R[i][j][k] for k in p] for j in p] for i in p]


def main():
    start=time.monotonic()
    rows=json.loads((ROOT/'data/census.json').read_text());by={r['id']:r for r in rows}
    ledger=json.loads((ROOT/'data/decisions.json').read_text());now={r['id']:r for r in ledger}
    hits=[];dimensions=[]
    for r in rows:
        if structural_data(r['N']) is not None:dimensions.append(r['id'])
        c=certificate(r['N'])
        if c is not None:verify(r['N'],c);hits.append(r['id'])
    require([rid for rid in hits if by[rid]['m']<=7]==['R6_2_25','R6_2_29','R6_2_51','R6_3_15','R6_4_19'],'established-prefix criterion coverage')
    require(all(now[rid]['status']=='excluded' for rid in hits),'Morita certificate not reflected in current ledger')
    require(sum(by[rid]['m']<=7 for rid in dimensions)==13,'established-prefix dimension scan')
    for positive in ['R6_2_105','R6_3_141']:
        require(certificate(by[positive]['N']) is None,'known A5 model excluded')
    constructor_matches=[]
    index={key(r['N']):r['id'] for r in rows}
    for name,R,ref,e in examples():constructor_matches.append(index[key(R)])
    require(constructor_matches==['R6_1_3','R6_2_14','R6_2_40'],'fermionic constructor controls')
    require(key(by['R6_2_40']['N'])!=key(by['R6_2_97']['N']),'opposite half-E6 model conflated')
    mutations=0
    for m,n in [(0,0),(0,2),(2,2)]:
        cert=local_certificate(m,n);verify_local_certificate(m,n,cert)
        for field,value in [('dual_action_scalar',[1,0]),('vacuum_projector_ranks',[[1,0],[0,1]])]:
            bad=copy.deepcopy(cert);bad[field]=value
            reject(lambda bad=bad:verify_local_certificate(m,n,bad));mutations+=1
    reject(lambda:local_data(4));mutations+=1
    for rid in ['R6_2_51','R6_3_15','R6_4_19']:
        R=by[rid]['N'];c=certificate(R);bad=copy.deepcopy(c);bad['dimensions'][1]+=1
        reject(lambda:verify(R,bad));mutations+=1
        if c['branch']=='dimension60':
            bad=copy.deepcopy(c);bad['group_theoretical_indicator_audit']['target_second_indicator']=0
            reject(lambda:verify(R,bad));mutations+=1
    relabelings=0
    for rid in ['R6_2_51','R6_3_15','R6_4_19']:
        for tail in itertools.permutations(range(1,6)):
            R=permute(by[rid]['N'],(0,)+tail);c=certificate(R)
            require(c is not None,'criterion depends on census labeling');verify(R,c);relabelings+=1
    require(now['R6_2_124']['existence']=={'general':'yes','pivotal':'yes','spherical':'yes','pseudo_unitary':'no','unitary':'no'},'Schopieray status changed')
    report={'passed':True,'optimized_python':not __debug__,'census_scanned':len(rows),
            'small_dimension_matches':dimensions,'criterion_hits':hits,'constructor_matches':constructor_matches,
            'relabelings_checked':relabelings,'mutations_rejected':mutations,
            'seconds':time.monotonic()-start,
            'scope':'Finite theorem hypotheses, scalar reconstruction and tensor identities. Categorical source theorems and the new mathematical proofs are not proof-assistant formalized.'}
    out=ROOT/'verification/current'/('morita_controls_optimized.json' if not __debug__ else 'morita_controls_normal.json')
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
