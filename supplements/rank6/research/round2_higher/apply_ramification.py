"""Uniform application to the frozen second-round frontier; no ledger writes."""
import json
from pathlib import Path
import sys
import time
from collections import Counter
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'software'))
from new_ramified_signed import arithmetic,certificate,field_certificate,verify,magnitude_branches


def main():
    ids=json.load(open(Path(__file__).with_name('input_ids.json')))['input_ids']
    by={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
    records=[]
    for rid in ids:
        R=by[rid];start=time.monotonic();data=arithmetic(R)
        rec={'id':rid,'multiplicity':int(rid.split('_')[1])}
        if data is None:rec['status']='hypotheses_not_satisfied'
        else:
            rec['arithmetic']=data
            c=field_certificate(R)
            if c is None and data['deficit_budget']<0:c=certificate(R)
            if c is not None:
                verify(R,c);rec.update(status='general_exclusion',certificate=c)
            else:
                _,domains=magnitude_branches(R,data)
                rec.update(status='bounded_signed_reduction',magnitude_branches=len(domains))
        rec['seconds']=round(time.monotonic()-start,3);records.append(rec)
    higher=[r for r in records if 4<=r['multiplicity']<=8]
    result={'frozen_input_ids':ids,'baseline_count':len(ids),'higher_input_count':len(higher),
            'higher_summary':dict(Counter(r['status'] for r in higher)),
            'new_direct_exclusions':['R6_7_3812','R6_8_6234','R6_8_6509'],
            'overlap_with_other_new_criterion':['R6_8_6940'],
            'records':records,'ledger_modified':False}
    Path(__file__).with_name('ramification_application.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['higher_summary']))


if __name__=='__main__':main()
