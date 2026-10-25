"""Integral Gram refinement of the finite relative-trace criterion."""
from higher_traces import *
from native_build import ensure_native
import subprocess,os,time,hashlib,re
from pathlib import Path

class GramSearchBudget(TimeoutError):
    """The exact Gram enumerator explicitly reported incomplete coverage."""
    def __init__(self,seconds,nodes=None,frames=None):
        self.seconds,self.nodes,self.frames=seconds,nodes,frames
        super().__init__(f'integral Gram deadline {seconds}s; nodes={nodes}, partial_frames={frames}; no conclusion')

def frames(Qm,cols,seconds=30):
    n=Qm.rows;ij=list(itertools.combinations_with_replacement(range(n),2));b=[int(Qm[i,j]) for i,j in ij]
    A=[[v[i]*v[j] for i,j in ij] for v,z in cols]
    source=Path(__file__).with_name('gram_frames.cpp');exe=source.with_suffix('')
    ensure_native(source,exe,flags=('-O3', '-std=c++17'))
    inp=f'{len(ij)} {len(cols)} {seconds} '+' '.join(map(str,b+[x for v in A for x in v]))
    try:
        run=subprocess.run([str(exe)],input=inp,text=True,capture_output=True,timeout=seconds+5)
    except subprocess.TimeoutExpired as exc:
        raise GramSearchBudget(seconds+5) from exc
    report=re.fullmatch(r'complete ([01]) nodes (\d+) frames (\d+)\s*',run.stderr)
    if run.returncode==3 and report and report[1]=='0':
        raise GramSearchBudget(seconds,int(report[2]),int(report[3]))
    require(run.returncode==0 and report is not None and report[1]=='1',
            'invalid integral Gram subprocess outcome: '+str(run.returncode)+' '+run.stderr)
    result=sorted(tuple(map(int,l.split())) for l in run.stdout.splitlines())
    for x in result:
        require(len(x)==len(cols) and all(t>=0 for t in x) and all(sum(A[j][i]*x[j] for j in range(len(cols)))==b[i] for i in range(len(b))),'incorrect integral Gram frame')
    return result

def frame_system(A,b,meta,counts):
    # Existing variables (v, trace type) are retained only for used columns.
    labels=meta['labels'];allvs=[]
    for v,ti in labels:
        if not allvs or tuple(v)!=allvs[-1]:allvs.append(tuple(v))
    require(len(allvs)==len(counts),'Gram/high column order mismatch')
    mult=dict(zip(allvs,counts));used=[j for j,(v,ti) in enumerate(labels) if mult[tuple(v)]>0]
    used+=list(range(len(labels),len(A[0])))
    AA=[[row[j] for j in used] for row in A];bb=list(b)
    for v,c in mult.items():
        if c:
            AA.append([int(j<len(labels) and tuple(labels[j][0])==v) for j in used]);bb.append(c)
    return AA,bb

def certificate(R,height=6,seconds=30,limit_frames=5000):
    data=quadratic_data(R,gram_prune=True)
    if data is None:return None
    branches=[]
    for cs in data['lows']:
        branch={'columns':[list(c) for c in cs]};why=low_failure(cs,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:branch['ordinary']=why;branches.append(branch);continue
        L=s.Matrix.hstack(*map(s.Matrix,cs));Qm,cols=high_columns(data,L);ff=frames(Qm,cols,seconds)
        if len(ff)>limit_frames:raise TimeoutError('integral frame count budget')
        branch['frames']=[list(x) for x in ff];branch['indicator_cases']=[]
        for ep in indicator_choices(R):
            A,b,meta=build_system(R,data,L,ep,height);common=farkas(A,b)
            if common:
                branch['indicator_cases'].append({'indicators':list(ep),'common_y':common});continue
            witnesses=[]
            for x in ff:
                AA,bb=frame_system(A,b,meta,x);y=farkas(AA,bb)
                if y is None:return None
                witnesses.append(y)
            branch['indicator_cases'].append({'indicators':list(ep),'ys':witnesses})
        branches.append(branch)
    return {'kind':'integral_gram_traces','height':height,'q':data['q'],'branches':branches}

def verify(R,c):
    data=quadratic_data(R,gram_prune=True);require(data is not None and c['kind']=='integral_gram_traces' and data['q']==c['q'],'invalid integral trace metadata')
    require(len(c['branches'])==len(data['lows']),'missing low branches')
    for cs,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==[list(x) for x in cs],'wrong low columns')
        why=low_failure(cs,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'wrong ordinary failure');continue
        L=s.Matrix.hstack(*map(s.Matrix,cs));Qm,cols=high_columns(data,L);ff=frames(Qm,cols,120)
        require(branch['frames']==list(map(list,ff)),'incomplete integral Gram decompositions')
        eps=indicator_choices(R);cases=branch['indicator_cases'];require([x['indicators'] for x in cases]==list(map(list,eps)),'incomplete indicators')
        for ep,case in zip(eps,cases):
            A,b,meta=build_system(R,data,L,ep,c['height'])
            if 'common_y' in case:check_farkas(A,b,case['common_y']);continue
            require(len(case['ys'])==len(ff),'missing Gram-frame witnesses')
            for x,y in zip(ff,case['ys']):
                AA,bb=frame_system(A,b,meta,x);check_farkas(AA,bb,y)
