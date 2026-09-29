import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];root=Path(__file__).parent;V=list(map(tuple,json.load(open(root/(rid+'_count_space.json')))['vectors']));sp=Spectrum(tab,cols,[(v,None) for v in V]);typ=dict(zip(sp.vectors,sp.types));allv=list(dict.fromkeys(sp.vectors));sig={v:(tab.dims[v]**2/tab.D**2,)+typ[v] for v in allv};low=Counter(sig[tuple(v)] for v in cols);records=json.load(open(root/(rid+'_word_profiles_h6.json')));out=[]
for br in records:
 for profile in br['survivors']:
  counts=low.copy();bad=[]
  for v,n in zip(V,profile['counts']):
   if n:counts[sig[(0,)+v]]+=n
  for a in range(data['F']):
   if math.gcd(a,data['F'])>1:continue
   z=C.unit**a;trans=Counter()
   for signature,count in counts.items():trans[tuple(evaluate(x.to_list(),z,C) for x in signature)]+=count
   if trans!=counts:bad.append(a)
  rec=dict(id=rid,lab=br['lab'],profile_index=profile['profile_index'],rank=profile['rank'],galois_weighted_signature_pass=not bad,bad_automorphisms=bad);out.append(rec);print(rec,flush=True)
(root/(rid+'_galois_norm_probe.json')).write_text(json.dumps(out,indent=2)+'\n')
