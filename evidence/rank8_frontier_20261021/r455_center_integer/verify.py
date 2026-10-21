"""Complete R455 central integer Gram, spectrum, cubic, and parity campaign."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import central_support as c,character_modular as modular,rotation_search as rotation
from exact import vector,discover_roots,pc
from proofs import multiplication_matrix
s=c.s;need=c.require


def source():
    row=next(x for x in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())if x['id']=='R8_3_455');R=row['tensor']
    need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==row['tensor_sha256'],'full source tensor')
    a=c.data(R);K=a['K'];a['coords']=lambda x:tuple(Fraction(str(v))for v in vector(x,4))
    chars=modular.characters(R,a)
    fp=next(i for i,ch in enumerate(chars)if ch==a['ds'])
    need(a['codegrees'][fp]==a['D']and a['multiplicities'][fp]==1,'FP character at repeated codegree')
    chars[0],chars[fp]=chars[fp],chars[0]
    need(chars[0]==a['ds'],'tensor-unit character explicitly FP')
    frames=[];passing=[]
    for index,cols in enumerate(a['lows']):
        why=c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],K,a['embedding'],a['du'])
        assignments=[]if why else modular.assignments(a,chars,cols)
        frames.append({'index':index,'columns':[list(v)for v in cols],'ordinary_obstruction':why,'S_assignments':[list(p)for p in assignments]})
        passing.extend((index,cols,p)for p in assignments)
    need([i for i,cols,p in passing]==[0,0],'complete unique low/S frame')
    cols=a['lows'][0];L,Q,H=rotation.bq.high_columns(a,cols)
    spectral=[]
    for index,(v,z)in enumerate(H):
        col=(0,)+v;dim=sum((K(x)*d for x,d in zip(col,a['ds'])),K.zero)
        for E,ch in enumerate(chars):
            ratio=a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*modular.value(ch,col,K)/dim
            cp=multiplication_matrix(ratio,K,a['factor']).charpoly().all_coeffs()
            if any(x.q!=1 for x in cp):spectral.append(index);break
    need(len(H)==13 and not spectral,'complete thirteen-vector spectral domain')
    return R,a,chars,cols,Q,H,{'id':row['id'],'tensor_sha256':row['tensor_sha256'],'tensor':R,
        'field_polynomial':pc(a['factor']),'frames':frames,'high_vectors':[list(v)for v,z in H],
        'residual_Gram':Q.tolist(),'partial_S_forbidden_indices':spectral}


def enumerate_grams(Q,H):
    indices=[0,2,3,4];vs=[tuple(v[i]for i in indices)for v,z in H];small=Q.extract([i+1 for i in indices],[i+1 for i in indices])
    lift=[0,0,1,2,3,1,1]
    need(all(v==tuple(w[j]for j in lift)for(v,z),w in zip(H,vs)),'complete rank-four high reduction')
    need(all(Q[i+1,j+1]==small[lift[i],lift[j]]for i in range(7)for j in range(7)),'complete residual Gram reduction')
    pairs=list(itertools.combinations_with_replacement(range(4),2));target=tuple(int(small[i,j])for i,j in pairs)
    forms=[tuple(v[i]*v[j]for i,j in pairs)for v in vs];groups=[[i for i,v in enumerate(vs)if next(j for j,x in enumerate(v)if x)==k]for k in range(4)]
    counts=[0]*len(vs);answers=[]
    def level(k,residual):
        if k==4:
            need(not any(residual),'terminal Gram residual');answers.append(tuple(counts));return
        row=[j for j,(i,z)in enumerate(pairs)if i==k];domain=groups[k]
        def choose(at,r):
            if at==len(domain):
                if not any(r[j]for j in row):level(k+1,r)
                return
            i=domain[at];f=forms[i];bound=min(r[j]//x for j,x in enumerate(f)if x)
            for m in range(bound+1):counts[i]=m;choose(at+1,tuple(v-m*w for v,w in zip(r,f)))
            counts[i]=0
        choose(0,residual)
    level(0,target);need(len(set(answers))==len(answers),'no duplicate integer Grams')
    # Independent two-block outer-product enumeration.
    blocks=[[i for i,v in enumerate(vs)if not any(v[2:])],[i for i,v in enumerate(vs)if not any(v[:2])]]
    need(sorted(blocks[0]+blocks[1])==list(range(len(H))),'complete disjoint block partition')
    independent=[]
    for block,coordinates in zip(blocks,[(0,1),(2,3)]):
        j,k=coordinates;goal=(int(small[j,j]),int(small[j,k]),int(small[k,k]));out=[]
        def visit(at,residual,terms):
            if at==len(block):
                if not any(residual):out.append(terms)
                return
            index=block[at];v=vs[index];form=(v[j]**2,v[j]*v[k],v[k]**2)
            bound=min(r//x for r,x in zip(residual,form)if x)
            for m in range(bound+1):visit(at+1,tuple(r-m*x for r,x in zip(residual,form)),terms+[(index,m)])
        visit(0,goal,[]);independent.append(out)
    other=[]
    for left,right in itertools.product(*independent):
        m=[0]*len(H)
        for i,z in left+right:m[i]=z
        other.append(tuple(m))
    answers=sorted(answers);need(answers==sorted(other),'two complete integer enumerations agree')
    for m in answers:
        need(all(sum(m[z]*H[z][0][i]*H[z][0][j]for z in range(len(H)))==Q[i+1,j+1]
                 for i in range(7)for j in range(7)),'full49 Gram identity')
    return answers,{'reduced_Gram':small.tolist(),'block_solution_counts':list(map(len,independent))}


def cubic_data(a,chars,cols,H):
    K=a['K'];need(all(ch[i]==ch[a['du'][i]]for ch in chars for i in range(8)),'all distinguished objects self-dual')
    allcols=list(cols)+[(0,)+v for v,z in H];out=[]
    for E,F,G in itertools.combinations_with_replacement(range(1,5),3):
        coeff=[]
        for col in allcols:
            dim=sum((K(x)*d for x,d in zip(col,a['ds'])),K.zero);value=a['D']/dim
            for j in (E,F,G):value*=modular.value(chars[j],col,K)/a['codegrees'][j]/K(a['multiplicities'][j])
            coeff.append(value)
        out.append(((E,F,G),sum(coeff[:5],K.zero),coeff[5:]))
    return out


def spectrum_data(a,chars,cols,H):
    K=a['K'];roots=discover_roots(a['factor'],K);need(roots is not None and len(roots)==4,'full quartic Galois orbit')
    def images(x):return{sum((K(co)*root**j for j,co in enumerate(reversed(x.to_list()))),K.zero)for root in roots}
    allcols=list(cols)+[(0,)+v for v,z in H];rows=[]
    for E,ch in enumerate(chars):
        ratios=[]
        for col in allcols:
            dim=sum((K(x)*d for x,d in zip(col,a['ds'])),K.zero)
            ratios.append(a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*modular.value(ch,col,K)/dim)
        seen=set()
        for value in ratios:
            if value in seen:continue
            orbit=images(value);seen.update(orbit)
            if len(orbit)==1:continue
            ordered=sorted(orbit,key=lambda x:tuple(map(str,x.to_list())));ref=ordered[0]
            for other in ordered[1:]:
                rows.append((E,ratios[:5].count(ref)-ratios[:5].count(other),
                             [int(x==ref)-int(x==other)for x in ratios[5:]]))
    return rows


def run():
    R,a,chars,cols,Q,H,meta=source();K=a['K'];solutions,stats=enumerate_grams(Q,H)
    need(len(solutions)==812,'complete integer Gram count');cubics=cubic_data(a,chars,cols,H);spectrum=spectrum_data(a,chars,cols,H)
    need(cols[0]==cols[1]==(1,0,0,0,0,0,0,0),'nontrivial central invertible forgets to unit')
    need(a['D']==a['codegrees'][1]and a['multiplicities'][1]==1,'central invertible distinguished character')
    parity=[]
    for i,(v,z)in enumerate(H):
        col=(0,)+v;dim=sum((K(x)*d for x,d in zip(col,a['ds'])),K.zero);charge=modular.value(chars[1],col,K)/dim
        need(charge in(K.one,-K.one),'C2 monodromy charge')
        if charge==-K.one:parity.append(i)
    records=[];cubic_survivors=[];spectrum_survivors=[];final=[]
    for i,m in enumerate(solutions):
        values=[low+sum((K(n)*z for n,z in zip(m,high)),K.zero)for triple,low,high in cubics]
        bad=[j for j,x in enumerate(values)if len(x.to_list())>1 or(x.to_list()and(x.to_list()[0].denominator!=1 or x.to_list()[0]<0))]
        spectral_bad=[j for j,(E,low,hi)in enumerate(spectrum)if low+sum(n*z for n,z in zip(m,hi))]
        parity_bad=[j for j in parity if m[j]%2]
        if not bad:cubic_survivors.append(i)
        if not bad and not spectral_bad:spectrum_survivors.append(i)
        if not bad and not spectral_bad and not parity_bad:final.append(i)
        records.append({'index':i,'multiplicities':list(m),'first_cubic_obstruction':None if not bad else {'indices':list(cubics[bad[0]][0]),'value':c.ec(values[bad[0]])},
            'Galois_spectrum_obstructions':spectral_bad,'odd_negative_monodromy_multiplicities':parity_bad})
    return {'kind':'complete_R455_central_integer_campaign','source':meta,'enumeration':stats,'integer_Gram_count':len(solutions),
        'cubic_triples':[list(x[0])for x in cubics],'Galois_spectrum_row_count':len(spectrum),'negative_monodromy_high_indices':parity,
        'patterns':records,'cubic_survivors':cubic_survivors,'cubic_and_spectrum_survivors':spectrum_survivors,
        'all_tests_survivors':final,'outcome':'general_exclusion'if not final else'necessary_integer_data_survives_not_a_model',
        'scope':'pseudo-unitary central necessary conditions; general categorification applicability follows independently certified Galois-pseudo-unitary gate; no no-integral-center assumption is imposed'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();actual=json.loads(json.dumps(run(),default=int));path=HERE/'results.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete R455 integer campaign replay')
    print('PASS R455:',actual['integer_Gram_count'],'integer Grams;',len(actual['cubic_survivors']),'cubic;',len(actual['cubic_and_spectrum_survivors']),'spectrum;',len(actual['all_tests_survivors']),'parity survivors.')
