"""Exact provenance transfer from a published Appendix C.3.2 to census tensors.

This checks fusion axioms, integral FP dimension characters, full based
isomorphisms and exact categorical type hypotheses.  The original paper's
Normaliz no-induction theorem remains the cited reason for negative cases;
this program does not purport to recompute its Normaliz search.
"""
from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'software'))
import analyze
import verify
from prepare import key

SOURCE_URL='https://bimsa.net/doc/publication/14753.pdf'
EXACT={3:('R8_1_24',[0,3,4,5,6,7,1,2],'positive_group_theoretical'),
       4:('R8_1_3',[0,7,1,2,5,6,3,4],'published_unresolved'),
       5:('R8_1_38',[0,3,7,6,1,2,4,5],'negative_Lemma_4_3'),
       6:('R8_2_202',[0,3,7,6,1,2,4,5],'positive_group_theoretical'),
       7:('R8_1_41',[0,5,7,6,1,2,3,4],'negative_Lemma_4_2'),
       11:('R8_2_241',[0,1,2,3,4,5,6,7],'positive_group_theoretical')}

def main():
    records=json.loads((HERE/'appendix_mle2_tensors.json').read_text())['entries']
    source11=json.loads((HERE/'appendix_c3_2_item11.json').read_text())
    records.append({'appendix_item':11,
      'header':'(11) FPdim 168, type [1, 1, 1, 3, 3, 7, 7, 7], duality [0, 2, 1, 4, 3, 5, 6, 7]',
      'source_tensor':source11['source_tensor'],
      'categorification_line':source11['categorification']})
    assert {x['appendix_item'] for x in records}==set(EXACT)
    grouped={m:sorted((R for R in analyze.read_source() if analyze.mult(R)==m),
      key=lambda R:tuple(v for M in R for row in M for v in row)) for m in (1,2)}
    decisions={r['id']:r for r in json.loads((ROOT/'data/decisions.json').read_text())}
    report=[]
    for item in sorted(records,key=lambda x:x['appendix_item']):
        n=item['appendix_item'];rid,expect,claim=EXACT[n]
        S=item['source_tensor'];verify.assert_fusion_tensor(S)
        m=analyze.mult(S);j=int(rid.split('_')[-1]);assert m==int(rid.split('_')[1])
        T=grouped[m][j-1]
        assert decisions[rid]['tensor_sha256']==analyze.fp(T)
        assert key(S)==key(T)
        p=analyze.model_basis_map(S,T);assert p==expect
        assert all(S[i][h][k]==T[p[i]][p[h]][p[k]]
              for i in range(8) for h in range(8) for k in range(8))
        header=item['header'];parsed=re.search(r'FPdim (\d+), type \[([\d, ]+)\], duality \[([\d, ]+)\]',header)
        assert parsed,header
        D=int(parsed[1]);d=[int(x.strip()) for x in parsed[2].split(',')]
        du=[int(x.strip()) for x in parsed[3].split(',')]
        assert min(d)==1 and all(x>0 for x in d)
        assert analyze.dual(S)==du and sum(x*x for x in d)==D
        assert all(d[i]*d[h]==sum(S[i][h][k]*d[k] for k in range(8))
                   for i in range(8) for h in range(8))
        assert max(x for M in S for row in M for x in row)==m
        if n==5:
            assert d==[1,1,1,1,1,1,3,3] and du==[0,1,2,3,5,4,6,7] and m==1
            assert 'Lemma 4.3' in item['categorification_line']
        elif n==7:
            assert d==[1,1,1,1,1,1,3,3] and du==[0,1,2,3,5,4,7,6]
            assert 'Lemma 4.2' in item['categorification_line']
        elif n in (3,6,11):
            assert 'C(' in item['categorification_line']
        report.append({'appendix_item':n,'census_id':rid,'multiplicity':m,
            'original_basis_to_census_basis':p,'source_tensor_sha256':analyze.fp(S),
            'census_tensor_sha256':analyze.fp(T),'global_FP_dimension':D,
            'FP_dimensions_in_source_basis':d,'source_duality':du,
            'published_status':claim,'source_url':SOURCE_URL,
            'appendix_reference':'Appendix C.3.2('+str(n)+')',
            'categorification_line':item['categorification_line']})
    (HERE/'appendix_transfers_verified.json').write_text(json.dumps(report,indent=2)+'\n')
    print('checked_exact_full_tensor_transfers',len(report))
    for r in report:
        print(r['census_id'],r['published_status'],r['original_basis_to_census_basis'])

if __name__=='__main__':main()
