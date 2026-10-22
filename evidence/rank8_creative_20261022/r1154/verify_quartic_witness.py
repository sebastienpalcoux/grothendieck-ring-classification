"""Replay one surviving exact fourth-word Gram/restriction witness, not a model."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
import quartic_projection_probe as q
l=q.l;s=q.s
p=Path(__file__).with_name('quartic_extension_results.json');raw=json.loads(p.read_text())
cert=raw['first_witnesses']['6971:1']['quartic_witness'];a,group,sig,inds,C,hh=q.context(6971)
W=[()]+[(i,)for i in range(1,5)]+l.pairs+l.triples+a['Q']
vecs=[];mc=[]
for j in range(5):
 vecs.append([a['mom'](w+((j,)if j else ()))for w in W]);mc.append(l.cols[j])
actual_counts={};actual_pairs={}
for z in cert:
 typ,x,t=z['type'],z['pair11'],z['triple133'];row,base,q3,opts=l.row_data(group,typ,x,sig);vb=[row[i]for i in inds]
 tri=[sum(y*C[k][j]for k,y in enumerate(vb))+(F(t)-q3)*hh[j]for j in range(20)]
 wd={w:row[i]for i,w in enumerate(l.words)};wd.update(dict(zip(l.triples,tri)));v=[F(wd[w])for w in a['B']]
 zz=[sum(v[i]*F(a['C'][i,j])for i in range(len(v)))for j in range(len(a['Q']))];alpha=F(a['H'][0,0]);h=[F(a['H'][0,j])/alpha for j in range(len(a['Q']))]
 for val,n in z['quartic1111_histogram']:
  quart=[x+(F(val)-zz[0])*y for x,y in zip(zz,h)];allw=dict(wd);allw.update(dict(zip(a['Q'],quart)));vv=[F(allw[w])for w in W]
  if not all(x.denominator==1 and x>=0 for x in vv):raise ValueError('nonnegative integer word coefficients')
  for _ in range(n):vecs.append(list(map(int,vv)));mc.append((0,)+tuple(l.domain['high_columns'][typ]))
  actual_counts[typ]=actual_counts.get(typ,0)+n;actual_pairs[typ,x]=actual_pairs.get((typ,x),0)+n
counts=l.domain['completions'][6971]
if actual_counts!={i:n for i,n in enumerate(counts)if n}:raise ValueError('full restriction pattern')
pr=next(r for r in l.fibers['results']if r['index']==6971);hist=pr['pair11_histogram_solutions_by_high_type'][1]
if actual_pairs!={(typ,x):n for typ,his in enumerate(hist)for x,n in his if n}:raise ValueError('accepted pair histogram')
V=s.Matrix(vecs);G=s.Matrix(len(W),len(W),lambda i,j:a['mom'](W[i]+W[j]));M=s.Matrix(mc).T
if V.T*V!=G:raise ValueError('full degree-eight Gram equality')
restr=s.Matrix([l.restriction(w)for w in W]).T
if M*V!=restr:raise ValueError('all eight restriction coordinates')
out={'schema':'r1154-quartic-witness-replay/v1','status':'PASS','pattern':6971,'pair_histogram':1,'center_rank':V.rows,'word_count':len(W),'word_span_rank':V.rank(),'full_gram_entries_checked':len(W)**2,'restriction_entries_checked':8*len(W),'scope':'One exact necessary fourth-word Gram extension survives. No exhaustive higher-word search, full fusion matrix, modular datum, algebra or category is asserted.','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('quartic_witness_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
