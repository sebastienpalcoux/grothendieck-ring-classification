"""Complete oriented signed quotients; no commutativity is imposed.

Cyclic trace symmetry and dual reversal are the only coefficient identifications.
"""
import itertools,collections,subprocess,tempfile,math
from pathlib import Path
from rings import *
from signed import from_values,gauge_original

def problem(R):
    n=len(R);require(n<=6 and max(flat(R))<=32,'oriented engine range');du=dual(R)
    def orbit(tri):
        a,b,c=tri;d=(du[c],du[b],du[a]);return sorted({tri,(b,c,a),(c,a,b),d,(d[1],d[2],d[0]),(d[2],d[0],d[1])})
    unseen=set(itertools.product(range(1,n),repeat=3));orbits=[]
    while unseen:
        tri=min(unseen);orb=orbit(tri);unseen.difference_update(orb);orbits.append(orb)
    active=[];mapping={};domains=[]
    for orb in orbits:
        a,b,c=orb[0];bound=R[a][b][du[c]];require(all(R[i][j][du[k]]==bound for i,j,k in orb),'oriented orbit mismatch')
        if not bound:continue
        v=len(active);active.append(orb);domains.append(list(range(-bound,bound+1,2)))
        for i,j,k in orb:mapping[i,j,du[k]]=v
    # Choose the positive-second-indicator lift for every self-dual simple.
    for i in range(1,n):
        if du[i]!=i:continue
        for j in range(1,n):
            bound=R[j][du[j]][i]
            if bound:
                v=mapping[j,du[j],i];domains[v]=[x for x in domains[v] if (bound-x)%4==0]
    sy=s.symbols('v:'+str(len(active)))
    def entry(i,j,k):
        if i==0:return s.Integer(j==k)
        if j==0:return s.Integer(i==k)
        if k==0:return s.Integer(du[i]==j)
        v=mapping.get((i,j,k));return s.S.Zero if v is None else sy[v]
    A=[s.Matrix(n,n,lambda j,k:entry(i,j,k)) for i in range(n)];eqs=set()
    for i in range(1,n):
        for j in range(1,n):
            # Row convention reverses composition of left multiplication.
            diff=A[i]*A[j]-sum((entry(j,i,k)*A[k] for k in range(n)),s.zeros(n))
            for e in diff:
                e=s.expand(e)
                if e:
                    po=s.Poly(e,*sy)
                    if po.LC()<0:po=-po
                    eqs.add(tuple(po.terms()))
    for eq in eqs:
        bound=sum(abs(int(co))*math.prod(max((abs(x) for x in domains[i]),default=0)**power for i,power in enumerate(mon)) for mon,co in eq)
        require(bound<2**62,'oriented polynomial integer range')
    supports=[{i for mon,co in eq for i,k in enumerate(mon) if k} for eq in eqs];order=[];left=set(range(len(active)))
    while left:
        av=[ss&left for ss in supports if ss&left]
        cand=min(av,key=lambda ss:(len(ss),sum(len(domains[i]) for i in ss),sorted(ss))) if av else {min(left)}
        chosen=min(cand,key=lambda i:(len(domains[i]),-sum(i in ss for ss in supports),i));order.append(chosen);left.remove(chosen)
    levels=collections.defaultdict(list);pos={v:i for i,v in enumerate(order)}
    for eq in sorted(eqs):
        ss={i for mon,co in eq for i,k in enumerate(mon) if k}
        text='+'.join('*'.join([str(int(co))]+[f'v[{i}]' for i,power in enumerate(mon) for _ in range(power)]) for mon,co in eq)
        if not ss:require(False,'constant nonzero associativity polynomial')
        levels[max(pos[i] for i in ss)+1].append(text)
    body=['#include <iostream>','#include <vector>','#include <limits>','#include <cstdlib>','using namespace std;',f'long long v[{len(active)}];unsigned long long nodes=0,solutions=0;', 'void dfs(int level){if(nodes==numeric_limits<unsigned long long>::max())exit(9);++nodes;switch(level){']
    for l in sorted(levels):body+=[f'case {l}:']+['if('+e+')return;' for e in levels[l]]+['break;']
    body+=['}switch(level){']
    for l,var in enumerate(order):body.append(f'case {l}:for(int x:vector<int>{{'+','.join(map(str,domains[var]))+f'}}){{v[{var}]=x;dfs(level+1);}}break;')
    body.append(f'case {len(active)}:if(solutions==numeric_limits<unsigned long long>::max())exit(9);++solutions;for(long long x:v)cout<<x<<" ";cout<<"\\n";break;}}}}')
    body.append('int main(){dfs(0);cerr<<"nodes "<<nodes<<" solutions "<<solutions<<"\\n";}')
    return dict(active=active,mapping=mapping,domains=domains,order=order,source='\n'.join(body)+'\n')

def enumerate_all(R,timeout=60):
    p=problem(R)
    with tempfile.TemporaryDirectory() as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(p['source']);subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=timeout)
    vals=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines());return vals,p,run.stderr.strip()

def validate_general(R,nonnegative=False):
    n=len(R);du=dual(R)
    require(all(type(x) is int and (not nonnegative or x>=0) for x in flat(R)),'tensor coefficients')
    require(all(du[du[i]]==i for i in range(n)),'dual involution')
    for i,j,k in itertools.product(range(n),repeat=3):
        require(R[0][i][j]==R[i][0][j]==int(i==j) and R[i][j][0]==int(du[i]==j),'unit')
        require(R[i][j][k]==R[du[i]][k][j]==R[k][du[j]][i]==R[du[j]][du[i]][du[k]],'Frobenius/dual reversal')
    N=matrices(R)
    for i,j in itertools.product(range(n),repeat=2):require(N[i]*N[j]==sum((R[j][i][k]*N[k] for k in range(n)),s.zeros(n)),'oriented associativity')
