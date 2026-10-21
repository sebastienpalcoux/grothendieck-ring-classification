"""Independent fifth-moment and hidden-projector audit of R721 center actions.
No follow-up producer functions are imported. Scratch-only; --write saves receipt.
"""
import argparse,hashlib,itertools,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root',type=Path,default=Path.cwd())
ap.add_argument('--write',action='store_true')
args=ap.parse_args();root=args.root.resolve();p=root/'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0,str(p))
import central_support as c
import character_modular as md
import rotation_search as base
base.install();s=c.s

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(f):return json.loads(f.read_text())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rat(z):
    co=list(map(s.Rational,c.ec(z)));need(len(co)<=1,'rational spectral moment');return co[0] if co else s.S.Zero
old=read(HERE/'quartic_center_independent_review.json')
producer=read(HERE/'r721_center_extension_receipt.json')
record=next(r for r in read(c.OLD.parent/'pipeline/census_m3.json') if r['id']=='R8_3_721')
R=record['tensor'];a=c.w.data(R);K=a['K'];low=a['lows'][10];chars=md.characters(R,a)
need(all(ch[j]==ch[a['du'][j]] for ch in chars for j in range(8)),'all distinguished objects selfdual')
_,high=md.full.base.grams.high_columns(a,s.Matrix.hstack(*map(s.Matrix,low)))
pairs=[tuple(v) for v in old['R721']['pair_order']];words=[()]+[(i,) for i in range(1,5)]+pairs
summary=[]
for previous in old['R721']['cases']:
    counts=previous['multiplicities'];perm=previous['permutation'];types=previous['high_types']
    cols=list(map(tuple,low))+[(0,)+tuple(high[t][0]) for t in types];n=len(cols)
    dimensions=[sum((K(m)*di for m,di in zip(v,a['ds'])),K.zero) for v in cols]
    lambdas=[tuple(a['D']/a['codegrees'][perm.index(i)]/K(a['multiplicities'][perm.index(i)])*md.value(chars[perm.index(i)],v,K)/d for i in range(1,5)) for v,d in zip(cols,dimensions)]
    packets={}
    for lam,d in zip(lambdas,dimensions):
        if lam not in packets:packets[lam]=[0,K.zero]
        packets[lam][0]+=1;packets[lam][1]+=d*d/a['D']**2
    need(len(packets)==9 and all(a['embedding'].sign(w)>0 for m,w in packets.values()),'exact nine positive vacuum packets')
    moments={}
    def moment(word):
        key=tuple(sorted(word))
        if key not in moments:
            z=K.zero
            for lam,(m,w) in packets.items():
                term=w
                for i in key:term*=lam[i-1]
                z+=term
            moments[key]=rat(z)
        return moments[key]
    C={(i,j,k):moment((i,j,k)) for i,j,k in itertools.product(range(1,5),repeat=3)}
    X=s.Matrix(previous['unique_high_pair_coefficients'])
    products=s.Matrix(n,10,lambda j,k:int(pairs[k][0]==pairs[k][1]) if j==0 else C[pairs[k]+(j,)] if j<5 else X[j-5,k])
    W=s.eye(n)[:,:5].row_join(products)
    need(W.rank()==9,'complete vacuum cyclic span')
    need(W.T*W==s.Matrix(15,15,lambda i,j:moment(words[i]+words[j])),'full redundant word Gram')
    # Different construction: use all 15 words and their Moore-Penrose inverse.
    Winv=W.pinv();P=W*Winv;Q=s.eye(n)-P
    F=[Winv.T*s.Matrix(15,15,lambda j,k:moment(words[j]+(i,)+words[k]))*Winv for i in range(1,5)]
    A=[5+j for j,t in enumerate(types) if t in (0,1)]
    Cpos=[5+j for j,t in enumerate(types) if t in (4,8)]
    D=[5+j for j,t in enumerate(types) if t==5]
    def projector(positions):
        E=s.zeros(n)
        for i,j in itertools.product(positions,repeat=2):E[i,j]=int(i==j)-s.Rational(1,len(positions))
        return E
    EA,EC,ED=map(projector,(A,Cpos,D))
    need(Q==EA+EC+ED,'hidden support exactly equal-restriction differences')
    expected={(K(-1),K(0),K(0),K(0)):7}
    if len(A)>1:expected[tuple(map(K,(1,-2,-2,1)))]=len(A)-1
    if len(Cpos)>1:expected[tuple(map(K,(1,0,0,-1)))]=len(Cpos)-1
    need({lam:m-1 for lam,(m,w) in packets.items() if m>1}==expected,'complete hidden joint eigenvalue multiplicities')
    case=next(z for z in producer['case_results'] if z['counts']==counts and z['permutation']==perm)
    if len(A)!=len(Cpos):
        block=F[1].extract(Cpos,Cpos) if len(A)==1 else (F[0]+F[1]-Q).extract(A,A)
        need(all(x.q==2 for x in block),'forced half-integer action entry')
        need(case['status']=='exact_necessary_pattern_exclusion','producer exclusion scope')
        summary.append({'permutation':perm,'center_rank':n,'counts':counts,'status':'pattern_excluded','fixed_block':[[str(x) for x in row] for row in block.tolist()]})
        continue
    def matchings(positions):
        yield ()
        edges=list(itertools.combinations(positions,2))
        for edge in edges:yield (edge,)
        for e,f in itertools.combinations(edges,2):
            if len(set(e+f))==4:yield (e,f)
    def matching(edges):
        E=s.zeros(n)
        for i,j in edges:
            E[i,i]+=s.Rational(1,2);E[j,j]+=s.Rational(1,2);E[i,j]-=s.Rational(1,2);E[j,i]-=s.Rational(1,2)
        return E
    choices=[(s.zeros(n),s.zeros(n))] if len(A)==1 else [(matching(ma)+EC-matching(mc),EA-matching(ma)+matching(mc)) for ma in matchings(A) for mc in matchings(Cpos) if len(ma)==len(mc)]
    allNs=[];M=s.Matrix.hstack(*map(s.Matrix,cols))
    for PA,PC in choices:
        need(PA*PA==PA and PC*PC==PC and PA*PC==s.zeros(n),'orthogonal hidden projectors')
        need(s.trace(PA)==len(A)-1 and s.trace(PC)==len(Cpos)-1,'hidden ranks')
        Ns=[F[0]-Q+2*(PA+PC),F[1]-2*PA,F[2]-2*PA,F[3]+PA-PC]
        for i,N in enumerate(Ns,1):
            need(N.T==N and all(x.q==1 and x>=0 for x in N),'nonnegative integer symmetric action')
            need(N[:,0]==s.eye(n)[:,i],'unit column')
            need(all(N[:,j]==products[:,pairs.index(tuple(sorted((i,j))))] for j in range(1,5)),'all known product columns')
            L=s.Matrix(8,8,lambda k,j:sum(low[i][u]*R[u][j][k] for u in range(8)))
            need(M*N==L*M,'forgetful action')
            for j,other in enumerate(Ns,1):
                need(N*other==other*N,'pairwise commutation')
                need(s.trace(N*other)==rat(sum((K(m)*lam[i-1]*lam[j-1] for lam,(m,w) in packets.items()),K.zero)),'all joint second spectral traces')
        allNs.append([[[int(x) for x in row] for row in N.tolist()] for N in Ns])
    recorded=[z['matrices'] for z in case['witnesses']] if n==22 else [case['matrices']]
    need(sorted(map(json.dumps,allNs))==sorted(map(json.dumps,recorded)),'complete independently reconstructed action tuples')
    summary.append({'permutation':perm,'center_rank':n,'counts':counts,'status':'necessary_actions_only','labelled_action_tuples':len(allNs),'matrix_set_sha256':hashlib.sha256(json.dumps(sorted(map(json.dumps,allNs))).encode()).hexdigest()})
