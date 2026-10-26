"""Check every ring hypothesis of the cyclic-stabilizer Morita reduction."""
from pathlib import Path
import hashlib,itertools,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]/'rank12-m1-offline-20261025'
def need(ok,text):
    if not ok:raise ValueError(text)
def main():
    D=json.loads((BASE/'tensors.json').read_text());P={r['id']:r for r in json.loads((BASE/'profile.json').read_text())['records']}
    F=json.loads((BASE/'unresolved_families.json').read_text())['records'];out=[]
    for row in F:
        if row['family']!='D40':continue
        rid=row['id'];R=D[rid];dual=P[rid]['dual'];G=[i for i in range(12)if sum(R[i][dual[i]])==1]
        # Identify the dimension-two objects by the exact fixed positive
        # dimension character 1^4,2^4,sqrt(5)^4 retained in the baseline.
        ds=row['dimensions_in_field'];pol=row['field_polynomial']
        # Its positive field generator is sqrt(5), with descending coefficient
        # lists padded variably; the approximate profile is used only to order
        # candidates, then the exact multiplication character is checked.
        twos=[i for i,d in enumerate(P[rid]['fp_hint'])if abs(d-2)<1e-6]
        odd=[i for i in range(12)if i not in G+twos];need(len(G)==len(twos)==len(odd)==4,'D40 dimension multiplicities')
        vals=[(1,0)if i in G else(2,0)if i in twos else(0,1)for i in range(12)]
        for a,b in itertools.product(range(12),repeat=2):
            lhs=(sum(R[a][b][k]*vals[k][0]for k in range(12)),sum(R[a][b][k]*vals[k][1]for k in range(12)))
            x,y=vals[a];z,w=vals[b];need(lhs==(x*z+5*y*w,x*w+y*z),'exact positive Qsqrt5 character')
        hs=[h for h in G if h and all(R[h][x][x]and R[x][h][x]for x in twos)];need(len(hs)==1,'unique common involution')
        h=hs[0];need(R[h][h][0]==1,'order-two subgroup')
        for x in twos:
            need({g for g in G if R[g][x][x]}=={0,h}=={g for g in G if R[x][g][x]},'exact common cyclic stabilizer')
        need(all(R[h][x]==R[x][h]for x in range(12)),'central involution at ring level')
        need(all(not R[h][x][x]for x in odd),'free action on sqrt5 simples')
        E=sorted(G+twos);degree=[int(i in odd)for i in range(12)]
        need(all(degree[k]==(degree[a]+degree[b])%2 for a,b,k in itertools.product(range(12),repeat=3)if R[a][b][k]),'actual integral C2 grading')
        comm=all(R[a][b]==R[b][a]for a,b in itertools.product(E,repeat=2))
        out.append(dict(id=rid,tensor_sha256=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),integral_subring=E,common_stabilizer=[0,h],integral_subring_commutative=comm,forced_feudal_serf_group='F20'if not comm else'F20_or_D10xC2'))
    need(len(out)==9 and sum(not r['integral_subring_commutative']for r in out)==8,'complete nine-case structural inventory')
    q=dict(status='PASS',exclusions_assigned=0,scope='Hypotheses and Morita structural reduction only; categorical lemma in companion Markdown.',records=out)
    (ROOT/'d40_morita_hypotheses.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
if __name__=='__main__':main()
