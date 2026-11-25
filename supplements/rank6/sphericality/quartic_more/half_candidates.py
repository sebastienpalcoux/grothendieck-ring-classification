"""Eliminate all ten further half-mass fields at trace at most 64."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from verify_quartic_half_ten import moments
from half_bound import CONDUCTORS


def run():
    c=defaultdict(lambda:[0,0,0,0])
    field_lists=[('biquadratic',3,[(*v,64) for v in CONDUCTORS[:-1]]),
                 ('cyclic',7,[(8,48,2,1,1,3,1,64)])]
    for kind,k,field_rows in field_lists:
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp);exe=work/'enumerate';fields=work/'fields';out=work/'elements'
            fields.write_text(''.join(' '.join(map(str,r))+'\n' for r in field_rows))
            subprocess.run(['c++','-O3','-std=c++17',str(HERE/(kind+'.cpp')),'-o',str(exe)],check=True)
            subprocess.run([str(exe),str(fields),str(out)],check=True)
            for line in out.read_text().splitlines():
                row=list(map(int,line.split()))
                poly=(row[k],*row[-3:])
                if any(v%2 for v in poly[:3]) or poly[-1]%2==0:continue
                cs=tuple(row[:3]) if k==3 else (8,48)
                cap=Fraction(7,10) if cs==(8,17,136) else None
                stats=moments(poly,kind,cap)
                for i,v in enumerate((1,*stats)):c[cs][i]+=v
    expected=[(11,2429,3,0),(2,1181,3,0),(0,0,0,0),(1,47,1,0),
              (10,1870,0,0),(4,1261,0,0),(6,1774,0,0),(1,416,0,0),
              (0,0,0,0),(3,1765,0,0)]
    for cs,want in zip(CONDUCTORS,expected):
        assert tuple(c[cs])==want,(cs,c[cs],want)
        print(cs,*c[cs])

if __name__=='__main__':run()
