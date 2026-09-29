"""Cyclotomic trace refinement with exact joint spectra and modular low pairs."""
from cyclotomic_trace import *
from character_induction import CharacterTable
from spectral_induction import Spectrum


def table_for(R,data):
    tab=CharacterTable.__new__(CharacterTable);tab.n=len(R);tab.du=data['ch'].du;tab.K=C=data['C'];tab.seed=[]
    roots=discover_roots(data['ch'].p,C);require(roots is not None,'characters do not split in ambient cyclotomic field');check_roots(data['ch'].p,C,roots)
    tab.rows=[tuple(evaluate(list(reversed(co)),r,C) for co in data['ch'].coeff) for r in roots]
    require(len(tab.rows)==len(R) and len(set(tab.rows))==len(R),'character table incomplete')
    require(all(row[i]*row[j]==sum((C(R[i][j][k])*row[k] for k in range(len(R))),C.zero) for row in tab.rows for i in range(len(R)) for j in range(len(R))),'character homomorphism')
    tab.codegrees=[sum((row[i]*row[tab.du[i]] for i in range(len(R))),C.zero) for row in tab.rows]
    tab.ds=data['dims'];tab.D=data['DD'];tab.fp=next(i for i,row in enumerate(tab.rows) if list(row)==tab.ds)
    tab.dims={};tab.values={};tab.allowed={};tab.compatibility={}
    tab._automorphisms=[C.unit**a for a in range(data['F']) if math.gcd(a,data['F'])==1]
    return tab


def stronger_system(data,tab,cols,lab,A,b,labels):
    C=data['C'];high=[(v,None) for v in dict.fromkeys(v for v,ti in labels)];spec=Spectrum(tab,cols,high)
    if spec.missing_low:return None,None,{'missing_low':spec.missing_low}
    # Galois multiplicities without fixed-twist-type refinement. For a
    # quartic trace field Galois squares need not fix the trace vector.
    rows,rhs=spec.balance(labels,len(A[0]),None);A+=rows;b+=rhs
    forbidden=set(map(tuple,spec.forbidden));keep=[j for j in range(len(A[0])) if j>=len(labels) or labels[j][0] not in forbidden]
    A=[[row[j] for j in keep] for row in A];tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,len(R)),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=tab.D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+tuple(labels[j][0])]*data['phases'][labels[j][1]][0] if j<len(labels) else C.zero for j in keep]
        for row,value in rational_rows(coeff,rhs,C):A.append(row);b.append(value)
    return A,b,{**spec.metadata(),'variables':len(A[0]),'rows':len(A)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='+');ap.add_argument('--output',default=str(Path(__file__).with_name('modular_trace_scan.json')));args=ap.parse_args()
    rings={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};patterns={r['id']:r for r in json.load(open(ROOT/'research/round2_theory/higher_stabilizer_patterns.json'))};out=[]
    for rid in args.ids:
        started=time.monotonic();R=rings[rid]['N'];data=data_for(R,3);tab=table_for(R,data);pat=patterns[rid]
        objects=[y for y,h in zip(pat['fixed'],pat['cubic_dimensions']) if y in pat['forced_minus_objects'] and h>0]
        rec={'id':rid,'F':data['F'],'lows':len(data['lows']),'objects':objects,'branches':[],'scope':'conditional_pseudo_unitary'}
        print({k:v for k,v in rec.items() if k!='branches'},flush=True)
        for ix,cols in enumerate(data['lows']):
            why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
            if why:rec['branches'].append({'low':ix,'ordinary':why});continue
            labs=tab.assignments(cols);print(rid,ix,'labs',labs,flush=True)
            if not labs:rec['branches'].append({'low':ix,'labellings':[]});continue
            for ep in indicator_choices(R):
                A0,b0,meta0,labels=system(R,data,cols,ep,objects,True)
                for lab in labs:
                    A,b,meta=stronger_system(data,tab,cols,lab,[r[:] for r in A0],b0[:],labels)
                    y=None if A is None else farkas(A,b)
                    case={'low':ix,'labelling':lab,'indicators':ep,'meta':meta,'excluded':A is None or y is not None}
                    if y is not None:check_farkas(A,b,y);case['ray']=y
                    rec['branches'].append(case);print(rid,ix,lab,ep,meta,'excluded',case['excluded'],flush=True)
        rec['seconds']=time.monotonic()-started;out.append(rec);Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
