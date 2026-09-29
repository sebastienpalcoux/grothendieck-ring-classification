"""Independent finite-box checks of the exact affine enumerator."""
import sys,json,itertools,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from round4_quartic_profiles import enumerate_affine
from exact import require
rng=random.Random(491);results=[]
fixtures=[([[2,1]],[3],[3,3]),([[0,0]],[1],[2,2]),([[1,-1]],[0],[3,3])]
for i in range(45):
 n=2+i%3;rows=1+i%4;A=[[rng.randrange(-3,4) for _ in range(n)] for _ in range(rows)];b=[rng.randrange(-3,8) for _ in range(rows)];fixtures.append((A,b,[2]*n))
for A,b,ub in fixtures:
 found,stats=enumerate_affine(A,b,ub);expected=[x for x in itertools.product(*(range(v+1) for v in ub)) if all(sum(a*y for a,y in zip(row,x))==rhs for row,rhs in zip(A,b))];require(found==expected,'enumeration differs from independent full box');results.append(dict(variables=len(ub),rows=len(A),solutions=len(found),nodes=stats['nodes']))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(passed=True,optimized_python=not __debug__,fixtures=len(results),results=results),indent=2)+'\n');print('48 exact finite-box comparisons passed')
