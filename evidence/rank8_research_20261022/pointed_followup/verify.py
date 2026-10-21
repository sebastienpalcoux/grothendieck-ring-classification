"""Read-only replay of both frozen C2 Fourier-packing results and receipts."""
from pathlib import Path
import hashlib
import json
import sys

from c2_fibres import HERE, require, verify_result


def main():
    require(len(sys.argv)==1,'this accepted verifier takes no arguments')
    root=HERE.parents[2]
    for index in (1768,1795):
        receipt=json.loads((HERE/f'verification_R8_3_{index}.json').read_text())
        expected={k:v for k,v in receipt.items() if k!='sources'}
        require(receipt.get('sources'),'missing frozen source hashes')
        for relative,digest in receipt['sources'].items():
            path=(root/relative).resolve()
            require(root in path.parents,'source hash path escapes repository')
            require(hashlib.sha256(path.read_bytes()).hexdigest()==digest,
                    f'frozen source hash differs: {relative}')
        require(verify_result(index)==expected,'exact replay receipt differs')
    snapshot=json.loads((HERE/'R1795_pointed_associator_obstruction.json').read_text())
    terminal=json.loads((HERE/'R8_3_1795.json').read_text())
    require(snapshot['id']==terminal['id'] and
            snapshot['tensor_sha256']==terminal['tensor_sha256'] and
            snapshot['base_metadata']==terminal['base_metadata'] and
            snapshot['record']==terminal['parities'][0],
            'independently audited R1795 odd snapshot differs from terminal result')
    print('PASS frozen C2 Fourier-fibre results, all recorded branches and source hashes')


if __name__=='__main__':
    main()
