"""Canonical exact-only replay of complete labeled-frame STS exclusions."""
import json
import column_generation as cg
from exact import require
TARGETS=(('R8_3_985',4),)
def main():
    for rid,height in TARGETS:
        source=cg.st.load_ring(rid);row=json.loads((cg.st.HERE/'sts_results'/f'{rid}_h{height}.json').read_text());require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'STS source binding differs');require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','STS result not general');require(row['certificate']['kind']=='frontier_sts_frame_induction_lift','missing STS signed lift');cg.verify(source['tensor'],row['certificate']);print('PASS',rid,'general labeled-frame STS exclusion',flush=True)
if __name__=='__main__':main()
