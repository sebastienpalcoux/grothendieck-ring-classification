"""Exhaust the FS-normalized signed tables with trace deficit 1080.
Standalone: Python standard library and a C++17 compiler. All checks survive -O.
No tensor, source path, equation list, domain, or completion status is trusted.
The mathematical necessity of this domain is in general_proof_8785.tex.
"""
import collections, hashlib, itertools, json, math, re, subprocess, sys, tempfile, time
from pathlib import Path

def need(condition, message):
    if not condition:
        raise ValueError(message)

def generate(R, deficit=1080):
    need(deficit == 1080, 'the proved exceptional spectrum has deficit 1080')
    need(len(R) == 6 and all(len(A)==6 and all(len(row)==6 for row in A) for A in R), 'rank')
    need(all(type(a) is int and 0<=a<=32 for A in R for row in A for a in row), 'integral bounds')
    need(all(R[0][i][j] == int(i==j) for i,j in itertools.product(range(6),repeat=2)), 'unit')
    need(all(R[i][j][0] == int(i==j) for i,j in itertools.product(range(6),repeat=2)), 'self dual')
    need(all(R[i][j][k] == R[a][b][c] for i,j,k in itertools.product(range(6),repeat=3) for a,b,c in itertools.permutations((i,j,k))), 'total symmetry')
    original_trace=sum(x*x for A in R for row in A for x in row)
    need(original_trace==4325, 'original Casimir trace')
    need(original_trace-deficit==1625+450+1170, 'exceptional Casimir trace')
    triples=list(itertools.combinations_with_replacement(range(1,6),3))
    need(len(triples)==35 and all(R[a][b][c]>0 for a,b,c in triples), 'active triples')
    mapping={q:i for i,tri in enumerate(triples) for q in set(itertools.permutations(tri))}
    domains=[]; weights=[]; bounds=[]
    for tri in triples:
        a,b,c=tri; N=R[a][b][c]; bounds.append(N)
        values=list(range(-N,N+1,2))
        if len(set(tri))<3:
            values=[v for v in values if (N-v)%4==0]
        need(values and max(abs(v) for v in values)<=N, 'domain')
        domains.append(values); weights.append(len(set(itertools.permutations(tri))))
    # An entry is either an integer constant or a single variable index.
    def entry(i,j,k):
        if 0 in (i,j,k):
            return ('c', int((i==0 and j==k) or (j==0 and i==k) or (k==0 and i==j)))
        return ('v', mapping[i,j,k])
    def addproduct(poly, a, b, sign):
        if a[0]=='c' and b[0]=='c':
            mon=(); coefficient=sign*a[1]*b[1]
        elif a[0]=='c':
            mon=(b[1],); coefficient=sign*a[1]
        elif b[0]=='c':
            mon=(a[1],); coefficient=sign*b[1]
        else:
            mon=tuple(sorted((a[1],b[1]))); coefficient=sign
        poly[mon]+=coefficient
    equations=set()
    # Every entry of every commutator of the five nonunit multiplication matrices.
    for i,j in itertools.combinations(range(1,6),2):
        for r,c in itertools.product(range(6),repeat=2):
            poly=collections.defaultdict(int)
            for k in range(6):
                addproduct(poly,entry(i,r,k),entry(j,k,c),1)
                addproduct(poly,entry(j,r,k),entry(i,k,c),-1)
            terms=tuple(sorted((mon,co) for mon,co in poly.items() if co))
            if terms:
                sign=1 if terms[-1][1]>0 else -1
                equations.add(tuple((mon,sign*co) for mon,co in terms))
    equations=sorted(equations)
    supports=[{v for mon,co in eq for v in mon} for eq in equations]
    order=[]; left=set(range(35))
    while left:
        available=[ss & left for ss in supports if ss & left]
        candidate=min(available,key=lambda ss:(len(ss),sum(len(domains[i]) for i in ss),sorted(ss))) if available else {min(left)}
        chosen=min(candidate,key=lambda i:(len(domains[i]),-sum(i in ss for ss in supports),i))
        order.append(chosen); left.remove(chosen)
    position={v:i for i,v in enumerate(order)}
    levels=collections.defaultdict(list)
    polynomial_bound=0
    for eq,ss in zip(equations,supports):
        bound=sum(abs(co)*math.prod(bounds[i] for i in mon) for mon,co in eq)
        polynomial_bound=max(polynomial_bound,bound)
        need(bound<2**62, 'native arithmetic overflow bound')
        need(ss, 'constant nonzero associativity equation')
        expr='+'.join('*'.join([str(co)]+[f'v[{i}]' for i in mon]) for mon,co in eq)
        levels[max(position[i] for i in ss)+1].append(expr)
    need(sum(weights[i]*bounds[i]**2 for i in range(35))<2**30, 'native deficit overflow bound')
    code=['#include <iostream>','#include <vector>','#include <limits>','#include <cstdlib>',
          'using namespace std;','long long v[35]; unsigned long long nodes=0, solutions=0;',
          'void dfs(int level,int cost){if(cost>1080)return;if(nodes==numeric_limits<unsigned long long>::max())exit(9);++nodes; switch(level){']
    for level in sorted(levels):
        code.append(f'case {level}:')
        code.extend('if('+e+')return;' for e in levels[level]);code.append('break;')
    code.append('} switch(level){')
    for level,var in enumerate(order):
        code.append(f'case {level}: for(int x:vector<int>{{'+','.join(map(str,domains[var]))+f'}}){{v[{var}]=x;dfs(level+1,cost+{weights[var]}*({bounds[var]**2}-x*x));}} break;')
    code.append('case 35: if(cost!=1080)return; if(solutions==numeric_limits<unsigned long long>::max())exit(9); ++solutions; for(long long x:v)cout<<x<<" ";cout<<"\\n";break;}}')
    code.append('int main(){dfs(0,0);cerr<<"nodes "<<nodes<<" solutions "<<solutions<<"\\n";}')
    source='\n'.join(code)+'\n'
    metadata={'variables':35,'equations':len(equations),'domains':domains,'order':order,'weights':weights,'polynomial_bound':polynomial_bound,'trace_deficit':deficit,'signed_trace':original_trace-deficit}
    return source, metadata

