"""Complete labeled-frame hull with real distinguished-center STS rows."""
import itertools,math
from fractions import Fraction as Q
import sympy as s
from exact import require,vector,key,evaluate
from partial_s import character_table
from spectral_frame import SpectralFrameCone
import streaming as st

class STSFrameCone(SpectralFrameCone):
    def __init__(self,R,height=4,data=None,duality=True):
        require(duality,'real STS compression requires complete high duality orbits')
        super().__init__(R,height,data,duality)
        table=character_table(R,self.a);K=table.K;w=self.width;self.pairs=list(itertools.combinations_with_replacement(range(8),2))
        V=s.Matrix.hstack(*(vector(b,table.degree) for b in table.basis));W=(V.T*V).inv()*V.T
        def coords(x):
            values=tuple(Q(str(v)) for v in W*vector(x,table.degree))
            require(sum((K(s.Rational(v.numerator,v.denominator))*b for v,b in zip(values,table.basis)),K.zero)==x,'STS real coefficient outside relative trace field')
            return values
        conjugate=table.conjugate
        real=lambda x:(x+conjugate(x))/K(2)
        values={};products={};realcoords={}
        def chi(v):
            v=tuple(v)
            if v not in values:values[v]=tuple(sum((K(n)*x for n,x in zip(v,row)),K.zero) for row in table.characters)
            return values[v]
        def product(x,y):
            pair=(tuple(key(x)),tuple(key(y)))
            if pair not in products:
                value=real(x*y);vk=tuple(key(value))
                if vk not in realcoords:realcoords[vk]=coords(value)
                products[pair]=realcoords[vk]
            return products[pair]
        all_frames=self.frames;all_assignments=self.meta['symmetric_character_assignments'];frames=[];labels=[];lowextra=[]
        for frame,assignments in zip(all_frames,all_assignments):
            columns=[(1,)+(0,)*7]+[self.low[j][1] for j in frame];chars=[chi(v) for v in columns]
            for assignment in assignments:
                inverse={E:j for j,E in enumerate(assignment)};require(len(inverse)==8,'incomplete low character assignment')
                feature=[]
                for E,F in self.pairs:
                    total=tuple(sum(product(c[E],c[F])[k] for c in chars[1:]) for k in range(w))
                    rhs=coords(real(table.codegrees[F]*chars[inverse[F]][E]))
                    feature.append(tuple(x-y for x,y in zip(total,rhs)))
                frames.append(frame);labels.append(assignment);lowextra.append(feature)
        self.frames=tuple(frames);shift=len(frames)-self.offset;self.offset=len(frames);self.high_end+=shift;self.nvars+=shift
        self.sts_high=[]
        for orbit in self.orbits:
            chars=[chi((0,)+tuple(self.a['high'][j][0])) for j in orbit]
            self.sts_high.append(tuple(tuple(sum(product(c[E],c[F])[k] for c in chars) for k in range(w)) for E,F in self.pairs))
        trace1=[tuple(map(Q,t[0])) for t in self.types]
        scales=[1]*w
        for features in lowextra:
            for co in features:
                for k,x in enumerate(co):scales[k]=math.lcm(scales[k],x.denominator)
        # Denominator bound for every product co*trace, avoiding the full
        # high-vector by trace-type matrix during construction.
        co_den=math.lcm(*(x.denominator for features in self.sts_high for co in features for x in co)) if self.sts_high else 1
        tr_den=math.lcm(*(x.denominator for tr in trace1 for x in tr))
        for k in range(w):scales[k]=math.lcm(scales[k],co_den*tr_den)
        self.sts_rows=[]
        for E,F in self.pairs:
            rr=[]
            for k in range(w):
                rr.append(len(self.rows));self.rows.append(('STS_real',E,F,k));self.rhs.append(-scales[k] if k==0 else 0);self.scales.append(scales[k])
            self.sts_rows.append(rr)
        self.nrows=len(self.rows);self.sts_scales=scales;self.sts_trace1=trace1
        self.sts_low=[{row:int(co[k]*scales[k]) for rr,co in zip(self.sts_rows,features) for k,row in enumerate(rr) if co[k]} for features in lowextra]
        # Oracle contraction co*trace is bilinear in the trace coordinates.
        basis=[tuple(Q(int(i==j)) for i in range(w)) for j in range(w)]
        def scaled(x,k):
            value=x*scales[k];require(value.denominator==1,'nonintegral scaled STS coefficient');return int(value)
        self.sts_products=[[tuple(tuple(scaled(x,k) for k,x in enumerate(self.a['mul'](co,e))) for e in basis) for co in features] for features in self.sts_high]
        # The basis coefficient times row scale is integral by construction.
        require(all(all(Q(x).denominator==1 for e in feature for x in e) for features in self.sts_products for feature in features),'STS scale failed')
        self.meta={**self.meta,'rows':self.nrows,'variables':self.nvars,'row_scales':self.scales,'low_domain':'complete_labeled_frames_with_partial_S_and_STS','low_frames':len(self.frames),'frame_domain_sha256':st.digest(self.frames),'frame_character_labels':labels,'STS_real_pairs':list(map(list,self.pairs)),'STS_scales':scales,'STS_feature_sha256':st.digest([lowextra,self.sts_high])}

    def column(self,index):
        col=dict(super().column(index))
        if index<self.offset:col.update(self.sts_low[index]);return col
        if index>=self.high_end:return col
        orbit,ti=divmod(index-self.offset,self.nt);trace=self.sts_trace1[ti]
        for rr,co in zip(self.sts_rows,self.sts_high[orbit]):
            values=self.a['mul'](co,trace)
            for k,row in enumerate(rr):
                value=values[k]*self.sts_scales[k];require(value.denominator==1,'nonintegral STS column')
                if value:col[row]=int(value)
        return col

    def low_scores(self,y):
        for index,value in super().low_scores(y):yield index,value+sum(y[r]*v for r,v in self.sts_low[index].items())

    def high_scores(self,y):
        corrections=[]
        for features in self.sts_products:
            coefficients=[sum(y[rr[k]]*product[l][k] for rr,product in zip(self.sts_rows,features) for k in range(self.width)) for l in range(self.width)]
            corrections.append([sum(Q(c)*x for c,x in zip(coefficients,trace)) for trace in self.sts_trace1])
        for index,value in super().high_scores(y):
            orbit,ti=divmod(index-self.offset,self.nt);extra=corrections[orbit][ti];require(extra.denominator==1,'nonintegral STS oracle score');yield index,value+int(extra)
