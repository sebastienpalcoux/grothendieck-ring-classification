"""Positive permutation tests and negative corruption tests for new certificates."""
import json
from pathlib import Path
import sys
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'software'))
import applications as a
from exact import VerificationError
from test_data import historical_labels
inputs=historical_labels()
def recognize_involution(R):
    return a.involution_propagation_recognizer(a.pseudo_certificate(R))
cases=[('F_{2,1}',a.ranktwo_recognizer,a.check_rank_two),
       ('F_{3,7}',a.diagonal_recognizer,a.check_diagonal),
       ('F_{5,33}',recognize_involution,a.check_type42),
       ('F_{9,151}',a.near_recognizer,a.check_near)]
passed=0
for label,recognize,check in cases:
    for p in a.PERMS:
        R=a.permute(inputs[label],p);c=recognize(R)
        assert c is not None
        check(R,c);passed+=1
bad=[]
for label,recognize,check in cases:
    R=inputs[label];c=recognize(R)
    if c['kind']=='rank_two_moment':c['a']+=1
    elif c['kind']=='diagonal_involution_moments':c['m']=2
    elif c['kind']=='near_group_root_length':c['lower_bound']='0'
    else:c['basis']=[0,1,3,2]
    try:check(R,c)
    except (VerificationError,AssertionError,ValueError,IndexError):bad.append(label)
    else:raise AssertionError('corrupt certificate accepted: '+label)
for name in sorted(a.BANNED):
    try:a.reject_legacy({'kind':'signed','branch':{'kind':name}})
    except VerificationError:bad.append('nested '+name)
    else:raise AssertionError('legacy exclusion accepted')
result={'basis_permutation_checks_passed':passed,'deliberate_corruptions_rejected':len(bad),'details':bad}
(root/'verification/applications_tests.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
