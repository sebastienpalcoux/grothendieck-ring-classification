from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
def read(name):return json.loads((P/name).read_text())
a,b=read('certificate.json'),read('B_certificate.json')
if a['rotation_blocks']!=52*6*23 or a['degree_one_checks']!=52*6:
 raise ValueError('Original-category coverage mismatch')
if b['blocks']!=26**3 or b['degree_one_checks']!=26**3:
 raise ValueError('Modular-factor coverage mismatch')
paths=['check.py','check_B.py','certificate.json','B_certificate.json',
       '../r155_modular/reconstruction.json']
out={
 'ring':'R6_4_155','profile':296,
 'scope':'necessary finite generalized-rotation checks, not categorification',
 'original_category':{'central_targets':52,'base_simples':6,'orders':list(range(2,25)),
   'rotation_blocks':a['rotation_blocks'],'degree_one_checks':a['degree_one_checks'],
   'passed':a['all_passed'],'failures':len(a['failed'])},
 'modular_factor_B':{'central_targets':26**2,'base_simples':26,'orders':[2],
   'rotation_blocks':b['blocks'],'degree_one_checks':b['degree_one_checks'],
   'passed':b['passed'],'failures':len(b['failed'])},
 'arithmetic':'exact rational cyclotomic fields; integral nonnegative Fourier multiplicities',
 'all_tensor_orders_certified':False,
 'source_theorem':'Ng–Schauenburg arXiv:0806.2493, Corollary 5.6, Lemmas 2.5–2.7, Proposition 2.8',
 'sha256':{p:hashlib.sha256((P/p).read_bytes()).hexdigest()for p in paths}}
(P/'summary_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
