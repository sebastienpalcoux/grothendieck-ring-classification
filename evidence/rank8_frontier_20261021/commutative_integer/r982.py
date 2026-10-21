"""Complete four-frame integer Gram/cubic lattice screen for R8_3_982."""
from pathlib import Path
import argparse,copy,itertools,json,sys,time
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
sys.path.insert(0,str(HERE.parent/'quadratic'))
import column_generation as cg
from partial_s import character_table
from atomic_galois_balance import append_galois_balance
import features as f
from lattice import modular,verify_result,hermite,verify_hermite
import bounds as box
import equations
st=cg.st;require=f.require

def filtered(C,fi):
    D=copy.copy(C);fixed=[(1,)+(0,)*7]+[C.low[j][1]for j in C.frames[fi]]
    H=s.Matrix(C.a['B'])-sum((s.Matrix(v)*s.Matrix(v).T for v in fixed),s.zeros(8))
    rank=H.rank();null=H.nullspace();I=next(I for I in itertools.combinations(range(8),rank)if H.extract(I,I).det())
    inverse=H.extract(I,I).inv();keep=set();norms={}
    for j,(v,z)in enumerate(C.a['high']):
        vv=s.Matrix((0,)+tuple(v))
        if any((w.T*vv)[0]for w in null):continue
        vi=vv.extract(I,[0]);norm=(vi.T*inverse*vi)[0];require(norm>0,'nonpositive restriction norm')
        if norm<=1:keep.add(j);norms[j]=str(norm)
    D.orbits=tuple(orbit for orbit in C.orbits if all(j in keep for j in orbit))
    return D,{'frame_index':fi,'residual_Gram_rank':rank,'high_vectors':len(keep),'high_orbits':len(D.orbits),
              'frame_sha256':st.digest([fixed,C.meta['frame_character_labels'][fi]]),'retained_norms_sha256':st.digest(norms)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frame',type=int,choices=range(4));ap.add_argument('--write',action='store_true');ap.add_argument('--hermite',action='store_true');ap.add_argument('--propose',type=int,default=0);args=ap.parse_args()
    source=st.load_ring('R8_3_982');C=cg.cone(source['tensor'],4,'sts_frame');T=character_table(source['tensor'],C.a)
    require(len(C.frames)==4,'complete low frame count changed')
    for fi in([args.frame]if args.frame is not None else range(4)):
        start=time.monotonic();D,profile=filtered(C,fi);print('filtered',fi,profile,flush=True)
        S=f.build(D,T,frame_index=fi);print('built',fi,S.metadata['rows'],S.metadata['variables'],round(time.monotonic()-start,3),flush=True)
        S=append_galois_balance(S,D,T)
        from fp_fusion_bounds import tighten_fusion_bounds
        S=tighten_fusion_bounds(S,D,T);print('Galois+FP bounds',fi,S.metadata['rows'],round(time.monotonic()-start,3),flush=True)
        path=HERE/f'R8_3_982_frame{fi}.json'
        if args.write:
            tests=[]
            for p in(2,3):
                tests.append(modular(S,p));print('modular',fi,p,tests[-1]['outcome'],tests[-1]['rank'],flush=True)
            out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'kind':'fixed_frame_integer_Gram_S_cubic_Galois_lattice','scope':'pseudo_unitary_necessary_system','profile':profile,'metadata':S.metadata,'tests':tests}
            out['box']=box.propagate(S);print('bounds',fi,out['box']['outcome'],out['box']['fixed_variables'],out['box']['tightenings'],flush=True)
            path.write_text(json.dumps(out,separators=(',',':'))+'\n')
            if args.hermite and out['box']['outcome']=='integer_box_consistent':
                reduced=box.reduced(S,out['box']);compact=equations.compact(reduced);out['compact_metadata']=compact.metadata
                print('compact',fi,len(compact.rhs),len(compact.columns),flush=True)
                out['Hermite']=hermite(compact,progress=lambda done,rank:print('HNF',fi,done,rank,flush=True));path.write_text(json.dumps(out,separators=(',',':'))+'\n')
                if args.propose and out['Hermite']['outcome']=='integer_lattice_member':
                    sys.path.insert(0,str(HERE.parent/'quadratic_atomic_integer'))
                    from proposal import propose
                    out['integer_proposal']=propose(compact,args.propose,f.check_integer)
                    if out['integer_proposal']['conclusion']=='exact_integer_feasible_relaxation':
                        original=box.lift(S,out['box'],out['integer_proposal']['integer_values']);f.check_integer(S,original)
                        out['original_integer_witness']=original
                    path.write_text(json.dumps(out,separators=(',',':'))+'\n')
                    print('proposal',fi,out['integer_proposal']['conclusion'],flush=True)
        else:
            out=json.loads(path.read_text());require(out['tensor_sha256']==source['tensor_sha256']and out['profile']==profile and out['metadata']==S.metadata,'source/domain receipt changed')
            for test in out['tests']:verify_result(S,test)
            box.verify(S,out['box'])
            if 'Hermite'in out:
                compact=equations.compact(box.reduced(S,out['box']));require(compact.metadata==out['compact_metadata'],'compressed system differs');verify_hermite(compact,out['Hermite'])
            if 'original_integer_witness'in out:f.check_integer(S,out['original_integer_witness'])
        print('PASS',source['id'],'frame',fi,[x['outcome']for x in out['tests']],round(time.monotonic()-start,3),flush=True)
if __name__=='__main__':main()
