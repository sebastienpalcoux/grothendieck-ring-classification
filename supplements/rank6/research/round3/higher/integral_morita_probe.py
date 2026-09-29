import sys,json,time,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'));import stabilizer_rotation_higher as H
D=Path(__file__).parent;C={r['id']:r['N']for r in json.load(open(ROOT/'data/census.json'))};out=[]
def end(*a):raise TimeoutError('300-second integer probe budget')
signal.signal(signal.SIGALRM,end);signal.alarm(300)
R=C['R6_5_638'];g=1;fixed,seed,nodes,reps=H.anti_representations(R,g)
profile=json.load(open(D/'morita_profiles.json'))[0]['involutions'][0]['branches']
for ix,b in enumerate(profile):
 if b['method']!='survives':continue
 ab,meta=H.C.morita_system(R,g,fixed,reps[ix]);A,bb=ab;row={'branch':ix,'objects':b['objects'],'meta':meta}
 import sympy as s
 M=s.Matrix(A);red,piv=M.row_join(s.Matrix(bb)).rref();row['rank']=len(piv);row['free']=M.cols-len(piv)
 if row['free']<=0:row['solution']=[str(x)for x in red[:M.cols,-1]]
 out.append(row);(D/'integral_morita_probe.json').write_text(json.dumps(out)+'\n');print(row,flush=True)
