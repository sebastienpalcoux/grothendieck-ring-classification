import json,sys,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import round3_m4 as m
from induction import low_failure
from gram_vectors_general import native
R=next(x['N'] for x in json.load(open(P/'data/census.json'))if x['id']=='R6_6_1035');st=time.monotonic()
def stop(*x):raise TimeoutError('budget840')
signal.signal(signal.SIGALRM,stop);signal.alarm(840)
d=m.data_for(R,3,60);print('data',time.monotonic()-st,flush=True)
for ix in [1,3]:
 c=d['lows'][ix];L=m.s.Matrix.hstack(*map(m.s.Matrix,c));G=(d['ch'].C-L*L.T).extract(range(1,6),range(1,6));vv=native(G);print('native',ix,len(vv),time.monotonic()-st,flush=True)
 G,vs=m.high_vectors(d,c);print('arith vectors',ix,len(vs),time.monotonic()-st,flush=True)
 sp=m.Spectrum(d['tab'],c,[(v,None) for v in vs]);print('Spectrum',ix,sp.metadata(),time.monotonic()-st,flush=True)
