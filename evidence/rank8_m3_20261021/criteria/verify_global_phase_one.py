"""Read-only replay of the phase-I dual-sign and exact-ray controls."""
import argparse,json
from pathlib import Path
import global_induction as g
from exact import require

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rediscover',action='store_true',help='optionally rerun numerical proposals; requires SciPy');args=parser.parse_args()
    here=Path(__file__).resolve().parent
    receipt=json.loads((here/'global_phase_one_validation.json').read_text())
    require(receipt['result']=='PASS','phase-I discovery controls did not pass')
    census={r['id']:r for r in json.loads((here.parent/'pipeline/census_m3.json').read_text())}
    require([r['id'] for r in receipt['records']]==['R8_3_334','R8_3_1453'],'phase-I controls incomplete')
    for item in receipt['records']:
        row=census[item['id']];R=row['tensor'];require(row['tensor_sha256']==item['tensor_sha256'],'phase-I source tensor mismatch')
        a=g.setup(R);rows,rhs,ir,meta=g.build(R,a,4);require(meta==item['metadata'],'phase-I system changed')
        require(item['indicators']==list(g.ht.indicator_choices(R)[0]),'phase-I indicator assignment changed')
        A,b=g.integers(rows,rhs,ir,a['global_dimension'],item['indicators'])
        if item['id']=='R8_3_1453':
            require(item['separated'],'negative control not separated');g.check(A,b,item['ray'],meta['variables'])
            require(sum(x*y for x,y in zip(b,item['ray']))==item['bTy']<0,'wrong phase-I dual sign')
        else:
            require(not item['separated'] and item['ray'] is None,'model control was excluded')
            models=json.loads((here.parent/'models/consolidated_models.json').read_text())
            model=next(r for r in models if r['id']==item['id'])
            require(model['tensor']==R and model['tensor_sha256']==item['tensor_sha256'] and model['status']=='unitarily_realized','positive control is not bound to the verified model')
        if args.rediscover:
            proposed=g.farkas(A,b,meta['variables'],True)
            require((proposed is not None)==item['separated'],'phase-I proposal control changed')
            if proposed:g.check(A,b,proposed,meta['variables'])
    print('PASS: phase-I sign, known-model control and full exact negative ray')
if __name__=='__main__':main()
