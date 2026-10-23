"""Read literal fusion coefficients as data; do not execute Mathematica code.

The downloaded package is locally retained for research, outside the release
dependency manifest. This program outputs hashes, inventory and basis maps,
not the third-party F-symbol data or fusion tensors.
"""
from pathlib import Path
import hashlib, itertools, json, re, sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from common import read, sha, validate, based_iso, require


def main():
    source = read()
    inventory = []
    matches = []
    for path in sorted((HERE / 'Titsworth_Hagge/Data').glob('*.m')):
        text = path.read_text()
        declarations = re.findall(r'^rank\[([^\]]+)\]\s*\^=\s*(\d+)', text, re.M)
        for symbol, raw_rank in declarations:
            n = int(raw_rank)
            record = {'file': str(path.relative_to(HERE)), 'symbol': symbol,
                      'rank': n, 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            inventory.append(record)
            if n != 11:
                continue
            function = re.search(r'^nFunction\[' + re.escape(symbol) +
                                 r'\]\s*\^=\s*(\w+)', text, re.M).group(1)
            entries = re.findall(r'^' + re.escape(function) +
                                 r'\[(\d+),\s*(\d+),\s*(\d+)\]\s*=\s*(\d+)\s*$', text, re.M)
            data = {tuple(map(int, row[:3])): int(row[3]) for row in entries}
            require(len(entries) == len(data) == n ** 3, 'complete literal coefficient table')
            require(set(data) == set(itertools.product(range(n), repeat=3)), 'all ordered coefficients')
            tensor = [[[data[i, j, k] for k in range(n)] for j in range(n)] for i in range(n)]
            validate(tensor)
            require(all(v in (0, 1) for v in data.values()), 'multiplicity one')
            dual = [next(j for j in range(n) if tensor[i][j][0]) for i in range(n)]
            dimensions = [1 if sum(tensor[i][dual[i]]) == 1 else 2 for i in range(n)]
            require(all(dimensions[i] * dimensions[j] ==
                        sum(tensor[i][j][k] * dimensions[k] for k in range(n))
                        for i, j in itertools.product(range(n), repeat=2)), 'positive dimension character')
            categories_match = re.search(r'fusionCategories\[' + re.escape(symbol) +
                                         r'\]\s*\^=\s*\{([^}]+)\}', text, re.S)
            categories = [x.strip() for x in categories_match.group(1).split(',')]
            require(all(re.search(r'ring\[' + re.escape(cat) + r'\]\s*\^=\s*' +
                                  re.escape(symbol) + r'\b', text) for cat in categories),
                    'all category records use the same ring')
            hits = []
            for rid, ring in source.items():
                p = based_iso(tensor, ring)
                if p is not None:
                    require(all(tensor[i][j][k] == ring[p[i]][p[j]][p[k]]
                                for i, j, k in itertools.product(range(n), repeat=3)),
                            'all crosswalk coefficients')
                    hits.append({'id': rid, 'input_tensor_sha256': sha(ring),
                                 'package_to_input': p, 'coefficients_compared': n ** 3})
            require(len(hits) == 1, 'exactly one census isomorphism class')
            record.update({'tensor_sha256': sha(tensor),
                           'commutative': all(tensor[i][j] == tensor[j][i]
                                             for i, j in itertools.product(range(n), repeat=2)),
                           'positive_integral_dimensions': dimensions,
                           'FP_dimension_exact': sum(x * x for x in dimensions),
                           'category_records': categories, 'crosswalk': hits})
            matches.append(record)
    require(len(inventory) == 34 and len(matches) == 1, 'complete supplied package inventory')
    result = {'status': 'PASS', 'source': 'https://mktitsworth.com/fusion-categories/',
              'package_ring_count': len(inventory), 'rank11_ring_count': len(matches),
              'rank11': matches, 'all_ring_inventory': inventory,
              'new_census_model_ids': [],
              'remaining_104_153_match': False,
              'scope': 'Full exact tensor crosswalk; F-symbol pentagons in the third-party package were not reverified.',
              'license': 'CC BY-NC-SA 3.0 IGO; downloaded package stays outside release dependencies.'}
    (HERE / 'titsworth_hagge_crosswalk.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'rings': len(inventory), 'rank11': matches}, indent=2))


if __name__ == '__main__':
    main()
