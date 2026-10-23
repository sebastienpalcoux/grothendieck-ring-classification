"""Exact fusion-table hypotheses for the Morita--GTY dimension-40 obstruction."""
import gzip, hashlib, itertools, json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise ValueError(message)

def main():
    with gzip.open(BASE/'inputs/rank10_M1_verified/FusionRingMultiplicationTables.txt.gz', 'rt') as f:
        tensors = [json.loads(s.replace('{','[').replace('}',']')) for s in f if s.strip()]
    records = json.load(open(HERE/'certificates.json'))
    for rec in records:
        N = tensors[int(rec['id'].split('_')[-1])-1]
        digest = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
        require(digest == rec['tensor_sha256'], 'input hash')
        inv, two, odd, h = (rec[k] for k in ['invertibles','dimension_two','dimension_sqrt10','h'])
        require(sorted(inv+two+odd)==list(range(10)), 'basis partition')
        require((len(inv),len(two),len(odd))==(4,4,2), 'dimension type')
        dual=[next(j for j in range(10) if N[i][j][0]) for i in range(10)]
        require(dual==rec['dual'], 'duality')
        for a in inv:
            require(N[a][a][0]==1 and sum(N[a][a])==1,'exponent-two group')
            for b in inv:
                require(sum(N[a][b])==1 and sum(N[a][b][c] for c in inv)==1,'pointed group')
                require(N[a][b]==N[b][a], 'abelian invertibles')
        for x in two:
            require({g for g in inv if N[g][x][x]}=={0,h},'left stabilizer')
            require({g for g in inv if N[x][g][x]}=={0,h},'right stabilizer')
        for x,y in [odd, list(reversed(odd))]:
            require(N[h][x][y]==1 and N[x][h][y]==1,'odd free orbit')
        require(any(dual[x]!=x for x in two),'non-self-dual dimension-two simple')
        dims=[(1,0) if i in inv else (2,0) if i in two else (0,1) for i in range(10)]
        for i,j in itertools.product(range(10),repeat=2):
            a,b=dims[i]; c,d=dims[j]
            require((a*c+10*b*d,a*d+b*c)==tuple(sum(N[i][j][k]*dims[k][q] for k in range(10)) for q in range(2)), 'exact FP dimension character')
            for k in range(10):
                require(not N[i][j][k] or int(k in odd)==(int(i in odd)^int(j in odd)), 'dimension grading')
        print(rec['id'], 'PASS: all hypotheses of the Morita--GTY obstruction')
    require({r['id'] for r in records}=={'R10_1_72','R10_1_127'},'scope')

if __name__=='__main__':
    main()
