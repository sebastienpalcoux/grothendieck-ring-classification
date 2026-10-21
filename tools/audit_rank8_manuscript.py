#!/usr/bin/env python3
"""Audit the current rank-eight TeX, compiled PDF and publication mirrors."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import re
from pypdf import PdfReader
from rank8_publication import ledger_path, extension

ROOT = Path(__file__).resolve().parents[1]

def require(value, message):
    if not value:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed-pages', nargs='*', type=int, default=[])
    args = parser.parse_args()
    folder = ROOT/'manuscripts/rank8/paper'
    mirror = ROOT/'supplements/rank8/paper'
    current = extension(ROOT)
    require(current is not None, 'Accepted M3 ledger required')
    sources = {}
    def collect(name):
        path = folder/name
        require(path.is_file(), 'Missing TeX input: '+name)
        if name in sources:
            return
        sources[name] = path.read_text()
        for child in re.findall(r'\\input\{([^}]+)\}', sources[name]):
            collect(child if child.endswith('.tex') else child+'.tex')
    collect('rank8.tex')
    text = '\n'.join(sources.values())
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', text)
    citations = {key.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', text) for key in group.split(',')}
    bibliography = re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', text)
    require(set(refs) <= set(labels), 'Unresolved cross-reference')
    require(citations <= set(bibliography), 'Unresolved citation')
    require(len(labels) == len(set(labels)), 'Duplicate label')
    require(len(bibliography) == len(set(bibliography)), 'Duplicate bibliography key')
    log = (folder/'rank8.log').read_text()
    require(not re.search(r'undefined|multiply defined|Overfull|^!', log, re.M), 'Unresolved TeX build diagnostic')
    pdf = (folder/'rank8.pdf').read_bytes()
    pages = len(PdfReader(folder/'rank8.pdf').pages)
    require(all(1 <= i <= pages for i in args.reviewed_pages), 'Visual review page outside PDF')
    for name in sources:
        require((folder/name).read_bytes() == (mirror/name).read_bytes(), 'TeX mirror differs: '+name)
    for path in (folder/'rank8-reviewed.pdf', mirror/'rank8.pdf', mirror/'rank8-reviewed.pdf'):
        require(path.read_bytes() == pdf, 'PDF alias differs: '+str(path))
    counts = Counter(r['status'] for r in json.loads((ROOT/ledger_path(ROOT)).read_text()))
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    result = {
        'status': 'PASS', 'date': '2026-10-21',
        'citations': len(citations), 'bibliography_entries': len(bibliography), 'labels': len(labels),
        'source_hashes': {(folder/name).relative_to(ROOT).as_posix():sha((folder/name).read_bytes()) for name in sorted(sources)},
        'counts': {'excluded':counts['excluded'], 'unitary_models':counts['unitarily_realized'], 'general_open':counts['unresolved']},
        'exact_multiplicity_three': {key:current[key] for key in ('rings','excluded','unitarily_realized','unresolved','unitary_excluded_ids','ledger_sha256')},
        'pdf_compiled_by_this_audit': False,
        'pdf_pages': pages, 'pdf_sha256':sha(pdf), 'build_log_sha256':sha((folder/'rank8.log').read_bytes()),
        'builds': ['Audited the completed latexmk/pdflatex build; no undefined references, duplicate labels or overfull boxes.'],
        'visual_reviewed_pdf_pages': sorted(set(args.reviewed_pages)),
        'checks': {'canonical_supplement_sources_identical':True, 'four_pdf_aliases_identical':True,
                   'citations_resolved':True, 'references_resolved':True, 'duplicate_labels':False, 'overfull_boxes':False},
        'claims': 'Current source, build and publication-consistency checks only. General and unitary-only conclusions remain distinct; no independent human mathematical validation or Lean formalization is asserted.',
    }
    raw = json.dumps(result, indent=2)+'\n'
    for path in (folder/'manuscript_static_audit.json',mirror/'manuscript_static_audit.json'):
        path.write_text(raw)
    print(json.dumps({'status':'PASS','pages':pages,'counts':result['counts'],'source_files':len(sources)}))

if __name__ == '__main__':
    main()
