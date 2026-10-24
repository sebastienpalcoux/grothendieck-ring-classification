"""Validate explicitly corrected derived files against preserved release receipts.

The old receipts retain their original expected hashes. Only files registered
by the 24 October audit's before/after receipt can supersede those bindings.
Canonical old categorical ledgers and tensor sources are never exceptions.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def matches(relative,expected):
 path=ROOT/relative;actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual==expected:return True
 latest=ROOT/'evidence/research_20261024/derived_publication_replacements.json'
 if latest.is_file() and relative.startswith('site/dist/data/'):
  d=json.loads(latest.read_text());entry=d['files'].get(relative)
  if entry and expected in entry['prior_sha256'] and actual==entry['after_sha256']:
   return all(hashlib.sha256((ROOT/d[k]).read_bytes()).hexdigest()==d[k+'_sha256'] for k in ('rank8_ledger','rank9_ledger'))
 receipt=ROOT/'evidence/audit_20261024/derived_publication_replacements.json'
 if not receipt.is_file():return False
 data=json.loads(receipt.read_text());entry=data['files'].get(relative)
 if entry is None:return False
 if not relative.startswith('site/dist/data/'):return False
 ledger=ROOT/data['corrected_ledger']
 return (entry['before_sha256']==expected and entry['after_sha256']==actual and
         data['corrected_ledger_sha256']==hashlib.sha256(ledger.read_bytes()).hexdigest())
