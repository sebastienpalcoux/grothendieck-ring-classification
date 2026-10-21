"""Reconstruct unchanged source constraints into a new exact analysis cache."""
from pathlib import Path
import sys,json,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_frontier_20261021'
sys.path.insert(0,str(OLD/'commutative_integer'))
sys.path.insert(0,str(OLD/'quadratic_atomic_integer'))
import r982 as old
from unit_pair_constraints import append_unit_pair_constraints
from fp_fusion_bounds import tighten_fusion_bounds

def make(fi):
 ring=old.st.load_ring('R8_3_982');C=old.cg.cone(ring['tensor'],4,'sts_frame');T=old.character_table(ring['tensor'],C.a)
 (HERE/'phase_low_columns.json').write_text(json.dumps({'tensor_sha256':ring['tensor_sha256'],'phase_metadata':C.meta,'columns':[C.column(j) for j in range(len(C.frames))]},separators=(',',':'))+'\n')
 D,profile=old.filtered(C,fi);print('filtered',fi,flush=True)
 S=old.f.build(D,T,frame_index=fi);S=old.append_galois_balance(S,D,T);S=tighten_fusion_bounds(S,D,T)
 S=append_unit_pair_constraints(S,D,T);print('built',fi,len(S.rhs),len(S.columns),flush=True)
 box=old.box.propagate(S);Q=old.equations.compact(old.box.reduced(S,box))
 out={'frame':fi,'tensor_sha256':ring['tensor_sha256'],'columns':Q.columns,'rhs':Q.rhs,'bounds':Q.bounds,'labels':Q.column_labels,'metadata':Q.metadata,'source_lower':box['lower_bounds'],'source_upper':box['upper_bounds']}
 (HERE/f'frame{fi}_system.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 print('cached',fi,len(Q.rhs),len(Q.columns),flush=True)
if __name__=='__main__':make(int(sys.argv[1]))
