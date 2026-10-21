"""Full low-frame hull with exact partial modular spectral conditions."""
import streaming as st
from frame_cone import FrameCone
from partial_s import character_table,filtered

class SpectralFrameCone(FrameCone):
    def __init__(self,R,height=4,data=None,duality=True):
        a=st.old.setup(R) if data is None else data
        table=character_table(R,a);a,filter_report=filtered(R,a,table)
        super().__init__(R,height,a,duality)
        full_frames=self.frames;kept=[];assignments=[]
        for i,frame in enumerate(full_frames):
            cols=[(1,)+(0,)*7]+[self.low[j][1] for j in frame];labels=table.assignments(cols)
            if labels:kept.append(i);assignments.append([list(p) for p in labels])
        self.frames=tuple(full_frames[i] for i in kept)
        shift=len(self.frames)-self.offset;self.offset=len(self.frames);self.high_end+=shift;self.nvars+=shift
        self.meta={**self.meta,'variables':self.nvars,'low_domain':'complete_frames_with_partial_modular_spectrum','low_frames':len(self.frames),'frames_before_S_symmetry':len(full_frames),'retained_frame_indices':kept,'symmetric_character_assignments':assignments,'frame_domain_sha256':st.digest(self.frames),'partial_S_filter_sha256':st.digest(filter_report),'partial_S_low_rejections':len(filter_report['low_failures']),'partial_S_high_rejections':len(filter_report['high_failures']),'character_table':table.metadata}
