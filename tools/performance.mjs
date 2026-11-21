import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import lighthouse from 'lighthouse';
import desktopConfig from 'lighthouse/core/config/desktop-config.js';
import * as chromeLauncher from 'chrome-launcher';
import {chromium} from 'playwright';
import {startServer, save} from './test-server.mjs';

const args = process.argv.slice(2);
const only = args.includes('--after-only');
const root = args.find(a => !a.startsWith('--')) || 'dist';
const nestedBaseline = 'cache-baseline/LCA_WEBSITE_v101_1_5I_DEPLOYABLE 2';
const routes = ['/', '/services', '/e-props-dealer-support', '/rotax-engine-systems-support',
  '/rotax-gearbox-propeller-vibration', '/rotax-installation-review', '/light-sport-prebuy-evaluation',
  '/support-request', '/our-work'];
const selected = process.env.LCA_PERF_ROUTES?.split(',') || routes;
if (selected.some(route => !routes.includes(route)) || new Set(selected).size !== selected.length) {
  throw Error('Unknown or duplicate performance route: ' + selected.join(','));
}
if (!only && !fs.existsSync('cache-baseline/index.html') && !fs.existsSync(nestedBaseline + '/index.html')) {
  execFileSync('python3', ['-c', "import zipfile; zipfile.ZipFile('reference/baseline-v101.1.5I.zip').extractall('cache-baseline')"]);
}
const before = only ? null : await startServer(fs.existsSync('cache-baseline/index.html') ? 'cache-baseline' : nestedBaseline, 8787);
const after = await startServer(root, 8793, {wrangler:only});
const results = [];
const dir = '.build-evidence/lighthouse';
fs.mkdirSync(dir, {recursive:true});

async function measure(release, url, route, device) {
  const chrome = await chromeLauncher.launch({
    chromePath: process.env.LCA_CHROMIUM_EXECUTABLE || chromium.executablePath(),
    chromeFlags: ['--headless','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--disable-background-networking'],
    logLevel: 'silent'
  });
  try {
    const flags = {port:chrome.port, output:'json', logLevel:'error', throttlingMethod:'simulate',
      onlyCategories:['performance','accessibility','best-practices','seo']};
    if (device === 'mobile') flags.screenEmulation = {mobile:true,width:412,height:823,deviceScaleFactor:1.75,disabled:false};
    const {lhr} = await lighthouse(url + route, flags, device === 'desktop' ? desktopConfig : undefined);
    const stem = route.slice(1) || 'home';
    save(dir + '/' + [release,stem,device].join('-') + '.json', lhr);
    if (lhr.runtimeError) throw Error(lhr.runtimeError.message);
    const score = id => Math.round(lhr.categories[id].score * 100);
    const metric = id => lhr.audits[id].numericValue;
    const row = {release,route,device,lighthouse_version:lhr.lighthouseVersion,chromium:lhr.environment.hostUserAgent,
      performance:score('performance'),accessibility:score('accessibility'),best_practices:score('best-practices'),seo:score('seo'),
      lcp_ms:metric('largest-contentful-paint'),cls:metric('cumulative-layout-shift'),
      tbt_ms:metric('total-blocking-time'),transfer_bytes:metric('total-byte-weight')};
    results.push(row);
    console.log(JSON.stringify(row));
  } finally {
    await chrome.kill();
  }
}

try {
  const servers = before ? [['before',before],['after',after]] : [['artifact',after]];
  for (const [release, server] of servers) {
    for (const route of routes.filter(route => selected.includes(route))) {
      for (const device of ['mobile','desktop']) await measure(release,server.url,route,device);
    }
  }
} finally {
  before?.stop();
  after.stop();
  const name = process.env.LCA_PERF_ROUTES ? 'affected-performance' : only ? 'artifact-performance' : 'performance';
  save('evidence/redesign/' + name + '.json', {method:'Cold local lab navigation per route and device. Simulated Lighthouse mobile and desktop profiles. Decimal bytes.',root,runs:results});
}
const expected = selected.length * 2 * (before ? 2 : 1);
if (results.length !== expected) throw Error(`Expected ${expected} Lighthouse measurements, got ${results.length}`);
const missed = results.filter(r => r.device === 'mobile' && (r.performance < 95 || r.accessibility < 98 || r.seo < 100 ||
  (['/','/e-props-dealer-support'].includes(r.route) && r.lcp_ms > 1800) || r.cls > 0.05 || r.tbt_ms > 100 ||
  (r.route === '/' && r.transfer_bytes > 350000)));
if (only && missed.length) process.exitCode = 1;
