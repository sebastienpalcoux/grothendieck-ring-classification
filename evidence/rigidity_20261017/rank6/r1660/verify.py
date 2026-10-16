#!/usr/bin/env python3
"""Replay source-bound R6_8_1660 necessary phase-mass conditions."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
from all_indicators import default_repo,need
HERE=Path(__file__).resolve().parent
PYTHON=[sys.executable]+(['-O']if not __debug__ else [])

def run(name,args):
 p=subprocess.run(PYTHON+[str(HERE/name),*map(str,args)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 need(p.returncode==0,name+' failed:\n'+p.stdout[-6000:])
 return p.stdout

def equal(a,b,label):need(json.loads(Path(a).read_text())==json.loads(Path(b).read_text()),label)

def negative_controls(repo):
 # Feed a malformed mass through the actual independent derivation checker.
 b=json.loads((HERE/'phase_masses.json').read_text())
 b['cases'][0]['masses'][0]['masses_K'][0][0]=str(int(b['cases'][0]['masses'][0]['masses_K'][0][0])+1)
 with tempfile.TemporaryDirectory(prefix='r1660-mass-negative-') as td:
  shadow=Path(td)
  (shadow/'all_indicators.json').symlink_to(HERE/'all_indicators.json')
  (shadow/'phase_masses.json').write_text(json.dumps(b))
  p=subprocess.run(PYTHON+[str(HERE/'independent_audit.py'),'--input-dir',str(shadow)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  need(p.returncode!=0 and 'ValueError: (0, 0,' in p.stdout,'phase-mass negative control was accepted')
 # Use a tiny shadow source tree: altered tensor input must fail its source hash
 # before any large character calculation starts.
 inputs=json.loads((HERE/'all_indicators.json').read_text())['source_files_sha256']
 with tempfile.TemporaryDirectory(prefix='r1660-negative-') as td:
  shadow=Path(td)
  for i,name in enumerate(inputs):
   dst=shadow/name;dst.parent.mkdir(parents=True,exist_ok=True)
   if i==0:dst.write_bytes((repo/name).read_bytes()+b' ')
   else:dst.symlink_to((repo/name).resolve())
  p=subprocess.run(PYTHON+[str(HERE/'all_indicators.py'),'--repo',str(shadow)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  need(p.returncode!=0 and 'source hash:' in p.stdout,'source-hash negative control was accepted')
 return ['altered_phase_mass_rejected','altered_source_tensor_file_rejected']

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--skip-independent',action='store_true');ap.add_argument('--skip-profile-grams',action='store_true');args=ap.parse_args()
 repo=(args.repo or default_repo()).resolve()
 manifest=json.loads((HERE/'manifest.json').read_text())
 for name,item in manifest['files'].items():
  raw=(HERE/name).read_bytes();need(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'package identity: '+name)
 for name,item in manifest.get('external_files',{}).items():
  raw=(repo/name).read_bytes();need(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'external source identity: '+name)
 with tempfile.TemporaryDirectory(prefix='r1660-phase-replay-') as td:
  tmp=Path(td)
  run('all_indicators.py',['--repo',repo,'--output',tmp/'all_indicators.json'])
  equal(tmp/'all_indicators.json',HERE/'all_indicators.json','all-order indicator values')
  run('phase_masses.py',['--input',tmp/'all_indicators.json','--output',tmp/'phase_masses.json'])
  equal(tmp/'phase_masses.json',HERE/'phase_masses.json','all phase masses')
  audit=None
  if not args.skip_independent:
   run('independent_audit.py',['--input-dir',tmp,'--output',tmp/'independent.json'])
   audit=json.loads((tmp/'independent.json').read_text());need(audit['status']=='PASS','independent Fourier audit')
  gram=None
  if not args.skip_profile_grams:
   run('phase_gram_audit.py',['--repo',repo,'--output',tmp/'gram.json'])
   gram=json.loads((tmp/'gram.json').read_text());need(gram['status']=='PASS'and gram['total_survivors']==640,'independent phase Gram audit')
  negatives=negative_controls(repo)
  out={'status':'PASS','ring':'R6_8_1660','scope':'All-order indicator, Fourier-mass and finite restriction-profile necessary conditions only. Categorification remains unresolved.','all_indicator_orders':48,'phase_masses_per_conjugate':288,'conjugate_choices':2,'independent_fourier_audit':audit,'phase_gram_audit':gram,'negative_controls':negatives,'optimized_python':not __debug__}
  if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
  print(json.dumps({k:v for k,v in out.items()if k not in ('independent_fourier_audit','phase_gram_audit')},indent=2))
if __name__=='__main__':main()
