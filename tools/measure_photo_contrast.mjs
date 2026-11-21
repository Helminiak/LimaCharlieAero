import {prepareCapture} from './prepare_capture.mjs';
import {chromium} from 'playwright';
import {startServer, save} from './test-server.mjs';

const server = await startServer('dist-preview',8795);
const browser = await chromium.launch();
const rows = [];
try {
  const page = await browser.newPage({deviceScaleFactor:1});
  for (const width of [320,375,390,768,1024,1440]) {
    await page.setViewportSize({width,height:width < 768 ? 844 : 900});
    await page.goto(server.url);
    await prepareCapture(page);
    const selector = '.hero-copy p,.hero-copy h1,.hero-copy a,.tile h3,.tile p';
    const boxes = await page.locator(selector).evaluateAll(elements => {
      const results = [];
      for (const el of elements) {
        const walker = document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
          const node = walker.currentNode;
          const range = new Range();
          range.selectNodeContents(node);
          const style = getComputedStyle(node.parentElement);
          // Include the entire tile heading's content box, including its line ends.
          const rects = el.matches('.tile h3') ? el.getClientRects() : range.getClientRects();
          const boxes = [...rects].filter(r => r.width && r.height).map(r =>
            [Math.floor(r.left),Math.floor(r.top),Math.ceil(r.right),Math.ceil(r.bottom)]);
          if (boxes.length) results.push({label:node.textContent.trim(),group:el.closest('.tile') ? 'tile' : 'hero',
            foreground:style.color,boxes});
        }
      }
      return results;
    });
    // Glyph paint only. Preserve backgrounds, layout, scrims, borders and foreground-derived colors.
    const screenshot = await page.screenshot({fullPage:true,style:'.hero-copy *, .tile * { -webkit-text-fill-color: transparent; }'});
    const samples = await page.evaluate(async ({boxes,png}) => {
      const image = new Image();
      image.src = 'data:image/png;base64,' + png;
      await image.decode();
      const canvas = document.createElement('canvas');
      canvas.width = image.width;
      canvas.height = image.height;
      const ctx = canvas.getContext('2d',{willReadFrequently:true});
      ctx.drawImage(image,0,0);
      const linear = Array.from({length:256},(_,v) => v <= 10 ? v/3294.6 : ((v/255+.055)/1.055)**2.4);
      const lum = (r,g,b) => .2126*linear[r] + .7152*linear[g] + .0722*linear[b];
      return boxes.map(({boxes,...entry}) => {
        const foreground = lum(...entry.foreground.match(/\d+/g).map(Number));
        const contrast = bg => (Math.max(foreground,bg)+.05)/(Math.min(foreground,bg)+.05);
        const luminances = [];
        let worst = Infinity;
        for (const [x,y,right,bottom] of boxes) {
          const data = ctx.getImageData(x,y,right-x,bottom-y).data;
          for (let i=0;i<data.length;i+=4) {
            const light = lum(data[i],data[i+1],data[i+2]);
            luminances.push(light);
            worst = Math.min(worst,contrast(light));
          }
        }
        luminances.sort((a,b) => b-a);
        const decile = luminances.slice(0,Math.ceil(luminances.length/10));
        return {...entry,pixels:luminances.length,worst,lightest_decile:contrast(decile.reduce((a,b) => a+b)/decile.length)};
      });
    },{boxes,png:screenshot.toString('base64')});
    rows.push({width,samples});
    console.log(width,...['hero','tile'].map(group => Math.min(...samples.filter(s => s.group===group).map(s=>s.worst))));
  }
  save('evidence/redesign/photo-contrast.json',rows);
} finally {
  await browser.close();
  server.stop();
}
