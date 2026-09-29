"""Ising subcategory projection and exact twist-resolved dimension masses.

Input and proof domains are recovered from the full tensor. The projected
primitive-sixteenth-root phases are complete, and no twist-order cutoff is used.
"""
import argparse,itertools,json,signal,time
from pathlib import Path
import sympy as s
import round3_m4 as ambient
from round3_m4 import (require,Ineligible,Characters,indicator_choices,low_failure,
 high_vectors,Spectrum,rational_rows,cached_farkas,check_farkas)
ROOT=Path(__file__).resolve().parents[1]

def ising_labels(R):
 n=len(R)
 return [(g,ss) for g in range(1,n) for ss in range(1,n) if g!=ss
         and R[g][g]==[int(k==0) for k in range(n)]
         and R[ss][ss]==[int(k==0)+int(k==g) for k in range(n)]
         and R[g][ss]==R[ss][g]==[int(k==ss) for k in range(n)]]

def data_for(R,height,F):
 labels=ising_labels(R)
 if not labels:raise Ineligible('no Ising based subcategory')
 d=ambient.data_for(R,height,F);F=d['F'];C=d['C'];types={}
 for g,ss in labels:
  types[ss]={ep:sorted({tuple(ambient.relative_root(C,F,16,a*k) for k in range(1,height+1)) for a in range(1,16,2)
     if ambient.relative_root(C,F,8,a)+ambient.relative_root(C,F,8,-a)==C(ep)*d['dims'][ss]},key=str) for ep in (-1,1)}
  if any(len(v)!=2 for v in types[ss].values()):raise Ineligible('ambient conductor must retain primitive-eighth-root pairs')
  require(all(t in d['phases'] for vals in types[ss].values() for t in vals),'Ising phase absent from complete ambient domain')
 d.update(ising_labels=labels,ising_types=types);return d

def projection_failure(data,cols):
 C=data['C']
 for g,ss in data['ising_labels']:
  for j,c in enumerate(cols):
   if c[ss] or c[g]>c[0]:return {'kind':'ising_low_support','column':j,'involution':g,'ising_object':ss}
  z=sum((C(c[g])*sum((C(c[i])*data['dims'][i] for i in range(len(c))),C.zero) for c in cols),C.zero)
  if C(2)*z!=data['DD']:return {'kind':'ising_low_twist_mass','involution':g,'ising_object':ss}
 return None

def system(R,data,cols,ep,lab):
    C=data['C'];D=data['DD'];dims=data['dims'];tab=data['tab'];height=data['height'];F=data['F'];types=data['phases'];n=len(R)
    cache=data.setdefault('_branch_cache',{});ck=tuple(map(tuple,cols))
    if ck not in cache:
        G,vectors=high_vectors(data,cols);spec=Spectrum(tab,cols,[(v,None) for v in vectors]);cache[ck]=(G,vectors,spec)
    G,vectors,spec=cache[ck]
    if spec.missing_low:return None,None,{'spectrum':spec.metadata()}
    bad=set(map(tuple,spec.forbidden));vectors=[v for v in vectors if v not in bad]
    labels=[(v,ti) for v in vectors for ti in range(len(types)) if all((not v[g-1] and not v[ss-1]) or (v[g-1] and not v[ss-1] and types[ti]==tuple(C((-1)**k) for k in range(1,height+1))) or (v[ss-1] and not v[g-1] and types[ti] in data['ising_types'][ss][ep[ss-1]]) for g,ss in data['ising_labels'])];nv=len(labels)
    zv={v:sum((C(v[i])*dims[i+1] for i in range(n-1)),C.zero) for v in vectors}
    low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(n)),C.zero) for i in range(n)]
    A=[];b=[]
    def add(co,rhs):
        for row,value in rational_rows(co,rhs,C):A.append(row);b.append(value)
    for i in range(n-1):
        for j in range(i,n-1):add([C(v[i]*v[j]) for v,ti in labels],C(int(G[i,j])))
    for obj in range(1,n):
        for power,target in [(1,0),(2,ep[obj-1])]:add([C(v[obj-1])*zv[v]*types[ti][power-1] for v,ti in labels],C(target)*D-low[obj])
    # Every divisor moment of the cyclic rotation on Hom(1,X^order).
    rotation_blocks=[]
    for obj in range(1,n):
        powers=[[1]+[0]*(n-1)]
        for k in range(height):powers.append([sum(powers[-1][i]*R[i][obj][j] for i in range(n)) for j in range(n)])
        for order in range(3,height+1):
            rs=[int(r) for r in s.divisors(order) if r<order]
            rt=sorted({tuple(ambient.relative_root(C,F,order,a*r) for r in rs) for a in range(order)},key=str)
            old=len(A[0]);count=len(rt)
            for row in A:row.extend([0]*count)
            add([C.zero]*old+[C.one]*count,C(powers[order][0]))
            for j,r in enumerate(rs):
                k=order//r;constant=sum((C(powers[r][i])*low[i] for i in range(n)),C.zero)
                co=[-C(sum(powers[r][i]*v[i-1] for i in range(1,n)))*zv[v]*types[ti][k-1] for v,ti in labels]+[C.zero]*(old-nv)+[D*tt[j] for tt in rt]
                add(co,constant)
            rotation_blocks.append((obj,order,old,count))
    # Galois-orbit count equality, without invalid fixed-trace refinement.
    rows,rhs=ambient.coupled_balance(data,spec,cols,labels,len(A[0]));A+=rows;b+=rhs
    tuples=dict(zip(spec.vectors,spec.types))
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),C.zero)
        coeff=[weights[(0,)+v]*types[ti][0] for v,ti in labels]+[C.zero]*(len(A[0])-nv)
        add(coeff,rhs)
    for g,ss in data['ising_labels']:
        for ty in data['ising_types'][ss][ep[ss-1]]:
            add([C(v[ss-1])*zv[v] if types[ti]==ty else C.zero for v,ti in labels]+[C.zero]*(len(A[0])-nv),D*dims[ss]/C(2))
    return A,b,{'spectrum':spec.metadata(),'vectors':len(vectors),'trace_types':len(types),'variables':len(A[0]),'equations':len(A),'rotation_blocks':rotation_blocks}


