"""Regenerate all quartic ratios for Q(sqrt(3),sqrt(5)) with an irrational complement."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from tempfile import TemporaryDirectory
import json,sys,subprocess
from golden_biquadratic import ordering
from verify_quartic_fields import rows,solve,gap
ROOT=Path(__file__).resolve().parent
CERT=ROOT/'three_five_duals.json'

def census():
    with TemporaryDirectory() as tmp:
        p=Path(tmp)
        (p/'fields').write_text('5 12 60 94\n')
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT.parent/'quartic_more/biquadratic.cpp'),'-o',str(p/'enum')],check=True)
        subprocess.run([str(p/'enum'),str(p/'fields'),str(p/'out')],check=True)
        return [tuple(map(int,l.split())) for l in (p/'out').read_text().splitlines()]

if __name__=='__main__':
    gen='--generate' in sys.argv
    cn=census()
    assert len(cn)==143
    for n in range(1,113):
        for l in range(24,n//2+1,12):
            h=l*l-4*n
            if h>0 and 20*l>9*n and l*l%n==0 and 24*h<=4*n*n and h%12==0:
                assert isqrt(h//12)**2!=h//12
    data=[] if gen else json.loads(CERT.read_text());gaps=[]
    for d,e,f,a,u,v,w,b,c,n in cn:
        order=ordering((d,e,f),(u,v,w))
        for field,t,cap in ((5,F(16,25),64),(0,F(1,2),64),(12,F(11,20),94),(60,F(3,4),24)):
            if a>cap:continue
            R=rows((a,b,c,n),(d,e,f),order,'gold-short' if field==0 else 'gold-long')
            if field:R[2]=([-10**9]*4,-int(t*10**9))
            if gen:data.append(solve(R))
            gaps.append(gap(R,data[len(gaps)]))
    assert len(gaps)==len(data) and min(gaps)>0
    if gen:CERT.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print('143 primitive ratios;',len(gaps),'positive certificates; minimum gap',min(gaps))
