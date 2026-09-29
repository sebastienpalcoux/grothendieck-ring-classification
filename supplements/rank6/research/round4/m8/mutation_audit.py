import copy,json,sys,time
from pathlib import Path
import scipy.optimize as opt
def forbidden(*a,**k):raise RuntimeError('optimizer forbidden in mutation audit')
opt.linprog=opt.milp=forbidden
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_subfield as M
from exact import VerificationError
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_3664')
c=json.load(open(P/'research/round4/m8/R6_8_3664_certificate.json'));q=c['pseudo'];st=time.monotonic()
# Reuse immutable exact domain for mutations of the certificate only.
# Different tensors, heights, or conductors always recompute the domain.
base=M.data_for(R,q['metadata']['height'],q['metadata']['F']);uncached=M.data_for
M.data_for=lambda T,h,F:base if T==R and h==q['metadata']['height'] and F==q['metadata']['F'] else uncached(T,h,F)
checks=[]
def reject(name,mut,full=False,T=None):
 try:(M.verify_general if full else M.verify)(R if T is None else T,mut)
 except (VerificationError,ValueError,KeyError) as e:checks.append({'mutation':name,'rejected':True,'reason':str(e)});return
 raise RuntimeError('mutation accepted: '+name)
y=copy.deepcopy(q);y['branches'].pop();reject('omit a low frame',y)
y=copy.deepcopy(q);y['metadata']['order_bound']+=1;reject('incorrect conductor completeness bound',y)
y=copy.deepcopy(q);y['branches'][0]['columns'][1][2]+=1;reject('alter low restriction column',y)
y=copy.deepcopy(q);y['branches'][5]['fibonacci_twist_one_failure']=[0,1];reject('false Fibonacci projection witness',y)
y=copy.deepcopy(q);y['branches'][4]['cases'][0]['ray']=[-a for a in y['branches'][4]['cases'][0]['ray']];reject('negate exact Farkas ray',y)
y=copy.deepcopy(c);y['reduction']['all_values'].pop();reject('omit signed sphericalization quotient',y,True)
y=copy.deepcopy(c);y['scope']='pseudo_unitary';reject('change claimed general scope',y,True)
T=copy.deepcopy(R);T[1][1][0]=2;reject('alter input tensor unit coefficient',q,T=T)
out={'passed':True,'optimizer_disabled':True,'domain_cache_key':'exact tensor,height,conductor','checks':checks,'seconds':time.monotonic()-st}
(P/'research/round4/m8/mutation_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
