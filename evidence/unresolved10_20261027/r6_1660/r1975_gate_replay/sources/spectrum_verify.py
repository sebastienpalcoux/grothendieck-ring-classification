def require(b,msg):
 if not b:raise ValueError(msg)
def verify(R,c):
    n=len(R); inds=c['indices']
    require(all(type(i)is int and 0<=i<n for i in inds),'index bounds')
    d=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    dot=lambda i,j,k,l:sum(R[i][j][h]*R[k][l][h] for h in range(n))
    if c['kind']=='zero_spectrum':
        require(len(inds)==9,'nine indices');a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==0,'empty spectrum')
        require(R[b][a][c0]==1,'distinguished multiplicity one')
        require(1 in [dot(v,u,c0,d[a]),dot(b,d[u],c0,d[w]),dot(d[v],b,w,d[a])],'left forced invertible')
        require(1 in [dot(b,x,c0,d[z]),dot(y,d[x],c0,d[a]),dot(d[b],y,a,d[z])],'right forced invertible')
    else:
        require(c['kind']=='one_spectrum' and len(inds)==10,'ten indices');q,a,b,c0,u,v,w,x,y,z=inds
        require(all([R[u][a][w],R[v][u][b],R[v][w][c0],R[x][z][a],R[b][x][y],R[y][z][c0]]),'six nonzero boundary spaces')
        require(sum(R[u][x][k]*R[d[v]][y][k]*R[w][d[z]][k] for k in range(n))==1,'equation6.13')
        require(R[u][x][q]==R[d[v]][y][q]==R[w][d[z]][q]==1,'equation6.14')
        require(R[b][a][c0]==0,'equation6.15')
        require(1 in [dot(v,u,y,d[x]),dot(v,q,b,x),dot(b,d[u],y,d[q])],'equation6.16')
        require(1 in [dot(v,q,c0,d[z]),dot(v,w,y,z),dot(y,d[q],c0,d[w])],'equation6.17')
        require(1 in [dot(u,x,w,d[z]),dot(u,a,q,z),dot(q,d[x],w,d[a])],'equation6.18')
    return True

