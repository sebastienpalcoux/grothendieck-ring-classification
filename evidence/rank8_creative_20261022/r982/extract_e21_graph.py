#!/usr/bin/env python3
"""Audit Figure 43 vector edges against the committed E21 graph receipt.

Usage: python3 extract_e21_graph.py /path/to/1007.0721v2.pdf
The source PDF is optional for the independent fusion-ring replay.
This script is read-only. Labels are transcribed in e21_graph.json;
their positions, trialities, and every edge are independently extracted.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import fitz

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run(pdf):
    expected = json.loads((HERE/'e21_graph.json').read_text())
    need(hashlib.sha256(pdf.read_bytes()).hexdigest() == expected['source_pdf_sha256'],
         'exact source PDF binding')
    page = fitz.open(pdf)[36]
    paths = page.get_drawings()
    circles = [p for p in paths if p['type'] == 'f']
    need(len(circles) == 24, '24 vertex circles')
    centers = [[float((p['rect'].x0+p['rect'].x1)/2),
                float((p['rect'].y0+p['rect'].y1)/2)] for p in circles]
    need(centers == expected['vertex_centers_pdf_points'], 'exact vertex centers/order')
    grades = [0 if p['fill'][0] > .7 else 1 if p['fill'][0] > .3 else 2 for p in circles]
    need(grades == expected['triality'], 'source colors give exact triality partition')
    edges, max_distance = [], 0.
    for p in paths:
        if p['type'] != 's':
            continue
        need(p['color'][0] > .8 and p['color'][1:] == (0., 0.), 'red source edge')
        need(len(p['items']) == 1 and p['items'][0][0] == 'l', 'single straight edge path')
        endpoints = []
        for point in p['items'][0][1:]:
            distances = [math.hypot(point.x-x, point.y-y) for x, y in centers]
            i = min(range(24), key=distances.__getitem__)
            need(distances[i] < 1, 'edge endpoint within one PDF point of unique vertex')
            need(sum(d < 1 for d in distances) == 1, 'unambiguous endpoint assignment')
            max_distance = max(max_distance, distances[i])
            endpoints.append(i)
        i, j = endpoints
        if (grades[j]-grades[i]) % 3 != 1:
            i, j = j, i
        need((grades[j]-grades[i]) % 3 == 1, 'orientation by triality')
        edges.append([i, j])
    need(sorted(edges) == expected['directed_edges'], 'all60 extracted directed edges match')
    need(abs(max_distance-expected['maximum_edge_endpoint_distance_pdf_points']) < 1e-12,
         'maximum endpoint distance receipt')
    print('PASS: all 24 source vertex positions, triality colors, and 60 directed edges match Figure43.')


if __name__ == '__main__':
    need(len(sys.argv) == 2, 'provide the original source PDF path')
    run(Path(sys.argv[1]))
