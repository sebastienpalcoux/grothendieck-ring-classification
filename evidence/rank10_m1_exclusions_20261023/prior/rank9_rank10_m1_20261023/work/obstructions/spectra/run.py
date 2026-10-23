#!/usr/bin/env python3
"""Exhaustive zero/one-spectrum application to supplied ranks 9 and 10.

C++ search is copied from the pinned project's rank-eight checker, with only
array capacity and rank upper bound increased from 8 to 12. Each found witness
is checked here by direct exact integer arithmetic before acceptance.
"""
import argparse, gzip, hashlib, json, subprocess, time
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[2]

def require(b,msg):
    if not b: raise ValueError(msg)
def fingerprint(R): return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def load():
    out=[]
    for n in (9,10):
        p=ROOT/'inputs'/f'rank{n}_M1_verified'/'FusionRingMultiplicationTables.txt.gz'
        for i,l in enumerate(gzip.open(p,'rt'),1):
            R=json.loads(l.replace('{','[').replace('}',']'))
            out.append({'id':f'R{n}_1_{i}','rank':n,'tensor':R,'tensor_sha256':fingerprint(R)})
    return out

def verify(R,c):
    n=len(R); inds=c['indices']
    require(all(type(i)is int and 0<=i<n for i in inds),'index bounds')
    d=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    dot=lambda i,j,k,l:sum(R[i][j][h]*R[k][l][h] for h in range(n))
    if c['kind']=='zero_spectrum':
        require(len(inds)==9,'nine indices');a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==0,'empty spectrum')
        require(R[b][a][c0]==1,'distinguished multiplicity one')
        require(1 in [dot(v,u,c0,d[a]),dot(b,d[u],c0,d[w]),dot(d[v],b,w,d[a])],'left forced invertible')
        require(1 in [dot(b,x,c0,d[z]),dot(y,d[x],c0,d[a]),dot(d[b],y,a,d[z])],'right forced invertible')
    else:
        require(c['kind']=='one_spectrum' and len(inds)==10,'ten indices');q,a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==1,'equation6.13')
        require(R[u][x][q]==R[d[v]][y][q]==R[w][d[z]][q]==1,'equation6.14')
        require(R[b][a][c0]==0,'equation6.15')
        require(1 in [dot(v,u,y,d[x]),dot(v,q,b,x),dot(b,d[u],y,d[q])],'equation6.16')
        require(1 in [dot(v,q,c0,d[z]),dot(v,w,y,z),dot(y,d[q],c0,d[w])],'equation6.17')
        require(1 in [dot(u,x,w,d[z]),dot(u,a,q,z),dot(q,d[x],w,d[a])],'equation6.18')
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('kind',choices=['zero_spectrum','one_spectrum']);ap.add_argument('--verify-only',action='store_true');a=ap.parse_args();rows=load();out=P/(a.kind+'.json')
    if a.verify_only:
        got=json.loads(out.read_text()); require(len(got['records'])==len(rows),'full inventory')
        for r,w in zip(rows,got['records']):
            require(r['id']==w['id'] and r['tensor_sha256']==w['tensor_sha256'],'identity')
            if w['certificate']:verify(r['tensor'],w['certificate'])
        print('PASS stored exact witnesses',a.kind);return
    name='one_spectrum_m3' if a.kind=='one_spectrum' else a.kind
    src=P/(name+'.cpp');exe=P/name; subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(exe)],check=True)
    values=[len(rows)]
    for r in rows:
        R=r['tensor'];values.append(len(R));values.extend(x for m in R for row in m for x in row)
    start=time.monotonic();proc=subprocess.run([str(exe)],input=' '.join(map(str,values)),capture_output=True,text=True,check=True)
    records=[]
    for j,line in enumerate(proc.stdout.splitlines()):
        nums=list(map(int,line.split()));require(nums[0]==j,'order');r=rows[j];c={'kind':a.kind,'indices':nums[2:]} if nums[1] else None
        if c:verify(r['tensor'],c)
        records.append({k:r[k] for k in ['id','rank','tensor_sha256']}|{'certificate':c,'outcome':'excluded' if c else 'no_conclusion','scope':'general_complex_fusion_category'})
    require(len(records)==len(rows),'all rings searched')
    result={'criterion':a.kind,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-start,'records':records}
    out.write_text(json.dumps(result,indent=2)+'\n');print(a.kind,'seconds',result['elapsed_seconds'],'counts',{n:sum(r['rank']==n and bool(r['certificate']) for r in records) for n in (9,10)},flush=True)
if __name__=='__main__':main()
