"""Complete bounded signed-table enumeration, with certified sign gauges.

Only commutative signed quotients are enumerated. The manuscript explains
why commutativity is necessary in each application where completeness is used.
"""
import itertools, collections, subprocess, tempfile, json, math
from pathlib import Path
from rings import *

def signed_problem(R,adjoint_parity=False,positive_indicators=False):
    n=len(R);require(n==5 and max(abs(x) for x in flat(R))<=32,'signed engine supports rank five through bound 32');du=dual(R);triples=list(itertools.combinations_with_replacement(range(1,n),3))
    unseen=set(triples);orbits=[]
    while unseen:
        q=min(unseen);qd=tuple(sorted(du[i] for i in q));orb=sorted({q,qd})
        unseen.difference_update(orb);orbits.append(orb)
    active=[];mapping={};domains=[];gauges=[];pivots={}
    pair={i:min(i,du[i]) for i in range(1,n)}
    for orb in orbits:
        a,b,c=orb[0];bound=R[a][b][du[c]]
        require(all(R[i][j][du[k]]==bound for tri in orb for i,j,k in itertools.permutations(tri)),'orbit bounds disagree')
        if not bound:continue
        mask=0
        for i in (a,b,c):mask^=1<<(pair[i]-1)
        residue=mask
        for bit in sorted(pivots,reverse=True):
            if residue&(1<<bit):residue^=pivots[bit]
        normalize=bool(bound%2 and residue and not positive_indicators)
        if normalize:pivots[residue.bit_length()-1]=residue
        values=list(range(1 if normalize else -bound,bound+1,2))
        v=len(active);active.append(orb);domains.append(values)
        if normalize:gauges.append({'variable':v,'mask':mask})
        for tri in orb:
            for i,j,k in itertools.permutations(tri):mapping[i,j,du[k]]=v
    parity_groups=[]
    if adjoint_parity or positive_indicators:
        for i in range(1,n):
            if du[i]!=i:continue
            odd=[]
            for j in range(1,n):
                bound=R[j][du[j]][i]
                if not bound:continue
                v=mapping[j,du[j],i]
                if bound%2 and not positive_indicators:odd.append((v,bound%4))
                else:domains[v]=[x for x in domains[v] if (bound-x)%4==0]
            parity_groups.append(sorted(set(odd)))
    sy=s.symbols('v:'+str(len(active)))
    def entry(i,j,k):
        if i==0:return s.Integer(j==k)
        if j==0:return s.Integer(i==k)
        if k==0:return s.Integer(du[i]==j)
        v=mapping.get((i,j,k));return s.S.Zero if v is None else sy[v]
    A=[s.Matrix(n,n,lambda j,k:entry(i,j,k)) for i in range(n)]
    eqs=set()
    for i in range(1,n):
        for j in range(i+1,n):
            for e in A[i]*A[j]-A[j]*A[i]:
                e=s.expand(e)
                if e:
                    po=s.Poly(e,*sy)
                    if po.LC()<0:po=-po
                    eqs.add(tuple(po.terms()))
    # Bound every polynomial evaluation before selecting the native backend.
    for eq in eqs:
        bound=sum(abs(int(co))*math.prod(max(abs(x) for x in domains[i])**power for i,power in enumerate(mon)) for mon,co in eq)
        require(bound<2**62,'native signed polynomial accumulator range')
    # Put variables completing the sparsest equations first, avoiding a
    # blind enumeration of the entire rectangular coefficient box.
    supports=[{i for mon,co in eq for i,k in enumerate(mon) if k} for eq in eqs]
    order=[];left=set(range(len(active)))
    while left:
        available=[ss&left for ss in supports if ss&left]
        candidate=min(available,key=lambda ss:(len(ss),sum(len(domains[i]) for i in ss),sorted(ss))) if available else {min(left)}
        chosen=min(candidate,key=lambda i:(len(domains[i]),-sum(i in ss for ss in supports),i))
        order.append(chosen);left.remove(chosen)
    levels=collections.defaultdict(list);pos={v:i for i,v in enumerate(order)}
    def expression(eq):
        terms=[]
        for mon,co in eq:
            factors=[str(int(co))]+[f'v[{i}]' for i,p in enumerate(mon) for _ in range(p)]
            terms.append('*'.join(factors))
        return '+'.join(terms)
    for eq,ss in zip(sorted(eqs),[{i for mon,co in eq for i,k in enumerate(mon) if k} for eq in sorted(eqs)]):
        levels[max(pos[i] for i in ss)+1].append(expression(eq))
    for group in parity_groups:
        for (v,a),(w,b) in itertools.combinations(group,2):
            levels[max(pos[v],pos[w])+1].append(f'(({a}*v[{v}]-{b}*v[{w}])%4)')
    body=['#include <iostream>','#include <vector>','#include <limits>','#include <cstdlib>','using namespace std;',f'long long v[{len(active)}]; unsigned long long nodes=0,solutions=0;',
          'void dfs(int level){if(nodes==numeric_limits<unsigned long long>::max())exit(9);++nodes; switch(level){']
    for level in sorted(levels):
        body.append(f'case {level}:')
        body.extend('if('+e+')return;' for e in levels[level]);body.append('break;')
    body.append('} switch(level){')
    for level,var in enumerate(order):
        body.append(f'case {level}: for(int x:vector<int>{{'+','.join(map(str,domains[var]))+f'}}){{v[{var}]=x;dfs(level+1);}} break;')
    body.append(f'case {len(active)}: if(solutions==numeric_limits<unsigned long long>::max())exit(9); ++solutions; for(long long x:v)cout<<x<<" ";cout<<"\\n";break;}}}}')
    body.append('int main(){dfs(0);cerr<<"nodes "<<nodes<<" solutions "<<solutions<<"\\n";}')
    return {'active':active,'mapping':mapping,'domains':domains,'gauges':gauges,'order':order,'source':'\n'.join(body)+'\n'}

def from_values(R,problem,values):
    n=len(R);du=dual(R)
    A=[[[int(j==k) if i==0 else int(i==k) if j==0 else int(du[i]==j) if k==0 else 0 for k in range(n)] for j in range(n)] for i in range(n)]
    for (i,j,k),v in problem['mapping'].items():A[i][j][k]=values[v]
    return A

def enumerate_signed(R,timeout=120,adjoint_parity=False,positive_indicators=False):
    p=signed_problem(R,adjoint_parity=adjoint_parity,positive_indicators=positive_indicators)
    with tempfile.TemporaryDirectory() as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(p['source'])
        subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True,capture_output=True)
        run=subprocess.run([str(exe)],capture_output=True,text=True,check=True,timeout=timeout)
    vals=sorted(tuple(map(int,line.split())) for line in run.stdout.splitlines())
    return vals,p,run.stderr.strip()

def gauge_original(T,R):
    n=len(R);du=dual(R)
    for tail in itertools.product((-1,1),repeat=n-1):
        signs=(1,)+tail
        if any(signs[i]!=signs[du[i]] for i in range(n)):continue
        if all(T[i][j][k]==signs[i]*signs[j]*signs[k]*R[i][j][k] for i,j,k in itertools.product(range(n),repeat=3)):return list(signs)
    return None
