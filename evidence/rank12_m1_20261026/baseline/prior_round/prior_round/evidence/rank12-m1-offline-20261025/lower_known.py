"""Replay all remaining matched excluded lower-rank subrings, then transfer."""
from pathlib import Path
import itertools,json,subprocess,sys,time
from fp import fp_character,require
from field_checks import central_order
from feudal import setup,contradictions
ROOT=Path(__file__).resolve().parent

def main():
    start=time.monotonic();cl=json.loads((ROOT/'subrings.json').read_text())['classes'];cross=json.loads((ROOT/'lower_subring_crosswalk.json').read_text());proofs=[]
    for x in cross:
        rid=x['source_id'];i=x['class_index'];R=cl[i]['tensor'];cert=None
        if rid in ['R10_1_118','R10_1_122','R10_1_180']:
            cert=contradictions(setup(R,True));require(cert is not None,'known Liptrap contradiction reproduced')
        elif rid in ['R6_1_12','R6_1_13']:
            n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)];G=[i for i in range(n)if sum(R[i][du[i]])==1];X=set(range(n))-set(G)
            require(X and {next(k for k in range(n)if R[g][min(X)][k])for g in G}==X,'two FP values gate')
            f,K,u,d,D,emb=fp_character(R);cert=central_order(R,f,K,u,d,D,emb,'two_FP_values_Galois_PU');require(cert is not None,'known dimension-order contradiction reproduced')
        elif rid=='R8_1_17':
            subprocess.run([sys.executable,str(ROOT/'verify_lower_signed.py')],check=True,capture_output=True,text=True)
            cert=dict(kind='frozen_rank8_signed_proof',source='sources/rank8_signed/R8_1_17.json',scope='general_complex_fusion_category')
        else:continue
        S=x['source_record']['tensor'];p=x['basis_map'];n=len(R)
        require(p[0]==0 and sorted(p)==list(range(n)),'unit-preserving subring-to-known-source map')
        require(all(R[a][b][c]==S[p[a]][p[b]][p[c]]for a,b,c in itertools.product(range(n),repeat=3)),'entire lower tensor match')
        proofs.append(dict(class_index=i,known_source_id=rid,certificate=cert));print(rid,'PASS',flush=True)
    (ROOT/'lower_known.json').write_text(json.dumps(dict(class_proofs=proofs,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
    print('DONE',len(proofs),'lower exclusions rechecked','seconds',time.monotonic()-start)
if __name__=='__main__':main()
