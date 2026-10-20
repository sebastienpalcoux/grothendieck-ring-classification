#!/usr/bin/env python3
"""Exact coefficient/Gram proof of the c0 forced order320 packet.

Conditional on each already covered active phase assignment, proves that
orbit45 has no order320 packet and orbit50 has exactly one, in two phases.
This is a finite refinement, not an exclusion.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent;EVIDENCE=HERE.parents[1];ROOT=EVIDENCE.parents[1]
SOURCE='8606c63a2f02ea028185db755a4b055382073b94736d5040ee92f3eec07f450c'


def require(ok,why):
    if not ok:raise ValueError(why)


def psd(matrix):
    A=[[F(v) for v in row] for row in matrix]
    if not A:return True
    if any(A[i][i]<0 for i in range(len(A))):return False
    p=next((i for i in range(len(A)) if A[i][i]>0),None)
    if p is None:return not any(v for row in A for v in row)
    J=[i for i in range(len(A)) if i!=p]
    return psd([[A[i][j]-A[i][p]*A[p][j]/A[p][p] for j in J] for i in J])


def subtract(A,rows,count=1):
    return [[x-count*sum(v[i]*v[j] for v in rows) for j,x in enumerate(row)] for i,row in enumerate(A)]


def capacity(A,v):
    hi=min(A[i][i]//(v[i]*v[i]) for i in range(len(v)) if v[i])
    return max(n for n in range(int(hi)+1) if psd(subtract(A,[v],n)))


def quad_mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])


def quad_div(a,b):
    den=b[0]*b[0]-5*b[1]*b[1]
    return (F(a[0]*b[0]-5*a[1]*b[1],den),F(a[1]*b[0]-a[0]*b[1],den))


def verify(case):
    path=EVIDENCE/'criteria'/f'R7_5_5039_c8_case{case}_chi8_0_system.json'
    system=json.loads(path.read_text());raw=json.dumps(next(r['tensor'] for r in json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']=='R7_5_5039'),separators=(',',':'))
    require(hashlib.sha256(raw.encode()).hexdigest()==system['source_sha256']==SOURCE,'canonical tensor')
    N=json.loads(raw);dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    B=[[sum(N[k][i][t]*N[t][dual[k]][j] for k in range(7) for t in range(7)) for j in range(7)] for i in range(7)]
    low=system['low'];labels=system['phase_labels'];orbits=system['orbits'];records=system['phase_records'];D=(720,320)
    bound=[[B[i+1][j+1]-sum(v[i+1]*v[j+1] for v in low) for j in range(6)] for i in range(6)]
    certificate_path=EVIDENCE/'integral_gram'/f'R7_5_5039_c8_case{case}_chi8_0_phase_gram_certificate.json'
    cert=json.loads(certificate_path.read_text())
    require(cert['hashes']['system']==hashlib.sha256(path.read_bytes()).hexdigest(),'Gram certificate source binding')
    v45=orbits[45][0][0];v50=orbits[50][0][0]
    require(v45==[1,1,1,1,1,1] and v50==[1,1,2,2,2,2],'pinned independent row vectors')
    require([sum(r[0][i] for r in orbits[24]) for i in range(6)]==v50,'active orbit row sum')
    require(quad_div(orbits[24][0][2],D)==(0,F(1,40)),'active relative dimension')
    require(quad_div(orbits[45][0][2],D)==(F(1,16),0),'orbit45 relative dimension')
    require(quad_div(orbits[50][0][2],D)==(0,F(1,20)),'orbit50 relative dimension')
    require(quad_div(orbits[51][0][2],D)==(F(1,8),0),'orbit51 relative dimension')
    active={j for j,l in enumerate(labels) if any(r[0][0]!=r[0][1] for r in orbits[l['orbit']])}
    answers=[]
    for branch in cert['branches']:
        support=branch['support'];require(len(support)==1,'one active packet')
        active_j,count=support[0];al=labels[active_j];ar=records[al['phase']]
        require(al['orbit']==24 and al['multiplicity_unit']==8 and count==1 and ar['orders']==[64],'complete fixed active assignment')
        sigma=F(ar['eighth_scaled8'][2],4);tau=F(ar['eighth_scaled8'][6],4)
        require(sigma in (-1,1) and tau in (-1,1),'active eighth-root signs')
        R=subtract(bound,[r[0] for r in orbits[24]],8);require(psd(R),'active residual Gram')
        caps={o:capacity(R,orbits[o][0][0]) for o in (45,50,51)}
        require(caps=={45:17,50:34,51:9},'exact individual Gram capacities')
        # Reconstruct every Gram-pruned column without the producer checker.
        kept=[];removed=[]
        for j,col in enumerate(system['columns']):
            if j in active:continue
            if j<len(labels):
                lab=labels[j];rest=subtract(R,[r[0] for r in orbits[lab['orbit']]],lab['multiplicity_unit'])
                if any(x<0 for row in rest for x in row) or not psd(rest):removed.append(j);continue
            kept.append(j)
        require(kept==branch['kept'] and removed==branch['removed'],'independent full Gram pruning replay')
        relevant=[];ten45=[];ten50=[]
        for j in kept:
            if j>=len(labels):continue
            lab=labels[j];rec=records[lab['phase']];mu=rec['eighth_scaled8']
            coeff=[]
            for block in (2,6):
                vector=[F(0)]*6
                for v,gram,z in orbits[lab['orbit']]:
                    qr=quad_mul(quad_div(z,D),(F(mu[block],8),F(mu[block+1],8)))
                    for i in range(6):vector[i]+=lab['multiplicity_unit']*v[i]*qr[1]
                coeff.append(vector)
            if any(mu[i] for i in (2,3,6,7)):relevant.append(j)
            if not any(v for vector in coeff for v in vector):continue
            require(lab['orbit'] in (45,50) and rec['orders']==[320] and lab['multiplicity_unit']==16,'only two inactive sqrt10 sources')
            vec=v45 if lab['orbit']==45 else v50;den=8 if lab['orbit']==45 else 10
            signs=[]
            for vector in coeff:
                sign=vector[0]*den;require(sign in (-1,1) and vector==[sign*F(v,den) for v in vec],'exact normalized sqrt10 coefficient vector')
                signs.append(int(sign))
            (ten45 if lab['orbit']==45 else ten50).append({'column':j,'phase':lab['phase'],'signs':signs})
        require({labels[j]['orbit'] for j in relevant}=={45,50,51},'complete sqrt2-bearing inactive support')
        require(len(ten45)==8 and len(ten50)==8,'eight primitive320 phases on each relevant orbit')
        # Independent vector equations: v45 and v50 are independent. Its
        # capacity permits at mostone 45-packet, which cannot have zero signed
        # coefficient. The 50-packet total is<=2 and must be odd, hence1.
        require(v45[0]*v50[2]-v45[2]*v50[0]!=0,'independent row directions')
        require(caps[45]//16==1 and caps[50]//16==2,'integer packet count bounds')
        choices=[t for t in ten50 if t['signs']==[-int(sigma),-int(tau)]]
        require(len(choices)==2,'two forced phase choices')
        after=subtract(R,[v50],16);require(psd(after),'forced50 packet fits Gram')
        answers.append({'phase_case':branch['phase_case'],'active_support':support,'active_signs':[int(sigma),int(tau)],
                        'kept_columns':len(kept),'capacities':caps,'forced_zero_columns':[t['column'] for t in ten45],
                        'forced_total_one_columns':[t['column'] for t in ten50],'allowed_forced_columns':[t['column'] for t in choices],
                        'allowed_forced_phases':[t['phase'] for t in choices],
                        'other_orbit50_phases_retained':True,'post_forced_capacities':{o:capacity(after,orbits[o][0][0]) for o in (45,50,51)}})
    require(len(answers)==4,'all four existing active phases covered')
    return {'case':case,'system_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'gram_certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),'branches':answers}


if __name__=='__main__':
    out={'status':'PASS','optimized_python':not __debug__,'source_sha256':SOURCE,'cases':[verify(0),verify(1)],
         'scope':'Exact finite refinement conditional on the previously covered active assignments; no whole-ring exclusion.'}
    path=HERE/f'c0_forced_eighth_packet_{"optimized" if not __debug__ else "normal"}.json'
    path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':2,'active_phases':8,'forced_phase_branches':16,'optimized_python':not __debug__}))
