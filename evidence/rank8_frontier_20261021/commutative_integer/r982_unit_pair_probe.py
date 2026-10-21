"""Exact source-unit product checks on the two saved R982 integer patterns.

The canonical r982.py replay verifies their full integer systems.  This
additive checker verifies all distinguished product unit multiplicities,
which are stronger than the atomic AM--GM relaxation for fixed low columns.
"""
from pathlib import Path
import argparse, itertools, json, sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'global_induction'))
import streaming as st
from exact import require


def run():
    source = st.load_ring('R8_3_982')
    R = source['tensor']
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    profiles = json.loads((HERE / 'R8_3_982_profile.json').read_text())
    require(profiles['tensor_sha256'] == source['tensor_sha256'], 'profile source differs')
    records = []
    for fi in (2, 3):
        old = json.loads((HERE / f'R8_3_982_frame{fi}.json').read_text())
        require(old['tensor_sha256'] == source['tensor_sha256'], 'integer source differs')
        meta = old['metadata']; values = old['original_integer_witness']
        p = profiles['records'][fi]; fp = meta['FP_character']
        vectors = {v['index']: (0,) + tuple(v['vector']) for v in p['high_vectors']}
        labels = [('high_orbit', tuple(o['indices']), tuple(vectors[j] for j in o['indices']))
                  for o in p['duality_orbits']]
        Es = [E for E in range(8) if E != fp]
        labels += [('fusion_coefficient', E, F, G)
                   for E, F in itertools.combinations_with_replacement(Es, 2) for G in Es]
        require(st.digest(labels) == meta['column_labels_sha256'] and len(values) == len(labels),
                'integer label binding differs')
        low = dict(zip(p['character_labels'], map(tuple, p['low_columns'])))
        require(low[fp] == (1,) + (0,) * 7, 'fixed unit differs')
        require(all(v[0] == 1 for v in low.values()), 'low source-unit multiplicities differ')
        dualE = meta['dual_characters']
        require(all(low[dualE[E]] == tuple(low[E][j] for j in dual) for E in range(8)),
                'fixed distinguished duality fails')
        fusion = {tuple(label[1:]): n for label, n in zip(labels, values)
                  if label[0] == 'fusion_coefficient'}
        checks = []
        for E, F in itertools.combinations_with_replacement(Es, 2):
            left = sum(fusion[E, F, G] for G in Es) + int(F == dualE[E])
            right = sum(low[E][i] * low[F][dual[i]] for i in range(8))
            require(left == right, 'source-unit product identity fails')
            checks.append([E, F, left, right])
        records.append({'frame_index': fi, 'integer_record_sha256': st.digest(old),
                        'integer_witness_sha256': st.digest(values), 'checks': checks,
                        'outcome': 'all_distinguished_source_unit_products_exact'})
    return {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
            'scope': 'pseudo_unitary_necessary_system_survival_only',
            'kind': 'fixed_integer_distinguished_unit_product_check',
            'profile_sha256': st.digest(profiles), 'records': records}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    args = ap.parse_args(); result = run()
    path = HERE / 'R8_3_982_unit_pair_probe.json'
    if args.write:
        path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    else:
        require(result == json.loads(path.read_text()), 'unit-product check changed')
    print('PASS R982 exact source-unit products: 28 per integer pattern', flush=True)
