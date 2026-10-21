"""Optional discovery accelerator; canonical r941_paired_rotation.py replays outputs."""
import hashlib,json
import r941_paired_rotation as p

def decide_reduced(A,b):
    # Select a basis of augmented rows exactly.  Their span includes the
    # right-hand side coordinate, so this removes only redundant equations.
    M=p.source.s.Matrix(A).row_join(p.source.s.Matrix(b))
    _,indices=M.T.rref()
    smallA=[A[i]for i in indices];smallb=[b[i]for i in indices]
    out=p.lp.decide(smallA,smallb)
    if out['status']=='exact_infeasible_relaxation':
        ray=[0]*len(b)
        for i,z in zip(indices,out['ray']):ray[i]=z
        out=dict(out,ray=ray)
    p.lp.verify(A,b,out)
    return out

def extend_ray(data,rhs,decision):
    columns,_,labels,_,_=data;y=list(decision['ray']);before=sum(a*b for a,b in zip(rhs,y))
    p.need(before<0,'input ray RHS negative')
    for col,(kind,canonical,ti)in zip(columns,labels):
        v=sum(a*b for a,b in zip(col,y))
        if v>=0:continue
        p.need(kind!='rotation_auxiliary','selected auxiliary column cannot be negative')
        at=len(rhs)-80+canonical+(0 if kind=='plus_pair'else 40)
        p.need(rhs[at]==0,'only absent zero-count blocks may need completion')
        y[at]-=v
    p.need(all(sum(a*b for a,b in zip(col,y))>=0 for col in columns),'completed universal ray')
    p.need(sum(a*b for a,b in zip(rhs,y))==before,'zero-RHS extension preserves strict separation')
    return dict(decision,ray=y)

def main():
    data=p.setup();progress=p.HERE/'r941_paired_rotation.progress.json';cached=json.loads(progress.read_text())if progress.exists()else[]
    cases=[];pool=[]
    for index in range(data[3]['complete_charge_allocation_count']):
        A,b,meta=p.build(data,index);decision=None
        if index<len(cached)and cached[index]['metadata']==meta:
            decision=cached[index]['decision'];p.lp.verify(A,b,decision)
            if decision['status']=='exact_infeasible_relaxation':decision=extend_ray(data,b,decision)
        if decision is None:
            decision=next((d for d in pool if sum(v*y for v,y in zip(b,d['ray']))<0),None)
        if decision is None:
            decision=decide_reduced(A,b)
            p.need(decision['status']in('exact_feasible_relaxation','exact_infeasible_relaxation'),'undecided discovery')
            p.lp.verify(A,b,decision)
            if decision['status']=='exact_infeasible_relaxation':decision=extend_ray(data,b,decision)
        # Even reused universal rays are checked by the unchanged canonical checker.
        p.lp.verify(A,b,decision);cases.append({'metadata':meta,'decision':decision})
        if decision['status']=='exact_infeasible_relaxation'and decision not in pool:pool.append(decision)
        progress.write_text(json.dumps(cases,indent=2)+'\n')
        print('941 fast',index,decision['status'],'universal rays',len(pool),flush=True)
    result={'id':'R8_3_941','kind':'complete_fermionic_correlated_trace_campaign','metadata':data[4],
        'complete_charge_allocation_count':data[3]['complete_charge_allocation_count'],'input_integer_pattern_count':343,
        'charge_surviving_pattern_count':data[3]['surviving_pattern_count'],'cases':cases,
        'exact_excluded_count':sum(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'exact_feasible_count':sum(c['decision']['status']=='exact_feasible_relaxation'for c in cases),
        'dependencies':{q.name:hashlib.sha256(q.read_bytes()).hexdigest()for q in
            (p.HERE/'source.json',p.HERE/'gram_cubic.json',p.HERE/'r941_fermionic.json',p.HERE/'r941_charges.json')},
        'scope':'complete finite integer-charge and height-six correlated twist relaxation; existence of a center or superfusion category is not asserted'}
    (p.HERE/'r941_paired_rotation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DONE',result['exact_excluded_count'],result['exact_feasible_count'])

if __name__=='__main__':main()
