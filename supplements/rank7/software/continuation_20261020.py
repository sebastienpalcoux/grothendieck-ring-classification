"""Pure ledger dispatch for the independently reviewed M5 continuation.

The R4982 component replay regenerates files only in an isolated temporary
tree. Assertion-based component programs run with optimization disabled;
the outer dispatch and all other checks remain valid under python -O.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'evidence/rank7_m5_20261020'


def require(value, message):
    if not value:
        raise ValueError(message)


def tensor_hash(R):
    return hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()


def load(name, path):
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check_file(binding, relative):
    require(binding['path'] == relative, 'unexpected proof input path')
    path = ROOT / relative
    require(hashlib.sha256(path.read_bytes()).hexdigest() == binding['sha256'],
            'changed proof input ' + relative)
    return path


def verify_q60(R, certificate):
    rid = certificate['id']
    require(rid in ('R7_5_443', 'R7_5_1214'), 'unsupported conductor-60 input')
    require(certificate['kind'] == 'q60_center_trace_general' and
            certificate['scope'] == 'general_complex', 'conductor-60 scope')
    require(tensor_hash(R) == certificate['tensor_sha256'], 'conductor-60 source binding')
    canonical = json.loads((ROOT / 'supplements/rank7/output/m5/census.json').read_text())
    require(next(row['tensor'] for row in canonical if row['id'] == rid) == R,
            'conductor-60 tensor differs from census')
    check_file(certificate['trace_certificate'],
               f'evidence/rank7_m5_20261020/criteria/{rid}_q60_trace.json')
    check_file(certificate['general_reduction'],
               'evidence/rank7_m5_20261020/sqrt15_reduction/discovery.json')
    reduction = load('m5_sqrt15_reduction', EVIDENCE / 'sqrt15_reduction/verify_reduction.py')
    result = reduction.run()
    require(result['status'] == 'PASS' and rid in [r['id'] for r in result['results']],
            'general-to-positive reduction did not cover input')
    trace = load('m5_q60_trace', EVIDENCE / 'criteria/q60_center_trace.py')
    trace.verify(rid, write_receipt=False)
    return True


def verify_r4982(R, certificate):
    require(certificate['id'] == 'R7_5_4982' and
            certificate['kind'] == 'cyclic3_full_morita_rank13_descent' and
            certificate['scope'] == 'general', 'Morita descent identity or scope')
    require(tensor_hash(R) == certificate['input_tensor_sha256'], 'Morita descent source binding')
    with tempfile.TemporaryDirectory(prefix='rank7_m5_morita_replay_') as tmp:
        isolated = Path(tmp)
        for relative in ('supplements/rank6/software', 'supplements/rank7/software',
                         'evidence/rank7_m5_20261020/modules'):
            destination = isolated / relative
            destination.mkdir(parents=True)
            for source in (ROOT / relative).iterdir():
                if source.suffix in ('.py', '.cpp'):
                    shutil.copyfile(source, destination / source.name)
        helper = 'evidence/rank7_m5_20261019/theory/cyclic3_spectral.py'
        (isolated / helper).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / helper, isolated / helper)
        census = isolated / 'supplements/rank7/output/m5/census.json'
        census.parent.mkdir(parents=True)
        census.write_text(json.dumps([{'id': 'R7_5_4982', 'tensor': R}]) + '\n')
        runner = isolated / 'evidence/rank7_m5_20261020/modules/verify_r4982.py'
        environment = os.environ.copy()
        environment.pop('PYTHONOPTIMIZE', None)
        process = subprocess.run([sys.executable, str(runner)], cwd=isolated,
                                 env=environment, capture_output=True, text=True,
                                 timeout=1200)
        require(process.returncode == 0, 'isolated Morita replay failed:\n' +
                process.stdout[-3000:] + process.stderr[-3000:])
        result = json.loads((runner.parent / 'r4982_exclusion_certificate.json').read_text())
        require(result == certificate, 'regenerated Morita certificate differs')
    return True


def verify_oriented(R, certificate):
    # Only a runtime limit changes: the canonical domains, equations, source
    # modules, and proof checker remain the historical implementations.
    import oriented_extension
    from analyze import verify_own
    original = oriented_extension.enumerate_all

    def with_longer_deadline(tensor, timeout=120):
        return original(tensor, timeout=max(timeout, 1200))

    oriented_extension.enumerate_all = with_longer_deadline
    try:
        verify_own(R, certificate)
    finally:
        oriented_extension.enumerate_all = original
    return True


def verify_q5_cyclic(R, certificate):
    """Replay the complete source-bound cyclic-rotation exclusion chain."""
    rid = certificate['id']
    require(rid in ('R7_5_3895','R7_5_5039'), 'unsupported cyclic-rotation input')
    require(certificate['kind'] == 'q5_cyclic_rotation_general' and
            certificate['scope'] == 'general_complex', 'cyclic-rotation scope')
    require(tensor_hash(R) == certificate['tensor_sha256'],
            'cyclic-rotation canonical tensor binding')
    relative = f'evidence/rank7_m5_20261020/accepted/{rid}_cyclic_rotation_certificate.json'
    path = check_file(certificate['proof_manifest'], relative)
    record = json.loads(path.read_text())
    require(record['kind'] == certificate['kind'] and record['id'] == rid and
            record['scope'] == certificate['scope'] and
            record['tensor_sha256'] == certificate['tensor_sha256'],
            'cyclic-rotation proof manifest identity')
    entrypoint = 'evidence/rank7_m5_20261020/models/sqrt5/verify_r'+rid.split('_')[-1]+'_cyclic_chain.py'
    inputs = record['proof_inputs']
    require(entrypoint in inputs and isinstance(inputs, dict),
            'cyclic-rotation verifier must be bound')
    for relative, digest in inputs.items():
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
                'repository-relative proof dependency')
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest,
                'changed cyclic-rotation proof input ' + relative)
    verifier = load('m5_'+rid+'_cyclic_chain', ROOT / entrypoint)
    result = verifier.verify(rid, R)
    require(result['status'] == 'PASS' and result['id'] == rid and
            result['kind'] == certificate['kind'] and
            result['scope'] == certificate['scope'] and
            result['tensor_sha256'] == certificate['tensor_sha256'] and
            result['read_only'] is True,
            'complete general cyclic-rotation replay failed')
    require(result['proof_manifest'] == inputs,
            'cyclic-rotation dependency closure changed')
    for key, value in record['coverage'].items():
        require(result[key] == value, 'incomplete cyclic-rotation coverage: ' + key)
    require([row['stage'] for row in result['stages']] == record['stage_names'],
            'incomplete cyclic-rotation stage coverage')
    return True
