#!/usr/bin/env python3
"""Independent 10-fixed-object charge constants and every fermion operator column."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
sys.path.insert(0,str(BASE/'quartic_integer_center'))
import r941_paired_rotation as producer
from fermion_center_control import compute as model_control

def need(ok,msg):
    if not ok:raise ValueError(msg)

def mul(a,b):
    z=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
    return tuple(z)

def value(ch,v):return tuple(sum(F(n)*a[k]for n,a in zip(v,ch))for k in range(4))
def total(vs):
    vs=list(vs);return tuple(sum(v[k]for v in vs)for k in range(4))
def scale(c,v):return tuple(c*x for x in v)

def compute():
    folder=BASE/'quartic_integer_center';r=json.loads((folder/'source.json').read_text())['records'][1]
    chars=[[tuple(F(x)for x in a)for a in ch]for ch in r['full_characters']];R=r['tensor'];g=3
    lows=list(map(tuple,r['low_columns']));highs=[(0,)+tuple(v)for v in r['canonical_high_vectors']];D=tuple(F(v)for v in r['formal_codegrees'][0])
    weights=lambda v:[mul(value(chars[0],v),value(ch,v))for ch in chars]
    q=[int(chars[E][g][0]/r['irreducible_dimensions'][E])for E in range(5)]
    need(q==[1,1,1,1,-1],'distinguished monodromy including matrix multiplicity')
    perm=[R[g][i].index(1)for i in range(8)]
    translated=[];fixed=[]
    for E,v in enumerate(lows):
        w=tuple(sum(v[i]*R[g][i][j]for i in range(8))for j in range(8));j=highs.index(w);translated.append(j)
        fixed.append({'vector':v,'charge':q[E],'twist':1,'weights':weights(v)})
        fixed.append({'vector':w,'charge':q[E],'twist':-q[E],'weights':weights(w)})
    need(translated==[40,41,42,43,57],'translated low vectors')
    orth=[total(scale(z['charge'],z['weights'][E])for z in fixed)for E in range(5)]
    sts=[total(scale(z['charge']*z['twist'],z['weights'][E])for z in fixed)for E in range(5)]
    target=[total([scale(-1,mul(D,chars[E][g])),scale(-1,sts[E])])for E in range(5)]
    need(orth[4]==(0,)*4 and target[4]==(0,)*4,'matrix-character fixed contribution makes both extra rows tautologies')
    w=[weights(v)for v in highs[:40]];patterns=json.loads((folder/'gram_cubic.json').read_text())['patterns'];solutions=[];trials=0
    for pi,m in enumerate(patterns):
        J=[j for j in range(40)if m[j]>=2]
        # Full independent finite box; coefficients come from all ten explicit
        # fixed restrictions, not a simplified low-row constant identity.
        rhs=[sum(m[j]*w[j][E][k]for j in range(40))-orth[E][k]for E in range(5)for k in range(4)]
        rows=[[4*w[j][E][k]for j in J]for E in range(5)for k in range(4)]
        nonzero=[(row,b)for row,b in zip(rows,rhs)if any(row)or b]
        for p in itertools.product(*(range(m[j]//2+1)for j in J)):
            trials+=1
            if not all(sum(a*x for a,x in zip(row,p))==b for row,b in nonzero):continue
            plus=[0]*40
            for j,x in zip(J,p):plus[j]=x
            solutions.append({'pattern_index':pi,'plus_pairs':plus,'minus_individuals':[m[j]-2*plus[j]for j in range(40)]})
    charge=json.loads((folder/'r941_charges.json').read_text());need(solutions==charge['solutions'],'complete independent charge allocation equality')
    need(trials==41664 and len(solutions)==93,'complete finite charge domain')
    columns,b,labels,charges,meta=producer.setup();need(charges['solutions']==solutions,'operator uses independently checked domain')
    rot=producer.rotation;mod=producer.modular;rot.install();a=rot.bq.data(R);cols=a['lows'][0];ep=(0,0,1,1,1,1,1)
    A0,b0,m0=rot.bq.system(R,a,cols,ep,6);A0,b0,m0=mod.append_sts(R,a,cols,(0,1,2,3,4),A0,b0,m0,6)
    old=list(zip(*A0));types,_=rot.bq.trace_types(6);nt=len(types);order=r['original_high_order'];original_rows=len(b0)
    for j,theta in zip(translated,[-1,-1,-1,-1,1]):
        tt=tuple((F(theta**k),F(0),F(0),F(0))for k in range(1,7));ti=types.index(tt)
        b0=[x-y for x,y in zip(b0,old[order[j]*nt+ti])]
    rawtarget=[x for t in target for x in t];coeff={}
    for j in range(40):
        for ti,tt in enumerate(types):coeff[j,ti]=[x for E in range(5)for x in scale(-1,mul(w[j][E],tt[0]))]
    den=[math.lcm(rawtarget[k].denominator,*(z[k].denominator for z in coeff.values()))for k in range(20)]
    expected_rhs=b0+[int(x*d)for x,d in zip(rawtarget,den)]+[0]*80
    need(b==expected_rhs,'all fixed RHS contributions including the matrix row')
    pairtypes=set();counts={}
    for col,label in zip(columns,labels):
        kind,j,ti=label;mass=[0]*80;extra=[0]*20
        if kind=='rotation_auxiliary':expected=list(old[j])
        elif kind=='minus_individual':
            expected=list(old[order[j]*nt+ti]);extra=[int(x*d)for x,d in zip(coeff[j,ti],den)];mass[40+j]=1
        else:
            need(kind=='plus_pair','known operator column kind')
            neg=tuple(tuple((-1 if k%2==0 else 1)*x for x in row)for k,row in enumerate(types[ti]));tj=types.index(neg)
            pair=tuple(tuple(x+y for x,y in zip(row,other))for row,other in zip(types[ti],types[tj]));pairtypes.add(pair)
            need(not any(pair[0]),'opposite pair first trace vanishes')
            expected=[x+y for x,y in zip(old[order[j]*nt+ti],old[order[j]*nt+tj])];mass[j]=1
        need(list(col)==expected+extra+mass,'every complete operator column independently reconstructed')
        counts[kind]=counts.get(kind,0)+1
    for i in range(93):
        A,bb,mm=producer.build((columns,b,labels,charges,meta),i);case=solutions[i]
        need(bb==b[:-80]+case['plus_pairs']+case['minus_individuals'],'every charge RHS')
        selected=[j for j,(kind,v,ti)in enumerate(labels)if kind=='rotation_auxiliary'or(case['plus_pairs'][v]>0 if kind=='plus_pair'else case['minus_individuals'][v]>0)]
        need(mm['selected_universal_columns']==selected and A==[list(v)for v in zip(*(columns[j]for j in selected))],'every zero-bound column removal')
    files=[Path(__file__),HERE/'fermion_center_control.py',HERE/'quartic_central_orbits.json']+[folder/f for f in('source.json','gram_cubic.json','r941_fermionic.py','r941_fermionic.json','r941_charges.py','r941_charges.json','r941_paired_rotation.py')]
    return {'kind':'independent_R941_fermion_operator_review','complete_box_assignments':trials,'complete_charge_allocations':len(solutions),
        'fixed_object_count':10,'fixed_orthogonality_contributions':[[str(v)for v in z]for z in orth],
        'fixed_STS_contributions':[[str(v)for v in z]for z in sts],'remaining_G_STS_rhs':[[str(v)for v in z]for z in target],
        'matrix_character_remaining_rows_are_zero':True,'universal_rows':len(b),'universal_columns':len(columns),'column_kinds':counts,
        'opposite_pair_trace_types':len(pairtypes),'all93_selected_operators_checked':True,'actual_model_control':model_control(),
        'scope':'complete domain and necessary operator review; numerical/exact branch decisions are a separate campaign',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=json.loads(json.dumps(compute()));path=HERE/'r941_fermion_operator_review.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'fermion operator review receipt differs')
    print('PASS941 independent ten-object constants,41664charge boxes,93allocations,allG/pair columns andactualZIsingcontrol')
