"""Complete low-frame convex hull strengthening of central induction.

Every actual low restriction matrix is one enumerated frame. A frame
column is the sum of its seven nonunit low-constituent columns. Taking
their convex hull preserves every genuine solution and adds all joint
row-sum and residual-Gram conditions before the high relaxation.
"""
from native_build import ensure_native
import os,subprocess
from pathlib import Path
import streaming as st
from exact import require

class FrameCone(st.Cone):
    def __init__(self,R,height=4,data=None,duality=True):
        super().__init__(R,height,data,duality)
        import low_frames_rank8 as native
        # Never compile into the immutable published proof root.
        source=st.BASE/'performance/low_frames_rank8.cpp'
        exe=st.HERE/'low_frames_frontier'
        ensure_native(source,exe,flags=('-O3', '-std=c++17'))
        native.executable=lambda:exe
        frames=native.low_matrices(self.a['columns'],self.a['B'],gram_prune=True)
        self.atom_columns=self.low_columns
        lookup={(g,c):i for i,(g,c,z) in enumerate(self.low)}
        self.frames=tuple(tuple(lookup[g,tuple(c)] for g,c in enumerate(frame[1:])) for frame in frames)
        require(len(self.frames)==len(set(self.frames)),'duplicate complete frame')
        oldoffset=self.offset
        self.offset=len(self.frames);self.high_end+=self.offset-oldoffset;self.nvars+=self.offset-oldoffset
        self.meta={**self.meta,'variables':self.nvars,'low_domain':'complete_joint_frames','low_frames':len(self.frames),'frame_domain_sha256':st.digest(self.frames),'frame_constraints':'unit-row equality; repeated-codegree order; residual Gram entrywise nonnegative and positive semidefinite'}
        # Native complete enumeration has been hashed; do not retain a second
        # multi-megabyte cache of the same frame tuples.
        native._cached.cache_clear()

    def column(self,index):
        if index>=self.offset:return super().column(index)
        require(0<=index<len(self.frames),'frame index outside complete domain')
        col={}
        for atom in self.frames[index]:
            for row,value in self.atom_columns[atom].items():col[row]=col.get(row,0)+value
        return {r:v for r,v in col.items() if v}

    def low_scores(self,y):
        scores=[sum(y[r]*v for r,v in c.items()) for c in self.atom_columns]
        return ((j,sum(scores[k] for k in frame)) for j,frame in enumerate(self.frames))

    def initial_columns(self):
        zero=next((j for j,tt in enumerate(self.types) if not any(x for v in tt for x in v)),0)
        n=len(self.frames);sample={i*n//min(128,n) for i in range(min(128,n))} if n else set()
        return sample|set(range(self.high_end,self.nvars))|{self.offset+i*self.nt+zero for i in range(len(self.high))}
