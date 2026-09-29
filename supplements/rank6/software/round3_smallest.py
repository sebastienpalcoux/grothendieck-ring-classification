"""Forced C4 associator twists combined with stabilizer rotation.

The full tensor, not a census identifier, determines applicability. Discovery
uses an LP only to propose rays; verify() calls only exact integer checkers.
"""
import itertools,json,time,signal
from pathlib import Path
from fractions import Fraction as Q
import stabilizer_rotation_higher as H
from exact import require
from rings import validate,dual,Characters
from module_dual_gram import anti_representations
from higher_traces import trace_types,farkas,check_farkas

ROOT=Path(__file__).resolve().parents[1]

class Ineligible(ValueError):pass
class Survives(ValueError):pass

def family(R):
    """Check all products of the uniform, self-dual C4 quadratic family."""
    if len(R)!=6:return None
    if any(R[i][j]!=R[j][i] for i in range(6) for j in range(6)):return None
    du=dual(R);unit=[1,0,0,0,0,0]
    G=[i for i in range(6) if R[i][du[i]]==unit]
    if len(G)!=4:return None
    X=[i for i in range(6) if i not in G]
    if any(du[x]!=x for x in X):return None
    for t in sorted(G):
        if t==0 or du[t]==t:continue
        h=next((k for k,v in enumerate(R[t][t]) if v),None)
        if h not in G or h in (0,t,du[t]) or R[h][h]!=unit:continue
        tp=du[t];x,y=X;m=R[x][x][x]
        indices=[0,t,h,tp,x,y];T=[[[0]*6 for _ in range(6)] for _ in range(6)]
        for a,b in itertools.product(range(6),repeat=2):
            if a<4 and b<4:T[a][b][(a+b)%4]=1
            elif a<4:T[a][b][4+(a+b-4)%2]=1
            elif b<4:T[a][b][4+(a+b-4)%2]=1
            else:
                parity=(a+b)%2;T[a][b][parity]=T[a][b][parity+2]=1
                T[a][b][4]=T[a][b][5]=m
        if all(R[indices[a]][indices[b]][indices[c]]==T[a][b][c] for a,b,c in itertools.product(range(6),repeat=3)):
            validate(R)
            return {'generator':t,'inverse_generator':tp,'involution':h,'noninvertibles':X,
                    'multiplicity':m,'pointed_associator_class':2,'fourth_indicator':-1}
    return None

def module_data(R,fam):
    info=anti_representations(R,fam['involution']);require(info is not None,'C4 module domain unavailable')
    fixed,seed,nodes,reps=info
    objects=[]
    if reps:
        objects=[x for x in fixed if H.cubic(R,x)>0 and all(T[fam['involution']][fixed.index(x)*len(fixed)+fixed.index(x)]==-1 for T in reps)]
    return {'fixed':fixed,'generators':list(seed),'generator_tuples':nodes,
            'representations':[[list(v) for v in T] for T in reps],'objects':objects}

def indicators(R,fam):
    # The fixed-point involution has trivial pointed associator, so nu2(h)=1.
    return [ep for ep in H.I.indicator_choices(R) if ep[fam['involution']-1]==1]

def system(R,data,tab,cols,ep,height,fam,modules):
    A,b,meta=H.trace_system(R,data,tab,cols,ep,height,None,None,modules['objects'])
    L=H.I.s.Matrix.hstack(*map(H.I.s.Matrix,cols))
    _,_,rot=H.I.system_rotation(R,data,L,ep,height);labels=rot['labels']
    ts,bound=trace_types(data['q'],data['primes'],height)
    t,tp=fam['generator'],fam['inverse_generator']
    keep=[j for j in range(len(A[0])) if j>=len(labels)
          or not(labels[j][0][t-1] or labels[j][0][tp-1])
          or ts[labels[j][1]][3]==(Q(-1),Q(0))]
    A=[[row[j] for j in keep] for row in A]
    return A,b,{**meta,'variables':len(keep),'before_forced_twist':len(rot['labels']),
                'forced_twist_removed':sum(j<len(labels) for j in range(len(rot['labels'])) if j not in set(keep)),
                'trace_order_bound':bound}

