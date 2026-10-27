from common import *
from scalar_characters import chars
from exact import *
import sympy as s
import dimension_order
from spherical_moments import spherical_global_moment,positive_sign_embedding
from induction import global_moment_certificate,pseudo_certificate
import collections,time,signal
def timed_out(*_):raise TimeoutError('discovery allowance')
def char_obstruction(a,f,required=None):
 K,ds,D,pD=a.component(f);required=required or a.cf
 zero=next((i for i,d in enumerate(ds) if not d),None)
 if zero is not None:return {'kind':'zero_dimension','object':zero}
 unequal=next((i for i,d in enumerate(ds) if d!=ds[a.du[i]]),None)
 if unequal is not None:return {'kind':'unequal_dual_dimensions','object':unequal}
 u=K(s.Poly(t,t).rem(f).all_coeffs())
 pD=s.Matrix.hstack(*(vector(D*u**i,f.degree()) for i in range(f.degree()))).charpoly(t).as_poly().sqf_part()
 c=norm_failure(pD,required) or field_failure(f,required)
 if c:return c
 old=a.cf;a.cf=required
 try:return dimension_order.certificate(a,f)
 finally:a.cf=old
def analyse(R,low=False):
 a=chars(R);branches=[];live=[];comm=all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(len(R)))
 for f,m in a.components:
  c=char_obstruction(a,f)
  if c is None and comm:c=spherical_global_moment(a,f)
  b={'factor':pc(f),'obstruction':c};branches.append(b)
  if c is None:live.append((f,b))
 pu=None
 if live and comm:
  pu=global_moment_certificate(R,a)
  if pu is None and low:pu=pseudo_certificate(R,gram_prune=True)
  if pu is not None:
   for f,b in live:
    K,ds,D,pD=a.component(f);g=positive_sign_embedding(R,f,ds)
    if g:b['obstruction']={'kind':'Galois_positive_dimension','gate':g,'pseudo_obstruction':pu}
 closed=all(b['obstruction'] is not None for b in branches)
 return {'spherical_excluded':closed,'branches':branches,'pseudo_obstruction':pu,'scalar_rank':getattr(a,'scalar_rank',len(R))}
def main():
 raw={r['id']:r for r in read()};out=[];t0=time.time();signal.signal(signal.SIGALRM,timed_out)
 for m in load('survivors_current.json'):
  R=raw[m['id']]['tensor'];signal.alarm(30)
  try:report=analyse(R,low=False)
  except TimeoutError:report={'outcome':'timeout'}
  finally:signal.alarm(0)
  out.append({'id':m['id'],'report':report});save('sphere_original.json',out)
  if len(out)%10==0:print(len(out),'spherical exclusions',sum(x['report'].get('spherical_excluded',False) for x in out),'seconds',round(time.time()-t0),flush=True)
 print('FINAL',len(out),'spherical exclusions',sum(x['report'].get('spherical_excluded',False) for x in out),flush=True)
if __name__=='__main__':main()
