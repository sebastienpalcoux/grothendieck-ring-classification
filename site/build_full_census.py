#!/usr/bin/env python3
"""Build a bounded, source-pinned static directory of the complete census.

No enumeration or categorification search is performed. Released tensors are
transported losslessly; structural flags and every detailed-profile basis map
are checked exactly. Generated files belong to the Pages artifact, not Git.
"""
from __future__ import annotations
import argparse
from array import array
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DIST = SITE / 'dist'
SOURCES = ('realized_rings.json', 'unresolved_cases.json', 'resolved_cases.json',
           'rank9_rank10_m1.json', 'rank11_m1.json', 'rank9_m2.json', 'rank12_m1.json')
FIELDS = ('integral', 'weakly_integral', 'simple', 'perfect', 'pointed',
          'commutative', 'self_dual', 'multiplicity_free')
STATUSES = {'excluded': 1, 'unitarily_realized': 2, 'pseudo_unitarily_realized': 3,
            'unresolved': 4, 'realized': 5}
PROFILE_BIT = 1 << 11
CHUNK_BYTES = 32768


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()


def file_record(path, relative_to):
    raw = path.read_bytes()
    return {'path': path.relative_to(relative_to).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def packed_record(path, raw, relative_to):
    path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return {**file_record(path, relative_to), 'encoding': 'gzip', 'uncompressed_bytes': len(raw)}


def version_inputs():
    paths = [SITE / 'census_sources.json', SITE / 'census_properties.cpp', Path(__file__),
             ROOT / 'data/classification_summary_all_ranks.json',
             DIST / 'data/ring_property_flags.json']
    paths += [DIST / 'data' / name for name in SOURCES]
    return {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in paths}


def fingerprint():
    return sha(compact(version_inputs()))[:20]


def tensor_bytes(tensor):
    values = array('H', (x for plane in tensor for row in plane for x in row))
    if sys.byteorder != 'little':
        values.byteswap()
    return values.tobytes()


def unpack_tensor(raw, n):
    values = array('H')
    values.frombytes(raw)
    if sys.byteorder != 'little':
        values.byteswap()
    return [[list(values[(i*n+j)*n:(i*n+j+1)*n]) for j in range(n)] for i in range(n)]


def vertex_signatures(tensor):
    n = len(tensor)
    result = []
    for i in range(n):
        axes = ([tensor[i][j][k] for k in range(n)] for j in range(n))
        left = tuple(sorted(tuple(sorted(row)) for row in axes))
        right = tuple(sorted(tuple(sorted(tensor[j][i][k] for k in range(n))) for j in range(n)))
        output = tuple(sorted(tuple(sorted(tensor[j][k][i] for k in range(n))) for j in range(n)))
        diagonal = tuple(sorted((tensor[i][j][j], tensor[j][i][j], tensor[j][j][i]) for j in range(n)))
        result.append((i == 0, tensor[i][i][0], tensor[i][i][i], left, right, output, diagonal))
    return result


def isomorphism(source, target):
    """Return source-index -> target-index, checking all n^3 coefficients."""
    n = len(source)
    colors, target_colors = vertex_signatures(source), vertex_signatures(target)
    if sorted(colors) != sorted(target_colors):
        return None
    candidates = {i: [j for j in range(n) if colors[i] == target_colors[j]] for i in range(n)}
    mapping, used = {0: 0}, {0}

    def search():
        if len(mapping) == n:
            return [mapping[i] for i in range(n)]
        remaining = [i for i in range(1, n) if i not in mapping]
        i = min(remaining, key=lambda a: len(set(candidates[a])-used))
        for j in candidates[i]:
            if j in used:
                continue
            mapping[i] = j
            assigned = tuple(mapping)
            if all(source[a][b][c] == target[mapping[a]][mapping[b]][mapping[c]]
                   for a in assigned for b in assigned for c in assigned
                   if i in (a, b, c)):
                used.add(j)
                result = search()
                if result is not None:
                    return result
                used.remove(j)
            del mapping[i]
        return None

    return search()


def load_profiles():
    profiles = {}
    properties = json.loads((DIST / 'data/ring_property_flags.json').read_text())['records']
    for name in SOURCES:
        payload = json.loads((DIST / 'data' / name).read_text())
        for original in payload.get('records', payload.get('cases', [])):
            r = dict(original)
            r.setdefault('status', 'unitarily_realized' if r.get('existence') == 'unitary' else 'realized')
            tensor = r.get('fusion_tensor', r.get('tensor'))
            digest = sha(compact(tensor))
            if digest != r['tensor_sha256'] or digest != properties[r['id']]['tensor_sha256']:
                raise ValueError('Profile tensor identity: ' + r['id'])
            r['properties'] = properties[r['id']]['properties']
            profiles[r['id']] = r
    if len(profiles) != 3462:
        raise ValueError('Review profile-coverage expectations before changing this snapshot')
    return profiles


def prepare_sources(config, cache):
    base = ('https://raw.githubusercontent.com/' + config['census_repository'] + '/' +
            config['census_commit'] + '/')

    def fetch(entry):
        path = cache / entry['tables']
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            temporary = path.with_suffix(path.suffix + '.downloading')
            with urllib.request.urlopen(base + entry['tables'], timeout=90) as response:
                temporary.write_bytes(response.read())
            temporary.replace(path)
        if sha(path.read_bytes()) != entry['tables_gz_sha256']:
            raise ValueError('Pinned census gzip mismatch: ' + str(path))
        return path

    entries = list(config['census']['ranks'].values())
    with ThreadPoolExecutor(max_workers=4) as executor:
        files = list(executor.map(fetch, entries))
    return dict(zip((e['rank'] for e in entries), files))


def compile_indexer(cache, boost_include=None):
    source = SITE / 'census_properties.cpp'
    binary = cache / ('properties-' + sha(source.read_bytes())[:16])
    if not binary.exists():
        command = [os.environ.get('CXX', 'g++'), '-O3', '-std=c++17', '-Wall', '-Wextra', '-Werror']
        if boost_include:
            command += ['-isystem', str(boost_include)]
        subprocess.run(command + [str(source), '-o', str(binary)], check=True)
    return binary


def derived_rank(binary, source, entry, cache):
    rank = entry['rank']
    prefix = cache / ('rank' + str(rank) + '-' + sha(binary.read_bytes())[:12] + '-' + entry['tables_gz_sha256'][:12])
    flags, tensors, receipt = (Path(str(prefix)+suffix) for suffix in ('.flags', '.tensors', '.json'))
    if receipt.exists():
        old = json.loads(receipt.read_text())
        if all(p.exists() and sha(p.read_bytes()) == old[p.suffix] for p in (flags, tensors)):
            return flags, tensors
    process = subprocess.Popen([str(binary), str(rank), str(flags), str(tensors)], stdin=subprocess.PIPE)
    digest = hashlib.sha256()
    try:
        with gzip.open(source, 'rb') as stream:
            for raw in iter(lambda: stream.read(1024*1024), b''):
                digest.update(raw)
                process.stdin.write(raw)
        process.stdin.close()
        if process.wait() != 0:
            raise ValueError('Exact structural indexer failed at rank ' + str(rank))
    except BaseException:
        process.kill()
        process.wait()
        raise
    if digest.hexdigest() != entry['tables_uncompressed_sha256']:
        raise ValueError('Pinned census uncompressed mismatch')
    if flags.stat().st_size != entry['classes']*4 or tensors.stat().st_size != entry['classes']*rank**3*2:
        raise ValueError('Lossless tensor or flag length mismatch')
    receipt.write_text(json.dumps({p.suffix: sha(p.read_bytes()) for p in (flags, tensors)}))
    return flags, tensors


def build(args):
    config = json.loads((SITE / 'census_sources.json').read_text())
    overlay = config.get('classification_overlay')
    if overlay and sha((ROOT / overlay['path']).read_bytes()) != overlay['sha256']:
        raise ValueError('Accepted classification overlay changed')
    if sha((ROOT / config['decompressor']['path']).read_bytes()) != config['decompressor']['sha256']:
        raise ValueError('Pinned browser decompressor source changed')
    summary_raw = (ROOT / 'data/classification_summary_all_ranks.json').read_bytes()
    if sha(summary_raw) != config['classification_summary_sha256']:
        raise ValueError('The accepted classification summary changed; review the source snapshot')
    rows = {(r['rank'], r['multiplicity']): r for r in json.loads(summary_raw)['rows']}
    profiles = load_profiles()
    by_band = defaultdict(list)
    literal = defaultdict(list)
    for rid, profile in profiles.items():
        if profile['rank'] >= 3:
            by_band[(profile['rank'], profile['multiplicity'])].append(rid)
            literal[(profile['rank'], tensor_bytes(profile['fusion_tensor']))].append(rid)
    cache = args.cache.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    sources = prepare_sources(config, cache)
    binary = compile_indexer(cache, args.boost_include)
    output = DIST / 'data/full-census'
    staging = Path(tempfile.mkdtemp(prefix='full-census-', dir=cache))
    (staging / 'profiles').mkdir()
    (staging / 'indexes').mkdir()
    matched, metadata, bands, ranks = {}, {}, [], []
    signature_indexes = {}
    totals = Counter()
    bindings = []
    max_tensor_request = 0

    for entry in config['census']['ranks'].values():
        rank = entry['rank']
        flags_file, tensors_file = derived_rank(binary, sources[rank], entry, cache)
        raw_flags = flags_file.read_bytes()
        raw_tensors = tensors_file.read_bytes()
        stride = rank**3*2
        chunk_size = min(256, max(1, CHUNK_BYTES//stride))
        chunks = []
        folder = staging / ('rank' + str(rank))
        folder.mkdir()
        for start in range(0, entry['classes'], chunk_size):
            p = folder / (str(start//chunk_size) + '.bin')
            raw_chunk = raw_tensors[start*stride:min(start+chunk_size, entry['classes'])*stride]
            chunks.append(packed_record(p, raw_chunk, staging))
        max_tensor_request = max(max_tensor_request, max(c['bytes'] for c in chunks))
        chunk_index = folder / 'chunks.bin'
        chunk_index.write_bytes(b''.join(bytes.fromhex(c['sha256'])+struct.pack('<I', c['bytes']) for c in chunks))
        rank_bands = defaultdict(list)
        for line, (m, bits) in enumerate(struct.iter_unpack('<HH', raw_flags), 1):
            if not 1 <= m <= entry['bound'] or bits & ~255:
                raise ValueError('Invalid structural index result')
            key = (rank, m)
            index = len(rank_bands[m])+1
            cid = f'C{rank}_{m}_{index}'
            tensor_raw = raw_tensors[(line-1)*stride:line*stride]
            hits = literal.get((rank, tensor_raw), [])
            tensor = None
            permutation = list(range(rank)) if hits else None
            if not hits and key in by_band:
                if key not in signature_indexes:
                    groups = defaultdict(list)
                    for rid in by_band[key]:
                        groups[tuple(sorted(vertex_signatures(profiles[rid]['fusion_tensor'])))].append(rid)
                    signature_indexes[key] = groups
                tensor = unpack_tensor(tensor_raw, rank)
                candidates = signature_indexes[key].get(tuple(sorted(vertex_signatures(tensor))), [])
                for rid in candidates:
                    candidate = isomorphism(tensor, profiles[rid]['fusion_tensor'])
                    if candidate is not None:
                        hits.append(rid)
                        permutation = candidate
            if len(hits) > 1:
                raise ValueError('Multiple detailed profiles identify the same census class: ' + cid)
            status = 'excluded'
            if hits:
                rid = hits[0]
                if rid in matched:
                    raise ValueError('A detailed profile identifies two census classes: ' + rid)
                profile = profiles[rid]
                if (profile['rank'], profile['multiplicity']) != key:
                    raise ValueError('Profile band mismatch')
                if any(profile['properties'][name] != bool(bits & (1 << k)) for k, name in enumerate(FIELDS)):
                    raise ValueError('Exact property implementations disagree: ' + rid)
                tensor = tensor or unpack_tensor(tensor_raw, rank)
                target = profile['fusion_tensor']
                if sorted(permutation) != list(range(rank)) or permutation[0] != 0 or any(
                        tensor[i][j][k] != target[permutation[i]][permutation[j]][permutation[k]]
                        for i in range(rank) for j in range(rank) for k in range(rank)):
                    raise ValueError('Incomplete basis-map verification')
                matched[rid] = {'census_id': cid, 'source_line': line,
                                'source_tensor_sha256': sha(compact(tensor)),
                                'profile_tensor_sha256': profile['tensor_sha256'],
                                'basis_map_census_to_profile': permutation}
                bindings.append({'profile_id': rid, **matched[rid]})
                status = profile['status']
                bits |= PROFILE_BIT
            bits |= STATUSES[status] << 8
            rank_bands[m].append((line, bits))
            totals[status] += 1
        for m in range(1, entry['bound']+1):
            records = rank_bands[m]
            if len(records) != entry['counts'][str(m)]:
                raise ValueError(f'Census band count: {rank}/{m}')
            expected = rows[(rank, m)]
            counts = Counter(next(s for s, code in STATUSES.items() if code == (bits >> 8) & 7)
                             for _, bits in records)
            modeled = sum(counts[s] for s in ('unitarily_realized', 'pseudo_unitarily_realized', 'realized'))
            expected_modeled = sum(expected[k] for k in ('realized_unitary', 'realized_other_or_unspecified', 'realized_spherical_nonpseudounitary'))
            if (expected['rings'] != len(records) or expected['unassessed'] != 0 or
                    counts['excluded'] != expected['excluded_general'] or
                    counts['unresolved'] != expected['unresolved_general'] or modeled != expected_modeled):
                raise ValueError(f'Classification partition does not transport to the census: {rank}/{m}')
            path = staging / 'indexes' / f'{rank}-{m}.bin'
            index_raw = b''.join(struct.pack('<IH', line, bits) for line, bits in records)
            index_record = packed_record(path, index_raw, staging)
            histogram = sorted(Counter(bits for _, bits in records).items())
            bands.append({'rank': rank, 'multiplicity': m, 'count': len(records),
                          'histogram': histogram, 'counts': dict(counts), **index_record})
        ranks.append({'rank': rank, 'bound': entry['bound'], 'count': entry['classes'],
                      'chunk_size': chunk_size, 'tensor_stride': stride,
                      'chunk_count': len(chunks), 'chunk_index': file_record(chunk_index, staging), 'tensor_encoding': 'gzip',
                      'tables_path': entry['tables'], 'tables_gz_sha256': entry['tables_gz_sha256'],
                      'tables_uncompressed_sha256': entry['tables_uncompressed_sha256'],
                      'completeness': entry.get('completeness_basis',
                         'Released census; validity and distinctness checked within the documented verification scope.')})
        print(f'Indexed rank {rank}: {entry["classes"]:,}; bounded tensor requests <= {CHUNK_BYTES:,} bytes', flush=True)

    required = {rid for rid, r in profiles.items() if r['rank'] >= 3}
    if set(matched) != required:
        raise ValueError('Unmatched detailed profiles: ' + str(sorted(required-set(matched))))
    for rid, profile in profiles.items():
        path = staging / 'profiles' / (sha(rid.encode())[:24] + '.bin')
        profile_raw = compact({'record': profile, 'census': matched.get(rid)}) + b'\n'
        profile_file = packed_record(path, profile_raw, staging)
        property_bits = sum((1 << k) for k, name in enumerate(FIELDS) if profile['properties'][name])
        criterion = profile.get('criterion', '')
        if not criterion and profile.get('research'):
            first = profile['research'][0].get('data', {})
            if isinstance(first, dict):
                criterion = first.get('criterion', '')
        metadata[rid] = {'rank': profile['rank'], 'multiplicity': profile['multiplicity'],
                         'name': profile.get('name', rid), 'status': profile['status'],
                         'flags': property_bits | (STATUSES[profile['status']] << 8) | PROFILE_BIT,
                         'census_id': matched.get(rid, {}).get('census_id'), 'search': str(criterion),
                         **profile_file}
    profile_index = staging / 'profiles.bin'
    profile_index_record = packed_record(profile_index, compact(metadata) + b'\n', staging)
    binding_file = staging / 'profile_bindings.json'
    binding_file.write_bytes(compact(bindings) + b'\n')
    version = fingerprint()
    manifest = {'schema': 'ring-atlas/full-census/v1', 'version': version,
                'date': config['census']['release_date'], 'total': config['census']['total_classes'],
                'counts': dict(totals), 'detailed_profiles': len(profiles),
                'census_detailed_profiles': len(matched), 'rank_two_profiles': 2,
                'property_fields': list(FIELDS), 'status_codes': STATUSES,
                'profile_bit': PROFILE_BIT, 'index_record_bytes': 6,
                'census_repository': config['census_repository'], 'census_commit': config['census_commit'],
                'classification_commit': os.environ.get('GITHUB_SHA', config['classification_commit']),
                'classification_baseline_commit': config['classification_commit'],
                'classification_overlay': config.get('classification_overlay'),
                'classification_summary': 'data/classification_summary_all_ranks.json',
                'source_inputs': version_inputs(), 'bands': bands, 'ranks': ranks,
                'profiles': profile_index_record, 'bindings': file_record(binding_file, staging),
                'identifiers': 'C{rank}_{exact multiplicity}_{1-based index within that band in the pinned census export}. Existing R and F profile identifiers retain their original meaning and URLs. Census basis maps are verified coefficient by coefficient.',
                'classification_scope': 'Published band classification transported by exact identification of every modeled and unresolved class. Other classes are excluded by that band classification; a case-specific criterion is shown only when documented.'}
    if sum(totals.values()) != 1434042 or len(matched) != 3460 or totals['unresolved'] != 6:
        raise ValueError('Review full-census coverage expectations before publication')
    manifest['generated_bytes'] = sum(p.stat().st_size for p in staging.rglob('*') if p.is_file())
    manifest['max_tensor_request_bytes'] = max_tensor_request
    manifest['max_index_request_bytes'] = max(b['bytes'] for b in bands)
    (staging / 'manifest.json').write_bytes(compact(manifest) + b'\n')
    script = DIST / 'census.js'
    source = script.read_text()
    updated = re.sub(r'const dataVersion = "[^"]+";', f'const dataVersion = "{version}";', source)
    if args.check and updated != source:
        raise ValueError('Refresh census.js fingerprint with build_full_census.py')
    if not args.check:
        script.write_text(updated)
    if output.exists():
        shutil.rmtree(output)
    staging.replace(output)
    total_site_bytes = sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())
    if total_site_bytes > 950_000_000:
        raise ValueError('Site exceeds the 950 MB publication guard below the Pages 1 GB limit')
    print(json.dumps({'rings': manifest['total'], 'counts': manifest['counts'],
                      'profiles': len(profiles), 'exact_basis_maps': len(matched),
                      'generated_bytes': manifest['generated_bytes'], 'site_bytes': total_site_bytes,
                      'max_tensor_request': manifest['max_tensor_request_bytes'],
                      'max_band_index_request': manifest['max_index_request_bytes'], 'version': version}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=ROOT / '.cache/full-census')
    parser.add_argument('--boost-include', type=Path, help='Optional local Boost header directory')
    parser.add_argument('--check', action='store_true', help='Build artifact and check the committed JS fingerprint')
    build(parser.parse_args())
