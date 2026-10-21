"""Complete raw low-frame S-symmetry preflight for R901 in its octic field.

No partial-S integrality or high-column filter is applied. Default is a
source-bound read-only replay, --write saves the complete finite result.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent;GI=HERE.parent/'global_induction'
sys.path.insert(0,str(GI))
import low_s_symmetry as low
from octic_complex_character_table import OcticTable
from rank_two_and_models import need
st=low.st


def run():
    source=st.load_ring('R8_3_901');R=source['tensor'];a=low.data(R);T=OcticTable(R,a)
    import low_frames_rank8 as native
    cpp=st.BASE/'performance/low_frames_rank8.cpp'
    with tempfile.TemporaryDirectory(prefix='octic-low-frames-') as tmp:
        exe=Path(tmp)/'low_frames'
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        native.executable=lambda:exe
        frames=native.low_matrices(a['columns'],a['B'],gram_prune=True)
    survivors=[]
    for i,frame in enumerate(frames):
        assignments=T.assignments(frame)
        if assignments:survivors.append({'frame_index':i,'columns':frame,'character_assignments':assignments})
    return {'kind':'complete_octic_raw_low_S_symmetry_preflight','id':source['id'],
            'tensor_sha256':source['tensor_sha256'],'low_column_counts':list(map(len,a['columns'])),
            'columns_sha256':st.digest(a['columns']),'complete_raw_frames':len(frames),'frames_sha256':st.digest(frames),
            'full_character_field':T.metadata,'symmetric_frames':len(survivors),
            'total_symmetric_labelings':sum(len(r['character_assignments'])for r in survivors),'survivors':survivors,
            'status':'pseudo_unitary_low_S_obstruction'if not survivors else'exact_symmetric_low_frames_survive',
            'scope':'necessary raw distinguished-low-frame condition; no high data, no integrality filter, no model claim',
            'sources':{str(p.relative_to(HERE.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in[cpp,Path(native.__file__),GI/'low_s_symmetry.py',HERE/'octic_complex_character_table.py']}}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=run();result=json.loads(json.dumps(result,default=int));path=HERE/'octic_low_s_symmetry_results.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(path.read_text())==result,'raw octic low-frame receipt differs')
    print('PASS:',result['complete_raw_frames'],'raw frames,',result['symmetric_frames'],'symmetric frames,',
          result['total_symmetric_labelings'],'symmetric labelings;',result['status'],flush=True)
