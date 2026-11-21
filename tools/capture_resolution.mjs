import fs from 'node:fs';
import AxeBuilder from '@axe-core/playwright';
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
const corrections2 = process.argv.includes('--corrections-2');
const targets = corrections2 ? {
 'rotax-gearbox-notice': 'main .lead', 'rotax-turbocharger-notice': '.source-note',
 'owner-notices': '.cards', 'updates': '.cards'
} : common;
const root = process.argv[2];
if (!['dist','dist-preview'].includes(root)) throw Error('Choose dist or dist-preview');
const out = path.join('evidence','redesign',corrections2?'corrections-2':'corrections',root==='dist'?'public':'preview');
fs.mkdirSync(out,{recursive:true});
const rows=[];
const server=await startServer(root,root==='dist'?18081:18082);
let browser;
try {
 browser=await chromium.launch({executablePath:process.env.LCA_CHROMIUM_EXECUTABLE});
 const context=await browser.newContext({reducedMotion:'reduce'});
 const page=await context.newPage();
 await page.route('**/*', req=>new URL(req.request().url()).origin===server.url?req.continue():req.abort());
 for(const [slug,selector] of Object.entries(targets)){
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
   const row = {slug,width,...metrics};
   if (corrections2 && width === 390) {
    const scan = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']).analyze();
    row.violations = scan.violations.map(v => v.id);
    if (row.violations.length) throw Error(JSON.stringify(row));
   }
   rows.push(row);
  }
 }
} finally {
 await browser?.close();
 await server.stop();
 save(path.join(out,'measurements.json'),rows);
}
console.log(root,rows.length,'rendered and captured');
