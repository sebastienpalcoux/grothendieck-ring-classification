"""Additional unitary models: Rep(AGL(1,5)) and an Izumi C2-equivariantization."""
from models import *

def frobenius20():
    # Four one-dimensional characters form C4; rho has degree 4.
    R=ty(True);R[4][4][4]=3;return R

def izumi_equivariantization():
    # Basis 1,g,V,X,Y.  The order-two symmetry in Izumi Example 13.10
    # acts by inversion on C3 and by a reflection on K_0.
    R=[[[0]*5 for j in range(5)] for i in range(5)]
    for i in range(5):R[0][i][i]=R[i][0][i]=1
    def put(i,j,values):R[i][j]=list(values);R[j][i]=list(values)
    put(1,1,[1,0,0,0,0]);put(1,2,[0,0,1,0,0]);put(1,3,[0,0,0,0,1]);put(1,4,[0,0,0,1,0])
    put(2,2,[1,1,1,0,0]);put(2,3,[0,0,0,1,1]);put(2,4,[0,0,0,1,1])
    put(3,3,[1,0,1,3,3]);put(4,4,[1,0,1,3,3]);put(3,4,[0,1,1,3,3])
    return R
