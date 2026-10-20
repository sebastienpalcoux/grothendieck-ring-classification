"""Independent exact justification of the frozen R3895 norm slack.

No producer inequality/lattice helpers are imported. The half-cost parity
is checked as an explicit sum of other necessary all-word equations.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = '590b613093643a1c3047e866213050ba7fd87c211a42906de823d0c613d11ad0'
SELECTED = (346,347,359,362,373,382,385,390)


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def verify(case):
    path = HERE / f'R7_5_3895_c8_case{case}_system.json'
    raw = path.read_bytes()
    system = json.loads(raw)
    source = next(r['tensor'] for r in json.loads(
        (ROOT/'supplements/rank7/output/m5/census.json').read_text())
        if r['id']=='R7_5_3895')
    require(digest(source)==system['source_sha256']==SOURCE,'canonical tensor')
    cut = system['norm_cut_coefficients']
    require(list(map(F,cut['x']))==[F(0),F(1,2),F(1,2),F(0),F(1),F(1),F(0)],
            'the exact source multiplier')
    require(all(F(a).denominator==1 for a in cut['low_linear_weights']),
            'integral coefficients of the actual low fusion multiplicities')
    require(F(cut['constant']).denominator==1,'integral source constant')
    # For n>=0, max_{k>=0 integer} ((n/2)k-k^2) = floor(n^2/8)/2.
    # The exact finite residue proof only depends on n modulo eight.
    for n in range(24):
        direct = max(F(n*k,2)-k*k for k in range(n//2+2))
        require(direct==F((n*n)//8,2),'quadratic integer maximum identity')
    costs = []
    for orbit in system['orbits']:
        twice_cost = 0
        for v,gram,z in orbit:
            n = v[0]+v[1]+2*v[3]+2*v[4]
            require(type(n)is int and n>=0,'nonnegative integral doubled multiplier')
            twice_cost += (n*n)//8
        costs.append(F(twice_cost,2))
    labels = system['phase_labels']
    columns = system['columns']
    rhs = system['rhs']
    words = system['all_word_congruences']
    require(words['source_sha256']==SOURCE,'necessary all-word source binding')
    # Verify that every selected system row is the corresponding all-word
    # congruence, with only the exact denominator-clearing scale applied.
    row_checks = []
    for row in SELECTED:
        rec = words['constraints'][row-346]
        modulus = rec['modulus']
        constant = rec['constant'] % modulus
        slack = [j for j,col in enumerate(columns) if j>=len(labels)
                 and col[row]<0 and sum(x!=0 for x in col)==1]
        require(len(slack)==1,'one all-word integer quotient variable')
        factor = F(-columns[slack[0]][row],modulus)
        require(factor>0,'positive exact equation scaling')
        for j,col in enumerate(columns):
            expected = (labels[j]['multiplicity_unit']*
                        (rec['coefficients'][labels[j]['orbit']] % modulus)
                        if j<len(labels) else -modulus if j==slack[0] else 0)
            require(col[row]==factor*expected,'independent all-word row reconstruction')
        require(rhs[row]==-factor*constant,'independent all-word target reconstruction')
        row_checks.append({'row':row,'modulus':modulus,'scale':str(factor)})
    parity = [int(2*costs[lab['orbit']]*lab['multiplicity_unit'])%2 for lab in labels]
    parity += [0]*(len(columns)-len(labels))
    require(all(sum(col[row] for row in SELECTED)%2==parity[j]
                for j,col in enumerate(columns)), 'explicit parity identity on every column')
    require(sum(rhs[row] for row in SELECTED)%2==0,'even target parity')
    return {'case':case,'system_sha256':hashlib.sha256(raw).hexdigest(),
            'half_integral_orbit_costs':sum(c.denominator==2 for c in costs),
            'columns_checked':len(columns),'selected_all_word_rows':row_checks,
            'norm_row_excluded':345,'conclusion':'The total orbit cost and the actual unscaled norm gap are integers.'}


def main():
    out={'status':'PASS','source_sha256':SOURCE,'optimized_python':not __debug__,
         'results':[verify(0),verify(2)],
         'scope':'The frozen R3895 slack encoding is necessary; no categorification exclusion follows by itself.'}
    path=HERE/f'r3895_norm_parity_{"optimized" if not __debug__ else "normal"}.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':
    main()
