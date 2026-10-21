"""Complete joint integer Gram and all distinguished cubic domains."""
from pathlib import Path
import argparse,hashlib,itertools,json,math,subprocess,tempfile
import sympy as s
import source
HERE=Path(__file__).resolve().parent;need=source.need


def make_problem(vectors,Q,cubics):
    count=len(vectors);Q=s.Matrix(Q)
    T=s.Matrix([[0,-1,1,0],[1,0,0,0],[-1,0,-1,1],[0,2,0,-1]])
    need(abs(T.det())==1,'unimodular coordinate change')
    G=T*Q*T.T;transformed=[T*s.Matrix(v)for v in vectors]
    bounds=[min(int(G[j,j])//int(w[j]**2)for j in range(4)if w[j])for w in transformed]
    rows=[[v[i]*v[j]for v in vectors]+[Q[i,j]]for i,j in itertools.combinations_with_replacement(range(4),2)]
    rows += [[s.Rational(c['coefficients'][i][k])for i in range(count)]+[-s.Rational(c['constant'][k])]
             for c in cubics for k in (1,2,3)]
    zeros=set();rounds=[]
    while True:
        matrix=s.Matrix(rows+[[int(i==z)for i in range(count)]+[0]for z in sorted(zeros)])
        rr,piv=matrix.rref();need(count not in piv,'rational necessary equations inconsistent')
        new=set()
        for j in range(len(piv)):
            coeff=list(rr.row(j))
            if not coeff[-1]and all(x>=0 for x in coeff[:-1]):new.update(i for i,x in enumerate(coeff[:-1])if x)
        if new<=zeros:break
        zeros|=new;rounds.append(sorted(zeros))
    free=[j for j in range(count)if j not in piv]
    expression=[None]*count
    for at,j in enumerate(free):expression[j]=(s.S.Zero,[s.Integer(i==at)for i in range(len(free))])
    for row,j in enumerate(piv):expression[j]=(rr[row,count],[-rr[row,k]for k in free])
    inequalities=[]
    def constraint(constant,coefficients,upper,label):
        den=math.lcm(int(constant.q),*(int(x.q)for x in coefficients))
        cc=int(constant*den);aa=[int(x*den)for x in coefficients]
        inequalities.append({'constant':cc,'coefficients':aa,'low':0,'high':int(upper)*den,'modulus':den,'label':label})
    for j in piv:constraint(*expression[j],bounds[j],f'multiplicity_{j}')
    for ci,c in enumerate(cubics):
        coeff=[s.Rational(x[0])for x in c['coefficients']];constant=s.Rational(c['constant'][0])
        constant+=sum(coeff[j]*expression[j][0]for j in range(count))
        linear=[sum(coeff[j]*expression[j][1][k]for j in range(count))for k in range(len(free))]
        maximum=constant+sum(max(0,x)*bounds[j]for x,j in zip(linear,free))
        need(maximum>=0,'cubic has a negative universal upper bound')
        constraint(constant,linear,int(s.floor(maximum)),f'cubic_{ci}')
    upper=[bounds[j]for j in free]
    arithmetic_bound=max(abs(r['constant'])+sum(abs(c)*u for c,u in zip(r['coefficients'],upper))+
                          abs(r['low'])+abs(r['high'])for r in inequalities)
    arithmetic_bound=max(arithmetic_bound,*(abs(x)for r in inequalities
        for x in [r['constant'],r['low'],r['high'],r['modulus'],*r['coefficients']]),*upper)
    need(arithmetic_bound*8<2**62,'native signed64 interval arithmetic bound')
    return {'coordinate_transform':T.tolist(),'transformed_Gram':G.tolist(),'complete_multiplicity_bounds':bounds,
        'rational_equation_rank':len(piv),'forced_zero_rounds':rounds,'free_indices':free,'free_upper_bounds':upper,
        'expressions':[{'constant':str(b),'coefficients':list(map(str,a))}for b,a in expression],
        'constraints':inequalities,'signed64_absolute_intermediate_bound':int(arithmetic_bound*8)}


def enumerate_native(problem):
    cpp=HERE/'enumerate.cpp';fingerprint=hashlib.sha256(cpp.read_bytes()).hexdigest()
    exe=Path(tempfile.gettempdir())/('rank8-quartic-integer-'+fingerprint[:24])
    if not exe.exists():subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True,capture_output=True)
    exe.chmod(exe.stat().st_mode|0o111)
    args=[len(problem['free_indices']),len(problem['constraints'])]+problem['free_upper_bounds']
    for r in problem['constraints']:args += [r['constant'],r['low'],r['high'],r['modulus']]+r['coefficients']
    result=subprocess.run([str(exe)],input=' '.join(map(str,args)),text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def reconstruct(problem,free_values):
    ans=[]
    for e in problem['expressions']:
        x=s.Rational(e['constant'])+sum(s.Rational(a)*v for a,v in zip(e['coefficients'],free_values))
        need(x.q==1 and x>=0,'native result reconstructs a noninteger multiplicity');ans.append(int(x))
    return ans


def enumerate_independent(problem):
    """Python finite-domain filtering; retain holes rather than interval boxes."""
    constraints=problem['constraints'];n=len(problem['free_indices']);solutions=[];nodes=0
    incidences=[[r for r in constraints if r['coefficients'][j]]for j in range(n)]
    def possible(row,domains,assigned=None):
        lo=hi=fixed=row['constant'];g=row['modulus']
        for j,a in enumerate(row['coefficients']):
            if not a:continue
            values=(assigned[1],)if assigned is not None and assigned[0]==j else domains[j]
            lo+=a*(min(values)if a>0 else max(values));hi+=a*(max(values)if a>0 else min(values))
            if len(values)==1:fixed+=a*next(iter(values))
            else:g=math.gcd(g,abs(a))
        return hi>=row['low']and lo<=row['high']and fixed%g==0
    def visit(domains):
        nonlocal nodes
        nodes+=1;domains=list(map(set,domains))
        changed=True
        while changed:
            changed=False
            if any(not possible(r,domains)for r in constraints):return
            for j in range(n):
                if len(domains[j])==1:continue
                values={x for x in domains[j]if all(possible(r,domains,(j,x))for r in incidences[j])}
                if not values:return
                if values!=domains[j]:domains[j]=values;changed=True
        choices=[j for j in range(n)if len(domains[j])>1]
        if not choices:
            candidate=[next(iter(v))for v in domains]
            for r in constraints:
                value=r['constant']+sum(a*v for a,v in zip(r['coefficients'],candidate))
                need(r['low']<=value<=r['high']and value%r['modulus']==0,'independent terminal constraint')
            solutions.append(candidate);return
        at=min(choices,key=lambda j:(len(domains[j]),-j))
        for value in sorted(domains[at]):
            child=domains.copy();child[at]={value};visit(child)
    visit([set(range(u+1))for u in problem['free_upper_bounds']])
    return {'nodes':nodes,'solutions':sorted(solutions)}


def verify_pattern(vectors,Q,cubics,m):
    need(all(sum(z*v[i]*v[j]for z,v in zip(m,vectors))==Q[i][j]for i in range(4)for j in range(4)),'full Gram check')
    values=[]
    for c in cubics:
        value=[s.Rational(c['constant'][k])+sum(z*s.Rational(v[k])for z,v in zip(m,c['coefficients']))for k in range(4)]
        need(value[1:]==[0,0,0]and value[0].q==1 and value[0]>=0,'full distinguished cubic check')
        values.append(int(value[0]))
    return values


def run():
    data=source.run();saved=json.loads((HERE/'source.json').read_text())
    need(json.loads(json.dumps(data,default=int))==saved,'complete exact source replay')
    first,second=data['records']
    need(first['low_cubic_equations']==second['low_cubic_equations'],'same exact20 low cubic equations')
    need(first['dual_high_indices']==second['dual_high_indices']==list(range(65)),'all high columns selfdual')
    problem=make_problem(first['reduced_high_vectors'],first['reduced_Gram'],first['low_cubic_equations'])
    enumeration=enumerate_native(problem);independent=enumerate_independent(problem)
    need(enumeration['solutions']==independent['solutions'],'independent complete finite-domain enumeration differs')
    patterns=[reconstruct(problem,v)for v in enumeration['solutions']]
    values=[verify_pattern(first['reduced_high_vectors'],first['reduced_Gram'],first['low_cubic_equations'],m)for m in patterns]
    return {'kind':'complete_joint_integer_Gram_and_all_twenty_low_cubic_patterns',
        'source_bindings':[{'id':r['id'],'tensor_sha256':r['tensor_sha256']}for r in data['records']],
        'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),
        'cpp_sha256':hashlib.sha256((HERE/'enumerate.cpp').read_bytes()).hexdigest(),
        'problem':problem,'search_nodes':enumeration['nodes'],'independent_Python_nodes':independent['nodes'],
        'complete_joint_pattern_count':len(patterns),
        'patterns':patterns,'all_twenty_cubic_values':values,
        'scope':'complete finite necessary Gram/cubic domain; no categorical center or associator is constructed',
        'outcome':'exact_joint_integer_necessary_patterns_survive'if patterns else'exact_joint_integer_domain_empty'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'gram_cubic.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete Gram/cubic replay differs')
    print('PASS928/941:',actual['complete_joint_pattern_count'],'complete joint integer Gram/cubic patterns.')
