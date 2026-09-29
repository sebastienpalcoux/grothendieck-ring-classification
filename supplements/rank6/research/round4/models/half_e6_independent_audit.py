"""Half-E6 source conjugation, indicators, detector and schema audit."""
import copy,itertools,json,sys,time,hashlib
from pathlib import Path
import sympy as s
import scipy.optimize as opt
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import field,evaluate,require,VerificationError
from rings import permute
import round4_higher_e6 as M
from round4_higher_fast import half_e6_subrings
def blocked(*a,**k):raise RuntimeError('optimizer disabled in independent audit')
opt.linprog=opt.milp=blocked
start=time.monotonic();path=ROOT/'research/round4/higher/R6_6_1035_general.json';c=json.loads(path.read_text());q=c['pseudo']
R=next(r['N']for r in json.loads((ROOT/'verification/round4/campaign_manifest.json').read_text())['tensors']if r['id']=='R6_6_1035')
checks=[];t=s.Symbol('t');K=field(s.Poly(s.cyclotomic_poly(12,t),t));z=K.unit
sqrt3=z+z**-1;require(sqrt3**2==K(3),'wrong square root');d=K.one+sqrt3;D=K(2)+d*d
columns=[(1,0,0),(0,1,0)]+[(0,0,1)]*5+[(1,0,1),(0,1,1),(1,1,1)]
exponents=[0,6,-3,5,5,2,-4,0,6,0]
for sign in (-1,1):
    for obj in (1,2):
        value=sum((K(v[obj])*(K(v[0]+v[1])+K(v[2])*d)*z**(sign*2*ex)
                   for v,ex in zip(columns,exponents)),K.zero)/D
        require(value==K.one,'second-indicator source filter invalid')
    for ex in exponents:
        require(evaluate((z**ex).to_list(),z**-1,K)==z**-ex,'source conjugation mismatch')
checks.append(dict(check='both source tables give nu2(g)=nu2(x)=1 and exchange by complex conjugation',passed=True))

E=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,0],[0,0,1]],[[0,0,1],[0,0,1],[1,1,2]]]
control=[[[E[i//2][j//2][k//2]*int(k%2==(i+j)%2)for k in range(6)]for j in range(6)]for i in range(6)]
for label,T in [('R6_6_1035',R),('half_E6_times_Vec_C2',control)]:
    original=half_e6_subrings(T);require(bool(original),'control has no half-E6')
    for tail in itertools.permutations(range(1,6)):
        p=(0,)+tail;inv={v:i for i,v in enumerate(p)}
        require(set(half_e6_subrings(permute(T,p)))=={(inv[g],inv[x])for g,x in original},'half-E6 detector is label dependent')
    checks.append(dict(check='all120 unit-preserving relabellings',input=label,passed=True))

data=M.data_for(R,3,60);uncached=M.data_for
M.data_for=lambda T,h,F:data if T==R and h==3 and F==60 else uncached(T,h,F)
def reject(name,mut,general=False):
    try:(M.verify_general if general else M.verify)(R,mut)
    except (VerificationError,ValueError,KeyError)as err:
        checks.append(dict(check=name,rejected=True,reason=str(err)));return
    raise RuntimeError('accepted mutation: '+name)
mut=copy.deepcopy(q);mut['complex_conjugation_reduction']=False;reject('remove global conjugation reduction',mut)
mut=copy.deepcopy(q);mut['branches'].pop();reject('omit a low frame',mut)
mut=copy.deepcopy(q);mut['metadata']['order_bound']+=1;reject('corrupt conductor bound',mut)
mut=copy.deepcopy(q);mut['subring']=[0,1,5];reject('claim wrong half-E6 subcategory',mut)
live=next(i for i,b in enumerate(q['branches'])if b.get('cases'))
mut=copy.deepcopy(q);mut['branches'][live]['cases'].pop();reject('omit a second-indicator branch',mut)
mut=copy.deepcopy(q);mut['branches'][live]['labellings']=[];reject('omit a character labelling',mut)
mut=copy.deepcopy(q);mut['branches'][live]['cases'][0]['conjugate']=True;reject('unannounced source-table convention',mut)
mut=copy.deepcopy(q);mut['branches'][live]['cases'][0]['indicators'][0]=-1;reject('invalid half-E6 second indicator',mut)
mut=copy.deepcopy(c);mut['scope']='pseudo_unitary';reject('alter general scope',mut,True)
ans=dict(passed=True,optimizer_disabled=True,python_optimized=not __debug__,
         certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),checks=checks,
         scope='source and targeted schema audit; complete numerical-free replays recorded by case and release agents',
         seconds=time.monotonic()-start)
Path(__file__).with_suffix('.json').write_text(json.dumps(ans,indent=2)+'\n');print(ans,flush=True)
