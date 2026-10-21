"""Complete fermion-charge paired trace cones for all93 R941 allocations."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math,sys
import source,r941_charges
HERE=Path(__file__).resolve().parent;FRONTIER=HERE.parent
sys.path.insert(0,str(FRONTIER/'noncommutative'))
import rotation_search as rotation,character_modular as modular,certified_lp as lp
need=source.need

def fixed_term_control():
    """Test the actual producer fixed-term builder on Z(Ising)."""
    s=source.s;K=s.QQ.algebraic_field(s.exp(s.pi*s.I/8));u=K.from_sympy(s.exp(s.pi*s.I/8));r=u**2-u**6
    one=(F(1),F(0),F(0),F(0));zero=(F(0),)*4;root=(F(0),F(1),F(0),F(0))
    chars=[[one,root,one],[one,r941_charges.scale(root,-1),one],[one,zero,r941_charges.scale(one,-1)]]
    R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,1],[0,1,0],[1,0,0]]]
    labels=list(itertools.product(range(3),repeat=2));known={(0,0),(2,2),(1,1),(2,0),(0,2)}
    dims=[K.one,r,K.one];twists=[K.one,u,-K.one]
    S0=[[K.one,r,K.one],[r,K.zero,-r],[K.one,-r,K.one]]
    charge=lambda ab:1 if ab[0]!=1 else -1
    def embed(x):return K(x[0])+K(x[1])*r
    values={ab:[r941_charges.value(ch,R[ab[0]][ab[1]])for ch in chars]for ab in labels}
    items=[]
    for ab in sorted(known):
        theta=twists[ab[0]]/twists[ab[1]];need(theta in(K.one,-K.one),'known Ising fixed-part twists')
        items.append((values[ab],charge(ab),1 if theta==K.one else -1))
    orth,sts=r941_charges.fixed_contributions(items)
    for E in range(3):
        direct_orth=K.zero;direct_sts=K.zero;remaining_orth=K.zero;remaining_sts=K.zero
        for ab in labels:
            val=embed(values[ab][E]);d=dims[ab[0]]*dims[ab[1]];q=S0[2][ab[0]]/dims[ab[0]];theta=twists[ab[0]]/twists[ab[1]]
            if ab in known:direct_orth+=q*d*val;direct_sts+=theta*q*d*val
            else:remaining_orth+=q*d*val;remaining_sts+=theta*q*d*val
        need(embed(orth[E])==direct_orth and embed(sts[E])==direct_sts,'producer fixed-part builder versus actual Ising S row')
        need(remaining_orth==-embed(orth[E]),'actual remaining orthogonality target')
        need(remaining_sts==-K(4)*embed(chars[E][2])-embed(sts[E]),'actual remaining STS target for scalar and negative-charge row')
    return {'actual_model':'Z(Ising)','known_union_count':5,'negative_charge_fixed_low_count':1,
        'checked_rows':3,'producer_fixed_term_builder_passes':True}

def setup():
    control=fixed_term_control()
    charges=r941_charges.run();need(charges==json.loads((HERE/'r941_charges.json').read_text()),'complete charge-allocation replay')
    row=source.data(941);R=row['tensor'];rotation.install();a=rotation.bq.data(R);cols=a['lows'][0]
    need(modular.assignments(a,modular.characters(R,a),cols)==[(0,1,2,3,4)],'complete full S assignment')
    ep=(0,0,1,1,1,1,1);old=json.loads((FRONTIER/'noncommutative/rotation_941_h6.json').read_text())
    choices=rotation.h.indicator_choices(R);systems=old['result']['branches'][0]['systems']
    need([v['indicators']for v in systems]==list(map(list,choices)),'complete original indicator domain')
    for candidate,case in zip(choices,systems):
        if candidate==ep:continue
        A0,b0,meta0=rotation.bq.system(R,a,cols,candidate,6)
        need(meta0==case['metadata']and case['ray']is not None,'other indicator excluded')
        rotation.h.check_farkas(A0,b0,case['ray'])
    need(ep in choices,'retained indicator')
    A,b,meta=rotation.bq.system(R,a,cols,ep,6)
    A,b,meta=modular.append_sts(R,a,cols,(0,1,2,3,4),A,b,meta,6)
    types,bound=rotation.bq.trace_types(6);nt=len(types);need(nt==38,'full trace domain')
    order=row['original_high_order'];high=rotation.bq.high_columns(a,cols)[2]
    need([list(high[j][0])for j in order]==row['canonical_high_vectors'],'source high order')
    oldcolumns=list(zip(*A));negative=[];pair_representatives=[];seen=set()
    for i,typ in enumerate(types):
        target=tuple(tuple((-1 if k%2==0 else 1)*v for v in moment)for k,moment in enumerate(typ))
        j=next(j for j,t in enumerate(types)if tuple(map(tuple,t))==target);negative.append(j)
        pair=tuple(tuple(x+y for x,y in zip(u,v))for u,v in zip(typ,types[j]))
        if pair not in seen:seen.add(pair);pair_representatives.append(i)
    need(all(negative[negative[i]]==i for i in range(nt)),'opposite phase involution')
    phase={theta:next(i for i,t in enumerate(types)if t==tuple((F(theta**k),F(0),F(0),F(0))for k in range(1,7)))for theta in(-1,1)}
    translated=[(j,-1)for j in(40,41,42,43)]+[(57,1)]
    for canonical,theta in translated:
        col=oldcolumns[order[canonical]*nt+phase[theta]];b=[v-z for v,z in zip(b,col)]
    chars=[[[F(z)for z in x]for x in ch]for ch in row['full_characters']]
    lowvalues=[[r941_charges.value(ch,v)for ch in chars]for v in row['low_columns']]
    highvalues=[[r941_charges.value(ch,[0]+v)for ch in chars]for v in row['canonical_high_vectors']]
    D=tuple(F(v)for v in row['formal_codegrees'][0]);weights=[[r941_charges.mul(v[0],v[E])for E in range(5)]for v in highvalues]
    fixed_items=[]
    for i,canonical in enumerate((40,41,42,43,57)):
        sign=1 if i<4 else -1
        fixed_items.append((lowvalues[i],sign,1))
        fixed_items.append((highvalues[canonical],sign,-sign))
    _,fixed_STS=r941_charges.fixed_contributions(fixed_items)
    Gtarget=[]
    for E in range(5):
        target=r941_charges.scale(r941_charges.mul(D,chars[E][3]),-1)
        target=r941_charges.add(target,r941_charges.scale(fixed_STS[E],-1))
        Gtarget.extend(target)
    Gcoeff=[]
    for canonical in range(40):
        block=[]
        for typ in types:
            block.append([z for E in range(5)for z in r941_charges.scale(r941_charges.mul(weights[canonical][E],typ[0]),-1)])
        Gcoeff.append(block)
    denominators=[math.lcm(Gtarget[k].denominator,*(v[k].denominator for block in Gcoeff for v in block))for k in range(20)]
    Gtarget=[int(x*d)for x,d in zip(Gtarget,denominators)]
    columns=[];labels=[]
    for canonical in range(40):
        raw=order[canonical]
        for ti in pair_representatives:
            oldcol=[x+y for x,y in zip(oldcolumns[raw*nt+ti],oldcolumns[raw*nt+negative[ti]])]
            count=[0]*80;count[canonical]=1
            columns.append(oldcol+[0]*20+count);labels.append(('plus_pair',canonical,ti))
        for ti in range(nt):
            count=[0]*80;count[40+canonical]=1
            gcol=[int(x*d)for x,d in zip(Gcoeff[canonical][ti],denominators)]
            columns.append(list(oldcolumns[raw*nt+ti])+gcol+count);labels.append(('minus_individual',canonical,ti))
    for j in range(65*nt,len(oldcolumns)):
        columns.append(list(oldcolumns[j])+[0]*100);labels.append(('rotation_auxiliary',j,0))
    rhs=b+Gtarget+[0]*80
    return columns,rhs,labels,charges,{'height':6,'root_order_bound':int(bound),'individual_trace_types':nt,
        'opposite_pair_trace_types':len(pair_representatives),'pair_representatives':pair_representatives,
        'negative_phase_indices':negative,'universal_rows':len(rhs),'universal_columns':len(columns),
        'G_row_STS_equations':20,'translated_low_twists':[list(v)for v in translated],
        'source_tensor_sha256':row['tensor_sha256'],'actual_fixed_term_control':control}

def build(data,index):
    columns,b,labels,charges,meta=data;case=charges['solutions'][index];p=case['plus_pairs'];q=case['minus_individuals']
    selected=[j for j,(kind,canonical,ti)in enumerate(labels)if kind=='rotation_auxiliary'or
        (p[canonical]>0 if kind=='plus_pair'else q[canonical]>0)]
    A=[list(v)for v in zip(*(columns[j]for j in selected))];rhs=list(b);rhs[-80:]=p+q
    metadata={'allocation_index':index,'pattern_index':case['pattern_index'],'plus_pairs':p,'minus_individuals':q,
        'selected_universal_columns':selected,'matrix_sha256':hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest(),
        'rhs_sha256':hashlib.sha256(json.dumps(rhs,separators=(',',':')).encode()).hexdigest()}
    return A,rhs,metadata

def run(write):
    data=setup();path=HERE/'r941_paired_rotation.json';progress=HERE/'r941_paired_rotation.progress.json'
    saved=None if write else json.loads(path.read_text());cached=json.loads(progress.read_text())if write and progress.exists()else[]
    cases=[];pool=[]
    for index in range(data[3]['complete_charge_allocation_count']):
        A,b,meta=build(data,index);decision=None
        if write:
            if index<len(cached)and cached[index]['metadata']==meta:decision=cached[index]['decision']
            if decision is None:
                for old in pool:
                    if sum(v*y for v,y in zip(b,old['ray']))>=0:continue
                    try:lp.verify(A,b,old);decision=old;break
                    except Exception:pass
            if decision is None:decision=lp.decide(A,b)
        else:
            need(saved['cases'][index]['metadata']==meta,'complete paired allocation domain');decision=saved['cases'][index]['decision']
        need(decision['status']in('exact_infeasible_relaxation','exact_feasible_relaxation'),'unfinished numerical decision')
        lp.verify(A,b,decision);cases.append({'metadata':meta,'decision':decision})
        if decision['status']=='exact_infeasible_relaxation'and decision not in pool:pool.append(decision)
        if write:
            progress.write_text(json.dumps(cases,indent=2)+'\n')
            print('941 paired',index,'pattern',meta['pattern_index'],decision['status'],flush=True)
    result={'id':'R8_3_941','kind':'complete_fermionic_correlated_trace_campaign','metadata':data[4],
        'complete_charge_allocation_count':data[3]['complete_charge_allocation_count'],'input_integer_pattern_count':343,'charge_surviving_pattern_count':data[3]['surviving_pattern_count'],
        'cases':cases,'exact_excluded_count':sum(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'exact_feasible_count':sum(c['decision']['status']=='exact_feasible_relaxation'for c in cases),
        'dependencies':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in(HERE/'source.json',HERE/'gram_cubic.json',HERE/'r941_fermionic.json',HERE/'r941_charges.json')},
        'scope':'complete finite integer-charge and height-six correlated twist relaxation; existence of a center or superfusion category is not asserted'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'complete correlated fermion receipt differs')
    print('PASS941 paired:',result['exact_excluded_count'],'excluded;',result['exact_feasible_count'],'exact feasible.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();run(args.write)
