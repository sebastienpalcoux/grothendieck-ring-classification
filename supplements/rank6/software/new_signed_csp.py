"""Unrestricted commutative signed search with exact quadratic propagation.

Uses only the certified dual-compatible sign gauges of signed.signed_problem.
No second-indicator or modulo-four restrictions are introduced.
"""
import os,re,subprocess
from pathlib import Path
from exact import require
from signed import signed_problem,from_values
from rings import validate


def equations(problem):
    out=[]
    for line in problem['source'].splitlines():
        match=re.fullmatch(r'if\((.*)\)return;',line)
        if not match:continue
        terms=[]
        for term in match[1].split('+'):
            pieces=term.split('*');co=int(pieces[0]);indices=[]
            for item in pieces[1:]:
                m=re.fullmatch(r'v\[(\d+)\]',item)
                require(m is not None,'unexpected signed equation token')
                indices.append(int(m[1]))
            require(len(indices)<=2,'equation is not quadratic')
            terms.append((co,*indices,*([-1]*(2-len(indices)))))
        out.append(terms)
    require(out,'no signed equations reconstructed')
    return out


def enumerate_unrestricted(R,seconds=60,absolute_values=None):
    problem=signed_problem(R,adjoint_parity=False,positive_indicators=False)
    if absolute_values is not None:
        require(len(absolute_values)==len(problem['domains']),'incomplete absolute-value assignment')
        for i,bound in enumerate(absolute_values):
            problem['domains'][i]=[x for x in problem['domains'][i] if abs(x)==bound]
            require(problem['domains'][i],'absolute-value assignment outside signed domain')
    eqs=equations(problem)
    cpp=Path(__file__).with_suffix('.cpp');exe=cpp.with_suffix('')
    if not exe.exists() or exe.stat().st_mtime<cpp.stat().st_mtime:
        tmp=exe.with_name(exe.name+'_'+str(os.getpid()))
        subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(tmp)],check=True,capture_output=True)
        os.replace(tmp,exe)
    data=[str(len(problem['domains'])),str(len(eqs)),str(seconds)]
    for domain in problem['domains']:data.extend([str(len(domain)),*map(str,domain)])
    for eq in eqs:data.extend([str(len(eq)),*(str(x) for term in eq for x in term)])
    result=subprocess.run([str(exe)],input=' '.join(data),text=True,capture_output=True,timeout=seconds+10)
    stats=re.fullmatch(r'complete ([01]) nodes (\d+) solutions (\d+)\s*',result.stderr)
    if result.returncode==3 and stats and stats[1]=='0':
        raise TimeoutError('incomplete signed CSP: '+result.stderr.strip())
    require(result.returncode==0 and stats and stats[1]=='1','signed CSP failed: '+result.stderr)
    values=sorted(tuple(map(int,line.split())) for line in result.stdout.splitlines())
    require(len(values)==int(stats[3]) and len(set(values))==len(values),'wrong signed CSP count')
    for v in values:
        require(len(v)==len(problem['domains']) and all(x in d for x,d in zip(v,problem['domains'])),'signed CSP domain')
        validate(from_values(R,problem,v),nonnegative=False)
    return values,problem,{'complete':True,'nodes':int(stats[2]),'solutions':int(stats[3]),
                           'equations':len(eqs),'variables':len(problem['domains']),
                           'indicator_restrictions':False,'gauge':problem['gauges']}
