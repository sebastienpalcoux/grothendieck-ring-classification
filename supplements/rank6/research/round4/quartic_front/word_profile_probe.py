import sys,json,itertools,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
from fractions import Fraction
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';height=int(sys.argv[2]) if len(sys.argv)>2 else 6;R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];root=Path(__file__).parent;vs=json.load(open(root/(rid+'_count_space.json')))['vectors'];V=list(map(tuple,vs));sp=Spectrum(tab,cols,[(v,None) for v in V]);typ=dict(zip(sp.vectors,sp.types));src=json.load(open(root/(rid+'_filtered_profiles.json')));out=[]
for br in src:
 lab=br['lab'];accepted=br['accepted'];active={z['profile_index']:z for z in accepted};reject=[];allv=list(dict.fromkeys(map(tuple,cols)))+[(0,)+v for v in V];lw=Counter(map(tuple,cols));weights={v:tab.dims[v]**2/tab.D**2 for v in allv};powers={v:[[C.one]+[typ[v][lab[a]]**k for k in range(1,height+1)] for a in range(1,6)] for v in allv};nw=0
 for degree in range(4,height+1):
  for word in itertools.combinations_with_replacement(range(1,6),degree):
   cc=Counter(word);ww={v:weights[v] for v in allv}
   for a,k in cc.items():
    for v in allv:ww[v]*=powers[v][a-1][k]
   const=sum((C(n)*ww[v] for v,n in lw.items()),C.zero);co=[ww[(0,)+v] for v in V]
   for ix,p in list(active.items()):
    value=const+sum((C(n)*z for n,z in zip(p['counts'],co) if n),C.zero);pp=value.to_list()
    if len(pp)>1 or (pp and (pp[0].denominator!=1 or pp[0]<0)):
     reject.append(dict(profile_index=ix,word=word,value=list(map(str,pp))));del active[ix]
   nw+=1
  print(rid,lab,'height',degree,'survive',len(active),flush=True)
 rec=dict(id=rid,lab=lab,height=height,words_checked=nw,rejected=reject,survivors=list(active.values()));out.append(rec);(root/(rid+'_word_profiles_h'+str(height)+'.json')).write_text(json.dumps(out,indent=2)+'\n')
