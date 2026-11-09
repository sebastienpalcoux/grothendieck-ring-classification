#!/usr/bin/env python3
"""Check manuscript numbers and model rows against verified structured data.

The authors' model-table caption and proof prose are preserved. Only its rows
may be regenerated; the five displayed stage counts are checked in their
surrounding sentences. This does not formally certify the mathematical proof.
"""
import argparse
from collections import Counter
from functools import cmp_to_key
import csv
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent

def manuscript_root():
    """Locate the unified manuscript above the supplementary directory."""
    for parent in ROOT.parents:
        if (parent/'manuscript.tex').is_file():
            return parent
    raise RuntimeError('Cannot locate manuscript.tex above the supplementary directory')

def require(test,message):
    if not test:raise RuntimeError(message)

def load(path):return json.loads(path.read_text())

def dimension(spec,x):
    if 'polynomial' in spec:
        q=s.Poly.from_list(spec['polynomial'],x)
        return s.CRootOf(q,q.degree()-1),spec['symbol']
    a,b,c,k=[spec[v] for v in ['constant','coefficient','radicand','denominator']]
    require(all(type(v) is int for v in [a,b,c,k]) and a>=0 and b>=0 and k>0,'invalid radical specification')
    val=(s.Integer(a)+b*s.sqrt(c))/k
    tex=str(a)
    if b:tex+='+'+('' if b==1 else str(b))+r'\sqrt{'+str(c)+'}'
    if k!=1:tex='('+tex+')/'+str(k)
    return val,tex

def ordered_models(meta,x):
    """Stable order by multiplicity and exact real algebraic global dimension."""
    def compare(a,b):
        if a['multiplicity'] != b['multiplicity']:
            return -1 if a['multiplicity'] < b['multiplicity'] else 1
        da,_=dimension(a['dimension'],x)
        db,_=dimension(b['dimension'],x)
        if bool(da < db): return -1
        if bool(da > db): return 1
        require(bool(s.simplify(da-db)==0),'undecided exact dimension comparison')
        return 0
    ordered=sorted(meta,key=cmp_to_key(compare))
    require(all(compare(a,b)<=0 for a,b in zip(ordered,ordered[1:])),
            'model-table order is not monotone')
    return ordered

def model_rows(meta,x):
    rows=[]
    for row in ordered_models(meta,x):
        value,tex=dimension(row['dimension'],x)
        approximation=f'{float(s.N(value,30)):.3f}'
        rows.append(f"${row['multiplicity']}$ & {row['name_tex']} & ${tex}$ & ${approximation}$ & {row['reference_tex']} "+r'\\')
    return '\n'.join(rows)+'\n'

