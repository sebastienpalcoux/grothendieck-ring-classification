"""Package the proved unitary R721 construction in the existing model schema.

The categorical proof is R721_QSYSTEM_CONSTRUCTION.md. Arithmetic components
have standalone exact verifiers and independent review receipts. This packager
binds their inputs and verifies the complete identified tensor/induction map.
"""
from pathlib import Path
import hashlib,itertools,json,sys
import sympy as s
from r721_dual_fusion import B,dims,mul,source,need,validate
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tensor_sha(t):return hashlib.sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest()
def main():
    crosspath=HERE.parent/'r721/census_dimension_crosswalk.json';cross=json.loads(crosspath.read_text())
    need(cross['status']=='PASS'and cross['scanned_cumulative_records']==4500,'exhaustive cumulative crosswalk')
    need(len(cross['matches'])==1 and cross['matches'][0]['id']=='R8_3_721','unique entire-ring identification')
    sourcepath=ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    R=cross['matches'][0]['tensor']
    frozen=next(row for row in json.loads(sourcepath.read_text())if row['id']=='R8_3_721')
    need(R==frozen['tensor'],'immutable census full tensor identity')
    digest=tensor_sha(R);need(digest==cross['matches'][0]['tensor_sha256']=='76e26a815651476dfda5c2aa654f0d1327bdc890e08086cb6dbfe39ef9a1cdc5','census tensor digest')
    p=[0,1,2,4,6,3,5,7];q=[p.index(i)for i in range(8)]
    T=[[[R[p[i]][p[j]][p[k]]for k in range(8)]for j in range(8)]for i in range(8)]
    validate(T);N=source()
    need(max(v for row in T for col in row for v in col)==3,'exact multiplicity3')
    for i,j in itertools.product(range(8),repeat=2):
        need(tuple(sum(T[i][j][k]*dims[k][h]for k in range(8))for h in(0,1))==mul(dims[i],dims[j]),'exact dimension character')
    for i,j,z in itertools.product(range(8),repeat=3):
        lhs=sum(B[i,x]*B[j,y]*T[x][y][z]for x in range(8)for y in range(8))
        rhs=sum(N[i][a][u]*N[u][j][t]*B[t,z]for a in(0,4)for u in range(8)for t in range(8))
        need(lhs==rhs,'all512 induction product coordinates')
    rankpath=HERE.parent/'semion_fermion/construction/r721_bimodule_rank.json';ranks=json.loads(rankpath.read_text())
    factor=next(r for r in ranks['factors']if r['rank']==8)
    need(sorted(map(tuple,factor['forgetful_rows']))==sorted(tuple(B[:,i])for i in range(8)),'exact unique rank8 Gram factor')
    need(ranks['remaining_dual_ranks']==[6,8],'rank alternatives before categorical conjugacy cut')
    boundpath=HERE/'r721_dual_multiplicity_verification.json';bounds=json.loads(boundpath.read_text())
    need(len(bounds['cases'])==4 and all(c['passed']and c['fusion_coefficients_covered']==512 and c['maximum_upper_bound']==3 for c in bounds['cases']),'complete exact coefficient bound')
    for name,hashvalue in bounds['files'].items():need(sha(HERE/name)==hashvalue,'coefficient verifier input binding')
    proof=HERE/'R721_QSYSTEM_CONSTRUCTION.md'
    files=[proof,rankpath,crosspath,boundpath,sourcepath,HERE/'r721_gi_identification.json',
           HERE.parent/'semion_fermion/construction/PROOF.md',HERE.parent/'review/R721_CATEGORICAL_REVIEW.md',
           HERE.parent/'quadratic/r721_bound_review.json',HERE/'R721_RANK_INDEPENDENT_REVIEW.json']
    model='Bimodules over 1+rho in the C2 de-equivariantization of GH(C8)'
    record=dict(id='R8_3_721',multiplicity=3,status='unitarily_realized',model=model,
        tensor_sha256=digest,tensor=R,source_certificate=str(Path(__file__).relative_to(ROOT)),
        model_scope='unitary',unitary='yes',pseudo_unitary='yes',constructors=[dict(model=model,
        reference='Grossman-Izumi arXiv:1501.07679v2 equations(2.21)-(2.22), Example4.4, Section6 and Example6.10; arXiv:1906.07397v2 Definition6.1 and Section6.1.6.',
        tensor=T,basis_map_source_to_model=q,construction=dict(proof=proof.name,
        source_category='C2 de-equivariantization of the existing C8 generalized-Haagerup category',
        algebra='Inherited connected separable Q-system 1+rho',
        identification='Actual Morita dual forced to rank8; exact rational inequalities force multiplicity<=3; the supplied complete4500-ring census gives the unique based ring. Its actual dual associator/fusion coefficients are not independently extracted.',
        basis_map_scope='The permutation verifies census-tensor compatibility with the mandatory induction columns; actual-category identification uses the multiplicity bound and complete-census uniqueness.',
        model_basis=['1','a','a*','b','b2','d','c','e'],
        model_to_census_basis=p,forgetful_columns=[[int(x)for x in row]for row in B.tolist()],
        independent_reviews=['../review/R721_CATEGORICAL_REVIEW.md','../quadratic/r721_bound_review.json','R721_RANK_INDEPENDENT_REVIEW.json']))],
        evidence_sha256={str(f.relative_to(ROOT)):sha(f)for f in files})
    (HERE/'consolidated_models.json').write_text(json.dumps([record],indent=2)+'\n')
    print(json.dumps(dict(id=record['id'],status=record['status'],model=model,tensor_sha256=digest,
        all512_induction_product_coordinates=True,full_tensor_axioms=True,census_unique=True,
        model_basis_to_census=p,model_record_sha256=sha(HERE/'consolidated_models.json')),indent=2))

if __name__=='__main__':main()
