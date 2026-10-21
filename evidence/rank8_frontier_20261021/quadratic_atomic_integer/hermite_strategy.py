"""Auxiliary-first exact HNF discovery with an explicit optional wall cap.

Permuting the generator columns preserves the lattice and its unique row
Hermite basis. A capped run makes no membership or obstruction assertion.
"""
from dataclasses import replace
import multiprocessing as mp
import resource
from pathlib import Path
import time
import lattice


def auxiliary_first(system, batch=512):
    order = sorted(range(len(system.columns)), key=lambda j:
        (system.column_labels[j][0] not in ('fusion_coefficient', 'unit_pair_AMGM_slack'), j))
    permuted = replace(system, columns=tuple(system.columns[j] for j in order),
                       bounds=tuple(system.bounds[j] for j in order),
                       column_labels=tuple(system.column_labels[j] for j in order))
    result = lattice.hermite(permuted, batch=batch)
    if result['outcome'] == 'integer_lattice_obstruction':
        lattice.verify_separator(system, result['certificate'])
    return result


def capped(system, seconds=120, batch=512, additional_memory_mib=256):
    context = mp.get_context('fork')
    receiver, sender = context.Pipe(duplex=False)

    def worker():
        receiver.close()
        try:
            # Limit additional virtual allocation, including FLINT's native
            # storage. Failure or an aborted native worker is inconclusive.
            status = dict(line.split(':', 1) for line in
                          Path('/proc/self/status').read_text().splitlines())
            current = int(status['VmSize'].split()[0]) * 1024
            limit = current + additional_memory_mib * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
            sender.send(auxiliary_first(system, batch))
        except Exception as error:
            sender.send({'outcome': 'no_exact_lattice_conclusion', 'worker_exception': repr(error)})
        finally:
            sender.close()

    process = context.Process(target=worker)
    process.start()
    sender.close()
    deadline = time.monotonic() + seconds
    result = None
    while time.monotonic() < deadline:
        if receiver.poll(min(0.5, max(0, deadline - time.monotonic()))):
            try:
                result = receiver.recv()
            except EOFError:
                pass
            break
        if not process.is_alive():
            break
    if result is None:
        result = {'outcome': 'no_exact_lattice_conclusion', 'wall_clock_limit': seconds,
                  'additional_virtual_memory_limit_mib': additional_memory_mib,
                  'search_interrupted': True,
                  'scope': 'no integer-lattice membership or obstruction is asserted'}
    if process.is_alive():
        process.terminate()
    process.join(timeout=5)
    if process.is_alive():
        process.kill()
        process.join(timeout=5)
    receiver.close()
    if result['outcome'] == 'no_exact_lattice_conclusion':
        result.update(wall_clock_limit=seconds,
                      additional_virtual_memory_limit_mib=additional_memory_mib,
                      scope='no integer-lattice membership or obstruction is asserted')
    if result['outcome'] == 'integer_lattice_obstruction':
        lattice.verify_separator(system, result['certificate'])
    return result
