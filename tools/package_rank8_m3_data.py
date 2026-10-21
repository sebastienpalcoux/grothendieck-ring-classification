#!/usr/bin/env python3
"""Register large accepted M3 JSON as checksummed gzip restoration parts."""
import gzip
import hashlib
import json
from pathlib import Path
from rank8_publication import EVIDENCE, extension
ROOT=Path(__file__).resolve().parents[1]
THRESHOLD=4*1024*1024
PART_BYTES=6*1024*1024
def digest(data):return hashlib.sha256(data).hexdigest()
def main():
    if extension(ROOT) is None:raise ValueError('Accepted publication ledger required')
    receipt=json.loads((ROOT/EVIDENCE/'pipeline/continuation_replay.json').read_text())
    optimized=json.loads((ROOT/EVIDENCE/'pipeline/continuation_replay_optimized_invocation.json').read_text())
    if receipt['status']!='PASS' or optimized['status']!='PASS' or receipt['ledger_digest']!=optimized['ledger_digest']:
        raise ValueError('Matching full receipts required')
    for name,sha in receipt['source_manifests_sha256'].items():
        if digest((ROOT/name).read_bytes())!=sha:raise ValueError('Frozen source changed: '+name)
    candidates=sorted({p for folder in (ROOT/EVIDENCE,ROOT/'supplements/rank8/output/m3') for p in folder.rglob('*.json') if p.stat().st_size>=THRESHOLD})
    path=ROOT/'data/large_files_manifest.json';manifest=json.loads(path.read_text());by_path={r['path']:r for r in manifest['files']}
    ignored=(ROOT/'.gitignore').read_text().splitlines();registered=[]
    for source in candidates:
        relative=source.relative_to(ROOT).as_posix();raw=source.read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0)
        part_dir=ROOT/'data/payloads'/relative.replace('/','__').replace('.','_');part_dir.mkdir(parents=True,exist_ok=True);parts=[]
        for index,start in enumerate(range(0,len(packed),PART_BYTES),1):
            chunk=packed[start:start+PART_BYTES];target=part_dir/f'part-{index:03}.bin';target.write_bytes(chunk)
            parts.append({'path':target.relative_to(ROOT).as_posix(),'bytes':len(chunk),'sha256':digest(chunk)})
        if gzip.decompress(b''.join((ROOT/p['path']).read_bytes() for p in parts))!=raw:raise ValueError('Restoration mismatch: '+relative)
        item={'path':relative,'bytes':len(raw),'sha256':digest(raw),'encoding':'gzip','parts':parts};previous=by_path.get(relative)
        if previous:
            history=list(previous.get('previous_sha256',[]))
            if previous['sha256']!=item['sha256'] and previous['sha256'] not in history:history.append(previous['sha256'])
            if history:item['previous_sha256']=history
            manifest['files'][manifest['files'].index(previous)]=item
        else:manifest['files'].append(item)
        retain={Path(p['path']).name for p in parts}
        for old in part_dir.glob('part-*.bin'):
            if old.name not in retain:old.unlink()
        if '/'+relative not in ignored and relative not in ignored:ignored.append('/'+relative)
        registered.append({'path':relative,'bytes':len(raw),'gzip_bytes':len(packed),'parts':len(parts)})
    path.write_text(json.dumps(manifest,indent=2)+'\n');(ROOT/'.gitignore').write_text('\n'.join(ignored)+'\n')
    print(json.dumps({'status':'PASS','registered':registered},indent=2))
if __name__=='__main__':main()
