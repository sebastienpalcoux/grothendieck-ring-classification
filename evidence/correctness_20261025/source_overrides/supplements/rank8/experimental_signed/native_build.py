"""Source/compiler-bound native cache; historical receipts are never rewritten."""
from pathlib import Path
from functools import lru_cache
import fcntl,hashlib,json,os,shutil,subprocess,tempfile


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=8)
def _compiler(path,mtime,size):
    return subprocess.check_output([path,'--version'],text=True)


def ensure_native(source,executable,flags=('-O3','-std=c++17')):
    """Return a binary bound to these source bytes, compiler and flags.

    Callers keep all mathematical input/domain guards. A lock and atomic
    replacement coordinate concurrent workers; a damaged/missing binary or
    receipt always triggers a fresh build rather than trusted cache reuse.
    """
    source=Path(source).resolve();executable=Path(executable).resolve()
    compiler=shutil.which('g++')
    if compiler is None:raise RuntimeError('A C++17 g++ compiler is required')
    compiler=str(Path(compiler).resolve());st=Path(compiler).stat()
    build={'schema':'native-source-cache/v1','source_sha256':_sha(source),
           'compiler':compiler,'compiler_version':_compiler(compiler,st.st_mtime_ns,st.st_size),
           'compiler_sha256':_sha(compiler),'flags':list(flags)}
    key=hashlib.sha256(json.dumps(build,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    receipt=executable.with_name(executable.name+'.build.json')
    lock=executable.with_name(executable.name+'.build.lock')
    executable.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        try:
            saved=json.loads(receipt.read_text())
            valid=(saved.get('key')==key and saved.get('build')==build
                   and executable.is_file() and os.access(executable,os.X_OK)
                   and saved.get('binary_sha256')==_sha(executable))
        except (OSError,ValueError):valid=False
        if valid:return executable
        fd,name=tempfile.mkstemp(prefix=executable.name+'.',dir=executable.parent);os.close(fd)
        temporary=Path(name)
        try:
            subprocess.run([compiler,*flags,str(source),'-o',str(temporary)],check=True,capture_output=True)
            # Refuse a source change concurrent with compilation.
            if _sha(source)!=build['source_sha256']:raise RuntimeError('Native source changed during build')
            os.replace(temporary,executable)
            payload={'key':key,'build':build,'binary_sha256':_sha(executable)}
            fd,name=tempfile.mkstemp(prefix=receipt.name+'.',dir=receipt.parent)
            with os.fdopen(fd,'w') as out:out.write(json.dumps(payload,indent=2)+'\n')
            os.replace(name,receipt)
        finally:
            temporary.unlink(missing_ok=True)
    return executable
