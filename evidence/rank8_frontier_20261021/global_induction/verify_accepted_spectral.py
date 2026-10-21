"""Canonical exact-only replay of named, fully lifted partial-S exclusions."""
import json
import column_generation as cg
from exact import require
TARGETS=('R8_3_926',)
def main():
    for rid in TARGETS:
        source=cg.st.load_ring(rid);row=json.loads((cg.st.HERE/'spectral_results'/f'{rid}_h4.json').read_text())
        require(row['id']==rid and row['tensor_sha256']==source['tensor_sha256']==cg.st.digest(source['tensor']),'accepted partial-S tensor binding fails')
        require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','accepted partial-S result is not general')
        require(row['certificate']['kind']=='frontier_spectral_frame_induction_lift','accepted partial-S result lacks its signed lift')
        cg.verify(source['tensor'],row['certificate']);print('PASS',rid,'general complex exclusion',flush=True)
    print('PASS',len(TARGETS),'accepted partial-S exclusions',flush=True)
if __name__=='__main__':main()
