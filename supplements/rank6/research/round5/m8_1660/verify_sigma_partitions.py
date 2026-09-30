"""Exact Fourier-form, capacity, and opposite-root partition control.

This checks only the sigma-supported part of the first actual-twist trace.
It is not a full twist assignment or a categorification certificate.
"""
import argparse, collections, hashlib, itertools, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from exact import require
import round5_1660 as T
from dimension_block_support import restriction_order_bounds
import sympy as s

def normalized(xs):
    xs=list(map(s.Rational,xs))
    while xs and xs[0]==0:xs.pop(0)
    return xs

def partition(pattern):
    v=list(pattern);allix=tuple(range(len(v)))
    require(len(v)==8,'sigma object count')
    total=lambda ix:tuple(sum(v[i][j] for i in ix) for j in range(6))
    for a in itertools.combinations(allix,2):
        left=tuple(i for i in allix if i not in a)
        for b in itertools.combinations(left,2):
            if total(a)!=total(b):continue
            left2=tuple(i for i in left if i not in b)
            for c in itertools.combinations(left2,2):
                dd=tuple(i for i in left2 if i not in c)
                if total(c)==total(dd):return [list(a),list(b),list(c),list(dd)]
    return None

def run():
    import scipy.optimize
    def denied(*_,**__):raise RuntimeError('optimizer disabled')
    scipy.optimize.linprog=scipy.optimize.milp=denied
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_8_1660')
    data=T.M.data_for(R,3,24)
    basis=[tuple(int(i==j) for i in range(6)) for j in range(6)]
    f=restriction_order_bounds(data,basis)
    forms={24:[1,1,1,1,2,-2],12:[1,1,-1,-1,1,1]}
    chars=f['metadata']['saturated_characters']
    require({c['conductor'] for c in chars}==set(forms),'saturated character list')
    for j,rec in enumerate(f['columns']):
        for c,coeff in zip(chars,rec['coefficients']):
            require(normalized(coeff)==normalized([s.Rational(a)*forms[c['conductor']][j] for a in c['fourier']]),'Fourier form')
    patterns={};branches=[]
    for low in (0,1):
        x=json.load(open(ROOT/f'research/round5/m8_1660/low{low}_profiles.json'))
        br=x['branches'][0];V=[(0,)+tuple(v) for v in br['high_vectors']]
        require(all(v[4]==0 for v in br['columns']),'low sigma support')
        for v in V:
            if not v[4]:continue
            require(v[0]==v[1]==0 and v[4]==1 and v[2]+v[3]==4 and v[5]==3,'sigma column shape')
            dv=sum((data['K'](a)*d for a,d in zip(v,data['ds'])),data['K'].zero)
            require(dv*8==data['D']*data['ds'][4],'individual sigma dimension')
        for case in br['cases']:
            counts=collections.Counter()
            for ix in case['gram_filter']['survivor_indices']:
                p=case['profiles'][ix]
                pat=tuple(sorted(v for v,n in zip(V,p) if v[4] for _ in range(n)))
                require(len(pat)==8,'profile sigma object count')
                counts[pat]+=1
            for pat in counts:
                if pat not in patterns:
                    bins=partition(pat);require(bins is not None,'no opposite-root partition')
                    patterns[pat]=bins
            branches.append({'low':low,'labelling':case['labelling'],'counts':[{'pattern':[list(v) for v in p],'profiles':n} for p,n in sorted(counts.items())]})
    return {'id':'R6_8_1660','passed':True,'optimizer_used':False,'scope':'Fourier forms, individual sigma dimensions, and sigma-only first-trace cancellation','forms':{str(k):v for k,v in forms.items()},'branches':branches,'partitions':[{'pattern':[list(v) for v in p],'opposite_root_pairs':bins} for p,bins in sorted(patterns.items())]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    output=Path(__file__).with_name('sigma_partitions.json');result=run()
    if args.verify:require(result==json.loads(output.read_text()),'control replay mismatch')
    else:output.write_text(json.dumps(result,indent=2)+'\n')
    paths={Path(__file__).resolve(),output,ROOT/'data/census.json'}|{ROOT/f'research/round5/m8_1660/low{i}_profiles.json' for i in (0,1)}
    for mod in list(sys.modules.values()):
        name=getattr(mod,'__file__',None)
        if name:
            p=Path(name).resolve()
            if p.is_relative_to(ROOT) and p.suffix=='.py':paths.add(p)
    receipt={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'patterns':len(result['partitions']),'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
    Path(__file__).with_name('sigma_partitions_replay.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='files_sha256'},sort_keys=True))
