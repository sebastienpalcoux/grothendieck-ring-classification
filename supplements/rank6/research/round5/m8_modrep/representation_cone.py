"""Complete signed T-spectrum cone for the canonical level-48 representation."""
import argparse, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from exact import require
HERE=Path(__file__).parent

def records():
 factors=[json.loads((HERE/f'sl2_{m}.json').read_text()) for m in (16,3)]
 require([x['group']['modulus'] for x in factors]==[16,3],'wrong CRT factors')
 merged={};full=[]
 for i,a in enumerate(factors[0]['irreps']):
  for j,b in enumerate(factors[1]['irreps']):
   spec=[0]*48
   for x,p in enumerate(a['T_multiplicities']):
    for y,q in enumerate(b['T_multiplicities']):spec[(3*x+16*y)%48]+=p*q
   sign=a['central_sign']*b['central_sign'];degree=a['degree']*b['degree'];require(sum(spec)==degree,'CRT degree mismatch')
   rec={'factor_irreps':[i,j],'degree':degree,'central_sign':sign,'spectrum':spec};full.append(rec)
   merged.setdefault((tuple(spec),sign),[]).append([i,j])
 require(sum(r['degree']**2 for r in full)==73728,'CRT irreducible degrees incomplete')
 cone=[{'degree':sum(spec),'central_sign':sign,'spectrum':list(spec),'factor_irreps':merged[spec,sign]} for spec,sign in sorted(merged)]
 return {'group':'SL2(Z/48)','group_order':73728,'irreducible_count':len(full),'signed_spectrum_types':len(cone),'cone':cone}

def append_cone(A,b,high_labels,low_counts,low_selfdual_counts=None):
 """Append nonnegative integer irrep multiplicities and central-sign bounds.

 high_labels[j] is (restriction_vector, actual zeta48 exponent) for the
 leading variables. low_counts is the omitted low-root multiplicity vector.
 Signed trace bounds use only the supplied proved low self-dual counts.
 No assertion of feasibility is made.
 """
 require(len(low_counts)==48,'wrong low T spectrum')
 if low_selfdual_counts is None:low_selfdual_counts=[0]*48
 require(len(low_selfdual_counts)==48 and all(0<=a<=b for a,b in zip(low_selfdual_counts,low_counts)),'wrong low self-dual bounds')
 data=records();cone=data['cone'];old=len(A[0]);count=len(cone);total=old+count+48
 require(len(high_labels)<=old,'incorrect high variable prefix')
 AA=[list(row)+[0]*(count+48) for row in A];bb=list(b)
 for k in range(48):
  row=[0]*total
  for j,(v,a) in enumerate(high_labels):
   if a%48==k:row[j]=1
  for j,rec in enumerate(cone):row[old+j]=-rec['spectrum'][k]
  AA.append(row);bb.append(-low_counts[k])
  row=[0]*total
  for j,rec in enumerate(cone):row[old+j]=rec['central_sign']*rec['spectrum'][k]
  row[old+count+k]=-1;AA.append(row);bb.append(low_selfdual_counts[k])
 return AA,bb,{'irreducible_count':data['irreducible_count'],'signed_spectrum_types':count,'equations_added':96,'variables_added':count+48,'low_counts':list(low_counts),'low_selfdual_counts':list(low_selfdual_counts)}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args();out=records();p=HERE/'representation_cone.json'
 if args.verify:require(out==json.loads(p.read_text()),'CRT cone replay mismatch')
 else:p.write_text(json.dumps(out,separators=(',',':'))+'\n')
 files=[Path(__file__).resolve(),p,HERE/'sl2_16.json',HERE/'sl2_3.json',ROOT/'software/exact.py'];receipt={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'irreducible_count':out['irreducible_count'],'signed_spectrum_types':out['signed_spectrum_types'],'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
 (HERE/'representation_cone_replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='files_sha256'},sort_keys=True))
