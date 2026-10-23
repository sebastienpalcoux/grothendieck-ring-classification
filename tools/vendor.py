#!/usr/bin/env python3
"""Fetch only hash-bound scientific inputs while building; runtime is offline."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import gzip, hashlib, json, os, time, urllib.request
ROOT=Path(__file__).resolve().parents[1]
def digest(data): return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def fetch(entry, base):
    target=ROOT/"vendor"/entry["path"]
    if target.is_file() and digest(target.read_bytes())==entry["git_blob_sha"]: return
    url=base+"/"+entry["path"]; last=None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as response: data=response.read()
            if digest(data)!=entry["git_blob_sha"]: raise ValueError("Git blob checksum mismatch: "+entry["path"])
            if len(data)!=entry["bytes"]: raise ValueError("Byte-count mismatch: "+entry["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary=target.with_name(target.name+".download")
            temporary.write_bytes(data); os.replace(temporary,target); return
        except Exception as error:
            last=error
            if attempt<3: time.sleep(1+attempt)
    raise RuntimeError(str(url)+": "+str(last))
def main():
    manifest=json.loads((ROOT/"vendor_manifest.json").read_text())
    base="https://raw.githubusercontent.com/"+manifest["repository"]+"/"+manifest["commit"]
    entries=manifest["files"]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(fetch,entry,base) for entry in entries]
        for future in as_completed(futures): future.result()
    for entry in manifest.get("restored",[]):
        compressed=b"".join((ROOT/"vendor"/part["path"]).read_bytes() for part in entry["parts"])
        data=gzip.decompress(compressed) if entry["encoding"]=="gzip" else compressed
        if len(data)!=entry["bytes"] or hashlib.sha256(data).hexdigest()!=entry["sha256"]:
            raise ValueError("Restored input mismatch: "+entry["path"])
        target=ROOT/"vendor"/entry["path"];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print("Scientific inputs:",len(entries),"pinned files;",len(manifest.get("restored",[])),"restored inputs",flush=True)
if __name__=="__main__":main()
