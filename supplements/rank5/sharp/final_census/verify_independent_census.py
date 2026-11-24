"""Optional cross-check of the optimized census and the SU(3)_4 model.

Regenerate symmetry orbits and associativity equations from the axioms,
check the C++ equations symbolically, and replay the census without its
nonlinear shortcuts. The replay shares the checked fraction-free linear
completion routine; it is not a formally verified independent implementation.
No stored witness records are read, and no network access is used.
"""
from pathlib import Path
import itertools
import json
import re
import subprocess
import sys
import tempfile

import sympy as s

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "generator"
sys.path[:0] = [str(GEN), str(ROOT / "criteria")]
from export_tables import maps, tensor
from exact import require
from rings import canonical, validate
from model_registry import build_model_registry


def symbolic_check(tag, kind, free):
    data = json.loads((GEN / f"census_system{kind}.json").read_text())
    dual, orbits = maps(5, tag, str(GEN))
    expected = {frozenset(itertools.permutations(q)) |
                frozenset(itertools.permutations(tuple(dual[i] for i in q)))
                for q in itertools.product(range(1, 5), repeat=3)}
    actual = {frozenset(t for q in orb for t in itertools.permutations(q))
              for orb in data["orbits"]}
    require(actual == expected, "incorrect reciprocity/duality orbit partition")
    variables = s.symbols(f"v:{len(orbits)}")
    R = [[[s.Integer(int(j == k) if i == 0 else int(i == k) if j == 0
                     else int(dual[i] == j) if k == 0 else 0)
           for k in range(5)] for j in range(5)] for i in range(5)]
    for variable, orb in zip(variables, orbits):
        for i, j, k in orb:
            R[i][j][k] = variable
    matrices = list(map(s.Matrix, R))

    def normalize(expression):
        p = s.Poly(expression, *variables)
        return p.monic().as_expr() if p else s.S.Zero

    equations = {normalize(q) for A in matrices for B in matrices
                 for q in A*B-B*A if q}
    stored = {normalize(sum(c*s.prod(x**a for x, a in zip(variables, powers))
                            for c, powers in row)) for row in data["equations"]}
    require(equations == stored, "stored associativity equations differ from commutators")

    def parse(expression):
        expression = re.sub(r"v\[(\d+)\]", lambda m: "v"+m.group(1), expression)
        return s.sympify(expression, locals={str(v): v for v in variables})

    if kind == 0:
        source = (GEN / "linear_completion.hpp").read_text()
        final = source.split("bool all_associative(const Vec&v){return ")[1].split(";")[0]
        linear = source.split("void linear_completion(Vec v,int lower){")[1].split("int piv[10]")[0]
    else:
        source = (GEN / "enumerate_nonselfdual.cpp").read_text()
        final = source.split(f"void emit{kind}(V v){{")[1].split("if(!(")[1].split("))return;")[0]
        linear = source.split(f"void complete{kind}(V v){{")[1].split("const int nr=")[0]
    final_equations = {normalize(parse(piece.strip()[1:-1].removesuffix("==0")))
                       for piece in final.split(" && ")}
    require(final_equations == equations, "C++ final conditions differ from associativity")
    entries = {(int(a), int(b)): parse(expression) for a, b, expression in
               re.findall(r"A\[(\d+)\]\[(\d+)\]=([^;]+);", linear)}
    nrows, ncols = 1+max(i for i, j in entries), len(free)
    linear_equations = {normalize(sum(entries.get((i, j), 0)*variables[k]
                                      for j, k in enumerate(free))
                                  - entries.get((i, ncols), 0))
                        for i in range(nrows)} - {s.S.Zero}
    require(linear_equations <= equations, "linear completion imposes a nonnecessary condition")
    print(f"{tag}: symmetry orbits, {len(equations)} associativity equations, "
          f"and {len(linear_equations)} linear equations checked.")


