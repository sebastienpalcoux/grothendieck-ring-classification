import contextlib,hashlib,json,signal,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_subfield as M
from exact import VerificationError
C={r['id']:r for r in json.load(open(P/'data/census.json'))};models=json.load(open(P/'data/model_catalog.json'));front=json.load(open(P/'verification/round4/campaign_manifest.json'))['tensors']
def stop(*a):raise TimeoutError('per-input 110 second budget')
signal.signal(signal.SIGALRM,stop);rows=[]
for typ,items in [('frontier',front),('positive_model',models)]:
 for rec in items:
  rid=rec['id'];R=C[rid]['N'];st=time.monotonic();o={'id':rid,'input_kind':typ,'tensor_sha256':M.ambient.__dict__.get('fingerprint',lambda x:hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest())(R)}
  labels=[a for a in range(1,len(R)) if R[a][a]==[int(k==0)+int(k==a) for k in range(len(R))]]
  if not labels:o.update(outcome='ineligible',reason='no Fibonacci based subcategory')
  elif rid=='R6_8_3664':o.update(outcome='general_exclusion',fibonacci_labels=labels,certificate='R6_8_3664_certificate.json')
  else:
   signal.alarm(110)
   try:
    if any(R[i][j]!=R[j][i] for i in range(len(R)) for j in range(len(R))):raise M.Ineligible('commutative input required')
    ch=M.Characters(R);p=ch.fp()[4];degree=p.degree()
    if degree>4:raise M.Ineligible('character field degree outside implementation')
    pp=sorted(map(int,M.s.factorint(abs(int(p.TC())))));ff=None
    for F in (5,8,12,15,16,20,24,40,60,120):
     if any(int(x) not in pp for x in M.s.factorint(F)):continue
     iso=M.field_isomorphism(M.s.AlgebraicNumber(M.s.CRootOf(p.as_expr(),degree-1)),M.s.AlgebraicNumber(2*M.s.cos(2*M.s.pi/F)))
     if iso is not None:ff=F;break
    if ff is None:raise M.Ineligible('no supported conductor')
    d=M.data_for(R,3,ff)
    with open(P/f'research/round4/m8/control_{rid}.log','w') as log,contextlib.redirect_stdout(log):
     q=M.run(R,3,ff,prepared=d)
    out=P/f'research/round4/m8/control_{rid}.json';out.write_text(json.dumps(q,separators=(',',':'))+'\n')
    o.update(outcome=q['outcome'],metadata=q['metadata'],fibonacci_labels=labels)
    if q['outcome']=='pseudo_unitary_excluded':raise RuntimeError('known PU realization falsely excluded')
   except M.Ineligible as e:o.update(outcome='ineligible',reason=str(e),fibonacci_labels=labels)
   except TimeoutError as e:o.update(outcome='budget_incomplete',reason=str(e),fibonacci_labels=labels)
   finally:signal.alarm(0)
  o['seconds']=time.monotonic()-st;rows.append(o);print(rid,o['outcome'],o['seconds'],flush=True)
  (P/'research/round4/m8/controls.json').write_text(json.dumps({'criterion':'Fibonacci subcategory twist support with biquadratic full-character projected traces','rows':rows},indent=2)+'\n')