def metadata(d):
    return dict(ambient.metadata(d),ising_labels=[list(x) for x in d['ising_labels']],subcategory_twist_pruning=True,twist_mass_constraints=True)


def run(R,height,F,output=None,prepared=None):
    d=prepared if prepared is not None else data_for(R,height,F);report={'kind':'ising_full_character_rotation','version':1,'scope':'pseudo_unitary_necessary','metadata':metadata(d),'branches':[]}
    print(report['metadata'],flush=True)
    for ix,cols in enumerate(d['lows']):
        why=low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
        br={'low':ix,'columns':list(map(list,cols))};report['branches'].append(br)
        if why:br['ordinary']=why;continue
        bad=projection_failure(d,cols)
        if bad:br['ising_projection_failure']=bad;continue
        labs=d['tab'].assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
        for lab in labs:
            for ep in indicator_choices(R):
                A,b,meta=system(R,d,cols,ep,lab);ray=None if A is None else cached_farkas(A,b)
                if ray is not None:check_farkas(A,b,ray)
                rec={'labelling':list(lab),'indicators':list(ep),'system':meta,'excluded':A is None or ray is not None,'ray':ray};br['cases'].append(rec)
                print(ix,lab,ep,meta.get('variables'),rec['excluded'],flush=True)
                if not rec['excluded']:report['outcome']='no_exact_obstruction';return report
        if output:output.write_text(json.dumps(report,separators=(',',':'))+'\n')
    report['outcome']='pseudo_unitary_excluded';return report


def verify(R,c):
    require(c['kind']=='ising_full_character_rotation' and c['version']==1 and c['scope']=='pseudo_unitary_necessary','wrong Ising certificate')
    require(c['outcome']=='pseudo_unitary_excluded','incomplete exclusion')
    md=c['metadata'];d=data_for(R,md['height'],md['F']);require(md==metadata(d),'wrong subfield/trace domain')
    require(len(c['branches'])==len(d['lows']),'missing low frames');rays=0
    for ix,(cols,br) in enumerate(zip(d['lows'],c['branches'])):
        require(br['low']==ix and br['columns']==list(map(list,cols)),'wrong low frame')
        why=low_failure(cols,d['ch'].C,d['ds'],d['D'],d['K'],d['embedding'],d['ch'].du)
        if why:require(br['ordinary']==why,'incorrect ordinary failure');continue
        bad=projection_failure(d,cols)
        if bad:require(br['ising_projection_failure']==bad,'wrong Ising low projection');continue
        labs=d['tab'].assignments(cols);require(br['labellings']==list(map(list,labs)),'missing label assignments')
        expected=[(list(lab),list(ep)) for lab in labs for ep in indicator_choices(R)]
        require([(cc['labelling'],cc['indicators']) for cc in br['cases']]==expected,'missing indicator branches')
        for cc in br['cases']:
            A,b,meta=system(R,d,cols,cc['indicators'],cc['labelling'])
            require(json.loads(json.dumps(meta))==cc['system'] and cc['excluded'] is True,'incorrect system metadata')
            if A is None:require(cc['ray'] is None,'unexpected ray')
            else:check_farkas(A,b,cc['ray']);rays+=1
    return dict(passed=True,low_frames=len(d['lows']),exact_rays=rays,optimizer_used=False)

def verify_general(R,c):
    import galois_pseudo_reduction as reduction
    require(c.get('kind')=='general_ising_projection_rotation' and c.get('version')==1 and c.get('scope')=='general','wrong general Ising certificate')
    red=reduction.verify(R,c['reduction']);out=verify(R,c['pseudo']);return dict(out,reduction=red)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('id');ap.add_argument('--height',type=int,default=3);ap.add_argument('--conductor',type=int,required=True);ap.add_argument('--seconds',type=int,default=800);ap.add_argument('--verify',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==a.id);st=time.monotonic()
    if a.verify:print(verify(R,json.load(open(a.output))));raise SystemExit
    def stop(*_):raise TimeoutError('explicit discovery budget')
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds)
    try:rec=run(R,a.height,a.conductor,a.output)
    except Ineligible as e:rec={'outcome':'ineligible','reason':str(e)}
    except TimeoutError as e:
        rec=json.loads(a.output.read_text()) if a.output.exists() else {};rec.update(outcome='budget_incomplete',reason=str(e))
    finally:signal.alarm(0)
    rec.update(id=a.id,seconds=time.monotonic()-st);a.output.write_text(json.dumps(rec,separators=(',',':'))+'\n');print({k:v for k,v in rec.items() if k!='branches'},flush=True)
