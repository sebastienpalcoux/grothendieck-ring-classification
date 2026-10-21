"""Exact phase compatibility for the two R982 integer/cubic/joint witnesses.

Only these fixed integer restriction multiplicities are tested. Rejection
of both patterns would not exclude the source fusion ring.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,itertools,json,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'global_induction'))
import column_generation as cg
st=cg.st;require=cg.require

class FixedMass:
    def __init__(self,C,fi,record,profile):
        self.C=C;self.fi=fi;self.R=C.R;self.profile=profile
        x=record['original_integer_witness'];fp=record['metadata']['FP_character'];Es=[E for E in range(8)if E!=fp]
        vectors={r['index']:(0,)+tuple(r['vector'])for r in profile['high_vectors']}
        labels=[('high_orbit',tuple(o['indices']),tuple(vectors[j]for j in o['indices']))for o in profile['duality_orbits']]
        labels += [('fusion_coefficient',E,F,G)for E,F in itertools.combinations_with_replacement(Es,2)for G in Es]
        require(st.digest(labels)==record['metadata']['column_labels_sha256']and len(x)==len(labels),'integer label binding differs')
        require(C.meta['frame_character_labels'][fi]==profile['character_labels'],'fixed distinguished labels differ')
        require([(1,)+(0,)*7]+[tuple(C.low[j][1])for j in C.frames[fi]]==list(map(tuple,profile['low_columns'])),'fixed low restrictions differ')
        orbit_lookup={tuple(sorted((0,)+tuple(C.a['high'][j][0])for j in orbit)):i for i,orbit in enumerate(C.orbits)}
        masses=[]
        for label,n in zip(labels,x):
            if label[0]!='high_orbit' or not n:continue
            key=tuple(sorted(label[2]));require(key in orbit_lookup,'integer witness orbit absent from this phase domain');masses.append((orbit_lookup[key],n))
        self.masses=tuple(masses);self.active=[];self.mass_for_local={}
        for row,(oi,n)in enumerate(masses):
            for ti in range(C.nt):
                local=len(self.active);self.active.append(C.offset+oi*C.nt+ti);self.mass_for_local[local]=row
        self.active.extend(range(C.high_end,C.nvars));self.nvars=len(self.active);self.nrows=C.nrows+len(masses)
        self.fixed=C.column(fi)
        self.metadata={'kind':'fixed_integer_central_multiplicities_phase_system','source_phase_metadata':C.meta,
                       'frame_index':fi,'rows':self.nrows,'variables':self.nvars,'nonzero_high_orbits':len(masses),
                       'masses':[list(v)for v in masses],'active_global_indices_sha256':st.digest(self.active),
                       'integer_record_sha256':st.digest(record),'integer_witness_sha256':st.digest(x)}
    def column(self,j):
        col=dict(self.C.column(self.active[j]))
        if j in self.mass_for_local:col[self.C.nrows+self.mass_for_local[j]]=1
        return col
    def rhs_for(self,ep):
        return [v-self.fixed.get(i,0)for i,v in enumerate(self.C.rhs_for(ep))]+[n for oi,n in self.masses]
    def check_feasible(self,c,ep):
        indices=c['indices'];weights=list(map(Q,c['weights']));require(len(indices)==len(weights)and all(v>=0 for v in weights),'invalid phase weights')
        total=[Q(0)]*self.nrows
        for j,x in zip(indices,weights):
            require(0<=j<self.nvars,'invalid phase column index')
            for i,a in self.column(j).items():total[i]+=a*x
        require(total==self.rhs_for(ep),'fixed integer mass phase equations fail')
        self.C.check_feasible([self.fi]+[self.active[j]for j in indices],['1']+list(map(str,weights)),ep)
        return True
    def check_ray(self,c,ep):
        rows=cg.active_rows(self,range(self.nvars));b=self.rhs_for(ep);require(st.old.check(rows,b,c['covector'],self.nvars,False),'fixed-mass separator fails')
        require(sum(a*v for a,v in zip(c['covector'],b))==c['rhs_value']<0,'fixed-mass separator sign differs');return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--height',type=int,default=4);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    source=st.load_ring('R8_3_982');R=source['tensor'];C=cg.cone(R,args.height,'sts_frame');profiles=json.loads((HERE/'R8_3_982_profile.json').read_text())
    require(profiles['tensor_sha256']==source['tensor_sha256'],'fixed-frame source differs');choices=list(map(list,st.old.ht.indicator_choices(R)))
    for fi in(2,3):
        record=json.loads((HERE/f'R8_3_982_frame{fi}.json').read_text());require(record['tensor_sha256']==source['tensor_sha256'],'integer source differs')
        D=FixedMass(C,fi,record,profiles['records'][fi]);path=HERE/f'R8_3_982_frame{fi}_phases_h{args.height}.json'
        if args.write:
            out={'id':source['id'],'tensor_sha256':source['tensor_sha256'],'scope':'compatibility_of_one_fixed_integer_necessary_system_witness','height':args.height,'metadata':D.metadata,'status':'running','attempts':[]}
            def save():path.write_text(json.dumps(out,separators=(',',':'))+'\n')
            save();rows=cg.active_rows(D,range(D.nvars))
            for ep in choices:
                b=D.rhs_for(ep);answer,diag=cg.phase_one(rows,b,D.nvars,120);attempt={'indicators':ep,'lp':diag};out['attempts'].append(attempt)
                print('phase LP',fi,args.height,ep,diag,flush=True)
                if not answer.success:out['status']='numerical_search_incomplete';save();break
                primal=cg.exact_feasible(D,list(range(D.nvars)),b,answer.x[:D.nvars])if answer.fun<1e-7 else None
                if primal is not None:
                    D.check_feasible(primal,ep);attempt.update(outcome='exact_phase_feasible',certificate=primal);out['status']='exact_integer_and_phase_compatible';save();break
                y=cg.reuse_dual(rows,b,D.nvars,answer)
                if y is None:y=st.old.farkas(rows,b,D.nvars,True)
                if y is None:out['status']='exact_reconstruction_incomplete';save();break
                cert={'covector':y,'rhs_value':sum(a*v for a,v in zip(y,b))};D.check_ray(cert,ep);attempt.update(outcome='exact_selected_pattern_obstruction',certificate=cert);save()
            else:out['status']='selected_integer_pattern_phase_incompatible';save()
        else:
            out=json.loads(path.read_text());require(out['tensor_sha256']==source['tensor_sha256']and out['metadata']==D.metadata,'fixed-mass domain binding differs')
            require(out['status']in('exact_integer_and_phase_compatible','selected_integer_pattern_phase_incompatible'),'incomplete fixed-mass phase search')
            for attempt in out['attempts']:
                require(attempt['indicators']in choices,'inadmissible phase indicators')
                if attempt['outcome']=='exact_phase_feasible':D.check_feasible(attempt['certificate'],attempt['indicators'])
                else:D.check_ray(attempt['certificate'],attempt['indicators'])
            if out['status']=='selected_integer_pattern_phase_incompatible':require([a['indicators']for a in out['attempts']]==choices,'indicator coverage incomplete')
            else:require(any(a['outcome']=='exact_phase_feasible'for a in out['attempts']),'missing compatible phase primal')
        print('PASS R982 fixed integer phase compatibility',fi,args.height,out['status'],flush=True)
if __name__=='__main__':main()
