"""Independent exhaustive dimension-compatible character assignments for R901.

Enumerates full bijections by dimension blocks before testing S symmetry;
it does not use Table.assignments or its recursive S pruning. The known
complex model control has an explicitly supplied symmetric low frame.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,subprocess,tempfile
import sympy as s
import octic_low_s_general as general
from octic_complex_character_table import OcticTable
from rank_two_and_models import need
st=general.st;low=general.preflight.low;HERE=Path(__file__).resolve().parent


def value_key(v):return tuple(map(str,v.to_list()))


def labelings(columns,T):
    K=T.K;positions={};labels={}
    for i,c in enumerate(columns):
        d=sum((K(n)*x for n,x in zip(c,T.ds)),K.zero);positions.setdefault(value_key(d),[]).append(i)
    for E,beta in enumerate(T.beta):labels.setdefault(value_key(beta),[]).append(E)
    if set(positions)!=set(labels)or any(len(positions[k])!=len(labels[k])for k in positions):return
    keys=sorted(positions)
    for selections in itertools.product(*(itertools.permutations(labels[k])for k in keys)):
        assignment=[None]*8
        for k,selection in zip(keys,selections):
            for position,E in zip(positions[k],selection):assignment[position]=E
        yield assignment


def symmetry_audit(frames,T):
    K=T.K;cache={};count=0;surviving=[];distribution={};failures=hashlib.sha256()
    for index,columns in enumerate(frames):
        columns=list(map(tuple,columns))
        for c in columns:
            if c not in cache:cache[c]=[beta*sum((K(n)*v for n,v in zip(c,row)),K.zero)
                                       for beta,row in zip(T.beta,T.characters)]
        local=0
        for assignment in labelings(columns,T):
            count+=1;local+=1;bad=None
            for i,j in itertools.combinations(range(8),2):
                E,F=assignment[i],assignment[j]
                if cache[columns[j]][E]!=cache[columns[i]][F]:bad=[i,j];break
            if bad is None:surviving.append([index,assignment])
            failures.update((json.dumps([index,assignment,bad],separators=(',',':'))+'\n').encode())
        distribution[local]=distribution.get(local,0)+1
    return {'complete_dimension_compatible_bijections':count,
            'bijection_count_distribution':{str(k):v for k,v in sorted(distribution.items())},
            'surviving_symmetric_labelings':surviving,'first_failed_pair_records_sha256':failures.hexdigest()}


def known_control():
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):R[i][j][4*z+(g+k)%4]+=1
    data={'field':{'radicands':[3,5]},'dimensions':[[1,0,0,0]]*4+[[s.Rational(1,2),0,s.Rational(1,2),0]]*4,
          'global_dimension':[10,0,2,0]}
    T=OcticTable(R,data);unit=[1]+[0]*7;both=[1,0,0,0,1,0,0,0]
    result=symmetry_audit([[unit]*4+[both]*4],T)
    need(result['surviving_symmetric_labelings'],'known complex model has no symmetric low frame')
    return {'model':'Fibonacci tensor Vec(C4)','tensor_sha256':st.digest(R),**result}


def run():
    source=st.load_ring('R8_3_901');R=source['tensor'];a=low.data(R);T=OcticTable(R,a)
    import low_frames_rank8 as native
    cpp=st.BASE/'performance/low_frames_rank8.cpp'
    with tempfile.TemporaryDirectory(prefix='independent-octic-frames-')as tmp:
        exe=Path(tmp)/'frames';subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        native.executable=lambda:exe;frames=native.low_matrices(a['columns'],a['B'],gram_prune=True)
    audit=symmetry_audit(frames,T)
    need(len(frames)==2024 and not audit['surviving_symmetric_labelings'],'complete raw low-S obstruction failed')
    path=HERE/'octic_low_s_general_results.json';record=json.loads(path.read_text());general.verify(source,record)
    g=record['certificate']['general']
    return {'kind':'independent_unpruned_octic_low_S_assignment_review','result':'PASS',
            'id':source['id'],'tensor_sha256':source['tensor_sha256'],'complete_frames':len(frames),
            'frame_sha256':st.digest(frames),'assignment_audit':audit,'known_complex_control':known_control(),
            'general_certificate_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'general_certificate_replay':'PASS','spherical_alternatives':g['sphere']['characters'],
            'signed_branch_count':len(g['branches']),'signed_obstructions':[b.get('obstruction')for b in g['branches']],
            'scope':'general_complex_fusion_category',
            'sources':{str(p.relative_to(HERE.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in[cpp,Path(native.__file__),HERE/'octic_low_s_general.py',HERE/'octic_low_s_symmetry.py',
                                 HERE/'octic_complex_character_table.py']}}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=run();result=json.loads(json.dumps(result,default=int));path=HERE/'review_octic_low_s_results.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'independent octic low-S receipt changed')
    print('PASS:901 independent complete unpruned character assignments and general lift',flush=True)
