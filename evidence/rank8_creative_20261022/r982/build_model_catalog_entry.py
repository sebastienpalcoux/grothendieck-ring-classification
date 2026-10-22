#!/usr/bin/env python3
"""Generate/replay the single accepted E21 model entry; read-only by default."""
from pathlib import Path
import argparse
import hashlib
import json
import e21_model

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'evidence/rank8_creative_20261022/'


def run():
    receipt, fusion = e21_model.run()
    e21_model.need(receipt == json.loads((HERE/'e21_model.json').read_text()), 'model receipt replay')
    census = json.loads(e21_model.SOURCE.read_text())
    canonical = next(r['tensor'] for r in census if r['id'] == 'R8_3_982')
    evidence = [
        'r982/E21_MODEL.md', 'r982/e21_graph.json', 'r982/e21_model.json',
        'r982/e21_fusion_tensor.json', 'r982/e21_model.py', 'r982/extract_e21_graph.py',
        'unified/E21_MODEL_AUDIT.md', 'unified/e21_model_verification.json',
        'unified/audits/e21_independent_verification.json',
        'r928_r941/E21_CATEGORICAL_BRIDGE.md']
    sources = [PREFIX+p for p in evidence]
    sources += ['evidence/rank8_m3_20261021/pipeline/census_m3.json',
                'evidence/rank8_research_20261022/r982/module_types.json']
    model = 'Triality-zero component of E21 from the conformal embedding SU(3)_21 into E7_1'
    permutation = fusion['canonical_R8_3_982_to_neutral_vertex']
    inverse = [permutation.index(i) for i in range(8)]
    result = {
        'id': 'R8_3_982', 'multiplicity': 3, 'status': 'unitarily_realized',
        'model': model, 'tensor_sha256': e21_model.TENSOR_SHA, 'tensor': canonical,
        'source_certificate': PREFIX+'r982/e21_model.py',
        'model_scope': 'unitary', 'unitary': 'yes', 'pseudo_unitary': 'yes',
        'constructors': [{
            'model': model,
            'reference': 'Bocken hauer-Evans, Commun. Math. Phys.205(1999),183-228, arXiv:hep-th/9812110v2 Section6.4 pp51-54 Figure13; Coquereaux-Isasi-Schieber, SIGMA6(2010),099, arXiv:1007.0721v2 Section4.6 Figure43 p37.',
            'tensor': fusion['neutral_tensor'], 'basis_map_source_to_model': permutation,
            'construction': {
                'proof': PREFIX+'r982/E21_MODEL.md',
                'source_category': 'Unitary 24-object E21=E^(24) chiral fusion category of SU(3)_21 subset E7_1',
                'operation': 'Neutral component of the faithful Z/3Z triality grading',
                'identification': 'Exact cyclic-unit reconstruction of all24 source fusion matrices from the fundamental graph and its transpose, followed by all512 neutral tensor coefficients.',
                'basis_map_scope': 'The permutation identifies every source-neutral fusion coefficient with the canonical census tensor.',
                'model_basis': fusion['vertex_labels'][:8],
                'model_to_census_basis': inverse,
                'source_graph': PREFIX+'r982/e21_graph.json',
                'source_fusion_tensor': PREFIX+'r982/e21_fusion_tensor.json',
                'source_graph_figure': 'Figure43, printed page37, arXiv:1007.0721v2',
                'source_graph_url': 'https://arxiv.org/pdf/1007.0721v2',
                'source_pdf_sha256': receipt['source_pdf_sha256'],
                'source_graph_sha256': receipt['source_graph_sha256'],
                'unit_evaluation_rank_by_total_degree': receipt['unit_evaluation_rank_by_total_degree'],
                'neutral_structure_constants_checked': 512,
                'additional_realized_algebra': 'X0 + X5 = V tensor V* for the degree-one fundamental V',
                'independent_reviews': [PREFIX+'unified/E21_MODEL_AUDIT.md',
                                        PREFIX+'unified/audits/e21_independent_verification.json',
                                        PREFIX+'r928_r941/E21_CATEGORICAL_BRIDGE.md'],
                'scope': 'Known unitary construction; new exact census identification. No braiding on the neutral fusion category or classification of its associators is asserted.'
            }}],
        'evidence_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}}
    # Use the canonical Unicode spelling without encoding it in a shell argument.
    result['constructors'][0]['reference'] = result['constructors'][0]['reference'].replace('Bocken hauer', 'Böckenhauer')
    return [result]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    path = HERE/'model_catalog_entry.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        e21_model.need(result == json.loads(path.read_text()), 'saved E21 model catalog entry')
    print('PASS: exact E21 catalog entry and all provenance hashes match.')
