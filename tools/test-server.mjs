import {spawn} from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';

async function requireFreePort(port) {
  const probe = net.createServer();
  await new Promise((resolve, reject) => {
    probe.once('error', reject);
    probe.listen(port, '127.0.0.1', () => probe.close(resolve));
  });
}

export async function startServer(root, port, {wrangler=false, editor=false, rootFile=null}={}) {
  await requireFreePort(port);
  if (wrangler) await requireFreePort(port + 1000);
  const args = wrangler
    ? ['node_modules/wrangler/bin/wrangler.js','pages','dev',root,'--ip','127.0.0.1',
       '--port',String(port),'--inspector-port',String(port+1000),'--compatibility-date','2025-09-01']
    : ['tools/preview.py','--root',root,'--port',String(port),...(editor?['--editor']:[]),
       ...(rootFile?['--root-file',rootFile]:[])];
  const env = {...process.env, CLOUDFLARE_CF_FETCH_ENABLED:'false', WRANGLER_SEND_METRICS:'false',
    // Wrangler's bundled registry-url uses rc('npm'), independently of telemetry.
    npm_registry:'http://127.0.0.1:1/', npm_config_registry:'http://127.0.0.1:1/',
    NODE_OPTIONS:'--require '+path.resolve('tools/wrangler-local.cjs')};
  const child = spawn(wrangler ? process.execPath : 'python3', args, {
    cwd:process.cwd(), detached:true, env, stdio:['ignore','pipe','pipe']
  });
  let logs = '';
  child.stdout.on('data', data => logs += data);
  child.stderr.on('data', data => logs += data);
  const interrupt = () => process.exit(130);
  const terminate = () => process.exit(143);
  function stop() {
    process.off('exit', stop);
    process.off('SIGINT', interrupt);
    process.off('SIGTERM', terminate);
    try { process.kill(-child.pid, 'SIGTERM'); }
    catch (error) { if (error.code !== 'ESRCH') throw error; }
  }
  process.once('exit', stop);
  process.once('SIGINT', interrupt);
  process.once('SIGTERM', terminate);
  const url = 'http://127.0.0.1:' + port;
  try {
    for (let i=0; i<200; i++) {
      if (child.exitCode !== null || child.signalCode !== null) throw Error(logs);
      try {
        const response = await fetch(url+(editor?'/__editor':'/'), {signal:AbortSignal.timeout(1000)});
        if (response.ok) return {url, stop, logs:()=>logs};
      } catch {}
      await new Promise(resolve => setTimeout(resolve,100));
    }
    throw Error('Preview did not start: '+logs);
  } catch (error) {
    stop();
    throw error;
  }
}

export function save(file,data) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  fs.writeFileSync(file,JSON.stringify(data,null,2)+'\n');
}
