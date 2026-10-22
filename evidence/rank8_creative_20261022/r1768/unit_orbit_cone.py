"""Force the distinguished Galois-unit column after the complete fibre split."""
from finite_fibres_cone import *
class UnitOrbitCone(FiniteFibresCone):
 def __init__(self,base):
  super().__init__(base,4);want=(1,0,2,2,2,2,2,2)
  domain=[i for i,(g,v,z)in enumerate(self.low)if z==(Q(73),Q(12))]
  keep=[i for i in domain if self.low[i][1]==want]
  f.require(len(domain)==532 and len(keep)==1,'distinguishedorbitdomain')
  self.allowed.difference_update(set(domain)-set(keep))
  self.meta={**self.meta,'distinguished_galois_unit_column':list(want),'distinguished_galois_unit_column_index':keep[0],'allowed_columns':len(self.allowed),'allowed_domain_sha256':f.st.digest(sorted(self.allowed))}
 def low_scores(self,y):
  for i,v in super().low_scores(y):
   if i in self.allowed:yield i,v
 def initial_columns(self):return super().initial_columns()&self.allowed

def main(verify,seconds,setup=None):
 source,base,old=f.setup(1768)if setup is None else setup;C=UnitOrbitCone(base);ep=[-1,1,1,1,1,1,1]
 path=HERE/'unit_orbit_cone.json'
 if verify:
  x=json.loads(path.read_text());f.require(x['tensor_sha256']==source['tensor_sha256'] and x['id']==source['id'],'source identity');f.require(x['metadata']==f.st.encode(C.meta),'domain');f.require(x['indicators']==ep,'indicators')
  if x['status']=='exact_infeasible':f.require(C.check_farkas(x['certificate']['y'],ep)==x['certificate']['bTy'],'separator')
  else:f.require(x['status']=='exact_feasible','acceptedstatus');C.check_feasible(x['certificate']['indices'],x['certificate']['weights'],ep)
  f.require(x['status']=='exact_feasible','claimed final relaxation survives')
  print('PASS',x['status'],flush=True);return {'status':x['status'],'indices':len(x['certificate']['indices'])}
 x={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'metadata':C.meta,'indicators':ep}
 def save():path.write_text(json.dumps(f.st.encode(x),separators=(',',':'))+'\n')
 def progress(it):x['iterations']=it;save();print('ROUND',it[-1]['outcome'],flush=True)
 cert,feas,active,it=f.cg.solve_case(C,ep,C.initial_columns(),512,seconds,progress)
 if cert:x.update(status='exact_infeasible',certificate=cert)
 elif feas:x.update(status='exact_feasible',certificate=feas)
 else:x['status']='inconclusive'
 save();print(x['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--seconds',type=int,default=180);a=p.parse_args();main(a.verify,a.seconds)
