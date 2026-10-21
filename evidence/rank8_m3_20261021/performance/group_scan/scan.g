if LoadPackage("smallgrp") = fail then Error("SmallGroups missing"); fi;
SetPrintFormattingStatus("*stdout*",false);
Print("{\"kind\":\"environment\",\"gap_version\":\"",GAPInfo.Version,"\",\"smallgrp_version\":\"",PackageInfo("smallgrp")[1].Version,"\"}\n");
orders := [40, 60, 78, 80, 84, 90, 96, 216, 280, 360, 660];
targets := [[1, 1, 1, 1, 1, 1, 3, 5], [1, 1, 1, 1, 1, 1, 6, 6], [1, 1, 1, 1, 1, 5, 5, 5], [1, 1, 1, 1, 2, 2, 6, 6], [1, 1, 1, 1, 2, 4, 6, 6], [1, 1, 1, 2, 2, 2, 3, 6], [1, 1, 2, 2, 2, 2, 6, 6], [1, 1, 2, 3, 3, 8, 8, 8], [1, 1, 5, 5, 6, 8, 8, 8], [1, 1, 5, 5, 7, 7, 7, 9], [1, 3, 3, 4, 5, 10, 10, 10], [1, 5, 5, 10, 10, 11, 12, 12]];
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
