"""Fourth pivotal-rotation moment refinement of surviving quartic branches."""
import modular_cyclotomic_trace as m
from modular_cyclotomic_trace import *


def fourth(data,R,ep,A,b,labels):
    C=data['C'];D=data['DD'];dims=data['dims'];n=len(R);cols=current_cols
    low=[sum((C(sum(c[i]*c[j] for c in cols))*dims[j] for j in range(n)),C.zero) for i in range(n)]
    zz={v:sum((C(v[i])*dims[i+1] for i in range(n-1)),C.zero) for v,ti in labels}
    iroot=C.unit**(data['F']//4);require(iroot**2==-C.one,'missing fourth root')
    for obj in range(1,n):
        old=len(A[0]);nw=4
        for row in A:row.extend([0]*nw)
        co=[C(v[obj-1])*zz[v]*data['phases'][ti][3] for v,ti in labels]+[C.zero]*(old-len(labels))+[-D*iroot**j for j in range(4)]
        for row,value in rational_rows(co,-low[obj],C):A.append(row);b.append(value)
        power=[1]+[0]*(n-1)
        for k in range(4):power=[sum(power[i]*R[i][obj][j] for i in range(n)) for j in range(n)]
        A.append([0]*old+[1]*4);b.append(power[0])
        v2=sum(R[obj][obj][i]*([1]+list(ep))[i] for i in range(n))
        A.append([0]*old+[1,-1,1,-1]);b.append(v2)
    return A,b

if __name__=='__main__':
    rings={r['id']:r for r in json.load(open(ROOT/'data/census.json'))};patterns={r['id']:r for r in json.load(open(ROOT/'research/round2_theory/higher_stabilizer_patterns.json'))};out=[]
    for rid in ['R6_4_22','R6_4_91']:
        R=rings[rid]['N'];m.R=R;data=data_for(R,4);tab=table_for(R,data);pat=patterns[rid];objects=[y for y,h in zip(pat['fixed'],pat['cubic_dimensions']) if y in pat['forced_minus_objects'] and h>0]
        ix=1;current_cols=cols=data['lows'][ix];ep=(0,0,1,1,1) if rid.endswith('_22') else (0,0,-1,1,1)
        A0,b0,meta,labels=system(R,data,cols,ep,objects,True);A0,b0=fourth(data,R,ep,A0,b0,labels)
        for lab in tab.assignments(cols):
            A,b,meta=stronger_system(data,tab,cols,lab,[r[:] for r in A0],b0[:],labels);y=farkas(A,b)
            if y is not None:check_farkas(A,b,y)
            rec={'id':rid,'low':ix,'lab':lab,'ep':ep,'bound':data['bound'],'trace_types':len(data['phases']),'rows':len(A),'variables':len(A[0]),'excluded':y is not None,'ray':y};out.append(rec)
            print({k:v for k,v in rec.items() if k!='ray'},flush=True)
            Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
