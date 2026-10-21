#!/usr/bin/env python3
"""Unrestricted signed audit for R1463, with explicit adjoint-parity failures."""
from pathlib import Path
import argparse, collections, hashlib, json
import verify_nc_gate_unrestricted as gate

HERE=Path(__file__).resolve().parent

def compute():
    source=next(r for r in json.loads((gate.OLD/'pipeline/census_m3.json').read_text()) if r['id']=='R8_3_1463')
    R=source['tensor'];values,p,statistics=gate.unrestricted(R);du=gate.old.dual(R)
    gate.need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'source identity')
    branches=[];counts=collections.Counter()
    for value in values:
        T=gate.old.from_values(R,p,value);gate.old.validate_general(T)
        obstruction=gate.old.proofs.signed_adjoint_parity(R,T)
        if obstruction is not None:
            i=obstruction['object'];gate.need(du[i]==i,'parity object is self-dual')
            for nu,j in zip((-1,1),obstruction['failed_rows']):
                gate.need((R[j][du[j]][i]-nu*T[j][du[j]][i])%4!=0,'explicit parity failure')
        else:
            signs=gate.old.proofs.gauge_original(T,R)
            gate.need(signs is not None and signs[0]==1 and all(signs[i]==signs[du[i]] for i in range(8)),'dual-compatible spherical section')
            gate.need(all(T[i][j][k]==signs[i]*signs[j]*signs[k]*R[i][j][k] for i in range(8) for j in range(8) for k in range(8)),'all gauge multiplication identities')
            obstruction={'kind':'gauge_original','signs':signs}
        counts[obstruction['kind']]+=1
        branches.append({'values':list(value),'obstruction':obstruction})
    gate.need(len(values)==512 and counts=={'gauge_original':128,'signed_adjoint_parity':384},'full signed accounting')
    return {'result':'PASS','id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'scope':'every complex categorification admits a spherical section',
            'complete_signed_count':len(values),'native_statistics':statistics,
            'normalized_indicator_domains_used':False,'commutativity_assumed':False,
            'branch_counts':dict(counts),'branches':branches}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'r1463_signed_unrestricted.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:gate.need(result==json.loads(path.read_text()),'complete unrestricted signed receipt')
    print('PASS R1463 all 512 unrestricted signed tensors: 384 explicit adjoint-parity failures and 128 spherical sections')

if __name__=='__main__':main()
