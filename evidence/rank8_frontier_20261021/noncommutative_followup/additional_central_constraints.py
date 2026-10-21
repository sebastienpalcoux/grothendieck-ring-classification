"""Central-image and full distinguished-S symmetry for R439,R455,R567.

Includes the nonreal one-dimensional characters of R567 in the exact
compositum of its FP field with Q(i). This tests necessary data, not
center fusion rings or categorical existence.
"""
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'noncommutative'))
import central_support as c
import character_modular as modular

def compute(source):
    R=source['tensor'];c.require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'source binding')
    a=c.data(R);original=a;sc=c.w.ScalarCharacters(R)
    split=all(c.w.discover_roots(f,a['K']) is not None for f,m in sc.components)
    if not split:
        oldK=a['K'];K=c.s.QQ.algebraic_field(oldK.ext,c.s.I)
        move=lambda x:K.from_sympy(oldK.to_sympy(x))
        # This algebraic inclusion preserves all old field identities; no
        # choice of a positive complex embedding is needed for S symmetry.
        c.require(all(move(x+y)==move(x)+move(y) and move(x*y)==move(x)*move(y)
                      for x in a['ds'] for y in a['ds']),'FP-to-splitting-field inclusion')
        a=dict(a,K=K,D=move(a['D']),ds=list(map(move,a['ds'])),codegrees=list(map(move,a['codegrees'])))
    characters=modular.characters(R,a);rows=[]
    for index,cols in enumerate(original['lows']):
        why=c.w.core.low_failure(cols,original['Gram'],original['ds'],original['D'],original['K'],original['embedding'],original['du'])
        assignments=modular.assignments(a,characters,cols) if why is None else []
        rows.append({'low_index':index,'columns':[list(v) for v in cols],
                     'ordinary_obstruction':why,'complete_symmetric_S_assignments':[list(p) for p in assignments]})
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'scope':'pseudo_unitary_necessary_conditions; general existence after additional_scope_gates.py Galois transport',
            'outcome':'necessary_frames_survive_not_models','gram_rank':original['Gram'].rank(),
            'column_counts':list(map(len,original['columns'])),'low_count':len(rows),
            'ordinary_surviving_count':sum(r['ordinary_obstruction'] is None for r in rows),
            'full_S_surviving_count':sum(bool(r['complete_symmetric_S_assignments']) for r in rows),
            'splitting_field_extension_by_i_used':not split,
            'character_field_polynomial':[str(x) for x in a['K'].mod.to_list()],
            'full_characters':[[c.ec(x) for x in chi] for chi in characters],
            'formal_codegrees':[c.ec(x) for x in a['codegrees']],
            'irreducible_dimensions':a['multiplicities'],'frames':rows}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census=json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())
    result=[compute(next(row for row in census if row['id']==f'R8_3_{i}')) for i in (439,455,567)]
    result=json.loads(json.dumps(result,default=int));path=HERE/'additional_central_constraints.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:c.require(result==json.loads(path.read_text()),'additional complete central/S replay')
    for row in result:print('PASS',row['id'],row['low_count'],'central-image frames ->',row['full_S_surviving_count'],'full-S frames; no model or general exclusion')

if __name__=='__main__':main()
