"""Pinned rank-four census, with streaming access and stable historical labels.

The source index is zero based and is the line number in the pinned compressed
parameter file minus one.  The basis of the source tensor is retained.  Labels
through multiplicity 32 refer to the supplied historical ordering; their explicit
basis-isomorphism witnesses are recorded in through32_mapping.json.gz.  Above
32, labels follow parameter-file order within each exact multiplicity.
"""
from collections import Counter
from functools import lru_cache
import gzip,hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PARAMETERS=ROOT/'data/parameters_128.txt.gz'
MANIFEST=ROOT/'data/census_128_manifest.json'
MAPPING=ROOT/'data/through32_mapping.json.gz'


def parameter_tensor(tag,p):
    if tag=='S':
        if len(p)!=10:raise ValueError('self-dual parameter length')
        a,b,c,d,e,f,g,h,i,j=p
        return [[[int(v==w) for w in range(4)] for v in range(4)],
            [[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],
            [[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],
            [[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
    if tag=='N':
        if len(p)!=6:raise ValueError('nonself-dual parameter length')
        a,b,c,d,e,f=p
        x=[[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]]
        y=[[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
        return [[[int(v==w) for w in range(4)] for v in range(4)],x,y,list(map(list,zip(*y)))]
    raise ValueError('unknown parameter tag')


def iter_parameters(path=None,bound=128):
    if type(bound) is not int or not 1<=bound<=128:raise ValueError('bound must be in [1,128]')
    path=Path(path) if path is not None else PARAMETERS
    opener=gzip.open if path.suffix=='.gz' else open
    with opener(path,'rt') as f:
        for source_index,line in enumerate(f):
            words=line.split()
            if not words:raise ValueError('empty census parameter line')
            tag=words[0];p=tuple(map(int,words[1:]))
            if tag not in ('S','N') or len(p)!=(10 if tag=='S' else 6):raise ValueError('invalid census parameter record')
            if any(v<0 or v>128 for v in p):raise ValueError('parameter outside pinned census bound')
            if max((1,)+p)<=bound:yield source_index,tag,p


def iter_rings(bound=128):
    for source_index,tag,p in iter_parameters(bound=bound):
        yield source_index,parameter_tensor(tag,p)


@lru_cache(maxsize=1)
def read_manifest():
    return json.loads(MANIFEST.read_text())


@lru_cache(maxsize=1)
def through32_lookup():
    with gzip.open(MAPPING,'rt') as f: rows=json.load(f)
    return {row['new_zero_based_index']:row for row in rows}


@lru_cache(maxsize=1)
def _local_indices():
    from array import array
    counts=Counter();indices=array('I')
    lookup=through32_lookup()
    for source_index,tag,p in iter_parameters():
        m=max((1,)+p);counts[m]+=1
        indices.append(lookup[source_index]['local_index'] if m<=32 else counts[m])
    return indices


def record_metadata(source_index,tag,p):
    """Metadata for the source basis; old labels are preserved by isomorphism."""
    m=max((1,)+tuple(p));local_index=_local_indices()[source_index]
    result={'index':source_index,'source_index':source_index,'multiplicity':m,
        'local_index':local_index,'label':f'F_{{{m},{local_index}}}',
        'sha256':hashlib.sha256(json.dumps(parameter_tensor(tag,p),separators=(',',':')).encode()).hexdigest()}
    if m<=32:result['old_index']=through32_lookup()[source_index]['old_zero_based_index']
    return result