# Actual Z(Vec(S3)): electric tensor actions on each flux centralizer block.
Ns=[s.diag(s.Matrix([[0,1,0],[1,0,0],[0,0,1]]),s.Matrix([[0,1],[1,0]]),s.eye(3)),s.diag(s.Matrix([[0,0,1],[0,0,1],[1,1,1]]),s.ones(2),s.ones(3)-s.eye(3))]
V=s.eye(8)[:,:3];control_packets=[((1,2),s.Rational(1,6)),((-1,0),s.Rational(1,2)),((1,-1),s.Rational(1,3))]
cwords=[(),(0,),(1,)]
for i,N in enumerate(Ns):
    B=s.zeros(3)
    for j,k in itertools.product(range(3),repeat=2):
        for lam,w in control_packets:
            value=w
            for t in cwords[j]+(i,)+cwords[k]:value*=lam[t]
            B[j,k]+=value
    # Word columns are e0, N_sign e0, N_standard e0, here exactly V.
    need(V*B*V.T==(V*V.T)*N*(V*V.T),'actual S3 cyclic moment normalization')
inputs=[HERE/'quartic_center_independent_review.py',HERE/'quartic_center_independent_review.json',HERE/'r721_center_extension.py',HERE/'r721_center_extension_receipt.json',HERE/'R721_CENTER_EXTENSION.md']
result={'status':'PASS','scope':'Two of four R721 center Gram patterns excluded; other two have necessary action data only. No source-ring exclusion, full center ring, or model.','cases':summary,'S3_fifth_moment_control':'PASS','projection_exhaustion':'Reviewed exact row-norm proof: diagonal quarter residues saturate projection rows; nonnegative N2 forces matchings; N4 forces P=EA+EC; equal matching sizes give 1+36+9.','source_sha256':{'followup/'+x.name:sha(x) for x in inputs},'reviewer_sha256':sha(Path(__file__))}
target=HERE/'r721_extension_independent_review.json'
if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
else:need(read(target)==result,'independent receipt changed')
print(json.dumps({'status':'PASS','cases':len(summary),'pattern_exclusions':2,'remaining_Gram_patterns':2,'S3_control':'PASS','receipt':target.name}))
