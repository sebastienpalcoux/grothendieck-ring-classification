"""Exact rank-four tensor presentations for the local signed cover.

The ordinary census and its accessors are in supplementary/census.
No external parameter file or historical catalogue is read here.
"""

def parameter_tensor(tag,p):
    if tag=='S':
        if len(p)!=10:raise ValueError('self-dual parameter length')
        a,b,c,d,e,f,g,h,i,j=p
        return [[[int(v==w) for w in range(4)] for v in range(4)],
            [[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],
            [[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],
            [[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
    if tag=='N':
        if len(p)!=6:raise ValueError('nonself-dual parameter length')
        a,b,c,d,e,f=p
        x=[[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]]
        y=[[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
        return [[[int(v==w) for w in range(4)] for v in range(4)],x,y,list(map(list,zip(*y)))]
    raise ValueError('unknown parameter tag')

