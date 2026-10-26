from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/rank8_signed'))
import advanced_criteria
r=json.loads((ROOT/'lower_rank8_signed.json').read_text());R=r['source_record']['tensor']
c=json.loads((ROOT/'sources/rank8_signed/R8_1_17.json').read_text())
advanced_criteria.verify(R,c['certificate'])
print('PASS unchanged rank-eight general-complex signed proof')
