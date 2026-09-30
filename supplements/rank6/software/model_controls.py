"""Exact model-coverage, cochain and positive-control checks."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,time,copy,itertools
from pathlib import Path
from exact import require,VerificationError
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)

def main():
    start=time.monotonic();report={}
    from model_catalog import verify_catalog
    from complete_models import examples
    from prepare import key
    from oriented_signed import validate_general
    from twisted_group_models import twisted_s4
    from quantum_rank2 import principal
    import involution_module
    rows={r['id']:r for r in json.load(open(P/'data/census.json'))}
    report['catalogue']=verify_catalog()
    from conformal_models import verify as verify_conformal
    report['conformal_models']=verify_conformal(fresh=True)
    census_index={}
    for r in rows.values():census_index.setdefault(key(r['N']),[]).append(r['id'])
    models=list(examples());checks=0
    for name,R,ref in models:
        validate_general(R)
        matches=census_index.get(key(R),[])
        require(len(matches)==1,'model has no unique census isomorphism class')
        require(involution_module.certificate(R) is None,'module criterion rejects positive model '+name)
        checks+=1
    report['additional_constructor_controls']=checks
    R,aux=twisted_s4();saved=json.load(open(P/'data/twisted_s4_certificate.json'))
    require(json.loads(json.dumps(aux))==saved,'twisted cochain record mismatch')
    # A modified boundary cochain must fail admissibility directly, not merely
    # because its serialized hash differs.
    from twisted_group_models import matmul,normalize
    mats=aux['matrices'];index={tuple(a):i for i,a in enumerate(mats)};G=[[index[normalize(matmul(a,b))[0]] for b in mats] for a in mats]
    alpha=[int((a[0]*a[3]-a[1]*a[2])%3==2) for a in mats]
    beta=[[normalize(matmul(a,b))[1] for b in mats] for a in mats]
    def boundary_ok(qvalues):
        q=dict(zip(map(tuple,aux['boundary_pairs']),qvalues));q.update({(0,h):0 for h in aux['H']});q.update({(h,0):0 for h in aux['H']})
        return all((q[b,c]+q[a,G[b][c]]-q[G[a][b],c]-q[a,b]-2*alpha[a]*beta[b][c])%4==0 for a,b,c in itertools.product(aux['H'],repeat=3))
    require(boundary_ok(aux['boundary_exponents_mod4']),'original boundary fails')
    bad=aux['boundary_exponents_mod4'].copy();bad[0]=(bad[0]+1)%4
    require(not boundary_ok(bad),'modified boundary cochain was not rejected')
    mod=copy.deepcopy(R);mod[4][4][0]+=1;rejected=False
    try:validate_general(mod)
    except Exception:rejected=True
    require(rejected,'corrupted positive tensor was accepted')
    g2,basis,cond=principal('G2',3)
    require(len(basis)==6 and cond==21 and key(g2)==key(rows['R6_2_144']['N']),'G2 reconstruction mismatch')
    report['twisted_group_checks']={'group_order':24,'boundary_triples':64,'cocycle_quadruples':24**4,'rejected_mutations':2}
    report.update(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-start)
    out=P/'verification/current'/('model_controls_optimized.json' if not __debug__ else 'model_controls_normal.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
