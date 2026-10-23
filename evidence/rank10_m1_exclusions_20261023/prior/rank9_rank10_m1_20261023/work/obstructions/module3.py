from arithmetic import *
import involution_module
import time
if __name__=='__main__':
 sv={r['id']for r in json.load(open(HERE/'survivors.json'))};out=[]
 for r in read():
  if r['id']not in sv or not comm(r['tensor']):continue
  t0=time.time();c=involution_module.certificate(r['tensor'])
  if c:involution_module.verify(r['tensor'],c);print(r['id'],'EXCLUDED',c,flush=True)
  out.append(dict(id=r['id'],tensor_sha256=r['tensor_sha256'],certificate=c,seconds=time.time()-t0))
  (HERE/'module3.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TOTAL',len(out),'EXCLUSIONS',sum(r['certificate']is not None for r in out))
