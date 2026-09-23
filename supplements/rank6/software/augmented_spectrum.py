"""Joint Galois compatibility of central dimensions and fusion eigenvalues."""
from spectral_induction import Spectrum as EigenSpectrum,Counter,evaluate,require

class AugmentedSpectrum(EigenSpectrum):
    def __init__(self,table,cols,high):
        self.table=table;K=table.K
        self.low=list(map(tuple,cols));self.high=[(0,)+tuple(v) for v,z in high];self.vectors=self.low+self.high
        self.types=[]
        for v in self.vectors:
            table.prepare(v)
            self.types.append(tuple((table.D/f)*table.values[h,v]/table.dims[v] for h,f in enumerate(table.codegrees)))
        self.augtypes=[(table.dims[v],t) for v,t in zip(self.vectors,self.types)]
        self._integer={};self.roots=table.automorphisms();alltypes=set(self.augtypes)
        bad={t for t in alltypes if not all(self.integral(x) for x in t[1])}
        self.conjugates={}
        for typ in alltypes:
            orbit=[]
            for root in self.roots:
                sd=evaluate(typ[0].to_list(),root,K);sD=evaluate(table.D.to_list(),root,K)
                scaled=table.D*sd/sD;ex=K.to_sympy(scaled)
                pos=ex.is_positive;neg=ex.is_negative
                require(pos is True or neg is True,'exact sign of normalized Galois dimension unavailable')
                dimension=scaled if pos else -scaled
                eigen=tuple(evaluate(x.to_list(),root,K) for x in typ[1])
                orbit.append((dimension,eigen))
            self.conjugates[typ]=tuple(orbit)
            if any(t not in alltypes for t in orbit):bad.add(typ)
        while True:
            new={t for t in alltypes-bad if any(u in bad for u in self.conjugates[t])}
            if not new:break
            bad|=new
        self.bad=bad
        self.forbidden=[list(v[1:]) for v,t in zip(self.high,self.augtypes[len(cols):]) if t in bad]
        self.missing_low=[j for j,t in enumerate(self.augtypes[:len(cols)]) if t in bad]
    def metadata(self):
        return {'mode':'dimension_and_joint_eigenvalues','high_columns':len(self.high),
                'forbidden':self.forbidden,'missing_low':self.missing_low,
                'joint_types':len(set(self.augtypes)),'forbidden_types':len(self.bad)}
    def balance(self,labs,nvars,trace_one=None):
        idx={v:t for v,t in zip(self.vectors,self.augtypes)};lows=Counter(self.augtypes[:len(self.low)])
        alltypes=sorted(set(self.augtypes),key=str);seen=set();rows=[];rhs=[]
        tis=[None] if trace_one is None else sorted(set(ti for v,ti in labs)|{trace_one})
        for t in alltypes:
            if t in seen or t in self.bad:continue
            orbit=set(self.conjugates[t]);seen|=orbit
            for w in sorted(orbit-{t},key=str):
                for ti in tis:
                    row=[(int(idx[(0,)+tuple(v)]==t)-int(idx[(0,)+tuple(v)]==w))*int(ti is None or ti==tj) for v,tj in labs]
                    row += [0]*(nvars-len(row));value=(lows[w]-lows[t])*int(ti is None or ti==trace_one)
                    if any(row) or value:rows.append(row);rhs.append(value)
        return rows,rhs
