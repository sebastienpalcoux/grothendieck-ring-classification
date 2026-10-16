#!/usr/bin/env python3
"""Check the portable exact integer witness; Python standard library only."""
from pathlib import Path
import collections,hashlib,json
HERE=Path(__file__).resolve().parent
def require(test,message):
 if not test:raise ValueError(message)
def load(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def sparse(row):return [[j,c] for j,c in enumerate(row) if c]
def main():
 for name,digest in load('source_manifest.json').items():require(sha(HERE/name)==digest,'Changed input: '+name)
 for name,entry in load('provenance.json').items():require(sha(HERE/name)==entry['sha256'],'Source provenance: '+name)
 d=load('system.json');w=load('witness.json');meta=d['meta'];reps=d['representations'];x=w['solution'];nv=len(x);oldnv=meta['variables'];base_rows=meta['equations']
 require(w['system_sha256']==sha(HERE/'system.json'),'System identity')
 require(len(d['bounds'])==nv==oldnv+len(reps)+48,'Variable coverage')
 require(all(type(v) is int for v in x),'Integer witness')
 for v,(lo,hi) in zip(x,d['bounds']):require(v>=lo and (hi is None or v<=hi),'Witness bound')
 require(len(d['rows'])==len(d['rhs'])==w['equations'],'Equation coverage')
 for row,rhs in zip(d['rows'],d['rhs']):
  require(type(rhs) is int and all(type(j) is int and type(c) is int and 0<=j<nv and c!=0 for j,c in row),'Integer sparse system')
  require([j for j,c in row]==sorted({j for j,c in row}),'Duplicate or unordered sparse coordinate')
  require(sum(c*x[j] for j,c in row)==rhs,'Integer equation')
 raw=load('inputs/low0_profiles.json')['branches'][0]
 case=next(r for r in raw['cases'] if r['labelling']==d['labelling'])
 require(case['profiles'][d['profile_index']]==w['profile'],'Canonical profile identity')
 packet=load('inputs/packet_gram_receipt.json')
 pb=next(r for r in packet['branches'] if r['low']==d['low'] and r['labelling']==d['labelling'])
 require(packet['surviving_count']==1136 and d['profile_index'] in pb['survivors'],'Packet survivor membership')
 require(raw['high_vectors']==d['profile_vectors'],'Restriction-column identity')
 prior=load('inputs/actual48_certificate.json')
 previous=next(r for r in prior['branches'] if r['low']==d['low'] and r['labelling']==d['labelling'] and r['outcome']=='profile_frontier')
 require(d['profile_index'] in previous['unresolved'],'Actual48 survivor membership')
 require(previous['source_sha256']==sha(HERE/'inputs/low0_profiles.json'),'Frozen canonical source hash')
 # Reconstruct every new row, beyond the frozen actual48 necessary system.
 rows=[];rhs=[]
 for k in range(48):
  row=[0]*nv
  for j,(v,a) in enumerate(meta['high_labels']):
   if a==k:row[j]=1
  for j,r in enumerate(reps):row[oldnv+j]=-r['spectrum'][k]
  rows.append(sparse(row));rhs.append(-6 if k==0 else 0)
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=r['central_sign']*r['spectrum'][k]
  row[oldnv+len(reps)+k]=-1
  rows.append(sparse(row));rhs.append(6 if k==0 else 0)
 for h,target in enumerate(d['torus_target']):
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=r['torus_weights'][h]
  rows.append(sparse(row));rhs.append(target)
 compression=d['compression'];require(len(compression['decompositions'])==1,'Unique compression type')
 for h,group in enumerate(compression['eligible_spectrum_types']):
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=int(r['factors'] in group['pairs'])
  rows.append(sparse(row));rhs.append(compression['decompositions'][0].count(h))
 for v,n in zip(d['profile_vectors'],w['profile']):
  row=[0]*nv
  for j,(u,a) in enumerate(meta['high_labels']):row[j]=int(u==v)
  rows.append(sparse(row));rhs.append(n)
 require(rows==d['rows'][base_rows:] and rhs==d['rhs'][base_rows:],'New constraints reconstructed')
 torus=load('inputs/torus_spectra.json')
 eligible={tuple(p) for p in compression['eligible_irrep_pairs']}
 expected=[r for r in torus['irreps'] if r['allowed'] and (r['T0']==0 or tuple(r['factors']) in eligible)]
 require(reps==expected,'Complete eligible representation list')
 # Rebuild each CRT T-spectrum from the two frozen character tables.
 factors=[load('inputs/sl2_16.json'),load('inputs/sl2_3.json')]
 for r in reps:
  a,b=[factors[k]['irreps'][i] for k,i in enumerate(r['factors'])];spectrum=[0]*48
  for i,p in enumerate(a['T_multiplicities']):
   for j,q in enumerate(b['T_multiplicities']):spectrum[(3*i+16*j)%48]+=p*q
  require(spectrum==r['spectrum'] and r['central_sign']==a['central_sign']*b['central_sign'],'CRT character data')
 require(all(x[j]==0 for j,(v,a) in enumerate(meta['high_labels']) if a==0),'No extra twist-one simple')
 for pair in d['known_Ising_pairs']:
  j=next(j for j,r in enumerate(reps) if r['factors']==pair);require(x[oldnv+j]>=1,'Forced Ising summand')
 rank=6+sum(x[:len(meta['high_labels'])])
 require(rank==sum(r['degree']*x[oldnv+j] for j,r in enumerate(reps)),'Representation rank')
 print(json.dumps({'status':'PASS','mathematical_verdict':'PASS_NECESSARY','id':'R6_8_1660','low':d['low'],'profile_index':d['profile_index'],'central_rank':rank,'integer_equations':len(d['rows']),'integer_variables':nv,'twist_one_multiplicity':6,'torus_weights':d['torus_target'],'new_constraints_reconstructed':True,'scope':'Exact witness for the recorded necessary system; not a center, modular datum, fusion category, or categorification. The frozen actual48 rows and finite-group character data are source-bound, not regenerated by this standard-library replay.'},indent=2))
if __name__=='__main__':main()
