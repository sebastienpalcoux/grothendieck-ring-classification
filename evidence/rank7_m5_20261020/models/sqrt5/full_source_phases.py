#!/usr/bin/env python3
"""Exact relative two-moment phases over two multiquadratic fields.

phase_records('L4') returns 22 records: 21 nonzero pairs obtained in Q(zeta_80)
and the zero pair for higher 2/5-primary orders. Coordinates are scaled by 8
in the ordered basis (1,sqrt(5),sqrt(-2),sqrt(-10)), first moment then second.
The fixed-row multiplicity restrictions require the categorical Galois
action described in FULL_SOURCE_PHASES_PROOF.md.

phase_records('F8') uses Q(sqrt(5),sqrt(2),i), returns 37 records, and uses
basis (1,sqrt(5),sqrt(2),sqrt(10),i,i*sqrt(5),i*sqrt(2),i*sqrt(10)).
The default L4 is retained for compatibility; F8 is the stronger unified set.
"""
from functools import lru_cache
import argparse
import json
import math
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chi_minus8(value):
    require(value % 2 == 1, "odd input for the conductor-eight character")
    return 1 if value % 8 in (1, 3) else -1


@lru_cache(maxsize=2)
def phase_records(field="L4"):
    """Return exact integer phase tuples and their order/multiplicity provenance."""
    x = s.Symbol("x")
    modulus = s.Poly(s.cyclotomic_poly(80, x), x, domain=s.QQ)
    require(modulus.degree() == 32, "cyclotomic degree")
    def reduce(value):
        return s.Poly(value, x, domain=s.QQ).rem(modulus)
    unit = reduce(1)
    sqrt5 = reduce(1 + 2*(x**16 + x**64))
    sqrt_minus2 = reduce(x**10 + x**30)
    sqrt_minus10 = reduce(sqrt5.as_expr() * sqrt_minus2.as_expr())
    if field == "L4":
        basis = [unit, sqrt5, sqrt_minus2, sqrt_minus10]
        subgroup = [1, 9, 11, 19, 41, 49, 51, 59]
        expected_count = 21
    elif field == "F8":
        sqrt2 = reduce(x**10 + x**70)
        imaginary_unit = reduce(x**20)
        require(reduce(sqrt2.as_expr()**2).as_expr() == 2, "sqrt-two embedding")
        require(reduce(imaginary_unit.as_expr()**2).as_expr() == -1, "imaginary-unit embedding")
        real_basis = [unit, sqrt5, sqrt2, reduce(sqrt5.as_expr()*sqrt2.as_expr())]
        basis = real_basis + [reduce(imaginary_unit.as_expr()*value.as_expr()) for value in real_basis]
        subgroup = [1, 9, 41, 49]
        expected_count = 36
    else:
        raise ValueError("field must be L4 or F8")
    require(reduce(sqrt5.as_expr()**2).as_expr() == 5, "sqrt-five embedding")
    require(reduce(sqrt_minus2.as_expr()**2).as_expr() == -2, "sqrt-minus-two embedding")
    vectors = s.Matrix([[value.nth(j) for value in basis] for j in range(32)])
    require(vectors.rank() == len(basis), "multiquadratic basis independence")
    source_fixing_subgroup = [u for u in range(80) if math.gcd(u, 80) == 1
                and u % 5 in (1, 4) and chi_minus8(u) == 1]
    require(source_fixing_subgroup == [1, 9, 11, 19, 41, 49, 51, 59], "source-fixing Galois subgroup")
    require(len(subgroup)*len(basis) == 32, "relative subgroup index")
    for u in subgroup:
        for value in basis:
            require(reduce(value.as_expr().subs(x, x**u)) == value, "fixed field basis")
    @lru_cache(maxsize=None)
    def relative_trace(exponent):
        value = reduce(sum(x**((exponent*u) % 80) for u in subgroup) / len(subgroup))
        coefficients = vectors.gauss_jordan_solve(s.Matrix([value.nth(j) for j in range(32)]))[0]
        require(all(coefficient.is_Rational for coefficient in coefficients), "rational phase coordinates")
        return tuple(coefficients)
    grouped = {}
    for k in range(80):
        raw = relative_trace(k) + relative_trace(2*k)
        scaled = tuple(8*value for value in raw)
        require(all(value.is_Integer for value in scaled), "scale-eight integrality")
        scaled = tuple(map(int, scaled))
        grouped.setdefault(scaled, []).append(k)
    require(len(grouped) == expected_count and (0,)*(2*len(basis)) not in grouped,
            "complete nonzero finite phase list")
    if field == "F8":
        def coordinates(value):
            polynomial = reduce(value)
            answer = vectors.gauss_jordan_solve(s.Matrix([polynomial.nth(j) for j in range(32)]))[0]
            require(all((8*z).is_Integer for z in answer), "closed-form phase scale")
            return tuple(int(8*z) for z in answer)
        xi = x**10
        cases = [(1, 1)] + [((-1+delta*sqrt5.as_expr())/4,
                            (-1-delta*sqrt5.as_expr())/4) for delta in (-1, 1)]
        closed_form = {coordinates(xi**j*c1) + coordinates(xi**(2*j)*c2)
                       for j in range(8) for c1, c2 in cases}
        closed_form.update((0,)*8 + coordinates(xi**j*c1)
                           for j in (1, 3, 5, 7) for c1, c2 in cases)
        require(len(closed_form) == 36 and closed_form == set(grouped),
                "24 plus 12 closed-form phase description")
    records = []
    for scaled, exponents in sorted(grouped.items()):
        orders = sorted({80 // math.gcd(80, k) for k in exponents})
        require(len(orders) == 1, "unique order provenance of finite phase")
        order = orders[0]
        multiple = 2 if order in (16, 80) else 1
        # Automorphisms fixing the entire source field act by squares on twists.
        for k in exponents:
            orbit = {(k*u*u) % 80 for u in source_fixing_subgroup}
            require(len(orbit) == multiple, "fixed-row square-action orbit size")
            require(all(relative_trace(j) + relative_trace(2*j)
                        == tuple(s.Rational(v, 8) for v in scaled) for j in orbit),
                    "relative phase invariant under square action")
        records.append({"scaled8": scaled, "orders": orders, "exponents80": exponents,
                        "fixed_row_multiple": multiple, "zero_semigroup": None})
    records.append({"scaled8": (0,)*(2*len(basis)), "orders": [], "exponents80": [],
                    "fixed_row_multiple": 1, "zero_semigroup": [4, 5],
                    "order_condition": "2^a*5^b with a>=5 or b>=2"})
    return records


def phases_scaled8(field="L4"):
    """Return the phase tuples, with the genuine zero phase last."""
    return [record["scaled8"] for record in phase_records(field)]


@lru_cache(maxsize=1)
def phase_records_fourth():
    """The49 exact F8 phase records for moments1,2,4, with all-level metadata.

    `scaled8` retains the old16-coordinate first/second-moment interface.
    `fourth_scaled8` has8 coordinates in the same F8 basis. The concatenated
    `moments_scaled8` has24 coordinates and distinguishes all49 records.
    """
    x=s.Symbol('x');modulus=s.Poly(s.cyclotomic_poly(160,x),x,domain=s.QQ)
    require(modulus.degree()==64,'degree of cyclotomic160')
    def reduce(value):return s.Poly(value,x,domain=s.QQ).rem(modulus)
    unit=reduce(1);sqrt5=reduce(1+2*(x**32+x**128));sqrt2=reduce(x**20+x**140);imaginary=reduce(x**40)
    require(reduce(sqrt5.as_expr()**2).as_expr()==5,'fourth-inventory sqrt5 embedding')
    require(reduce(sqrt2.as_expr()**2).as_expr()==2,'fourth-inventory sqrt2 embedding')
    require(reduce(imaginary.as_expr()**2).as_expr()==-1,'fourth-inventory imaginary embedding')
    real=[unit,sqrt5,sqrt2,reduce(sqrt5.as_expr()*sqrt2.as_expr())]
    basis=real+[reduce(imaginary.as_expr()*v.as_expr()) for v in real]
    vectors=s.Matrix([[v.nth(j) for v in basis] for j in range(64)])
    require(vectors.rank()==8,'fourth-inventory field basis')
    pivots=vectors.T.rref()[1];inverse=vectors.extract(pivots,range(8)).inv()
    subgroup=[u for u in range(160) if math.gcd(u,160)==1 and u%8==1 and u%5 in (1,4)]
    require(subgroup==[1,9,41,49,81,89,121,129],'F8 fixing subgroup modulo160')
    source_subgroup=[u for u in range(160) if math.gcd(u,160)==1 and u%5 in (1,4) and chi_minus8(u)==1]
    require(len(source_subgroup)==16,'complete source-field-fixing subgroup')
    for u in subgroup:
        for b in basis:require(reduce(b.as_expr().subs(x,x**u))==b,'F8 basis fixed by relative subgroup')
    def coordinates(poly):
        vec=s.Matrix([poly.nth(j) for j in range(64)]);answer=inverse*vec.extract(pivots,[0])
        require(vectors*answer==vec,'exact membership in F8')
        return tuple(answer)
    @lru_cache(maxsize=160)
    def relative_trace(k):
        k%=160
        return coordinates(reduce(sum(x**((k*u)%160) for u in subgroup)/8))
    @lru_cache(maxsize=160)
    def moments(k):return relative_trace(k%160)+relative_trace(2*k%160)+relative_trace(4*k%160)
    grouped={}
    for k in range(160):
        scaled=tuple(8*t for t in moments(k));require(all(t.is_Integer for t in scaled),'fourth moment scale8')
        grouped.setdefault(tuple(map(int,scaled)),[]).append(k)
    require(len(grouped)==48 and (0,)*24 not in grouped,'complete48 nonzero moment triples')
    def scaled_coordinates(value):
        ans=coordinates(reduce(value));require(all((8*t).is_Integer for t in ans),'closed fourth-moment coordinates')
        return tuple(int(8*t) for t in ans)
    xi=x**20;cases=[(1,1)]+[((-1+delta*sqrt5.as_expr())/4,(-1-delta*sqrt5.as_expr())/4) for delta in (-1,1)]
    closed={scaled_coordinates(xi**j*c1)+scaled_coordinates(xi**(2*j)*c2)+scaled_coordinates(xi**(4*j)*c1) for j in range(8) for c1,c2 in cases}
    closed.update((0,)*8+scaled_coordinates(xi**j*c1)+scaled_coordinates(xi**(2*j)*c2) for j in (1,3,5,7) for c1,c2 in cases)
    closed.update((0,)*16+scaled_coordinates(xi**j*c1) for j in (1,3,5,7) for c1,c2 in cases)
    require(closed==set(grouped) and len(closed)==48,'24+12+12 closed-form inventory')
    old=phase_records(field='F8');old_index={tuple(r['scaled8']):i for i,r in enumerate(old)}
    records=[]
    for scaled,exponents in sorted(grouped.items()):
        orders=sorted({160//math.gcd(160,k) for k in exponents});require(len(orders)==1,'unique fourth-inventory order')
        order=orders[0];multiple=4 if order in (32,160) else 2 if order in (16,80) else 1
        for k in exponents:
            orbit={(k*u*u)%160 for u in source_subgroup}
            require(len(orbit)==multiple,'exact source-fixed square-orbit length modulo160')
            require(all(moments(j)==moments(k) for j in orbit),'full moment triple fixed on source-fixed packet')
        records.append({'scaled8':scaled[:16],'fourth_scaled8':scaled[16:],'moments_scaled8':scaled,
                        'orders':orders,'exponents160':exponents,'fixed_row_multiple':multiple,'zero_semigroup':None,
                        'first_two_phase_index':old_index[scaled[:16]]})
    records.append({'scaled8':(0,)*16,'fourth_scaled8':(0,)*8,'moments_scaled8':(0,)*24,
                    'orders':[],'exponents160':[],'fixed_row_multiple':1,'zero_semigroup':[8,5],
                    'order_condition':'2^a*5^b with a>=6 or b>=2',
                    'first_two_phase_index':old_index[(0,)*16],
                    'actual_T_fixed_up_to_duality_zero_multiples':{'five_part_1':8,'five_part_5':16,'five_part_at_least_25':10}})
    require(len(records)==49,'49 total fourth-moment phase records')
    require(sum(all(t==0 for t in r['scaled8']) and any(t!=0 for t in r['fourth_scaled8']) for r in records)==12,'twelve fourth-only records')
    return records



@lru_cache(maxsize=None)
def phase_records_powers(max_power=3):
    """F8 relative phases for moments 1,2,...,2**max_power.

    This separate generic API leaves the historical two- and three-moment
    records unchanged. The first two moments remain in ``scaled8``; later
    moments have named fields and all moments occur in ``moments_scaled8``.
    There are 25+12*max_power records, including the higher-order zero.
    """
    require(isinstance(max_power,int) and max_power>=1,'max_power must be an integer at least1')
    M=40*2**max_power; degree=16*2**max_power
    x=s.Symbol('x'); modulus=s.Poly(s.cyclotomic_poly(M,x),x,domain=s.QQ)
    require(modulus.degree()==degree,'generic cyclotomic degree')
    def reduce(value):return s.Poly(value,x,domain=s.QQ).rem(modulus)
    unit=reduce(1);sqrt5=reduce(1+2*(x**(M//5)+x**(4*M//5)))
    sqrt2=reduce(x**(M//8)+x**(7*M//8));imaginary=reduce(x**(M//4))
    for value,square,name in ((sqrt5,5,'sqrt5'),(sqrt2,2,'sqrt2'),(imaginary,-1,'i')):
        require(reduce(value.as_expr()**2).as_expr()==square,'generic embedding '+name)
    real=[unit,sqrt5,sqrt2,reduce(sqrt5.as_expr()*sqrt2.as_expr())]
    basis=real+[reduce(imaginary.as_expr()*v.as_expr()) for v in real]
    vectors=s.Matrix([[v.nth(j) for v in basis] for j in range(degree)])
    require(vectors.rank()==8,'generic F8 field basis')
    pivots=vectors.T.rref()[1]; inverse=vectors.extract(pivots,range(8)).inv()
    subgroup=[u for u in range(M) if math.gcd(u,M)==1 and u%8==1 and u%5 in (1,4)]
    source_subgroup=[u for u in range(M) if math.gcd(u,M)==1 and u%5 in (1,4) and chi_minus8(u)==1]
    require(len(subgroup)*8==degree and len(source_subgroup)==2*len(subgroup),'generic subgroup sizes')
    # Check the fixed field through generators, with exponents reduced first.
    for u in subgroup:
        require(reduce(1+2*(x**((M//5*u)%M)+x**((4*M//5*u)%M)))==sqrt5,'generic fixed sqrt5')
        require(reduce(x**((M//8*u)%M)+x**((7*M//8*u)%M))==sqrt2,'generic fixed sqrt2')
        require(reduce(x**((M//4*u)%M))==imaginary,'generic fixed i')
    def coordinates(poly):
        vec=s.Matrix([poly.nth(j) for j in range(degree)]);answer=inverse*vec.extract(pivots,[0])
        require(vectors*answer==vec,'generic exact membership in F8')
        return tuple(answer)
    @lru_cache(maxsize=None)
    def relative_trace(k):
        k%=M
        return coordinates(reduce(sum(x**((k*u)%M) for u in subgroup)/len(subgroup)))
    @lru_cache(maxsize=None)
    def moments(k):return sum((relative_trace((2**j*k)%M) for j in range(max_power+1)),())
    grouped={}
    for k in range(M):
        scaled=tuple(8*t for t in moments(k));require(all(t.is_Integer for t in scaled),'generic scale-eight moments')
        grouped.setdefault(tuple(map(int,scaled)),[]).append(k)
    width=8*(max_power+1);expected=24+12*max_power
    require(len(grouped)==expected and (0,)*width not in grouped,'generic nonzero phase count')
    def scaled_coordinates(value):
        ans=coordinates(reduce(value));require(all((8*t).is_Integer for t in ans),'generic closed-form scale')
        return tuple(int(8*t) for t in ans)
    xi=x**(M//8)
    cases=[(1,1)]+[((-1+delta*sqrt5.as_expr())/4,(-1-delta*sqrt5.as_expr())/4) for delta in (-1,1)]
    closed=set()
    for first in range(max_power+1):
        for ell in (range(8) if first==0 else (1,3,5,7)):
            for c in cases:
                value=(0,)*(8*first)
                for j in range(first,max_power+1):
                    value+=scaled_coordinates(xi**((2**(j-first)*ell)%8)*c[(j-first)%2])
                closed.add(value)
    require(closed==set(grouped) and len(closed)==expected,'generic 24+12k closed-form inventory')
    old=phase_records('F8');old_index={tuple(r['scaled8']):i for i,r in enumerate(old)}
    fourth=phase_records_fourth() if max_power>=2 else None
    fourth_index={tuple(r['moments_scaled8']):i for i,r in enumerate(fourth)} if fourth else None
    records=[]
    for scaled,exponents in sorted(grouped.items()):
        orders=sorted({M//math.gcd(M,k) for k in exponents});require(len(orders)==1,'generic unique exact order')
        order=orders[0];a=0;odd=order
        while odd%2==0:a+=1;odd//=2
        require(odd in (1,5),'finite generic order prime factors')
        multiple=2**max(a-3,0)
        for k in exponents:
            orbit={(k*u*u)%M for u in source_subgroup}
            require(len(orbit)==multiple,'generic source-fixed square-action orbit size')
            require(all(moments(j)==moments(k) for j in orbit),'generic moments fixed on source packet')
        record={'scaled8':scaled[:16],'moments_scaled8':scaled,'orders':orders,
                'exponents_modulus':exponents,'cyclotomic_modulus':M,'exponents'+str(M):exponents,
                'fixed_row_multiple':multiple,'zero_semigroup':None,
                'first_two_phase_index':old_index[scaled[:16]]}
        if max_power>=2:record.update(fourth_scaled8=scaled[16:24],fourth_phase_index=fourth_index[scaled[:24]])
        if max_power>=3:record['eighth_scaled8']=scaled[24:32]
        records.append(record)
    zero={'scaled8':(0,)*16,'moments_scaled8':(0,)*width,'orders':[],
          'exponents_modulus':[],'cyclotomic_modulus':M,'exponents'+str(M):[],
          'fixed_row_multiple':1,'zero_semigroup':[2**(max_power+1),5],
          'order_condition':f'2^a*5^b with a>={max_power+4} or b>=2',
          'first_two_phase_index':old_index[(0,)*16],
          'actual_T_fixed_up_to_duality_zero_multiples':{'five_part_1':2**(max_power+1),
              'five_part_5':2**(max_power+2),'five_part_at_least_25':10}}
    if max_power>=2:zero.update(fourth_scaled8=(0,)*8,fourth_phase_index=fourth_index[(0,)*24])
    if max_power>=3:zero['eighth_scaled8']=(0,)*8
    records.append(zero)
    require(len(records)==expected+1,'generic total phase count')
    # Exact projection checks keep old stable inventories usable without any
    # assumptions about the independently sorted generic record numbering.
    require({tuple(r['scaled8']) for r in records}==set(old_index),'generic projection to old37 phases')
    if max_power>=2:
        require({tuple(r['moments_scaled8'][:24]) for r in records}==set(fourth_index),'generic projection to old49 phases')
    if max_power==2:
        by_tuple={tuple(r['moments_scaled8']):r for r in fourth}
        for r in records:
            previous=by_tuple[tuple(r['moments_scaled8'])]
            for key in ('orders','fixed_row_multiple','zero_semigroup'):
                require(r[key]==previous[key],'generic fourth inventory compatibility '+key)
            require(r['exponents_modulus']==previous['exponents160'],'generic fourth exponent compatibility')
    return records


def powers_receipt(max_power=3):
    records=phase_records_powers(max_power);M=40*2**max_power
    return {'schema':'relative-F8-power-of-two-moments-v1','basis':['1','sqrt(5)','sqrt(2)','sqrt(10)','i','i*sqrt(5)','i*sqrt(2)','i*sqrt(10)'],
            'scale':8,'max_power':max_power,'moments':[2**j for j in range(max_power+1)],
            'cyclotomic_modulus':M,'cyclotomic_degree':16*2**max_power,
            'relative_subgroup':[u for u in range(M) if math.gcd(u,M)==1 and u%8==1 and u%5 in (1,4)],
            'nonzero_phase_count':len(records)-1,'total_phase_count':len(records),'phases':records}


def fourth_receipt():
    return {'schema':'relative-F8-moments-1-2-4-v1','basis':['1','sqrt(5)','sqrt(2)','sqrt(10)','i','i*sqrt(5)','i*sqrt(2)','i*sqrt(10)'],
            'scale':8,'moments':[1,2,4],'cyclotomic_modulus':160,'cyclotomic_degree':64,
            'relative_subgroup':[1,9,41,49,81,89,121,129],'nonzero_phase_count':48,'total_phase_count':49,
            'phases':phase_records_fourth()}


def receipt(field="L4"):
    bases = {"L4": ["1", "sqrt(5)", "sqrt(-2)", "sqrt(-10)"],
             "F8": ["1", "sqrt(5)", "sqrt(2)", "sqrt(10)", "i", "i*sqrt(5)", "i*sqrt(2)", "i*sqrt(10)"]}
    return {
        "schema": "relative-full-source-field-two-moments-v1",
        "field": "Q(sqrt(5),sqrt(-2))" if field == "L4" else "Q(sqrt(5),sqrt(2),i)", "basis": bases[field],
        "scale": 8, "cyclotomic_modulus": 80, "cyclotomic_degree": 32,
        "relative_subgroup": [1, 9, 11, 19, 41, 49, 51, 59] if field == "L4" else [1, 9, 41, 49],
        "nonzero_phase_count": len(phase_records(field))-1, "total_phase_count": len(phase_records(field)),
        "phases": phase_records(field),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--field", choices=("L4", "F8"), default="L4")
    parser.add_argument("--fourth",action="store_true",help="verify the separate49-record F8 moments1,2,4 inventory")
    parser.add_argument("--max-power",type=int,help="separate generic F8 moments1,2,...,2^k inventory")
    args = parser.parse_args()
    require(not(args.fourth and args.max_power is not None),'choose fourth or generic powers')
    result = json.loads(json.dumps(powers_receipt(args.max_power) if args.max_power is not None else fourth_receipt() if args.fourth else receipt(args.field)))
    path = HERE / (f"power_{args.max_power}_moment_phases_certificate.json" if args.max_power is not None else "fourth_moment_phases_certificate.json" if args.fourth else "full_source_phases_certificate.json" if args.field == "L4" else "maximal_multiquadratic_phases_certificate.json")
    if args.write_receipt:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(json.loads(path.read_text()) == result, "relative phase receipt mismatch")
    if args.max_power is not None:print(f"PASS: all{result['cyclotomic_modulus']} roots, {result['nonzero_phase_count']} nonzero F8 power-moment records, exact source-fixed packets, plus higher-order zero")
    elif args.fourth:print('PASS: all160 roots,48 nonzero F8 moment triples, source-fixed packet sizes, plus true higher-order zero')
    else:print(f"PASS: all 80 roots, {result['nonzero_phase_count']} nonzero {args.field} phase pairs, square-action row multiplicities, plus higher-order zero")


if __name__ == "__main__":
    main()
