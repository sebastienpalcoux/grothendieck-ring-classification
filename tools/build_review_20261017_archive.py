#!/usr/bin/env python3
"""Package current manuscripts, proof sources and exact verification evidence.

The standalone extraction test checks current documents and decision metadata. Full historical
replay is a separate command requiring the complete repository. Repository
archives above 12 MiB are stored as raw 6 MiB parts for tools/restore_data.py;
the generated ZIP remains available locally for the site but is ignored by Git.
An --output outside the repository creates a draft without registering parts.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'review-update-2026-10-17'
PART_THRESHOLD = 12 * 1024 * 1024
PART_BYTES = 6 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def merge_payload(payload, additions):
    """Merge packaged bytes, including virtual preserved baseline members."""
    for name, raw in additions.items():
        if name in ('README.md', 'SHA256SUMS.json'):
            continue
        if name in payload and payload[name] != raw:
            raise ValueError('Conflicting common and rank-eight package source: ' + name)
        payload[name] = raw


def preserve_rank8_standalone_replays(root, fresh_files, fresh_package, source_publication_only=False,
                                       continuation_package=None):
    """Carry validated archive-only evidence into the fresh common payload.

    The selected current collector supplies publication files. For a successor
    release, fresh_package is the frozen frontier package retained by that
    collector, not a newly generated frontier package. Imported replays certify
    only their identical mathematical manifests and ledger; they do not certify
    subsequent decisions, research, or edited publication prose.
    """
    from build_rank8_frontier_release import ARCHIVE_PREFIX, CENTER_FOLLOWUP
    from rank8_frontier import ARCHIVE, PUBLICATION, LEDGER, commands, safe_path

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    def stream_digest(handle):
        value = hashlib.sha256()
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(block)
        return value.hexdigest()

    release_name = PUBLICATION + '/release_manifest.json'
    release_path = root / release_name
    archive_path = root / ARCHIVE
    need(release_path.is_file() and archive_path.is_file(),
         'Build the validated dedicated rank-eight frontier release before the common archive')
    release_raw = release_path.read_bytes()
    release = json.loads(release_raw)
    source_mode = release.get('publication_mode') == 'source_publication'
    need(not source_mode or source_publication_only,
         'Dedicated archive is a source publication; explicitly select --source-publication-only')
    with archive_path.open('rb') as handle:
        need(stream_digest(handle) == release.get('archive_sha256'),
             'Dedicated rank-eight archive SHA-256 differs from its release manifest')
    expected = release.get('files_sha256')
    need(isinstance(expected, dict) and expected, 'Missing dedicated archive member hashes')
    manifest_name = PUBLICATION + '/source_manifest.json'
    package_name = PUBLICATION + '/package_manifest.json'
    manifest_sha = digest(fresh_files[manifest_name])
    ledger_sha = digest(fresh_files[LEDGER])
    need(release.get('frontier_source_manifest_sha256') == manifest_sha
         == fresh_package['frontier_source_manifest_sha256'],
         'Dedicated extracted replay has a stale frontier source manifest')
    need(release.get('frontier_summary', {}).get('ledger_sha256') == ledger_sha
         == fresh_package['frontier_summary']['ledger_sha256'],
         'Dedicated extracted replay has a stale frontier ledger')
    need(release.get('baseline_archive_sha256') == fresh_package['baseline_archive_sha256']
         and release.get('baseline_replays') == fresh_package['baseline_replays'],
         'Dedicated release has different immutable baseline inputs')
    source_manifest = json.loads(fresh_files[manifest_name])
    for name, value in source_manifest.items():
        need(expected.get(name) == value and digest(fresh_files[name]) == value,
             'Dedicated/current mathematical source mismatch: ' + name)
    need(expected.get(manifest_name) == manifest_sha and expected.get(LEDGER) == ledger_sha,
         'Dedicated mathematical manifest or ledger member differs')

    metadata = release.get('standalone_metadata_checks', [])
    required_metadata = {(script, optimized) for script in
                         ('supplements/rank8/software/verify_m3_continuation.py',
                          'tools/verify_rank8_frontier.py') for optimized in (False, True)}
    if source_mode:
        check = release.get('source_publication_metadata_check', {})
        need(check.get('status') == 'SOURCE_METADATA_PASS'
             and check.get('mathematical_replay_performed') is False
             and check.get('source_manifest_sha256') == manifest_sha
             and check.get('ledger_sha256') == ledger_sha
             and release.get('extracted_mathematical_replay_performed') is False
             and not metadata and not release.get('standalone_full_replay_checks')
             and not release.get('standalone_center_followup_checks'),
             'Invalid source-publication scope or metadata receipt')
    else:
        need(len(metadata) == 4 and
             {(x.get('script'), x.get('optimized_python')) for x in metadata} == required_metadata
             and all(x.get('status') == 'METADATA_PASS' for x in metadata),
             'Dedicated normal/optimized baseline and frontier metadata gates are incomplete')
    additions = {}
    preserved = {}
    with zipfile.ZipFile(archive_path) as archive:
        members = {}
        for item in archive.infolist():
            need(not item.is_dir() and item.filename.startswith(ARCHIVE_PREFIX),
                 'Unexpected dedicated archive member root')
            name = item.filename[len(ARCHIVE_PREFIX):]
            need(safe_path(name) and name not in members,
                 'Unsafe or duplicate dedicated archive member: ' + name)
            need((item.external_attr >> 16) & 0o170000 != 0o120000,
                 'Symlink in dedicated archive: ' + name)
            members[name] = item
        need(set(members) == set(expected), 'Dedicated archive member inventory differs')
        for name, item in members.items():
            with archive.open(item) as handle:
                need(stream_digest(handle) == expected[name],
                     'Dedicated archive member checksum differs: ' + name)

        def raw(name):
            need(safe_path(name) and name in members,
                 'Missing or unsafe dedicated replay member: ' + name)
            return archive.read(members[name])

        checksums = json.loads(raw('SHA256SUMS.json'))
        need(checksums == {name: value for name, value in expected.items()
                           if name != 'SHA256SUMS.json'},
             'Dedicated inner checksum manifest differs')
        archived_package = json.loads(raw(package_name))
        need(archived_package == {name: value for name, value in release.items()
                                  if name not in ('files_sha256', 'archive_sha256')},
             'Dedicated package and root release manifests disagree')

        def retain(name, expected_sha):
            content = raw(name)
            need(digest(content) == expected_sha == expected[name],
                 'Dedicated replay receipt/log binding differs: ' + name)
            if name in fresh_files:
                need(fresh_files[name] == content,
                     'Fresh and dedicated replay bytes conflict: ' + name)
            additions[name] = content
            preserved[name] = expected_sha
            return json.loads(content) if name.endswith('.json') else None

        if source_mode:
            lanes = release.get('frontier_replays', [])
            need(lanes and lanes[0].get('optimized_python') is False
                 and len({x.get('optimized_python') for x in lanes}) == len(lanes),
                 'Source publication requires a complete normal canonical replay')
            need(release['source_publication_metadata_check'].get('canonical_replays') == lanes,
                 'Source publication canonical receipt inventory differs')
            for lane in lanes:
                optimized = lane['optimized_python']
                name = PUBLICATION + '/replay_' + ('optimized' if optimized else 'normal') + '.json'
                need(lane.get('path') == name, 'Unexpected canonical source-publication receipt')
                report = retain(name, lane['sha256'])
                need(report.get('status') == 'PASS' and report.get('mathematical_replay_performed') is True
                     and report.get('optimized_python') is optimized
                     and report.get('source_manifest_sha256') == manifest_sha
                     and report.get('ledger_sha256') == ledger_sha,
                     'Incomplete source-publication canonical receipt')
                sections = report.get('sections', [])
                need([x.get('script') for x in sections] == commands(root)
                     and all(x.get('returncode') == 0 for x in sections),
                     'Source-publication canonical command coverage differs')
                for section in sections:
                    retain(section['log'], section['log_sha256'])
        else:
            full = release.get('standalone_full_replay_checks', [])
            need(len(full) == 1, 'A complete extracted normal frontier replay is required')
            check = full[0]
            need(check.get('script') == 'tools/verify_rank8_frontier.py'
                 and check.get('optimized_python') is False and check.get('status') == 'PASS'
                 and check.get('mathematical_replay_performed') is True
                 and check.get('source_inventory_unchanged') is True,
                 'Dedicated extracted frontier replay did not complete')
            report_name = PUBLICATION + '/standalone_full_replay_normal.json'
            need(check.get('packaged_report') == report_name, 'Unexpected extracted frontier receipt path')
            report = retain(report_name, check['packaged_report_sha256'])
            for value in (check, report):
                need(value.get('source_manifest_sha256') == manifest_sha
                     and value.get('ledger_sha256') == ledger_sha,
                     'Extracted frontier receipt source or ledger mismatch')
            need(report.get('status') == 'PASS' and report.get('optimized_python') is False
                 and report.get('mathematical_replay_performed') is True
                 and report.get('log_paths_relocated_for_package') is True
                 and report.get('extracted_replay_original_report_sha256') == check['original_report_sha256'],
                 'Incomplete or unrelocated extracted frontier receipt')
            sections = report.get('sections', [])
            need(sections == check.get('sections') and len(sections) == check.get('section_count')
                 and [x.get('script') for x in sections] == commands(root)
                 and all(x.get('returncode') == 0 for x in sections),
                 'Extracted frontier replay command coverage differs')
            log_names = []
            for section in sections:
                name = section['log']
                need(name.startswith(PUBLICATION + '/standalone_full_replay_normal_logs/'),
                     'Extracted frontier log is not package-relative')
                retain(name, section['log_sha256'])
                log_names.append(name)
            need(len(log_names) == len(set(log_names)), 'Duplicate extracted frontier replay logs')

        center_checks = release.get('standalone_center_followup_checks', [])
        if source_mode:
            center_checks = [dict(item, script=CENTER_FOLLOWUP + '/verify.py', status='PASS',
                                  mathematical_replay_performed=True, packaged_report=item['path'],
                                  report_sha256=item['sha256'])
                             for item in release.get('center_followup', {}).get('canonical_replays', [])]
        center_manifest_name = CENTER_FOLLOWUP + '/source_manifest.json'
        if CENTER_FOLLOWUP + '/verify.py' in fresh_files:
            center_sha = digest(fresh_files[center_manifest_name])
            center_manifest = json.loads(fresh_files[center_manifest_name])
            need(expected.get(center_manifest_name) == center_sha and
                 release.get('center_followup', {}).get('input_files_sha256', {}).get(center_manifest_name) == center_sha,
                 'Extracted center replay has a stale mathematical manifest')
            for name, value in center_manifest['package_files'].items():
                path = CENTER_FOLLOWUP + '/' + name
                need(expected.get(path) == value and digest(fresh_files[path]) == value,
                     'Dedicated/current center source mismatch: ' + path)
            need(len(center_checks) == 2 and
                 {x.get('optimized_python') for x in center_checks} == {False, True},
                 'Both extracted center mathematical replay lanes are required')
            for check in center_checks:
                optimized = check['optimized_python']
                lane = 'optimized' if optimized else 'normal'
                name = CENTER_FOLLOWUP + '/publication/' + ('' if source_mode else 'standalone_') + 'replay_' + lane + '.json'
                need(check.get('script') == CENTER_FOLLOWUP + '/verify.py'
                     and check.get('status') == 'PASS'
                     and check.get('mathematical_replay_performed') is True
                     and check.get('packaged_report') == name,
                     'Incomplete extracted center replay')
                report = retain(name, check['report_sha256'])
                need(report.get('status') == 'PASS' and report.get('completed') is True
                     and report.get('mathematical_replay_performed') is True
                     and report.get('optimized_python') is optimized
                     and report.get('source_manifest_sha256') == center_sha
                     and report.get('baseline_source_manifest') == manifest_name
                     and report.get('baseline_source_manifest_sha256') == manifest_sha,
                     'Extracted center receipt source binding differs')
                need([x.get('script') for x in report.get('checks', [])] ==
                     [x['script'] for x in center_manifest['checks']]
                     and all(x.get('status') == 'PASS' for x in report['checks']),
                     'Extracted center replay command coverage differs')
                for actual, wanted in zip(report['checks'], center_manifest['checks']):
                    need(actual.get('kind') == wanted['kind'],
                         'Extracted center replay kind differs')
                    if 'receipt' in wanted:
                        path = CENTER_FOLLOWUP + '/' + wanted['receipt']
                        need(actual.get('stored_receipt') == wanted['receipt']
                             and actual.get('stored_receipt_sha256') == digest(fresh_files[path]),
                             'Extracted center primary receipt binding differs')
        else:
            need(not center_checks and not release.get('center_followup'),
                 'Dedicated center addendum is missing from the fresh common payload')

    additions[release_name] = release_raw
    provenance = {
        'schema': 'rank8-dedicated-replay-provenance/v1',
        'scope': ('Completed installed canonical replay receipts preserved from a source-publication archive; no extracted mathematical replay is claimed.'
                  if source_mode else
                  'Extracted mathematical replays preserved from the validated dedicated archive; publication files are freshly collected.'),
        'publication_mode': 'source_publication' if source_mode else 'extracted_full_replay',
        'extracted_mathematical_replay_performed': not source_mode,
        'dedicated_archive': ARCHIVE, 'dedicated_archive_sha256': release['archive_sha256'],
        'release_manifest': release_name, 'release_manifest_sha256': digest(release_raw),
        'dedicated_package_manifest_sha256': expected[package_name],
        'fresh_package_manifest_sha256': digest(fresh_files[package_name]),
        'frontier_source_manifest_sha256': manifest_sha, 'ledger_sha256': ledger_sha,
        'preserved_archive_members_sha256': dict(sorted(preserved.items())),
    }
    if continuation_package is not None:
        need(continuation_package.get('schema') in
             ('rank8-next-package/v1', 'rank8-research-20261022-package/v1'),
             'Unexpected successor package for historical replay provenance')
        need(fresh_package == archived_package,
             'Successor must preserve the original frontier package manifest')
        provenance['current_publication'] = {
            'schema': continuation_package['schema'],
            'new_source_manifest_sha256': continuation_package['new_source_manifest_sha256'],
            'ledger_sha256': continuation_package['current_summary']['ledger_sha256'],
            'historical_replays_certify_current_overlay': False,
        }
        provenance['scope'] += (' These historical receipts do not certify the successor '
                                'release\'s new decisions or necessary-condition research.')
    additions[PUBLICATION + '/dedicated_replay_provenance.json'] = (
        json.dumps(provenance, indent=2) + '\n').encode()
    return additions


def preserve_rank8_next_release(root, fresh_files, fresh_package, inventory):
    """Bind the current expanded payload to the completed dedicated release.

    Only its release manifest, package metadata and provenance are carried into
    the common archive. The separately published ZIP is checked, not nested.
    No mathematical verification command is run here.
    """
    from build_rank8_next_release import ARCHIVE, ARCHIVE_PREFIX, PUBLICATION, safe_path

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    release_name = PUBLICATION + '/release_manifest.json'
    package_name = PUBLICATION + '/package_manifest.json'
    manifest_name = PUBLICATION + '/source_manifest.json'
    archive_path = root / ARCHIVE
    need(archive_path.is_file() and (root / release_name).is_file(),
         'Build the finalized dedicated rank-eight next release before the common archive')
    release_raw = (root / release_name).read_bytes()
    release = json.loads(release_raw)
    need(digest(archive_path.read_bytes()) == release.get('archive_sha256'),
         'Dedicated next archive differs from its release manifest')
    archived_package = {name: value for name, value in release.items()
                        if name not in ('files_sha256', 'archive_sha256')}
    need({name: value for name, value in archived_package.items()
          if name != 'extracted_metadata_checks'} == fresh_package,
         'Dedicated next package is stale; rebuild it before the common archive')
    need(json.loads(fresh_files[manifest_name]) == inventory,
         'Current next source inventory differs from its packaged manifest')
    checks = archived_package.get('extracted_metadata_checks', [])
    required = {(script, optimized) for script in
                ('supplements/rank8/software/verify_m3_continuation.py',
                 'tools/verify_rank8_frontier.py', 'tools/rank8_next.py')
                for optimized in (False, True)}
    need(len(checks) == 6 and
         {(x.get('script'), x.get('optimized_python')) for x in checks} == required
         and all(x.get('status') == 'METADATA_PASS'
                 and x.get('mathematical_replay_performed') is False for x in checks)
         and archived_package.get('full_historical_mathematical_replay_performed') is False
         and archived_package.get('packaging_mathematical_replay_performed') is False,
         'Dedicated next metadata gates or proof-replay scope differ')
    expected = release.get('files_sha256')
    need(isinstance(expected, dict) and set(expected) == set(fresh_files),
         'Dedicated next member inventory differs from the current collection')
    with zipfile.ZipFile(archive_path) as archive:
        members = {}
        for item in archive.infolist():
            need(not item.is_dir() and item.filename.startswith(ARCHIVE_PREFIX),
                 'Unexpected dedicated next archive member root')
            name = item.filename[len(ARCHIVE_PREFIX):]
            need(safe_path(name) and name not in members
                 and (item.external_attr >> 16) & 0o170000 != 0o120000,
                 'Unsafe, duplicate or symlinked dedicated next member: ' + name)
            members[name] = item
        need(set(members) == set(expected), 'Dedicated next ZIP inventory differs')
        for name, item in members.items():
            raw = archive.read(item)
            need(digest(raw) == expected[name], 'Dedicated next member checksum differs: ' + name)
            if name not in (package_name, 'SHA256SUMS.json'):
                need(raw == fresh_files[name], 'Dedicated/current next source differs: ' + name)
        package_raw = archive.read(members[package_name])
        need(json.loads(package_raw) == archived_package,
             'Dedicated next package and root release manifests disagree')
        need(json.loads(archive.read(members['SHA256SUMS.json'])) ==
             {name: value for name, value in expected.items() if name != 'SHA256SUMS.json'},
             'Dedicated next inner checksums differ')
    # The only package difference is its completed extracted metadata receipts.
    # Preserve those exact bytes after checking every source and virtual member.
    fresh_files[package_name] = package_raw
    provenance = {
        'schema': 'rank8-next-dedicated-release-provenance/v1',
        'scope': ('Expanded sources match the finalized dedicated next archive. '
                  'Its extracted checks are metadata checks; no full historical '
                  'mathematical replay is claimed for this continuation.'),
        'dedicated_archive': ARCHIVE,
        'dedicated_archive_sha256': release['archive_sha256'],
        'dedicated_archive_included': False,
        'release_manifest': release_name,
        'release_manifest_sha256': digest(release_raw),
        'package_manifest': package_name,
        'package_manifest_sha256': digest(package_raw),
        'source_manifest_sha256': digest(fresh_files[manifest_name]),
        'ledger_sha256': fresh_package['current_summary']['ledger_sha256'],
        'validated_archive_members': len(expected),
        'packaging_mathematical_replay_performed': False,
    }
    return {release_name: release_raw,
            PUBLICATION + '/dedicated_release_provenance.json':
                (json.dumps(provenance, indent=2) + '\n').encode()}


def preserve_rank8_research_release(root, fresh_files, fresh_package, inventory):
    """Check the finalized research ZIP and preserve its proof-replay scope.

    This validates the expanded current files and the byte-preservation map;
    it neither recollects an old release nor edits a historical replay receipt.
    """
    from build_rank8_research_20261022_release import (
        ARCHIVE, ARCHIVE_PREFIX, BASELINE_ARCHIVE, BASELINE_SHA256,
        PUBLICATION, safe_path,
    )
    from rank8_next import PUBLICATION as NEXT_PUBLICATION

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    release_name = PUBLICATION + '/release_manifest.json'
    package_name = PUBLICATION + '/package_manifest.json'
    manifest_name = PUBLICATION + '/source_manifest.json'
    archive_path = root / ARCHIVE
    need(archive_path.is_file() and (root / release_name).is_file(),
         'Build the finalized dedicated rank-eight research release before the common archive')
    release_raw = (root / release_name).read_bytes()
    release = json.loads(release_raw)
    need(digest(archive_path.read_bytes()) == release.get('archive_sha256'),
         'Dedicated research archive differs from its release manifest')
    archived_package = {name: value for name, value in release.items()
                        if name not in ('files_sha256', 'archive_sha256')}
    need(archived_package.get('schema') == 'rank8-research-20261022-package/v1'
         and archived_package.get('status') == 'PASS'
         and archived_package.get('publication_mode') == 'targeted_proof_receipts_and_extracted_metadata',
         'A completed research release is required; provisional snapshots are not accepted')
    need({name: value for name, value in archived_package.items()
          if name != 'extracted_metadata_checks'} == fresh_package,
         'Dedicated research package is stale; rebuild it before the common archive')
    need(json.loads(fresh_files[manifest_name]) == inventory,
         'Current research source inventory differs from its packaged manifest')
    need(archived_package.get('baseline_archive') == BASELINE_ARCHIVE
         and archived_package.get('baseline_archive_sha256') == BASELINE_SHA256,
         'Research release does not preserve the frozen next-stage archive')
    checks = archived_package.get('extracted_metadata_checks', [])
    required = {(script, optimized) for script in
                ('supplements/rank8/software/verify_m3_continuation.py',
                 'tools/verify_rank8_frontier.py', 'tools/rank8_next.py',
                 'tools/rank8_research_20261022.py',
                 'tools/verify_rank8_research_20261022.py')
                for optimized in (False, True)}
    need(len(checks) == 10 and
         {(x.get('script'), x.get('optimized_python')) for x in checks} == required
         and all(x.get('status') in ('METADATA_PASS', 'SOURCE_METADATA_PASS')
                 and x.get('mathematical_replay_performed') is False for x in checks)
         and all(x.get('status') == 'METADATA_PASS' for x in checks
                 if x.get('script') == 'tools/verify_rank8_research_20261022.py')
         and archived_package.get('full_historical_mathematical_replay_performed') is False
         and archived_package.get('packaging_mathematical_replay_performed') is False,
         'Dedicated research metadata gates or proof-replay scope differ')
    expected = release.get('files_sha256')
    need(isinstance(expected, dict) and set(expected) == set(fresh_files),
         'Dedicated research member inventory differs from the current collection')
    with zipfile.ZipFile(archive_path) as archive:
        members = {}
        for item in archive.infolist():
            need(not item.is_dir() and item.filename.startswith(ARCHIVE_PREFIX),
                 'Unexpected dedicated research archive member root')
            name = item.filename[len(ARCHIVE_PREFIX):]
            need(safe_path(name) and name not in members
                 and (item.external_attr >> 16) & 0o170000 != 0o120000,
                 'Unsafe, duplicate or symlinked dedicated research member: ' + name)
            members[name] = item
        need(set(members) == set(expected), 'Dedicated research ZIP inventory differs')
        for name, item in members.items():
            raw = archive.read(item)
            need(digest(raw) == expected[name], 'Dedicated research member checksum differs: ' + name)
            if name not in (package_name, 'SHA256SUMS.json'):
                need(raw == fresh_files[name], 'Dedicated/current research source differs: ' + name)
        package_raw = archive.read(members[package_name])
        need(json.loads(package_raw) == archived_package,
             'Dedicated research package and root release manifests disagree')
        need(json.loads(archive.read(members['SHA256SUMS.json'])) ==
             {name: value for name, value in expected.items() if name != 'SHA256SUMS.json'},
             'Dedicated research inner checksums differ')

    preservation = archived_package.get('baseline_byte_preservation', {})
    need(isinstance(preservation, dict)
         and len(preservation) == archived_package.get('baseline_members')
         and preservation, 'Missing complete next-stage byte-preservation map')
    for name, item in preservation.items():
        path = item.get('path', '')
        need(safe_path(name) and safe_path(path) and path in fresh_files
             and digest(fresh_files[path]) == item.get('sha256'),
             'Historical next-stage bytes differ: ' + name)

    # The next-stage external release manifest is not inside its ZIP. Bind it
    # to the pinned old ZIP and its preserved package without regenerating it.
    next_release_name = NEXT_PUBLICATION + '/release_manifest.json'
    next_release_raw = (root / next_release_name).read_bytes()
    next_release = json.loads(next_release_raw)
    need(next_release.get('archive_sha256') == BASELINE_SHA256
         and next_release.get('files_sha256') ==
             {name: item['sha256'] for name, item in preservation.items()},
         'Historical next release manifest differs from the preserved archive')
    next_package_path = preservation[NEXT_PUBLICATION + '/package_manifest.json']['path']
    need(json.loads(fresh_files[next_package_path]) ==
         {name: value for name, value in next_release.items()
          if name not in ('files_sha256', 'archive_sha256')},
         'Historical next package and release manifests disagree')
    fresh_files[package_name] = package_raw
    replays = {lane: {'path': PUBLICATION + '/replay_' + lane + '.json',
                      'sha256': digest(fresh_files[PUBLICATION + '/replay_' + lane + '.json'])}
               for lane in ('normal', 'optimized')}
    targeted_counts = {len(json.loads(fresh_files[item['path']])['sections'])
                       for item in replays.values()}
    need(len(targeted_counts) == 1 and next(iter(targeted_counts)) > 0,
         'Current targeted replay lanes have different command coverage')
    provenance = {
        'schema': 'rank8-research-dedicated-release-provenance/v1',
        'scope': ('Expanded sources match the finalized research archive. Both completed '
                  'targeted mathematical replay receipts are included. Its extracted '
                  'packaging checks verify metadata; historical receipts retain their '
                  'original sources and proof scope.'),
        'dedicated_archive': ARCHIVE,
        'dedicated_archive_sha256': release['archive_sha256'],
        'dedicated_archive_included': False,
        'release_manifest': release_name,
        'release_manifest_sha256': digest(release_raw),
        'package_manifest': package_name,
        'package_manifest_sha256': digest(package_raw),
        'source_manifest_sha256': digest(fresh_files[manifest_name]),
        'ledger_sha256': fresh_package['current_summary']['ledger_sha256'],
        'canonical_targeted_replays': replays,
        'targeted_scripts_per_lane': next(iter(targeted_counts)),
        'preserved_next_members': len(preservation),
        'historical_next_release_manifest': next_release_name,
        'historical_next_release_manifest_sha256': digest(next_release_raw),
        'validated_archive_members': len(expected),
        'packaging_mathematical_replay_performed': False,
        'full_historical_mathematical_replay_performed': False,
    }
    return {release_name: release_raw, next_release_name: next_release_raw,
            PUBLICATION + '/dedicated_release_provenance.json':
                (json.dumps(provenance, indent=2) + '\n').encode()}


def collect_rank8_creative_release(root):
    """Expand the validated creative release without recollecting old stages.

    The complete prior scientific archive remains nested byte-for-byte. Its
    original routers certify the earlier mathematics; current routers and the
    new accepted evidence have separate source and receipt bindings.
    """
    import rank8_creative_20261022 as stage
    import rank8_creative_history as history
    from build_rank8_creative_20261022_release import PREFIX as archive_prefix
    from verify_rank8_creative_20261022 import check_reports

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    summary = stage.validate_ledger(root)
    inventory = stage.source_inventory(root)
    manifest_sha, receipt_shas = check_reports(root, summary, inventory)
    historical = history.baseline(root)
    package_name = stage.EVIDENCE + '/package.json'
    package_raw = (root / package_name).read_bytes()
    package = json.loads(package_raw)
    archive_path = root / stage.ARCHIVE
    need(package.get('schema') == 'rank8-creative-20261022-package/v1'
         and package.get('status') == 'PASS',
         'A completed dedicated creative release is required')
    need(package.get('archive') == stage.ARCHIVE
         and package.get('archive_sha256') == digest(archive_path.read_bytes())
         and package.get('archive_bytes') == archive_path.stat().st_size,
         'Dedicated creative archive identity differs from its package receipt')
    need(package.get('classification') == summary
         and package.get('source_manifest_sha256') == manifest_sha
         and package.get('targeted_replay_receipt_sha256') == receipt_shas
         and package.get('historical_archive_sha256') == history.ARCHIVE_SHA256,
         'Dedicated creative package is stale or has different accepted inputs')
    files = {}
    with zipfile.ZipFile(archive_path) as archive:
        for item in archive.infolist():
            need(not item.is_dir() and item.filename.startswith(archive_prefix),
                 'Unexpected dedicated creative archive member root')
            name = item.filename[len(archive_prefix):]
            need(stage.safe_path(name) and name not in files
                 and (item.external_attr >> 16) & 0o170000 != 0o120000,
                 'Unsafe, duplicate or symlinked creative member: ' + name)
            files[name] = archive.read(item)
    need(len(files) == package.get('members'), 'Dedicated creative member count differs')
    checks = json.loads(files['SHA256SUMS.json'])
    need(set(checks) == set(files) - {'SHA256SUMS.json'},
         'Dedicated creative inner checksum coverage differs')
    for name, value in checks.items():
        need(digest(files[name]) == value, 'Dedicated creative member checksum differs: ' + name)
    manifest_name = stage.PUBLICATION + '/source_manifest.json'
    need(digest(files[manifest_name]) == manifest_sha
         and json.loads(files[manifest_name]) == inventory,
         'Dedicated creative source manifest differs from current accepted inputs')
    for name, value in inventory.items():
        need(name in files and digest(files[name]) == value,
             'Dedicated creative scientific source differs: ' + name)
    need(history.ARCHIVE in files
         and digest(files[history.ARCHIVE]) == history.ARCHIVE_SHA256,
         'Dedicated creative archive does not preserve the complete historical ZIP')
    replays = []
    for lane, value in zip(('normal', 'optimized'), receipt_shas):
        name = stage.PUBLICATION + '/replay_' + lane + '.json'
        need(name in files and digest(files[name]) == value,
             'Dedicated creative canonical replay differs: ' + lane)
        for section in json.loads(files[name])['sections']:
            log_name = section['log']
            need(log_name in files and digest(files[log_name]) == section['log_sha256'],
                 'Dedicated creative replay log missing or changed: ' + log_name)
        replays.append({'path': name, 'sha256': value})
    # check_reports has validated the canonical log identities on disk. Bind
    # every archived current publication receipt and log to those same bytes.
    for name, raw in files.items():
        if name.startswith(stage.PUBLICATION + '/'):
            need((root / name).is_file() and (root / name).read_bytes() == raw,
                 'Dedicated/current creative receipt or log differs: ' + name)
    need(package_name not in files or files[package_name] == package_raw,
         'Conflicting creative package receipt in dedicated archive')
    files[package_name] = package_raw
    provenance = {
        'schema': 'rank8-creative-dedicated-release-provenance/v1',
        'scope': ('Expanded current sources and both completed canonical targeted replay '
                  'lanes are bound to the dedicated creative release. The complete earlier '
                  'scientific ZIP remains byte-exact, including its original routers and '
                  'proof sources. Common-archive extraction checks metadata and does not '
                  'claim a fresh mathematical replay.'),
        'dedicated_archive': stage.ARCHIVE,
        'dedicated_archive_sha256': package['archive_sha256'],
        'dedicated_archive_included': False,
        'package_receipt': package_name,
        'package_receipt_sha256': digest(package_raw),
        'source_manifest_sha256': manifest_sha,
        'ledger_sha256': summary['ledger_sha256'],
        'models_sha256': summary['models_sha256'],
        'canonical_targeted_replays': replays,
        'validated_archive_members': len(checks) + 1,
        'historical_archive': historical,
        'historical_archive_included': True,
        'current_publication_overlays': {},
        'packaging_mathematical_replay_performed': False,
    }
    return files, provenance, inventory


def package_publication_archive(root, output):
    """Register only this generated ZIP; preserve every other restoration entry."""
    try:
        relative = output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return {'storage': 'external draft', 'parts': 0}
    manifest_path = root / 'data/large_files_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    matches = [item for item in manifest['files'] if item['path'] == relative]
    if len(matches) > 1:
        raise ValueError('Duplicate archive restoration entries: ' + relative)
    raw = output.read_bytes()
    previous = matches[0] if matches else None
    if len(raw) <= PART_THRESHOLD and previous is None:
        return {'storage': 'direct file', 'parts': 0}
    part_dir = root / 'data/payloads' / relative.replace('/', '__').replace('.', '_')
    part_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for index, start in enumerate(range(0, len(raw), PART_BYTES), 1):
        chunk = raw[start:start + PART_BYTES]
        path = part_dir / f'part-{index:03}.bin'
        temporary = path.with_suffix('.writing')
        temporary.write_bytes(chunk)
        temporary.replace(path)
        parts.append({'path': path.relative_to(root).as_posix(),
                      'bytes': len(chunk), 'sha256': digest(chunk)})
    current_sha = digest(raw)
    item = {'path': relative, 'bytes': len(raw), 'sha256': current_sha,
            'encoding': 'raw', 'parts': parts}
    if previous:
        historical = list(previous.get('previous_sha256', []))
        if previous['sha256'] != current_sha and previous['sha256'] not in historical:
            historical.append(previous['sha256'])
        if historical:
            item['previous_sha256'] = historical
        manifest['files'][manifest['files'].index(previous)] = item
    else:
        manifest['files'].append(item)
    # Match restore_data's public format, including per-part and final identities.
    packed = b''.join((root / part['path']).read_bytes() for part in parts)
    if packed != raw:
        raise ValueError('Raw archive parts do not reconstruct the ZIP')
    temporary = manifest_path.with_suffix('.writing')
    temporary.write_text(json.dumps(manifest, indent=2) + '\n')
    temporary.replace(manifest_path)
    retained = {Path(part['path']).name for part in parts}
    for stale in part_dir.glob('part-*.bin'):
        if stale.name not in retained:
            stale.unlink()
    ignore = root / '.gitignore'
    text = ignore.read_text() if ignore.exists() else ''
    rule = '/' + relative
    if rule not in text.splitlines():
        text = text.rstrip() + ('\n\n' if text.strip() else '')
        text += '# Restored from checksummed repository parts; generated for GitHub Pages.\n' + rule + '\n'
        ignore.write_text(text)
    return {'storage': 'raw repository parts', 'parts': len(parts),
            'part_bytes': PART_BYTES, 'manifest': 'data/large_files_manifest.json',
            'omit_from_git': relative}


def collect(root, source_publication_only=False):
    from current_publication import DOCUMENT_REVISION, validate_documents, replay_sources
    from reader_resources import validate_reader_resources
    revision = validate_documents(root)
    validate_reader_resources(root)
    preserved = replay_sources(root)
    spec = importlib.util.spec_from_file_location('frozen_bundle', root / 'tools/build_unified_20261016_archive.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    paths = set(old.REQUIRED)
    for folder in ('evidence/unified_20261016', 'evidence/theoretical_20261016',
                   'evidence/review_20261017', 'evidence/prepublication_20261017',
                   'evidence/publication_20261017', 'evidence/rank4_unrestricted_20261017',
                   'evidence/rigidity_20261017', 'evidence/citation_20261019',
                   'evidence/rank7_m5_20261019', 'evidence/rank7_m5_20261020', 'supplements/rank7/output/m5',
                   'supplements/rank7/provenance', 'supplements/rank7/output'):
        paths.update(path.relative_to(root).as_posix() for path in (root / folder).rglob('*')
                     if path.is_file() and not {'__pycache__', '.pytest_cache'}.intersection(path.parts)
                     and not any(part.startswith('.') for part in path.relative_to(root).parts)
                     and path.suffix not in ('.pyc', '.pyo', '.tmp', '.writing', '.swp', '.log')
                     and not (folder == 'evidence/rank7_m5_20261020' and not path.suffix)
                     and not (folder == 'evidence/rank7_m5_20261020' and
                              (path.name.endswith(('.progress.json', '_checkpoint.json', '.checkpoint.json'))
                               or path.suffix not in {'.py','.cpp','.json','.jsonl','.gz','.txt','.md','.tex','.pdf','.csv'}))
                     and path.name != '.DS_Store')
    paths.update(revision['documents'])
    for folder in ('supplements/rank6/software','supplements/rank7/software','supplements/rank7/data'):
        paths.update(path.relative_to(root).as_posix() for path in (root/folder).rglob('*')
                     if path.is_file() and path.suffix in ('.py','.cpp','.h','.hpp','.json','.gz','.txt','.csv','.md'))
    paths.update(path.relative_to(root).as_posix() for path in (root/'supplements/rank7').glob('*')
                 if path.is_file() and path.suffix in ('.py','.cpp','.md','.txt'))
    paths.update(('tools/sync_rank7_m5_publication.py', 'tools/import_rank7_m5_counts.py',
                  'tools/build_novelty_frontier_brief.py', 'tools/build_rank7_m5_continuation_overview.py',
                  'tools/audit_rank7_manuscript.py', 'tools/replay_m5_ci.py',
                  'data/counts.json', 'data/classification_status.json'))
    paths.update(json.loads((root / 'evidence/rigidity_20261017/source_files.json').read_text()))
    necessary = json.loads((root / 'evidence/rigidity_20261017/rank6/MANIFEST.json').read_text())
    paths.update(item['path'] for item in necessary['external_inputs'])
    paths.update(path.relative_to(root).as_posix()
                 for path in (root / 'supplements/rank4/unrestricted').rglob('*')
                 if path.is_file() and not {'__pycache__', '.pytest_cache'}.intersection(path.parts)
                 and path.suffix not in ('.pyc', '.pyo', '.o', '.aux', '.log', '.out', '.toc')
                 and path.name not in ('enumerate', 'enumerate_signed'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'docs').glob('*.md'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'supplements').glob('rank*/README.md'))
    # Include the current reader indexes and the clean status-PDF source, so the
    # downloaded edition has the same navigation and rebuild inputs as GitHub.
    paths.update(('manuscripts/README.md', 'manuscripts/prepublication-review-2026-10-17.pdf', 'supplements/README.md',
                  'tools/build_prepublication_review.py', 'docs/prepublication_review_content.json'))
    paths.update(path.relative_to(root).as_posix() for path in (root / 'supplements/rank6').rglob('*.md')
                 if path.name in ('README.md', 'CURRENT_STATUS.md'))
    paths.update((DOCUMENT_REVISION, 'tools/verify_current_publication.py',
                  'tools/current_publication.py', 'tools/verify_review_20261017.py',
                  'tools/verify_rigidity_20261017.py',
                  'tools/build_review_20261017_archive.py', 'tools/build_current_document_revision.py',
                  'tools/reader_resources.py', 'data/remaining_cases.py', 'data/manuscript_page_counts.json',
                  'docs/PREPUBLICATION_REVIEW.md', 'docs/RESEARCH_STATUS.md', 'docs/VERIFY.md'))
    paths.update(('tools/rank7_publication.py',
                  'supplements/rank7/output/rank7_ledger.json',
                  'supplements/rank7/output/rank7_ledger_through_m4.json',
                  'supplements/rank7/data/rank7_tables_through_m4.txt.gz'))
    from rank8_publication import active
    extension_files = {}
    creative_provenance = None
    creative_inventory = None
    if active(root):
        from rank8_frontier import active as frontier_active, PUBLICATION as FRONTIER_PUBLICATION
        from rank8_next import active as next_active
        from rank8_research_20261022 import active as research_active
        from rank8_creative_20261022 import active as creative_active
        if creative_active(root):
            extension_files, creative_provenance, creative_inventory = collect_rank8_creative_release(root)
        elif research_active(root):
            from build_rank8_research_20261022_release import collect as collect_research
            extension_files, extension_package, inventory = collect_research(root)
            research_additions = preserve_rank8_research_release(
                root, extension_files, extension_package, inventory)
            frontier_package = json.loads(extension_files[
                FRONTIER_PUBLICATION + '/package_manifest.json'])
            merge_payload(extension_files, preserve_rank8_standalone_replays(
                root, extension_files, frontier_package, source_publication_only,
                continuation_package=extension_package))
            merge_payload(extension_files, research_additions)
        elif next_active(root):
            from build_rank8_next_release import collect as collect_next
            extension_files, extension_package, inventory = collect_next(root)
            next_additions = preserve_rank8_next_release(
                root, extension_files, extension_package, inventory)
            # The successor already contains the entire immutable frontier
            # archive. Regenerating that old package would conflict with its
            # preserved manifest and superseded publication byte streams.
            frontier_package = json.loads(extension_files[
                FRONTIER_PUBLICATION + '/package_manifest.json'])
            merge_payload(extension_files, preserve_rank8_standalone_replays(
                root, extension_files, frontier_package, source_publication_only,
                continuation_package=extension_package))
            merge_payload(extension_files, next_additions)
        elif frontier_active(root):
            from build_rank8_frontier_release import collect as collect_rank8
            extension_files, extension_package = collect_rank8(root, source_publication_only)
            merge_payload(extension_files, preserve_rank8_standalone_replays(
                root, extension_files, extension_package, source_publication_only))
        else:
            from build_rank8_m3_release import collect as collect_rank8
            extension_files, extension_package = collect_rank8(root)
        paths.update(path.relative_to(root).as_posix() for path in (root/'tools').glob('*rank8_m3*.py'))
        paths.update(path.relative_to(root).as_posix() for path in (root/'tools/templates').glob('rank8_m3_*.tex'))
    payload = {name: (root / name).read_bytes() for name in sorted(paths)}
    if creative_provenance is not None:
        # The dedicated release freezes the mathematical evidence. Current
        # publication documents may have been rebuilt after that release; bind
        # those overlays explicitly without changing any accepted source.
        for name in sorted(set(payload) & set(extension_files)):
            if payload[name] == extension_files[name]:
                continue
            if name in creative_inventory:
                raise ValueError('Changed creative scientific input in common package: ' + name)
            creative_provenance['current_publication_overlays'][name] = {
                'dedicated_member_sha256': digest(extension_files[name]),
                'current_publication_sha256': digest(payload[name]),
                'changes_bound_scientific_input': False}
            extension_files[name] = payload[name]
        from rank8_creative_20261022 import PUBLICATION as CREATIVE_PUBLICATION
        extension_files[CREATIVE_PUBLICATION + '/dedicated_release_provenance.json'] = (
            json.dumps(creative_provenance, indent=2, sort_keys=True) + '\n').encode()
    merge_payload(payload, extension_files)
    # The immutable proof manifest keeps its exact original hashes. Revised
    # documents are verified separately; their original replay bytes are in the
    # independently pinned archive and are restored only by the dispatcher.
    frozen = json.loads(payload['evidence/unified_20261016/source_files.json'])
    for name, expected in frozen.items():
        raw = preserved[name] if name in preserved else payload.get(name)
        if raw is None or digest(raw) != expected:
            raise ValueError('Missing or changed immutable proof source: ' + name)
    for source in revision['web_copies'].values():
        if source not in payload or not payload[source].startswith(b'%PDF-'):
            raise ValueError('Current downloadable manuscript missing: ' + source)
    return payload


def source_publication_metadata(root):
    """Check current publication identities without asserting a fresh proof replay."""
    from current_publication import validate_documents, replay_sources
    from reader_resources import validate_reader_resources
    root = Path(root)
    documents = validate_documents(root, check_web=(root / 'site/dist/papers').is_dir())
    readers = validate_reader_resources(root, check_web=(root / 'site/dist/papers').is_dir())
    preserved = replay_sources(root)
    from rank8_creative_20261022 import active as creative_active
    if creative_active(root):
        import rank8_creative_20261022 as stage
        import rank8_creative_history as history
        from verify_rank8_creative_20261022 import check_reports
        historical = history.baseline(root)
        summary = stage.validate_ledger(root)
        inventory = stage.source_inventory(root)
        manifest_sha, receipt_shas = check_reports(root, summary, inventory)
        return {'status': 'SOURCE_PUBLICATION_METADATA_PASS',
                'mathematical_replay_performed': False,
                'scope': ('Current document and reader identities, current creative-stage source '
                          'and ledger bindings, both completed canonical targeted replay receipts '
                          'and logs, and the pinned historical archive; no fresh mathematical replay'),
                'current_documents': len(documents['documents']),
                'historical_accepted_decisions': documents['accepted_decisions'],
                'historical_replay_source_files': len(preserved),
                'reader_resources': readers,
                'source_manifest_sha256': manifest_sha,
                'ledger_sha256': summary['ledger_sha256'],
                'historical_rank8_archive': historical,
                'current_rank8': summary,
                'current_rank8_source_manifest_sha256': manifest_sha,
                'canonical_current_rank8_replays': [
                    {'path': stage.PUBLICATION + '/replay_' + lane + '.json', 'sha256': value}
                    for lane, value in zip(('normal', 'optimized'), receipt_shas)]}
    from build_rank8_frontier_release import frontier_inputs
    _, summary, reports, manifest_sha = frontier_inputs(root, True)
    result = {'status': 'SOURCE_PUBLICATION_METADATA_PASS',
            'mathematical_replay_performed': False,
            'scope': 'Current document and reader identities, immutable source identities, frontier ledger and completed canonical receipts; no fresh historical or extracted mathematical replay',
            'current_documents': len(documents['documents']),
            'historical_accepted_decisions': documents['accepted_decisions'],
            'historical_replay_source_files': len(preserved),
            'reader_resources': readers,
            'source_manifest_sha256': manifest_sha,
            'ledger_sha256': summary['ledger_sha256'],
            'canonical_frontier_replays': reports}
    from rank8_research_20261022 import active as research_active
    from rank8_next import active as next_active
    if research_active(root):
        from rank8_research_20261022 import validate_ledger, source_inventory, PUBLICATION
        from verify_rank8_research_20261022 import check_reports
        current = validate_ledger(root)
        inventory = source_inventory(root)
        current_sha, receipt_shas = check_reports(root, current, inventory)
        result['current_rank8'] = current
        result['current_rank8_source_manifest_sha256'] = current_sha
        result['canonical_current_rank8_replays'] = [
            {'path': PUBLICATION + '/replay_' + lane + '.json', 'sha256': value}
            for lane, value in zip(('normal', 'optimized'), receipt_shas)]
        result['scope'] += ('; current rank-eight accepted decisions and research bindings, '
                            'plus both completed accepted targeted replay receipts and '
                            'logs, are checked separately from the historical receipts')
    elif next_active(root):
        from rank8_next import validate_ledger, source_inventory, PUBLICATION
        current = validate_ledger(root)
        manifest_raw = (root / PUBLICATION / 'source_manifest.json').read_bytes()
        if json.loads(manifest_raw) != source_inventory(root):
            raise ValueError('Current next source manifest differs from its validated inventory')
        result['current_rank8'] = current
        result['current_rank8_source_manifest_sha256'] = digest(manifest_raw)
        result['scope'] += ('; current rank-eight accepted decisions, model and research '
                            'bindings are checked separately from the historical receipts')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--source-publication-only', action='store_true',
                        help='Preserve completed source-publication receipts without claiming extracted mathematical replay')
    args = parser.parse_args()
    root = args.repo.resolve()
    payload = collect(root, args.source_publication_only)
    inputs = {name: digest(raw) for name, raw in payload.items()}
    payload['README.md'] = ("""# Grothendieck-ring classification · manuscripts and verification

