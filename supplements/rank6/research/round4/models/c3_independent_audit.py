"""Independent C3 phase, detector, scope and certificate mutation checks."""
import copy,itertools,json,math,sys,time,hashlib
from pathlib import Path
import sympy as s
import scipy.optimize as opt
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import field,evaluate,require,VerificationError
from rings import permute,Characters
import round4_higher_c3 as M
from round4_higher_fast import cyclic_three_subrings,cyclic_three_allowed
def blocked(*a,**k):raise RuntimeError('optimizer disabled in independent audit')
opt.linprog=opt.milp=blocked
start=time.monotonic();path=ROOT/'research/round4/higher/R6_6_49_general.json'
c=json.loads(path.read_text());R=next(r['N']for r in json.loads((ROOT/'verification/round4/campaign_manifest.json').read_text())['tensors']if r['id']=='R6_6_49')
checks=[]
# Independently sum the relative Galois action in a common cyclotomic field.
t=s.Symbol('t');C=field(s.Poly(s.cyclotomic_poly(24,t),t));E=field(s.Poly(s.cyclotomic_poly(72,t),t));H=[j for j in range(72)if math.gcd(j,72)==1 and j%24==1]
require(len(H)==3,'wrong relative degree')
phase_checks=0
for omega in range(3):
    expected=({tuple(C.unit**(8*b*k)for k in range(1,4))for b in range(3)}if omega==0 else{(C.zero,C.zero,C.unit**(8*omega))})
    for a in (1,2):
        for b in range(3):
            exponent=8*omega*a*a+24*a*b
            actual=tuple(sum((E.unit**((exponent*k*j)%72)for j in H),E.zero)/E(3)for k in range(1,4))
            require(any(actual==tuple(evaluate(z.to_list(),E.unit**3,E)for z in ph)for ph in expected),'wrong C3 projected phase')
            phase_checks+=1
checks.append(dict(check='direct C72 relative Galois phase sum',cases=phase_checks,passed=True))
# Check every unit-preserving relabelling, including moving the subgroup.
cyclic6=[[[int(k==(i+j)%6)for k in range(6)]for j in range(6)]for i in range(6)]
for label,T in [('R6_6_49',R),('Vec_C6',cyclic6)]:
    old={frozenset((0,g,h))for g,h in cyclic_three_subrings(T)}
    require(bool(old),'control has no C3')
    for tail in itertools.permutations(range(1,6)):
        p=(0,)+tail;inv={v:i for i,v in enumerate(p)}
        expected={frozenset(inv[j]for j in J)for J in old}
        actual={frozenset((0,g,h))for g,h in cyclic_three_subrings(permute(T,p))}
        require(actual==expected,'C3 detector is label dependent')
    checks.append(dict(check='all120 unit-preserving relabellings',input=label,passed=True))

data=M.data_for(R,3,24);uncached=M.data_for
M.data_for=lambda T,h,F:data if T==R and h==3 and F==24 else uncached(T,h,F)
q=c['pseudo']
def reject(name,mut,general=False,T=None):
    try:(M.verify_general if general else M.verify)(R if T is None else T,mut)
    except (VerificationError,ValueError,KeyError)as err:
        checks.append(dict(check=name,rejected=True,reason=str(err)));return
    raise RuntimeError('accepted mutation: '+name)
mut=copy.deepcopy(c);mut['reduction']['kind']='unsupported';reject('invalid general reduction gate',mut,True)
mut=copy.deepcopy(q);mut['branches'].pop();reject('omitted low frame',mut)
mut=copy.deepcopy(q);mut['metadata']['order_bound']+=1;reject('false complete conductor bound',mut)
mut=copy.deepcopy(q);mut['subring']=[0,1,3];reject('wrong C3 subgroup',mut)
mut=copy.deepcopy(q);mut['branches'][0]['columns'][0][1]+=1;reject('altered low column',mut)
live=next(i for i,b in enumerate(q['branches'])if b.get('cases'))
mut=copy.deepcopy(q);mut['branches'][live]['cases']=[r for r in mut['branches'][live]['cases']if r['associator_class']!=2];reject('omitted nontrivial associator class',mut)
mut=copy.deepcopy(q);mut['branches'][live]['cases'].pop();reject('omitted indicator branch',mut)
mut=copy.deepcopy(q);r=mut['branches'][live]['cases'][0];r['ray']=[-v for v in r['ray']];reject('negated exact separating ray',mut)
ans=dict(passed=True,optimizer_disabled=True,python_optimized=not __debug__,
         certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
         domain_cache='exact tensor,height3,conductor24 only',checks=checks,
         scope='independent targeted audit, not a third complete exclusion replay',seconds=time.monotonic()-start)
Path(__file__).with_suffix('.json').write_text(json.dumps(ans,indent=2)+'\n');print(ans,flush=True)
