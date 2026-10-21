"""Actual integer center of Fibonacci tensor Vec(C4), without optimization."""
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'quadratic'))
from review_cm_real_sts import fib_group
from atomic_cm_real_sts import AtomicCMRealSTS
from quartic_complex_character_table import QuarticComplexTable
import features as f
from lattice import modular,hermite
import bounds as box
st=f.st;require=f.require

def build():
    R=fib_group(True);C=AtomicCMRealSTS(R,4);T=QuarticComplexTable(R,C.a);S=f.build(C,T)
    counts={}
    for g in range(4):
        for v,n in[(tuple(int(i==g)for i in range(8)),4),(tuple(int(i==g+4)for i in range(8)),8),(tuple(int(i in(g,g+4))for i in range(8)),4)]:counts[v]=n
    unit=(1,)+(0,)*7;pair=(1,0,0,0,1,0,0,0);counts[unit]-=4;counts[pair]-=4
    values=[0]*len(S.columns)
    for j,label in enumerate(S.column_labels):
        if label[0]=='low':
            _,E,v=label
            if tuple(v)==(unit if T.beta[E]==T.K.one else pair):values[j]=1
        elif label[0]=='high_orbit':
            vs=label[2];ns=[counts.get(tuple(v),0)for v in vs];require(len(set(ns))==1,'known high counts not dual balanced');values[j]=ns[0]
    total=[sum(values[j]*col[i]for j,col in enumerate(S.columns)if values[j])for i in range(len(S.rhs))]
    for j,label in enumerate(S.column_labels):
        if label[0]!='fusion_coefficient':continue
        col=S.columns[j];positions=[i for i,x in enumerate(col)if x];require(len(positions)==1,'fusion auxiliary not a single constant-coordinate variable')
        i=positions[0];numerator=S.rhs[i]-total[i];require(numerator%col[i]==0,'known cubic coefficient not integral');values[j]=numerator//col[i]
    f.check_integer(S,values)
    intervals=box.propagate(S);require(intervals['outcome']=='integer_box_consistent','actual center rejected by interval propagation')
    require(all(l<=v<=h for l,v,h in zip(intervals['lower_bounds'],values,intervals['upper_bounds'])),'actual center witness removed by propagated bounds')
    modular_tests=[modular(S,p)for p in(2,3)];require(all(t['outcome']=='consistent_mod_prime'for t in modular_tests),'actual center rejected modulo a prime')
    H=hermite(S);require(H['outcome']=='integer_lattice_member','actual center rejected by HNF')
    return {'kind':'actual_complex_rank8_center_integer_control','model':'Fibonacci tensor Vec(C4)',
            'tensor_sha256':st.digest(R),'metadata':S.metadata,'integer_witness':values,
            'actual_center_simple_count':64,'modular_tests':modular_tests,'box':intervals,'Hermite':H,'scope':'Gram, full distinguished S, duality, and all196 low cubic coefficients with the actual nonnegative integer center multiplicities'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=build();path=HERE/'control.json'
    if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(path.read_text())==out,'actual integer center control differs')
    print('PASS actual Fibonacci tensor Vec(C4) integer center',out['metadata']['rows'],out['metadata']['variables'],flush=True)
if __name__=='__main__':main()
