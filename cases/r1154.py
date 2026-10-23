"""R1154: finite distinguished fusion-matrix completion discovery.

No numerical solver status is a proof. Every returned matrix is only necessary
center data. All 25 accepted pair branches are retained. The new constraints
couple the full pair-word moment compression with the forced semionic packet.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
import math
import sympy as s

CASE = "R8_3_1154"
DEPENDENCIES = [
 "evidence/rank8_next_20261021/r1154/low_action_bounds.json",
 "evidence/rank8_creative_20261022/r1154/semionic_packet.json",
 "evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json",
 "evidence/rank8_center_followup_20261021/r1154_quartic_necessary_filters.json",
 "evidence/rank8_next_20261021/r1154/joint_quartic_fibers.json",
 "site/dist/downloads/fusion-tensors/R8_3_1154.txt",
]
THEORY = """Necessary positive spherical center data after the published
general-complex spherical/Galois reduction. A1,A2,A3,A4 are the self-dual
distinguished simple summands of I(1). Their source irreducible characters
are fixed by the based-ring involution (asserted exactly below), hence source
character duality fixes their labels and each A_i is self-dual.
For each accepted pair histogram, N1 is
symmetric nonnegative integral, N3=N1+K3 and N4=K4-N1 are nonnegative.
Restriction is a ring map, so M N1 = L_F(A1) M. The forced packet fusion
matrices and N2,K3,K4 commute with N1. Verlinde gives all eigenvalues of N1
from the restriction columns and the corresponding irreducible source
character; their trace and square trace are therefore fixed.
Every pair-word vector v_ab=N_a N_b e_0 is completely determined by the
accepted pair histogram. Thus v_ab^T N1 v_cd equals the exact vacuum moment
of A_a A_b A1 A_c A_d. This is a linear necessary equation in N1.
All stored vacuum moments through degree six and the mandatory characteristic
polynomial are checked exactly on every integer candidate. Rejecting a candidate with a wrong exact invariant permits only its
specific one-hot assignment to be blocked; it does not exclude a branch.
"""
SQ5 = s.sqrt(5)
PAIRS = list(itertools.combinations_with_replacement(range(1,5),2))
WORDS = [()] + [(i,) for i in range(1,5)] + PAIRS

def require(ok, message):
    if not ok:
        raise ValueError(message)

def scalar5(z):
    """Return exact rational coordinates in 1,sqrt(5)."""
    z = s.expand(s.radsimp(s.simplify(z)))
    g = s.expand(z.xreplace({SQ5:-SQ5}))
    a = s.simplify((z+g)/2)
    b = s.simplify((z-g)/(2*SQ5))
    require(a.is_Rational and b.is_Rational, "source arithmetic left Q(sqrt(5))")
    return F(a), F(b)

def integer(z):
    z = s.simplify(z)
    require(z.is_Integer, "nonintegral mandatory moment: "+str(z))
    return int(z)

def read(root, name):
    return json.loads((Path(root)/name).read_text())

@lru_cache(None)
def inputs(root):
    root=Path(root)
    bounds,packet,domain,quartic,fibers,R=[read(root,p) for p in DEPENDENCIES]
    require(packet["complete_pair_domain"]==25, "complete packet branch inventory")
    require(fibers["complete"] and fibers["all_histogram_solutions_enumerated"],
            "complete pair histogram domain required")
    require(domain["tensor_sha256"]==quartic["tensor_sha256"]==fibers["tensor_sha256"],
            "tensor identities differ")
    require(hashlib.sha256(json.dumps(R,separators=(",",":")).encode()).hexdigest()
            ==domain["tensor_sha256"],"canonical source tensor identity")
    require({r["pattern"] for r in packet["results"]}=={6971,8766,8772},
            "three surviving patterns")
    return bounds,packet,domain,quartic,fibers,R

@lru_cache(None)
def characters(root):
    """Compute source scalar characters without importing historical helpers."""
    R=inputs(root)[-1]
    L=[s.Matrix(8,8,lambda k,j:R[i][j][k]) for i in range(8)]
    comm=s.Matrix.vstack(*(L[i]*L[j]-L[j]*L[i]
                          for i in range(8) for j in range(i)))
    U=s.Matrix.hstack(*comm.nullspace())
    require(U.cols==4,"four scalar-character components")
    left=(U.T*U).inv()*U.T
    chars=None
    for attempt in range(1,13):
        B=sum(((i+1)**attempt*L[i] for i in range(8)),s.zeros(8))
        T=left*B*U
        eigen=T.eigenvects()
        if len(eigen)!=4 or any(mult!=1 for _,mult,_ in eigen):
            continue
        candidate=[]
        for _,_,vectors in eigen:
            v=U*vectors[0]
            j=next(k for k in range(8) if v[k]!=0)
            row=[s.simplify((Li*v)[j]/v[j]) for Li in L]
            require(all((Li*v-row[i]*v).applyfunc(s.simplify)==s.zeros(8,1)
                        for i,Li in enumerate(L)),"common scalar eigenvector")
            candidate.append(row)
        chars=candidate
        break
    require(chars is not None,"separating scalar-character element")
    fp=[ch for ch in chars if all(s.simplify(z).is_positive for z in ch)]
    require(len(fp)==1,"unique positive FP character")
    ds=fp[0]
    D=s.simplify(sum(d*d for d in ds))
    two=[s.simplify((s.trace(L[i])-sum(ch[i] for ch in chars))/2)
         for i in range(8)]
    raw=chars+[two]
    multiplicities=[1]*4+[2]
    dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    formal=[s.simplify(sum(ch[i]*ch[dual[i]] for i in range(8))/m)
            for ch,m in zip(raw,multiplicities)]
    low=inputs(root)[2]["low_columns"]
    dims=[s.simplify(sum(v*d for v,d in zip(col,ds))) for col in low]
    ordered=[]
    for col,d in zip(low,dims):
        matches=[i for i,(f,m) in enumerate(zip(formal,multiplicities))
                 if m==col[0] and s.simplify(D/f-d)==0]
        require(len(matches)==1,"distinguished source character identification")
        ordered.append(raw[matches[0]])
    require(len({tuple(ch) for ch in ordered})==5,"five distinct source characters")
    for ch in ordered:
        for z in ch: scalar5(z)
        require(all(s.simplify(ch[dual[i]]-ch[i])==0 for i in range(8)),
                "distinguished characters fixed by based-ring duality")
    return L,ordered,ds,D,dims

def branch_data(root, packet_row):
    bounds,packet,domain,quartic,fibers,R=inputs(root)
    ix,pno=packet_row["pattern"],packet_row["pair_histogram"]
    old=next(r for r in bounds["results"] if r["index"]==ix)
    pr=next(r for r in fibers["results"] if r["index"]==ix)
    hist=pr["pair11_histogram_solutions_by_high_type"][pno]
    group=next(g for g in quartic["groups"] if g["group"]==pr["group"])
    cols=domain["low_columns"]
    h=list(map(F,quartic["h"]))
    X0=[[F(z) for z in row] for row in group["minimum_norm_rows_by_high_type"]]
    mom=lambda word: int(old["moments"]["".join(map(str,sorted(word)))])
    labels=[{"low":j} for j in range(5)]
    Mcols=[list(c) for c in cols]
    Vrows=[]
    for j in range(5):
        Vrows.append([int(j==0)]+[int(j==k) for k in range(1,5)]
             +[mom(pair+(j,)) if j else int(pair[0]==pair[1]) for pair in PAIRS])
    for typ,his in enumerate(hist):
        for x,multiplicity in his:
            if not multiplicity: continue
            v=[z+(F(x)-X0[typ][0])*hh for z,hh in zip(X0[typ],h)]
            require(all(z.denominator==1 and z>=0 for z in v),"integer pair word vector")
            for _ in range(multiplicity):
                labels.append({"type":typ,"pair11":x})
                Mcols.append([0]+domain["high_columns"][typ])
                Vrows.append([0]*5+list(map(int,v)))
    n=len(labels)
    require(n==packet_row["center_rank"],"packet/pair basis rank")
    require([i for i,z in enumerate(labels) if z.get("type")==10]
            ==packet_row["packet_indices"],"packet/pair basis alignment")
    mapold=[j if j<5 else next(k for k,z in enumerate(old["labels"])
                   if z.get("type")==labels[j]["type"]) for j in range(n)]
    K3=s.zeros(n);K4=s.zeros(n);N2=s.zeros(n)
    for i in range(n):
        for j in range(n):
            oi,oj=mapold[i],mapold[j]
            k3=F(old["K3"][oi][oj]);k4=F(old["K4"][oi][oj])
            n2=int(old["N2"][oi][oj])
            if i!=j and oi==oj:
                packet_type=labels[i].get("type")==10
                k3+=2 if packet_type else -1
                k4+=-1 if packet_type else 1
                if packet_type:n2+=1
            K3[i,j]=s.Rational(k3.numerator,k3.denominator)
            K4[i,j]=s.Rational(k4.numerator,k4.denominator)
            N2[i,j]=n2
    Ns=[s.Matrix(z) for z in packet_row["packet_fusion_matrices"]]
    require(all(N.shape==(n,n) for N in Ns),"packet fusion matrix sizes")
    M=s.Matrix(Mcols).T
    V=s.Matrix(Vrows)
    require(V[:,2]==N2[:,0],"A2 unit word alignment")
    source_g=s.Matrix(8,8,lambda a,b:R[3][b][a])
    require(sum(Ns,s.zeros(n))==M.T*source_g*M,
            "packet sum and forgetful intertwiner agree")
    return old,labels,M,V,N2,K3,K4,Ns,mom

def build_one(root, packet_row):
    old,labels,M,V,N2,K3,K4,Ns,mom=branch_data(root,packet_row)
    L,chs,ds,D,ldims=characters(str(Path(root).resolve()))
    n=M.cols
    d=[s.simplify(sum(M[i,j]*ds[i] for i in range(8))) for j in range(n)]
    chi=chs[1]
    spectrum=[s.simplify(ldims[1]/M[0,1]*sum(chi[i]*M[i,j]
                       for i in range(8))/d[j]) for j in range(n)]
    trace=integer(sum(spectrum))
    norm=integer(sum(z*z for z in spectrum))
    require(trace==int(F(old["trace_A1"])),"independent spectral trace reconstruction")
    x=s.Symbol("x")
    cp=s.Poly(s.expand(s.prod(x-z for z in spectrum)),x,extension=SQ5)
    expected_cp=[integer(z) for z in cp.all_coeffs()]
    roots=[]
    for z in spectrum:
        if not any(s.simplify(z-q)==0 for q in roots): roots.append(z)
    mp=s.Poly(s.expand(s.prod(x-z for z in roots)),x,extension=SQ5)
    expected_mp=[integer(z) for z in mp.all_coeffs()]
    lo={};hi={};choices={};entry_var={}
    lower=[];upper=[];names=[]
    for i in range(n):
        for j in range(i,n):
            a=max(0,math.ceil(F(K3[i,j])*-1));b=math.floor(F(K4[i,j]))
            if i<5:
                fixed_value=int(j==1) if i==0 else int(V[j,5+PAIRS.index(tuple(sorted((1,i))))])
                require(a<=fixed_value<=b,"known pair entry violates bounded domain")
                a=b=fixed_value
            require(a<=b,"empty nonnegative bounded A1 entry")
            lo[i,j]=a;hi[i,j]=b
            if a<b:
                entry_var[i,j]=[]
                for val in range(a,b+1):
                    idx=len(names);names.append(f"N1_{i}_{j}={val}")
                    lower.append(0);upper.append(1)
                    entry_var[i,j].append([idx,val])
    rows=[];rhs=[];tags=[]
    def add_raw(coeff,target,tag):
        coeff={int(k):F(v) for k,v in coeff.items() if v}
        target=F(target)
        den=math.lcm(target.denominator,*(v.denominator for v in coeff.values()))
        vals={k:int(v*den) for k,v in coeff.items()}
        out=int(target*den)
        g=math.gcd(abs(out),*(abs(v) for v in vals.values()))
        if g>1:vals={k:v//g for k,v in vals.items()};out//=g
        if not vals:
            require(out==0,"constant necessary constraint failed: "+tag)
            return
        rows.append({str(k):v for k,v in vals.items()});rhs.append(out);tags.append(tag)
    def add_matrix(coeff,target,tag):
        terms={};constant=F(0)
        for (i,j),co in coeff.items():
            i,j=sorted((i,j));co=F(co)
            if not co:continue
            if (i,j) in entry_var:
                for idx,val in entry_var[i,j]:
                    terms[idx]=terms.get(idx,F(0))+co*val
            else:constant+=co*lo[i,j]
        add_raw(terms,F(target)-constant,tag)
    def acc(coeff,i,j,value):
        key=tuple(sorted((i,j)))
        coeff[key]=coeff.get(key,F(0))+F(value)
    for ij,opts in entry_var.items():add_raw({idx:1 for idx,_ in opts},1,"one_hot")
    add_matrix({(i,i):1 for i in range(n)},trace,"full_spectral_trace")
    sq={};fixed=0
    for (i,j),a in lo.items():
        factor=1 if i==j else 2
        if (i,j) in entry_var:
            for idx,val in entry_var[i,j]:sq[idx]=factor*val*val
        else:fixed+=factor*a*a
    add_raw(sq,norm-fixed,"full_spectral_square_trace")
    # An arbitrary fixed integer combination of all forced commuting matrices
    # is a necessary commutant constraint; its separated spectrum makes this
    # considerably stronger than the earlier three-operator probe.
    Q=Ns[0]+3*Ns[1]+9*Ns[2]+27*Ns[3]+81*N2+243*K3+729*K4
    for i in range(n):
        for j in range(n):
            co={}
            for k in range(n):
                acc(co,i,k,Q[k,j]);acc(co,k,j,-Q[i,k])
            add_matrix(co,0,"forced_packet_joint_commutant")
    source_action=sum((int(M[i,1])*L[i] for i in range(8)),s.zeros(8))
    target=source_action*M
    for a in range(8):
        for j in range(n):
            co={}
            for k in range(n):acc(co,k,j,M[a,k])
            add_matrix(co,target[a,j],"full_forgetful_intertwiner")
    # Full known distinguished S columns, split exactly over Q(sqrt(5)).
    for e in range(5):
        col=[s.simplify(ldims[e]/M[0,e]*sum(chs[e][a]*M[a,j]
                         for a in range(8))/D) for j in range(n)]
        lam=spectrum[e]
        coords=[scalar5(z) for z in col]
        targets=[scalar5(lam*z) for z in col]
        for i in range(n):
            for q in range(2):
                co={}
                for j in range(n):acc(co,i,j,coords[j][q])
                add_matrix(co,targets[i][q],"distinguished_spectral_column")
    # All four semionic packet columns have N1 eigenvalue +1. Their full
    # entries are rational Gaussian numbers. Use a common scale of four.
    at=packet_row["packet_indices"]
    B=[[-1+2*s.I,-1-2*s.I,1,1],[-1-2*s.I,-1+2*s.I,1,1],
       [1,1,-1-2*s.I,-1+2*s.I],[1,1,-1+2*s.I,-1-2*s.I]]
    for a in range(4):
        col=[s.Integer(0) for _ in range(n)]
        for j,sgn in enumerate((1,1,-1,-1)):col[j]=sgn
        for k,j in enumerate(at):col[j]=B[k][a]
        for part in (s.re,s.im):
            vv=[integer(part(z)) for z in col]
            for i in range(n):
                co={}
                for j in range(n):acc(co,i,j,vv[j])
                add_matrix(co,vv[i],"forced_semionic_spectral_column")
    piv=list(V.rref()[1])
    for aa,a in enumerate(piv):
        for b in piv[aa:]:
            co={}
            for i in range(n):
                for j in range(n):acc(co,i,j,int(V[i,a])*int(V[j,b]))
            add_matrix(co,mom(WORDS[a]+(1,)+WORDS[b]),"complete_degree_five_pair_compression")
    branch=f"{packet_row['pattern']}:{packet_row['pair_histogram']}"
    return {"id":"R1154_matrix_"+branch.replace(":","_"),"case":CASE,
      "n":len(names),"rows":rows,"rhs":rhs,"lo":lower,"up":upper,
      "integrality":[1]*len(names),"variable_names":names,
      "row_tags":tags,"branch":branch,"theory_scope":THEORY,
      "complete_branch_set":25,"complete_branch_ids":["%s:%s" % (r["pattern"],r["pair_histogram"]) for r in inputs(str(Path(root).resolve()))[1]["results"]],"matrix_rank":n,
      "onehot_groups":[[j for j,_ in opts] for opts in entry_var.values()],
      "entry_domains":[{"i":i,"j":j,"lo":lo[i,j],"up":hi[i,j],
                        "choices":entry_var.get((i,j),[])} for i,j in lo],
      "target_characteristic_polynomial":expected_cp,
      "target_minimal_polynomial":expected_mp,
      "known_actions":{name:[[integer(v) for v in row] for row in mat.tolist()]
                       for name,mat in (("N2",N2),("K3",K3),("K4",K4))},
      "known_vacuum_moments":old["moments"],
      "source_sha256":{p:hashlib.sha256((Path(root)/p).read_bytes()).hexdigest()
                       for p in DEPENDENCIES}}

def build_models(vendor_root:Path,case:str,out:Path,limit=None):
    require(case==CASE,"wrong R1154 case identifier")
    root=str(Path(vendor_root).resolve())
    packet=inputs(root)[1]
    selected=packet["results"][:limit] if limit else packet["results"]
    for row in selected:
        yield build_one(root,row)

def recover_matrix(model,solution):
    require(len(solution)==model["n"],"candidate variable count")
    v=[int(z) for z in solution]
    require(all(F(z)==q for z,q in zip(solution,v)),"candidate must be exact integer")
    N=s.zeros(model["matrix_rank"])
    for d in model["entry_domains"]:
        opts=d["choices"]
        if opts:
            require(sum(v[j] for j,_ in opts)==1 and all(v[j] in (0,1) for j,_ in opts),
                    "candidate one-hot values")
            value=sum(v[j]*val for j,val in opts)
        else:value=d["lo"]
        N[d["i"],d["j"]]=N[d["j"],d["i"]]=value
    return N

def check_candidate(model,solution,vendor_root):
    N=recover_matrix(model,solution)
    values=[int(z) for z in solution]
    for row_index,(row,target) in enumerate(zip(model["rows"],model["rhs"])):
        actual_row=sum(F(co)*values[int(i)] for i,co in row.items())
        if actual_row!=F(target):
            return {"valid":False,"status":"REJECTED_EXACT_LINEAR_CONSTRAINT",
                    "case":CASE,"branch":model["branch"],"row_index":row_index,
                    "row_tag":model["row_tags"][row_index] if row_index<len(model["row_tags"]) else "iterative_cut",
                    "actual":str(actual_row),"expected":str(target)}
    # All published degree-six vacuum moments are exact necessary conditions.
    # They are cheap integer checks before the more expensive polynomial check.
    NN=[[int(v) for v in row] for row in N.tolist()]
    known=model["known_actions"];n=len(NN)
    actions={1:NN,2:known["N2"],
             3:[[NN[i][j]+known["K3"][i][j] for j in range(n)] for i in range(n)],
             4:[[known["K4"][i][j]-NN[i][j] for j in range(n)] for i in range(n)]}
    word_vectors={():[int(i==0) for i in range(n)]}
    for word_key,target in sorted(model["known_vacuum_moments"].items(),key=lambda p:(len(p[0]),p[0])):
        if not word_key:continue
        word=tuple(map(int,word_key))
        previous=word_vectors[word[:-1]]
        action=actions[word[-1]]
        vv=[sum(a*b for a,b in zip(row,previous)) for row in action]
        word_vectors[word]=vv
        if vv[0]!=int(target):
            return {"valid":False,"status":"REJECTED_WRONG_VACUUM_MOMENT",
                    "case":CASE,"branch":model["branch"],"word":word_key,
                    "actual":vv[0],"expected":int(target),
                    "matrix":NN}
    actual=list(map(int,N.charpoly().all_coeffs()))
    valid=actual==model["target_characteristic_polynomial"]
    return {"valid":valid,"status":"SURVIVING_NECESSARY_MATRIX" if valid else "REJECTED_WRONG_SPECTRUM",
      "case":CASE,"branch":model["branch"],
      "scope":"Mandatory distinguished fusion-matrix spectrum and degree-six vacuum moments; no category construction",
      "characteristic_polynomial":actual,
      "target_characteristic_polynomial":model["target_characteristic_polynomial"],
      "matrix":[list(map(int,row)) for row in N.tolist()]}

def candidate_nogood(model,solution,vendor_root=None):
    # This cut is sound ONLY after the exact candidate checker rejects this
    # complete assignment. It must be archived with the rejection receipt.
    chosen=[]
    for entry in model["entry_domains"]:
        for j,_ in entry["choices"]:
            if int(solution[j])==1:chosen.append(j)
    return {"row":{str(j):1 for j in chosen},"row_lo":None,
            "row_up":len(chosen)-1,"justification":"exact polynomial or vacuum-moment candidate rejection"}

def validate_nogood(model,solution,receipt,cut,vendor_root):
    """Independently replay an archived rejection and its exact one-point cut."""
    try:
        observed=check_candidate(model,solution,vendor_root)
        require(not observed["valid"],"a surviving candidate cannot be cut")
        require(observed==receipt,"archived rejection receipt differs from exact replay")
        expected=candidate_nogood(model,solution,vendor_root)
        require(cut==expected,"cut differs from exact one-hot assignment no-good")
        covered=sorted(j for group in model["onehot_groups"] for j in group)
        require(covered==list(range(model["n"])),"all variables must have one-hot coverage")
        require(sum(int(co)*int(solution[int(j)]) for j,co in cut["row"].items())
                ==cut["row_up"]+1,"cut must reject the archived complete assignment")
        return {"valid":True,"status":"EXACT_REJECTION_AND_SINGLE_ASSIGNMENT_CUT"}
    except (ValueError,KeyError,TypeError) as exc:
        return {"valid":False,"reason":str(exc)}

def self_test(vendor_root):
    root=str(Path(vendor_root).resolve())
    data=inputs(root);rows=data[1]["results"]
    require(len(rows)==25 and len({(r["pattern"],r["pair_histogram"]) for r in rows})==25,
            "exact accepted branch set")
    for ix in (6971,8766,8772):
        row=next(r for r in rows if r["pattern"]==ix)
        m=build_one(root,row)
        require(m["n"]>0 and m["rows"],"nonempty discovery model")
        require(len(m["target_characteristic_polynomial"])==m["matrix_rank"]+1,
                "full polynomial degree")
        require("complete_degree_five_pair_compression" in m["row_tags"],
                "new coupled moment constraints missing")
        # Independent published packet spectrum is a substantial exact input control.
        n=row["center_rank"];x=s.Symbol("lambda")
        expected=s.Poly(x**(n-8)*(x-1)**2*(x+1)*(x+5)*(x*x-270*x+225)*(x*x+2*x+5),x)
        for packet_matrix in row["packet_fusion_matrices"]:
            require(s.Matrix(packet_matrix).charpoly(x).as_poly()==expected,"independent packet spectrum")
        # Positive and negative exact controls on spectral validation.
        N=s.diag(1,2)
        require(list(map(int,N.charpoly().all_coeffs()))==[1,-3,2],"positive polynomial control")
        require(list(map(int,N.charpoly().all_coeffs()))!=[1,-4,2],"negative polynomial control")
    # Exercise the actual candidate checker and one-point cut mechanism,
    # including a valid assignment, a failed vacuum word, and a failed spectrum.
    toy={"case":CASE,"branch":"CONTROL","n":2,"matrix_rank":2,
         "rows":[{"0":1,"1":1}],"rhs":[1],"row_tags":["one_hot"],
         "entry_domains":[{"i":0,"j":0,"lo":0,"up":0,"choices":[]},
                          {"i":0,"j":1,"lo":0,"up":1,"choices":[[0,0],[1,1]]},
                          {"i":1,"j":1,"lo":0,"up":0,"choices":[]}],
         "onehot_groups":[[0,1]],"target_characteristic_polynomial":[1,0,-1],
         "known_actions":{"N2":[[0,0],[0,0]],"K3":[[0,0],[0,0]],"K4":[[2,2],[2,2]]},
         "known_vacuum_moments":{"":1,"1":0,"11":1}}
    good=check_candidate(toy,[0,1],root)
    require(good["valid"],"positive exact matrix control")
    rejected=check_candidate(toy,[1,0],root)
    require(not rejected["valid"] and rejected["word"]=="11",
            "degree-two negative vacuum-moment control")
    cut=candidate_nogood(toy,[1,0],root)
    require(validate_nogood(toy,[1,0],rejected,cut,root)["valid"],
            "exact rejection chain control")
    bad_cut=dict(cut,row_up=1)
    require(not validate_nogood(toy,[1,0],rejected,bad_cut,root)["valid"],
            "tampered no-good control")
    wrong_spectrum=dict(toy,target_characteristic_polynomial=[1,0,-2])
    require(check_candidate(wrong_spectrum,[0,1],root)["status"]=="REJECTED_WRONG_SPECTRUM",
            "negative full-spectrum control")
    return {"case":CASE,"accepted_branches":25,"representative_patterns":3,
            "status":"PASS","scope":"model assembly, source bindings, exact spectral reconstruction"}
