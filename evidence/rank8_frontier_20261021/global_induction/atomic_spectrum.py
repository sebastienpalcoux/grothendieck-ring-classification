"""Full splitting-field S symmetry without enlarging the twist-trace field."""
import itertools,math,sys
from fractions import Fraction as Q
import streaming as st
from exact import require,discover_roots
from rings import Characters
from partial_s import RealTable,filtered
sys.path.insert(0,str(st.HERE.parent/'quadratic'))

def table_for(R,a):
    ch=Characters(R)
    if discover_roots(ch.p,a['K']) is not None:return RealTable(R,a)
    if all(R[i][i][0]==1 for i in range(8)):
        from sextic_character_table import SexticTable
        return SexticTable(R,a)
    from quartic_complex_character_table import QuarticComplexTable
    return QuarticComplexTable(R,a)

class AtomicSpectrum(st.Cone):
    def __init__(self,R,height=4,data=None,duality=True):
        a=st.old.setup(R) if data is None else data;T=table_for(R,a);a,report=filtered(R,a,T);K=T.K
        fp=T.characters.index(tuple(T.ds));labels=[E for E in range(8) if E!=fp];columns=[]
        for E in labels:
            choices=set()
            for cs in a['columns']:
                for c in cs:
                    if sum((K(n)*d for n,d in zip(c,T.ds)),K.zero)==T.beta[E]:choices.add(tuple(c))
            require(choices,'empty character-labeled column domain');columns.append(sorted(choices))
        super().__init__(R,height,dict(a,columns=columns),duality)
        d=T.degree;pairs=list(itertools.combinations(labels,2));features=[]
        for group,c,z in self.low:
            G=labels[group];cv=[sum((K(n)*v for n,v in zip(c,row)),K.zero) for row in T.characters];f=[]
            for E,F in pairs:f.append(T.coordinates((T.beta[E]*cv[E] if G==F else K.zero)-(T.beta[F]*cv[F] if G==E else K.zero)))
            features.append(f)
        scales=[1]*d
        for f in features:
            for co in f:
                for k,x in enumerate(co):scales[k]=math.lcm(scales[k],x.denominator)
        rows=[]
        for E,F in pairs:
            rr=[]
            for k in range(d):rr.append(len(self.rows));self.rows.append(('atomic_S_full_field',E,F,k));self.rhs.append(0);self.scales.append(scales[k])
            rows.append(rr)
        def integer(x,k):
            x=Q(x)*scales[k];require(x.denominator==1,'full-field S coefficient is not integral');return int(x)
        self.extra_low=[{row:integer(co[k],k) for rr,co in zip(rows,f) for k,row in enumerate(rr) if co[k]} for f in features];self.nrows=len(self.rows)
        self.meta={**self.meta,'rows':self.nrows,'row_scales':self.scales,'low_domain':'independent_character_labeled_columns_with_full_field_S_symmetry','FP_character':fp,'low_character_labels':labels,'character_table':T.metadata,'partial_S_filter_sha256':st.digest(report),'partial_S_low_rejections':len(report['low_failures']),'partial_S_high_rejections':len(report['high_failures']),'S_full_field_degree':d,'S_feature_sha256':st.digest(features),'S_coordinate_scales':scales}
    def column(self,index):
        out=dict(super().column(index))
        if index<self.offset:out.update(self.extra_low[index])
        return out
    def low_scores(self,y):
        for index,value in super().low_scores(y):yield index,value+sum(y[r]*v for r,v in self.extra_low[index].items())
