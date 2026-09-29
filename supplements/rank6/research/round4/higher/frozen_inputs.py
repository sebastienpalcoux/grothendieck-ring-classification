"""Ten inherited unresolved inputs plus the54 inherited realized controls."""
import json

def rows(root):
 frontier=set(json.loads((root/'verification/round4/campaign_manifest.json').read_text())['ids'])
 models={r['id']:r for r in json.loads((root/'data/model_catalog.json').read_text())}
 if len(frontier)!=10 or len(models)!=54 or frontier&set(models):raise ValueError('wrong frozen fourth-continuation inputs')
 census=json.loads((root/'data/census.json').read_text());wanted=frontier|set(models)
 out=[{'id':r['id'],'status':'unresolved'if r['id']in frontier else models[r['id']]['status']}for r in census if r['id']in wanted]
 if len(out)!=64:raise ValueError('missing frozen input tensor')
 return out
