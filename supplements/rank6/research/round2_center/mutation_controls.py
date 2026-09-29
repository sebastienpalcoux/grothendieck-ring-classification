"""Negative controls for exact stabilizer-rotation certificate coverage."""
import json,sys,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
from stabilizer_rotation import verify,verify_conditional
from galois_pseudo_reduction import verify as verify_reduction
from exact import require,VerificationError
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')
c=json.loads((ROOT/'certificates/stabilizer_rotation_215.json').read_text())['certificate']
controls=[]
def reject(name,checker,bad):
    try:checker(R,bad)
    except (VerificationError,ValueError,AssertionError,KeyError,TypeError,IndexError) as e:
        controls.append({'mutation':name,'rejected':True,'reason':str(e)});return
    require(False,'mutated certificate accepted: '+name)
p=copy.deepcopy(c['pseudo']);p['branches'].pop();reject('omitted_involution_module_branch',verify,p)
p=copy.deepcopy(c['pseudo']);b=next(b for b in p['branches'] if b['method']=='stabilizer_rotation');b['objects']=[4];reject('omitted_forced_rotation_object',verify,p)
p=copy.deepcopy(c['pseudo']);b=next(b for b in p['branches'] if b['method']=='morita_gram');b.update(method='stabilizer_rotation',objects=[4,5],conditional=0);reject('false_negative_stabilizer_signature',verify,p)
t=copy.deepcopy(c['pseudo']['conditionals'][0]);t['branches'].pop();reject('omitted_low_frame',verify_conditional,t)
t=copy.deepcopy(c['pseudo']['conditionals'][0]);b=next(b for b in t['branches'] if b.get('cases'));b['cases'].pop();reject('omitted_indicator_assignment',verify_conditional,t)
t=copy.deepcopy(c['pseudo']['conditionals'][0]);b=next(b for b in t['branches'] if b.get('cases'));b['cases'][0]['y']=[0]*len(b['cases'][0]['y']);reject('zero_separating_vector',verify_conditional,t)
r=copy.deepcopy(c['reduction']);r['all_values'].pop();reject('omitted_unrestricted_signed_quotient',verify_reduction,r)
r=copy.deepcopy(c['reduction']);r['branches'].pop();reject('omitted_signed_sign_orbit',verify_reduction,r)
r=copy.deepcopy(c['reduction']);r['normalized_indicator_restrictions_used']=True;reject('unauthorized_signed_normalization',verify_reduction,r)
print(json.dumps({'controls':controls,'all_rejected':True},indent=2))
