"""Replay exact arithmetic certificates; no optimizer or network is used."""
import argparse,json,time
from common import HERE,require,stable
from verify_quartic import run as quartic
from verify_7018_quadratic import run as quadratic
p=argparse.ArgumentParser();p.add_argument('--source-root');args=p.parse_args()
start=time.monotonic();stored=json.loads((HERE/'certificates.json').read_text())
actual={'quartic':stable(quartic(args.source_root)),'quadratic_7018':stable(quadratic(args.source_root))}
require(actual==stored,'regenerated certificate differs')
print(json.dumps({'verified':list(actual),'complete':True,'seconds':time.monotonic()-start},indent=2))
