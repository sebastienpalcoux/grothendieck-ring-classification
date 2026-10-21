"""Complete distinguished-S-symmetric low-frame obstruction, without high data."""
import argparse,copy,json,os,subprocess
from fractions import Fraction as Q
import streaming as st
from exact import require,vector,discover_roots,check_roots
from rings import Characters,codegree_poly
from partial_s import RealTable
s=st.old.s
KIND='frontier_no_symmetric_low_frame'

def data(R):
    import rank8_signed_bridge
    rank8_signed_bridge.install()
    import biquadratic_traces as bq
    require(len(R)==8 and all(R[i][j]==R[j][i] for i in range(8) for j in range(8)),'commutative rank8 required')
    ch=Characters(R);f,K,ds,D,pD,e=ch.fp();require(f.degree()==4,'quartic FP field required');roots=discover_roots(codegree_poly(R),K)
    require(roots is not None,'codegrees do not split');check_roots(codegree_poly(R),K,roots);require(D in roots and len(roots)==8,'incomplete codegrees');roots.remove(D)
    radicals=[];t=s.Symbol('t')
    for n in (3,5):
        rr=discover_roots(s.Poly(t*t-n,t),K);require(rr is not None and len(rr)==2,'required radical absent');radicals.append(next(x for x in rr if e.sign(x)>0))
    inv=s.Matrix.hstack(*(vector(x,4) for x in [K.one,radicals[0],radicals[1],radicals[0]*radicals[1]])).inv()
    coords=lambda x:tuple(Q(str(c)) for c in inv*vector(x,4))
    columns=[bq.w.core.restriction(ds,D/fc,1,K,ch.C) for fc in roots]
    return dict(factor=f,K=K,ds=ds,D=D,embedding=e,B=ch.C,Gram=ch.C,codegrees=[D]+roots,columns=columns,dimensions=list(map(coords,ds)),global_dimension=coords(D),width=4,field={'degree':4,'radicands':[3,5]})

def witness(R):
    a=data(R);T=RealTable(R,a)
    import low_frames_rank8 as native
    source=st.BASE/'performance/low_frames_rank8.cpp';exe=st.HERE/'low_frames_frontier'
    if not exe.exists() or exe.stat().st_mtime_ns<source.stat().st_mtime_ns:
        tmp=exe.with_name(exe.name+'_'+str(os.getpid()));subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(tmp)],check=True,capture_output=True);os.replace(tmp,exe)
    native.executable=lambda:exe
    frames=native.low_matrices(a['columns'],a['B'],gram_prune=True);surviving=[]
    for i,frame in enumerate(frames):
        labels=T.assignments(frame)
        if labels:surviving.append([i,list(map(list,labels))])
    require(not surviving,'symmetric distinguished low frames survive')
    return {'kind':KIND,'field':a['field'],'low_column_counts':list(map(len,a['columns'])),'columns_sha256':st.digest(a['columns']),'complete_low_frames':len(frames),'complete_frame_sha256':st.digest(frames),'character_table':T.metadata,'surviving_symmetric_frames':0}

def verify_pseudo(R,c):require(c==witness(R),'low symmetric-frame certificate differs')
def install():
    st.old.install();import oriented_extension as oe
    if getattr(oe,'_frontier_low_s_installed',False):return
    original=oe.pseudo_check
    def check(R,c):return verify_pseudo(R,c) if c['kind']==KIND else original(R,c)
    oe.pseudo_check=check;oe._frontier_low_s_installed=True

def verify(R,c):
    install();require(c['kind']==KIND+'_lift','wrong low-frame lift kind');import advanced_criteria;advanced_criteria.verify(R,c['general'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();source=st.load_ring('R8_3_1463');dest=st.HERE/'generic_results/R8_3_1463_low_s.json'
    if args.write:
        prior=json.loads((st.HERE/'generic_results/R8_3_1463_sts_frame_h4.json').read_text());require(prior['tensor_sha256']==source['tensor_sha256'] and prior['status']=='excluded','source lifted result missing')
        general=copy.deepcopy(prior['certificate']['general']);general['sphere']['pseudo']=witness(source['tensor']);c={'kind':KIND+'_lift','general':general};verify(source['tensor'],c)
        row={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'status':'excluded','scope':'general_complex_fusion_category','method':'complete_distinguished_S_symmetric_low_frame_obstruction','certificate':c};dest.write_text(json.dumps(row,separators=(',',':'))+'\n')
    row=json.loads(dest.read_text());require(row['id']==source['id'] and row['tensor_sha256']==source['tensor_sha256']==st.digest(source['tensor']),'source binding mismatch');require(row['status']=='excluded' and row['scope']=='general_complex_fusion_category','wrong low-frame scope');verify(source['tensor'],row['certificate']);print('PASS R8_3_1463 general low-S-symmetric-frame exclusion',flush=True)
if __name__=='__main__':main()
