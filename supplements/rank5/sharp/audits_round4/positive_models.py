"""Fresh round-four probes on all seventeen known positive model tensors."""
if not __debug__:
    raise RuntimeError("Run this audit with Python assertions enabled")

from pathlib import Path
import itertools
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'final_census/criteria'))
from exact import require, norm_failure, field_failure
from rings import Characters, dnumber, validate
from model_registry import build_model_registry
from decisions import multiplication_matrix
from induction import global_moment_certificate, pseudo_certificate

models = build_model_registry()
subrings = 0
for model in models:
    R = model['tensor']
    validate(R)
    a = Characters(R)
    f, K, ds, D, pD, emb = a.fp()
    require(dnumber(R) is None, 'd-number test excluded a positive model')
    require(norm_failure(pD, a.cf) is None, 'norm test excluded a positive model')
    require(field_failure(f, a.cf, limit=100) is None, 'field test excluded a positive model')
    require(global_moment_certificate(R, a) is None, 'global moment test excluded a positive model')
    require(pseudo_certificate(R, gram_prune=True) is None, 'induction test excluded a positive model')
    count = 0
    for size in range(1, 4):
        for tail in itertools.combinations(range(1, 5), size):
            J = (0,)+tail
            if not all(a.du[i] in J for i in J):
                continue
            if any(R[i][j][k] for i in J for j in J for k in range(5) if k not in J):
                continue
            dimension = sum((ds[i]*ds[a.du[i]] for i in J), K.zero)
            polynomial = multiplication_matrix(D/dimension, K, f).charpoly().as_poly()
            require(all(v.q == 1 for v in polynomial.all_coeffs()),
                    'subcategory-divisibility test excluded a positive model')
            count += 1
    subrings += count
    print(model['name'], ': all necessary-condition probes passed;', count,
          'proper nontrivial fusion subrings checked.', flush=True)
require(len(models) == 17 and subrings == 27, 'incomplete positive-model audit coverage')
print('Positive-model probe complete:', len(models), 'models and', subrings,
      'proper nontrivial fusion subrings.', flush=True)
