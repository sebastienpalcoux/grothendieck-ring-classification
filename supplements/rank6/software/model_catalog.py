"""A complete named positive-model table with explicit based isomorphisms."""
import itertools,json,csv
from pathlib import Path
from exact import require
from rings import permute
P=Path(__file__).resolve().parents[1]
from existence import REGISTRIES,POSITIVE_STATUSES,model_existence,verify_ledger
# The keys only control presentation. No classification decision uses these names.
LABELS={
'R6_4_22':(r'Neutral modules for $(B_2)_7\subset(D_7)_1$','CRT'),
'R6_4_91':(r'Neutral modules for $(C_3)_4\subset(B_{10})_1$','CKMP'),
'R6_4_629':(r'Neutral modules for $(B_2)_{12}\subset(E_8)_1$','CRT'),
'R6_6_1712':(r'Relative Fibonacci center $Z_{\mathrm{Fib}}(TT_3)$','GNNrel,EM'),
'R6_4_249':(r'Sign-swap equivariantization of the equal half-$E_6$ quotient','ALW'),
'R6_4_322':(r'Diagonal-fermion quotient of half-$E_6\boxtimes PSU(2)_6$','ALW'),
'R6_5_17':(r"Izumi's $C_5+5$ near-group category",'Izumi'),
'R6_7_2274':(r'Extended Haagerup category $\mathcal{EH}_1$','BMPS,BPEH'),
'R6_1_1':(r'$\mathcal I(C_4,1)$: cyclic, non-self-dual Ising zest','LPR'),
'R6_1_3':(r'$\mathcal I(C_4,0)$: cyclic, self-dual Ising zest','LPR'),
'R6_1_4':(r'$\Rep(C_3\rtimes C_4)$','LPR'),
'R6_1_6':(r'$\Vec_{C_2}\boxtimes\Vec_{C_3}\simeq\Vec_{C_6}$','LPR'),
'R6_1_7':(r'Tambara--Yamagami category for $C_5$','LPR'),
'R6_1_9':(r'$\mathcal I(C_2^2,1)$: non-self-dual Ising zest','LPR'),
'R6_1_10':(r'Zested $SO(5)_2$ category','LPR'),
'R6_1_11':(r'$\mathrm{Fib}\boxtimes\Vec_{C_3}$','LPR'),
'R6_1_14':(r'$\Vec_{S_3}$','LPR'),
'R6_1_15':(r'Haagerup category $\mathcal H_3$','GS'),
'R6_1_20':(r'$\Vec_{C_2}\boxtimes\mathrm{Ising}$; also $R(0,0)$','LPR,MY'),
'R6_1_21':(r'$\Vec_{C_2}\boxtimes\Rep(S_3)$; also $R(0,1)$','LPR,MY'),
'R6_1_23':(r'$\Vec_{C_2}\boxtimes PSU(2)_5$','LPR'),
'R6_1_24':(r'$PSU(2)_{10}$ (the other $3311$ even-part ring)','LPR,IJMS'),
'R6_1_26':(r'$SO(5)_2$','LPR'),
'R6_1_30':(r'$\Rep(D_9)$, with $|D_9|=18$','LPR'),
'R6_1_32':(r'$\Rep((C_3\times C_3)\rtimes C_2)$, inversion action','LPR'),
'R6_1_34':(r'$PSU(2)_{11}$','LPR'),
'R6_1_36':(r'$\mathrm{Fib}\boxtimes\mathrm{Ising}$','LPR'),
'R6_1_37':(r'$\mathrm{Fib}\boxtimes\Rep(S_3)$','LPR'),
'R6_1_38':(r'$\mathrm{Fib}\boxtimes PSU(2)_5$','LPR'),
'R6_2_4':(r'$\mathcal E_4(G_2)$: modules for $G_{2,4}\subset\operatorname{Spin}(14)_1$','CRT'),
'R6_2_2':(r'Fermionic $C_2$-zest of $\operatorname{Ad}(E_6)\boxtimes\Vec_{C_2}$','DGP'),
'R6_2_11':(r'$\Rep((C_3\times C_3)\rtimes C_4)$','EGNO'),
'R6_2_14':(r'Fermionic grading zest of the $E_6$ category','DGP'),
'R6_2_34':(r'$TT_3$','EM'),
'R6_2_40':(r'Diagonal-fermion quotient of two identical half-$E_6$ categories','ALW'),
'R6_2_36':(r'$\mathcal C(A_4,1,C_2,1)$','Integral'),
'R6_2_49':(r'Quadratic category $R^{\prime}(2)$','MY'),
'R6_2_53':(r'$\Vec_{C_2}\boxtimes\operatorname{Ad}(E_6)$; also $R(0,2)$','MY'),
'R6_2_71':(r'$\mathcal C(S_4,\omega,C_2^2,\psi)$ of Theorem~\ref{thm:s4-model}','GNgt'),
'R6_2_69':(r'$C_2$-extension of $\Rep(H_8)$','CLS'),
'R6_2_94':(r'Diagonal-fermion quotient of $\mathrm{Ising}\boxtimes PSU(2)_6$','EGNO'),
'R6_2_98':(r'Dual even part of the Izumi $C_4$ subfactor','IMP'),
'R6_2_124':(r'Schopieray: $\mathcal C(\mathfrak{so}_5,3/2)_{\mathrm{ad}}$','SchNonPU'),
'R6_2_75':(r'$E_6$ modules over $SU(2)_{10}$','KO'),
'R6_2_97':(r'Dual Goodman--de la Harpe--Jones $3311$ even part','IJMS'),
'R6_2_105':(r'$\mathcal C(A_5,1,D_{10},1)$','Integral'),
'R6_2_127':(r'$\mathrm{Fib}\boxtimes\operatorname{Ad}(E_6)$','KO'),
'R6_2_128':(r'$D_6$ modules over $SU(2)_8$','KO'),
'R6_2_140':(r'Local $D_{10}$ modules over $SU(2)_{16}$','KO'),
'R6_2_143':(r'Commutative even part of the Izumi $C_5$ subfactor','EG'),
'R6_2_144':(r'Principal $G_2$ level-three category','QGsurvey'),
'R6_3_47':(r'$\Rep(GL(3,\FF_2))\simeq\Rep(PSL(2,7))$','Integral'),
'R6_3_218':(r"Inversion equivariantization of Izumi's $C_5+5$ near-group category",'Izumi'),
'R6_3_141':(r'$\mathcal C(A_5,1,S_3,1)$','Integral'),
'R6_6_1764':(r'Asaeda--Haagerup category $\mathcal{AH}_1$','GSAH'),
'R6_7_572':(r'$\Rep((C_3\times C_3)\rtimes Q_8)$','EGNO'),
'R6_6_345':(r'$\mathcal C_{4,8,4}$, with ring $R(4,6)$','MY')}

