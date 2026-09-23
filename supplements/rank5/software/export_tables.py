"""Regenerate manuscript tables and machine-readable summaries from the ledger."""
import json,collections,csv
from pathlib import Path
from exact import require
P=Path(__file__).resolve().parents[1]

def main():
    d=json.load(open(P/'data/decisions.json'));cache=json.load(open(P/'certificates/exclusions.json'))
    report=json.load(open(P/'verification/pinned_full_verification.json'))
    require(report['status']=='PASS' and report.get('pinned_repository_commit')=='b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
            'tables require a successful pinned-source full verification')
    extension_report=json.load(open(P/'verification/extension19_20_verification.json'))
    require(extension_report['status']=='PASS' and extension_report['general_exclusions']==12506,
            'tables require complete, independently rerun extension verification')
    extension=[json.loads(line) for line in open(P/'data/extension19_20/full.jsonl')]
    require(len(extension)==12506 and all(r['criterion']!='general_residual' and r['certificate'] is not None for r in extension),
            'extension decisions must all carry exact general certificates')
    bym=collections.defaultdict(list)
    for r in extension:bym[r['m']].append(r)
    a=['\\begin{table}[ht]\\centering\\small','\\begin{tabular}{rrrrr}\\toprule',r'$\mu$&Total&Unitary models&General exclusions&General residuals\\\midrule']
    for m in range(1,21):
        if m<=18:
            rr=[r for r in d if r['m']==m];cc=collections.Counter(r['general'] for r in rr)
            values=[m,len(rr),cc['realized'],cc['excluded'],cc['unresolved']]
        else:values=[m,len(bym[m]),0,len(bym[m]),0]
        a.append('&'.join(map(str,values))+r'\\')
    a += [r'\bottomrule\end{tabular}',r'\caption{Exact automatic coverage of all pinned rank-five tensors through multiplicity twenty. Spherical and pivotal residual counts are zero throughout; the two general residuals at eighteen have spherical exclusion certificates.}\label{tab:coverage}\end{table}']
    (P/'papers/coverage_table.tex').write_text('\n'.join(a)+'\n')
    # Match unified.basic_certificate -> cyclic_four -> parity -> general_certificate.
    names={'dnumber':'Formal-codegree $d$-number test','cyclotomic':'Cyclotomicity test','subring':'Fusion-subring index test','cyclic_four_central':'Cyclic-four central support','quadratic_parity_pseudo':'Quadratic parity and positive induction','quadratic_parity_spherical':'Quadratic parity and spherical characters','pseudo_gate':'Positive reduction and central induction','signed_extension_positive':'Positive-indicator sphericalization'}
    a=[r'\begin{table}[ht]\centering\small',r'\begin{tabular}{lrrrr}\toprule',r'First accepted top-level certificate&First $\mu$&$\mu\le17$&$\mu\le18$&$\mu\le20$\\\midrule']
    for kind,label in names.items():
        a.append(label+'&'+str(min(r['m'] for r in d if r['criterion']==kind))+'&'+str(sum(r['criterion']==kind and r['m']<=17 for r in d))+'&'+str(sum(r['criterion']==kind for r in d))+'&'+str(sum(r['criterion']==kind for r in d)+sum(r['criterion']==kind for r in extension))+r'\\')
    exclusions=lambda subset:sum(r['general']=='excluded' for r in subset)
    a += [r'\midrule Total general exclusions&&'+str(exclusions(r for r in d if r['m']<=17))+'&'+str(exclusions(d))+'&'+str(exclusions(d)+len(extension))+r'\\',r'\bottomrule\end{tabular}',r'\caption{Disjoint first-accepted certificates in executable order. First use at a multiplicity does not date the underlying theorem. The order favors cheap general tests, then structural recognition before restricted and full central-induction searches.}\label{tab:allocation}\end{table}']
    (P/'papers/allocation_table.tex').write_text('\n'.join(a)+'\n')
    short=[('dnumber','D'),('cyclotomic','Cy'),('subring','Sub'),('cyclic_four_central','C4'),('quadratic_parity_pseudo','QP'),('quadratic_parity_spherical','QS'),('pseudo_gate','Gate'),('signed_extension_positive','Sign')]
    a=[r'\begin{table}[ht]\centering\small',r'\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{r|r|rrrrrrrr|r}\toprule',r'$\mu$&To decide&'+'&'.join(label for _,label in short)+r'&Open\\\midrule']
    for m in range(1,21):
        if m<=18:
            rr=[r for r in d if r['m']==m]
            cc=collections.Counter(r['criterion'] for r in rr)
            pending=sum(r['general']!='realized' for r in rr)
            open_count=sum(r['general']=='unresolved' for r in rr)
        else:
            rr=bym[m];cc=collections.Counter(r['criterion'] for r in rr)
            pending=len(rr);open_count=0
        a.append('&'.join(map(str,[m,pending]+[cc[k] for k,_ in short]+[open_count]))+r'\\')
    a += [r'\bottomrule\end{tabular}',r'\caption{Exact-multiplicity exclusion sequence. To decide omits independently constructed unitary models. Stage symbols follow the row order in Table~\ref{tab:allocation}; each ring appears once, at its first accepted certificate. Open concerns general categorification by these criteria.}\label{tab:stages}\end{table}']
    (P/'papers/stage_table.tex').write_text('\n'.join(a)+'\n')
    a=[r'\begin{table}[ht]\centering\small',r'\begin{tabular}{rrl}\toprule',r'$(\mu,j)$&Local index&Unitary realization\\\midrule']
    labels={'Vec(C5)':r'$\Vec(C_5)$','TY(C4)':r'Tambara--Yamagami for $C_4$','TY(C2xC2)':r'Tambara--Yamagami for $C_2^2$','SU(2)_4':r'$SU(2)_4$','PSU(2)_8':r'$PSU(2)_8$','PSU(2)_9':r'$PSU(2)_9$','Rep(S4)':r'$\Rep(S_4)$','Rep(D14)':r'$\Rep(D_{14})$','Rep(C7 semidirect C3)':r'$\Rep(C_7\rtimes C_3)$','Rep(A5)':r'$\Rep(A_5)$','PSU(3)_4':r'$PSU(3)_4$','Rep(AGL(1,5))':r'$\Rep(\operatorname{AGL}(1,5))$','Izumi C3+6 equivariantization':r'$C_2$-equivariantization of an Izumi $C_3+6$ category','Izumi C4+4':r'Izumi near-group $C_4+4$','Izumi V4+4':r'Izumi near-group $C_2^2+4$','LPR-12':r'The dimension-twelve model of \cite{LPR}','LPR-24':r'The dimension-twenty-four model of \cite{LPR}'}
    for r in sorted((r for r in d if r['general']=='realized'),key=lambda r:(r['m'],r['j'])):
        a.append(f"$({r['m']},{r['j']})$&{r['local_index']}&"+labels[r['model']['name']]+r'\\')
    a += [r'\bottomrule\end{tabular}',r'\caption{The seventeen positive rings. $D_{14}$ has order fourteen. Each tensor is constructed and matched by a unit-fixing permutation; the supplied permutation is checked.}\label{tab:models}\end{table}']
    (P/'papers/models_table.tex').write_text('\n'.join(a)+'\n')
    with (P/'data/decisions.csv').open('w',newline='') as out:
        fields=['m','j','local_index','fingerprint','general','pivotal','spherical','pseudo_unitary','unitary','criterion']
        w=csv.DictWriter(out,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(d)
    all_rows=[]
    for r in d:all_rows.append(dict(r,index_scheme='archival',repository_index=None))
    for r in extension:
        all_rows.append({'m':r['m'],'j':None,'local_index':None,
                         'repository_index':r['repository_index'],
                         'index_scheme':'pinned_repository',
                         'fingerprint':r['fingerprint'],
                         'general':'excluded','pivotal':'excluded',
                         'spherical':'excluded','pseudo_unitary':'excluded',
                         'unitary':'excluded','criterion':r['criterion']})
    require(len(all_rows)==40999,'combined ledger size')
    (P/'data/decisions_all.json').write_text(json.dumps(all_rows,separators=(',',':'))+'\n')
    with (P/'data/decisions_all.csv').open('w',newline='') as out:
        fields=['m','j','local_index','repository_index','index_scheme','fingerprint',
                'general','pivotal','spherical','pseudo_unitary','unitary','criterion']
        w=csv.DictWriter(out,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(all_rows)
    # Exact frontier coordinates in the public triple convention.
    triples=__import__('itertools').combinations_with_replacement(range(1,5),3)
    triples=list(triples);front=json.load(open(P/'data/frontier.json'))
    a=[r'\begin{equation}\label{eq:frontier-tensors}\begin{aligned}']
    for n,r in enumerate(front):
        v=[r['N'][i][j][k] for i,j,k in triples]
        a.append(r'v^{('+str(r['j'])+r')}&=('+','.join(map(str,v[:10]))+r',\\ &\hspace{15mm}'+','.join(map(str,v[10:]))+r')'+(r',\\' if n==0 else r'.'))
    a.append(r'\end{aligned}\end{equation}')
    (P/'papers/frontier_tensors.tex').write_text('\n'.join(a)+'\n')
    print('PASS generated coverage, model, criterion and frontier tables, and complete 40,999-row decision ledger.')
if __name__=='__main__':main()
