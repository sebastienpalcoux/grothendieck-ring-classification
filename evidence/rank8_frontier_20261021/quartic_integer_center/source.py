"""Exact complete central source and cubic data for R928 and R941."""
from pathlib import Path
import argparse
from fractions import Fraction
import hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import central_support as c
import rotation_search as rotation
import character_modular as modular
from exact import vector,discover_roots
s=c.s;need=c.require


def data(number):
    census=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())
    row=next(r for r in census if r['id']==f'R8_3_{number}');R=row['tensor']
    need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==row['tensor_sha256'],'source hash')
    a=c.data(R);K=a['K'];degree=K.mod.degree();need(degree==4,'quartic FP field')
    a['coords']=lambda x:tuple(Fraction(str(v))for v in vector(x,4))
    chars=modular.characters(R,a);frames=[];good=[]
    for index,cols in enumerate(a['lows']):
        fail=c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],K,a['embedding'],a['du'])
        perms=[]if fail else modular.assignments(a,chars,cols)
        frames.append({'index':index,'columns':[list(v)for v in cols],'ordinary_obstruction':fail,
                       'symmetric_S_assignments':[list(p)for p in perms]})
        if perms:good.append(index)
    need(good==[0],'complete unique low frame');cols=a['lows'][0]
    L,Qfull,H=rotation.bq.high_columns(a,cols);Q=Qfull[1:,1:]
    indices=[6,0,2,4]if number==928 else[2,3,0,5]
    reduced=[tuple(v[i]for i in indices)for v,z in H]
    need(len(H)==65 and len(set(reduced))==65,'complete distinct65-vector domain')
    order=sorted(range(65),key=lambda i:reduced[i]);high=[H[i]for i in order];vectors=[reduced[i]for i in order]
    full=[tuple(v)for v,z in high];lift=[1,1,2,2,3,3,0]if number==928 else[2,2,0,1,1,3,3]
    need(all(v==tuple(w[k]for k in lift)for v,w in zip(full,vectors)),'exact full-vector lift')
    Q4=Q.extract(indices,indices)
    need(Q4==s.Matrix([[8,8,8,12],[8,50,58,73],[8,58,74,89],[12,73,89,117]]),'common reduced Gram')
    need(all(Q[i,j]==Q4[lift[i],lift[j]]for i in range(7)for j in range(7)),'complete Gram lift')
    def dim(col):return sum((K(v)*d for v,d in zip(col,a['ds'])),K.zero)
    spectral_bad=[]
    for index,(v,z)in enumerate(high):
        col=(0,)+v;d=dim(col)
        for E,ch in enumerate(chars):
            ev=a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*modular.value(ch,col,K)/d
            poly=s.Matrix.hstack(*(vector(ev*K.unit**j,4)for j in range(4))).charpoly().all_coeffs()
            if any(x.q!=1 for x in poly):spectral_bad.append({'index':index,'character':E,'polynomial':list(map(str,poly))});break
    need(not spectral_bad,'source spectral filter unexpectedly changed')
    dual=[]
    for v in full:
        col=(0,)+v;dv=tuple(col[a['du'][j]]for j in range(1,8))
        need(dv in full,'dual-closed high domain');dual.append(full.index(dv))
    need(all(ch[a['du'][j]]==ch[j]for ch in chars for j in range(8)),'all distinguished central objects selfdual')
    roots=[]
    for q in (2,3):
        rr=discover_roots(s.Poly(c.w.t*c.w.t-q,c.w.t),K)
        roots.append(next(x for x in rr if a['embedding'].sign(x)>0))
    basis=[K.one,roots[0],roots[1],roots[0]*roots[1]]
    C=s.Matrix.hstack(*(vector(x,4)for x in basis)).inv()
    coords=lambda x:tuple(Fraction(str(v))for v in C*vector(x,4))
    lowvalues=[[modular.value(ch,col,K)for ch in chars]for col in cols]
    highvalues=[[modular.value(ch,(0,)+v,K)for ch in chars]for v,z in high]
    lowdims=[dim(col)for col in cols];highdims=[dim((0,)+v)for v,z in high]
    cubics=[]
    for E,F,G in itertools.combinations_with_replacement(range(1,5),3):
        scale=a['D']
        for index in (E,F,G):scale/=a['codegrees'][index]*K(a['multiplicities'][index])
        constant=scale*sum((v[E]*v[F]*v[G]/d for v,d in zip(lowvalues,lowdims)),K.zero)
        coefficients=[scale*v[E]*v[F]*v[G]/d for v,d in zip(highvalues,highdims)]
        cubics.append({'triple':[E,F,G],'constant':list(map(str,coords(constant))),
                       'coefficients':[list(map(str,coords(x)))for x in coefficients]})
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],'tensor':R,
        'all_low_frames':frames,'low_index':0,'low_columns':[list(v)for v in cols],
        'formal_codegrees':[list(map(str,coords(x)))for x in a['codegrees']],
        'irreducible_dimensions':a['multiplicities'],
        'full_characters':[[list(map(str,coords(x)))for x in ch]for ch in chars],
        'canonical_high_vectors':[list(v)for v in full],'reduced_high_vectors':[list(v)for v in vectors],
        'original_high_order':order,'reduced_coordinates':['g','a','b','c'],'full_coordinate_lift':lift,
        'reduced_Gram':Q4.tolist(),'spectral_exclusions':spectral_bad,'dual_high_indices':dual,
        'cubic_coordinate_basis':['1','sqrt(2)','sqrt(3)','sqrt(6)'],'low_cubic_equations':cubics,
        'scope':'necessary pseudo-unitary center data, applicable to any complex categorification after the independently proved Galois reduction'}


def run():
    records=[data(n)for n in (928,941)]
    need(records[0]['reduced_high_vectors']==records[1]['reduced_high_vectors'],'same canonical65 high vectors')
    need(records[0]['reduced_Gram']==records[1]['reduced_Gram'],'same residual Gram')
    return {'kind':'complete_quartic_pair_central_Gram_and_cubic_domains','records':records}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'source.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete source data changed')
    print('PASS928/941: identical complete65-vector Gram domain; exact full-character spectral and20 cubic equations each.')
