"""Fresh explicit check of both complete stabilizers in the D120 argument.

This checks tensor premises, not the categorical proof or cohomology theorem.
Only the new round-four directory receives output.
"""
from pathlib import Path
import hashlib, itertools, json

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / 'prior_round/round3/d120'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def main():
    sources = json.loads((BASE/'source_tensors.json').read_text())
    meta = json.loads((BASE/'source_meta.json').read_text())
    records = []
    for rid, R in sources.items():
        d = meta[rid]['dimensions']
        G = [i for i in range(12) if d[i] == 1]
        T = [i for i in range(12) if d[i] == 2]
        F = [i for i in range(12) if d[i] == 5]
        require(sorted(d) == [1]*4+[2]*4+[5]*4, 'dimension type')
        require(all(sum(R[i][j][k]*d[k] for k in range(12)) == d[i]*d[j]
                    for i,j in itertools.product(range(12),repeat=2)), 'FP character')
        require(all(not R[i][j][k] for i,j in itertools.product(G+T,repeat=2)
                    for k in F), 'dimension20 closed')
        stabilizers = []
        for x in T:
            left = [g for g in G if R[g][x][x]]
            right = [g for g in G if R[x][g][x]]
            require(left == right and len(left) == 2 and left[0] == 0,
                    'full left and right cyclic stabilizers')
            stabilizers.append(left)
        require(all(H == stabilizers[0] for H in stabilizers), 'same full subgroup')
        b = stabilizers[0][1]
        require(R[b][b][0] == 1, 'order2')
        require(all(not R[b][x][x] and R[b][x] == R[x][b] for x in F),
                'free coincident dimension5 actions')
        compact = json.dumps(R,separators=(',',':')).encode()
        h = hashlib.sha256(compact).hexdigest()
        require(h == meta[rid]['tensor_sha256'], 'input hash')
        records.append(dict(id=rid,tensor_sha256=h,full_common_stabilizer=stabilizers[0],
                            left_and_right_checked=True,closed_dimension20=True,
                            free_coincident_dimension5_actions=True))
    require(len(records)==16, 'all16')
    out = dict(status='PASS', normal_python=__debug__, records=records,
               scope='Exact tensor hypotheses only; categorical arguments separately reviewed.')
    (HERE/('d120_premises.json' if __debug__ else 'd120_premises_optimized.json')).write_text(
        json.dumps(out,indent=2)+'\n')
    print('PASS all 16 D120 full left and right stabilizers')

if __name__ == '__main__':
    main()
