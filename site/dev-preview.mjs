// Dependency-free local preview. Deployment serves only dist/.
import {createServer} from "node:http";
import {readFile, stat} from "node:fs/promises";
import {resolve, extname, sep} from "node:path";
const directory=resolve(import.meta.dirname,"dist");
const mime={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"application/javascript; charset=utf-8",".json":"application/json; charset=utf-8",".csv":"text/csv; charset=utf-8",".pdf":"application/pdf",".svg":"image/svg+xml"};
const port=Number(process.env.PORT||4173);
createServer(async (request,response)=>{
  try {
    const pathname=decodeURIComponent(new URL(request.url,"http://localhost").pathname);
    const filename=resolve(directory,`.${pathname === "/" ? "/index.html":pathname}`);
    if (filename!==directory && !filename.startsWith(directory+sep)) throw new Error("Invalid path");
    const info=await stat(filename);
    if (!info.isFile()) throw new Error("Not a file");
    const body=await readFile(filename);
    response.writeHead(200,{"content-type":mime[extname(filename)]||"application/octet-stream","cache-control":"no-cache"});
    response.end(request.method==="HEAD"?undefined:body);
  } catch {
    response.writeHead(404,{"content-type":"text/plain"});response.end("Not found");
  }
}).listen(port,"0.0.0.0");
