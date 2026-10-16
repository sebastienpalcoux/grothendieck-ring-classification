stats={'passed':True,'optimized_python':not __debug__,'census_tensors':len(rows),'unit_fixing_permutations':0,'census_validation':'trusted repository SHA256, coverage and tensor-ID checks','source':source,'negative_certificates':len(work),'selected_multiplicity':a.multiplicity,'structure_only_exclusions':len(scoped_structure),'frontier':frontier,'counts':dict(collections.Counter(d['status'] for d in ledger)),'seconds':time.monotonic()-st,'ledger_sha256':hashlib.sha256((P/'data/decisions.json').read_bytes()).hexdigest()}
out.with_suffix('.summary.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
return 0
