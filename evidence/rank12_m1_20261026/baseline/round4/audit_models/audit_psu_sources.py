"""Fresh tensor replay for the ordinary PSU(2)6 rank-eight sources."""
from itertools import product
from pathlib import Path
import json,sys
from audit_liptrap import HERE,FIRST,need
sys.path.insert(0,str(FIRST/'sources/work/rank11'))
import common

def main():
    lower={r['id']:r for r in json.loads((FIRST/'lower_rank8_models.json').read_text())}
    labels=[0,2,4,6]
    B=[[[int(abs(a-b)<=c<=min(a+b,12-a-b) and (a+b-c)%2==0) for c in labels] for b in labels] for a in labels]
    # Full all-module bosonic quotient, using representatives of every free orbit.
    E=list(product(range(4),range(4)));orb=lambda x:(3-x[0],(x[1]+2)%4)
    reps=[];which={}
    for x in E:
        if x in which:continue
        need(orb(x)!=x and orb(orb(x))==x,'free boson involution')
        i=len(reps);reps.append(x);which[x]=which[orb(x)]=i
    need(len(reps)==8,'all free-orbit simples')
    T=[[[0]*8 for _ in reps] for _ in reps]
    for i,(a,b) in enumerate(reps):
        for j,(c,d) in enumerate(reps):
            for e in range(4):T[i][j][which[e,(b+d)%4]]+=B[a][c][e]
    checks=[]
    for rid,M in [('R8_1_6',T)]:
        p=common.based_iso(lower[rid]['tensor'],M);need(p is not None,'boson-orbit tensor binding')
        need(all(lower[rid]['tensor'][a][b][c]==M[p[a]][p[b]][p[c]] for a,b,c in product(range(8),repeat=3)),'all512coefficients')
        checks.append(dict(id=rid,basis_map=p,coefficients=512,actual_source='PSU(2)6 times metric C4; all modules over1+(f,z^2), self-braiding1'))
    # The exceptional actual tensor involution swaps labels2 and4.
    tau=[0,2,1,3];f=3;act=[3,2,1,0]
    need(all(B[a][b][c]==B[tau[a]][tau[b]][tau[c]] for a,b,c in product(range(4),repeat=3)),'fusion action')
    # Aut_tensor(Id)=1 follows directly from x²=1+x+y and xy=f+x+y.
    need(B[1][1]==[1,1,1,0] and B[1][2]==[0,1,1,1],'unique coherent square and central lift')
    for epsilon,rid in [(0,'R8_1_25'),(1,'R8_1_14')]:
        M=[[[0]*8 for _ in range(8)] for _ in range(8)]
        for a,b,i,j,k in product(range(2),range(2),range(4),range(4),range(4)):
            target=act[k] if epsilon*a*b else k
            M[4*a+i][4*b+j][4*((a+b)%2)+target]=B[i][tau[j] if a else j][k]
        p=common.based_iso(lower[rid]['tensor'],M);need(p is not None,'actual extension tensor binding')
        need(all(lower[rid]['tensor'][a][b][c]==M[p[a]][p[b]][p[c]] for a,b,c in product(range(8),repeat=3)),'all512coefficients')
        checks.append(dict(id=rid,basis_map=p,coefficients=512,actual_source='Edie-Michell1709.04721Lemma4.10 tensor involution; unique coherent square; canonical fixed central f; H4(C2,U1)=0 for central twist'))
    out=dict(status='PASS',records=checks)
    (HERE/'psu_source_reaudit.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

if __name__=='__main__':main()
