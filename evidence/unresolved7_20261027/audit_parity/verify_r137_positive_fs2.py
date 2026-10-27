"""Independent standard-library replay of the two stronger feasible systems."""
from pathlib import Path
from fractions import Fraction
import gzip, hashlib, json

HERE=Path(__file__).resolve().parent
receipts=json.loads((HERE/'r137_positive_fs2_receipt.json').read_text())
for rec in receipts:
    sign='plus' if rec['tau']==1 else 'minus'
    prior=(HERE/f'R137_tau_{sign}_prior_system.json.gz').read_bytes()
    if hashlib.sha256(prior).hexdigest()!=rec['prior_sha256']:
        raise ValueError('Prior system hash mismatch')
    old=json.loads(gzip.decompress(prior))
    blob=gzip.decompress((HERE/f'R137_tau_{sign}_positive_fs2_system.json.gz').read_bytes())
    if hashlib.sha256(blob).hexdigest()!=rec['system_sha256']:
        raise ValueError('New system hash mismatch')
    new=json.loads(blob);A,b=new['A'],new['b']
    if A[:-4]!=old['A'] or b[:-4]!=old['b']:
        raise ValueError('An inherited equation changed')
    for row,rhs,j in zip(A[-4:],b[-4:],rec['fixed_indicator_columns']):
        if rhs!=1 or [(i,c) for i,c in enumerate(row) if c]!=[(j,1)]:
            raise ValueError('Wrong new positive-indicator equation')
    witness={int(j):Fraction(v) for j,v in new['witness']}
    if len(witness)!=len(new['witness']) or min(witness.values())<0:
        raise ValueError('Invalid rational witness')
    for row,rhs in zip(A,b):
        if sum(row[j]*v for j,v in witness.items())!=rhs:
            raise ValueError('Witness fails an equation')
    print(json.dumps({'tau':rec['tau'],'status':'EXACT_PASS','equations':len(A),'support':len(witness)}))
