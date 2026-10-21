"""Independent comparison with fixed-low frozen trace systems; no LP search."""
from pathlib import Path
import argparse,itertools,json,math,time
import global_induction as g
from exact import require

def normalized(row,b):
    divisor=math.gcd(int(b),*(int(v) for v in row.values())) or 1
    return {k:int(v)//divisor for k,v in row.items() if v},int(b)//divisor

def verify_case(R,ring,indices=None):
    g.install();a=g.setup(R)
    if a['width']==2:
        import tensor_rotation as engine
        data=g.ht.quadratic_data(R,gram_prune=True);lows=data['lows']
    else:
        import biquadratic_commutative
        engine,_=biquadratic_commutative.install();data=engine.data(R);lows=data['lows']
    require(lows,'no low frames for specialization');indices=indices or sorted({0,len(lows)//2,len(lows)-1});checks=[]
    for index in indices:
        columns=lows[index];L=g.s.Matrix.hstack(*map(g.s.Matrix,columns));ep=g.ht.indicator_choices(R)[0]
        if a['width']==2:
            high=g.ht.high_columns(data,L)[1];A,b,meta=engine.system_rotation(R,data,L,ep,4)
            # The frozen engine also appends rational-indicator inequalities,
            # duality and Galois balance. Compare the common Gram/moment and
            # rotation equations only, dropping their unused slack columns.
            selected=list(range(28+28))+list(range(len(A)-meta['rotation_rows'],len(A)))
            high_count=len(meta['labels']);old_count=len(A[0])-meta['rotation_variables'];gap=old_count-high_count
            keepcols=list(range(high_count))+list(range(old_count,len(A[0])))
            A=[[A[i][j] for j in keepcols] for i in selected];b=[b[i] for i in selected]
        else:
            _,_,high=engine.high_columns(data,columns);A,b,meta=engine.system(R,data,columns,ep,4)
        # Restrict BEFORE constructing the global system, avoiding its much
        # larger full-Gram high domain. Every retained column must be global.
        require(set((tuple(v),tuple(z)) for v,z in high)<=set((tuple(v),tuple(z)) for v,z in a['high']),'fixed-frame high column absent globally')
        local=dict(a,high=high);rows,rhs,ir,gm=g._build(R,local,4);rows,rhs=g.integers(rows,rhs,ir,a['global_dimension'],ep)
        chosen=[];offset=0
        for cs,c in zip(a['columns'],columns[1:]):
            require(tuple(c) in list(map(tuple,cs)),'fixed low column absent');chosen.append(offset+list(map(tuple,cs)).index(tuple(c)));offset+=len(cs)
        start=len(a['columns']);gram=list(itertools.combinations_with_replacement(range(8),2))
        kept=[start+k for k,(i,j) in enumerate(gram) if i>0]+list(range(start+len(gram),len(rows)))
        require(len(kept)==len(A),'fixed-low row count differs')
        for at,j in enumerate(kept):
            rr={k-offset:v for k,v in rows[j].items() if k>=offset};bb=rhs[j]-sum(rows[j].get(k,0) for k in chosen)
            target={k:int(x) for k,x in enumerate(A[at]) if x}
            require(normalized(rr,bb)==normalized(target,b[at]),'fixed-low exact row mismatch '+str((ring,index,at)))
        checks.append({'frame_index':index,'rows_matched':len(A),'high_columns':len(high),'variables':len(A[0])})
    return {'id':ring,'low_frames':len(lows),'checks':checks}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',default='R8_3_1453');ap.add_argument('--write',action='store_true');args=ap.parse_args()
    row=next(r for r in json.loads((g.HERE.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring);start=time.monotonic();report=verify_case(row['tensor'],args.ring)
    out={'result':'PASS','tensor_sha256':row['tensor_sha256'],'report':report,'seconds':round(time.monotonic()-start,3)}
    path=g.HERE/f'global_specialization_{args.ring}.json'
    if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:
        saved=json.loads(path.read_text())
        require(all(saved[key]==out[key] for key in ('result','tensor_sha256','report')),'specialization receipt differs')
    print(json.dumps(out))
if __name__=='__main__':main()
