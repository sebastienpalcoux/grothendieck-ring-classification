#!/usr/bin/env python3
"""Read-only default replay of the four accepted R1154 result families.

Producer scripts retain their standalone receipt-writing interface. This
aggregator intercepts their receipt writes in memory and compares complete
JSON values with the checked-in receipts. It never updates those receipts.
"""
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch
import io,json,runpy,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def main():
    pairs=[('verify_semionic_packet.py','semionic_packet.json'),('verify_quartic_witness.py','quartic_witness_replay.json'),('verify_packet_closure.py','packet_closure.json'),('verify_quantum_subgroup_route.py','quantum_subgroup_route.json')]
    results=[]
    for script,receipt in pairs:
        expected_path=HERE/receipt;captured=[]
        expected=json.loads(expected_path.read_text())
        def capture(path,data,*args,**kwargs):
            if path.resolve()!=expected_path:raise ValueError('Unexpected producer write: '+str(path))
            captured.append(json.loads(data));return len(data)
        with patch.object(Path,'write_text',capture),redirect_stdout(io.StringIO()):
            runpy.run_path(str(HERE/script),run_name='__main__')
        if len(captured)!=1 or captured[0]!=expected:raise ValueError('Receipt mismatch: '+receipt)
        results.append({'verifier':script,'receipt':receipt,'status':'PASS'})
    print(json.dumps({'status':'PASS','read_only':True,'scope':'Exact necessary packet data on all25 branches; one quartic witness; joint closure/commutant; one excluded quantum-subgroup route. R1154 remains unresolved.','checks':results},indent=2))
if __name__=='__main__':main()
