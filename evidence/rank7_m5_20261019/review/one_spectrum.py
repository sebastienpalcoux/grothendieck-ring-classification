"""Exact one-spectrum certificates, TPE arXiv:2203.06522v5, Theorem 6.8.

Only the complex fusion-category application is claimed in this release.
No pivotal, spherical, pseudo-unitary, or unitary assumption is made.
"""
import argparse, collections, gzip, hashlib, json, subprocess, time
from pathlib import Path

HERE=Path(__file__).resolve().parent

def verify(R,certificate):
    if certificate.get('kind')!='one_spectrum':raise ValueError('wrong kind')
    indices=certificate['indices'];n=len(R)
    if len(indices)!=10 or any(type(i) is not int or not 0<=i<n for i in indices):raise ValueError('indices')
    p,a,b,c,u,v,w,x,y,z=indices
    dual=[]
    for i in range(n):
        hits=[j for j in range(n) if R[i][j][0]]
        if len(hits)!=1 or R[i][hits[0]][0]!=1:raise ValueError('duality')
        dual.append(hits[0])
    def dot(a,b,c,d):return sum(R[a][b][k]*R[c][d][k] for k in range(n))
    if not all((R[u][a][w],R[v][u][b],R[v][w][c],R[x][z][a],R[b][x][y],R[y][z][c])):raise ValueError('boundary')
    if sum(R[u][x][k]*R[dual[v]][y][k]*R[w][dual[z]][k] for k in range(n))!=1:raise ValueError('6.13')
    if (R[u][x][p],R[dual[v]][y][p],R[w][dual[z]][p])!=(1,1,1):raise ValueError('6.14')
    if R[b][a][c]!=0:raise ValueError('6.15')
    if 1 not in (dot(v,p,b,x),dot(v,u,y,dual[x]),dot(b,dual[u],y,dual[p])):raise ValueError('6.16')
    if 1 not in (dot(v,w,y,z),dot(v,p,c,dual[z]),dot(y,dual[p],c,dual[w])):raise ValueError('6.17')
    if 1 not in (dot(u,a,p,z),dot(u,x,w,dual[z]),dot(p,dual[x],w,dual[a])):raise ValueError('6.18')
    return True

def batch(tensors):
    executable=HERE/'one_spectrum'
    subprocess.run(['g++','-O3','-std=c++17',str(HERE/'one_spectrum.cpp'),'-o',str(executable)],check=True)
    values=[len(tensors)]
    for R in tensors:values.extend([len(R)]+[x for M in R for row in M for x in row])
    run=subprocess.run([str(executable)],input=' '.join(map(str,values)),text=True,capture_output=True,check=True)
    result=[]
    for line in run.stdout.splitlines():
        v=list(map(int,line.split()))
        if v[0]!=len(result):raise ValueError('output ordering')
        c={'kind':'one_spectrum','indices':v[2:]} if v[1] else None
        if c:verify(tensors[len(result)],c)
        result.append(c)
    if len(result)!=len(tensors):raise ValueError('incomplete scan')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--minimum-m',type=int,default=5);ap.add_argument('--output',default=str(HERE/'one_spectrum_results.json'));args=ap.parse_args()
    source=Path(args.source);counts=collections.Counter();rows=[]
    with gzip.open(source,'rt') as f:
        for line_no,line in enumerate(f,1):
            R=json.loads(line.replace('{','[').replace('}',']'));m=max(x for M in R for row in M for x in row);counts[m]+=1
            if m>=args.minimum_m:rows.append({'id':f'R7_{m}_{counts[m]}','source_line':line_no,'tensor':R})
    start=time.monotonic();certs=batch([r['tensor'] for r in rows]);out=[]
    for row,c in zip(rows,certs):
        if c:out.append({'id':row['id'],'source_line':row['source_line'],'certificate':c})
    report={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'minimum_m':args.minimum_m,'tested':len(rows),'excluded':len(out),'seconds':time.monotonic()-start,'scope':'general complex fusion categories','reference':'arXiv:2203.06522v5 Theorem 6.8','certificates':out}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='certificates'},indent=2))

if __name__=='__main__':main()
