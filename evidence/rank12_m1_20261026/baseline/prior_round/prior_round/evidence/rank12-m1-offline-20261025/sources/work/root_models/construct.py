"""Exact graded pullback and half-even-metaplectic model constructors."""
from pathlib import Path
import sys,json,itertools
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'models'))
from match_models import read,based_iso,tensor_hash,ty,pointed_dihedral,rep_dihedral

def pullback_ising_s3():
    A=ty((2,));B=pointed_dihedral(3)
    # S3 elements are (reflection bit,rotation exponent), in that order.
    labs=[(a,b) for a in range(3) for b in range(6) if int(a==2)==b//3]
    return [[[A[a][c][e]*B[b][d][f] for e,f in labs] for c,d in labs] for a,b in labs],labs

def half_even_metaplectic(N):
    # N divisible by4. Subcategory 1,h,g,hg,X_i,V_1,V_2 of SO(N)_2.
    assert N%4==0 and N>=8
    k=N//2;r=k//2-1;d=4+r;n=d+2
    A=rep_dihedral(k)
    assert len(A)==d
    R=[[[0]*n for _ in range(n)] for _ in range(n)]
    for i,j,l in itertools.product(range(d),repeat=3):R[i][j][l]=A[i][j][l]
    # In the standard dihedral labeling h=2, g=3 and hg=1.
    # h fixes V, whereas g and hg exchange the two V's.
    for a in range(4):
        for u in range(2):R[a][d+u][d+(u^(a%2))]=R[d+u][a][d+(u^(a%2))]=1
    for a in range(4,d):
        for u,v in itertools.product(range(2),repeat=2):R[a][d+u][d+v]=R[d+u][a][d+v]=1
    for u,v in itertools.product(range(2),repeat=2):
        for a in ([0,2] if u==v else [1,3])+list(range(4,d)):R[d+u][d+v][a]=1
    return R,['1','hg','h','g']+[f'X{i}' for i in range(r)]+['V1','V2']

def main():
    out=[]
    constructors=[('Ising graded pullback Vec(S3)',pullback_ising_s3(),
                   {'kind':'graded_pullback','left':'Ising','right':'Vec(S3)','grading':'C2; Ising parity and permutation sign'},
                   'Full fusion subcategory of Ising x Vec(S3) on matching C2 degrees; explicit construction in report.'),
                  ('Half SO(16)_2',half_even_metaplectic(16),{'kind':'half_even_metaplectic','N':16},
                   'Gustafson--Rowell--Ruan, Metaplectic Categories, Gauging and Property F, Section3.3, arXiv:1808.00698v3.'),
                  ('Half SO(20)_2',half_even_metaplectic(20),{'kind':'half_even_metaplectic','N':20},
                   'Gustafson--Rowell--Ruan, Metaplectic Categories, Gauging and Property F, Section3.3, arXiv:1808.00698v3.')]
    for name,(M,labs),params,ref in constructors:
        n=len(M);hits=[]
        for idx,R in enumerate(read(n),1):
            p=based_iso(R,M)
            if p is not None:
                rid=f'R{n}_1_{idx}';hits.append(rid)
                out.append({'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':[{'model':name,'constructor':params['kind'],'parameters':params,'labels':labs,'reference':ref,'basis_map_source_to_model':p,'model_tensor':M}]})
        print(name,hits)
        assert len(hits)==1
    (HERE/'models.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