def check_stage_numbers(source,summary):
    """Check the displayed stage counts without rewriting the authors' prose."""
    stages={row['filter']:row for row in summary['stages']}
    expected_order=['rank_two','formal_codegree_dnumber','spherical_arithmetic',
                    'published_rank_four_families','central_induction']
    require([row['filter'] for row in summary['stages']]==expected_order,'unexpected filter order')
    normalized=' '.join(source.split())
    snippets={
      'rank_two':('excludes ${excluded}$ rings containing a rank-two', 'leaves ${remaining}$ rings.'),
      'formal_codegree_dnumber':('rules out ${excluded}$ fusion rings', 'It remains ${remaining}$ fusion rings.'),
      'spherical_arithmetic':('eliminates ${excluded}$ rings', 'leaving ${remaining}$ rings.'),
      'published_rank_four_families':('give ${excluded}$ further exclusions.', 'leaves ${remaining}$ rings.'),
      'central_induction':('excludes ${excluded}$ rings in this subset', 'There remain ${remaining}$ fusion rings')}
    for key in expected_order:
        for template in snippets[key]:
            require(template.format(**stages[key]) in normalized,'displayed stage count differs: '+key)
    require('$'+str(summary['census_count'])+'$' in source,'displayed census total differs')
    require('$'+str(summary['census_count']-summary['model_count'])+'$' in source,
            'displayed exclusion total differs')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Regenerate only model-table rows after checking data and displayed stage counts.')
    parser.add_argument('--output',type=Path,default=ROOT/'validation/manuscript_data_check.json')
    args=parser.parse_args()
    counts={int(r['multiplicity']):int(r['rings']) for r in csv.DictReader((ROOT/'census/data/counts.csv').open())}
    summary=load(ROOT/'classification/results/summary.json')
    verification=load(ROOT/'classification/results/verification.json')
    require(verification['all_checks_passed'],'certificate replay has not passed')
    ledger=[json.loads(line) for line in (ROOT/'classification/results/certificates.jsonl').read_text().splitlines()]
    stages=Counter(row['stage'] for row in ledger)
    remaining=summary['census_count']
    require(sum(counts.values())==remaining==len(ledger)==verification['checked_rings'],'census totals differ')
    for row in summary['stages']:
        require(row['excluded']==stages[row['filter']],'stage count differs')
        remaining-=row['excluded']
        require(remaining==row['remaining'],'running total differs')
    require(remaining==summary['model_count']==stages['model'],'model total differs')
    x,u=s.symbols('x u')
    q7=x**3-27*x**2+162*x-243
    qE=x**4-45*x**3+375*x**2-1125*x+1125
    shifted=[s.Poly(q.subs(x,44+u),u) for q in [q7,qE]]
    require(all(all(a>0 for a in q.all_coeffs()) for q in shifted),'root upper bound failed')
    meta=load(ROOT/'model_table.json');model_report=load(ROOT/'independent/results/independent_models.json')
    require(model_report['passed'] and len(meta)==len(model_report['rows'])==15,'model-table count differs')
    calculations=[]
    for spec,row in zip(meta,model_report['rows']):
        require(spec['model']==row['independent_model'],'model-table order differs')
        require(spec['multiplicity']==row['multiplicity'],'model multiplicity differs')
        d,tex=dimension(spec['dimension'],x)
        cp=s.Poly.from_list(row['casimir_polynomial'],x);mp=s.Poly(s.minpoly(d,x),x)
        require(cp.rem(mp).is_zero,'displayed dimension is not a formal codegree: '+row['independent_model'])
        lo,hi=map(s.Rational,row['FP_dimension_isolating_interval'])
        require(bool(d>=lo) and bool(d<=hi),'displayed dimension not the FP root: '+row['independent_model'])
        calculations.append({'model':row['independent_model'],'dimension':str(d),'dimension_tex':tex,'approximation':f'{float(s.N(d,30)):.3f}','verified':True})
    path=manuscript_root()/'manuscript.tex'
    source=path.read_text()
    check_stage_numbers(source,summary)
    table_end=source.index(r'\label{tab:models}')
    table_start=source.rfind(r'\begin{table}',0,table_end)
    start=source.index(r'\midrule',table_start)+len(r'\midrule')
    stop=source.index(r'\bottomrule',start)
    require(stop<table_end,'model-table bounds differ')
    expected=model_rows(meta,x)
    if args.write:
        source=source[:start]+'\n'+expected+source[stop:]
        path.write_text(source)
    else:
        require(source[start:stop].strip()==expected.strip(),'model-table rows differ; rerun with --write')
    result={'all_checks_passed':True,'multiplicity_rows':len(counts),'census_total':sum(counts.values()),
            'checked_content':['model-table rows','five stage counts'],'manuscript':'manuscript.tex','stage_numbers_match':True,'model_table_order':'multiplicity, then exact global FP dimension',
            'displayed_model_order':[row['model'] for row in ordered_models(meta,x)],
            'displayed_model_dimensions':calculations,
            'shifted_polynomials':[str(q.as_expr()) for q in shifted],
            'scope':'Verified-data model rows, displayed counts and sharp-bound arithmetic; not proof-assistant certification.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
