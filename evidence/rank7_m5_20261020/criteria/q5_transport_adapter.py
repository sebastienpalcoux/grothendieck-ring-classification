"""Bind the trace engine to the independently verified exact CRT transport."""
import functools
import importlib.util
from quadratic_compression import require, ROOT, tensor_hash

TABLES={
 'R7_5_3895': [[1,0,0,0,0,0,0],[2,2,1,2,-2,-2,0],[2,1,2,2,-2,-2,0],[4,2,2,5,-4,-4,0],[4,2,2,4,-4,-3,0],[4,2,2,4,-3,-4,0],[4,2,2,4,-4,-4,1]],
 'R7_5_5039': [[1,0,0,0,0,0,0],[2,2,1,-2,-2,2,0],[2,1,2,-2,-2,2,0],[4,2,2,-4,-3,4,0],[4,2,2,-3,-4,4,0],[4,2,2,-4,-4,5,0],[4,2,2,-4,-4,4,1]],
}

@functools.lru_cache(maxsize=1)
def verified_transports():
    path=ROOT/'evidence/rank7_m5_20261020/models/sqrt5/verify_transport.py'
    spec=importlib.util.spec_from_file_location('verified_q5_transports',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify_all()

def transport_matrix(N,rid):
    data=verified_transports()[rid]
    require(tensor_hash(N)==data['sha256'], 'source binding for CRT transport')
    T=[[int(v) for v in row] for row in data['T'].tolist()]
    require(T==TABLES[rid], 'CRT transport agrees with recorded matrix')
    return T
