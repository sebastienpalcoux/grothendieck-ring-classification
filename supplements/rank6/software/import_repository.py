"""Import the pinned authoritative census, preserving existing tensor identifiers.

This is a source-integrity and coverage check, not a new census enumeration.
Existing representatives must occur exactly in the trusted source. New records
are numbered by exact multiplicity and lexicographic full-tensor order.
"""
import argparse, collections, gzip, hashlib, json, shutil, subprocess
from pathlib import Path
from prepare import read_tables, flatten, dual

P = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify_source(rows=None):
    meta = json.loads((P/'provenance/repository_source.json').read_text())
    src = P/'data/rank6_tables.txt.gz'
    if digest(src) != meta['sha256']:
        raise ValueError('trusted source archive checksum mismatch')
    raw = list(read_tables(src))
    counts = dict(sorted(collections.Counter(max(flatten(R)) for R in raw).items()))
    expected = {int(m):v for m,v in meta['counts'].items()}
    if counts != expected or len(raw) != meta['tensors']:
        raise ValueError('trusted source counts do not match its manifest')
    rows = rows if rows is not None else json.loads((P/'data/census.json').read_text())
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('repeated classification identifier')
    # Multiplicity and representative identity, not independently recomputed
    # based-isomorphism or associativity: those are supplied by the census.
    if collections.Counter(flatten(R) for R in raw) != collections.Counter(flatten(r['N']) for r in rows):
        raise ValueError('classification tensors do not cover the trusted source')
    for r in rows:
        if r['m'] != max(flatten(r['N'])) or r['id'] != f"R6_{r['m']}_{r['index']}":
            raise ValueError('invalid classification multiplicity or identifier')
    return {'tensors':len(raw), 'source_commit':meta['source_commit'],
            'sha256':meta['sha256'], 'counts':counts,
            'method':'pinned-source checksum and exact representative coverage',
            'independent_census_recomputed':False}

def import_source(repo):
    repo=Path(repo).resolve()
    source=repo/'results/rank6/tables.txt.gz'
    manifest=json.loads((repo/'results/census.json').read_text())['ranks']['6']
    if not (manifest['complete'] and manifest['verified']):
        raise ValueError('source does not claim a complete verified rank-six census')
    raw=list(read_tables(source)); available={flatten(R) for R in raw}
    old=json.loads((P/'data/census.json').read_text())
    if any(flatten(r['N']) not in available for r in old):
        raise ValueError('existing representative absent: explicit basis transport is required')
    have={flatten(r['N']) for r in old}; counters=collections.Counter(r['m'] for r in old)
    for R in sorted((R for R in raw if flatten(R) not in have),key=lambda R:(max(flatten(R)),flatten(R))):
        m=max(flatten(R)); counters[m]+=1
        old.append({'id':f'R6_{m}_{counters[m]}','m':m,'index':counters[m],
                    'source_label':None,'dual':dual(R),
                    'commutative':all(R[i][j]==R[j][i] for i in range(6) for j in range(6)), 'N':R})
    old.sort(key=lambda r:(r['m'],r['index']))
    shutil.copy2(source,P/'data/rank6_tables.txt.gz')
    (P/'data/census.json').write_text(json.dumps(old,separators=(',',':'))+'\n')
    meta={'repository':'https://github.com/sebastienpalcoux/fusion-ring-census',
          'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
          'path':'results/rank6/tables.txt.gz','sha256':digest(source),
          'uncompressed_sha256':hashlib.sha256(gzip.decompress(source.read_bytes())).hexdigest(),
          'tensors':manifest['classes'],'bound':manifest['bound'],'counts':manifest['counts'],
          'source_complete':True,'source_verified':True,
          'classification_import':'Existing tensors and identifiers retained exactly; new representatives sorted by full tensor within exact multiplicity.',
          'census_authority':'The referenced repository supplies completeness, validity, and based-isomorphism uniqueness; this package does not repeat its census.'}
    (P/'provenance/repository_source.json').write_text(json.dumps(meta,indent=2)+'\n')
    return verify_source(old)

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('--repository',type=Path)
    args=a.parse_args()
    print(json.dumps(import_source(args.repository) if args.repository else verify_source(),indent=2))
