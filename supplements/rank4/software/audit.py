"""Fresh census integrity, fusion-axiom, uniqueness and historical-label audit."""
from pathlib import Path
import sys
from census_data import iter_parameters,parameter_tensor,record_metadata


def audit_census_inputs(root=None):
    root=Path(root) if root is not None else Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:sys.path.insert(0,str(root))
    from audit_census import audit_census
    return audit_census(root)


def audited_records(root=None,bound=128):
    audit_census_inputs(root)
    for source_index,tag,p in iter_parameters(bound=bound):
        yield parameter_tensor(tag,p),record_metadata(source_index,tag,p)


def audit(root,source=False,bound=128):
    """Compatibility wrapper; large callers should use audited_records()."""
    pairs=list(audited_records(root,bound=bound));return [r for r,m in pairs],[m for r,m in pairs]
