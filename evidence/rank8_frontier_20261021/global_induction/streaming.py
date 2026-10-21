"""Streaming exact global-induction cone; published M3 code is read-only.

Columns are generated on demand. The full Farkas oracle factors the high
columns into Gram, restriction and relative-moment contributions, so it
does not allocate the full matrix or a large dual simplex basis.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,heapq,itertools,json,math,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank8_m3_20261021'
sys.path.insert(0,str(BASE/'criteria'))
import global_induction as old
from exact import require

def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x

def digest(x):return hashlib.sha256(json.dumps(encode(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()

class Cone:
    def __init__(self,R,height=4,data=None,duality=True):
        self.R=R;self.height=height;self.a=a=old.setup(R) if data is None else data
        self.width=w=a['width'];self.D=tuple(map(Q,a['global_dimension']));self.duality=duality
        self.types,self.bound=a['traces'](height);self.types=[[tuple(map(Q,v)) for v in t] for t in self.types]
        self.nt=len(self.types);self.low=[]
        for g,cs in enumerate(a['columns']):
            for c in cs:
                z=tuple(sum((Q(c[i])*a['dimensions'][i][k] for i in range(8)),Q(0)) for k in range(w))
                self.low.append((g,tuple(map(int,c)),z))
        du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        require(all(du[du[i]]==i for i in range(8)),'source duality is not involutive')
        lookup={tuple(v):i for i,(v,z) in enumerate(a['high'])};require(len(lookup)==len(a['high']),'duplicate high vector')
        self.high=[];self.orbits=[]
        self.gram_pairs=list(itertools.combinations_with_replacement(range(1,8),2))
        for i,(v,z) in enumerate(a['high']):
            vd=tuple(v[du[k]-1] for k in range(1,8));j=lookup.get(vd)
            require(j is not None and tuple(a['high'][j][1])==tuple(z),'high set is not dimension-preserving dual closed')
            require(tuple(a['high'][j][0][du[k]-1] for k in range(1,8))==tuple(v),'high duality is not involutive')
            if duality and j<i:continue
            pair=(i,) if not duality or i==j else (i,j)
            vectors=[a['high'][k][0] for k in pair]
            vs=tuple(sum(v[k] for v in vectors) for k in range(7))
            gram=tuple(sum(v[k-1]*v[l-1] for v in vectors) for k,l in self.gram_pairs)
            self.high.append((vs,gram,tuple(map(Q,z))));self.orbits.append(pair)
        self.offset=len(self.low);self.high_end=self.offset+len(self.high)*self.nt
        self.rows=[];self.rhs=[];self.moment_rows={};self.rotation_rows={};self.rotation_specs=[]
        def add(label,b=0):
            at=len(self.rows);self.rows.append(label);self.rhs.append(Q(b));return at
        self.simplex=[add(('simplex',g),1) for g in range(len(a['columns']))]
        self.gram={}
        for i,j in itertools.combinations_with_replacement(range(8),2):self.gram[i,j]=add(('gram',i,j),int(a['B'][i,j])-int(i==j==0))
        for power in (1,2):
            for i in range(1,8):
                for k in range(w):self.moment_rows[power,i,k]=add(('moment',power,i,k))
        self.powers={};self.rotation=[]
        for obj in range(1,8):
            powers=[[1]+[0]*7]
            for order in range(1,height+1):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(8)) for j in range(8)])
            self.powers[obj]=powers
            for order in range(3,height+1):
                rs=[int(r) for r in old.s.divisors(order) if r<order]
                traces=a['rotations'](order,rs);sumrow=add(('rotation_sum',obj,order),powers[order][0]);rr={}
                for at,r in enumerate(rs):
                    for k in range(w):rr[at,k]=add(('rotation',obj,order,r,k),powers[r][0] if k==0 else 0)
                self.rotation_specs.append((obj,order,rs,rr))
                for tt in traces:self.rotation.append((sumrow,rr,tuple(tuple(map(Q,a['mul'](self.D,t))) for t in tt)))
        self.nvars=self.high_end+len(self.rotation);self.nrows=len(self.rows)
        # Shared exact moments depend on dimension and phase type, never on v.
        self.moments={}
        for z in set(h[2] for h in self.high):self.moments[z]=tuple(tuple(tuple(map(Q,a['mul'](z,t))) for t in tt) for tt in self.types)
        scales=[1]*w
        for g,c,z in self.low:
            for k,x in enumerate(z):scales[k]=math.lcm(scales[k],x.denominator)
        for moments in self.moments.values():
            for tt in moments:
                for z in tt:
                    for k,x in enumerate(z):scales[k]=math.lcm(scales[k],x.denominator)
        for sumrow,rr,moments in self.rotation:
            for z in moments:
                for k,x in enumerate(z):scales[k]=math.lcm(scales[k],x.denominator)
        for k,x in enumerate(self.D):scales[k]=math.lcm(scales[k],x.denominator)
        self.coordinate_scales=scales
        self.scales=[scales[label[-1]] if label[0] in ('moment','rotation') else 1 for label in self.rows]
        self.moments={z:tuple(tuple(tuple(int(x*scales[k]) for k,x in enumerate(v)) for v in tt) for tt in moments) for z,moments in self.moments.items()}
        self.rhs=[int(b*scale) for b,scale in zip(self.rhs,self.scales)]
        self.low_columns=[self._low_column(g,c,z) for g,c,z in self.low]
        self.rotation_columns=[]
        for sumrow,rr,moments in self.rotation:
            col={sumrow:1}
            for (at,k),row in rr.items():
                value=int(moments[at][k]*scales[k])
                if value:col[row]=value
            self.rotation_columns.append(col)
        self.meta={'height':height,'field':a['field'],'rows':self.nrows,'variables':self.nvars,'low_column_counts':list(map(len,a['columns'])),'high_columns':len(a['high']),'high_duality_orbits':len(self.high),'trace_types':self.nt,'order_bound':self.bound,'duality':duality,'row_scales':self.scales,'domain_sha256':digest([self.low,a['high'],self.orbits,self.types,self.rows,self.rotation])}

    def rhs_for(self,indicators):
        b=list(self.rhs)
        for (power,i,k),row in self.moment_rows.items():
            if power==2:b[row]=int(indicators[i-1])*int(self.D[k]*self.coordinate_scales[k])
        return b

    def _low_column(self,g,c,z):
        col={self.simplex[g]:1}
        for (i,j),row in self.gram.items():
            if c[i]*c[j]:col[row]=c[i]*c[j]
        for (power,i,k),row in self.moment_rows.items():
            value=c[i]*int(z[k]*self.coordinate_scales[k])
            if value:col[row]=value
        for obj,order,rs,rr in self.rotation_specs:
            for at,r in enumerate(rs):
                count=sum(x*y for x,y in zip(self.powers[obj][r],c))
                for k in range(self.width):
                    value=-count*int(z[k]*self.coordinate_scales[k])
                    if value:col[rr[at,k]]=value
        return col

    def column(self,index):
        require(0<=index<self.nvars,'column index outside complete domain')
        if index<self.offset:return self.low_columns[index]
        if index>=self.high_end:return self.rotation_columns[index-self.high_end]
        orbit,ti=divmod(index-self.offset,self.nt);v,gram,z=self.high[orbit];mom=self.moments[z][ti]
        col={self.gram[i,j]:value for (i,j),value in zip(self.gram_pairs,gram) if value}
        for (power,i,k),row in self.moment_rows.items():
            value=v[i-1]*mom[power-1][k]
            if value:col[row]=value
        for obj,order,rs,rr in self.rotation_specs:
            for at,r in enumerate(rs):
                count=sum(self.powers[obj][r][i]*v[i-1] for i in range(1,8))
                for k in range(self.width):
                    value=-count*mom[order//r-1][k]
                    if value:col[rr[at,k]]=value
        return col

    def low_scores(self,y):
        return ((index,sum(y[row]*value for row,value in col.items())) for index,col in enumerate(self.low_columns))

    def high_scores(self,y):
        for orbit,(v,gram,z) in enumerate(self.high):
            constant=sum(y[self.gram[i,j]]*value for (i,j),value in zip(self.gram_pairs,gram))
            coefficients=[[0]*self.width for _ in range(self.height)]
            for (power,i,k),row in self.moment_rows.items():coefficients[power-1][k]+=v[i-1]*y[row]
            for obj,order,rs,rr in self.rotation_specs:
                for at,r in enumerate(rs):
                    count=sum(self.powers[obj][r][i]*v[i-1] for i in range(1,8))
                    for k in range(self.width):coefficients[order//r-1][k]-=count*y[rr[at,k]]
            for ti,mom in enumerate(self.moments[z]):
                value=constant+sum(c*x for cc,xx in zip(coefficients,mom) for c,x in zip(cc,xx))
                yield self.offset+orbit*self.nt+ti,value

    def oracle(self,y,limit=256):
        require(len(y)==self.nrows and all(type(x) is int for x in y),'Farkas vector must be integral and complete')
        worst=[];minimum=0;negative=0
        def include(index,value):
            nonlocal minimum,negative
            minimum=min(minimum,value)
            if value<0:
                negative+=1
                if len(worst)<limit:heapq.heappush(worst,(-value,index))
                elif -value>worst[0][0]:heapq.heapreplace(worst,(-value,index))
        for index,value in self.low_scores(y):include(index,value)
        for index,value in self.high_scores(y):include(index,value)
        for at,col in enumerate(self.rotation_columns):include(self.high_end+at,sum(y[row]*value for row,value in col.items()))
        return {'minimum':minimum,'negative_columns':negative,'violating_columns':[j for _,j in sorted(worst,reverse=True)]}

    def check_farkas(self,y,indicators):
        report=self.oracle(y);b=self.rhs_for(indicators);value=sum(x*z for x,z in zip(b,y))
        require(report['negative_columns']==0 and value<0,'full streaming Farkas verification failed')
        return value

    def check_feasible(self,indices,weights,indicators):
        require(len(indices)==len(weights) and len(set(indices))==len(indices),'invalid feasible support')
        out=[Q(0)]*self.nrows
        for index,weight in zip(indices,weights):
            weight=Q(weight);require(weight>=0,'negative feasible weight')
            for row,value in self.column(index).items():out[row]+=weight*value
        require(out==self.rhs_for(indicators),'exact feasible cone certificate failed')

def load_ring(rid):return next(r for r in json.loads((BASE/'pipeline/census_m3.json').read_text()) if r['id']==rid)
