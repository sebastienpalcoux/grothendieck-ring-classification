"""Replay each negative oriented-sphericalization tree admitted to the ledger.

The proof trees for four rank-seven closed subrings are copied into the
rank-eight supplement to make the based-subring transfer independently
checkable.  The 75 rank-eight signed witnesses are pinned to the complete
rank-eight source by both census ID and exact tensor/hash.
"""
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
    inherited=json.loads((ROOT/'data/rank7_certified_negative_subrings.json').read_text())
    assert len(inherited)==4
    for row in inherited:
        tensor=row['tensor']
        assert len(tensor)==7 and analyze.fp(tensor)==row['tensor_sha256']
        advanced_criteria.verify(tensor,row['certificate'])
        print('rank7 inherited exact negative',row['id'],flush=True)

    ids=json.loads((ROOT/'data/signed_certified_witness_ids.json').read_text())
    campaign=json.loads((HERE/'signed_certified_campaign.json').read_text())
    assert ids==[row['id'] for row in campaign['entries']]
    source=analyze.read_source()
    grouped={m:sorted((R for R in source if analyze.mult(R)==m),
        key=lambda R:tuple(x for M in R for line in M for x in line)) for m in (1,2)}
    assert [len(grouped[m]) for m in (1,2)]==[96,877]
    for row in campaign['entries']:
        rid=row['id']
        _,m,j=rid.split('_')
        R=grouped[int(m)][int(j)-1]
        path=HERE/'certificates'/(rid+'.json')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==row['certificate_sha256']
        signed=json.loads(path.read_text())
        assert signed['id']==rid and analyze.fp(R)==signed['tensor_sha256']==row['source_tensor_sha256']
        advanced_criteria.verify(R,signed['certificate'])
        print('rank8 exact signed negative',rid,flush=True)
    print('ALL IMPORTED EXACT PROOF TREES CHECKED',len(inherited),len(ids),flush=True)


if __name__=='__main__':
    main()
