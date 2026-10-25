"""Liu--Palcoux--Ren zero-spectrum criterion (all characteristics)."""
from rings import *
from native_build import ensure_native
import subprocess,os
from pathlib import Path

def verify(R,c):
    require(c['kind']=='zero_spectrum' and len(c['indices'])==9,'wrong spectrum certificate')
    a,b,c0,u,v,w,x,y,z=c['indices'];du=dual(R);n=len(R);require(all(type(i) is int and 0<=i<n for i in c['indices']),'spectrum indices')
    dot=lambda a,b,c,d:sum(R[a][b][k]*R[c][d][k] for k in range(n))
    require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'zero boundary space')
    require(sum(R[u][x][k]*R[du[v]][y][k]*R[w][du[z]][k] for k in range(n))==0,'spectrum not empty')
    require(R[b][a][c0]==1,'distinguished multiplicity not one')
    require(1 in [dot(v,u,c0,du[a]),dot(b,du[u],c0,du[w]),dot(du[v],b,w,du[a])],'left factor not forced invertible')
    require(1 in [dot(b,x,c0,du[z]),dot(y,du[x],c0,du[a]),dot(du[b],y,a,du[z])],'right factor not forced invertible')

def batch(tensors):
    src=Path(__file__).with_suffix('.cpp');exe=src.with_suffix('')
    ensure_native(src,exe,flags=('-O3', '-std=c++17'))
    values=[len(tensors)]
    for R in tensors:values+=[len(R)]+list(flat(R))
    run=subprocess.run([str(exe)],input=' '.join(map(str,values)),text=True,capture_output=True,check=True,timeout=120)
    out=[]
    for line in run.stdout.splitlines():
        a=list(map(int,line.split()));require(a[0]==len(out),'spectrum output order')
        c={'kind':'zero_spectrum','indices':a[2:]} if a[1] else None
        if c:verify(tensors[len(out)],c)
        out.append(c)
    require(len(out)==len(tensors),'incomplete spectrum scan');return out

if __name__=='__main__':
    import json,time,collections
    P=Path(__file__).resolve().parents[1];rows=json.load(open(P/'data/census.json'));st=time.monotonic();cs=batch([r['N'] for r in rows]);out=[{'id':r['id'],'m':r['m'],'certificate':c} for r,c in zip(rows,cs) if c];(P/'certificates/zero_spectrum.json').write_text(json.dumps(out,separators=(',',':')));print('zero spectrum',len(out),collections.Counter(r['m'] for r in out),'seconds',time.monotonic()-st)
