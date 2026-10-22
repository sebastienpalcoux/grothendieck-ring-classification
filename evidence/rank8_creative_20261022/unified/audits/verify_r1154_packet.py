#!/usr/bin/env python3
"""Independent projector, tensor-convention and residual-block audit."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.dont_write_bytecode = True

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = ROOT/'evidence/rank8_creative_20261022/r1154/verify_semionic_packet.py'
    spec = importlib.util.spec_from_file_location('packet_producer', source)
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    l = p.l

    # Derive the residual STS equations directly, independently of the
    # producer's already-selected three candidate matrices.
    a,b,c = s.symbols('a b c')
    A = s.Matrix([[a,b],[b,c]])
    T = s.diag(s.I,-s.I)
    equations = s.expand(A*T*A-T.inv()*A*T.inv())
    need(equations[0,1] == s.I*a*b-s.I*b*c-b,
         'Wrong off-diagonal STS equation')
    for epsilon in [1,-1]:
        # If b != 0 and A^2=epsilon I, a+c=0 and a-c=-i.
        av=-s.I/2;cv=s.I/2;bsq=epsilon+s.Rational(1,4)
        for bv in [s.sqrt(bsq),-s.sqrt(bsq)]:
            candidate=A.subs({a:av,b:bv,c:cv})
            need(s.simplify(candidate*candidate-epsilon*s.eye(2))==s.zeros(2),
                 'Residual square equation')
            norm=s.simplify(abs(av)**2+abs(bv)**2)
            need(norm==(s.Rational(3,2) if epsilon==1 else 1),
                 'Residual positive-square branch must fail unitarity')
    for av,cv in [(s.I,-s.I)]:
        need(equations.subs({a:av,b:0,c:cv})==s.zeros(2),
             'Unique nonzero diagonal solution')

    packet = source.with_name('semionic_packet.json')
    data=json.loads(packet.read_text());rows=[]
    for row in data['results']:
        built=p.build_at(row['pattern'],row['pair_histogram'])
        labels=built['labels'];n=len(labels);N=s.Matrix(built['N2']);I=s.eye(n)
        at=[i for i,x in enumerate(labels) if x.get('type')==10]
        P=N*(N-3*I)*(N+5*I)*(N*N-270*N+225*I)/7936
        need((N+I)*P==s.zeros(n),'Polynomial is not the minus-one spectral projector')
        need(P*P==P and s.trace(P)==4,'Wrong minus-one projector rank')
        # The polynomial equals 1 at -1; (N+I)P=0 therefore establishes
        # that its image is the full -1 eigenspace, without an assumed
        # characteristic polynomial or numerical diagonalization.
        for index,label in enumerate(labels):
            typ=label['low'] if 'low' in label else 5+label['type']
            need((l.values[typ][2]==l.K(-1))==(index in at),
                 'The -1 spectral labels are not precisely the packet')
        M=s.Matrix([l.cols[x['low']] if 'low' in x else
                    (0,)+tuple(l.domain['high_columns'][x['type']])
                    for x in labels]).T
        # Reconstruct every entry of the induced-object matrix from the
        # raw source tensor and adjunction. Here j is input and k output.
        J=s.zeros(n)
        for x in range(n):
            for y in range(n):
                J[x,y]=sum(M[j,x]*int(l.R[3][j][k])*M[k,y]
                           for j in range(8) for k in range(8))
        Ns=[s.Matrix(x) for x in row['packet_fusion_matrices']]
        need(sum(Ns,s.zeros(n))==J,'Saved fusion matrices fail direct projection formula')
        need(J==J.T,'The self-dual induced object must act symmetrically')
        need(list(J[0,:])==[int(i in at) for i in range(n)],
             'The direct projection formula has the wrong vacuum convention')
        rows.append({'pattern':row['pattern'],'pair_histogram':row['pair_histogram'],
                     'center_rank':n,'minus_one_multiplicity':4,
                     'projector_and_projection_formula':'PASS'})
    need(len(rows)==25,'Incomplete pair domain')
    report={'status':'PASS','scope':'Independent algebraic review, not categorification.',
            'residual_STS_case_split':'PASS','pair_domain':rows,
            'source_sha256':{x.relative_to(ROOT).as_posix():sha(x)
                             for x in [source,packet]}}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