This package contains the current manuscript sources and PDFs for ranks two
through eight, verification guides, proof sources, exact computational evidence,
and the publication identity manifest data/current_document_revision.json.

Ranks two, three and four have unrestricted complex classifications. The
rank-four article proves a theoretical dimension bound without pivotality
or a multiplicity restriction, then classifies its complete 1,692-ring
finite census into 1,677 exclusions and 15 models. Its replay package is
supplements/rank4/unrestricted; the sharp multiplicity bound is six.

The historical 38-case continuation has 36 accepted decisions (29 proposed exclusions and
7 constructions). R6_4_155 and R6_8_1660 remain unresolved. The earlier rank-eight
classification through multiplicity two had 896 exclusions and 77 unitary models. The inner-square
obstruction for R8_2_24 uses pivotal duality, short gauge weights and tensor-functor rigidity.
Treat these AI-generated results and data with caution: independent human
verification and Lean formalization have not been completed.

Start with docs/RESEARCH_STATUS.md and the manuscripts directory.
The verification procedures and their precise limits are in docs/VERIFY.md.
The exact tensors of the current open cases are plain Python nested lists in
data/remaining_cases.py, with unit, duality, convention and source hashes.
data/manuscript_page_counts.json counts each distinct current PDF once.

Standalone publication, source-identity and decision check:
    python3 tools/verify_current_publication.py --metadata-only

