"""Compare native elimination with independent rational row reduction.

This is an audit probe, not a replacement census proof. It uses all generated
parameter records and fixed-seed boundary/random inputs for each duality type.
"""
if not __debug__:
    raise RuntimeError("Run this audit with Python assertions enabled")

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import random
import subprocess
import tempfile
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / 'final_census/generator'

def generate(kind, temporary):
    binary = temporary / kind
    subprocess.run(['g++', '-O1', '-g', '-std=c++17', '-fopenmp',
                    '-fsanitize=undefined', '-fno-sanitize-recover=undefined',
                    str(GEN / f'enumerate_{kind}.cpp'), '-o', str(binary)],
                   check=True, capture_output=True)
    completed = subprocess.run([str(binary), '4'], check=True, capture_output=True, text=True)
    return completed.stdout.splitlines()

with tempfile.TemporaryDirectory() as temporary:
    temp = Path(temporary)
    with ThreadPoolExecutor(max_workers=2) as pool:
        outputs = list(pool.map(lambda kind: generate(kind, temp), ('selfdual', 'nonselfdual')))
    lines = [line for group in outputs for line in group]
    assert len(lines) == 269
    print('Both optimized generators completed the multiplicity-four census with undefined-behavior sanitization: 269 rings.', flush=True)
    cases = {'S': [], 'N2': [], 'N4': []}
    for line in lines:
        tag, *values = line.split()
        cases[tag].append(tuple(map(int, values)))

    wide_printer = r'''
void print_wide(Wide v) {
 if (v<0) {std::cout << '-';v=-v;}
 std::string digits;
 do {digits += char('0'+v%10);v/=10;} while(v);
 std::reverse(digits.begin(),digits.end());std::cout << digits;
}
'''
    rng = random.Random(20261124)
    total = 0
    for tag, rows, width, length in [('S', 15, 11, 20), ('N2', 11, 5, 13), ('N4', 12, 3, 13)]:
        if tag == 'S':
            source = (GEN / 'linear_completion.hpp').read_text()
            body = source.split('void linear_completion(Vec v,int lower){', 1)[1].split(
                'for(int i=rank;i<15;++i)if(A[i][10]!=0)return;', 1)[0]
            point = 'int piv[10]'
        else:
            source = (GEN / 'enumerate_nonselfdual.cpp').read_text()
            body = source.split(f'void complete{tag[1:]}(V v){{', 1)[1].split(
                'for(int i=rank;i<nr;++i)if(A[i][nc])return;', 1)[0]
            point = 'const int nr='
        before, after = body.split(point, 1)
        copy = f'Wide original[{rows}][{width}];for(int i=0;i<{rows};i++)for(int j=0;j<{width};j++)original[i][j]=A[i][j];\n'
        emit = f'for(auto &matrix:{{original,A}})for(int i=0;i<{rows};i++)for(int j=0;j<{width};j++){{print_wide(matrix[i][j]);std::cout<<" ";}}std::cout<<"\\n";\n'
        program = ('#include <array>\n#include <algorithm>\n#include <iostream>\n#include <string>\n#include <stdexcept>\n'
                   '#include "census_integer.hpp"\nusing I=long long;\n'+wide_printer+
                   f'using Vec=std::array<I,{length}>;void probe(Vec v){{\n'+before+copy+point+after+emit+'}\n'+
                   f'int main(){{Vec v;while(std::cin>>v[0]){{for(int j=1;j<{length};j++)std::cin>>v[j];probe(v);}}}}\n')
        cpp, binary = temp / f'probe_{tag}.cpp', temp / f'probe_{tag}'
        cpp.write_text(program)
        subprocess.run(['g++', '-O1', '-std=c++17', '-I', str(GEN), '-fsanitize=undefined',
                        '-fno-sanitize-recover=undefined', str(cpp), '-o', str(binary)],
                       check=True, capture_output=True)
        inputs = {tuple(v)+(0,)*(length-len(v)) for v in cases[tag]}
        inputs.update((0,)*length for _ in [0])
        inputs.add((4,)*length)
        for _ in range(128):
            inputs.add(tuple(rng.randrange(5) for _ in range(length)))
        data = '\n'.join(' '.join(map(str, v)) for v in sorted(inputs))+'\n'
        result = subprocess.run([str(binary)], input=data, text=True, capture_output=True, check=True)
        assert len(result.stdout.splitlines()) == len(inputs)
        for line in result.stdout.splitlines():
            values = list(map(int, line.split()))
            assert len(values) == 2*rows*width
            left = s.Matrix(rows, width, values[:rows*width])
            right = s.Matrix(rows, width, values[rows*width:])
            assert left.rref()[0] == right.rref()[0], (tag, left, right)
        print(f'{tag}: {len(inputs)} native augmented-matrix eliminations agree with independent exact rational row reduction.', flush=True)
        total += len(inputs)
    assert total == 659, 'incomplete linear-completion audit coverage'
    print(f'Linear-completion probe complete: {total} augmented matrices.', flush=True)
