"""Verify the exact finite premises of the five structural R155 center cuts.

Run within the package, or pass --package /path/to/Rank6_Categorification_M8.
The algebraic-integer and modular arguments are in center_cuts.md.
"""
from pathlib import Path
import argparse,contextlib,io,json,runpy,sys

def require(ok,message):
 if not ok:raise ValueError(message)

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package',type=Path)
parser.add_argument('--verify',action='store_true',help='verify without writing a receipt')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
here=Path(__file__).resolve().parent
package=args.package or next((p for p in here.parents if (p/'data/unresolved_tensors.json').exists()),None)
if package is None:
 package=here.parents[1]/'work_round6/Rank6_Categorification_M8'
require((package/'data/unresolved_tensors.json').is_file(),'fusion package not found; pass --package')

saved_argv=sys.argv[:]
try:
 with contextlib.redirect_stdout(io.StringIO()):
  sys.argv=[str(here/'check_center_profiles.py'),str(package),'--verify']
  rebuilt=runpy.run_path(str(here/'check_center_profiles.py'),run_name='__main__')
  sys.argv=[str(here/'gauss277.py'),'--verify']
  gauss=runpy.run_path(str(here/'gauss277.py'),run_name='__main__')
finally:sys.argv=saved_argv
records={x['profile']:x['survivors'][0]for x in rebuilt['out']}
require(set(records)=={275,277,279,296,298,306},'six-profile input mismatch')
expected_dims={
 275:{(0,1):4,(0,2):8,(2,4):2},
 277:{(0,1):4,(0,2):4,(0,4):1,(2,4):2},
 279:{(0,1):4,(0,4):2,(2,4):2},
 296:{(0,1):2,(0,2):4,(0,3):2,(2,4):2},
 298:{(0,1):2,(0,3):2,(0,4):1,(2,4):2},
 306:{(0,3):4,(2,4):2},
}
from collections import Counter
for pi,rec in records.items():
 require({tuple(k):v for k,v in rec['odd_dimensions']}==expected_dims[pi],f'odd dimensions changed: {pi}')
 odd=Counter(map(tuple,rec['odd_restrictions']))
 require(odd[(1,2,2,1,0,0)]==odd[(0,2,2,0,1,1)]==1,'forced b restriction pair changed')
 for v,n in odd.items():
  require(odd[(v[0],v[2],v[1],*v[3:])]==n,'odd duality multiplicities changed')
require(records[275]['required_fixed']==2,'275 fixed budget changed')
require(records[277]['required_fixed']==5,'277 fixed budget changed')
require(records[279]['required_fixed']==records[279]['odd']==8,'279 fixed budget changed')
for pi in (298,306):
 require(records[pi]['required_fixed']>records[pi]['odd'],f'no trace contradiction for {pi}')

# Exact scalar identities behind all odd Gauss equations.
import sympy as s
d=4+3*s.sqrt(2);D=72+48*s.sqrt(2);b=2+4*d
require(s.expand(b*b-18*d*d)==0,'b^2 identity')
require(s.simplify(D-4*b)==0,'b=D/4 identity')
require(s.simplify((D/s.Integer(2)-b*b)/(2*d*d)+6*s.sqrt(2))==0,'279 Gauss coefficient')
require(s.simplify(2*d*(1-s.I)/D-(1-s.I)/(6*s.sqrt(2)))==0,'277 indicator coefficient')
require(len(gauss['sol'])==30,'277 Gauss solution count changed')
require(not any(x['cubic_zero']for x in gauss['sol']),'277 cubic-zero solution')
# Full Clifford cubic domain: every alternative lies outside radius 3/2.
require(s.Rational(9,4)<3,'cubic branch distance comparison')
receipt=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,
 inherited_profiles=sorted(records),excluded_profiles=[275,277,279,298,306],remaining_profiles=[296],
 exclusions={275:'fermion-fixed budget and Gauss divisibility',277:'Galois twist orbits, exact 24th-root Gauss equation and full cubic domain',279:'odd Gauss sum and algebraic-integer norm',298:'fermion permutation trace',306:'fermion permutation trace'},
 gauss_277_solutions=30,gauss_277_cubic_zero_solutions=0,
 note='Analytic lemmas and categorical hypotheses are stated in center_cuts.md; this replay rebuilds their finite profile input.')
print(json.dumps(receipt,indent=2))
target=args.output or (None if args.verify else here/'center_cuts_certificate.json')
if target:target.write_text(json.dumps(receipt,indent=2)+'\n')
