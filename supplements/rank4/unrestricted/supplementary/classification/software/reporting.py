"""Reproducible criterion-use statistics, computed only after verification.

Raw witness names and grouped mathematical inputs are both retained. First
use depends on ordering/grouping and does not establish irredundancy.
"""
from collections import Counter,defaultdict

def criterion_report(records):
    counts=Counter();first={};rings=defaultdict(set)
    def walk(value,m,label):
        if isinstance(value,dict):
            kind=value.get('kind')
            if isinstance(kind,str):
                counts[kind]+=1;first[kind]=min(first.get(kind,m),m);rings[kind].add(label)
            for v in value.values():walk(v,m,label)
        elif isinstance(value,list):
            for v in value:walk(v,m,label)
    for r in records:walk(r['certificate'],r['multiplicity'],r['label'])
    # A rejected duality branch is an application of the established
    # spherical-dimension-character input, not a new obstruction family.
    grouping={
        'arithmetic_dnumbers':['dnumber'],
        'subring_dimensions':['subring'],
        'nonselfdual_quadratic_moments':['Sm'],
        'cyclotomicity':['cyclotomic'],
        'signed_dimension_characters':['signed','spherical','signed_characters','zero','duality','galois_fp','unsigned_gauge'],
        'normalized_norms':['norm','all_norms','det_prime'],
        'low_induction_and_moments':['induction','moment','gram_minor','gram_entry','rank_two_moment','diagonal_involution_moments','involution_propagation_42'],
        'quadratic_root_length':['root_length','near_group_root_length'],
        'dimension_field_containment':['field_prime','field_degree'],
        'central_sign_moments':['sign_moments'],
        'spherical_global_moments':['spherical_global_moment','global_codegree_moment'],
        'signed_adjoint_parity':['signed_adjoint_parity'],
        'literature_near_group':['literature_near_group'],
        'weak_integral_reduction':['weak_integral'],
        'two_dimension_Galois_reduction':['two_dimensions'],
    }
    grouped={name:min(first[k] for k in kinds if k in first) for name,kinds in grouping.items() if any(k in first for k in kinds)}
    return {'counts':dict(counts),'first_multiplicity':first,
        'rings':{k:sorted(v) for k,v in rings.items()},
        'group_definitions':grouping,'grouped_first_multiplicity':grouped,
        'largest_grouped_first_use':max(grouped.values()),
        'first_use_of_new_central_sign_obstruction':first.get('sign_moments'),
        'interpretation':'First-use statistics concern this fixed ordering and grouping; they do not prove toolkit minimality or completeness at unbounded multiplicity.'}
