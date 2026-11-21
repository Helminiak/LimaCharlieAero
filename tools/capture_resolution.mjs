import fs from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';
import {startServer, save} from './test-server.mjs';
import {prepareCapture} from './prepare_capture.mjs';

const common = {
  'rotax-gearbox-propeller-vibration': '.pair',
  's-lsa-e-lsa-maintenance': '.limits',
  'rotax-gearbox-notice': 'main .lead',
  'rotax-turbocharger-notice': '.source-note',
  'e-props-dealer-support': '.proof-grid:has(.document)',
  'faq': '#question-17',
  'our-work': '.legend',
  'index': '.sand:has(a[href="/our-work"])'
};
const root = process.argv[2];
if (!['dist','dist-preview'].includes(root)) throw Error('Choose dist or dist-preview');
const out = path.join('evidence','redesign','corrections',root==='dist'?'public':'preview');
fs.mkdirSync(out,{recursive:true});
const rows=[];
const server=await startServer(root,root==='dist'?18081:18082);
let browser;
try {
 browser=await chromium.launch({executablePath:process.env.LCA_CHROMIUM_EXECUTABLE});
 const page=await browser.newPage({reducedMotion:'reduce'});
 await page.route('**/*', req=>new URL(req.request().url()).origin===server.url?req.continue():req.abort());
 for(const [slug,selector] of Object.entries(common)){
  for(const width of [320,375,390,768,1024,1440]){
   const name=slug+'-'+width;
   await page.setViewportSize({width,height:width<768?844:900});
   await page.goto(server.url+(slug==='index'?'/':'/'+slug));
   await prepareCapture(page);
   const metrics=await page.evaluate(()=>({height:document.documentElement.scrollHeight,
    overflow:document.documentElement.scrollWidth-innerWidth}));
   if(metrics.overflow || (slug==='our-work' && width===1440 && metrics.height>8000)) throw Error(JSON.stringify({slug,width,...metrics}));
   await page.screenshot({path:path.join(out,name+'-full.jpg'),fullPage:true,type:'jpeg',quality:73});
   const target=page.locator(selector).first();
   await target.evaluate(el=>{for(let n=el;n;n=n.parentElement) if(n.matches('details')) n.open=true;el.scrollIntoView({block:'start'});scrollBy(0,-24)});
   await page.screenshot({path:path.join(out,name+'-focus.jpg'),type:'jpeg',quality:82});
   if(slug==='our-work'||(slug==='index'&&root==='dist-preview')){
    const other=slug==='index'?'.case-panel':'.hero-figure';
    await page.locator(other).first().scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(out,name+'-detail.jpg'),type:'jpeg',quality:82});
   }
   rows.push({slug,width,...metrics});
  }
 }
} finally {
 await browser?.close();
 await server.stop();
 save(path.join(out,'measurements.json'),rows);
}
console.log(root,rows.length,'rendered and captured');
