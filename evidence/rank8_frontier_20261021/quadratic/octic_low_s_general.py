"""Minimal general signed lift of the complete R901 octic low-S obstruction."""
from pathlib import Path
import argparse,json
import octic_low_s_symmetry as preflight
from rank_two_and_models import need
st=preflight.st
HERE=Path(__file__).resolve().parent
KIND='frontier_octic_no_symmetric_low_frame'


def witness(R):
    result=preflight.run();need(st.digest(R)==result['tensor_sha256'],'wrong source tensor')
    need(result['symmetric_frames']==0 and result['total_symmetric_labelings']==0,'symmetric frame survives')
    return {'kind':KIND,'witness':result}


def install():
    st.old.install()
    import oriented_extension as oe
    if getattr(oe,'_frontier_octic_low_S_installed',False):return
    original=oe.pseudo_check
    def check(R,c):
        if c['kind']==KIND:need(c==witness(R),'octic low-S witness differs')
        else:original(R,c)
    oe.pseudo_check=check;oe._frontier_octic_low_S_installed=True


def verify(source,row):
    need(row['id']==source['id']and row['tensor_sha256']==source['tensor_sha256']==st.digest(source['tensor']),
         'source binding mismatch')
    need(row['status']=='excluded'and row['scope']=='general_complex_fusion_category','incomplete general result')
    need(row['certificate']['kind']==KIND+'_lift','wrong general proof kind')
    install();import advanced_criteria
    advanced_criteria.verify(source['tensor'],row['certificate']['general'])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    source=st.load_ring('R8_3_901');path=HERE/'octic_low_s_general_results.json'
    if args.write:
        install();import character_induction
        pseudo=witness(source['tensor']);general=character_induction.lift_general(source['tensor'],pseudo,1200)
        need(general is not None,'complete general signed lift unavailable')
        result={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'status':'excluded',
                'scope':'general_complex_fusion_category','method':'complete_raw_low_S_symmetry_over_octic_character_field',
                'certificate':{'kind':KIND+'_lift','general':general}}
        verify(source,result);path.write_text(json.dumps(result,indent=2)+'\n')
    else:verify(source,json.loads(path.read_text()))
    print('PASS: R901 complete raw low-S obstruction and general signed lift',flush=True)
if __name__=='__main__':main()
