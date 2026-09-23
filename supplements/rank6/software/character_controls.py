"""Exact character-induction mutations and multiplicity-two model controls."""
import json,time,copy
from pathlib import Path
from exact import require,VerificationError
from character_induction import reciprocity_data,certificate as discover,verify as verify_pseudo,pruned_system,check_farkas,indicator_choices
from exceptional_g2 import construct
from prepare import key
from oriented_signed import validate_general
from existence import verify_ledger
import sympy as s
P=Path(__file__).resolve().parents[1]
(P/'verification/current').mkdir(parents=True,exist_ok=True)

def reject(fn):
    try:fn()
    except (VerificationError,ValueError,KeyError,IndexError):return
    raise RuntimeError('corrupted certificate accepted')
def run():
    st=time.monotonic();rows={r['id']:r['N'] for r in json.load(open(P/'data/census.json'))}
    saved=json.load(open(P/'certificates/character_induction.json'))
    def pu(c):return c['pseudo'] if c['kind']=='oriented_pseudo_gate' else c['sphere']['pseudo']
    audited=[]
    for rec in saved:
        R=rows[rec['id']];c=pu(rec['certificate']);data,tab=reciprocity_data(R)
        require(c['table']==tab.metadata(),'table mismatch')
        branch=next(b for b in c['branches'] if b.get('rotation'))
        cols=branch['columns'];L=s.Matrix.hstack(*map(s.Matrix,cols));ep=tuple(branch['rotation'][0]['indicators'])
        A,b,keep=pruned_system(R,data,L,ep,c['height'],branch['galois'])
        y=branch['rotation'][0]['y'];check_farkas(A,b,y)
        reject(lambda:check_farkas(A,b,[0]*len(y)))
        bad=copy.deepcopy(c);bad['table']['characters'][0][0]=['2']
        reject(lambda:verify_pseudo(R,bad))
        if rec['id']=='R6_2_41':
            bad=copy.deepcopy(c)
            q=next(x for x in bad['branches'] if x.get('galois',{}).get('forbidden'))
            q['galois']['forbidden']=q['galois']['forbidden'][1:]
            reject(lambda:verify_pseudo(R,bad))
        audited.append(rec['id'])
    # Discovery positive control: existence is established independently by the
    # conformal embedding; the new necessary-condition suite must not reject it.
    R,aux=construct();require(key(R)==key(rows['R6_2_4']),'G2 model identification')
    require(discover(R,6) is None,'character-induction test rejects unitary G2 model')
    bad=copy.deepcopy(R);bad[1][1][1]+=1
    reject(lambda:validate_general(bad,nonnegative=True))
    now=json.load(open(P/'data/decisions.json'));verify_ledger(now);by={r['id']:r for r in now}
    m2=[d for d in now if d['m']==2]
    require(len(m2)==154 and sum(d['status']=='excluded' for d in m2)==132 and sum(d['status']=='unitarily_realized' for d in m2)==21 and sum(d['status']=='spherically_realized_nonpseudounitary' for d in m2)==1,'multiplicity two not completely classified')
    require(by['R6_2_124']['existence']==dict(general='yes',pivotal='yes',spherical='yes',pseudo_unitary='no',unitary='no'),'Schopieray status corrupted')
    return dict(passed=True,optimized_python=not __debug__,seconds=time.monotonic()-st,
                checked_new_negative_tensors=audited,positive_G2_control=True,
                mutated_character_table_rejected=True,
                missing_Galois_exclusion_rejected=True,zero_Farkas_vector_rejected=True,
                multiplicity_two_complete=True)
if __name__=='__main__':
    result=run();name='character_controls_optimized.json' if not __debug__ else 'character_controls_normal.json'
    (P/'verification/current'/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
