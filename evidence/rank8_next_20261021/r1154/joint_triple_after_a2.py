"""Joint sixth-moment fibers on the four patterns left by the forced A2 action.

Every central fusion word is constant on the four high10 copies: their
difference subspace is the forced hidden A2 eigenvalue-minus-one projector,
orthogonal to the vacuum-generated subspace. The scalar triple residual
therefore has one common coordinate on these four copies.
"""
import sys,json,math,time,hashlib,argparse
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
UPSTREAM=Path(__file__).resolve().with_name('triple_projection.py')
exec(compile(UPSTREAM.read_text().split('failures=[];')[0],str(UPSTREAM),'exec'))
sys.path.insert(0,str(HERE));from joint_quartic_fibers import histogram_options
@lru_cache(None)
def restriction(word):
    z=(1,0,0,0,0,0,0,0)
    for ii in word:
        y=cols[ii];z=tuple(sum(z[i]*y[j]*R[i][j][k]for i in range(8)for j in range(8))for k in range(8))
    return z
@lru_cache(None)
def augmented(signature):
    moments=dict(zip(moment_coefficients,signature));moment=lambda w:moments[tuple(sorted(w))]
    G=s.Matrix(15,15,lambda i,j:moment(words[i]+words[j]));FW=s.Matrix([restriction(w)for w in words])
    GA=G.row_join(FW).col_join(FW.T.row_join(a['Gram']));inds=list(GA.rref()[1]);need(len(inds)==9,'augmented rank nine')
    V=s.Matrix(15,20,lambda i,j:moment(words[i]+triples[j])).col_join(s.Matrix([restriction(t)for t in triples]).T)
    C=GA.extract(inds,inds).inv()*V.extract(inds,list(range(20)))
    H=s.Matrix(20,20,lambda i,j:moment(triples[i]+triples[j]))-V.extract(inds,list(range(20))).T*C
    alpha=F(H[7,7]);hh=[F(x/alpha)for x in H[7,:]]
    need(H==s.Matrix(hh)*s.Matrix(hh).T*alpha,'rank-one exact triple residual')
    return inds,[[F(v)for v in rr]for rr in C.tolist()],alpha,hh,moments
