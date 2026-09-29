import copy,hashlib,json,itertools,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize
def forbidden(*a,**kw):raise RuntimeError('optimizer forbidden')
scipy.optimize.linprog=scipy.optimize.milp=forbidden
import round3_noncommutative as m
from exact import require,VerificationError
start=time.monotonic()
rows=json.load(open(ROOT/'data/census.json'));byid={r['id']:r for r in rows}
R=byid['R6_6_170']['N'];path=Path(__file__).parent/'R6_6_170_certificate.json'
c=json.load(open(path));m.verify(R,c)
mutations=[]
for name in ('trace','spectrum','sign_table','gauge','induction_branch','scope'):
    bad=copy.deepcopy(c)
    if name=='trace':bad['arithmetic']['hypotheses']['Casimir_trace']+=1
    elif name=='spectrum':bad['arithmetic']['spectra'].pop()
    elif name=='sign_table':bad['reduction']['signed_tables'].pop()
    elif name=='gauge':bad['reduction']['signed_tables'][0]['gauge_original'][1]*=-1
    elif name=='induction_branch':bad['pseudo']['branches'].pop()
    else:bad['scope']='pseudo_unitary_only'
    try:m.verify(R,bad)
    except VerificationError:mutations.append(name)
    else:raise RuntimeError('accepted mutated certificate: '+name)
relabels=[]
for p in ((0,2,1,3,4,5),(0,5,4,3,2,1),(0,3,1,5,2,4)):
    T=[[[R[p[i]][p[j]][p[k]] for k in range(6)] for j in range(6)] for i in range(6)]
    z=m.certificate(T);require(z is not None,'relabeled exclusion missing');m.verify(T,z)
    relabels.append(list(p))
ledger=json.load(open(ROOT/'data/decisions.json'))
positive=[r for r in ledger if 'realized' in r['status']]
for r in positive:
    require(m.certificate(byid[r['id']]['N']) is None,'positive model excluded')
scan=[]
for r in rows:
    if all(r['N'][i][j]==r['N'][j][i] for i,j in itertools.product(range(6),repeat=2)):continue
    z=m.arithmetic(r['N'],allow_even_commutators=True)
    scan.append({'id':r['id'],'hypotheses':z is not None,'arithmetic':z})
extra=[]
for rid in ('R6_7_200','R6_8_491'):
    pp=Path(__file__).parent/(rid+'_certificate.json');cc=json.load(open(pp));rr=byid[rid]['N']
    m.verify(rr,cc)
    bad=copy.deepcopy(cc);bad.pop('commutative_sector')
    try:m.verify(rr,bad)
    except VerificationError:pass
    else:raise RuntimeError('missing commutative sector accepted')
    p=(0,5,4,3,2,1);tt=[[[rr[p[i]][p[j]][p[k]] for k in range(6)] for j in range(6)] for i in range(6)]
    zz=m.certificate(tt);require(zz is not None,'missing relabeled full sector proof');m.verify(tt,zz)
    extra.append({'id':rid,'passed':True,'certificate_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),
                  'full_relabeled_replay':list(p),'missing_sector_rejected':True})
result={'passed':True,'additional_general_certificates':extra,'optimized_python':not __debug__,'optimizer_disabled':True,
    'seconds':time.monotonic()-start,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'mutations_rejected':mutations,'full_relabeled_replays':relabels,'positive_controls':len(positive),
    'census_tensors_screened':len(rows),'noncommutative_source_cases':scan}
out=Path(__file__).parent/('verification_optimized.json' if not __debug__ else 'verification_normal.json')
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='noncommutative_source_cases'},indent=2))
