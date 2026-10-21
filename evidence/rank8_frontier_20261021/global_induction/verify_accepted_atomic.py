"""Canonical exact-only replay of full-field atomic spectral exclusions."""
import json
import atomic_spectrum_generation as driver
from exact import require
cg=driver.cg
TARGETS=(('R8_3_1055',4),('R8_3_3413',4))
def main():
    for rid,height in TARGETS:
        source=cg.st.load_ring(rid);row=json.loads((cg.st.HERE/'atomic_spectrum_results'/f'{rid}_h{height}.json').read_text());require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'atomic source binding differs');require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','atomic result not general');require(row['certificate']['kind']=='frontier_atomic_spectrum_induction_lift','missing atomic signed lift');cg.verify(source['tensor'],row['certificate']);print('PASS',rid,'general full-field atomic spectral exclusion',flush=True)
if __name__=='__main__':main()
