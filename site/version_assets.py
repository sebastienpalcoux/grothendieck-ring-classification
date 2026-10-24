#!/usr/bin/env python3
"""Bind local JS/CSS URLs to their current bytes on every static page."""
from pathlib import Path
import hashlib,re
DIST=Path(__file__).resolve().parent/'dist'
def version_assets():
 for page in DIST.glob('*.html'):
  text=page.read_text()
  def replace(match):
   name=match[2];target=DIST/name
   if not target.is_file():return match[0]
   digest=hashlib.sha256(target.read_bytes()).hexdigest()[:12]
   return match[1]+name+'?v='+digest+match[3]
  text=re.sub(r'(\b(?:src|href)="\./)([^"?#]+\.(?:js|css))(?:\?v=[^"]*)?(")',replace,text)
  if text!=page.read_text():page.write_text(text)
if __name__=='__main__':version_assets()
