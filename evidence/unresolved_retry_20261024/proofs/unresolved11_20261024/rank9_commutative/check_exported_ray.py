"""Dependency-free exact check of an exported matrix and Farkas ray.

The categorical system reconstruction remains a separate proof obligation.
"""
import gzip,hashlib,json,sys
path=sys.argv[1]
with gzip.open(path,'rt') as f:x=json.load(f)
A,b,y=x['A'],x['b'],x['ray']
if not(len(A)==len(b)==len(y)):raise ValueError('Incorrect row count')
digest=hashlib.sha256(json.dumps({'A':A,'b':b},separators=(',',':')).encode()).hexdigest()
if digest!=x['system_sha256']:raise ValueError('System hash mismatch')
bTy=sum(a*c for a,c in zip(b,y))
ATy=[0]*len(A[0])
for row,c in zip(A,y):
    if c:
        for j,a in enumerate(row):ATy[j]+=a*c
if bTy>=0 or min(ATy)<0:raise ValueError('Invalid exact separator')
print(json.dumps({'status':'PASS','rows':len(A),'variables':len(A[0]),'bTy':bTy,'minimum_ATy':min(ATy),'system_sha256':digest}))
