import {chromium} from 'playwright';

import http from 'node:http';import fs from 'node:fs';import path from 'node:path';
const root=path.resolve(process.argv[2] || '.'),out=path.join(root,'baselines/live-v100.2.5F/verification');
const types={'.html':'text/html','.css':'text/css','.js':'application/javascript','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname);let f=path.join(root,p);if(p==='/')f=path.join(root,'index.html');if(!fs.existsSync(f)&&fs.existsSync(f+'.html'))f+='.html';if(!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);res.end();return}res.setHeader('Content-Type',types[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f))});
await new Promise(r=>server.listen(8792,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{}),args:['--no-sandbox','--disable-dev-shm-usage']});const results=[];const page=await browser.newPage();
for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
 await page.setViewportSize(viewport);
 for(const route of ['index','services','rotax-engine-systems-support','e-props-dealer-support','contact','support-request']){
 const errors=[],failed=[];page.removeAllListeners('pageerror');page.removeAllListeners('response');page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith('http://127.0.0.1')&&r.status()>=400)failed.push({url:r.url(),status:r.status()})});
 await page.goto('http://127.0.0.1:8792/'+route+'.html',{waitUntil:'networkidle'});
 const details=await page.evaluate(()=>({title:document.title,h1:document.querySelector('h1')?.textContent,brokenImages:[...document.images].filter(i=>i.getAttribute('loading')!=='lazy'&&(!i.complete||!i.naturalWidth)).map(i=>i.src),bodyWidth:document.body.scrollWidth,viewportWidth:innerWidth}));
 await page.screenshot({path:path.join(out,route+'-'+viewport.width+'.png'),fullPage:true});results.push({route,viewport,...details,errors,failed});
 }
}
fs.writeFileSync(path.join(out,'render-results.json'),JSON.stringify({browser:browser.version(),environment:'Local static HTTP server, Chromium desktop and mobile viewport emulation; hosting redirects, external services and form delivery not validated',results},null,2)+'\n');await browser.close();server.close();console.log(JSON.stringify(results.map(r=>({route:r.route,width:r.viewport.width,errors:r.errors,failed:r.failed,brokenImages:r.brokenImages,overflow:r.bodyWidth>r.viewportWidth})),null,2));
