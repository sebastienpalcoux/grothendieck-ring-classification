"""Exhaustive exact cubic and spectral tests on saved integral Gram domains."""
import argparse,itertools,json,math
from fractions import Fraction as F
import verlinde_low as v
c=v.c

def coordinates(x):
    values=list(map(F,c.ec(x)))
    c.require(len(values)<=2,'quadratic field')
    return [F(0)]*(2-len(values))+values

def scale(values):
    den=math.lcm(*(x.denominator for x in values))
    return [int(x*den) for x in values],den

def cubic_rows(R,a,cols,perm):
    rows=[]
    for triple,constant,coefficients in v.linear_coefficients(R,a,cols,perm):
        entries=[coordinates(x) for x in [constant]+coefficients]
        parts=[scale([x[j] for x in entries]) for j in range(2)]
        rows.append({'triple':list(triple),'irrational':parts[0][0],
                     'rational':parts[1][0],'rational_denominator':parts[1][1]})
    return rows

def cubic_values(rows,counts):
    values=[]
    for row in rows:
        irrational=row['irrational'][0]+sum(n*x for n,x in zip(counts,row['irrational'][1:]))
        rational=row['rational'][0]+sum(n*x for n,x in zip(counts,row['rational'][1:]))
        if irrational or rational<0 or rational%row['rational_denominator']:
            return None
        values.append(rational//row['rational_denominator'])
    return values

def spectral_rows(R,a,cols):
    K=a['K'];chs=v.modular.characters(R,a)
    _,high=v.modular.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))
    allcols=[tuple(x) for x in cols]+[(0,)+tuple(x) for x,z in high]
    dims=[sum((K(x)*y for x,y in zip(col,a['ds'])),K.zero) for col in allcols]
    coefficient=int(a['factor'].all_coeffs()[1]);rows=[]
    for E,ch in enumerate(chs):
        eigs=[tuple(coordinates(a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*v.modular.value(ch,col,K)/d)) for col,d in zip(allcols,dims)]
        seen=set()
        for key in eigs:
            if key[0]==0 or key in seen:continue
            conjugate=(-key[0],key[1]-coefficient*key[0]);seen.update((key,conjugate))
            row=[int(x==key)-int(x==conjugate) for x in eigs]
            rows.append({'character':E,'eigenvalue':[str(x) for x in key],
                         'conjugate':[str(x) for x in conjugate],
                         'equation':[sum(row[:5])]+row[5:]})
    return rows

def compute_1154():
    v.modular.full.base.install()
    source=c.HERE.parent/'central_integrality/integer_gram_1154.json'
    domain=json.loads(source.read_text())
    row=next(r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text()) if r['id']==domain['id'])
    c.require(row['tensor_sha256']==domain['tensor_sha256'],'tensor binding')
    R=row['tensor'];a=c.w.data(R);cols=a['lows'][31]
    c.require([list(x) for x in cols]==domain['low_columns'],'same low domain')
    _,high=v.modular.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))
    c.require([list(x) for x,z in high]==domain['high_columns'],'same high domain')
    permutations=v.modular.assignments(a,v.modular.characters(R,a),cols)
    c.require(permutations==[(0,1,2,3,4)],'unique S assignment')
    cubics=cubic_rows(R,a,cols,permutations[0]);spectral=spectral_rows(R,a,cols)
    cubic_pass=[];spectral_pass=[]
    for i,counts in enumerate(domain['completions']):
        if cubic_values(cubics,counts) is not None:cubic_pass.append(i)
        if all(row['equation'][0]+sum(n*x for n,x in zip(counts,row['equation'][1:]))==0 for row in spectral):spectral_pass.append(i)
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],
            'scope':'pseudo_unitary_only','low_index':31,
            'gram_domain':'../central_integrality/integer_gram_1154.json',
            'gram_pattern_count':len(domain['completions']),
            'cubic_rows':cubics,'spectral_rows':spectral,
            'cubic_survivor_indices':cubic_pass,'spectral_survivor_indices':spectral_pass,
            'combined_survivor_indices':sorted(set(cubic_pass)&set(spectral_pass)),
            'conclusion':'Necessary central fusion constraints; survivors are not constructed centers or categories.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute_1154();path=c.HERE/'central_integral_filters_1154.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:c.require(result==json.loads(path.read_text()),'complete cubic and spectral replay')
    print('PASS R1154:',result['gram_pattern_count'],'complete integral Gram patterns;',
          len(result['cubic_survivor_indices']),'cubic survivors;',
          len(result['spectral_survivor_indices']),'spectral survivors;',
          len(result['combined_survivor_indices']),'combined survivors')

if __name__=='__main__':main()
