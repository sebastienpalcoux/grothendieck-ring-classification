import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'software'))
from rings import casimir
src=(P/'research/round2_external/sources/R3582_General_Exclusion/verify.py').read_text()
start=src.index('# Twice the four')
end=src.index('\ndef verify_pseudo_unitary')
src=src[start:end]
src=src.replace('6+x','7+x').replace('(1,6,6,6,6,6)','(1,7,7,7,7,7)')
src=src.replace('[14,14,15,16,16]','[33,33,35,37,37]')
src=src.replace('226','1229').replace('12290','6145').replace('150','175')
# Previous generic replacement transforms2260->12290, now6145.
base=(P/'research/round2_external/sources/R3582_General_Exclusion/verify.py').read_text()
ns={};exec(base[:base.index('\ndef verify_ring')],ns);exec(src,ns)
R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']=='R6_8_6520')
G=casimir(R);report={};t=time.monotonic();branches=ns['low_branches'](G,report)
for i,b in enumerate(branches):
 h,c=ns['high_columns'](b);b['high_columns']=h;b['high_counts']=c
 print(i,c,h,flush=True)
report['seconds']=time.monotonic()-t
(P/'research/round2_higher/R6_8_6520_low_high.json').write_text(json.dumps(report,indent=2))