SELFDUAL_MAIN = r'''
int main(){
 M=4;counts=false;cnt.resize(5);
 std::vector<std::array<int,3>>tri;
 for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=j;k<4;k++)tri.push_back({i,j,k});
 std::array<int,4>p{0,1,2,3};
 do{std::array<int,20>map;
  for(int k=0;k<20;k++){
   std::array<int,3>q{p[tri[k][0]],p[tri[k][1]],p[tri[k][2]]};
   std::sort(q.begin(),q.end());map[k]=std::find(tri.begin(),tri.end(),q)-tri.begin();
  }perms.push_back(map);
 }while(std::next_permutation(p.begin(),p.end()));
 omp_set_num_threads(std::min(8,omp_get_max_threads()));
 #pragma omp parallel for schedule(dynamic,64)
 for(I ind=0;ind<15625;ind++){
  Vec v{};I x=ind;for(int j:{4,7,9,5,6,8}){v[j]=x%5;x/=5;}
  I bmax=std::min({v[4],v[7],v[9]});
  for(v[1]=0;v[1]<=bmax;v[1]++)for(v[2]=v[1];v[2]<=4;v[2]++)
  for(v[3]=v[2];v[3]<=4;v[3]++)for(v[0]=0;v[0]<=4;v[0]++)
   linear_completion(v,v[1]);
 }
}
'''
NONSELFDUAL_MAIN = r'''
int main(){M=4;counts=false;cn2.resize(5);cn4.resize(5);V v{};
 for(I a=0;a<1953125;a++){
  I x=a;for(int j:{2,4,5,6,8,9,10,11,12}){v[j]=x%5;x/=5;}complete2(v);
 }
 v=V{};
 for(I a=0;a<390625;a++){
  I x=a;for(int j=0;j<8;j++){v[j]=x%5;x/=5;}complete4(v);
 }
}
'''


def census_check(directory):
    all_keys = set()
    for kind, main in (("selfdual", SELFDUAL_MAIN), ("nonselfdual", NONSELFDUAL_MAIN)):
        source = GEN / f"enumerate_{kind}.cpp"
        reference = directory / f"reference_{kind}.cpp"
        reference.write_text(source.read_text().split("int main(")[0] + main)
        outputs = []
        for name, src, args in (("optimized", source, ["4"]), ("reference", reference, [])):
            binary = directory / f"{name}_{kind}"
            subprocess.run(["g++", "-O3", "-std=c++17", "-fopenmp", "-I", str(GEN),
                            str(src), "-o", str(binary)], check=True)
            result = subprocess.run([str(binary), *args], capture_output=True, text=True, check=True)
            lines = result.stdout.splitlines()
            require(len(lines) == len(set(lines)), "duplicate parameter records")
            outputs.append(set(lines))
        require(outputs[0] == outputs[1], "optimized and unpruned censuses differ")
        for line in outputs[0]:
            R = tensor(5, line, GEN)
            validate(R)
            key = canonical(R)
            require(key not in all_keys, "based-isomorphic duplicate")
            all_keys.add(key)
        print(f"{kind}: optimized and unpruned censuses agree on {len(outputs[0])} rings.")
    require(len(all_keys) == 269, "unexpected independent census size")


def pieri_check():
    weights = [(a, b) for a in range(5) for b in range(5-a)]
    F = s.zeros(len(weights))
    for i, (a, b) in enumerate(weights):
        for w in ((a+1, b), (a-1, b+1), (a, b-1)):
            if w in weights:
                F[i, weights.index(w)] += 1
    G, I = F.T, s.eye(len(weights))
    A = F*G-I
    B, C = F**3-2*F*G+I, G**3-2*F*G+I
    E = A**2-B-C-2*A-I
    indices = [weights.index(w) for w in ((0, 0), (3, 0), (0, 3), (2, 2), (1, 1))]
    R = [[[int(x) for x in row] for row in M.extract(indices, indices).tolist()]
         for M in (I, B, C, E, A)]
    validate(R)
    model = next(m["tensor"] for m in build_model_registry() if m["name"] == "PSU(3)_4")
    require(canonical(R) == canonical(model), "SU(3)_4 Pieri construction differs from registry")
    print("The Ad(SU(3)_4) model agrees with its independent Pieri construction.")


def main():
    for tag, kind, free in (("S", 0, list(range(10, 20))), ("N2", 2, [0, 1, 3, 7]), ("N4", 4, [8, 9])):
        symbolic_check(tag, kind, free)
    with tempfile.TemporaryDirectory() as directory:
        census_check(Path(directory))
    pieri_check()


if __name__ == "__main__":
    main()
