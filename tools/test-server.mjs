import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
export async function startServer(root,port,{wrangler=false,editor=false,rootFile=null}={}){
 const args=wrangler?['node_modules/wrangler/bin/wrangler.js','pages','dev',root,'--ip','127.0.0.1','--port',String(port),'--compatibility-date','2025-09-01']:['tools/preview.py','--root',root,'--port',String(port),...(editor?['--editor']:[]),...(rootFile?['--root-file',rootFile]:[])];
 const child=spawn(wrangler?process.execPath:'python3',args,{cwd:process.cwd(),detached:true,env:{...process.env,WRANGLER_SEND_METRICS:'false',NODE_OPTIONS:'--require '+path.resolve('tools/wrangler-local.cjs')},stdio:['ignore','pipe','pipe']});
 let logs='';child.stdout.on('data',d=>logs+=d);child.stderr.on('data',d=>logs+=d);
 const stop=()=>{try{process.kill(-child.pid,'SIGTERM')}catch{};child.unref()};
 const url='http://127.0.0.1:'+port;
 for(let i=0;i<200;i++){try{const r=await fetch(url+(editor?'/__editor':'/'));if(r.ok)return {url,stop,logs:()=>logs}}catch{};if(child.exitCode!==null){stop();throw new Error(logs)}await new Promise(r=>setTimeout(r,100))};stop();throw new Error('Preview did not start: '+logs);
}
export function save(file,data){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,JSON.stringify(data,null,2)+'\n')}
