#!/usr/bin/env python3
"""Audit census coverage, partitions, aliases, integrity and lossless transport."""
import argparse
from array import array
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
from build_full_census import (DIST, ROOT, FIELDS, STATUSES, PROFILE_BIT, compact,
                               fingerprint, load_profiles, tensor_bytes, unpack_tensor)


def check(source_cache, full=False, property_samples=False):
    root = DIST / 'data/full-census'
    manifest = json.loads((root / 'manifest.json').read_text())
    assert manifest['version'] == fingerprint(), 'Stale full census artifact'
    assert manifest['total'] == 1434042
    assert manifest['detailed_profiles'] == 3462 and manifest['census_detailed_profiles'] == 3460
    assert manifest['rank_two_profiles'] == 2
    assert manifest['counts'] == {'unitarily_realized': 528, 'excluded': 1433506,
                                  'unresolved': 6, 'realized': 1, 'pseudo_unitarily_realized': 1}
    assert manifest['max_tensor_request_bytes'] <= 32768
    assert manifest['max_index_request_bytes'] <= 160000
    all_ranks = {r['rank']: r for r in manifest['ranks']}
    codes = {v: k for k, v in STATUSES.items()}
    by_line, seen, total_counts, chunk_entries = {}, {}, Counter(), {}

    def verified(entry):
        path = root / entry['path']
        assert path.is_relative_to(root)
        raw = path.read_bytes()
        assert len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], entry['path']
        if entry.get('encoding') == 'gzip':
            raw = gzip.decompress(raw)
            assert len(raw) == entry['uncompressed_bytes']
        return raw

    for r, rank in all_ranks.items():
        seen[r] = bytearray(rank['count'])
        by_line[r] = bytearray(rank['count']*8)
        assert rank['chunk_count'] == (rank['count']+rank['chunk_size']-1)//rank['chunk_size']
        assert rank['tensor_stride'] == r**3*2
        hashes = verified(rank['chunk_index'])
        assert len(hashes) == rank['chunk_count']*36
        chunk_entries[r] = []
        for number in range(rank['chunk_count']):
            count = min(rank['chunk_size'], rank['count']-number*rank['chunk_size'])
            chunk = {'path': f'rank{r}/{number}.bin', 'bytes': struct.unpack_from('<I', hashes, number*36+32)[0],
                     'sha256': hashes[number*36:number*36+32].hex(), 'encoding': rank['tensor_encoding'],
                     'uncompressed_bytes': count*rank['tensor_stride']}
            chunk_entries[r].append(chunk)
            raw = verified(chunk)
            assert len(raw) == count*rank['tensor_stride'] <= 32768
    for band in manifest['bands']:
        counts = Counter()
        rows = list(struct.iter_unpack('<IH', verified(band)))
        assert len(rows) == band['count']
        assert dict(Counter(bits for _, bits in rows)) == dict(band['histogram'])
        rank, m = band['rank'], band['multiplicity']
        assert [line for line, _ in rows] == sorted(line for line, _ in rows)
        for index, (line, bits) in enumerate(rows, 1):
            assert 1 <= line <= len(seen[rank]) and not seen[rank][line-1]
            seen[rank][line-1] = 1
            assert not bits & ~4095 and ((bits >> 8) & 7) in codes
            counts[codes[(bits >> 8) & 7]] += 1
            struct.pack_into('<HHI', by_line[rank], (line-1)*8, m, bits, index)
        assert dict(counts) == band['counts']
        total_counts.update(counts)
    assert dict(total_counts) == manifest['counts']
    assert all(all(flags) for flags in seen.values()), 'Missing census records'
    profiles = load_profiles()
    metadata = json.loads(verified(manifest['profiles']))
    bindings = json.loads(verified(manifest['bindings']))
    assert set(metadata) == set(profiles) and len(bindings) == 3460
    binding_ids = set()
    source_cache_buffers = {}

    def tensor_at(rank, line):
        entry = all_ranks[rank]
        number = (line-1)//entry['chunk_size']
        key = rank, number
        if key not in source_cache_buffers:
            source_cache_buffers.clear()
            source_cache_buffers[key] = verified(chunk_entries[rank][number])
        raw = source_cache_buffers[key]
        start = ((line-1)%entry['chunk_size'])*entry['tensor_stride']
        return raw[start:start+entry['tensor_stride']]

    for binding in bindings:
        rid = binding['profile_id']
        assert rid not in binding_ids
        binding_ids.add(rid)
        profile, entry = profiles[rid], metadata[rid]
        n, m = profile['rank'], profile['multiplicity']
        source_m, bits, index = struct.unpack_from('<HHI', by_line[n], (binding['source_line']-1)*8)
        cid = f'C{n}_{source_m}_{index}'
        assert cid == binding['census_id'] == entry['census_id'] and source_m == m
        assert bits & PROFILE_BIT and codes[(bits >> 8) & 7] == profile['status']
        assert all(profile['properties'][key] == bool(bits & (1 << i)) for i, key in enumerate(FIELDS))
        tensor = unpack_tensor(tensor_at(n, binding['source_line']), n)
        assert hashlib.sha256(compact(tensor)).hexdigest() == binding['source_tensor_sha256']
        p = binding['basis_map_census_to_profile']
        assert sorted(p) == list(range(n)) and p[0] == 0
        assert all(tensor[i][j][k] == profile['fusion_tensor'][p[i]][p[j]][p[k]]
                   for i in range(n) for j in range(n) for k in range(n))
    assert binding_ids == {rid for rid, r in profiles.items() if r['rank'] >= 3}
    for rid, entry in metadata.items():
        payload = json.loads(verified(entry))
        assert payload['record'] == profiles[rid]
        if entry['rank'] == 2:
            assert entry['census_id'] is None and payload['census'] is None
        else:
            assert payload['census']['census_id'] == entry['census_id']
    if full:
        config = json.loads((ROOT / 'site/census_sources.json').read_text())
        checked = 0
        for r, rank in all_ranks.items():
            item = config['census']['ranks'][str(r)]
            path = source_cache / item['tables']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['tables_gz_sha256']
            counts = Counter()
            uncompressed = hashlib.sha256()
            with gzip.open(path, 'rb') as stream:
                for line, raw in enumerate(stream, 1):
                    uncompressed.update(raw)
                    tensor = json.loads(raw.replace(b'{', b'[').replace(b'}', b']'))
                    assert len(tensor) == r and all(len(p) == r and all(len(row) == r for row in p) for p in tensor)
                    assert tensor_bytes(tensor) == tensor_at(r, line), (r, line)
                    m = max(x for p in tensor for row in p for x in row)
                    assert m == struct.unpack_from('<H', by_line[r], (line-1)*8)[0]
                    counts[m] += 1
                    checked += 1
            assert line == rank['count'] and dict(counts) == {int(k): v for k, v in item['counts'].items()}
            assert uncompressed.hexdigest() == item['tables_uncompressed_sha256']
            print(f'Independent JSON-parser roundtrip: rank {r}, {line:,} complete source tensors', flush=True)
        assert checked == 1434042
    if property_samples:
        from build_ring_properties import derive
        samples = 0
        for r, rank in all_ranks.items():
            candidates = {1, rank['count'], rank['count']//2}
            candidates.update(1 + (i*104729+7919) % rank['count'] for i in range(12))
            for line in sorted(candidates):
                tensor = unpack_tensor(tensor_at(r, line), r)
                exact = derive(tensor)['properties']
                bits = struct.unpack_from('<H', by_line[r], (line-1)*8+2)[0]
                assert all(exact[key] == bool(bits & (1 << i)) for i, key in enumerate(FIELDS)), (r, line)
                samples += 1
        print('Independent SymPy root-isolation and subring-closure samples:', samples, flush=True)
    print('Full census audit PASS: 1,434,042 records; exact status partition; 3,460 complete basis maps; all file hashes and bounded requests.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-cache', type=Path, default=ROOT / '.cache/full-census')
    parser.add_argument('--full', action='store_true', help='Independently parse and compare all 1,434,042 released source tensors')
    parser.add_argument('--property-samples', action='store_true', help='Compare independent symbolic root isolation on deterministic samples throughout the full census')
    args = parser.parse_args()
    check(args.source_cache, args.full, args.property_samples)
