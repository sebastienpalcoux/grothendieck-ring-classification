#!/usr/bin/env python3
"""Prepare a complete ordinary-group representation search for integral profiles."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
EVIDENCE=HERE.parents[1]
profiles=json.loads((EVIDENCE/'pipeline/survivor_profiles.json').read_text())
rows=[]
for p in profiles:
 if p.get('integral') is not True:continue
 d=p['fp_dimensions']
 if len(d)!=8 or any(type(x) is not int or x<=0 for x in d):raise ValueError(p['id'])
 rows.append({'id':p['id'],'order':sum(x*x for x in d),'degrees':d,'commutative':p['commutative'],'tensor_sha256':p['tensor_sha256']})
rows.sort(key=lambda x:int(x['id'].rsplit('_',1)[1]));orders=sorted({x['order'] for x in rows});degrees=sorted({tuple(sorted(x['degrees'])) for x in rows})
source=EVIDENCE/'pipeline/survivor_profiles.json'
(HERE/'targets.json').write_text(json.dumps({'scope':'All integral profiles among the 277 first-stage rank-eight exact-multiplicity-three survivors. This target selection is a fixed baseline snapshot, not a current unresolved-status ledger.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'orders':orders,'targets':rows},indent=2)+'\n')
script=r'''if LoadPackage("smallgrp") = fail then Error("SmallGroups missing"); fi;
SetPrintFormattingStatus("*stdout*",false);
Print("{\"kind\":\"environment\",\"gap_version\":\"",GAPInfo.Version,"\",\"smallgrp_version\":\"",PackageInfo("smallgrp")[1].Version,"\"}\n");
orders := @ORDERS@;
targets := @DEGREES@;
ScanOrder := function(n)
  local count,index,G,rank,tbl,irr,degrees,trivial,perm,tensor;
  count := NumberSmallGroups(n);
  Print("{\"kind\":\"order_start\",\"order\":",n,",\"groups\":",count,"}\n");
  for index in [1..count] do
    G := SmallGroup(n,index);
    rank := NrConjugacyClasses(G);
    if rank <> 8 then
      Print("{\"kind\":\"group\",\"order\":",n,",\"index\":",index,",\"rank\":",rank,"}\n");
    else
      tbl := CharacterTable(G); irr := Irr(tbl);
      degrees := List(irr,x->x[1]);
      if Sum(degrees,x->x*x) <> n then Error("degree square sum"); fi;
      Print("{\"kind\":\"group\",\"order\":",n,",\"index\":",index,",\"rank\":8,\"degrees\":",degrees);
      if SortedList(degrees) in targets then
        trivial := Position(irr,TrivialCharacter(tbl));
        perm := Concatenation([trivial],Filtered([1..8],x->x<>trivial));
        irr := irr{perm}; degrees := degrees{perm};
        tensor := List([1..8],i->List([1..8],j->List([1..8],k->ScalarProduct(tbl,irr[i]*irr[j],irr[k]))));
        if not ForAll(Flat(tensor),x->IsInt(x) and x>=0) then Error("nonintegral character tensor"); fi;
        Print(",\"unit_first_degrees\":",degrees,",\"tensor\":",tensor);
      fi;
      Print("}\n");
    fi;
  od;
  Print("{\"kind\":\"order_complete\",\"order\":",n,",\"groups\":",count,"}\n");
end;
for n in orders do ScanOrder(n); od;
Print("{\"kind\":\"scan_complete\"}\n");
QUIT;
'''.replace('@ORDERS@',json.dumps(orders)).replace('@DEGREES@',json.dumps(degrees))
(HERE/'scan.g').write_text(script)
print(json.dumps({'orders':orders,'targets':len(rows)}))
