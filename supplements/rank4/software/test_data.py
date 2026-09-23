"""Small regression fixtures read from the released compressed artifacts."""
from pathlib import Path
import gzip,json
from census_data import iter_parameters,parameter_tensor
ROOT=Path(__file__).resolve().parents[1]

def historical_rings():
    with gzip.open(ROOT/'data/historical_32.json.gz','rt') as f:return json.load(f)

def certificate_records():
    with gzip.open(ROOT/'certificates/classification.jsonl.gz','rt') as f:
        header=json.loads(next(f))
        if header.get('schema')!=2:raise ValueError('unsupported test certificate schema')
        for line in f:yield json.loads(line)

def source_tensors(indices):
    wanted=set(indices);out={}
    for sid,tag,p in iter_parameters():
        if sid in wanted:
            out[sid]=parameter_tensor(tag,p)
            if len(out)==len(wanted):return out
    raise ValueError('missing test input')

def historical_labels():
    from collections import Counter
    from rings import multiplicity
    counts=Counter();out={}
    for R in historical_rings():
        m=multiplicity(R);counts[m]+=1;out[f'F_{{{m},{counts[m]}}}']=R
    return out
