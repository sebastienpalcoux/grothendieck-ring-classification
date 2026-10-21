exec(open(__file__.replace('second_indicator_probe.py','twist_sums_probe.py')).read().split('for case in cases:')[0])
s=c.s
v0=(0,)+tuple(high[0][0]);v3=(0,)+tuple(high[3][0]);v4=(0,)+tuple(high[4][0]);v5=(0,)+tuple(high[5][0]);ds=[md.value(chs[0],v,K)for v in cols];d0=md.value(chs[0],v0,K);d3=md.value(chs[0],v3,K);d4=md.value(chs[0],v4,K);d5=md.value(chs[0],v5,K)
known=[sum((d*K(v[j])for d,v in zip(ds,cols)),K.zero)+K(4)*d0*K(v0[j])+d3*K(v3[j])for j in range(8)]
for signs in itertools.product([-1,1],repeat=5):
 eps=[1,0,0]+list(signs);A=[[d4*K(v4[j]),d5*K(v5[j]),a['D']*K(eps[j])-known[j]]for j in range(8)]
 # choose independent rows
 det=next(((i,j,A[i][0]*A[j][1]-A[i][1]*A[j][0])for i,j in itertools.combinations(range(8),2)if A[i][0]*A[j][1]!=A[i][1]*A[j][0]),None)
 i,j,d=det;x=(A[i][2]*A[j][1]-A[i][1]*A[j][2])/d;y=(A[i][0]*A[j][2]-A[i][2]*A[j][0])/d
 if all(r[0]*x+r[1]*y==r[2]for r in A): print('INDICATORS',eps,'C2',c.ec(x),'D2',c.ec(y))
