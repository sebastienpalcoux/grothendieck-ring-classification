from pathlib import Path
import itertools,json,sys,time,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025'
OLD=ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/family_integral'
ROUND3=ROOT/'prior_round/round3/d48'
sys.path.insert(0,str(BASE));sys.path.insert(0,str(OLD))
import group_models as gm
import common
DATA=json.loads((BASE/'tensors.json').read_text())
IDS=json.loads((ROUND3/'results.json').read_text())['remaining_unresolved']
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
