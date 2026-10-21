"""Exact all-entry comparison with Grossman--Izumi Definition 6.1, Section 6.1.6.

Primary sources: arXiv:1906.07397v2, pp.50,54-55; arXiv:1501.07679v2,
Example 6.10. This identifies modular data, not a Lagrangian algebra.
"""
from pathlib import Path
import hashlib
import itertools
import json
import networkx as nx
import sympy as s

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'r721/modular_completions.json'

def need(ok,label):
    if not ok: raise ValueError(label)

def main():
    source=json.loads(SOURCE.read_text())[0]
    x=s.Symbol('x');L=s.QQ.alg_field_from_poly(s.Poly(s.cyclotomic_poly(17,x),x));z=L.unit
    qr={k*k%17 for k in range(1,17)}
    rad=L.one+2*sum((z**k for k in qr),L.zero)
    need(rad**2==L(17),'Gauss square')
    C=[[sum((L(s.Rational(t))*z**i for i,t in enumerate(v)),L.zero)for v in row]for row in source['S_coefficients_ascending']]
    CT=source['T_exponents_mod_136']
    group=list(itertools.product(range(4),repeat=2))
    K=[v for v in group if all(2*t%4==0 for t in v)]
    gs=[v for v in group if v not in K and v<tuple(-t%4 for t in v)]
    js=[(v,e)for v in K if v!=(0,0)for e in (1,-1)]
    labels=['0','pi']+[['k',list(k),e]for k,e in js]+[['g',list(g)]for g in gs]+[['gamma',i]for i in range(1,9)]
    need(len(labels)==22,'rank22')
    a=L(s.Rational(1,4));b=L.one/rad
    G=[[L.zero for j in range(22)]for i in range(22)]
    G[0][0]=G[1][1]=(a-b)/2;G[0][1]=G[1][0]=(a+b)/2
    for i in range(2,8):G[0][i]=G[i][0]=G[1][i]=G[i][1]=a/2
    for i in range(8,14):G[0][i]=G[i][0]=G[1][i]=G[i][1]=a
    for i in range(14,22):G[0][i]=G[i][0]=b;G[1][i]=G[i][1]=-b
    qexp=lambda v:(v[0]*v[0]-v[1]*v[1])%8
    # Bicharacter q(x+y)/(q(x)q(y)) = i^(xx'-yy').
    bexp=lambda v,w:(v[0]*w[0]-v[1]*w[1])%4
    realphase=lambda k:L(1 if k%4==0 else -1) if k%2==0 else None
    for i,(k,e)in enumerate(js,2):
        for j,(l,f)in enumerate(js,2):
            G[i][j]=(a*realphase(bexp(k,l))+L(e*f*(1 if qexp(k)==0 else -1)*int(k==l)))/2
        for j,g in enumerate(gs,8):G[i][j]=G[j][i]=a*realphase(bexp(k,g))
    for i,g in enumerate(gs,8):
        for j,h in enumerate(gs,8):G[i][j]=a*L([2,0,-2,0][bexp(g,h)])
    for i in range(1,9):
        for j in range(1,9):G[13+i][13+j]=-(z**(6*i*j%17)+z**(-6*i*j%17))/rad
    GT=[0,0]+[17*qexp(k)for k,e in js]+[17*qexp(g)for g in gs]+[8*(3*l*l%17)for l in range(1,9)]
    key=lambda v:tuple(str(c)for c in v.to_list())
    def graph(M,T):
        H=nx.Graph()
        for i in range(22):H.add_node(i,color=(T[i],key(M[0][i]),key(M[i][i])))
        for i in range(22):
            for j in range(i+1,22):H.add_edge(i,j,color=key(M[i][j]))
        return H
    matcher=nx.algorithms.isomorphism.GraphMatcher(graph(C,CT),graph(G,GT),
        node_match=lambda a,b:a['color']==b['color'],edge_match=lambda a,b:a['color']==b['color'])
    need(matcher.is_isomorphic(),'GI full S/T isomorphism')
    p=[matcher.mapping[i]for i in range(22)]
    need(all(C[i][j]==G[p[i]][p[j]]for i in range(22)for j in range(22)),'all484 exact S entries')
    need(all(CT[i]==GT[p[i]]for i in range(22)),'all22 exact T entries')
    lagrangian=[source['restriction_columns'][i][0]for i in range(22)]
    record=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        comparator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        metric_G='C4 x C4',q1='zeta8^(x^2-y^2)',metric_Gamma='C17',q2='zeta17^(3*l^2)',
        references=['https://arxiv.org/pdf/1906.07397, Definition6.1 and Section6.1.6',
                    'https://arxiv.org/pdf/1501.07679, Example6.10'],
        candidate_to_GI_permutation=p,GI_labels=labels,exact_S_entries_compared=484,
        exact_T_entries_compared=22,all_match=True,
        lagrangian_candidate_GI_labels=[[labels[p[i]],m]for i,m in enumerate(lagrangian)if m],
        conclusion='Exact modular-data identification with the center of the C2 de-equivariantization of the known Z8 generalized Haagerup category. No algebra structure on the R721 Lagrangian candidate is proved here.')
    (HERE/'r721_gi_identification.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
