"""Six exact old separators + all palindromic parity signs; no solver."""
from pathlib import Path
import sys,json,hashlib,time,runpy
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
R=H/'replay_source'
sys.path.insert(0,str(R/'evidence/rank8_creative_20261022/r1768'))
import finite_fibres_cone as fibres
import verify_arithmetic as arithmetic

def need(c,m):
 if not c:raise RuntimeError(m)
start=time.monotonic()
# The cleaned repository no longer keeps the old whole-band census JSON.
# Replace only that input loader by the exact same SHA-bound source tensor;
# every equation/domain builder below is the unchanged published program.
tensor=runpy.run_path(str(H.parents[1]/'prior/data/current_remaining_cases.py'))['TENSORS']['R8_3_1768']
th=hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest()
need(th=='240509807c67da437c86f2a51efeb831364734feb93ed18a1d2f32087ebc1af0','exact source tensor')
def source_loader(rid):
 need(rid=='R8_3_1768','restricted loader')
 return {'id':rid,'tensor':tensor,'tensor_sha256':th}
fibres.f.st.load_ring=source_loader
setup=fibres.f.setup(1768)
# Complete sign domain implied by conjugation parity, with epsilon(unit)=1.
signs=[]
import itertools
for tail in itertools.product((-1,1),repeat=7):
 es=[1]+list(tail)
 if all(es[y]==es[k] or sum(tensor[x][y][a]*tensor[a][x][k] for a in range(8))%2==0
        for x,y,k in itertools.product(range(8),repeat=3)):
  signs.append(es)
need(signs==[[1,-1,1,1,-1,1,-1,-1],[1,1,1,1,1,1,1,1]],'complete palindromic indicator domain')
ar=arithmetic.run(setup)
need(ar==json.loads((R/'evidence/rank8_creative_20261022/r1768/arithmetic_verification.json').read_text()),'complete finite-domain arithmetic')
out=json.loads((R/'evidence/rank8_creative_20261022/r1768/finite_fibres_cone.json').read_text())
ep=[-1,1,1,-1,1,-1,-1]
checks=[]
for r in out['fibres']:
 C=fibres.FiniteFibresCone(setup[1],r['j'])
 need(fibres.f.st.encode(C.meta)==r['metadata'],'exact cone metadata')
 b=next(x for x in r['branches'] if x['indicators']==ep)
 need(b['status']=='exact_infeasible','old separator exists')
 cert=b['certificate']; y=cert['y']
 ans=C.oracle(y,1)
 need(ans['negative_columns']==0,'every allowed column has nonnegative dot product')
 rhs=sum(a*b for a,b in zip(y,C.rhs_for(ep)))
 need(rhs==cert['bTy'] and rhs<0,'strict negative RHS')
 checks.append({'V':r['j'],'U':16-4*r['j'],'indicators':ep,'allowed_columns':len(C.allowed),'minimum_column_pairing':ans['minimum'],'negative_columns':ans['negative_columns'],'rhs':str(rhs)})
 print('PASS negative pointed sign, V=',r['j'],flush=True)
need([x['V'] for x in checks]==list(range(5)),'five complete branches')
# The other possible sign vector is all-positive. It is rejected already
# by the earlier C2 Fourier cone, without any primitive37 decomposition.
old=json.loads((R/'evidence/rank8_research_20261022/pointed_followup/R8_3_1768.json').read_text())
pr=next(r for r in old['parities'] if r['metadata']['pointed_second_indicator']==1)
PC=fibres.f.PointedCone(setup[1],1)
need(fibres.f.st.encode(PC.meta)==pr['metadata'],'positive cone metadata')
pb=next(b for b in pr['branches'] if b['indicators']==[1]*7)
need(pb['status']=='exact_infeasible','all-positive exact separator')
cert=pb['certificate']; ans=PC.oracle(cert['y'],1)
need(ans['negative_columns']==0,'positive separator column signs')
rhs=sum(a*b for a,b in zip(cert['y'],PC.rhs_for([1]*7)))
need(rhs==cert['bTy'] and rhs<0,'positive strict negative RHS')
positive={'indicators':[1]*7,'allowed_columns':len(PC.allowed),'minimum_column_pairing':ans['minimum'],'negative_columns':ans['negative_columns'],'rhs':str(rhs)}
print('PASS all-positive sign vector',flush=True)
receipt={'id':'R8_3_1768','verification':'PASS','scope':'Complete two-sign palindromic domain; six prior Farkas separators replayed exactly. No optimization or associator search.', 'tensor_sha256':setup[0]['tensor_sha256'],'palindromic_signs':signs,'negative_sign_five_Gram_branches':checks,'positive_sign_branch':positive,'arithmetic_domain_replayed':True,'seconds':round(time.monotonic()-start,3)}
(H/'palindromic_center_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS all six exact separators;',round(time.monotonic()-start,3),'seconds')