@lru_cache(None)
def row_data(group,typ,pair11,signature):
    inds,C,alpha,hh,moments=augmented(signature);X0=[[F(x)for x in rr]for rr in groups[group]['minimum_norm_rows_by_high_type']];h=list(map(F,quartic['h']))
    xs=[v+(F(pair11)-X0[typ][0])*h[j]for j,v in enumerate(X0[typ])]
    row=tuple([F(0)]*5+xs+[F(0)]+list(map(F,domain['high_columns'][typ])))
    vb=[row[i]for i in inds];zs=tuple(sum(x*C[k][j]for k,x in enumerate(vb))for j in range(20));q=zs[7]
    B=math.isqrt(alpha.numerator//alpha.denominator)+2;center=q.numerator//q.denominator
    vals=[]
    for x in range(max(0,center-B),center+B+2):
        t=F(x)-q
        if t*t>alpha:continue
        vv=[z+t*h for z,h in zip(zs,hh)]
        if all(v.denominator==1 and v>=0 for v in vv):vals.append(x)
    # These are the four independent high-coordinate columns in the augmented basis.
    basis=tuple(int(row[i])for i in inds[5:]);need(len(basis)==4,'high basis dimension')
    return row,basis,q,tuple(vals)
def solve(histograms,group,signature,all_solutions=False):
    inds,C,alpha,hh,moments=augmented(signature)
    rr=[]
    for typ,hist in enumerate(histograms):
        for x,n in hist:
            if n:
                row,basis,q,vals=row_data(group,typ,x,signature)
                if not vals:return None,{'reason':'empty_coordinate_domain','type':typ,'pair11':x,'nodes':0}
                rr.append((typ,x,n,row,basis,q,vals))
    den=math.lcm(alpha.denominator,*(z[5].denominator for z in rr));norm=alpha*den*den;need(norm.denominator==1,'scaled norm integer');norm=int(norm)
    bases=[min((int(den*(F(x)-r[5]))for x in r[6]),key=lambda z:z*z)for r in rr]
    minimum=sum(r[2]*z*z for r,z in zip(rr,bases))
    if minimum>norm:return None,{'reason':'coordinate_minimum_norm','nodes':0}
    if (norm-minimum)%den:return None,{'reason':'norm_congruence','nodes':0}
    budget=(norm-minimum)//den
    rawtarget=[-sum(r[2]*r[4][j]*z for r,z in zip(rr,bases))for j in range(4)]
    if any(z%den for z in rawtarget):return None,{'reason':'linear_congruence','nodes':0}
    target=tuple(z//den for z in rawtarget);types=[]
    for i,(r,z0)in enumerate(zip(rr,bases)):
        typ,x,n,row,basis,q,vals=r;zs=[int(den*(F(x)-q))for x in vals];ys=[(z-z0)//den for z in zs];costs=[(z*z-z0*z0)//den for z in zs]
        need(all(z>=0 for z in costs),'nonnegative excess costs')
        if typ==10:
            options=[(n*y,n*dc,tuple(n if k==j else 0 for k in range(len(vals))))for j,(y,dc)in enumerate(zip(ys,costs))if n*dc<=budget]
        else:options=histogram_options(n,ys,costs,budget)
        dedup={}
        for sy,cost,his in options:dedup.setdefault((sy,cost),(sy,cost,his))
        os=options if all_solutions else list(dedup.values());os.sort(key=lambda z:z[1]);types.append((i,basis,os))
    types.sort(key=lambda z:(sum(v!=0 for v in z[1]),len(z[2]),-max(z[1])))
    N=len(types);lows=[[0]*5 for _ in range(N+1)];highs=[[0]*5 for _ in range(N+1)]
    for k in range(N-1,-1,-1):
        i,col,os=types[k]
        for j in range(5):
            vs=[cost if j==4 else sy*col[j]for sy,cost,his in os];lows[k][j]=lows[k+1][j]+min(vs);highs[k][j]=highs[k+1][j]+max(vs)
    nodes=0
    @lru_cache(None)
    def search(k,state):
        nonlocal nodes;nodes+=1
        if any(not lows[k][j]<=state[j]<=highs[k][j]for j in range(5)):return ()
        if k==N:return ((),) if all(v==0 for v in state)else ()
        i,col,os=types[k]
        answers=[]
        for sy,cost,his in os:
            if cost>state[4]:continue
            nxt=tuple(state[j]-sy*col[j]for j in range(4))+(state[4]-cost,)
            tails=search(k+1,nxt)
            for tail in tails:
                answers.append((his,)+tail)
                if not all_solutions:return tuple(answers)
        return tuple(answers)
    answers=search(0,target+(budget,));stats={'nodes':nodes,'budget':budget,'type_options':[len(os)for i,col,os in types]}
    if not answers:return None,dict(stats,reason='complete_joint_triple_fiber_empty')
    witnesses=[]
    for ans in answers:
        witness=[];linear=[F(0)]*23;norm=F(0)
        for (i,col,os),his in zip(types,ans):
            typ,x,n,row,basis,q,vals=rr[i];need(sum(his)==n,'histogram count');entries=[]
            for val,m in zip(vals,his):
                if m:entries.append([val,m]);t=F(val)-q;norm+=m*t*t;linear=[v+m*t*y for v,y in zip(linear,row)]
            witness.append({'type':typ,'pair11':x,'triple133_histogram':entries})
        need(norm==alpha and all(v==0 for v in linear),'direct full 23-coordinate and norm witness verification')
        witnesses.append(sorted(witness,key=lambda z:(z['type'],z['pair11'])))
    stats['witness_count']=len(witnesses)
    return witnesses,dict(stats,reason='exact_joint_triple_fiber_witness')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int);ap.add_argument('--output',type=Path);ap.add_argument('--all-solutions',action='store_true');args=ap.parse_args();out=[];start=time.monotonic();done=False
    tracepath=HERE/'single_induction_trace.json';trace=json.load(open(tracepath));need(trace['verifier_sha256']==digest(HERE/'single_induction_trace.py'),'single induction trace binding')
    actpath=HERE/'a2_action_probe.json';act=json.load(open(actpath));need(act['verifier_sha256']==digest(HERE/'a2_action_probe.py'),'forced A2 binding')
    allowed={(z['index'],z['histogram_solution'])for z in act['results']if z['status']=='passes_fixed_action'and z['index']in trace['surviving_pattern_indices']};need(len(allowed)==37,'exact four-pattern domain')
    need(values[15]==list(map(K,[1,1,-1,-1,0])),'all distinguished fusion actions are scalar on the A2 minus-one eigenspace')
    for row in fibers['results']:
        if row['status']!='exact_joint_fiber_witness':continue
        ix=row['index'];ns=[1]+domain['completions'][ix];signature=[]
        for word,(co,den)in moment_coefficients.items():
            irr=sum(n*v[0]for n,v in zip(ns,co));rat=sum(n*v[1]for n,v in zip(ns,co));need(irr==0 and rat%den==0,'integer moments');signature.append(rat//den)
        signature=tuple(signature)
        for number,histograms in enumerate(row['pair11_histogram_solutions_by_high_type']):
            if (ix,number)not in allowed:continue
            wit,stats=solve(histograms,row['group'],signature,args.all_solutions);rec={'index':ix,'histogram_solution':number,'group':row['group'],'status':stats.pop('reason'),'statistics':stats}
            if wit is not None:rec['witnesses']=wit
            out.append(rec);print(json.dumps({'done':len(out),'index':ix,'histogram_solution':number,'status':rec['status'],'nodes':stats['nodes'],'seconds':round(time.monotonic()-start,2)}),file=sys.stderr,flush=True)
            if args.limit and len(out)>=args.limit:done=True;break
        if done:break
    survivors=[z for z in out if z['status']=='exact_joint_triple_fiber_witness'];result={'schema':'r1154-joint-triple-after-a2/v1','id':r['id'],'tensor_sha256':r['tensor_sha256'],'scope':'Necessary exact pair/triple product Gram and forgetful completion with the forced A2 difference projector; no categorification assertion','complete':len(out)==len(allowed),'all_histogram_solutions_enumerated':args.all_solutions,'processed_pair_completions':len(out),'surviving_pair_completions':len(survivors),'remaining_patterns':len(set(z['index']for z in survivors)),'results':out,'source_sha256':{p.relative_to(ROOT).as_posix():digest(p)for p in [domainpath,fiberpath,quarticpath,UPSTREAM,tracepath,actpath]},'verifier_sha256':digest(Path(__file__))};text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')
if __name__=='__main__':main()
