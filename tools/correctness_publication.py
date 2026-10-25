"""Dated proof/code correction overlay; classifications and old receipts stay fixed."""
from pathlib import Path
import re
EVIDENCE='evidence/correctness_20261025'
DATE='2026-10-25'
BASE_COMMIT='8014c749c17ddd2ad3d1b99a4359d49a8be921c5'
GITHUB='https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/'
MODELS={
 'R8_1_36':('TY_C3_C2.md','The TY(C3) crossed-C2 model is checked by tools/verify_anyonwiki_import.py. This corrects the obsolete verifier path; its tensor and categorical realization are unchanged.'),
 'R6_2_143':('rank6_r143_module_repair.md','The actual HI(C5) Q-system dual is identified from its canonical module. Both possible dualities are included; exact module equations force every fusion coefficient without numerical center data.'),
 'R8_2_820':('rank8-neargroup-exact-repair.md','The actual NG(C5,5) center factor is identified by its known tube blocks, exhaustive associative completions, and exact third indicators with balancing. No numerical recognition of the unknown tube block is used.'),
 'R8_2_869':('rank8-neargroup-exact-repair.md','The second actual NG(C5,5) center factor is distinguished by exact third indicators and balancing after all associative completions and dualities are exhausted. No numerical recognition of the unknown tube block is used.'),
 'R8_3_721':('r721-exact-completion-proof.md','The actual inherited-Q-system dual is identified by a direct exact completion of its induction equations. All four dualities give one based-ring class in a 14-node search; census completeness is not assumed.'),
 'R8_2_868':('HI7_EXACT_CENTER.md','The actual HI(C7) center identification uses Gannon–Schopieray–Yadav, Theorem A(2)/5.1 (arXiv:2609.25185v1), followed by the canonical-algebra argument. Its generator matrix alone is not a full fusion-tensor proof.')}
def active(repo):return (Path(repo)/EVIDENCE/'README.md').is_file()
def update_models(records):
 for record in records:
  if record['id'] not in MODELS:continue
  proof,note=MODELS[record['id']]
  record['construction_proof_file']=EVIDENCE+'/'+proof
  record['construction_notes']=[note,'Exact proof and tensor checks remain subject to independent human verification.']
  record['model_reference']=note+' See the current manuscript and the dated exact proof.'
 return records

def revise_document(name,text,repo):
 text=re.sub(r'<!-- correctness-20261025 -->.*?<!-- /correctness-20261025 -->\n*','',text,flags=re.S)
 text=text.replace('Exact rank and coefficient bounds identify its unique dimension type in the supplied complete rank-eight multiplicity-at-most-three census.','Exact rank and coefficient bounds, followed by a direct exhaustive fusion completion, identify its entire based ring without assuming census completeness.')
 text=text.replace('4,402 general\nexclusions, 93 unitary models and five unresolved rings','4,403 general\nexclusions, 93 unitary models and four unresolved rings')
 text=text.replace('the ledger restored as `output/audited_20261024/ledger.json`','the historical audit ledger; the current ledger is `output/research_20261024/ledger.json`')
 text=text.replace('[Complete proof and replay archive](replay.zip)','[Historical source archive](replay.zip)')
 if name=='docs/VERIFY.md':
  a=text.find('## Complete rank-six route');b=text.find('## Upper-rank and continuation checks',a)
  if a>=0 and b>a:
   text=text[:a]+'''## Current complete rank-six exclusion replay

From the repository root, use a new output directory:

```bash
python3 evidence/correctness_20261025/replay_rank6.py \\
  --output-dir /tmp/rank6-current-complete --jobs 2
```

This checks all 25,362 current exclusion certificates using the complete
mathematical workers. It retains every original raw verdict and retries ordinary failures as full
unchanged workers in fresh Python-ground-types processes. The eleven
multiplicity-nine certificates run in their exact immutable source contexts;
the current tensors and certificates must match byte for byte.
It then re-executes both original post-loop checks and checks that all inputs
and rank-six source bytes stayed fixed. Positive categorical existence and
constructor proofs have their separate audited routes. The source-bound
correction release records the actual outcome, without relabeling a failed
initial invocation as a single successful run.

The earlier frozen orchestrator and its original failures are historical.
The 25 October pre-revision audit had partly log-derived rank-six coverage;
that limitation remains recorded in its original evidence archive. Historical
manifests are not rewritten to accept changed current source files.

'''+text[b:]
  text=text.replace('From `supplements/rank6`, the following check the named components:', 'The standalone commands below belong to the pinned scientific snapshot `8014c749c17ddd2ad3d1b99a4359d49a8be921c5`, from its `supplements/rank6` directory. They retain their original source-hash requirements. In the current checkout, use the complete source-context adapter above. To replay just the eleven immutable completion proofs from the repository root, use `python3 evidence/correctness_20261025/replay_immutable_m9.py --output-dir /tmp/immutable-m9-complete`.')
  text=text.replace('For the current checkout, replay `python3 tools/verify_rank8_exclusion_20261022.py`; add `--historical` to replay earlier rank-eight stages in their preserved contexts.','The stage-specific commands below retain their original source contexts. Use the current correction commands above for the revised proof and code checks.')
 if name=='evidence/rank9_m2_20261024/README.md':
  a=text.find('The current archive authority is');b=text.find('\n\n',a)
  if a>=0:
   text=text[:a]+'''The current archive authority is `phase5/results/ledger.json`. The old archive's root `verify.py` checks phase five; `--baseline` adds phase four, not phases one–three. Use the new all-phase entry point from the repository root:

```bash
python3 evidence/correctness_20261025/replay_rank9.py \\
  --output-dir /tmp/rank9-current-complete --frontier --jobs 2
```

It verifies the unchanged archive before each stage, supplies the two separately bound missing phase-three certificates, replays the accepted baseline and phases two–five, and regenerates the model tensors. R920 uses an explicitly labelled exact pseudo-Boolean fallback, sharing the discovery implementation; no successful independent eight-bit replay is claimed. Stored group/cohomology narrowing records are checked here. Their fresh full regeneration is in the dated audit archive. Separate categorical premises remain explicit.'''+text[b:]
 depth=0 if name=='README.md' else 2 if name.startswith(('supplements/rank','evidence/rank9')) else 1
 prefix='../'*depth
 if name in ('README.md','docs/VERIFY.md','docs/PREPUBLICATION_REVIEW.md','docs/PROJECT_GUIDE.md','manuscripts/README.md','supplements/rank6/README.md','supplements/rank7/README.md','supplements/rank8/README.md','evidence/rank9_m2_20261024/README.md'):
  banner=('<!-- correctness-20261025 -->\n**Correctness revision · 25 October 2026.** The current classification is unchanged. '
          'Three model-identification arguments are repaired, R8_3_721 has a direct exact completion, and implementation/replay defects are corrected. '
          f'[Findings, corrections and exact commands]({prefix}{EVIDENCE}/README.md). '
          'Independent human verification remains pending.\n<!-- /correctness-20261025 -->\n\n')
  at=text.find('\n\n');text=text[:at+2]+banner+text[at+2:]
 return text
