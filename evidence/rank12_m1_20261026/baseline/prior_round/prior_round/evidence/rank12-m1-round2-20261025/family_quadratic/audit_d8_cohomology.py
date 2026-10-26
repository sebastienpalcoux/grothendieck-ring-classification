"""Independent integer-lattice audit of the sixteen relative D8 cocycles.

Uses Hermite normal form of [d2 | m I], not the constructing agent's
mod-four kernel/cokernel reduction.
"""
from pathlib import Path
import hashlib,itertools,json,math,time
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'family_graded/d8_cocycles.json'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    start=time.monotonic();z=json.loads(SOURCE.read_text());G=z['group_table'];c=z['subgroup_generator'];ws=z['representatives'];n=len(G)
    need(n==8 and len(ws)==16,'sixteen retained relative cocycles')
    triples=list(itertools.product(range(1,n),repeat=3));pairs=list(itertools.product(range(1,n),repeat=2));pi={k:i for i,k in enumerate(pairs)}
    B=[]
    for a,b,d in triples:
        row=[0]*len(pairs)
        for v,k in [(1,(b,d)),(-1,(G[a][b],d)),(1,(a,G[b][d])),(-1,(a,b))]:
            if k in pi:row[pi[k]]+=v
        B.append(row)
    for w in ws:
        need(w[c][c][c]%4==0,'actual subgroup restriction')
        need(all(w[a][b][d]%4==0 for a,b,d in itertools.product(range(n),repeat=3)if not(a and b and d)),'normalization')
        need(all((w[b][d][e]-w[G[a][b]][d][e]+w[a][G[b][d]][e]-w[a][b][G[d][e]]+w[a][b][d])%4==0 for a,b,d,e in itertools.product(range(n),repeat=4)),'all cocycle equations')
    output={}
    for modulus,scale in [(4,1),(8,2)]:
        L=s.Matrix(B).row_join(modulus*s.eye(len(triples)))
        H=hermite_normal_form(L);need(H.shape==(len(triples),len(triples)),'full rank coboundary lattice')
        columns=[[int(H[a,b])for a in range(len(triples))]for b in range(len(triples))]
        def key(w):
            v=[scale*w[a][b][d]for a,b,d in triples]
            for j in range(len(triples)-1,-1,-1):
                q,v[j]=divmod(v[j],columns[j][j])
                if q:
                    for i in range(j):v[i]-=q*columns[j][i]
            return tuple(v)
        keys=[key(w)for w in ws];classes={k:i for i,k in enumerate(sorted(set(keys)))}
        output[str(modulus)]=dict(distinct_classes=len(classes),class_labels=[classes[k]for k in keys],coboundary_lattice_determinant=str(math.prod(columns[i][i]for i in range(len(triples)))))
    need(output['4']['distinct_classes']==16,'distinct modulo fourth-root coboundaries')
    need(output['8']['distinct_classes']==8,'eight independent complex cohomology classes')
    receipt=dict(status='PASS',method='Integer Hermite normal form of normalized coboundary lattices, moduli four and eight.',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),source=str(SOURCE.relative_to(ROOT.parent)),normalized_variables=len(triples),normalized_two_cochain_variables=len(pairs),checked_cocycles=len(ws),coverage=output,elapsed_seconds=time.monotonic()-start)
    (ROOT/'d8_cohomology_audit.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
