#!/usr/bin/env python3
"""Permutation fixed-point bounds and nonnegative mixed fusion traces for R941."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=BASE.parents[1]
ZERO=(F(0),)*4;ONE=(F(1),F(0),F(0),F(0))

def need(ok,msg):
    if not ok:raise ValueError(msg)

def mul(a,b):
    z=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
    return tuple(z)

def inv(a):
    v=ONE
    for s,t in((-1,1),(1,-1),(-1,-1)):v=mul(v,(a[0],s*a[1],t*a[2],s*t*a[3]))
    n=mul(a,v);need(n[0]!=0 and n[1:]==ZERO[1:],'nonzero field norm')
    return tuple(x/n[0]for x in v)

def value(ch,col):return tuple(sum(n*x[k]for n,x in zip(col,ch))for k in range(4))
def weighted(values,weights):return tuple(sum(n*v[k]for n,v in zip(weights,values))for k in range(4))

def actual_control():
    # Actual integer fusion matrices in Z(Ising)=Ising x Ising^rev.
    R=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,1],[0,1,0],[1,0,0]]]
    labels=list(itertools.product(range(3),repeat=2));g=(2,0);dist=[(0,0),(2,2),(1,1)]
    rt=(F(0),F(1),F(0),F(0));S0=[[ONE,rt,ONE],[rt,ZERO,tuple(-x for x in rt)],[ONE,tuple(-x for x in rt),ONE]];dims=[ONE,rt,ONE]
    mats={a:[[R[a[0]][x[0]][y[0]]*R[a[1]][x[1]][y[1]]for x in labels]for y in labels]for a in dist+[g]}
    values=[tuple(mul(mul(S0[a][c],S0[b][d]),inv(mul(dims[c],dims[d])))for a,b in dist)for c,d in labels]
    charges=[mul(mul(S0[2][c],S0[0][d]),inv(mul(dims[c],dims[d])))[0]for c,d in labels]
    need(all(m in(-1,1)for m in charges),'actual fermion charges')
    fixed=sum(mats[g][i][i]for i in range(9));need(fixed==sum(charges)==3,'actual permutation trace equals actual fixed count')
    need(all(charges[i]==-1 for i in range(9)if mats[g][i][i]),'actual fixed objects have negative charge')
    def mm(A,B):return [[sum(A[i][k]*B[k][j]for k in range(9))for j in range(9)]for i in range(9)]
    products={():mats[(0,0)]};eigen={():[ONE]*9};count=0
    for degree in range(7):
        for mon in itertools.combinations_with_replacement((1,2),degree):
            if mon:
                products[mon]=mm(products[mon[:-1]],mats[dist[mon[-1]]])
                eigen[mon]=[mul(x,t[mon[-1]])for x,t in zip(eigen[mon[:-1]],values)]
            for e in(0,1):
                A=products[mon]if not e else mm(mats[g],products[mon]);tr=sum(A[i][i]for i in range(9))
                need(tr>=0 and weighted(eigen[mon],charges if e else [1]*9)==(F(tr),F(0),F(0),F(0)),'actual integer fusion trace equals modular spectrum')
                count+=1
    return {'model':'Z(Ising)','center_rank':9,'actual_fixed_fermion_objects':fixed,'mixed_integer_matrix_trace_identities':count}

def compute():
    folder=BASE/'quartic_integer_center';source=json.loads((folder/'source.json').read_text())['records'][1]
    need(source['id']=='R8_3_941','source identity');chars=[[tuple(map(F,a))for a in ch]for ch in source['full_characters']]
    degrees=source['irreducible_dimensions'];f=[tuple(map(F,a))for a in source['formal_codegrees']];D=f[0]
    columns=[tuple(c)for c in source['low_columns']]+[(0,)+tuple(v)for v in source['canonical_high_vectors']]
    scales=[tuple(x/m for x in mul(D,inv(codegree)))for codegree,m in zip(f,degrees)]
    values=[tuple(mul(mul(scale,value(ch,v)),inv(value(chars[0],v)))for scale,ch in zip(scales,chars))for v in columns]
    joint=json.loads((BASE/'r928_semion_rotation/joint_spectrum.json').read_text())['records'][1]
    need(values==[tuple(tuple(map(F,z))for z in t)for t in joint['low_high_joint_eigenvalue_tuples']],'independent full-S eigenvalue reconstruction')
    need(all(t[0]==ONE for t in values),'unit fusion eigenvalue')
    monos=[()]+[m for k in range(1,7)for m in itertools.combinations_with_replacement(range(1,5),k)]
    products={():[ONE]*70}
    for mon in monos[1:]:products[mon]=[mul(a,t[mon[-1]])for a,t in zip(products[mon[:-1]],values)]
    charges=json.loads((folder/'r941_charges.json').read_text())['solutions'];signs=[1,1,1,1,-1];translated=[40,41,42,43,57];cases=[]
    for at,c in enumerate(charges):
        p=c['plus_pairs'];n=c['minus_individuals'];P=8+2*sum(p);N=2+sum(n);fixed=P-N;minimum=sum(x%2 for x in n);maximum=sum(n)
        bound=minimum<=fixed<=maximum and (fixed-sum(n))%2==0
        first=None
        for e in(0,1):
            w=[q if e else 1 for q in signs]+[2*p[j]+(-n[j]if e else n[j])for j in range(40)]+[0]*25
            for j,q in zip(translated,signs):w[5+j]=q if e else 1
            for mon in monos:
                tr=weighted(products[mon],w)
                if tr[1:]!=ZERO[1:]or tr[0].denominator!=1 or tr[0]<0:
                    first=first or {'central_involution_power':e,'distinguished_factors':list(mon),'trace':list(map(str,tr))}
        cases.append({'allocation_index':at,'pattern_index':c['pattern_index'],'positive_charge_count':P,'negative_charge_count':N,
            'forced_fixed_simple_count':fixed,'minimum_fixed_simples':minimum,'maximum_fixed_simples':maximum,
            'fixed_point_bounds_pass':bound,'first_mixed_trace_failure':first,'passes':bound and first is None})
    surviving=[c['allocation_index']for c in cases if c['passes']];need(len(surviving)==71,'complete trace survivor count')
    paired=json.loads((folder/'r941_paired_rotation.json').read_text());old=[c['metadata']['allocation_index']for c in paired['cases']if c['decision']['status']=='exact_feasible_relaxation']
    retained=[j for j in old if j in surviving];removed=[j for j in old if j not in surviving]
    need(len(retained)==14 and removed==[4,86],'precise intersection with paired survivors')
    integer=json.loads((folder/'r941_integer_counts.json').read_text());integer_good=[];integer_unknown=[]
    for c in integer['cases']:
        j=c['metadata']['allocation_index']
        if j not in retained:continue
        (integer_good if c['result']['status']=='exact_nonnegative_integer_witness'else integer_unknown).append(j)
    need(len(integer_good)==11 and len(integer_unknown)==3,'terminal integer survivor count')
    files=[Path(__file__),folder/'source.json',folder/'r941_charges.json',folder/'r941_paired_rotation.json',folder/'r941_integer_counts.json',BASE/'r928_semion_rotation/joint_spectrum.json',HERE/'r941_fermion_operator_review.json']
    return {'kind':'complete_R941_permutation_and_mixed_fusion_trace_test','status':'exact_complete','complete_charge_allocation_count':len(charges),'actual_center_control':actual_control(),
        'distinguished_monomial_degree_bound':6,'mixed_traces_per_allocation':2*len(monos),'cases':cases,'complete_surviving_allocations':surviving,
        'paired_surviving_allocations':retained,'paired_allocations_removed':removed,
        'retained_exact_integer_witness_allocations':integer_good,'retained_integer_feasibility_unresolved':integer_unknown,
        'scope':'finite necessary test;14 rational and11 integer survivors, not categorifications',
        'files_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=compute();path=HERE/'r941_fusion_traces.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'trace receipt differs')
    print('PASS941 complete fixed-point/mixed-trace gate:71 allocations;14 paired/11 integer survivors')
