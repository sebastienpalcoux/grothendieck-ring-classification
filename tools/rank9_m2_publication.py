"""Current rank-nine M2 presentation derived from the accepted ledger."""
from pathlib import Path
import json,re
from current_frontier import count as open_count
ROOT=Path(__file__).resolve().parents[1];REL='evidence/rank9_m2_20261024';ATLAS='https://sebastienpalcoux.github.io/grothendieck-ring-classification/'
def active():return(ROOT/REL/'summary.json').is_file()
def counts():return json.loads((ROOT/REL/'summary.json').read_text())
def banner():
 c=counts()
 return(f'**Current results · 24 October 2026.** Rank nine at exact multiplicity two has **{c["excluded"]:,} general exclusions, {c["modelled"]} unitary models and {c["unresolved"]} unresolved rings** among 2,083 inputs. '
        f'The complete rank-nine census through multiplicity two contains 2,225 rings. The project now has **{open_count()} unresolved rings** across ranks six, eight, nine and ten. '
        '[Rank-nine M2 manuscript](../publications/rank9-m2/paper/rank9-m2.pdf) · [Current proofs and exact replay](../evidence/rank9_m2_20261024/README.md) · [All current manuscripts](../manuscripts/README.md) · [All open cases]('+ATLAS+'unresolved.html).')
def front(text):
 c=counts();row=f'| 9 | Through 2 | **Complete through 1**; multiplicity 2 partial | Through 2: {c["excluded"]+102:,} excluded, {c["modelled"]+40} realized, [{c["unresolved"]} unresolved]({ATLAS}unresolved.html?rank=9&m=2). |'
 text=re.sub(r'^\| 9 \|(?: Multiplicity 1| Through 2) \|.*$',lambda _:row,text,flags=re.M)
 text=re.sub(r'\*\*\d+ open cases\.\*\*',f'**{open_count()} open cases.**',text,count=1)
 lines=text.splitlines()
 for i,line in enumerate(lines):
  if re.match(r'^\| 2 \| 0 \| 1 \|',line):
   cells=[x.strip()for x in line.strip('|').split('|')]
   if len(cells)==11:cells[8]='≥'+str(c['modelled']);lines[i]='| '+' | '.join(cells)+' |'
 text='\n'.join(lines)+'\n'
 if '[Rank-nine M2 ledger]' not in text:text=text.replace('[Rank-11 ledger]',f'[Rank-nine M2 ledger]({REL}/ledger.csv) · [Rank-11 ledger]')
 if '[Current open tensors]' not in text:text=text.replace('[Earlier construction-candidates report · PDF](docs/New_category_candidates_and_open_cases.pdf)', '[Current open tensors](data/current_remaining_cases.py) · [Earlier construction-candidates report · PDF](docs/New_category_candidates_and_open_cases.pdf)')
 if '[Rank-nine M2 replay]' not in text:
  latest='[Rank-nine M2 replay](evidence/rank9_m2_20261024/README.md) · '
  if '[Rank-11 replay]' in text:text=text.replace('[Rank-11 replay]',latest+'[Rank-11 replay]')
  else:text=text.replace('[Replay instructions](docs/VERIFY.md)',latest+'[Rank-11 replay](evidence/rank11_m1_20261023/README.md) · [Earlier replay instructions](docs/VERIFY.md)')
 return text

def index(text):
 text=text.replace('seven unresolved rings, including R10_1_189',f'{open_count()} unresolved rings across ranks six, eight, nine and ten')
 text=text.replace('**Ranks 9–11:** multiplicity one only. Rank 9 has 102 exclusions and 40 unitary models; rank 10 has 136 exclusions, 57 unitary models and 1 unresolved; rank 11 has 155 exclusions and 27 unitary models.', '**Rank 9:** through multiplicity two, 2,135 general exclusions, 72 unitary models and 18 unresolved. Exact multiplicity two contributes 2,033 exclusions and 32 models.\n\n**Ranks 10–11:** multiplicity one. Rank 10 has 136 exclusions, 57 unitary models and 1 unresolved; rank 11 has 155 exclusions and 27 unitary models.')
 return text
