"""Independent exact colored-graph proof that the16 outsiders are not in the8 models."""
from pathlib import Path
from itertools import product
import json,time
import networkx as nx
from audit_liptrap import HERE,need

def signature(R):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    return [(i==0,du[i]==i,tuple(sorted(sum(v) for v in R[i])),tuple(sorted(sum(R[j][i]) for j in range(n))),tuple(sorted(R[i][du[i]])),sum(R[i][j][j] for j in range(n))) for i in range(n)]

def graph(R):
    G=nx.MultiDiGraph();n=len(R);sig=signature(R)
    for i in range(n):G.add_node(('o',i),color=('basis',sig[i]))
    for i,j in product(range(n),repeat=2):
        p=('p',i,j);G.add_node(p,color=('product',sig[i],sig[j],sum(R[i][j])))
        G.add_edge(('o',i),p,role='left');G.add_edge(('o',j),p,role='right')
        for k,v in enumerate(R[i][j]):
            if v:G.add_edge(p,('o',k),role=('output',v))
    return G

def main():
    start=time.monotonic();D=json.loads((HERE.parent/'d32/original_tensors.json').read_text());allowed=json.loads((HERE.parent/'d32/exhaustive_catalog.json').read_text())['allowed_ids'];out=[];graphs={}
    for rid in D:
        if rid in allowed:continue
        candidates=[aid for aid in allowed if sorted(signature(D[rid]))==sorted(signature(D[aid]))]
        for aid in candidates:
            graphs.setdefault(rid,graph(D[rid]));graphs.setdefault(aid,graph(D[aid]))
            matcher=nx.algorithms.isomorphism.MultiDiGraphMatcher(graphs[rid],graphs[aid],node_match=nx.algorithms.isomorphism.categorical_node_match('color',None),edge_match=nx.algorithms.isomorphism.categorical_multiedge_match('role',None))
            need(not matcher.is_isomorphic(),'unexpected based isomorphism')
        out.append(dict(id=rid,coarse_candidate_ids=candidates,remaining_candidates_excluded_by='exact directed colored product-graph isomorphism'))
    need(len(out)==16,'all16outside')
    result=dict(status='PASS',outsiders=16,exact_graph_pairs=sum(len(r['coarse_candidate_ids']) for r in out),records=out,seconds=time.monotonic()-start)
    (HERE/'d32_nonisomorphism_independent.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

if __name__=='__main__':main()
