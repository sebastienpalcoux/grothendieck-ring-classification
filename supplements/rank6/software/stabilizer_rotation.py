"""Stabilizer rotation and exact third-indicator separation.

For a pseudo-unitary fusion category, the pair-insertion lemma applies to a
self-dual simple Y fixed by an invertible involution g. If left multiplication
by g exchanges the two (1+g)-module structures on Y, and [Y^3:1]=2, cyclic
rotation is not scalar. When 3 is absent from the Frobenius--Schur exponent's
prime support, its trace is therefore -1. This module combines that necessary
condition with exhaustive involution-module actions and central trace systems.
All discovery rays are replayed using exact integer arithmetic. No census ID,
rank-specific branch, selected center, or dimension lookup enters the test.
"""
import itertools
from exact import require
from augmented_spectrum import AugmentedSpectrum
import modular_character_induction as I
from higher_traces import trace_types, check_farkas, farkas
from full_morita_gram import system as morita_system
from module_dual_gram import anti_representations
from involution_module import invs


def trace_system(R,data,table,columns,indicators,height,labelling,spectrum,objects,values=None):
    """Append exact equations nu_3(Y)=-1 to the inherited modular system."""
    require(height>=3,'third indicator outside trace height')
    K=table.K
    A,b,meta=I.equation_system(R,data,table,columns,indicators,height,labelling,spectrum)
    L=I.s.Matrix.hstack(*map(I.s.Matrix,columns))
    base,_,rotation=I.system_rotation(R,data,L,indicators,height)
    labels=rotation['labels'];forbidden=set(map(tuple,spectrum.forbidden))
    keep=[j for j in range(len(base[0])) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
    require(len(keep)==len(A[0]),'modular/rotation variable ordering mismatch')
    types,_=trace_types(data['q'],data['primes'],height)
    square=K.from_sympy(I.s.sqrt(data['q']))
    phase=[K(t[2][0])+K(t[2][1])*square for t in types]
    values=[-1]*len(objects) if values is None else list(values)
    require(len(values)==len(objects) and all(type(v) is int for v in values),'invalid prescribed third indicators')
    added=0
    for obj,value in zip(objects,values):
        rhs=K(value)*table.D-sum((K(v[obj])*table.dims[tuple(v)] for v in columns),K.zero)
        coeff=[K(labels[j][0][obj-1])*table.dims[(0,)+tuple(labels[j][0])]*phase[labels[j][1]]
               if j<len(labels) else K.zero for j in keep]
        for row,value in I.rational_rows(coeff,rhs,K):
            A.append(row);b.append(value);added+=1
    return A,b,{**meta,'third_indicator_equations':added,'equations':len(A)}


def conditional_certificate(R,objects,height=3,progress=None):
    """Exclude all central data satisfying the listed third indicators.

    This subcertificate by itself is conditional, not a categorification
    obstruction. The outer certificate supplies its categorical hypotheses.
    """
    objects=sorted(set(objects));require(objects and all(0<j<len(R) for j in objects),'bad third-indicator objects')
    try:data,table=I.reciprocity_data(R)
    except I.Ineligible:return None
    if table.K.mod.degree()>(1 if data['q']==1 else 2):return None
    if 3 in data['primes']:return None
    branches=[]
    for ix,columns in enumerate(data['lows']):
        branch={'columns':list(map(list,columns))}
        why=I.low_failure(columns,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:branch['ordinary']=why;branches.append(branch);continue
        labs=table.assignments(columns);branch['labellings']=list(map(list,labs))
        if labs:
            _,high=I.high_columns(data,I.s.Matrix.hstack(*map(I.s.Matrix,columns)))
            sp=AugmentedSpectrum(table,columns,high);branch['spectrum']=sp.metadata()
            if not sp.missing_low:
                cases=[]
                for lab in labs:
                    for ep in I.indicator_choices(R):
                        A,b,meta=trace_system(R,data,table,columns,ep,height,lab,sp,objects)
                        y=farkas(A,b)
                        if progress:progress(ix,lab,ep,y is not None)
                        if y is None:return None
                        check_farkas(A,b,y)
                        cases.append({'labelling':list(lab),'indicators':list(ep),'system':meta,'y':y,
                                      'bTy':sum(a*z for a,z in zip(b,y))})
                branch['cases']=cases
        branches.append(branch)
    return {'kind':'conditional_third_indicator','version':1,'objects':objects,'values':[-1]*len(objects),
            'height':height,'q':data['q'],'prime_support':data['primes'],'table':table.metadata(),
            'column_counts':list(map(len,data['columns'])),'branches':branches}


def verify_conditional(R,c):
    data,table=I.reciprocity_data(R);objects=c['objects']
    require(c['kind']=='conditional_third_indicator' and c.get('version')==1,'wrong conditional indicator kind/version')
    require(objects==sorted(set(objects)) and objects and all(type(j) is int and 0<j<len(R) for j in objects),'bad conditional object set')
    require(c['values']==[-1]*len(objects),'wrong conditional third indicators')
    require(type(c['height']) is int and 3<=c['height']<=12,'invalid conditional height')
    require(table.K.mod.degree()<=(1 if data['q']==1 else 2),'character field outside trace field')
    require(c['q']==data['q'] and c['prime_support']==data['primes'] and 3 not in data['primes'],'wrong Cauchy prime support')
    require(c['table']==table.metadata() and c['column_counts']==list(map(len,data['columns'])),'incorrect exhaustive character/column domain')
    require(len(c['branches'])==len(data['lows']),'omitted low induction frame')
    for columns,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==list(map(list,columns)),'wrong low induction frame')
        why=I.low_failure(columns,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'wrong ordinary obstruction');continue
        labs=table.assignments(columns)
        require(branch['labellings']==list(map(list,labs)),'missing character labelling')
        if not labs:continue
        _,high=I.high_columns(data,I.s.Matrix.hstack(*map(I.s.Matrix,columns)))
        sp=AugmentedSpectrum(table,columns,high)
        require(branch['spectrum']==sp.metadata(),'wrong augmented spectrum')
        if sp.missing_low:continue
        expected=[(list(lab),list(ep)) for lab in labs for ep in I.indicator_choices(R)]
        require([(r['labelling'],r['indicators']) for r in branch['cases']]==expected,'missing labelling/second-indicator branch')
        for rec in branch['cases']:
            A,b,meta=trace_system(R,data,table,columns,rec['indicators'],c['height'],rec['labelling'],sp,objects)
            require(rec['system']==meta,'incorrect conditional system metadata')
            check_farkas(A,b,rec['y'])
            require(rec['bTy']==sum(a*z for a,z in zip(b,rec['y'])),'wrong conditional separating value')
    return True


def rotation_objects(R,g,fixed,T):
    """Objects meeting the local pair-insertion hypothesis in this branch."""
    f=len(fixed)
    return [y for a,y in enumerate(fixed)
            if R[y][y][0]==1 and R[y][y][y]==2 and T[g][a*f+a]==-1]


def zero_column_ray(A,b):
    if len(A[0]):return farkas(A,b)
    if not any(b):return None
    y=[0]*len(b);j=next(j for j,z in enumerate(b) if z);y[j]=-1 if b[j]>0 else 1
    return y


def certificate(R,height=3,node_limit=2000000,progress=None):
    n=len(R)
    if any(R[i][j]!=R[j][i] for i in range(n) for j in range(n)):return None
    for g in invs(R):
        info=anti_representations(R,g)
        if info is None:continue
        fixed,seed,nodes,reps=info;branches=[];conditionals=[];cache={};failed=False
        for ti,T in enumerate(reps):
            ab,meta=morita_system(R,g,fixed,T,node_limit)
            branch={'T':list(map(list,T))}
            if ab is None:branch.update(method='morita_rank',meta=meta)
            else:
                y=zero_column_ray(*ab)
                if y is not None:
                    check_farkas(*ab,y);branch.update(method='morita_gram',meta=meta,y=y)
                else:
                    objects=rotation_objects(R,g,fixed,T)
                    if not objects:failed=True;break
                    key=tuple(objects)
                    if key not in cache:
                        conditional=conditional_certificate(R,objects,height,progress)
                        if conditional is None:failed=True;break
                        cache[key]=len(conditionals);conditionals.append(conditional)
                    branch.update(method='stabilizer_rotation',objects=objects,conditional=cache[key])
            branches.append(branch)
        if not failed:
            return {'kind':'stabilizer_rotation','version':1,'scope':'pseudo_unitary','involution':g,
                    'fixed':fixed,'generators':list(seed),'generator_tuples':nodes,
                    'branches':branches,'conditionals':conditionals}
    return None


def verify(R,c):
    require(c['kind']=='stabilizer_rotation' and c.get('version')==1 and c['scope']=='pseudo_unitary','wrong stabilizer-rotation kind/version/scope')
    g=c['involution'];require(g in invs(R),'invalid stabilizer involution')
    info=anti_representations(R,g);require(info is not None,'ineligible involution module domain')
    fixed,seed,nodes,reps=info
    require(c['fixed']==fixed and c['generators']==list(seed) and c['generator_tuples']==nodes,'incorrect exhaustive module domain')
    require([r['T'] for r in c['branches']]==[list(map(list,T)) for T in reps],'missing involution module branch')
    # Check combinatorial branch coverage before the expensive exact traces.
    for T,branch in zip(reps,c['branches']):
        if branch['method']=='stabilizer_rotation':
            objects=rotation_objects(R,g,fixed,T)
            require(objects and branch['objects']==objects,'local pair-insertion hypotheses fail')
            ix=branch['conditional'];require(type(ix) is int and 0<=ix<len(c['conditionals']),'bad conditional reference')
            require(c['conditionals'][ix]['objects']==objects,'conditional indicator set mismatch')
    for cc in c['conditionals']:verify_conditional(R,cc)
    used=set()
    for T,branch in zip(reps,c['branches']):
        if branch['method']=='stabilizer_rotation':
            objects=rotation_objects(R,g,fixed,T)
            require(objects and branch['objects']==objects,'local pair-insertion hypotheses fail')
            ix=branch['conditional'];require(type(ix) is int and 0<=ix<len(c['conditionals']),'bad conditional reference')
            require(c['conditionals'][ix]['objects']==objects,'conditional indicator set mismatch');used.add(ix)
        else:
            ab,meta=morita_system(R,g,fixed,T)
            require(branch['meta']==meta,'wrong full Morita Gram metadata')
            if ab is None:require(branch['method']=='morita_rank','incorrect Morita rank branch')
            else:
                require(branch['method']=='morita_gram','incorrect Morita Gram branch')
                check_farkas(*ab,branch['y'])
    require(used==set(range(len(c['conditionals']))),'unused or duplicate conditional subcertificate')
    return True

def general_certificate(R,height=3,node_limit=2000000,progress=None):
    from galois_pseudo_reduction import certificate as reduction_certificate
    pseudo=certificate(R,height,node_limit,progress)
    if pseudo is None:return None
    reduction=reduction_certificate(R)
    if reduction is None:return None
    return {'kind':'general_stabilizer_rotation','version':1,'scope':'general',
            'reduction':reduction,'pseudo':pseudo}


def verify_general(R,c):
    from galois_pseudo_reduction import verify as verify_reduction
    require(c['kind']=='general_stabilizer_rotation' and c.get('version')==1 and c['scope']=='general','wrong general stabilizer-rotation kind/version/scope')
    report=verify_reduction(R,c['reduction'])
    verify(R,c['pseudo'])
    return {**report,'involution_module_branches':len(c['pseudo']['branches']),
            'conditional_trace_certificates':len(c['pseudo']['conditionals']),
            'general_categorification_excluded':True}


if __name__=='__main__':
    import argparse,json,time
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('id');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify',action='store_true');ap.add_argument('--general',action='store_true',help='generate a full general-scope certificate');args=ap.parse_args()
    R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']==args.id)
    if args.verify:
        record=json.loads(args.output.read_text());require(record['id']==args.id,'wrong tensor label');cc=record['certificate'];report=verify_general(R,cc) if cc.get('kind')=='general_stabilizer_rotation' else verify(R,cc);print('EXACT STABILIZER ROTATION CERTIFICATE VERIFIED',args.id,report)
    else:
        started=time.monotonic();discover=general_certificate if args.general else certificate;c=discover(R,progress=lambda ix,lab,ep,ok:print(ix,lab,ep,ok,flush=True))
        if c:
            if args.general:verify_general(R,c)
            else:verify(R,c)
        args.output.write_text(json.dumps({'id':args.id,'outcome':('general_excluded' if args.general else 'pseudo_unitary_excluded') if c else 'no_exact_obstruction','certificate':c,'seconds':time.monotonic()-started},separators=(',',':'))+'\n')
        print(('EXACT GENERAL EXCLUSION' if args.general else 'EXACT PSEUDO-UNITARY EXCLUSION') if c else 'NO EXACT OBSTRUCTION',args.id,flush=True)
