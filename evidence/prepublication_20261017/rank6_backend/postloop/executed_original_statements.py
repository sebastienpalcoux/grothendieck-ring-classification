m1=[d for d in ledger if d['m']==1]
require(len(m1)==39 and sum(d['status']=='excluded' for d in m1)==18 and sum(d['status']=='unitarily_realized' for d in m1)==21,'explicit multiplicity-one classification count mismatch')
positive=set(positive_registry())
require(positive=={d['id'] for d in ledger if d['status'] in POSITIVE_STATUSES},'positive registry not exhaustive for claimed positives')
