"""Complete integer fermion-charge allocations, with independent full-box replay."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math
import sympy as s
import source,r941_fermionic
HERE=Path(__file__).resolve().parent;need=source.need

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,z):return tuple(x*z for x in a)
def mul(a,b):
    z=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
    return tuple(z)
def value(ch,v):
    z=(F(0),)*4
    for m,a in zip(v,ch):z=add(z,scale(a,m))
    return z

def fixed_contributions(items):
    """Each item is (full character values, actual monodromy, actual twist)."""
    orth=[(F(0),)*4 for _ in items[0][0]];sts=list(orth)
    for values,charge,twist in items:
        for E,z in enumerate(values):
            w=mul(values[0],z)
            orth[E]=add(orth[E],scale(w,charge))
            sts[E]=add(sts[E],scale(w,charge*twist))
    return orth,sts

def data():
    branch=json.loads(json.dumps(r941_fermionic.run(),default=int))
    need(branch==json.loads((HERE/'r941_fermionic.json').read_text()),'fermionic branch source replay')
    row=source.data(941);saved=json.loads((HERE/'source.json').read_text())['records'][1]
    need(row==saved,'complete source replay')
    patterns=json.loads((HERE/'gram_cubic.json').read_text())['patterns'];need(len(patterns)==343,'complete Gram/cubic domain')
    chars=[[[F(z)for z in a]for a in ch]for ch in row['full_characters']]
    low=[[value(ch,v)for ch in chars]for v in row['low_columns']]
    high=[[value(ch,[0]+v)for ch in chars]for v in row['canonical_high_vectors']]
    weights=[[mul(v[0],v[E])for E in range(5)]for v in high]
    items=[]
    for tr in branch['fermionic_branch']['translated_low_twists']:
        i,j,sign=tr['low_index'],tr['high_index'],tr['monodromy']
        items.append((low[i],sign,1));items.append((high[j],sign,tr['forced_twist']))
    constant,_=fixed_contributions(items)
    return row,patterns,weights,constant

def equations(m,weights,constant):
    J=[j for j in range(40)if m[j]>=2];rhs=list(constant)
    for j in range(40):
        for E in range(5):rhs[E]=add(rhs[E],scale(weights[j][E],-m[j]))
    rows=[[4*weights[j][E][k]for j in J]+[-rhs[E][k]]for E in range(5)for k in range(4)]
    integers=[]
    for row in rows:
        den=math.lcm(*(v.denominator for v in row));integers.append([int(v*den)for v in row])
    return J,integers

def run():
    row,patterns,weights,constant=data();records=[];solutions=[];rref_trials=full_trials=0
    for index,m in enumerate(patterns):
        J,rows=equations(m,weights,constant);upper=[m[j]//2 for j in J];rr,p=s.Matrix(rows).rref();local=[];trials=0
        if len(J)not in p:
            free=[j for j in range(len(J))if j not in p]
            for vals in itertools.product(*(range(upper[j]+1)for j in free)):
                trials+=1;v=[s.S.Zero]*len(J)
                for j,z in zip(free,vals):v[j]=s.Integer(z)
                for i,j in enumerate(p):v[j]=rr[i,-1]-sum(rr[i,k]*v[k]for k in free)
                if any(z<0 or z>upper[j]or z.q!=1 for j,z in enumerate(v)):continue
                local.append(tuple(map(int,v)))
        independent=[]
        for v in itertools.product(*(range(u+1)for u in upper)):
            full_trials+=1
            if all(sum(a*z for a,z in zip(r[:-1],v))==r[-1]for r in rows):independent.append(v)
        need(sorted(local)==independent,'independent complete full-box charge search differs')
        rref_trials+=trials
        indices=[]
        for v in independent:
            plus=[0]*40
            for j,z in zip(J,v):plus[j]=z
            need(all(0<=2*p<=m[j]for j,p in enumerate(plus)),'charge pair bounds')
            indices.append(len(solutions));solutions.append({'pattern_index':index,'plus_pairs':plus,
                'minus_individuals':[m[j]-2*plus[j]for j in range(40)]})
        records.append({'pattern_index':index,'nonzero_pair_coordinates':J,'pair_upper_bounds':upper,
            'equations':rows,'rational_rank':len(p),'rref_assignments_tested':trials,
            'independent_full_box_count':math.prod(u+1 for u in upper),'solution_indices':indices})
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],
        'kind':'complete_integer_fermion_monodromy_allocation_domain',
        'input_Gram_cubic_patterns':343,'surviving_pattern_count':len({x['pattern_index']for x in solutions}),'complete_charge_allocation_count':len(solutions),
        'rref_assignments_tested':rref_trials,'independent_full_box_assignments_tested':full_trials,
        'records':records,'solutions':solutions,
        'dependencies':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in
            (HERE/'source.json',HERE/'gram_cubic.json',HERE/'r941_fermionic.json')},
        'scope':'necessary integer monodromy data; charge-plus simples form opposite-twist fermion pairs, charge-minus simples may be fixed; no high restriction column is assigned a charge a priori'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'r941_charges.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete charge receipt changed')
    print('PASS941:',actual['independent_full_box_assignments_tested'],'charge assignments;',actual['complete_charge_allocation_count'],'solutions on',actual['surviving_pattern_count'],'of343 patterns.')
