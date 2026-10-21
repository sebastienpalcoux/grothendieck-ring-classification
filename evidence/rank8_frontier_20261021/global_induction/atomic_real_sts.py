"""Character-labeled atomic induction with exact real S symmetry and STS.

Every low character has its own choice simplex. This avoids enumerating
joint frames, while retaining all linear label-dependent modular identities.
It is a necessary relaxation, not the complete joint-frame hull.
"""
import itertools,math
from fractions import Fraction as Q
import sympy as s
import streaming as st
from exact import require,vector,key
from partial_s import RealTable,filtered

class AtomicRealSTS(st.Cone):
    def __init__(self,R,height=4,data=None,duality=True):
        require(duality,'real STS requires complete duality orbits')
        a=st.old.setup(R) if data is None else data;table=RealTable(R,a);a,report=filtered(R,a,table);K=table.K
        fp=table.characters.index(tuple(table.ds));labels=[E for E in range(8) if E!=fp];columns=[]
        for E in labels:
            choices=set()
            for cs in a['columns']:
                for c in cs:
                    dim=sum((K(n)*d for n,d in zip(c,table.ds)),K.zero)
                    if dim==table.beta[E]:choices.add(tuple(c))
            require(choices,'empty labeled low domain');columns.append(sorted(choices))
        super().__init__(R,height,dict(a,columns=columns),duality)
        w=self.width;coords=table.coordinates
        values={}
        def chi(c):
            c=tuple(c)
            if c not in values:values[c]=tuple(sum((K(n)*v for n,v in zip(c,row)),K.zero) for row in table.characters)
            return values[c]
        pairs=list(itertools.combinations_with_replacement(range(8),2));sympairs=list(itertools.combinations(labels,2));lowextra=[]
        # Row convention: symmetry, then STS. Fixed tensor-unit terms are
        # moved to rhs exactly once; the remaining choices are independent.
        extra_rhs=[(Q(0),)*w for pair in sympairs]+[coords((table.codegrees[F] if F==fp else K.zero)-K.one) for E,F in pairs]
        for group,c,z in self.low:
            G=labels[group];cv=chi(c);features=[]
            for E,F in sympairs:features.append(coords((table.beta[E]*cv[E] if G==F else K.zero)-(table.beta[F]*cv[F] if G==E else K.zero)))
            for E,F in pairs:features.append(coords(cv[E]*cv[F]-(table.codegrees[F]*cv[E] if G==F else K.zero)))
            lowextra.append(features)
        self.extra_high=[]
        for orbit in self.orbits:
            chars=[chi((0,)+tuple(self.a['high'][j][0])) for j in orbit]
            self.extra_high.append([coords(sum((cv[E]*cv[F] for cv in chars),K.zero)) for E,F in pairs])
        traces=[tuple(map(Q,t[0])) for t in self.types];scales=[1]*w
        for feature in lowextra+[extra_rhs]:
            for co in feature:
                for k,x in enumerate(co):scales[k]=math.lcm(scales[k],x.denominator)
        cden=math.lcm(*(x.denominator for feature in self.extra_high for co in feature for x in co)) if self.extra_high else 1
        tden=math.lcm(*(x.denominator for tr in traces for x in tr))
        for k in range(w):scales[k]=math.lcm(scales[k],cden*tden)
        def integer(x,k):
            x=Q(x)*scales[k];require(x.denominator==1,'atomic modular row scale is not integral');return int(x)
        self.extra_rows=[]
        for j,(pair,rhs) in enumerate(zip(sympairs+pairs,extra_rhs)):
            rr=[];kind='atomic_S_symmetry' if j<len(sympairs) else 'atomic_STS'
            for k in range(w):
                rr.append(len(self.rows));self.rows.append((kind,*pair,k));self.rhs.append(integer(rhs[k],k));self.scales.append(scales[k])
            self.extra_rows.append(rr)
        self.sts_rows=self.extra_rows[len(sympairs):];self.extra_scales=scales;self.extra_traces=traces
        self.extra_low=[{row:integer(co[k],k) for rr,co in zip(self.extra_rows,feature) for k,row in enumerate(rr) if co[k]} for feature in lowextra]
        basis=[tuple(Q(int(i==j)) for i in range(w)) for j in range(w)]
        self.extra_products=[[tuple(tuple(integer(x,k) for k,x in enumerate(self.a['mul'](co,e))) for e in basis) for co in feature] for feature in self.extra_high]
        self.nrows=len(self.rows)
        self.meta={**self.meta,'rows':self.nrows,'row_scales':self.scales,'low_domain':'independent_character_labeled_columns_with_real_S_and_STS','FP_character':fp,'low_character_labels':labels,'character_table':table.metadata,'partial_S_filter_sha256':st.digest(report),'partial_S_low_rejections':len(report['low_failures']),'partial_S_high_rejections':len(report['high_failures']),'modular_feature_sha256':st.digest([lowextra,self.extra_high,extra_rhs]),'modular_scales':scales}

    def column(self,index):
        out=dict(super().column(index))
        if index<self.offset:out.update(self.extra_low[index]);return out
        if index>=self.high_end:return out
        orbit,ti=divmod(index-self.offset,self.nt)
        for rr,co in zip(self.sts_rows,self.extra_high[orbit]):
            for k,x in enumerate(self.a['mul'](co,self.extra_traces[ti])):
                x*=self.extra_scales[k];require(x.denominator==1,'atomic high coefficient not integral')
                if x:out[rr[k]]=int(x)
        return out
    def low_scores(self,y):
        for index,value in super().low_scores(y):yield index,value+sum(y[r]*v for r,v in self.extra_low[index].items())
    def high_scores(self,y):
        corrections=[]
        for feature in self.extra_products:
            coefficients=[sum(y[rr[k]]*product[l][k] for rr,product in zip(self.sts_rows,feature) for k in range(self.width)) for l in range(self.width)]
            corrections.append([sum(Q(c)*x for c,x in zip(coefficients,trace)) for trace in self.extra_traces])
        for index,value in super().high_scores(y):
            orbit,ti=divmod(index-self.offset,self.nt);x=corrections[orbit][ti];require(x.denominator==1,'atomic high oracle coefficient not integral');yield index,value+int(x)
