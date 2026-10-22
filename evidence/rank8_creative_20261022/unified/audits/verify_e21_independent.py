"""Independent exact reconstruction of the E21 graph fusion ring.

Optional --pdf checks all sixty vector edges against the cited figure.
The core verifier requires only the transcribed graph and canonical tensor.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'evidence/rank8_creative_20261022/r982/e21_graph.json'
    graph = json.loads(path.read_text())
    labels, grades = graph['vertex_labels'], graph['triality']
    edges = {tuple(e) for e in graph['directed_edges']}
    need(len(edges) == len(graph['directed_edges']) == 60, 'Sixty distinct edges')
    need(len(set(labels)) == len(labels) == 24, 'Twenty-four labels')
    need(all((grades[b]-grades[a]) % 3 == 1 for a,b in edges), 'Edge trialities')
    if args.pdf:
        import fitz
        need(hashlib.sha256(args.pdf.read_bytes()).hexdigest() == graph['source_pdf_sha256'], 'Source PDF identity')
        page = fitz.open(args.pdf)[36]
        centers = graph['vertex_centers_pdf_points']
        extracted = set()
        for item in page.get_drawings():
            color = item['color']
            if not color or not (color[0] > .9 and color[1] < .1 and color[2] < .1):
                continue
            need(len(item['items']) == 1 and item['items'][0][0] == 'l', 'One straight edge')
            ends = []
            for point in item['items'][0][1:]:
                distances = [(point.x-x)**2+(point.y-y)**2 for x,y in centers]
                vertex = min(range(24), key=distances.__getitem__)
                need(distances[vertex] < .3**2, 'Edge terminates at a vertex')
                ends.append(vertex)
            a,b = ends
            if (grades[b]-grades[a]) % 3 != 1:
                a,b = b,a
            extracted.add((a,b))
        need(extracted == edges, 'All published vector edges match')
    A = S.zeros(24)
    for a,b in edges:
        A[a,b] = 1
    need(A*A.T == A.T*A, 'Normal fundamental adjacency')
    need(S.trace(A**3) == 120, 'Forty oriented triangles')
    powers = [S.eye(24)]
    for i in range(1,25):
        powers.append(powers[-1]*A)
    matrices, words, rows = [], [], S.zeros(0,24)
    for degree in range(25):
        for a in range(degree+1):
            b = degree-a
            P = powers[a]*powers[b].T
            test = rows.col_join(P[0,:])
            if test.rank() > rows.rows:
                rows = test
                matrices.append(P)
                words.append([a,b])
        if rows.rows == 24:
            break
    need(rows.rows == 24, 'Unit is cyclic in the graph algebra')
    inverse = rows.inv()
    fusion = []
    for a in range(24):
        N = sum((inverse[a,k]*matrices[k] for k in range(24)), S.zeros(24))
        need(all(x.is_Integer and x >= 0 for x in N), 'Integral positive fusion coefficients')
        need(N[0,:] == S.eye(24)[a,:], 'Correct unit row')
        fusion.append(N)
    for a in range(24):
        for b in range(24):
            product = sum((fusion[a][b,k]*fusion[k] for k in range(24)), S.zeros(24))
            need(fusion[a]*fusion[b] == product, 'Full 24-object multiplication identity')
    dual = []
    for a in range(24):
        matches = [b for b in range(24) if fusion[b] == fusion[a].T]
        need(len(matches) == 1, 'Unique dual')
        dual.append(matches[0])
    for a in range(24):
        for b in range(24):
            for c in range(24):
                need(not fusion[a][b,c] or (grades[a]+grades[b]-grades[c]) % 3 == 0, 'Fusion respects triality')
    # Read the input census independently of either reconstruction output.
    census = json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    record = next(r for r in census if r['id'] == 'R8_3_982')
    need(record['tensor_sha256'] == 'f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c', 'Canonical case identity')
    tensor = record['tensor']
    need(hashlib.sha256(json.dumps(tensor,separators=(',',':')).encode()).hexdigest() == record['tensor_sha256'], 'Actual canonical tensor hash')
    mapping = [0,2,3,4,5,1,7,6]
    need(len(set(mapping)) == 8 and all(grades[v] == 0 for v in mapping), 'Entire neutral component')
    checked = 0
    for a in range(8):
        for b in range(8):
            for c in range(8):
                need(int(fusion[mapping[a]][mapping[b],mapping[c]]) == tensor[a][b][c], 'Canonical neutral tensor identity')
                checked += 1
    report = {'status':'PASS','graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
              'canonical_tensor_sha256':record['tensor_sha256'],'edges':60,'oriented_triangles':40,
              'full_fusion_rank':24,'cyclic_words':words,'evaluation_determinant':int(rows.det()),
              'neutral_tensor_entries_checked':checked,'canonical_to_figure43':[labels[v]for v in mapping],
              'duality':dual,'scope':'Exact independent fusion-ring identity; categorical existence is justified separately in E21_MODEL_AUDIT.md.'}
    output = HERE/'e21_independent_verification.json'
    if args.write:
        output.write_text(json.dumps(report,indent=2)+'\n')
    else:
        need(json.loads(output.read_text()) == report, 'Independent receipt unchanged')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
