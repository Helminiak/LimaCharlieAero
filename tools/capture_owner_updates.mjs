import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import {prepareCapture} from './prepare_capture.mjs';
import {startServer, save} from './test-server.mjs';

const reviewFixes = process.argv.includes('--review-fixes');
const routes = reviewFixes ? ['/','/our-work'] : ['/','/our-work','/e-props-dealer-support','/services','/owner-notices','/rotax-turbocharger-notice',
 '/rotax-915-tbo-extension','/rotax-gearbox-notice','/support-request?topic=notice','/about-credentials'];
const root = process.argv[2] || 'dist';
assert(['dist','dist-preview'].includes(root));
const out = path.join('evidence/redesign/owner-updates-3',reviewFixes?'review-fixes':'',root==='dist'?'public':'preview');
fs.mkdirSync(out,{recursive:true});
const server = await startServer(root,root==='dist'?18081:18082);
let browser;
const rows=[];
try {
 browser=await chromium.launch({executablePath:process.env.LCA_CHROMIUM_EXECUTABLE});
 const context=await browser.newContext({reducedMotion:'reduce'});
 await context.route('**/*', req=>new URL(req.request().url()).origin===server.url?req.continue():req.abort());
 const page=await context.newPage();
 for(const route of routes){
  for(const width of reviewFixes ? [390,1440] : [320,375,390,768,1024,1440]){
   await page.setViewportSize({width,height:width<768?844:900});
   await page.goto(server.url+route);
   await prepareCapture(page);
   const metrics=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth-innerWidth,height:document.documentElement.scrollHeight}));
   const row={route,width,...metrics};
   rows.push(row);
   assert.equal(metrics.overflow,0, JSON.stringify(row));
   if(route==='/'){
    assert.equal(await page.locator('.trust').getByRole('link',{name:'ROTAX iRMT listing (opens rotaxirmt.com)',exact:true}).count(),1);
    const link=await page.locator('.trust a').boundingBox();
    assert(link.height>=44 && link.width>=44);
   }
   if(route.includes('?'))assert.equal(await page.locator('#support-topic').inputValue(),'notice');
   if(width===390 || width===1440){
    const scan=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']).analyze();
    row.violations=scan.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}));
    assert.equal(row.violations.length,0,JSON.stringify(row));
   }
   const slug=route.slice(1).split('?')[0] || 'home';
   await page.screenshot({path:path.join(out,slug+'-'+width+'.jpg'),fullPage:true,type:'jpeg',quality:72});
  }
 }
} finally {
 try {await browser?.close();} finally {server.stop();save(path.join(out,'measurements.json'),rows);}
}
const desktopWork = rows.find(row=>row.route==='/our-work' && row.width===1440);
assert(desktopWork.height<=8000,`Desktop Our Work exceeds 8,000 px: ${desktopWork.height}`);
console.log(root,rows.length,'captures');