def build_catalog():
    rows={r['id']:r for r in json.load(open(P/'data/census.json'))};ledger=json.load(open(P/'data/decisions.json'));positive={r['id'] for r in ledger if r['status'] in POSITIVE_STATUSES};by={}
    for fn in REGISTRIES:
        for rec in json.load(open(P/f'data/{fn}.json')):
            rid=rec['id'];require(rid in positive,'constructor not a claimed positive')
            matches=[(0,)+p for p in itertools.permutations(range(1,6)) if permute(rec['N'],(0,)+p)==rows[rid]['N']]
            require(matches,'no explicit tensor isomorphism')
            by.setdefault(rid,[]).append({'name':rec['name'],'registry':fn+'.json','basis_permutation':list(min(matches)),'reference':rec.get('reference',rec.get('proof','Construction in the manuscript'))})
    require(set(by)==positive==set(LABELS),'model table does not cover exactly all positive rings')
    result=[]
    for d in ledger:
        if d['id'] not in positive:continue
        label,source=LABELS[d['id']];result.append({'id':d['id'],'multiplicity':d['m'],'index':d['index'],'latex_model':label,'citation_keys':source,'existence':d['existence'],'status':d['status'],'constructors':by[d['id']]})
    (P/'data/model_catalog.json').write_text(json.dumps(result,indent=2)+'\n')
    with (P/'data/model_catalog.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['id','multiplicity','status','general','pivotal','spherical','pseudo_unitary','unitary','constructor','registry','basis_permutation','reference'])
        for row in result:
            for c in row['constructors']:
                w.writerow([row['id'],row['multiplicity'],row['status'],*[row['existence'][k] for k in ('general','pivotal','spherical','pseudo_unitary','unitary')],c['name'],c['registry'],json.dumps(c['basis_permutation']),c['reference']])
    return result

def verify_catalog():
    saved=json.load(open(P/'data/model_catalog.json'));rows={r['id']:r for r in json.load(open(P/'data/census.json'))};ledger=json.load(open(P/'data/decisions.json'));positive={r['id'] for r in ledger if r['status'] in POSITIVE_STATUSES}
    require(len(saved)==len(positive) and {r['id'] for r in saved}==positive,'incomplete model catalogue')
    verify_ledger(ledger)
    ledger_byid={r['id']:r for r in ledger}
    records={fn+'.json':{r['name']:r for r in json.load(open(P/f'data/{fn}.json'))} for fn in REGISTRIES};seen=set()
    for row in saved:
        require(row['existence']==ledger_byid[row['id']]['existence'] and row['status']==ledger_byid[row['id']]['status'],'model catalogue existence mismatch')
        require(row['latex_model']==LABELS[row['id']][0] and row['citation_keys']==LABELS[row['id']][1],'model table label mismatch')
        for c in row['constructors']:
            r=records[c['registry']][c['name']];p=c['basis_permutation']
            require(sorted(p)==list(range(6)) and p[0]==0 and r['id']==row['id'],'invalid model match')
            require(model_existence(r)==row['existence'],'constructor existence does not match catalogue')
            require(permute(r['N'],p)==rows[row['id']]['N'],'model match fails full tensor check');seen.add((c['registry'],c['name']))
    require(seen=={(fn,name) for fn,rs in records.items() for name in rs},'a considered constructor was omitted')
    return {'positive_rings':len(positive),'constructors':len(seen)}

def latex_table():
    rows=json.load(open(P/'data/model_catalog.json'))
    text=[r'\begingroup\small\renewcommand{\arraystretch}{1.12}\setlength{\LTcapwidth}{\textwidth}',
          r'\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}lp{8.0cm}cl@{}}',
          r'\caption{All positively identified rings in the census. U means a unitary realization; S means a spherical realization and no pseudo-unitary categorification (hence no unitary one). The numbers of types U and S are given in Table~\ref{tab:classification}. Here $R_{m,j}=R^{(6)}_{m,j}$. Every constructor and its based isomorphism are recorded electronically.}\label{tab:models}\\',
          r'\toprule Ring & Model or construction & Type & Source\\\midrule\endfirsthead',
          r'\multicolumn{4}{l}{\tablename\ \thetable\ continued}\\',
          r'\toprule Ring & Model or construction & Type & Source\\\midrule\endhead',
          r'\midrule\multicolumn{4}{r}{Continued on the next page}\\\endfoot',r'\bottomrule\endlastfoot']
    old=None
    for row in rows:
        if old is not None and row['multiplicity']!=old:text.append(r'\addlinespace')
        old=row['multiplicity']
        tag='U' if row['existence']['unitary']=='yes' else 'S'
        construction_sections={'R6_4_22':'sec:conformal-models','R6_4_91':'sec:conformal-models','R6_4_629':'sec:conformal-models','R6_4_249':'sec:sign-swap','R6_4_322':'sec:mixed-fermion','R6_6_1712':'sec:relative-fibonacci'}
        source=(r'\S\ref{%s}'%construction_sections[row['id']] if row['id'] in construction_sections else r'\cite{%s}'%row['citation_keys'])
        text.append(r'$R_{%s,%s}$ & %s & %s & %s\\'%(row['multiplicity'],row['index'],row['latex_model'],tag,source))
    text += [r'\end{longtable}',r'\endgroup']
    (P/'papers/generated_models.tex').write_text('\n'.join(text)+'\n')
if __name__=='__main__':build_catalog();print(verify_catalog());latex_table()
