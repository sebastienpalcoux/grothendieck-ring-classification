"""Necessary integral fusion matrix for a unique self-dual central lift.

Discovery uses a numerical optimizer. A displayed feasible matrix is checked
entry-by-entry over the integers. Infeasibility is not claimed without an
exact Farkas certificate or a complete exact integer tree.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint,linprog
from scipy.sparse import csc_matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
q=modular.q


def analyze(data,result,path,budget=120,balancing=False):
    rid=data['id'];N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    n=len(N);du=[next(j for j in range(n) if N[i][j][0]) for i in range(n)]
    rows=[(1,0,0,0,0,0,0)]+[tuple(v) for v in data['low']]
    phases=[[8,0,0,0,0,0,0,0]]*len(rows)
    for item in result['support']:
        for v,g,z in data['orbits'][item['orbit']]:
            copies=item['count']*item['multiplicity_unit'];rows.extend([(0,)+tuple(v)]*copies)
            phases.extend([data['phase_records'][item['phase']]['scaled8'][:8]]*copies)
    candidates=[i for i,v in enumerate(rows) if i and sum(v)==1 and rows.count(v)==1 and tuple(v[du[k]] for k in range(n))==v]
    outputs=[];r=len(rows)
    for yi in candidates:
        vx=rows[yi];target=[[sum(vx[a]*v[b]*N[a][b][k] for a in range(n) for b in range(n)) for k in range(n)] for v in rows]
        # Remove the unit row/column, which are prescribed by the simple Y.
        rhs=[]
        for i in range(1,r):rhs.extend(target[i][k]-int(i==yi)*rows[0][k] for k in range(n))
        labels=[(i,j) for i in range(1,r) for j in range(i,r)];cols=[];ubs=[]
        for i,j in labels:
            col=[0]*len(rhs)
            for k in range(n):
                col[(i-1)*n+k]+=rows[j][k]
                if i!=j:col[(j-1)*n+k]+=rows[i][k]
            cols.append(col);ubs.append(min(rhs[k]//c for k,c in enumerate(col) if c>0))
        selected=[j for j,ub in enumerate(ubs) if ub>0]
        cols=[cols[j] for j in selected];labels=[labels[j] for j in selected];ubs=[ubs[j] for j in selected]
        if balancing:
            # Trace balancing into F8. Unique self-dual lift has rational twist here.
            q.require(phases[yi] in ([8,0,0,0,0,0,0,0],[-8,0,0,0,0,0,0,0]),'rational twist of chosen lift')
            twist_y=phases[yi][0]//8
            ds,D,B,zs,transport,signs=q.source_data(N,rid);table=modular.ExactQuadraticCharacterTable(N,ds,5);K=table.K
            domain=next(d for d in json.loads((HERE.parent/'integral_gram'/(rid+'_domains.json')).read_text()) if d['low_index']==result['index'])
            labeling=domain['cases'][result['case']]['label']
            gamma=[]
            for row,phase in zip(rows,phases):
                z=tuple(sum(row[k]*ds[k][j] for k in range(n)) for j in range(2))
                gamma.append([x for j in range(0,8,2) for x in q.base.mul(z,phase[j:j+2],5)])
            for i in range(1,7):
                E=labeling[i];chi=sum((K(vx[k])*table.rows[E][k] for k in range(n)),K.zero)
                value=8*twist_y*table.D*chi/table.codegrees[E]
                pair=modular.quadratic_coeff(value,K);q.require(pair is not None,'real quadratic low balancing RHS')
                rhs.extend(list(pair)+[0]*6)
                for col,(a,b) in zip(cols,labels):
                    col.extend([(gamma[b][k] if a==i else 0)+(gamma[a][k] if b==i and a!=b else 0) for k in range(8)])
            cols,rhs=modular.integral_system(cols,rhs)
        matrix=csc_matrix(np.array(cols,dtype=float).T);start=time.monotonic()
        result_lp=linprog(np.zeros(len(cols)),A_eq=matrix,b_eq=rhs,bounds=list(zip([0]*len(cols),ubs)),method='highs')
        out={'id':rid,'source_file':path.name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'case':result['case'],'center_rank':r,'lift_index':yi,'lift_row':vx,'variables':len(cols),'equations':len(rhs),'lp_status':int(result_lp.status),'balancing':balancing}
        if not result_lp.success:
            sep=q.separate(cols,rhs,[])
            out['exact_farkas']=sep
        else:
            solved=milp(np.zeros(len(cols)),integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),ubs),constraints=LinearConstraint(matrix,rhs,rhs),options={'time_limit':budget})
            out['milp_status']=int(solved.status)
            if solved.x is not None:
                counts=[round(float(x)) for x in solved.x]
                exact=all(sum(c[i]*x for c,x in zip(cols,counts))==b for i,b in enumerate(rhs))
                out['exact_feasible']=exact
                if exact:
                    M=[[0]*r for _ in range(r)];M[0][yi]=M[yi][0]=1
                    for (i,j),count in zip(labels,counts):M[i][j]=M[j][i]=count
                    q.require(all(M[i][j]>=0 and M[i][j]==M[j][i] for i in range(r) for j in range(r)),'symmetric nonnegative integer matrix')
                    q.require([[sum(M[i][j]*rows[j][k] for j in range(r)) for k in range(n)] for i in range(r)]==target,'complete exact fusion restriction equations')
                    out['matrix']=M;out['restriction_rows']=rows
        out['seconds']=time.monotonic()-start;outputs.append(out)
        print(json.dumps({k:v for k,v in out.items() if k not in ('matrix','restriction_rows')}),flush=True)
    return outputs


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--file',default='R7_5_3895_full_field_verlinde_branch0_fp5_words.json');ap.add_argument('--budget',type=int,default=120);ap.add_argument('--balancing',action='store_true');args=ap.parse_args()
    path=HERE.parent/'integral_gram'/args.file;data=json.loads(path.read_text());out=[]
    for result in data['results']:
        if result.get('exact_feasible'):out.extend(analyze(data,result,path,args.budget,args.balancing))
    (HERE/(path.stem+('_balanced_small_lift_matrix.json' if args.balancing else '_small_lift_matrix.json'))).write_text(json.dumps(out,indent=2)+'\n')
    if not out:print(json.dumps({'status':'no unique self-dual simple lift'}))

if __name__=='__main__':main()
