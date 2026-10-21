#!/usr/bin/env python3
"""Record source, cross-reference, build-log and mirror checks after a PDF build."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed-pages', nargs='*', type=int, default=[])
    parser.add_argument('--date', default='2026-10-20', help='ISO date of this source and PDF audit')
    args = parser.parse_args()
    folder = ROOT / 'manuscripts/rank7/papers'
    sources = {}

    def collect(name):
        path = folder / name
        need(path.is_file(), 'Missing TeX input: ' + name)
        if name in sources:
            return
        text = path.read_text()
        sources[name] = text
        for target in re.findall(r'\\input\{([^}]+)\}', text):
            collect(target if target.endswith('.tex') else target + '.tex')

    collect('manuscript.tex')
    text = '\n'.join(sources.values())
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', text)
    citations = {key.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', text)
                 for key in group.split(',')}
    bibliography = re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', text)
    need(set(refs) <= set(labels), 'Unresolved cross-references: ' + repr(set(refs) - set(labels)))
    need(citations <= set(bibliography), 'Unresolved citations: ' + repr(citations - set(bibliography)))
    need(len(labels) == len(set(labels)), 'Duplicate TeX labels')
    need(len(bibliography) == len(set(bibliography)), 'Duplicate bibliography keys')
    log = (folder / 'manuscript.log').read_text()
    need(not re.search(r'undefined|multiply defined|Overfull|^!', log, re.M), 'Unresolved TeX build diagnostics')
    pdf = folder / 'manuscript.pdf'
    pages = len(PdfReader(pdf).pages)
    need(all(1 <= page <= pages for page in args.reviewed_pages), 'Visual review page outside PDF')
    for name in [*sources, 'manuscript.pdf']:
        need((folder / name).read_bytes() == (ROOT / 'supplements/rank7/papers' / name).read_bytes(),
             'Supplement mirror differs: ' + name)
    need(pdf.read_bytes() == (ROOT / 'site/dist/papers/rank7.pdf').read_bytes(), 'Website PDF mirror differs')
    ledger = json.loads((ROOT / 'supplements/rank7/output/rank7_ledger.json').read_text())
    counts = Counter(row['status'] for row in ledger)
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    result = {
        'status': 'PASS', 'date': args.date, 'citations': len(citations),
        'bibliography_entries': len(bibliography), 'labels': len(labels),
        'canonical_supplement_tex_identical': True, 'all_inputs_present': True,
        'source_hashes': {(folder / name).relative_to(ROOT).as_posix(): sha((folder / name).read_bytes())
                          for name in sorted(sources)},
        'counts': {'excluded': counts['excluded'], 'unitary_models': counts['unitarily_realized'],
                   'general_open': counts['unresolved']},
        'build_log_sha256': sha((folder / 'manuscript.log').read_bytes()),
        'builds': ['latexmk/pdflatex completed; final log has no undefined references, duplicate labels or overfull boxes'],
        'visual_reviewed_pdf_pages': sorted(set(args.reviewed_pages)),
        'claims': 'Source, build and publication-consistency checks only; no independent human mathematical validation or Lean formalization is asserted.',
        'pdf_pages': pages, 'pdf_sha256': sha(pdf.read_bytes()),
        'checks': {'canonical_supplement_sources_identical': True, 'citations_resolved': True,
                   'references_resolved': True, 'duplicate_labels': False, 'overfull_boxes': False,
                   'website_pdf_identical': True},
    }
    for target in (folder, ROOT / 'supplements/rank7/papers'):
        (target / 'manuscript_static_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'pages': pages, 'counts': result['counts'],
                      'source_files': len(sources), 'reviewed_pages': result['visual_reviewed_pdf_pages']}))


if __name__ == '__main__':
    main()
