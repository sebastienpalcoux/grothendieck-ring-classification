import json,sys,time,subprocess,math
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parent;d=json.load(open(P/'enumerate_gram.json'));V=d['vs'];rr=[[Fraction(y) for y in r] for r in d['rref']];piv=d['pivots'];free=d['free'];G=d['b'][:15];diag=[G[j] for j in [0,5,9,12,14]];ub=[min(diag[k]//v[k]**2 for k in range(5) if v[k]) for v in V];co=[[int(i==j) for j in free] for i in range(len(V))];const=[0]*len(V)
for row,i in enumerate(piv):
 if not all(x.denominator==1 for x in rr[row]):raise ValueError('nonintegral RREF')
 const[i]=int(rr[row][-1]);co[i]=[-int(rr[row][j]) for j in free]
order=sorted(range(len(free)),key=lambda j:(ub[free[j]],-sum(abs(c[j]) for c in co)));co=[[c[j] for j in order] for c in co];bounds=[ub[free[j]] for j in order]
inp=' '.join(map(str,[len(free),len(V)]+bounds+ub+const+[c for row in co for c in row]));(P/'profiles_input.txt').write_text(inp+'\n');subprocess.run(['g++','-O3','-std=c++17',str(P/'profiles.cpp'),'-o',str(P/'profiles_engine')],check=True)
st=time.monotonic();out=subprocess.run([str(P/'profiles_engine'),str(P/'profiles_counts.jsonl')],input=inp,text=True,capture_output=True,timeout=790);rec=json.loads(out.stdout);rec.update(seconds=time.monotonic()-st,id='R6_4_629',input='enumerate_gram.json',free_bounds=bounds);(P/'profiles_summary.json').write_text(json.dumps(rec));print(rec)
