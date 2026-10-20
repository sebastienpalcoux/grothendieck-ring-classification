"""Exact negative-indicator separators for the two q5 low frames."""
import argparse
import hashlib
import json
import explore as e
q=e.q;HERE=e.HERE


def run(discover=False):
    path=HERE/'R7_5_3895_negative_indicator_certificate.json'
    domain_path=HERE/'R7_5_3895_domains.json';domains=json.loads(domain_path.read_text())
    if discover:cert={'domain_sha256':hashlib.sha256(domain_path.read_bytes()).hexdigest(),'separators':[],'cases':[]}
    else:cert=json.loads(path.read_text())
    q.require(cert['domain_sha256']==hashlib.sha256(domain_path.read_bytes()).hexdigest(),'domain content binding')
    inventory=[]
    for dom in domains:
        for ci,case in enumerate(dom['cases']):
            if -1 not in case['sign']:continue
            cols=dom['columns'];rhs=case['rhs'];key=(dom['low_index'],ci)
            if discover:
                idx=q.separate(cols,rhs,cert['separators']);q.require(idx is not None,'negative indicator branch separated')
                cert['cases'].append({'low_index':key[0],'case':key[1],'separator':idx})
            else:
                record=next((r for r in cert['cases'] if (r['low_index'],r['case'])==key),None)
                q.require(record is not None,'complete negative indicator branch cover');idx=record['separator']
            y=cert['separators'][idx]
            q.require(len(y)==len(rhs) and all(type(x)is int for x in y),'integer separating covector')
            q.require(q.base.dot(rhs,y)<0 and all(q.base.dot(c,y)>=0 for c in cols),'strict exact negative-indicator separation')
            inventory.append(key)
    q.require(len(inventory)==len(cert['cases'])==8,'all eight negative-indicator labellings')
    if discover:path.write_text(json.dumps(cert,indent=2)+'\n')
    result={'status':'PASS','negative_cases':len(inventory),'separators':len(cert['separators']),'optimized_python':not __debug__,'optimizer_used':discover}
    if not discover:(HERE/('negative_indicator_replay_'+('normal' if __debug__ else 'optimized')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--discover',action='store_true');a=p.parse_args();run(a.discover)
