#!/usr/bin/env python3
"""Reproduce the pinned-data tensor integrity and uniqueness audit.

No network or untrusted serialized objects are used.  The compressed parameters
are expanded by the documented tensor formulas, and the resulting bytes
must equal the SHA-256-pinned published tensors.  A separate C++ verifier then
checks all tensor axioms and all six unit-fixing basis permutations.  Every
historical rank-four tensor is appended and must match a new representative;
its explicit basis permutation must agree with the retained map.

Census completeness is the result documented in the pinned source repository.
This program checks the supplied tensors, their published digest, fusion axioms,
pairwise nonisomorphism, and agreement with the historical label map.
"""
from pathlib import Path
from collections import Counter
import argparse,csv,gzip,hashlib,json,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from census_data import iter_parameters,parameter_tensor,read_manifest,through32_lookup

PINNED_COMMIT='7f1b36e74df53a8a1cf8597db45d261e408d61b2'
PINNED_PARAMETERS_SHA256='0c3ab657ebfa9c78719e909a7d5857769e0bf791564a67971350237e752aaf6d'
PINNED_TABLES_SHA256='d54fe08711103f970fa08ae346a4d03e9277aac403054a87d89a2d760d8d5fc9'


def require(condition,message):
    if not condition:raise RuntimeError(message)


def audit(root=ROOT):
    root=Path(root)
    start=time.monotonic();manifest=json.loads((root/'data/census_128_manifest.json').read_text());counts=Counter();N=manifest['rings']
    require(manifest['commit']==PINNED_COMMIT,'wrong pinned commit')
    require(hashlib.sha256((root/'data/parameters_128.txt.gz').read_bytes()).hexdigest()==PINNED_PARAMETERS_SHA256,'wrong parameter-file bytes')
    old_bytes=gzip.decompress((root/'data/historical_32.json.gz').read_bytes())
    old=json.loads(old_bytes)
    require(hashlib.sha256(old_bytes).hexdigest()==manifest['source_32_sha256'],'wrong historical census bytes')
    table_hash=hashlib.sha256();tag_counts=Counter();previous=None
    with tempfile.TemporaryDirectory(prefix='rank4-census-audit-') as tmp:
        tmp=Path(tmp);tensor_file=tmp/'tensors.txt';number=0
        with tensor_file.open('wb') as f:
            for i,tag,p in iter_parameters(root/'data/parameters_128.txt.gz'):
                number+=1;counts[max((1,)+p)]+=1;tag_counts[tag]+=1
                require(previous is None or previous<(tag,p),'nonincreasing source order')
                previous=(tag,p)
                line=(json.dumps(parameter_tensor(tag,p),separators=(',',':')).replace('[','{').replace(']','}')+'\n').encode()
                table_hash.update(line);f.write(line)
            require(number==N,'wrong source record count')
            require(table_hash.hexdigest()==PINNED_TABLES_SHA256,'parameters do not reproduce the pinned tensor file')
            for R in old:f.write((json.dumps(R,separators=(',',':'))+'\n').encode())
        require(dict(counts)=={int(k):v for k,v in manifest['by_m'].items()},'parameter counts mismatch')
        exe=tmp/'verify';out=tmp/'audit'
        subprocess.run(['g++','-O3','-std=c++17',str(root/'software/verify_census_tensors.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(tensor_file),str(out),'--exhaustive'],check=True)
        summary=json.loads((out/'summary.json').read_text())
        require(summary['input_records']==N+len(old),'wrong tensor audit count')
        require(summary['distinct_rings']==N,'duplicate or missing fusion rings')
        require(summary['associativity_checked'] is True,'associativity was not checked')
        require(summary['canonical_mode']=='all unit-fixing permutations','incomplete basis-permutation check')
        require(summary['permutations_examined']==6*(N+len(old)),'wrong basis-permutation count')
        lookup={row['new_zero_based_index']:row for row in json.loads(gzip.decompress((root/'data/through32_mapping.json.gz').read_bytes()))};observed_old=set()
        with (out/'line_map.csv').open() as f:
            for r in csv.DictReader(f):
                i=int(r['source_line'])-1
                if i<N:require(r['kind']=='retained','duplicate pinned tensor')
                else:
                    source_index=int(r['representative_source_line'])-1
                    require(source_index<N and r['kind']!='retained','old tensor missing from new census')
                    row=lookup[source_index];observed_old.add(i-N)
                    require(row['old_zero_based_index']==i-N,'historical witness index mismatch')
                    perm=list(map(int,r['permutation_source_to_representative'].split(';')))
                    require(row['permutation_old_to_new']==perm,'historical isomorphism witness mismatch')
        require(observed_old==set(range(len(old))),'incomplete historical comparison')
        with (out/'counts.csv').open() as f:
            for r in csv.DictReader(f):
                require(int(r['rank'])==4,'non-rank-four tensor')
                require(int(r['noncommutative'])==0,'noncommutative tensor')
                require(int(r['distinct_rings'])==counts[int(r['multiplicity'])],'audited count mismatch')
    report={'commit':PINNED_COMMIT,'rank':4,'bound':128,'rings':N,'by_m':dict(sorted(counts.items())),
        'type_counts':dict(tag_counts),'parameters_to_published_tensor_sha256_checked':True,
        'full_tensor_axioms_checked':True,'all_six_unit_fixing_permutations_checked':True,
        'pairwise_nonisomorphism_checked':True,'historical_basis_witnesses_checked':len(old),
        'census_completeness_source':'Pinned fusion-ring-census repository; local audit validates supplied records.',
        'elapsed_seconds':round(time.monotonic()-start,3),'tensor_checker':summary}
    return report


def audit_census(root):
    return audit(root=root)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'verification/census_128_reaudit.json')
    a=p.parse_args();report=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
