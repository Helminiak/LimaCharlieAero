import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {chromium} from 'playwright';
import {startServer,save} from './test-server.mjs';

const root='dist-preview';
const server=await startServer(root,8791,{wrangler:true});
const browser=await chromium.launch({headless:true});
const dir=process.env.LCA_CAPTURE_DIR || 'evidence/redesign/candidate';
fs.mkdirSync(dir,{recursive:true});
const routes=JSON.parse(fs.readFileSync('.build-evidence/'+root+'/routes.json'));
const widths=(process.env.LCA_WIDTHS || '320,375,390,768,1024,1440').split(',').map(Number);
const filter=process.env.LCA_CAPTURE_ROUTES?.split(',');
const rows=[];
const encode=`import io,sys
from PIL import Image
image=Image.open(sys.stdin.buffer)
if image.width>960: image=image.resize((960,round(image.height*960/image.width)),Image.Resampling.LANCZOS)
image.save(sys.argv[1],quality=58,method=4)`;
try {
  const page=await browser.newPage({reducedMotion:'reduce'});
  await page.route('**/*',r=>new URL(r.request().url()).origin===server.url?r.continue():r.abort());
  for(const route of routes.filter(r=>!filter||filter.includes(r.route))) {
    for(const width of widths) {
      await page.setViewportSize({width,height:width<768?844:900});
      await page.goto(server.url+route.route);
      const metrics=await page.evaluate(async()=>{
        const visibleImages=[...document.images].filter(i=>i.getClientRects().length);
        visibleImages.forEach(i=>i.loading='eager');
        await Promise.all(visibleImages.map(i=>i.decode()));
        await document.fonts.ready;
        return {height:document.documentElement.scrollHeight,overflow:document.documentElement.scrollWidth-innerWidth,
          requestBottom:document.querySelector('main .button')?.getBoundingClientRect().bottom};
      });
      const name=route.file.replace('.html','')+'-'+width+'.webp';
      const png=await page.screenshot({fullPage:true,timeout:60000});
      const result=spawnSync('python3',['-c',encode,dir+'/'+name],{input:png,encoding:'utf8'});
      if(result.status!==0)throw Error(result.stderr);
      rows.push({route:route.route,width,file:name,...metrics});
    }
    console.log(route.route);
  }
} finally {
  save(dir+'/measurements.json',rows);
  await browser.close();
  server.stop();
}
