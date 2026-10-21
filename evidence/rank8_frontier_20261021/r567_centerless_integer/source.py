"""Exact complete central-frame and partial-S domain for R8_3_567."""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import full_rotation as full
import character_modular as modular
from exact import vector
c=full.c;s=c.s;need=c.require


def data():
    full.base.install()
    census=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())
    source=next(r for r in census if r['id']=='R8_3_567');R=source['tensor']
    need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'source tensor binding')
    a=c.w.data(R);K0=a['K'];K=s.QQ.algebraic_field(K0.ext,s.I)
    move=lambda x:K.from_sympy(K0.to_sympy(x))
    need(all(move(x+y)==move(x)+move(y)and move(x*y)==move(x)*move(y)for x in a['ds']for y in a['ds']),'FP field inclusion')
    b=dict(a,K=K,D=move(a['D']),ds=list(map(move,a['ds'])),codegrees=list(map(move,a['codegrees'])))
    chars=modular.characters(R,b);frames=[];survivors=[]
    for index,cols in enumerate(a['lows']):
        why=c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        perms=[]if why else modular.assignments(b,chars,cols)
        frames.append({'index':index,'columns':[list(v)for v in cols],'ordinary_obstruction':why,'symmetric_S_assignments':[list(p)for p in perms]})
        survivors.extend((index,cols,p)for p in perms)
    need([i for i,cols,p in survivors]==[2,2],'complete unique full-S low frame')
    cols=a['lows'][2];L=s.Matrix.hstack(*map(s.Matrix,cols));Q,high=full.base.grams.high_columns(a,L)
    spectral_bad=[];degree=K.mod.degree()
    for index,(v,z)in enumerate(high):
        col=(0,)+tuple(v);dim=sum((K(x)*d for x,d in zip(col,b['ds'])),K.zero)
        for E,chi in enumerate(chars):
            ratio=b['D']/b['codegrees'][E]/K(b['multiplicities'][E])*modular.value(chi,col,K)/dim
            polynomial=s.Matrix.hstack(*(vector(ratio*K.unit**j,degree)for j in range(degree))).charpoly().all_coeffs()
            if any(x.q!=1 for x in polynomial):
                spectral_bad.append({'index':index,'character_index':E,'ratio_power_basis':c.ec(ratio),
                    'ratio_characteristic_polynomial':list(map(str,polynomial))});break
    integral_bad=[i for i,(v,z)in enumerate(high)if z[1]==0]
    need(integral_bad==[i for i,(v,z)in enumerate(high)if v[2:4]==(0,0)],'all integral restrictions identified')
    vectors=[tuple(v)for v,z in high]
    dual_indices=[]
    for v in vectors:
        col=(0,)+v;dual=tuple(col[a['du'][j]]for j in range(1,8))
        need(dual in vectors,'complete high domain closed under duality');dual_indices.append(vectors.index(dual))
    need(len(high)==45 and integral_bad==[0,34],'finite high domain')
    need([r['index']for r in spectral_bad]==[9,13,16,24,27,30,32,33,42],'complete partial-S spectral filter')
    allowed=[i for i in range(len(high))if i not in integral_bad+[r['index']for r in spectral_bad]]
    meta={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'tensor':R,
        'character_field_polynomial':[str(x)for x in K.mod.to_list()],
        'all_low_frames':frames,'low_index':2,'low_columns':[list(v)for v in cols],
        'residual_Gram':Q.tolist(),'high_vectors':[list(v)for v in vectors],
        'integral_forbidden_indices':integral_bad,'spectral_exclusions':spectral_bad,'allowed_indices':allowed,
        'dual_high_indices':dual_indices,'formal_codegrees':[c.ec(x)for x in b['codegrees']],
        'irreducible_dimensions':b['multiplicities'],'full_characters':[[c.ec(x)for x in ch]for ch in chars]}
    return R,a,b,chars,cols,Q,high,meta


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=json.loads(json.dumps(data()[-1],default=int));path=HERE/'source.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete R567 source/domain replay')
    print('PASS R567: one low frame,45 high vectors,2 integral and9 spectral exclusions,34 allowed vectors.')
