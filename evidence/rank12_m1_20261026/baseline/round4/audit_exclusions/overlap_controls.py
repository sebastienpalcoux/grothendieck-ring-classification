"""Recheck accepted overlapping zero-spectrum and involution-module records."""
from pathlib import Path
import itertools,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
FIRST=BASE/'prior_round/evidence/rank12-m1-offline-20261025'
STRUCT=FIRST/'sources/evidence/rank11_m1_20261023/work/rank11/structural'
sys.path[:0]=[str(FIRST),str(STRUCT)]
import adapted_module
def need(x,m):
    if not x:raise ValueError(m)
data=json.loads((FIRST/'tensors.json').read_text())
zero=[]
for r in json.loads((FIRST/'spectra.json').read_text())['zero_spectrum']['records']:
    c=r.get('certificate')
    if not c:continue
    R=data[r['id']];du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)]
    a,b,d,u,v,w,x,y,z=c['indices'];dot=lambda i,j,k,l:sum(R[i][j][h]*R[k][l][h] for h in range(12))
    need(all([R[u][a][w],R[v][u][b],R[v][w][d],R[x][z][a],R[b][x][y],R[y][z][d]]),'six nonzero boundaries')
    need(sum(R[u][x][k]*R[du[v]][y][k]*R[w][du[z]][k] for k in range(12))==0 and R[b][a][d]==1,'zero spectrum and scalar target')
    # Use the direct Hom-space forms printed in Theorem 6.7, rather than
    # the Frobenius-reciprocity forms in the original checker.
    need(1 in [dot(v,w,b,a),dot(v,u,d,du[a]),dot(b,du[u],d,du[w])],'left nonzero scalar forced')
    need(1 in [dot(b,a,y,z),dot(b,x,d,du[z]),dot(y,du[x],d,du[a])],'right nonzero scalar forced')
    zero.append(r['id'])
classes=json.loads((FIRST/'subrings.json').read_text())['classes'];modules=[]
for r in json.loads((FIRST/'modules.json').read_text())['records']:
    c=r.get('certificate')
    if not c:continue
    need(r['id'].startswith('subring_class_'),'expected lower-rank control')
    index=int(r['id'].rsplit('_',1)[1]);R=classes[index]['tensor']
    need(c['kind']=='involution_module' and c['involution'] in adapted_module.invs(R),'involution control binding')
    # The stored general wrapper calls the certificate involution_module;
    # the older convenience verifier expects a noncommutative-specific name.
    # Replay the checked engine directly, as the integrated verifier does.
    result=adapted_module.solve(R,c['involution'])
    need(result is not None and all(c[k]==v for k,v in result.items()),'all exact module-search metadata')
    budget=1
    for i in c['generators']:budget*=c['candidate_counts'][i]
    need(c['nodes']==budget and not c['feasible'],'complete finite domain, no timeout used')
    modules.append({'class_index':index,'fixed_rank':len(c['fixed']),'candidate_assignments':budget,'fully_exhausted':True})
need(len(zero)==10 and len(modules)==6,'all accepted overlap controls')
report={'status':'PASS','zero_spectrum_ids':zero,'module_controls':modules,'new_disjoint_exclusions':0}
(HERE/'overlap_controls.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS ten exact zero-spectrum witnesses and six complete small module systems')
