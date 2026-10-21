"""Exact fixed-low-frame integer Gram domain profiles; no exclusion claim."""
from pathlib import Path
import argparse,itertools,json,sys,time
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import column_generation as cg
from exact import require
st=cg.st

def build(rid):
    source=st.load_ring(rid);R=source['tensor'];C=cg.cone(R,4,'sts_frame');du=C.meta['source_duality']if 'source_duality'in C.meta else[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    B=s.Matrix(C.a['B']);out=[]
    for fi,frame in enumerate(C.frames):
        cols=[(1,)+(0,)*7]+[C.low[j][1]for j in frame]
        L=s.Matrix.hstack(*(s.Matrix(v)for v in cols));H=B-L*L.T;rank=H.rank();null=H.nullspace()
        indices=next((I for I in itertools.combinations(range(8),rank)if H.extract(I,I).det()!=0),())
        require(len(indices)==rank,'no nonsingular principal rank basis')
        inverse=H.extract(indices,indices).inv();high=[]
        for j,(v,z)in enumerate(C.a['high']):
            vv=s.Matrix((0,)+tuple(v))
            if any((w.T*vv)[0]for w in null):continue
            vi=vv.extract(indices,[0]);norm=(vi.T*inverse*vi)[0]
            require(norm>0,'nonpositive nonzero vector norm')
            if norm<=1:high.append({'index':j,'vector':list(v),'dimension':list(map(str,z)),'gram_norm':str(norm),'multiplicity_bound':int(s.floor(1/norm))})
        retained={h['index']for h in high};orbits=[]
        for orbit in C.orbits:
            if not all(j in retained for j in orbit):continue
            G=sum((s.Matrix((0,)+tuple(C.a['high'][j][0]))*s.Matrix((0,)+tuple(C.a['high'][j][0])).T for j in orbit),s.zeros(8))
            bound=min(int(H[i,i]//G[i,i])for i in range(8)if G[i,i])
            if bound:orbits.append({'indices':list(orbit),'diagonal_bound':bound,'gram':list(map(list,G.tolist()))})
        out.append({'frame_index':fi,'character_labels':C.meta['frame_character_labels'][fi],
                    'low_columns':list(map(list,cols)),'residual_gram':H.tolist(),'rank':rank,
                    'range_basis':list(indices),'duality_invariant':all(H[i,j]==H[du[i],du[j]]for i in range(8)for j in range(8)),
                    'low_duality_closed':sorted(tuple(c[du[i]]for i in range(8))for c in cols)==sorted(cols),
                    'high_vectors':high,'duality_orbits':orbits})
    return {'id':rid,'tensor_sha256':source['tensor_sha256'],'kind':'exact_fixed_frame_integer_gram_domain_profile',
            'scope':'finite necessary-domain profile; no categorifiability conclusion',
            'complete_labeled_low_frames':len(C.frames),'global_filtered_high_count':len(C.a['high']),
            'frame_domain_sha256':st.digest(C.frames),'records':out}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',default='R8_3_982');ap.add_argument('--write',action='store_true');args=ap.parse_args();start=time.monotonic();out=build(args.ring);path=HERE/f'{args.ring}_profile.json'
    out=json.loads(json.dumps(out,default=int))
    if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(path.read_text())==out,'fixed-frame profile differs')
    print('PASS',args.ring,[(r['frame_index'],r['rank'],len(r['high_vectors']),len(r['duality_orbits']))for r in out['records']],round(time.monotonic()-start,3),flush=True)

if __name__=='__main__':main()
