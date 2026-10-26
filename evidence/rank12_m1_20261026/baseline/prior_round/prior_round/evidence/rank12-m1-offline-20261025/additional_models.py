"""Established graded pullbacks and coherent crossed products; full-table matches."""
from pathlib import Path
import collections,itertools,json,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/work/models'))
from match_models import ty
from extra_models import crossed
from zest_models import gradings,zest
sys.path.insert(0,str(ROOT/'sources/work/rank11/known_models'))
from standard import cyclic_equivariant
sys.path.insert(0,str(ROOT/'sources/work/rank11'))
import common

def candidates():
    I=ty((2,))
    for r in json.loads((ROOT/'lower_rank8_models.json').read_text()):
        B=r['tensor']
        for degree in gradings(B):
            if degree.count(0)!=4:continue
            labs=[(a,b)for a in range(3)for b in range(8)if int(a==2)==degree[b]]
            T=[[[I[a][c][e]*B[b][d][f]for e,f in labs]for c,d in labs]for a,b in labs]
            h=labs.index((1,0))
            yield 'Ising graded pullback '+r['id'],T,'graded_pullback',dict(left_name='Ising',left_tensor=I,right_id=r['id'],right_tensor=B,right_constructors=r['constructors'],right_grading=degree,labels=labs),h
    base=ty((5,));sigma=[(-a)%5 for a in range(5)]+[5]
    for parity in [0,1]:
        pp=[0]*5+[parity];B,labs=cyclic_equivariant(base,sigma,2,pp)
        action=[(i^1)if O==[5]else i for i,(O,j)in enumerate(labs)]
        # Both lifts of the unique TY-odd object are consecutive in this list.
        require=common.require
        require(all(action[action[i]]==i for i in range(6)),'strict order-two action')
        T=crossed(B,action)
        yield f'TY(C5)^C2 crossed C2[parity={parity}]',T,'metaplectic_character_crossed_product',dict(base_tensor=B,TY_tensor=base,TY_inversion=sigma,TY_action_parity=pp,labels=labs,action=action,coherence='identity',categorical_action='multiply the equivariance isomorphism by -1 on the TY-odd component'),1

def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());buckets=collections.defaultdict(list)
    for rid,R in data.items():buckets[common.coarse(R)].append((rid,R))
    out=collections.defaultdict(list);attempts=[];seen=set()
    for name,R,kind,par,h in candidates():
        variants=[(name,R,kind,par)]
        # h has an explicit central lift: the Ising fermion in a pullback,
        # or the preserved canonical Rep(C2) boson in the crossed product.
        for g in gradings(R):
            if g[h]:continue
            M=zest(R,g,h)
            variants.append((f'C2-zest({name};h={h})',M,'associative_C2_zest',dict(base_name=name,base_constructor=kind,base_parameters=par,base_tensor=R,grading=g,central_invertible=h,central_lift='inherited_Ising_fermion'if kind=='graded_pullback'else'canonical_Rep_C2_boson_preserved_by_action')))
        for nm,M,kd,parameters in variants:
            sh=common.sha(M)
            if sh in seen:continue
            seen.add(sh);common.validate(M);hits=[]
            for rid,R0 in buckets[common.coarse(M)]:
                p=common.based_iso(R0,M)
                if p is None:continue
                common.require(all(R0[i][j][k]==M[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all tensor coefficients match')
                out[rid].append(dict(name=nm,constructor=kd,parameters=parameters,model_tensor=M,basis_map_source_to_model=p));hits.append(rid)
            attempts.append(dict(name=nm,constructor=kd,tensor_sha256=sh,matches=hits))
    rows=[dict(id=rid,tensor_sha256=common.sha(data[rid]),models=ms)for rid,ms in out.items()]
    (ROOT/'additional_models.json').write_text(json.dumps(rows,indent=2)+'\n')
    (ROOT/'additional_model_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
    print('matched',len(rows),'candidates',len(attempts),'seconds',time.monotonic()-start)
    print([(r['id'],r['models'][0]['name'])for r in rows])
if __name__=='__main__':main()
