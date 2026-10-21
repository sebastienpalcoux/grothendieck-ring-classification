"""Exact partial modular eigenvalue integrality in Q(zeta_24).

For commutative R, lambda(E,Z)=D chi_E(FZ)/(f_E dim Z) is a
modular fusion eigenvalue and hence an algebraic integer. The full
integer ring of a cyclotomic field is Z[zeta], so testing all power
basis coordinates is an exact integral-closure test, not a numerical
minimal-polynomial heuristic.
"""
import argparse,json,time
import sympy as s
import streaming as st
from exact import require,discover_roots,check_roots,key
from rings import Characters

class Table:
    def __init__(self,R,a):
        require(a['width']==4 or a['field'].get('q') in (1,2,3,6),'this exact adapter uses Q(zeta24)')
        self.R=R;self.a=a;ch=Characters(R);x=s.Symbol('x');p=s.Poly(s.cyclotomic_poly(24,x),x)
        self.K=K=s.QQ.alg_field_from_poly(p,alias='zeta');z=K([1,0]);require(z**8-z**4+K.one==K.zero,'wrong cyclotomic generator')
        r2=z**3+z**(-3);r3=z**2+z**(-2);require(r2*r2==K(2) and r3*r3==K(3),'wrong real radical basis')
        if a['width']==4:
            require(a['field']['radicands']==[2,3],'unsupported biquadratic field');basis=[K.one,r2,r3,r2*r3]
        else:basis=[K.one,{1:K.one,2:r2,3:r3,6:r2*r3}[a['q']]]
        self.ds=[sum((K(s.Rational(v.numerator,v.denominator))*b for v,b in zip(d,basis)),K.zero) for d in a['dimensions']]
        self.D=sum((d*d for d in self.ds),K.zero)
        roots=discover_roots(ch.p,K);require(roots is not None,'character field does not embed in Q(zeta24)');check_roots(ch.p,K,roots)
        self.characters=[tuple(sum((K(co)*root**j for j,co in enumerate(cf)),K.zero) for cf in ch.coeff) for root in roots]
        require(len(set(self.characters))==8 and tuple(self.ds) in self.characters,'incomplete character table or missing FP embedding')
        for row in self.characters:
            require(row[0]==K.one and all(row[i]*row[j]==sum((K(R[i][j][k])*row[k] for k in range(8)),K.zero) for i in range(8) for j in range(8)),'character multiplication fails')
        self.codegrees=[sum((row[i]*row[ch.du[i]] for i in range(8)),K.zero) for row in self.characters]
        for i,row in enumerate(self.characters):
            for j,other in enumerate(self.characters):require(sum((row[k]*other[ch.du[k]] for k in range(8)),K.zero)==(self.codegrees[i] if i==j else K.zero),'character orthogonality fails')
        self.beta=[self.D/f for f in self.codegrees];self.cache={};self._values={};self._allowed={}
        self.metadata={'conductor':24,'character_generator':ch.k,'cyclotomic_polynomial':list(map(str,p.all_coeffs())),'characters':[[list(map(str,key(v))) for v in row] for row in self.characters],'codegrees':[list(map(str,key(v))) for v in self.codegrees]}

    def failure(self,v):
        v=tuple(v)
        if v in self.cache:return self.cache[v]
        K=self.K;dim=sum((K(n)*d for n,d in zip(v,self.ds)),K.zero);require(dim!=K.zero,'zero proposed central dimension')
        for E,(row,beta) in enumerate(zip(self.characters,self.beta)):
            value=beta*sum((K(n)*ch for n,ch in zip(v,row)),K.zero)/dim
            if any(x.q!=1 for x in key(value)):
                result={'character':E,'cyclotomic_coordinates':list(map(str,key(value)))};self.cache[v]=result;return result
        self.cache[v]=None;return None

    def prepare(self,v):
        v=tuple(v)
        if v in self._allowed:return
        K=self.K;dim=sum((K(n)*d for n,d in zip(v,self.ds)),K.zero)
        self._allowed[v]=[E for E,beta in enumerate(self.beta) if beta==dim]
        for E,row in enumerate(self.characters):self._values[E,v]=self.beta[E]*sum((K(n)*ch for n,ch in zip(v,row)),K.zero)

    def assignments(self,columns):
        columns=tuple(map(tuple,columns))
        for v in columns:self.prepare(v)
        out=[]
        def recurse(chosen):
            j=len(chosen)
            if j==len(columns):out.append(tuple(chosen));return
            for E in self._allowed[columns[j]]:
                if E in chosen:continue
                if any(self._values[E,columns[i]]!=self._values[F,columns[j]] for i,F in enumerate(chosen)):continue
                recurse(chosen+[E])
        recurse([]);return out

def filtered(R,a):
    T=Table(R,a);columns=[];low_failures=[]
    for g,cs in enumerate(a['columns']):
        keep=[]
        for c in cs:
            why=T.failure(c)
            if why:low_failures.append({'group':g,'column':list(c),**why})
            else:keep.append(c)
        columns.append(keep)
    high=[];high_failures=[]
    for v,z in a['high']:
        why=T.failure((0,)+tuple(v))
        if why:high_failures.append({'column':list(v),**why})
        else:high.append((v,z))
    report={'table':T.metadata,'old_low_counts':list(map(len,a['columns'])),'new_low_counts':list(map(len,columns)),'old_high_count':len(a['high']),'new_high_count':len(high),'low_failures':low_failures,'high_failures':high_failures}
    return dict(a,columns=columns,high=high),report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--write',action='store_true');args=ap.parse_args();source=st.load_ring(args.ring);t=time.monotonic();a=st.old.setup(source['tensor']);filtered_data,report=filtered(source['tensor'],a);out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'report':report};dest=st.HERE/'partial_s_results'/f'{args.ring}.json'
    if args.write:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(json.loads(dest.read_text())==out,'partial-S source-bound replay differs')
    print(args.ring,report['old_low_counts'],report['new_low_counts'],report['old_high_count'],report['new_high_count'],'PASS',round(time.monotonic()-t,3),flush=True)
if __name__=='__main__':main()
