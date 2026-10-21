"""Canonical exact-only replay of named, fully lifted frame exclusions."""
import json
import column_generation as cg
from exact import require

TARGETS=(('R8_3_925',4),('R8_3_1739',6))

def main():
    for rid,height in TARGETS:
        folder='frame_results';kind='frontier_frame_induction_lift'
        source=cg.st.load_ring(rid);row=json.loads((cg.st.HERE/folder/f'{rid}_h{height}.json').read_text())
        require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'accepted frame tensor binding fails')
        require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','accepted frame result is not general')
        require(row['certificate']['kind']==kind,'accepted frame result lacks its signed lift')
        cg.verify(source['tensor'],row['certificate'])
        print('PASS',rid,'general complex exclusion',flush=True)
    print('PASS',len(TARGETS),'accepted frame exclusions',flush=True)
if __name__=='__main__':main()