def certificate(R,height=4,progress=None):
    fam=family(R)
    if fam is None:raise Ineligible('not the uniform self-dual C4 quadratic family')
    modules=module_data(R,fam)
    if not modules['representations']:
        return {'kind':'c4_associator_stabilizer','version':1,'scope':'general','family':fam,'modules':modules,'method':'empty_module_domain'}
    if any(H.cubic(R,x)%2 for x in modules['objects']):
        return {'kind':'c4_associator_stabilizer','version':1,'scope':'general','family':fam,'modules':modules,'method':'odd_clifford_dimension'}
    require(4<=height<=12,'invalid forced fourth-twist trace height')
    try:data,tab=H.I.reciprocity_data(R)
    except H.I.Ineligible as e:raise Ineligible(str(e)) from e
    branches=[]
    for ix,cols in enumerate(data['lows']):
        rec={'columns':list(map(list,cols))}
        why=H.I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:rec['ordinary']=why;branches.append(rec);continue
        # All summands of I(1) have trivial twist.
        if any(c[fam['generator']] or c[fam['inverse_generator']] for c in cols):
            rec['method']='low_twist_conflict';branches.append(rec);continue
        cases=[]
        for ep in indicators(R,fam):
            A,b,meta=system(R,data,tab,cols,ep,height,fam,modules);ray=farkas(A,b)
            if progress:progress(ix,list(ep),ray is not None)
            if ray is None:raise Survives('a necessary forced-twist central branch survives')
            check_farkas(A,b,ray);cases.append({'indicators':list(ep),'system':meta,'ray':ray})
        rec['cases']=cases;branches.append(rec)
    return {'kind':'c4_associator_stabilizer','version':1,'scope':'general','family':fam,'modules':modules,'method':'forced_twist_trace',
            'reduction':{'kind':'two_fp_values'},'height':height,'q':data['q'],'prime_support':data['primes'],
            'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify(R,c):
    require(c.get('kind')=='c4_associator_stabilizer' and c.get('version')==1 and c.get('scope')=='general','incorrect C4 scope')
    fam=family(R);require(fam is not None and c['family']==fam,'full tensor C4 hypothesis failed')
    modules=module_data(R,fam);require(c['modules']==modules,'incomplete module domain')
    if c['method']=='empty_module_domain':require(not modules['representations'],'module representation exists');return True
    if c['method']=='odd_clifford_dimension':
        require(modules['representations'] and any(H.cubic(R,x)%2 for x in modules['objects']),'no odd forced Clifford space');return True
    require(c['method']=='forced_twist_trace' and c['reduction']=={'kind':'two_fp_values'},'bad reduction')
    require(len(set(Characters(R).fp()[2]))==2,'two-dimensional Galois-PU reduction unavailable')
    height=c['height'];require(type(height) is int and 4<=height<=12,'bad trace height')
    data,tab=H.I.reciprocity_data(R)
    require(c['q']==data['q'] and c['prime_support']==data['primes'] and c['column_counts']==list(map(len,data['columns'])),'bad trace metadata')
    require(len(c['branches'])==len(data['lows']),'missing low frame')
    for cols,rec in zip(data['lows'],c['branches']):
        require(rec['columns']==list(map(list,cols)),'wrong low frame')
        why=H.I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(rec.get('ordinary')==why,'wrong ordinary obstruction');continue
        if any(v[fam['generator']] or v[fam['inverse_generator']] for v in cols):
            require(rec.get('method')=='low_twist_conflict','wrong low twist conflict');continue
        eps=indicators(R,fam);require([z['indicators'] for z in rec['cases']]==list(map(list,eps)),'omitted FS2 assignment')
        for ep,z in zip(eps,rec['cases']):
            A,b,meta=system(R,data,tab,cols,ep,height,fam,modules)
            require(z['system']==meta,'wrong reconstructed system');check_farkas(A,b,z['ray'])
    return True

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('id');ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=890);ap.add_argument('--height',type=int,default=4);ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==args.id)
    if args.verify:
        c=json.load(open(args.output))['certificate'];verify(R,c);print('EXACT C4 ASSOCIATOR VERIFIED',args.id,flush=True)
    else:
        start=time.monotonic();out={'id':args.id};last=[None]
        def budget(*a):raise TimeoutError('explicit per-input discovery budget reached')
        def progress(*a):last[0]=a;print(json.dumps({'id':args.id,'progress':a}),flush=True)
        signal.signal(signal.SIGALRM,budget);signal.alarm(args.seconds)
        try:out.update(outcome='general_excluded',certificate=certificate(R,args.height,progress))
        except Ineligible as e:out.update(outcome='ineligible',reason=str(e))
        except Survives as e:out.update(outcome='no_exact_obstruction',reason=str(e))
        except TimeoutError as e:out.update(outcome='budget_incomplete',reason=str(e),last_progress=last[0])
        finally:signal.alarm(0)
        out['seconds']=time.monotonic()-start;args.output.write_text(json.dumps(out,separators=(',',':'))+'\n')
        print(json.dumps({k:v for k,v in out.items() if k!='certificate'}),flush=True)
