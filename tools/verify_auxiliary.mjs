import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import {startServer,save} from './test-server.mjs';
const server=await startServer(process.argv[2]||'verification-root',8794,{wrangler:true});
const browser=await chromium.launch({executablePath:process.env.LCA_CHROMIUM_EXECUTABLE,headless:true,args:['--no-sandbox']});
const result={status:'PASS',root:process.argv[2]||'verification-root',checks:[],limits:['Local event dispatch only; no external analytics collection or inbox delivery tested']};
try {
 const context=await browser.newContext({viewport:{width:390,height:844}}),page=await context.newPage();
 await page.addInitScript(()=>{window.lcaEvents=[];document.addEventListener('lca:measurement',e=>window.lcaEvents.push(e.detail));document.addEventListener('click',e=>{const a=e.target.closest('a');if(a&&/^(tel|sms):/.test(a.getAttribute('href')))e.preventDefault()},true)});
 let syntheticRequests=0;await page.route('https://formspree.io/**',route=>{syntheticRequests++;return route.fulfill({status:200,contentType:'application/json',body:'{"ok":true}'})});
 await page.goto(server.url+'/support-request?topic=prebuy');
 await page.locator('a[href^="tel:"]').first().click();await page.locator('a[href^="sms:"]').first().click();
 await page.locator('[name="name"]').fill('Synthetic LOCAL test');
 await page.locator('[name="email"]').fill('synthetic@example.invalid');
 await page.locator('[name="message"]').fill('Synthetic local event check, no real submission.');
 await page.locator('button[type="submit"]').click();await page.locator('#form-status.success').waitFor();
 const events=await page.evaluate(()=>window.lcaEvents);
 for(const name of ['contact_call_click','contact_text_click','form_start','form_accepted'])if(!events.some(e=>e.event===name))throw new Error('Missing '+name);
 if(events.some(e=>Object.keys(e).some(k=>!['event','topic'].includes(k))))throw new Error('Private event property');
 result.checks.push({test:'Call/Text clicks, form start and locally mocked provider acceptance emit only event/topic',status:'PASS',kind:'LOCAL MOCK',events});
 for(const digits of ['1234','1234567890123456']){await page.goto(server.url+'/support-request');await page.locator('[name="preferred_contact"]').selectOption('phone');await page.locator('[name="name"]').fill('Synthetic LOCAL test');await page.locator('[name="best_contact"]').fill(digits);await page.locator('[name="message"]').fill('Synthetic invalid-phone check.');await page.locator('button[type="submit"]').click();if(await page.locator('#support-phone').getAttribute('aria-invalid')!=='true'||syntheticRequests!==1)throw new Error('Invalid phone submitted');}
 result.checks.push({test:'Selected phone method rejects four-digit and sixteen-digit phone numbers without a provider request',status:'PASS',kind:'LOCAL MOCK'});
 await page.locator('#support-message').scrollIntoViewIfNeeded();await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 result.message_style=await page.locator('#support-message').evaluate(el=>({foreground:getComputedStyle(el).color,background:getComputedStyle(el).backgroundColor,placeholder:getComputedStyle(el,'::placeholder').color,placeholder_opacity:getComputedStyle(el,'::placeholder').opacity}));
 const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
 result.axe_incomplete_followup=axe.incomplete.map(r=>({id:r.id,nodes:r.nodes.map(n=>({target:n.target,html:n.html,summary:n.failureSummary}))}));
 // Confirm the actual native select colors, not a hidden offscreen honeypot.
 result.native_select_style=await page.locator('[name="need_type"]').evaluate(el=>({color:getComputedStyle(el).color,background:getComputedStyle(el).backgroundColor}));
 await context.close();
 const fallback=await browser.newContext({viewport:{width:390,height:844}}),p=await fallback.newPage();
 await p.route('**/assets/site.*.js',r=>r.abort());
 await p.goto(server.url+'/');await p.locator('.nav-toggle').click();
 if(!await p.locator('.nav a[href="/support-request"]').isVisible())throw new Error('Independent navigation failed');
 await p.goto(server.url+'/support-request');if(!await p.locator('#aircraft-intake-form').isVisible())throw new Error('Native form missing');
 result.checks.push({test:'Independent menu and native form remain usable when the external enhancement script fails',status:'PASS',limit:'Native provider POST not sent'});
 await p.goto(server.url+'/e-props-dealer-support#eprops-benchmark');
 const at=await p.locator('#eprops-benchmark').evaluate(el=>({top:el.getBoundingClientRect().top,pageTop:el.getBoundingClientRect().top+scrollY}));
 if(at.pageTop>1000)throw new Error('Legacy fragment sent to page footer');
 result.checks.push({test:'Legacy benchmark fragment lands at retained page introduction rather than obsolete footer alias',status:'PASS',position:at});
 await fallback.close();
} catch(e){result.status='FAIL';result.error=String(e);process.exitCode=1}finally{await browser.close();server.stop();save('evidence/auxiliary-checks.json',result);console.log(JSON.stringify(result))}
