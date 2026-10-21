"""Exact feasibility of a complete low frame with its integral high domain.

A feasible result is only a necessary-condition witness. An infeasible
result excludes this specific frame, never the entire ring by itself.
"""
import argparse,json,time
from fractions import Fraction as Q
import column_generation as cg
from frame_cone import FrameCone
from exact import require

class FixedFrame(FrameCone):
    def __init__(self,full,index):
        self.__dict__=full.__dict__.copy();require(0<=index<len(full.frames),'fixed frame index invalid')
        self.frame_index=index;self.frames=(full.frames[index],)
        columns=[(1,)+(0,)*7]+[self.low[k][1] for k in self.frames[0]]
        residual=[[int(self.a['B'][i,j])-sum(c[i]*c[j] for c in columns) for j in range(1,8)] for i in range(1,8)]
        import low_failure_exact as lf
        high=[];orbits=[];retained=[]
        for at,(v,gram,z) in enumerate(full.high):
            rem=[list(row) for row in residual]
            for (i,j),value in zip(self.gram_pairs,gram):
                rem[i-1][j-1]-=value
                if i!=j:rem[j-1][i-1]-=value
            if any(x<0 for row in rem for x in row):continue
            psd=lf.positive_semidefinite(tuple(tuple(row) for row in rem))
            require(psd is not None,'integer PSD filter returned indeterminate')
            if psd:high.append(full.high[at]);orbits.append(full.orbits[at]);retained.append(at)
        self.high=high;self.orbits=orbits;self.offset=1;self.high_end=1+len(high)*self.nt;self.nvars=self.high_end+len(self.rotation_columns)
        self.meta={**full.meta,'variables':self.nvars,'low_frames':1,'fixed_frame_index':index,'fixed_frame':self.frames[0],'high_duality_orbits':len(high),'retained_high_orbits':retained,'residual_gram':residual,'high_filter':'integral pair subtraction is entrywise nonnegative and positive semidefinite'}

def verify(source,row):
    require(source['tensor_sha256']==row['tensor_sha256'],'fixed-frame source hash differs')
    full=FrameCone(source['tensor'],row['height']);C=FixedFrame(full,row['frame_index']);require(cg.st.encode(C.meta)==row['metadata'],'fixed-frame metadata differs')
    ep=row['indicators'];require(ep in list(map(list,cg.st.old.ht.indicator_choices(source['tensor']))),'fixed-frame indicators ineligible')
    if row['status']=='exact_feasible_relaxation':C.check_feasible(row['certificate']['indices'],row['certificate']['weights'],ep)
    elif row['status']=='this_frame_indicator_excluded':require(C.check_farkas(row['certificate']['y'],ep)==row['certificate']['bTy'],'fixed-frame separator differs')
    else:raise ValueError('fixed-frame search has no replayable conclusion')

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--from-feasible');g.add_argument('--verify');ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=512);ap.add_argument('--frame',type=int);args=ap.parse_args()
    if args.verify:
        row=json.loads(cg.st.Path(args.verify).read_text());verify(cg.st.load_ring(row['id']),row);print('PASS',row['id'],row['frame_index']);return
    previous=json.loads(cg.st.Path(args.from_feasible).read_text());require(previous['status']=='exact_feasible_relaxation','need an exact feasible seed');source=cg.st.load_ring(previous['id']);full=FrameCone(source['tensor'],args.height)
    c=previous['certificate'];weighted=[(Q(w),i) for i,w in zip(c['indices'],c['weights']) if i<c['metadata']['low_frames']]
    index=args.frame if args.frame is not None else max(weighted)[1];C=FixedFrame(full,index);ep=c['indicators'];start=time.monotonic()
    out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'height':args.height,'frame_index':index,'indicators':ep,'metadata':cg.st.encode(C.meta),'status':'running','scope':'single_frame_pseudo_unitary_induction_relaxation'}
    dest=cg.st.HERE/'fixed_results'/f"{source['id']}_frame{index}_h{args.height}.json";dest.parent.mkdir(parents=True,exist_ok=True)
    def progress(iterations):
        out['iterations']=iterations;out['seconds']=round(time.monotonic()-start,3);dest.write_text(json.dumps(out,separators=(',',':'))+'\n');print(source['id'],index,iterations[-1]['outcome'],iterations[-1]['active_columns'],flush=True)
    negative,feasible,active,iterations=cg.solve_case(C,ep,C.initial_columns(),args.batch,300,progress)
    if feasible is not None:out.update(status='exact_feasible_relaxation',certificate=feasible)
    elif negative is not None:out.update(status='this_frame_indicator_excluded',certificate=negative)
    else:out['status']='search_incomplete'
    if out['status']!='search_incomplete':verify(source,out)
    out['seconds']=round(time.monotonic()-start,3);dest.write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