def run(path=None, deficit=1080, timeout=600):
    st=time.monotonic();path=Path(path) if path else Path(__file__).with_name('tensor_8785.json')
    R=next(r['N'] for r in json.load(open(path)) if r['id']=='R6_9_8785')
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(digest=='7897af45c48cb1d416710f37ea9c4c11226490421317d193c85e3cc5022b3da8','tensor SHA256')
    source, metadata=generate(R,deficit)
    with tempfile.TemporaryDirectory() as td:
        cpp=Path(td)/'enum.cpp';exe=Path(td)/'enum';cpp.write_text(source)
        build=subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],capture_output=True,text=True)
        need(build.returncode==0,'compiler failed: '+build.stderr)
        result=subprocess.run([str(exe)],capture_output=True,text=True,timeout=timeout)
        need(result.returncode==0,'enumeration did not complete successfully')
        match=re.fullmatch(r'nodes ([0-9]+) solutions ([0-9]+)\n',result.stderr)
        need(match is not None,'missing native completion report')
        nodes,solutions=map(int,match.groups())
        need(nodes>0,'missing search')
        need(solutions==0 and result.stdout=='','signed table survives')
    return {'id':'R6_9_8785','tensor_sha256':digest,'scope':'complete FS-normalized signed tables at exceptional trace 3245','complete':True,'nodes':nodes,'solutions':solutions,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),**metadata,'seconds':time.monotonic()-st}
if __name__=='__main__':
    print(json.dumps(run(sys.argv[1] if len(sys.argv)>1 else None),indent=2))
