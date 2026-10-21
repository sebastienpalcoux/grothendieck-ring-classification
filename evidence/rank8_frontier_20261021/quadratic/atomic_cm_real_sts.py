"""Full-field atomic S symmetry plus real STS over a quadratic CM fixed field.

The character field is Q(sqrt(q),sqrt(-r)); its real fixed field is the
existing FP relative-trace field Q(sqrt(q)). No pinned core is modified.
"""
from pathlib import Path
from fractions import Fraction as Q
import itertools,math,sys
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import streaming as st
from atomic_spectrum import AtomicSpectrum
from quartic_complex_character_table import QuarticComplexTable
from sextic_character_table import rational_vector
from exact import require,key


class AtomicCMRealSTS(AtomicSpectrum):
    def __init__(self,R,height=4,data=None,duality=True):
        require(duality,'CM real STS requires complete duality orbits')
        a=st.old.setup(R)if data is None else data
        require(a['width']==2 and a['q']in(5,37),'CM adapter requires supported quadratic FP field')
        table=QuarticComplexTable(R,a);K=table.K;q=a['q'];r=1 if q==5 else 3
        super().__init__(R,height,data=a,duality=duality)
        labels=self.meta['low_character_labels'];fp=self.meta['FP_character'];w=self.width
        require(table.characters[fp]==tuple(table.ds),'character indexing changed between adapters')
        u=K([1,0]);rad=(u*u+K(q+r))/(K(2)*u);basis=[K.one,rad]
        V=s.Matrix.hstack(*(rational_vector(v,4)for v in basis));W=(V.T*V).inv()*V.T
        coordinate_cache={};real_cache={};character_cache={}
        def coords(value):
            vk=tuple(key(value))
            if vk not in coordinate_cache:
                require(table.conjugate(value)==value,'STS coefficient not fixed by conjugation')
                co=tuple(Q(str(v))for v in W*rational_vector(value,4))
                require(sum((K(s.Rational(c.numerator,c.denominator))*b for c,b in zip(co,basis)),K.zero)==value,
                        'real STS coefficient outside original FP trace field')
                coordinate_cache[vk]=co
            return coordinate_cache[vk]
        def real(value):
            vk=tuple(key(value))
            if vk not in real_cache:real_cache[vk]=coords((value+table.conjugate(value))/K(2))
            return real_cache[vk]
        def chi(v):
            v=tuple(v)
            if v not in character_cache:
                character_cache[v]=tuple(sum((K(n)*x for n,x in zip(v,row)),K.zero)for row in table.characters)
            return character_cache[v]
        pairs=list(itertools.combinations_with_replacement(range(8),2))
        rhs=[real((table.codegrees[F]if F==fp else K.zero)-K.one)for E,F in pairs]
        low=[]
        for group,v,z in self.low:
            G=labels[group];cv=chi(v)
            low.append([real(cv[E]*cv[F]-(table.codegrees[F]*cv[E]if G==F else K.zero))for E,F in pairs])
        self.cm_high=[]
        for orbit in self.orbits:
            chars=[chi((0,)+tuple(self.a['high'][j][0]))for j in orbit]
            self.cm_high.append([coords(sum((cv[E]*cv[F]for cv in chars),K.zero))for E,F in pairs])
        self.extra_traces=[tuple(map(Q,t[0]))for t in self.types]
        scales=[1]*w
        for features in low+[rhs]:
            for co in features:
                for k,x in enumerate(co):scales[k]=math.lcm(scales[k],x.denominator)
        cd=math.lcm(*(x.denominator for f in self.cm_high for co in f for x in co))if self.cm_high else 1
        td=math.lcm(*(x.denominator for tr in self.extra_traces for x in tr))
        for k in range(w):scales[k]=math.lcm(scales[k],cd*td)
        def scaled(value,k):
            v=Q(value)*scales[k];require(v.denominator==1,'nonintegral scaled CM STS coefficient');return int(v)
        self.sts_rows=[]
        for (E,F),co in zip(pairs,rhs):
            rows=[]
            for k in range(w):
                rows.append(len(self.rows));self.rows.append(('CM_STS_real',E,F,k));self.rhs.append(scaled(co[k],k));self.scales.append(scales[k])
            self.sts_rows.append(rows)
        self.cm_scales=scales
        self.cm_low=[{row:scaled(co[k],k)for rr,co in zip(self.sts_rows,f)for k,row in enumerate(rr)if co[k]}for f in low]
        unit_basis=[tuple(Q(int(i==j))for i in range(w))for j in range(w)]
        self.extra_products=[[tuple(tuple(scaled(x,k)for k,x in enumerate(self.a['mul'](co,e)))for e in unit_basis)
                              for co in features]for features in self.cm_high]
        self.nrows=len(self.rows)
        self.meta={**self.meta,'rows':self.nrows,'row_scales':self.scales,
                   'low_domain':'independent_character_labeled_columns_with_full_field_S_and_CM_real_STS',
                   'CM_STS_field':'Q(sqrt(q)) fixed by complex conjugation in Q(sqrt(q),sqrt(-r))',
                   'CM_STS_radicands':[q,-r],'CM_STS_projection_basis':['1',f'sqrt({q})'],
                   'CM_STS_pairs':list(map(list,pairs)),'CM_STS_row_scales':scales,
                   'CM_STS_feature_sha256':st.digest([low,self.cm_high,rhs]),
                   'CM_STS_high_orbits_checked_fixed':len(self.orbits)}

    def column(self,index):
        out=dict(super().column(index))
        if index<self.offset:out.update(self.cm_low[index]);return out
        if index>=self.high_end:return out
        orbit,ti=divmod(index-self.offset,self.nt)
        for rows,co in zip(self.sts_rows,self.cm_high[orbit]):
            for k,x in enumerate(self.a['mul'](co,self.extra_traces[ti])):
                x*=self.cm_scales[k];require(x.denominator==1,'nonintegral exact CM high STS entry')
                if x:out[rows[k]]=int(x)
        return out

    def low_scores(self,y):
        for index,value in super().low_scores(y):
            yield index,value+sum(y[r]*v for r,v in self.cm_low[index].items())

    def high_scores(self,y):
        corrections=[]
        for features in self.extra_products:
            co=[sum(y[rows[k]]*product[l][k]for rows,product in zip(self.sts_rows,features)for k in range(self.width))
                for l in range(self.width)]
            corrections.append([sum(Q(c)*x for c,x in zip(co,tr))for tr in self.extra_traces])
        for index,value in super().high_scores(y):
            orbit,ti=divmod(index-self.offset,self.nt);extra=corrections[orbit][ti]
            require(extra.denominator==1,'nonintegral CM high oracle score');yield index,value+int(extra)
