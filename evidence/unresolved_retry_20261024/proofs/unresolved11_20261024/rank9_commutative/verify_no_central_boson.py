"""Bind conditional quotients to two generally excluded rank-six tensors.

The categorical implication is justified in NO_CENTRAL_BOSON.md. This script
only verifies its exact inputs, transports, and existing exclusion proofs.
Use --replay-dependencies to replay both lower-rank certificates exactly.
"""
import argparse, hashlib, itertools, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
REPO = WORK / 'online_revision/grothendieck-ring-classification'

def require(x, msg):
    if not x:
        raise ValueError(msg)

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay-dependencies', action='store_true')
    args = ap.parse_args()
    cert = json.loads((HERE/'central_lift_reduction_certificate.json').read_text())
    deps = {x['id']:x for x in json.loads((HERE/'lower_rank_dependencies.json').read_text())['rows']}
    p = [0, 5, 1, 2, 3, 4]
    links = []
    for rec in cert['candidate_quotient_rings']:
        rid = {'V4':'R6_4_174', 'C4':'R6_4_6'}[rec['invertible_group']]
        T, target = rec['tensor'], deps[rid]['N']
        require(all(T[i][j][k] == target[p[i]][p[j]][p[k]]
                    for i,j,k in itertools.product(range(6), repeat=3)), 'quotient transport')
        for m in rec['maps']:
            prof = json.loads((HERE.parent/'inputs'/f"{m['id']}.json").read_text())
            S, F = prof['fusion_tensor'], m['source_to_quotient_matrix']
            require(digest(S) == m['source_sha256'] == prof['tensor_sha256'], 'source hash')
            require(all(sum(S[i][j][r]*F[r][k] for r in range(9)) ==
                        sum(F[i][a]*F[j][b]*T[a][b][k] for a,b in itertools.product(range(6),repeat=2))
                        for i,j,k in itertools.product(range(9),range(9),range(6))), 'source quotient map')
            # Explicit adjoint generation, hence trivial universal grading.
            dual = [next(j for j in range(9) if S[i][j][0]) for i in range(9)]
            adj = {k for i in range(9) for k in range(9) if S[i][dual[i]][k]}
            while True:
                nxt = adj | {k for i in adj for j in adj for k in range(9) if S[i][j][k]}
                if nxt == adj:
                    break
                adj = nxt
            require(adj == set(range(9)), 'nontrivial universal grading')
        dep = deps[rid]
        c = dep['decision']['certificate']
        require(c['scope'] == 'general', 'dependency scope')
        links.append({'target':rid,'group':rec['invertible_group'],
                      'permutation_quotient_to_target':p, 'target_tensor_sha256':digest(target),
                      'certificate_kind':c['kind'], 'coefficient_checks':216,
                      'source_maps_checked':3, 'map_coefficients_checked':1458})
    if args.replay_dependencies:
        sys.path.insert(0, str(REPO/'supplements/rank6/software'))
        import scipy.optimize
        def forbidden(*a, **k):
            raise RuntimeError('Optimizer entry point forbidden during exact replay')
        for name in ('linprog','milp','minimize','least_squares'):
            setattr(scipy.optimize,name,forbidden)
        import stabilizer_rotation_higher, round3_smallest
        for rid, f in [('R6_4_174',stabilizer_rotation_higher.verify_general),
                       ('R6_4_6',round3_smallest.verify)]:
            require(f(deps[rid]['N'],deps[rid]['decision']['certificate']), 'dependency replay')
            print('EXACT GENERAL EXCLUSION REPLAYED',rid,flush=True)
    out = {'status':'PASS','classification_changes':[],
           'new_conclusion':'The unique isotropic free involution has no central lift; the pointed center is Vec or sVec.',
           'links':links,'dependency_replay':args.replay_dependencies}
    (HERE/'no_central_boson_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
