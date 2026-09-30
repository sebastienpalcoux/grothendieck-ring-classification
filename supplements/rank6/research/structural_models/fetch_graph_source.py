"""Optional: download the published PDF and reproduce the two graph extractions."""
from pathlib import Path
import hashlib,json,urllib.request,subprocess,sys
root=Path(__file__).resolve().parent
meta=json.loads((root/'r629/graph_extraction.json').read_text())
target=root/'r629/1001.5416.pdf'
if not target.exists():
 with urllib.request.urlopen(meta['source'],timeout=60) as response:target.write_bytes(response.read())
if hashlib.sha256(target.read_bytes()).hexdigest()!=meta['source_sha256']:raise RuntimeError('Source PDF hash differs')
for script in ['quartic/extract_b2_7.py','r629/extract_graph.py']:
 subprocess.run([sys.executable,'-O',str(root/script)],cwd=root,check=True,timeout=120)
