"""Exhaustive bounded nonnegative integer feasibility, with exact pruning."""
from math import gcd
from functools import reduce

def solve(matrix, targets, first_only=True):
    rows=[[(j,int(c)) for j,c in enumerate(row) if c] for row in matrix]
    targets=list(map(int,targets));n=len(matrix[0]);visits=0;leaves=[]
    high=[min(b//c for row,b in zip(rows,targets) for k,c in row if k==j) for j in range(n)]
    def propagate(lo,hi):
      changed=True
      while changed:
        changed=False
        for row,b in zip(rows,targets):
          lower=sum(c*lo[j] for j,c in row);upper=sum(c*hi[j] for j,c in row)
          if lower>b or upper<b:return False
          gap=b-lower;g=reduce(gcd,(c for j,c in row if lo[j]!=hi[j]),0)
          if g and gap%g:return False
          if not g and gap:return False
          for j,c in row:
            if hi[j]==lo[j]:continue
            low=max(lo[j],hi[j]-(upper-b)//c)
            high=min(hi[j],lo[j]+gap//c)
            if low>high:return False
            if low!=lo[j] or high!=hi[j]:
              lo[j]=low;hi[j]=high;changed=True
      return True
    def visit(lo,hi):
      nonlocal visits
      visits+=1
      if not propagate(lo,hi):return False
      choices=[j for j in range(n) if lo[j]!=hi[j]]
      if not choices:
        leaves.append(lo)
        return first_only
      j=min(choices,key=lambda j:(hi[j]-lo[j],-sum(any(k==j for k,c in row) for row in rows)))
      for value in range(lo[j],hi[j]+1):
        l=lo.copy();h=hi.copy();l[j]=h[j]=value
        if visit(l,h):return True
      return False
    visit([0]*n,high)
    return {'solutions':leaves,'nodes':visits,'complete':not leaves or not first_only}
