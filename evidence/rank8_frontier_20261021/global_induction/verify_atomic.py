"""Exact atomic modular oracle validation and Fib x Vec(V4) control.
Numerical control rediscovery is explicit; default replay is exact-only.
"""
import argparse,json
import atomic_generation as driver
from atomic_real_sts import AtomicRealSTS
from partial_s import RealTable
from exact import require
cg=driver.cg;st=cg.st

def fib_v4():
    R=[[[0]*8 for j in range(8)] for i in range(8)]
    for a in range(2):
        for b in range(2):
            outputs=(0,1) if a==b==1 else (max(a,b),)
            for g in range(4):
                for h in range(4):
                    for c in outputs:R[g+4*a][h+4*b][(g^h)+4*c]=1
    return R

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rediscover',action='store_true');ap.add_argument('--write',action='store_true');args=ap.parse_args();R=fib_v4();C=AtomicRealSTS(R,4);table=RealTable(R,C.a)
    # All twelve actual restriction types from Z(Fib) x Z(Vec(V4)).
    for g in range(4):
        for v in ((int(i==g) for i in range(8)),(int(i==g+4) for i in range(8)),(int(i in (g,g+4)) for i in range(8))):require(table.failure(tuple(v)) is None,'known model central restriction rejected')
    # Independently reconstruct every dimension-compatible symmetric labeling
    # of the complete joint-frame domain, then compare its aggregate defect.
    from frame_cone import FrameCone
    Fcone=FrameCone(R,4);atom={(g,c):j for j,(g,c,z) in enumerate(C.low)};labelgroup={E:g for g,E in enumerate(C.meta['low_character_labels'])};frame_controls=[]
    K=table.K
    for fi,frame in enumerate(Fcone.frames):
        cols=[(1,)+(0,)*7]+[Fcone.low[j][1] for j in frame]
        for assignment in table.assignments(cols):
            inverse={E:j for j,E in enumerate(assignment)};indices=[atom[labelgroup[E],cols[inverse[E]]] for E in labelgroup];total={}
            for index in indices:
                for row,value in C.column(index).items():total[row]=total.get(row,0)+value
            chis=[[sum((K(n)*v for n,v in zip(c,ch)),K.zero) for ch in table.characters] for c in cols]
            defects=[]
            for ri,label in enumerate(C.rows):
                if label[0]=='atomic_S_symmetry':require(total.get(ri,0)==0,'complete labeled frame violates atomic S symmetry')
                if label[0]=='atomic_STS':
                    _,E,F,k=label;v=sum((cc[E]*cc[F] for cc in chis),K.zero)-table.codegrees[F]*chis[inverse[F]][E];co=table.coordinates(v)[k]*C.extra_scales[k]
                    require(co.denominator==1 and int(co)==total.get(ri,0)-C.rhs[ri],'atomic frame STS defect differs including fixed unit');defects.append(int(co))
            frame_controls.append([fi,assignment,st.digest(defects)])
    require(frame_controls,'positive model has no symmetric complete low frame')
    controls=[]
    for seed in (3,11,29):
        y=[((seed*(j+1)*(j+7))%31)-15 for j in range(C.nrows)]
        values=[sum(y[r]*v for r,v in C.column(j).items()) for j in range(C.nvars)];report=C.oracle(y,64)
        require(report['minimum']==min([0]+values) and report['negative_columns']==sum(v<0 for v in values),'atomic oracle differs from direct columns')
        controls.append({'seed':seed,'minimum':report['minimum'],'negative_columns':report['negative_columns'],'column_values_sha256':st.digest(values)})
    dest=st.HERE/'atomic_validation.json';base={'result':'PASS','control':'Fib tensor Vec(V4)','tensor_sha256':st.digest(R),'metadata':C.meta,'oracle_controls':controls,'complete_frame_count':len(Fcone.frames),'labeled_frame_checks':len(frame_controls),'frame_defects_sha256':st.digest(frame_controls)}
    if args.rediscover:
        ray,feasible,active,iterations=cg.solve_case(C,[1]*7,cg.initial_columns(C),1024,300,lambda it:print('control',it[-1]['iteration'],it[-1]['outcome'],flush=True))
        require(feasible is not None and ray is None,'known model relaxation did not produce a feasible certificate');base['feasible']={'indicators':[1]*7,**feasible};base['discovery_iterations']=iterations
        require(args.write,'rediscovery requires explicit --write')
        dest.write_text(json.dumps(base,separators=(',',':'))+'\n')
    else:
        saved=json.loads(dest.read_text())
        if args.write:
            base['feasible']=saved['feasible'];base['discovery_iterations']=saved.get('discovery_iterations',[]);f=base['feasible'];C.check_feasible(f['indices'],f['weights'],f['indicators']);dest.write_text(json.dumps(base,separators=(',',':'))+'\n')
        else:require(all(saved[k]==v for k,v in base.items()),'atomic validation receipt differs');base=saved
    f=base['feasible'];C.check_feasible(f['indices'],f['weights'],f['indicators']);print('PASS atomic oracle and known Fib x Vec(V4) exact feasible control',flush=True)
if __name__=='__main__':main()
