"""Canonical exact-only replay of accepted complete sparse-cone exclusions."""
import json
import column_generation as cg
from exact import require

TARGETS=(('R8_3_903','sts_frame',4),('R8_3_1615','sts_frame',4),('R8_3_1661','sts_frame',4))

def main():
    for rid,variant,height in TARGETS:
        source=cg.st.load_ring(rid)
        row=json.loads((cg.st.HERE/'complete_results'/f'{rid}_{variant}_h{height}.json').read_text())
        require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'complete-cone source binding differs')
        require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','complete-cone result not general')
        require(row['certificate']['kind']==cg.kinds(variant)[2],'missing complete signed lift')
        cg.verify(source['tensor'],row['certificate'])
        print('PASS',rid,'general complete-cone exclusion',flush=True)

if __name__=='__main__':main()
