"""Exact replay of one frozen rank-eight oriented signed witness."""
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
sys.path.insert(1,str(ROOT/'software'))
import advanced_criteria
import analyze


def main():
    rid=sys.argv[1]
    _,multiplicity,index=rid.split('_')
    multiplicity,index=int(multiplicity),int(index)
    path=HERE/'certificates'/(rid+'.json')
    data=json.loads(path.read_text())
    assert data['id']==rid
    manifest=json.loads((HERE/'signed_certified_campaign.json').read_text())
    row=next(d for d in manifest['entries'] if d['id']==rid)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==row['certificate_sha256']
    rings=sorted((R for R in analyze.read_source() if analyze.mult(R)==multiplicity),
        key=lambda R:tuple(x for M in R for line in M for x in line))
    R=rings[index-1]
    assert analyze.fp(R)==data['tensor_sha256']==row['source_tensor_sha256']
    advanced_criteria.verify(R,data['certificate'])
    print(rid,'exact signed proof checked')


if __name__=='__main__':main()
