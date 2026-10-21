"""Canonical exact-only replay of character-labeled atomic STS exclusions."""
import json
import atomic_generation as driver
from exact import require
cg=driver.cg
TARGETS=(('R8_3_3258',4),)
def main():
    for rid,height in TARGETS:
        source=cg.st.load_ring(rid);row=json.loads((cg.st.HERE/'atomic_results'/f'{rid}_h{height}.json').read_text());require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'atomic STS source binding differs');require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','atomic STS result not general');require(row['certificate']['kind']=='frontier_atomic_real_sts_induction_lift','missing atomic STS signed lift');cg.verify(source['tensor'],row['certificate']);print('PASS',rid,'general atomic STS exclusion',flush=True)
if __name__=='__main__':main()
