"""Literal512-coefficient transfer of published F660; not the residual R731."""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3];sys.path.insert(0,str(REPO/'supplements/rank8/software'))
from analyze import fp,ckey,model_basis_map
from m3_campaign import require
import zero_spectrum
# Each line is one printed horizontal row across the eight matrices in
# arXiv:2203.06522 Section7.2, page33, immediately before Theorem7.14.
PRINTED_ROWS='''
10000000 01000000 00100000 00010000 00001000 00000100 00000010 00000001
01000000 00111000 10000011 00101111 00110111 00011111 01011111 01011111
00100000 10000011 01011000 01001111 01010111 00011111 00111111 00111111
00010000 00101111 01001111 10031122 01111222 01112222 01122222 01122222
00001000 00110111 01010111 01111222 10013122 01121222 01122222 01122222
00000100 00011111 00011111 01112222 01121222 11122222 01122232 01122223
00000010 01011111 00111111 01122222 01122222 01122232 11122323 01122233
00000001 01011111 00111111 01122222 01122222 01122223 01122233 11122332
'''
def literal():
 lines=[line.split() for line in PRINTED_ROWS.splitlines() if line.strip()];require(len(lines)==8 and all(len(line)==8 for line in lines),'printed array')
 return [[[int(v) for v in lines[j][i]] for j in range(8)] for i in range(8)]
def build():
 R=literal();rows=json.loads((HERE.parent/'census_m3.json').read_text());key=ckey(R);matches=[r for r in rows if ckey(r['tensor'])==key];require([r['id'] for r in matches]==['R8_3_722'],'published F660 identity')
 match=matches[0];p=model_basis_map(match['tensor'],R);w={'kind':'zero_spectrum','indices':[1,3,4,1,1,3,4,2,2]};zero_spectrum.verify(R,w)
 return {'result':'PASS','source_url':'https://arxiv.org/abs/2203.06522','source_section':'7.2','source_theorem':'7.14','printed_tensor':R,'printed_tensor_sha256':fp(R),'id':match['id'],'tensor_sha256':match['tensor_sha256'],'basis_map_source_to_published':p,'coefficients_checked':512,'published_zero_spectrum_witness':w,'scope':'general_complex_fusion_category','distinction':'Published F660 is R8_3_722; it is not R8_3_731.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--verify',action='store_true',help='Read-only exact replay (the default).');args=ap.parse_args();out=build();path=HERE/'f660_match.json'
 if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
 else:require(json.loads(path.read_text())==out,'publishedF660 source match differs')
 print('PASS F660 identity',out['id'],'512coefficients; general zero-spectrum witness')
if __name__=='__main__':main()
