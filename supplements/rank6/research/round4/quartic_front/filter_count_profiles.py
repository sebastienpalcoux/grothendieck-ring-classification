import sys,json,itertools,time,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
from exact import vector
import sympy as s
from fractions import Fraction
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];root=Path(__file__).parent;cs=json.load(open(root/(rid+'_count_space.json')));V=list(map(tuple,cs['vectors']));profiles=json.load(open(root/(rid+'_count_profiles.json')))['counts'];sp=Spectrum(tab,cols,[(v,None) for v in V]);typ=dict(zip(sp.vectors,sp.types));out=[]
for lab in tab.assignments(cols):
 print('start',lab,flush=True);triples=list(itertools.combinations_with_replacement(range(1,6),3));weights=[];low=[]
 for a,b,c in triples:
  ww={v:typ[v][lab[a]]*typ[v][lab[b]]*typ[v][lab[c]]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)};weights.append([ww[(0,)+v] for v in V]);low.append(sum((ww[v] for v in cols),C.zero))
 coeff=[]
 for j in range(len(triples)):
  # Clear denominators once, preserving all ambient coefficients.
  row=[vector(x,C.mod.degree()) for x in [low[j]]+weights[j]]
  for h in range(C.mod.degree()):
   pp=[Fraction(x[h]) for x in row];den=math.lcm(*(x.denominator for x in pp));coeff.append((j,h,den,[int(x*den) for x in pp]))
 accepted=[];reject={};galois_gram=len(profiles)
 for ix,x in enumerate(profiles):
  triplevalues=[None]*len(triples);bad=None
  for j,h,den,row in coeff:
   value=row[0]+sum(a*b for a,b in zip(row[1:],x))
   if h and value:bad='nonrational_low_fusion';break
   if not h:
    if value<0 or value%den:bad='nonintegral_or_negative_low_fusion';break
    triplevalues[j]=value//den
  if bad:reject[bad]=reject.get(bad,0)+1;continue
  conj=lambda z:evaluate(z.to_list(),C.unit**(data['F']-1),C)
  star=[lab.index(tab.rows.index(tuple(conj(z) for z in tab.rows[lab[a]]))) for a in range(6)];n3=dict(zip(triples,triplevalues))
  for a,b in itertools.combinations_with_replacement(range(1,6),2):
   prod=[sum(cols[a][j]*cols[b][k]*R[j][k][i] for j in range(6) for k in range(6)) for i in range(6)]
   rest=[prod[i]-int(a==star[b] and i==0)-sum(n3[tuple(sorted((a,b,star[c]))) ]*cols[c][i] for c in range(1,6)) for i in range(6)]
   if any(z<0 for z in rest):bad='negative_restriction_remainder';break
  if bad:reject[bad]=reject.get(bad,0)+1;continue
  accepted.append(dict(profile_index=ix,counts=x,low_triples=triplevalues,rank=6+sum(x)))
 rec=dict(id=rid,lab=lab,input_profiles=galois_gram,rejected=reject,accepted=accepted);out.append(rec);print('accepted',len(accepted),'ranks',sorted(set(z['rank'] for z in accepted)),'zero sigma',sum(z['counts'][V.index((0,0,1,0,0))]==0 for z in accepted),'zero g',sum(z['counts'][V.index((0,0,0,1,0))]==0 for z in accepted),flush=True);(root/(rid+'_filtered_profiles.json')).write_text(json.dumps(out,indent=2)+'\n')
