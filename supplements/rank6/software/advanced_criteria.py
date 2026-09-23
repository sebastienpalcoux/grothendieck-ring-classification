"""General-scope wrappers for the existing advanced necessary conditions.

These routines do not turn a failed character, pseudo-unitary obstruction,
timeout, or failed search into a general exclusion.  They either use an exact
categorical reduction or cover every oriented sphericalization branch.  The
returned proof trees use the existing exact checker's certificate vocabulary.
"""
import itertools
import math

import sympy as s

import character_induction
import dimension_order
import modular_character_induction
import oriented_extension
import proofs
import tensor_rotation
from exact import pc, require
from involution_module import generated_basis
from oriented_signed import enumerate_all, from_values
from rings import Characters, flat, matrices


MODES = ('dimension_order', 'character', 'tensor_rotation', 'modular')


def _squarefree_discriminant(f):
    a, b, c = f.all_coeffs()
    discriminant = s.Rational(b*b-4*a*c)
    # The factors are monic integral characteristic-polynomial factors.
    require(discriminant.q == 1, 'nonintegral quadratic discriminant')
    return (-1 if discriminant < 0 else 1) * math.prod(
        int(p) for p, exponent in s.factorint(abs(int(discriminant))).items()
        if exponent % 2)


def eligibility(R, mode='dimension_order', height=6):
    """Report checked implementation hypotheses, not categorifiability.

    Eligibility means that the generator can attempt its finite condition.
    A generator returning None supplies no complete exclusion certificate.
    Runtime limits must be enforced by the calling campaign and recorded as
    time limits, rather than as mathematical outcomes.
    """
    require(mode in MODES, 'unknown advanced criterion')
    require(type(height) is int and 2 <= height <= 12, 'invalid trace height')
    info = {'mode': mode, 'scope': 'general_after_verified_reduction',
            'eligible': False, 'height': height}
    n = len(R)
    if n != 6:
        return info | {'reason': 'the general oriented wrapper is rank-six only'}
    if any(R[i][j] != R[j][i] for i in range(n) for j in range(n)):
        return info | {'reason': 'commutative character machinery required'}
    if max(flat(R)) > 32:
        return info | {'reason': 'oriented signed engine coefficient bound is 32'}
    a = Characters(R)
    f, K, ds, D, pD, emb = a.fp()
    gate = ('weak_integrality' if pD.degree() == 1 else
            'two_FP_values' if len(set(ds)) == 2 else None)
    info.update(fp_field_degree=f.degree(), general_reduction=gate or
                'complete_oriented_sphericalization')
    if mode == 'dimension_order':
        return info | {'eligible': True,
                       'reason': 'exact spherical-character lattice test with full lifting'}
    if f.degree() not in (1, 2):
        return info | {'reason': 'implemented trace field must be rational or quadratic'}
    if f.degree() == 2 and pD.degree() == 1:
        return info | {'reason': 'current quadratic trace implementation requires irrational total dimension'}
    if mode == 'tensor_rotation':
        return info | {'eligible': True,
                       'reason': 'rational or quadratic rotation system; generator checks codegree splitting'}
    factors = {i: a.N[i].charpoly().as_poly().factor_list()[1]
               for i in range(1, n)}
    seed_labels = [i for i, ff in factors.items()
                   if all(g.degree() <= 2 for g, multiplicity in ff)]
    seeds = [list(seed) for size in (1, 2)
             for seed in itertools.combinations(seed_labels, size)
             if generated_basis(R, seed) is not None]
    if not seeds:
        return info | {'reason': 'no one- or two-object quadratic-spectrum generating set'}
    info['generating_sets'] = seeds
    if mode == 'modular':
        fp_squarefree = _squarefree_discriminant(f) if f.degree() == 2 else 1
        for ff in factors.values():
            for g, multiplicity in ff:
                if g.degree() > 2:
                    return info | {'reason': 'whole character field exceeds the quadratic trace field'}
                if g.degree() == 2 and _squarefree_discriminant(g) != fp_squarefree:
                    return info | {'reason': 'a character field lies outside the relative trace field'}
    return info | {'eligible': True,
                   'reason': 'character generator hypotheses checked; low-frame coverage checked in generator'}


