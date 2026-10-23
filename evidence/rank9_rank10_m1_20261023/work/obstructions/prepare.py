from pathlib import Path
import json,gzip,itertools,collections,hashlib
P=Path(__file__).resolve().parents[1]
def read_tables(path):
    f=gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)
    for line in f:
        if line.strip():yield json.loads(line.replace('{','[').replace('}',']'))
def flatten(R):return tuple(x for M in R for row in M for x in row)
def dual(R):return [next(j for j in range(len(R)) if R[i][j][0]) for i in range(len(R))]
def key(R, witness=False):
    # Isomorphism-invariant key: order intrinsic signature classes, then minimize
    # inside them. This is not necessarily the global lexicographic orbit minimum.
    n=len(R);du=dual(R)
    sig=[(int(du[i]==i),tuple(sorted(sum(row) for row in R[i])),tuple(sorted(R[i][du[i]])),sum(R[i][j][j] for j in range(n))) for i in range(1,n)]
    groups=[[i+1 for i,s in enumerate(sig) if s==v] for v in sorted(set(sig))]
    out=None;best=None
    for parts in itertools.product(*(list(itertools.permutations(g)) for g in groups)):
        p=(0,)+tuple(i for g in parts for i in g)
        v=tuple(R[i][j][k] for i in p for j in p for k in p)
        if out is None or v<out:
            out=v;best=p
    return (out,best) if witness else out
if __name__=='__main__':
    # Preparation never re-enumerates or silently restores an obsolete bound.
    from import_repository import verify_source
    print(json.dumps(verify_source(),indent=2))
