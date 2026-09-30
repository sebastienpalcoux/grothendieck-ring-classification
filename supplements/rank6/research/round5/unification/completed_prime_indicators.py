"""Compare completed-center indicators with independently forced prime targets."""
import argparse,ast,hashlib,json,math,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
from exact import require
from round5_modular_checks import centers
from round5_629 import source_data
import scipy.optimize

def forbidden(*_,**__):raise RuntimeError('optimizer disabled during exact indicator comparison')
scipy.optimize.linprog=scipy.optimize.milp=forbidden


def values(data,W,ds,ee):
    C=data['C'];F=data['F'];out=[]
    for n in range(F):
        if math.gcd(n,F)!=1:continue
        row=[]
        for i in range(len(W[0])):
            x=sum((d*C(w[i])*C.unit**((n*e)%F) for w,d,e in zip(W,ds,ee)),C.zero)/data['DD'];co=x.to_list()
            require(len(co)<=1 and (not co or co[0].denominator==1),'noninteger coprime indicator');row.append(int(co[0]) if co else 0)
        out.append(dict(residue=n,values=row))
    return out


def reconstruct():
    target_path=ROOT/'research/round5/unification/prime_indicator_congruences.json';targets=json.loads(target_path.read_text());out=[];sources=[ROOT/'data/census.json',target_path,ROOT/'data/unresolved_tensors.json',ROOT/'research/round4/m4_629/filtered_profiles.json'];census=json.loads(sources[0].read_text())
    for rid in ['R6_4_22','R6_4_91','R6_4_629']:
        variants=[]
        if rid!='R6_4_629':
            R=next(x['N'] for x in census if x['id']==rid);p=ROOT/f'research/round5/quartic_pair/{rid}_center_reconstruction.json';sources.append(p);cert=json.loads(p.read_text())['certificate']
            for data,label,W,ds,S,ee in centers(rid,cert,R):variants.append(dict(label=label,indicators=values(data,W,ds,ee)))
        else:
            R,data,cols,lab,src=source_data();require(R==next(x['N'] for x in census if x['id']==rid),'R629 tensor source mismatch');C=data['C'];p=ROOT/'research/round5/m4_629/decoded_twists.json';sources.append(p)
            for case in json.loads(p.read_text()):
                if case['rank']!=35:continue
                W=list(cols);ee=[0]*len(cols)
                for o in case['orbits']:W.extend([(0,)+tuple(o['column'])]*o['copies']);ee.extend([15//o['root_order']*o['root_power']%15]*o['copies'])
                ds=[sum((C(n)*d for n,d in zip(v,data['dims'])),C.zero) for v in W];variants.append(dict(label=dict(solution=case['solution']),indicators=values(data,W,ds,ee)))
        target=next(x for x in targets['cases'] if x['id']==rid);wanted=[dict(residue=x['residue'],values=x['values']) for x in target['targets']]
        require(all(v['indicators']==wanted for v in variants),'prime congruence target mismatch');require(len(variants)==2,'incomplete conjugate modular variants');out.append(dict(id=rid,conductor=data['F'],variants=variants,all_prime_targets_match=True))
    return dict(passed=True,optimizer_used=False,categorification_claimed=False,formula='nu_n(X_i)=(1/D)sum_Z d_Z W_Zi theta_Z^n',cases=out,inputs_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})


def source_hashes():
    todo=[Path(__file__).resolve()];seen=set()
    while todo:
        p=todo.pop()
        if p in seen:continue
        seen.add(p)
        for n in ast.walk(ast.parse(p.read_text())):
            names=[n.module] if isinstance(n,ast.ImportFrom) else [a.name for a in n.names] if isinstance(n,ast.Import) else []
            for name in names:
                if not name:continue
                for d in [p.parent,ROOT/'software']:
                    f=d/(name.split('.')[0]+'.py')
                    if f.exists():todo.append(f);break
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(seen)}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));ap.add_argument('--verify',action='store_true');a=ap.parse_args();start=time.monotonic();cert=reconstruct()
    if a.verify:require(cert==json.loads(a.output.read_text()),'completed indicator comparison record differs')
    else:a.output.write_text(json.dumps(cert,indent=2)+'\n')
    receipt=dict(passed=True,optimizer_used=False,python_optimized=not __debug__,completed_rings=3,modular_variants=6,coprime_indicator_vectors=48,seconds=time.monotonic()-start,source_sha256={**source_hashes(),**cert['inputs_sha256'],str(a.output.resolve().relative_to(ROOT)):hashlib.sha256(a.output.read_bytes()).hexdigest()})
    if a.verify:a.output.with_name(a.output.stem+'_replay_O.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_sha256'}),flush=True)