def _sphere_with_order(R, height):
    """Augment the spherical character tree by the existing order criterion."""
    a = Characters(R)
    fp = a.fp()[0]
    branches = []
    pseudo = None
    for f, multiplicity in a.components:
        K, ds, D, pD = a.component(f)
        zero = next((i for i, d in enumerate(ds) if not d), None)
        unequal = next((i for i in range(a.n) if ds[i] != ds[a.du[i]]), None)
        if zero is not None:
            why = {'kind': 'zero', 'object': zero}
        elif unequal is not None:
            why = {'kind': 'duality', 'object': unequal}
        else:
            why = (proofs.norm_failure(pD, a.cf) or
                   proofs.field_failure(f, a.cf) or
                   dimension_order.certificate(a, f) or
                   proofs.spherical_global_moment(a, f))
            if why is None:
                reduction = ({'kind': 'galois_fp'} if f == fp else
                             proofs.positive_sign_embedding(R, f, ds))
                if reduction is not None:
                    if pseudo is None:
                        pseudo = oriented_extension.pseudo_discover(R, height, True)
                    if pseudo is not None:
                        why = reduction
        if why is None:
            return None
        branches.append({'factor': pc(f), 'obstruction': why})
    return {'kind': 'spherical', 'generator': a.k,
            'characters': branches, 'pseudo': pseudo}


def _complete_oriented_lift(R, sphere, timeout):
    vals, problem, stats = enumerate_all(R, timeout)
    branches = []
    for values in vals:
        T = from_values(R, problem, values)
        branch = {'values': list(values)}
        parity = proofs.signed_adjoint_parity(R, T)
        gauge = proofs.gauge_original(T, R)
        if parity is not None:
            branch['obstruction'] = parity
        elif gauge is not None:
            branch['obstruction'] = {'kind': 'gauge_original', 'signs': gauge}
        elif any(T[i][j] != T[j][i] for i in range(6) for j in range(6)):
            cert = oriented_extension.nc_certificate(R, T)
            if cert is None:
                return None
            branch['noncommutative'] = cert
        else:
            a = Characters(T)
            characters = [{'factor': pc(f), 'obstruction':
                           proofs.signed_component_certificate(R, T, a, f, sphere)}
                          for f, multiplicity in a.components]
            if any(c['obstruction'] is None for c in characters):
                return None
            branch.update(characters=characters, generator=a.k)
        branches.append(branch)
    return {'kind': 'oriented_signed', 'sphere': sphere, 'branches': branches}


def general_certificate(R, mode='dimension_order', timeout=60, height=6):
    """Return a complete general-scope proof tree, or no conclusion.

    ``timeout`` limits the signed enumeration subprocess. The calling driver
    must separately bound the whole criterion, including discovery and
    certificate verification. Unexpected exceptions propagate as errors.
    """
    require(isinstance(timeout, (int, float)) and timeout > 0,
            'signed enumeration timeout must be positive')
    info = eligibility(R, mode, height)
    if not info['eligible']:
        return None
    if mode == 'dimension_order':
        sphere = _sphere_with_order(R, height)
        return None if sphere is None else _complete_oriented_lift(R, sphere, timeout)
    generator = {'character': character_induction.certificate,
                 'tensor_rotation': tensor_rotation.certificate,
                 'modular': modular_character_induction.certificate}[mode]
    pseudo = generator(R, height=height)
    return None if pseudo is None else character_induction.lift_general(R, pseudo, timeout)


def verify(R, certificate):
    """Use the inherited exact verifier for every returned proof tree."""
    oriented_extension.verify(R, certificate)