Full proof-history replay, from a complete repository checkout:
    python3 tools/verify_current_publication.py --historical

The dispatcher reconstructs each immutable proof stage in an isolated temporary
workspace. It never replaces the current manuscripts. A computational PASS
certifies the stated checks, not the mathematical correctness of every argument.

ARCHIVE_MANIFEST.json records each included source's SHA-256 and byte size.
Fixed timestamps and sorted paths make identical inputs produce identical ZIP bytes.
""").encode()
    if args.source_publication_only:
        payload['README.md'] = payload['README.md'].replace(
            b'Standalone publication, source-identity and decision check:\n    python3 tools/verify_current_publication.py --metadata-only',
            b'Source-publication identity check (no mathematical replay):\n'
            b'    python3 -c "import json,sys;from pathlib import Path;sys.path.insert(0,\'tools\');from build_review_20261017_archive import source_publication_metadata;print(json.dumps(source_publication_metadata(Path.cwd())))"\n\n'
            b'The strict current-publication verifier remains available and requires both completed canonical frontier lanes. An unfinished lane is not represented as a PASS.')
    from rank7_publication import summary
    payload['README.md'] += ('\n' + summary(root) + '\n').encode()
    from rank8_publication import summary as rank8_summary
    payload['README.md'] += ('\n' + rank8_summary(root) + '\n').encode()
    from rank8_creative_20261022 import active as creative_active, PUBLICATION as CREATIVE_PUBLICATION
    creative_current = creative_active(root)
    if creative_current and args.source_publication_only:
        payload['README.md'] = payload['README.md'].replace(
            b'both completed canonical frontier lanes',
            b'both completed canonical creative-stage targeted lanes and their logs')
    from rank8_frontier import active as frontier_active, PUBLICATION
    if frontier_active(root) and not creative_current:
        payload['README.md'] += (
            ('\nThe dedicated rank-eight source archive preserves completed canonical replay receipts '
             'and logs. No new extracted mathematical replay is claimed. '
             if args.source_publication_only else
             '\nThe dedicated rank-eight archive\'s extracted mathematical replay receipts and logs are preserved here. ')
            + 'Their validated archive identity and unchanged '
            'mathematical inputs are recorded in `'+PUBLICATION+'/dedicated_replay_provenance.json`; '
            'the dedicated root release manifest is included alongside it. Publication '
            'documents in this common archive are freshly collected.\n').encode()
    from rank8_next import active as next_active, PUBLICATION as NEXT_PUBLICATION
    from rank8_research_20261022 import active as research_active, PUBLICATION as RESEARCH_PUBLICATION
    if creative_current:
        payload['README.md'] += (
            '\nThe current rank-eight creative stage realizes R8_3_982 as the triality-zero '
            'component of the known unitary E21 fusion category. Its source graph, full '
            '24-object fusion tensor and exact 512-coefficient neutral-component identity '
            'are included. Both completed canonical targeted replay receipts (normal and '
            'optimized Python), their logs, and all current scientific inputs are bound '
            'by the creative source manifest. The dedicated release identity and current '
            'publication-document overlays are recorded in `'
            + CREATIVE_PUBLICATION + '/dedicated_release_provenance.json`. The dedicated '
            'creative ZIP is published separately. The entire immutable historical ZIP '
            '`supplements/rank8/release/rank8-certified-research-20261022.zip` is included '
            'byte-for-byte, preserving the old routers and proof sources.\n\n'
            'Replay the current creative mathematics with:\n'
            '    python3 tools/verify_rank8_creative_20261022.py\n'
            '    python3 -O tools/verify_rank8_creative_20261022.py\n\n'
            'Adding --historical replays the earlier rank-eight mathematical chain from '
            'the pinned nested archive with assertions enabled. Common-archive extraction '
            'checks publication metadata and does not claim a fresh historical mathematical '
            'replay. Five rank-eight cases remain unresolved.\n').encode()
    elif research_active(root):
        payload['README.md'] += (
            '\nThe current rank-eight research stage is included as expanded sources. '
            'The accepted decisions and current case counts are recorded in its ledger. '
            'Both completed targeted replay receipts '
            '(all accepted mathematical checks, with child assertions enabled) and '
            'their logs are included. The finalized dedicated release is bound by `'
            + RESEARCH_PUBLICATION + '/dedicated_release_provenance.json`. Its ZIP is '
            'published separately. Every member of the previous next-stage archive '
            'is preserved byte-for-byte at the path recorded in the current package '
            'manifest. Extracted packaging checks verify metadata; the earlier '
            'mathematical receipts retain their original proof scope.\n').encode()
    elif next_active(root):
        payload['README.md'] += (
            '\nThe current rank-eight continuation is included as expanded sources, with its '
            'accepted decisions, model catalogue, research audit, exact evidence and source '
            'manifest. The finalized dedicated release is bound by `'
            + NEXT_PUBLICATION + '/dedicated_release_provenance.json`. Its ZIP is published '
            'separately, without duplication inside this archive. Every prior frontier member '
            'is preserved at its original path or at the historical path recorded in the '
            'current package manifest. Dedicated next extraction checks verify metadata; '
            'older mathematical replay receipts retain their original proof scope.\n').encode()
    payload['ARCHIVE_MANIFEST.json'] = (json.dumps({name: {'bytes': len(raw), 'sha256': digest(raw)}
                                                   for name, raw in sorted(payload.items())}, indent=2) + '\n').encode()
    output = (args.output or root / 'site/dist/downloads' / f'{PREFIX}.zip').resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review-bundle-') as directory:
        temp = Path(directory)
        archive = temp / output.name
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name, raw in sorted(payload.items()):
                info = zipfile.ZipInfo(PREFIX + '/' + name, date_time=(2026, 10, 17, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.create_system = 3
                bundle.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        extracted = temp / 'extracted'
        with zipfile.ZipFile(archive) as bundle:
            if bundle.testzip() is not None:
                raise ValueError('ZIP integrity')
            bundle.extractall(extracted)
        isolated = extracted / PREFIX
        inventory = json.loads((isolated / 'ARCHIVE_MANIFEST.json').read_text())
        actual = {path.relative_to(isolated).as_posix() for path in isolated.rglob('*') if path.is_file()}
        if actual != set(inventory) | {'ARCHIVE_MANIFEST.json'}:
            raise ValueError('Extracted archive inventory differs from its manifest')
        for name, expected in inventory.items():
            raw = (isolated / name).read_bytes()
            if len(raw) != expected['bytes'] or digest(raw) != expected['sha256']:
                raise ValueError('Extracted archive source identity: ' + name)
        if args.source_publication_only:
            command = [sys.executable, '-c',
                       "import json,sys;from pathlib import Path;sys.path.insert(0,'tools');"
                       "from build_review_20261017_archive import source_publication_metadata;"
                       "print(json.dumps(source_publication_metadata(Path.cwd())))"]
        else:
            command = [sys.executable, str(isolated / 'tools/verify_current_publication.py'), '--metadata-only']
        run = subprocess.run(command, cwd=isolated, text=True, capture_output=True)
        if run.returncode:
            raise ValueError('Standalone publication check failed:\n' + run.stdout + run.stderr)
        receipt = json.loads(run.stdout)
        expected_status = 'SOURCE_PUBLICATION_METADATA_PASS' if args.source_publication_only else 'PASS'
        if receipt['status'] != expected_status or receipt['historical_accepted_decisions'] != 36:
            raise ValueError('Inconsistent receipt')
        # Some extension members are generated byte streams (in particular
        # preserved baseline_members), not files in the checkout. Recollect
        # the complete payload to bind those origins as well as disk inputs.
        fresh_inputs = {name: digest(raw) for name, raw in collect(root, args.source_publication_only).items()}
        if fresh_inputs != inputs:
            changed = sorted(name for name in set(inputs) | set(fresh_inputs)
                             if inputs.get(name) != fresh_inputs.get(name))
            raise ValueError('Inputs changed during packaging: ' + ', '.join(changed))
        temporary = output.with_suffix('.writing')
        temporary.write_bytes(archive.read_bytes())
        temporary.replace(output)
    storage = package_publication_archive(root, output)
    print(json.dumps({'status': 'PASS', 'files': len(payload), 'archive': str(output),
                      'publication_mode': ('source_publication' if args.source_publication_only else
                                           'creative_targeted_receipts_and_extracted_metadata' if creative_current else
                                           'extracted_full_replay_preserved'),
                      'sha256': digest(output.read_bytes()), 'bytes': output.stat().st_size,
                      'publication_storage': storage, 'standalone_metadata_check': receipt}, indent=2))


if __name__ == '__main__':
    main()
