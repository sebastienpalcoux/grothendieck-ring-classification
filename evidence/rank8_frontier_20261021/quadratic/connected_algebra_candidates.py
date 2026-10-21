"""Complete underlying-object filter for connected separable algebras.

All complex fusion categorifications are covered; no pivotal or unitary
assumption. Survivors are necessary objects only, NOT algebra structures.
The C++ enumeration uses exact integer arithmetic, independently checked
on all survivors and on the full known-model control domain in Python.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import itertools
import json
import math
import subprocess
import tempfile
import sympy as s
from rank_two_and_models import TARGETS, exact_dimensions, need

HERE=Path(__file__).resolve().parent


def gram(R,a):
    return [[sum(a[k]*R[k][i][j] for k in range(8))-a[i]*a[j] for j in range(8)] for i in range(8)]


def python_psd(G):
    """Independent rational Schur elimination, no fraction-free recurrence."""
    M=[[Fraction(v) for v in row] for row in G]
    rank=0
    while M:
        if any(M[i][i]<0 for i in range(len(M))):return False,rank
        pivot=next((i for i in range(len(M)) if M[i][i]>0),None)
        if pivot is None:return all(v==0 for row in M for v in row),rank
        indices=[i for i in range(len(M)) if i!=pivot]
        M=[[M[i][j]-M[i][pivot]*M[pivot][j]/M[pivot][pivot] for j in indices] for i in indices]
        rank+=1
    return True,rank


def stabilizers_ok(R,a,dual):
    for g in range(1,8):
        if a[g] and R[g][dual[g]]==[1]+[0]*7:
            if any(sum(a[i]*R[g][i][k] for i in range(8))!=a[k] for k in range(8)):return False
    return True


def python_control(R,upper,dual):
    variables=[i for i in range(1,8) if i<=dual[i]]
    survivors=[]
    for values in itertools.product(*(range(upper[i]+1) for i in variables)):
        a=[1]+[0]*7
        for i,v in zip(variables,values):a[i]=a[dual[i]]=v
        if not stabilizers_ok(R,a,dual):continue
        G=gram(R,a)
        if any(v<0 for row in G for v in row):continue
        if python_psd(G)[0]:survivors.append(a)
    return survivors


def run():
    rows={int(r['id'].rsplit('_',1)[1]):r for r in json.loads((HERE.parents[1]/'rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    cpp=HERE/'connected_algebra_candidates.cpp'
    records=[]
    # Proved integer arithmetic bound for the 7-by-7 residual Gram matrix.
    hadamard=6**3*400**6
    need(2*hadamard**2<2**127,'C++ arithmetic bound is not safe')
    modules=json.loads((HERE/'rank_two_and_models_results.json').read_text())
    with tempfile.TemporaryDirectory(prefix='rank8-algebra-') as temp:
        executable=Path(temp)/'enumerate'
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(executable)],check=True,capture_output=True)
        for index in TARGETS+[342]:
            row=rows[index];R=row['tensor']
            dims=list(map(s.sympify,exact_dimensions(index) if index!=342 else [1,1,1,1,1,6,6,1]))
            upper=[int(s.floor(d)) for d in dims]
            need(all(u<=d<u+1 for u,d in zip(upper,dims)),'floor bound incorrect')
            need(all(d>0 for d in dims) and all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k] for k in range(8)))==0
                 for i,j in itertools.product(range(8),repeat=2)),'positive FP homomorphism failed')
            sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
            need(sha==row['tensor_sha256'],'tensor source mismatch')
            dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
            need(all(R[i][j]==R[j][i] for i,j in itertools.product(range(8),repeat=2)),'commutative Gram convention required')
            need(all(R[dual[k]][j][i]==R[k][i][j] for i,j,k in itertools.product(range(8),repeat=3)),
                 'source action transposes fail duality')
            # After entrywise rejection every Gram entry lies in [0,400].
            need(max(v for M in R for line in M for v in line)*sum(upper)<=400,'input exceeds exact C++ bound')
            values=[index]+upper+dual+[v for M in R for line in M for v in line]
            output=subprocess.run([str(executable)],input=' '.join(map(str,values)),text=True,capture_output=True,check=True)
            result=json.loads(output.stdout);survivors=result['necessary_survivor_vectors']
            expected=math.prod(upper[i]+1 for i in range(1,8) if i<=dual[i])
            need(result['bounded_selfdual_vectors_tested']==expected,'finite domain not exhausted')
            need(len(survivors)==result['PSD_Gram_survivors'] and len({tuple(a)for a in survivors})==len(survivors),
                 'survivor count or uniqueness mismatch')
            ranks={}
            for a in survivors:
                need(a[0]==1 and all(0<=a[i]<=upper[i] and a[i]==a[dual[i]] for i in range(8)),
                     'survivor outside domain')
                need(stabilizers_ok(R,a,dual),'survivor violates invertible stabilization')
                G=gram(R,a);need(G==list(map(list,zip(*G))) and all(v>=0 for line in G for v in line),'bad Gram matrix')
                ok,rank=python_psd(G);need(ok,'independent rational PSD verification failed')
                ranks[str(rank)]=ranks.get(str(rank),0)+1
            result.update({'id':row['id'],'tensor_sha256':sha,'exact_fp_dimensions':list(map(str,dims)),
                'complete_coefficient_upper_bounds':upper,'duality':dual,
                'independent_Python_PSD_rank_counts':ranks,
                'scope':'all underlying objects of connected separable algebras pass this necessary filter; survivors need not admit algebra structures',
                'classification_status':'unresolved; no associator or separable algebra is constructed'})
            result['one_plus_simple_surviving_indices']=[i for i in range(1,8)
                if [1]+[int(j==i) for j in range(1,8)] in survivors]
            if index==342:
                independent=python_control(R,upper,dual)
                need(independent==survivors,'independent full known-model control enumeration disagrees')
                need(upper in survivors and gram(R,upper)==[[0]*8 for _ in range(8)],'regular function algebra control failed')
                result['positive_control']={'model':'Rep(C13 semidirect C6)',
                    'algebra':'functions on the group, the regular representation',
                    'regular_algebra_vector':upper,'independent_complete_domain':expected,
                    'classification_status':'known realized model; filter is not an existence criterion'}
            else:
                rowmod=next(r for r in modules['records'] if r['id']==row['id'])
                internal=[a for c in rowmod['rank_two_module_search']['classes'] for a in c['internal_end_candidates']]
                need(all(a in survivors for a in internal),'a rank-two based internal end failed the independent Gram filter')
                result['rank_two_internal_end_candidates_retained']=internal
            records.append(result)
    return {'kind':'complete_connected_separable_algebra_underlying_object_filter',
            'cpp_sha256':hashlib.sha256(cpp.read_bytes()).hexdigest(),
            'arithmetic':'signed128 integer fraction-free PSD; independently rational-verified survivors; full independent control domain',
            'exact_max_entry_bound':400,'intermediate_absolute_bound':str(2*hadamard**2),
            'records':records}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=run();path=HERE/'connected_algebra_candidates_results.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(json.loads(path.read_text())==actual,'connected-algebra evidence did not replay')
    print('PASS: complete connected-algebra underlying-object domains for six residuals and independent positive control')
