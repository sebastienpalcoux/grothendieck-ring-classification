"""Portable exact fourth-round verification; replay writes only into a temporary copy.

Python 3, NumPy and SymPy are required. Pass --baseline to replay the frozen
third-round verifier too. Discovery scripts and exploratory numerical tests
are not used as exclusion evidence.
"""
from pathlib import Path
import collections, csv, hashlib, itertools, json, os, shutil, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parent
LOG = ROOT / 'verification'
LOG.mkdir(exist_ok=True)
MODE = 'normal' if __debug__ else 'optimized'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def read(path):
    return json.loads(path.read_text())

def digest(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()

def main():
    started = time.monotonic()
    summary = read(ROOT / 'summary.json')
    ledger = read(ROOT / 'ledger.json')
    previous = read(ROOT / 'prior_round/ledger.json')
    original = read(ROOT / 'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json')
    decisions = read(ROOT / 'new_decisions.json')
    old = {r['id']: r for r in previous['records']}
    rows = ledger['records']
    by = {r['id']: r for r in rows}
    positive, negative = decisions['models'], decisions['exclusions']
    need(ledger['summary'] == summary, 'summary binding')
    need((summary['excluded'], summary['modeled'], summary['unresolved']) == (478, 151, 3), 'final counts')
    need(not summary['online_revision_performed'], 'offline restriction')
    need(len(rows) == len(by) == 632 and set(by) == set(original) == set(old), 'all input IDs exactly once')
    need(len(positive) == 3 and len(negative) == 40 and not set(positive) & set(negative), 'new decisions')
    for rid, tensor in original.items():
        expected = 'unitarily_realized' if rid in positive else 'excluded' if rid in negative else old[rid]['status']
        need(by[rid]['status'] == expected, 'decision ' + rid)
        need(by[rid]['tensor_sha256'] == digest(tensor), 'physical tensor binding ' + rid)
        if rid in positive or rid in negative:
            need(old[rid]['status'] == 'unresolved', 'only previously unresolved input changed')
    need(collections.Counter(r['status'] for r in rows) == {'excluded': 478, 'unitarily_realized': 151, 'unresolved': 3}, 'ledger counts')
    for rid, model in positive.items():
        p, tensor, target = model['basis_map'], model['model_tensor'], original[rid]
        need(p[0] == 0 and sorted(p) == list(range(12)), 'unit-preserving basis bijection')
        if model['basis_map_direction'] == 'census_to_model':
            need(all(target[i][j][k] == tensor[p[i]][p[j]][p[k]] for i, j, k in itertools.product(range(12), repeat=3)), 'all model coefficients ' + rid)
        else:
            need(all(tensor[i][j][k] == target[p[i]][p[j]][p[k]] for i, j, k in itertools.product(range(12), repeat=3)), 'all model coefficients ' + rid)
    for row in list(positive.values()) + list(negative.values()):
        for field in ['proof', 'replay', 'independent_audit']:
            need((ROOT / row[field]).is_file(), 'evidence link ' + row[field])
    for row in negative.values():
        need(row['scope'] == 'general_complex_fusion_category', 'negative scope')
    remaining = read(ROOT / 'unresolved_tensors.json')
    need({r['id'] for r in remaining} == {'R12_1_561', 'R12_1_623', 'R12_1_628'}, 'exact unresolved IDs')
    for r in remaining:
        need(r['tensor'] == original[r['id']] and r['tensor_sha256'] == digest(r['tensor']), 'unresolved tensor binding')
    with (ROOT / 'ledger.csv').open(newline='') as f:
        csvrows = list(csv.DictReader(f))
    need(len(csvrows) == 632 and all(r['status'] == by[r['id']]['status'] and r['tensor_sha256'] == by[r['id']]['tensor_sha256'] for r in csvrows), 'CSV binding')
    for rel, expected in read(ROOT / 'prior_snapshot_manifest.json').items():
        need(hashlib.sha256((ROOT / 'prior_round' / rel).read_bytes()).hexdigest() == expected, 'unchanged preceding package: ' + rel)
    print('PASS complete ledger, three models, forty exclusions, frozen baseline', flush=True)

    steps = [
        ['d32/verify.py'], ['d32/finite_bicharacter_lemmas.py'], ['d32/shapiro_check.py'],
        ['d32/exhaustive_catalog.py'], ['d32/structural_binding.py'],
        ['d144/verify_reductions.py'], ['d144/verify_positive_models.py'], ['d144/verify_brpic.py'],
        ['d144/verify_sylow_certificates.py'], ['d144/verify_zest_cocycle.py'],
        ['d32/d144_assist/local_c4.py'], ['d32/d144_assist/nimrep.py'],
        ['d48/verify_decisions.py', '--full'], ['d48/rank6_swap_rings.py'], ['d48/triality_orthogonal.py'],
        ['c6/verify_R332.py'], ['c6/verify_C3_sections.py'], ['c6/verify_R623_C2.py'], ['c6/verify_TY8_lagrangians.py'],
        ['audit_exclusions/audit_R332.py'], ['audit_exclusions/verify_R513_GT.py'],
        ['audit_exclusions/audit_d48_cohomology.py'],
        ['audit_models/audit_d32_nonsplit.py'], ['audit_models/audit_d32_catalog.py'],
        ['audit_models/audit_d144_local_and_tensor.py'],
        ['audit_models/audit_d48_catalog.py'], ['audit_models/audit_h16_independent.py'],
        ['audit_models/audit_quotient_reconstruction.py'], ['audit_models/audit_rank9_quotient_reconstruction.py'],
        ['root/audit_d120_premises.py'], ['root/audit_R350.py'],
    ]
    checks = []
    with tempfile.TemporaryDirectory(prefix='rank12-round4-replay-') as tmp:
        shadow = Path(tmp)
        for name in ['round4', 'prior_round']:
            shutil.copytree(ROOT / name, shadow / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONPATH', None)
        if '--baseline' in sys.argv:
            steps.append(['../prior_round/verify.py'])
        for i, args in enumerate(steps, 1):
            script = (shadow / 'round4' / args[0]).resolve()
            tick = time.monotonic()
            result = subprocess.run([sys.executable, *([] if __debug__ else ['-O']), str(script), *args[1:]], cwd=script.parent, capture_output=True, text=True, env=env)
            (LOG / f'{MODE}_{i:02d}.log').write_text(result.stdout + result.stderr)
            if result.returncode:
                print((result.stdout + result.stderr)[-7000:])
                raise RuntimeError('Replay failed: ' + args[0])
            checks.append(dict(script=args[0], arguments=args[1:], status='PASS', seconds=time.monotonic()-tick))
            print(f'{i:02d}/{len(steps)} PASS {args[0]}', flush=True)
    receipt = dict(status='PASS', excluded=478, modeled=151, unresolved=3, new_exclusions=40,
                   new_models=3, prior_decisions_withdrawn=0, optimized_python=not __debug__,
                   baseline_replayed='--baseline' in sys.argv, steps=checks, seconds=time.monotonic()-started)
    (LOG / (MODE + '.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'steps'}, indent=2))

if __name__ == '__main__':
    main()
