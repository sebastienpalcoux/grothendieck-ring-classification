"""Dated rank-twelve publication overlay; older decisions remain immutable."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE='evidence/rank12_m1_20261026'

def active(repo=ROOT):return (Path(repo)/EVIDENCE/'ledger.json').is_file()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def publication_matches(relative,expected,repo=ROOT):
 """Only explicit before/after publication replacements may supersede a hash."""
 repo=Path(repo);p=repo/relative
 if not p.is_file():return False
 actual=digest(p)
 if actual==expected:return True
 from frontier_20261027 import publication_matches as frontier_matches
 if frontier_matches(relative,expected,repo):return True
 receipt=repo/'data/rank12_publication_replacements.json'
 if not receipt.is_file():return False
 r=json.loads(receipt.read_text());entry=r['files'].get(relative)
 if not entry or expected not in entry['prior_sha256'] or actual!=entry['after_sha256']:return False
 return all(digest(repo/name)==h for name,h in r['immutable_decisions'].items())

def extend_readme(front,guide,repo=ROOT):
 if not active(repo):return front,guide
 row='| 12 | Through 1 | **Complete through 1** | 632 rings: 480 general exclusions, 152 modeled, none unresolved. 151 models are unitary; R12_1_623 is complex/pseudo-unitary, with unitarity unproved. |'
 def extend(text,prefix):
  lines=text.splitlines();out=[];in_counts=False
  for line in lines:
   if line.startswith('| Multiplicity |'):
    in_counts=True;line+=' Rank 12 |'
   elif in_counts and re.fullmatch(r'\|[\s|:-]+\|',line):line+=' ---: |'
   elif in_counts and re.match(r'\| \d+ \|',line):line+=(' 152 |'if line.startswith('| 1 |')else' — |')
   elif not line.startswith('|'):in_counts=False
   out.append(line)
   if line.startswith('| 11 |')and not in_counts:out.append(row)
  text='\n'.join(out)+'\n'
  note=('**26 October 2026 · rank twelve, multiplicity one.** All 632 supplied rings are decided: '
        '**480 excluded and 152 modeled**. Exactly **151 models are known unitary**; '
        'R12_1_623 has a complex/pseudo-unitary model with unitarity unproved. '
        f'[Manuscript]({prefix}publications/rank12/README.md) · '
        f'[Proofs, ledger and replay]({prefix}{EVIDENCE}/README.md) · '
        f'[All-rank count summary]({prefix}data/classification_summary_all_ranks.csv).\n\n')
  marker='## Classification at a glance'if'## Classification at a glance'in text else'## Grothendieck rings · known realizations at each exact multiplicity'
  return text.replace(marker,note+marker,1)
 return extend(front,''),extend(guide,'../')

def extend_document(name,content,repo=ROOT):
 if not active(repo):return content
 if name=='manuscripts/README.md':
  content=content.replace('Current classification through rank eleven:','Current classification through rank twelve:')
  content+='\n**Rank 12, multiplicity one:** 480 general exclusions and 152 models; 151 unitary, with R12_1_623 complex/pseudo-unitary and unitarity unproved. No rank-twelve case remains unresolved. [Proofs and exact replay](../'+EVIDENCE+'/README.md). The ten open cases at lower ranks are unchanged.\n'
 if name in ('docs/VERIFY.md','docs/PROVENANCE.md','docs/RESEARCH_STATUS.md','docs/PREPUBLICATION_REVIEW.md'):
  content+='\n## Rank twelve, multiplicity one · 26 October 2026\n\nThe new release classifies 632 supplied rings: 480 general exclusions and 152 models. Of these, 151 are unitary; R12_1_623 has a complex/pseudo-unitary model whose unitarity is unproved. The ten earlier open cases are unchanged. [Current manuscript](../publications/rank12/README.md) · [Complete proof archive and accepted replay](../'+EVIDENCE+'/README.md). Full census enumeration was not independently repeated.\n'
 return content

def _pages(repo):
 p=Path(repo)/'data/current_manuscript_page_counts.json'
 for r in json.loads(p.read_text())['documents']:
  if r['path']=='publications/rank12/paper/rank12.pdf':return r['pages']
 raise ValueError('Missing rank-twelve page inventory')
