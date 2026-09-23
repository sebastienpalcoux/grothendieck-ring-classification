"""Shared complete catalog of signed rings surviving universal exact criteria.

The global enumerator quotients by all nonunit basis permutations and sign
gauges. Formal codegrees and cyclotomicity are invariant under these operations.
The catalog is only a common necessary-condition filter: each unsigned tensor
still receives its own bounded signed-lift and categorical-witness checks.
"""
from pathlib import Path
from collections import Counter
import gzip,hashlib,io,json,multiprocessing,subprocess,sys,tempfile,time
from census_data import parameter_tensor
from rapid import dnumber,cyclotomic_failure,casimir_polynomial
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data/signed_universal_128.jsonl.gz'
MANIFEST=ROOT/'data/signed_universal_128_manifest.json'
SOURCE=ROOT/'software/enumerate_global_signed.cpp'


def _filter_chunk(chunk):
    kept=[];counts=Counter()
    for p in chunk:
        R=parameter_tensor('S',p)
        if dnumber(R):counts['dnumber']+=1
        elif cyclotomic_failure(R):counts['cyclotomic']+=1
        else:kept.append((tuple(p),int(casimir_polynomial(R)[0])));counts['retained']+=1
    return kept,dict(counts)


def _chunks(lines,size=512):
    chunk=[]
    for line in lines:
        words=line.split()
        if len(words)!=11 or words[0]!='S':raise ValueError('invalid global signed-enumerator record')
        p=tuple(map(int,words[1:]))
        if max(map(abs,p))>128:raise ValueError('signed global coefficient guard')
        chunk.append(p)
        if len(chunk)==size:yield chunk;chunk=[]
    if chunk:yield chunk


def filter_lines(lines,workers=4):
    counts=Counter();kept=[];start=time.monotonic();last=0
    with multiprocessing.Pool(workers) as pool:
        for part,stats in pool.imap_unordered(_filter_chunk,_chunks(lines),chunksize=1):
            kept.extend(part);counts.update(stats);n=sum(counts.values())
            if n-last>=100000:
                print('GLOBAL SIGNED FILTER',n,dict(counts),round(time.monotonic()-start,1),flush=True);last=n
    kept.sort();
    if len({p for p,d in kept})!=len(kept):raise ValueError('duplicate universally admissible orbit')
    return kept,dict(counts)


def _write_catalog(path,kept):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,compresslevel=6,mtime=0) as compressed,io.TextIOWrapper(compressed,encoding='utf-8',newline='\n') as out:
        for p,det in kept:out.write(json.dumps({'tuple':p,'determinant':str(det)},separators=(',',':'))+'\n')


def build_catalog(lines,bound=128,workers=4,catalog=CATALOG,manifest=MANIFEST,generator_source=SOURCE):
    start=time.monotonic();kept,counts=filter_lines(lines,workers)
    if any(max(map(abs,p))>bound for p,d in kept):raise ValueError('catalog coefficient exceeds requested bound')
    temporary=catalog.with_suffix(catalog.suffix+'.tmp');_write_catalog(temporary,kept);temporary.replace(catalog)
    report={'schema':1,'bound':bound,'total_orbits':sum(counts.values()),'universal_dnumber_rejections':counts.get('dnumber',0),
        'universal_cyclotomic_rejections':counts.get('cyclotomic',0),'retained_orbits':len(kept),
        'catalog_sha256':hashlib.sha256(catalog.read_bytes()).hexdigest(),
        'generator_source_sha256':hashlib.sha256(generator_source.read_bytes()).hexdigest(),
        'filter_source_sha256':hashlib.sha256(Path(__file__).with_name('rapid.py').read_bytes()).hexdigest(),
        'pipeline_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds':round(time.monotonic()-start,3),'scope':'All associative self-dual signed rank-four tensors of coefficient absolute value at most bound, modulo S3 and sign gauges, after necessary formal-codegree d-number and cyclotomicity conditions.',
        'verified':False}
    temporary_manifest=manifest.with_suffix(manifest.suffix+'.tmp');temporary_manifest.write_text(json.dumps(report,indent=2)+'\n');temporary_manifest.replace(manifest);return kept,report


def load_catalog(catalog=CATALOG,manifest=MANIFEST,require_bound=128):
    report=json.loads(manifest.read_text())
    if report['schema']!=1 or (require_bound is not None and report['bound']!=require_bound):raise ValueError('wrong universal signed catalog scope')
    if hashlib.sha256(catalog.read_bytes()).hexdigest()!=report['catalog_sha256']:raise ValueError('universal signed catalog checksum mismatch')
    with gzip.open(catalog,'rt') as f:
        rows=[(tuple(r['tuple']),int(r['determinant'])) for line in f if (r:=json.loads(line))]
    if len(rows)!=report['retained_orbits'] or rows!=sorted(rows) or len({p for p,d in rows})!=len(rows):raise ValueError('invalid universal catalog ordering/size')
    return rows,report



def build_from_enumerator(bound=128,workers=4,threads=4):
    with tempfile.TemporaryDirectory(prefix='rank4-global-build-') as td:
        exe=Path(td)/'global_signed'
        subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(SOURCE),'-o',str(exe)],check=True)
        process=subprocess.Popen([str(exe),str(bound),str(threads)],stdout=subprocess.PIPE,text=True,bufsize=1048576)
        try:rows,report=build_catalog(process.stdout,bound=bound,workers=workers)
        finally:process.stdout.close()
        if process.wait()!=0:
            if MANIFEST.exists():MANIFEST.unlink()
            raise ValueError('global signed enumeration failed')
    return rows,report


def verify_global_catalog(workers=4,threads=4):
    rows,report=load_catalog()
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=report['generator_source_sha256']:raise ValueError('global signed generator source mismatch')
    if hashlib.sha256(Path(__file__).with_name('rapid.py').read_bytes()).hexdigest()!=report['filter_source_sha256']:raise ValueError('universal criterion source mismatch')
    if hashlib.sha256(Path(__file__).read_bytes()).hexdigest()!=report.get('pipeline_source_sha256'):raise ValueError('universal catalog pipeline source mismatch')
    start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='rank4-global-signed-') as td:
        exe=Path(td)/'global_signed'
        subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(SOURCE),'-o',str(exe)],check=True)
        process=subprocess.Popen([str(exe),'128',str(threads)],stdout=subprocess.PIPE,text=True,bufsize=1048576)
        try:regenerated,counts=filter_lines(process.stdout,workers)
        finally:process.stdout.close()
        if process.wait()!=0:raise ValueError('global signed enumeration failed')
    if regenerated!=rows:raise ValueError('universal signed catalog differs from exhaustive replay')
    if sum(counts.values())!=report['total_orbits'] or counts.get('dnumber',0)!=report['universal_dnumber_rejections'] or counts.get('cyclotomic',0)!=report['universal_cyclotomic_rejections']:raise ValueError('universal signed criterion counts disagree')
    result={**report,'verified':True,'verification_elapsed_seconds':round(time.monotonic()-start,3)}
    (ROOT/'verification/global_signed_catalog.json').write_text(json.dumps(result,indent=2)+'\n');return result
