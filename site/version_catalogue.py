#!/usr/bin/env python3
"""Hash-version the shared catalogue's complete, mutually bound data snapshot."""
from pathlib import Path
import argparse,hashlib,re
from build_ring_properties import SOURCES
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'site/dist'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(check=False):
 names=(*SOURCES,'ring_property_flags.json')
 fingerprint=hashlib.sha256('\n'.join(name+':'+sha(D/'data'/name)for name in names).encode()).hexdigest()[:20]
 p=D/'catalogue.js';source=p.read_text()
 result=re.sub(r'const dataVersion = "[^"]+";',f'const dataVersion = "{fingerprint}";',source)
 if result==source and f'const dataVersion = "{fingerprint}";'not in source:raise ValueError('Catalogue version declaration is missing')
 if check:
  if result!=source:raise ValueError('Refresh catalogue data version')
 else:p.write_text(result)
 asset=sha(p)[:12]
 for page in D.glob('*.html'):
  source=page.read_text()
  result=re.sub(r'(src="\./catalogue\.js)(?:\?v=[^"]*)?(")',lambda m:m[1]+'?v='+asset+m[2],source)
  if check:
   if result!=source:raise ValueError('Stale catalogue asset: '+page.name)
  elif source!=result:page.write_text(result)
 print('Catalogue data and asset versions match all eight source payloads:',fingerprint)
if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--check',action='store_true');main(a.parse_args().check)
