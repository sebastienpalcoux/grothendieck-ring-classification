"""Small exact bookkeeping for the theoretical relative-center cuts.
No optimizers; categorical arguments are in central_fs_note.tex.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
SRC = Path(__file__).with_name('relative_reduction_certificate.json')

def require(test, message):
    if not test:
        raise RuntimeError(message)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    candidates = json.loads(SRC.read_text())['survivors']
    require(len(candidates) == 58, 'prior arithmetic survivor count changed')
    fs = [a for a in candidates if a['L'] == 1]
    require(len(fs) == 3, 'unexpected nonselfdual-t survivors')
    allones = [a for a in fs if a['A'] == [1]*9]
    require(len(allones) == 1, 'all-ones branch absent or duplicated')
    final = [a for a in fs if a['A'] != [1]*9]
    require({tuple(a['A']) for a in final} == {
        (0,0,0,0,0,0,2,2,3), (0,0,2,0,0,2,0,0,3)},
        'unexpected final representatives')
    profiles = []
    for low in (0,1):
        path = ROOT / f'research/round5/m8_1660/low{low}_profiles.json'
        data = json.loads(path.read_text())
        for branch in data['branches']:
            gidx = branch['high_vectors'].index([1,0,0,0,0])
            for case in branch['cases']:
                counts = Counter(p[gidx] for p in case['profiles'])
                require(set(counts) == {1}, 'a raw profile lacks the unique central lift of g')
                profiles.append({'low':low, 'labelling':case['labelling'],
                    'raw_profile_count':len(case['profiles']),
                    'g_column_multiplicities':dict(counts),
                    'g_high_vector_index':gidx,'source_sha256':digest(path)})
    receipt = {'status':'necessary_reduction_only_original_unresolved',
        'input_sha256':digest(SRC), 'arithmetic_candidates':58,
        'central_FS_cut':{'excluded_L_unit':55,'remaining_labelled':3},
        'central_g_cut':{'excluded_all_ones':1,'remaining_labelled':2,
                        'remaining_factor_exchange_classes':1},
        'all_raw_profile_g_lifts':profiles,'survivors':final}
    target = Path(__file__).with_name('structural_cuts_certificate.json')
    target.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'arithmetic':58,'after_FS':3,'after_central_g':2,
                      'up_to_factor_exchange':1,'raw_profiles_checked':sum(x['raw_profile_count'] for x in profiles)}))
if __name__ == '__main__':
    main()
