#!/usr/bin/env python3
"""Complete algebra-object necessary filter for seventeen frontier rings.

The noncommutative source convention is transported to the opposite ring
so that the shared engine computes right-multiplication induction Gram.
No candidate object is claimed to admit an associative algebra structure.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import subprocess
import sys
import tempfile
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
QDIR=HERE.parent/'quadratic'
sys.path.insert(0,str(QDIR))
from connected_algebra_candidates import gram,python_psd,python_control,stabilizers_ok

TARGETS=[65,439,455,567,721,901,903,928,941,982,985,1154,1463,1615,1617,1660,1661]
INDEPENDENT_FULL=[65,439,455,567,901,903,928,982,985,1463]


def need(c,m):
    if not c:raise ValueError(m)


def dimensions(index):
    d=(11+5*s.sqrt(5))/2
    if index==65:return [1,1,1,d,d,d,d,1]
    d=3+2*s.sqrt(3)
    if index==439:return [1,1,1,1,d,d,1,1]
    if index==567:return [1,1,1,d,d,1,1,1]
    if index==455:
        d=(3+s.sqrt(13))/2
        return [1,1,1,d,s.sqrt(3),d*s.sqrt(3),d,d]
    if index==721:
        q=s.sqrt(17)
        return [1,(3+q)/2,(3+q)/2,4+q,(5+q)/2,3+q,(5+q)/2,5+q]
    if index==1154:
        a=7+3*s.sqrt(5);b=a-1
        return [1,a,a,1,b,b,a,a]
    a=2+s.sqrt(2)+s.sqrt(3)+s.sqrt(6)
    b=a+s.sqrt(2);c=b+1+s.sqrt(3)
    quartic={903:[1,a,a,c,c,b,1,b],928:[1,a,a,b,b,c,c,1],
             941:[1,b,b,1,a,a,c,c],982:[1,b,b,c,c,a,1,a],
             985:[1,b,b,c,c,1,a,a],1615:[1,1,a,b,c,c,b,a],
             1617:[1,1,a,b,c,c,b,a],1660:[1,1,b,a,c,c,a,b],
             1661:[1,1,b,a,c,c,a,b]}
    if index in quartic:return quartic[index]
    p=(1+s.sqrt(5))/2
    a=(3+s.sqrt(5)+s.sqrt(18+6*s.sqrt(5)))/2
    if index==901:return [1,a,a,p*a,p*a,p,p,1]
    if index==1463:return [1,1,p,a,p*a,p*a,a,p]
    raise ValueError(index)


def run():
    rows={int(r['id'].rsplit('_',1)[1]):r for r in json.loads(
        (REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    cpp=QDIR/'connected_algebra_candidates.cpp'
    hadamard=6**3*400**6
    need(2*hadamard**2<2**127,'signed128 bound')
    records=[]
    with tempfile.TemporaryDirectory(prefix='rank8-structural-algebra-')as temp:
        exe=Path(temp)/'enumerate'
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        for index in TARGETS:
            row=rows[index];R=row['tensor'];dims=list(map(s.sympify,dimensions(index)))
            sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
            need(sha==row['tensor_sha256'],'source hash')
            upper=[int(s.floor(d))for d in dims]
            need(all(u<=d<u+1 and d>0 for u,d in zip(upper,dims)),'exact positive floors')
            need(all(s.simplify(dims[i]*dims[j]-sum(R[i][j][k]*dims[k]for k in range(8)))==0
                for i,j in itertools.product(range(8),repeat=2)),'exact positive dimension homomorphism')
            dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
            # Adjunction Hom(X_i A,X_j A)=Hom(X_i,X_j A) uses RIGHT A.
            # Engine gram uses a_k*input[k][i][j], so transport R to R^op.
            op=[[R[j][i]for j in range(8)]for i in range(8)]
            need(all(op[dual[k]][j][i]==op[k][i][j]
                for i,j,k in itertools.product(range(8),repeat=3)), 'right action dual transpose')
            need(max(v for M in op for line in M for v in line)*sum(upper)<=400,'exact engine bound')
            values=[index]+upper+dual+[v for M in op for line in M for v in line]
            output=subprocess.run([str(exe)],input=' '.join(map(str,values)),capture_output=True,text=True,check=True)
            result=json.loads(output.stdout);survivors=result['necessary_survivor_vectors']
            expected=math.prod(upper[i]+1 for i in range(1,8)if i<=dual[i])
            need(result['bounded_selfdual_vectors_tested']==expected,'complete box count')
            need(len(survivors)==result['PSD_Gram_survivors']==len({tuple(a)for a in survivors}),'survivor count')
            ranks={}
            for a in survivors:
                need(a[0]==1 and all(0<=a[i]<=upper[i]and a[i]==a[dual[i]]for i in range(8)), 'candidate domain')
                need(stabilizers_ok(op,a,dual)and stabilizers_ok(R,a,dual),'left/right invertible stabilization')
                G=gram(op,a)
                need(G==list(map(list,zip(*G)))and all(v>=0 for line in G for v in line),'induction Gram symmetry/positivity')
                ok,rank=python_psd(G);need(ok,'independent rational Schur PSD')
                ranks[str(rank)]=ranks.get(str(rank),0)+1
            # Ten small domains receive a second complete Python search.
            # Every survivor of all seventeen receives independent rational PSD.
            independent=None
            if index in INDEPENDENT_FULL:
                independent=python_control(op,upper,dual)
                need(independent==survivors,'independent complete Python domain')
            result.update({'id':row['id'],'tensor_sha256':sha,
                'exact_fp_dimensions':list(map(str,dims)), 'duality':dual,
                'complete_coefficient_upper_bounds':upper,
                'engine_convention':'opposite_source_tensor; induction Gram is right multiplication by A',
                'independent_rational_PSD_rank_counts':ranks,
                'independent_complete_Python_domain':expected if independent is not None else None,
                'one_plus_simple_surviving_indices':[i for i in range(1,8)if [1]+[int(j==i)for j in range(1,8)]in survivors],
                'scope':'complete finite necessary filter for underlying objects of all connected separable algebras in any complex categorification',
                'limitation':'Surviving objects are not algebra structures; no multiplication, associator, model or general exclusion is claimed.'})
            if index==65:
                modules=json.loads((HERE/'r65_rank_two_modules.json').read_text())
                internal=[a for c in modules['classes']for a in c['internal_end_candidates']]
                need(all(a in survivors for a in internal),'complete rank-two internal ends must survive')
                result['rank_two_internal_end_candidates_retained']=internal
            records.append(result)
    return {'kind':'complete_structural_connected_algebra_object_filter',
            'cpp_source':str(cpp.relative_to(REPO)),
            'cpp_sha256':hashlib.sha256(cpp.read_bytes()).hexdigest(),
            'arithmetic':'exact signed128 Schur/Bareiss with proved entry bound; independent rational PSD on all survivors',
            'exact_max_entry_bound':400,'intermediate_absolute_bound':str(2*hadamard**2),
            'proof':'ALGEBRA_CANDIDATES.md','records':records}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=run();path=HERE/'algebra_candidates.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'saved algebra-object filter changed')
    print('PASS: seventeen complete algebra-object domains; all survivors independently exact PSD; ten full independent Python domains; no associators claimed.')
