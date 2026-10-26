// Real-browser checks for the complete census under the GitHub project prefix.
// Requires Playwright and a local Chromium/Chrome (BROWSER_EXECUTABLE override).
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const args = process.argv.slice(2), at = args.indexOf('--output-dir');
if (at < 0 || !args[at+1]) throw Error('Use --output-dir NEW_DIRECTORY');
const out = path.resolve(args[at+1]);
if (fs.existsSync(out)) throw Error('Choose a new output directory');
fs.mkdirSync(out, {recursive: true});
const dist = path.resolve(__dirname, 'dist'), prefix = '/grothendieck-ring-classification';
const manifest = JSON.parse(fs.readFileSync(path.join(dist, 'data/full-census/manifest.json')));
const band = manifest.bands.find(b => b.rank === 4 && b.multiplicity === 128);
const mime = {'.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.bin': 'application/octet-stream', '.txt': 'text/plain'};
const server = http.createServer((req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (!url.pathname.startsWith(prefix + '/')) throw Error('Prefix');
    const file = path.resolve(dist, '.' + decodeURIComponent(url.pathname.slice(prefix.length)));
    if (!file.startsWith(dist + path.sep)) throw Error('Path');
    const raw = fs.readFileSync(file);
    res.writeHead(200, {'content-type': mime[path.extname(file)] || 'application/octet-stream'});res.end(raw);
  } catch {res.writeHead(404);res.end('Not found');}
});
const report = {layout: [], interactions: [], requests: []};
let browser;
async function ready(page) {
  await page.waitForFunction(() => document.querySelector('#record-count')?.textContent.includes('matching') || document.querySelector('#case-title')?.textContent.match(/^([CR]\d+_\d+_\d+|F_\{\d+,\d+\})$/));
}
async function noOverflow(page, width, route) {
  const value = await page.evaluate(() => ({width: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth}));
  assert(value.document <= width+1 && value.body <= width+1, JSON.stringify({route, width, ...value}));
  report.layout.push({route, width, ...value, passed: true});
}
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = 'http://127.0.0.1:' + server.address().port + prefix;
  browser = await chromium.launch({headless: true, ...(process.env.BROWSER_EXECUTABLE ? {executablePath: process.env.BROWSER_EXECUTABLE} : {}), args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']});
  for (const width of [320, 390, 430, 768, 1440]) {
    const context = await browser.newContext({viewport: {width, height: 900}, deviceScaleFactor: 1, isMobile: width < 500, hasTouch: width < 500, acceptDownloads: true, reducedMotion: 'reduce'});
    const page = await context.newPage(), errors = [], requests = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('response', r => {if (r.url().startsWith(base)) requests.push(r.url().slice(base.length));});
    for (const route of ['/records.html', '/case.html?id=C3_1000_1', '/case.html?id=R12_1_623', '/case.html?id=F_%7B1%2C10%7D']) {
      await page.goto(base+route, {waitUntil: 'networkidle'});await ready(page);
      await noOverflow(page, width, route);
      assert(!requests.some(p => /^\/data\/(rank9_m2|rank12_m1|realized_rings|resolved_cases|unresolved_cases)\.json/.test(p)), 'Single-record views must not request full legacy tensor catalogues');
      if (route === '/records.html') {
        assert.match(await page.locator('#record-count').innerText(), /^1,434,042 matching census rings/);
        assert.equal(await page.locator('.census-card').count(), 24);
        assert(!requests.some(p => /\/rank\d+\/\d+\.bin/.test(p)), 'Directory must not request tensors');
        if ([390, 1440].includes(width)) await page.screenshot({path: path.join(out, `census-${width}.png`), fullPage: false});
      }
      if (route.includes('R12_1_623')) {
        assert.match(await page.locator('#case-detail').innerText(), /[Uu]nitarity remains unproved/);
        assert.match(await page.locator('.census-profile-note').innerText(), /C12_1_/);
      }
    }
    if (width === 390) {
      await page.goto(base+'/records.html', {waitUntil: 'networkidle'});await ready(page);
      const first = await page.locator('.census-card-title a').first().innerText();
      await page.locator('#record-next').click();
      await page.waitForFunction(value => document.querySelector('.census-card-title a').textContent !== value, first);
      assert.equal(await page.locator('#record-page').inputValue(), '2');
      const second = await page.locator('.census-card-title a').first().innerText();
      await page.reload({waitUntil: 'networkidle'});await ready(page);
      assert.equal(await page.locator('.census-card-title a').first().innerText(), second);
      await page.locator('#record-previous').click();
      await page.waitForFunction(value => document.querySelector('.census-card-title a').textContent === value, first);
      await page.locator('#record-page').fill(String(Math.ceil(manifest.total/24)));
      await page.locator('#record-page').press('Enter');
      await page.waitForFunction(() => document.querySelector('.census-card-title a')?.textContent.startsWith('C12_'));
      assert.equal(await page.locator('.census-card-title a').last().innerText(), 'C12_1_632');
      report.interactions.push('phone: pagination, reload preservation, first/last page and Enter jump');

      await page.goto(base+'/records.html', {waitUntil: 'networkidle'});await ready(page);
      await page.locator('#record-rank').selectOption('4');
      await page.locator('#record-m').fill('128');
      await page.waitForFunction(n => document.querySelector('#record-count').textContent.startsWith(n.toLocaleString('en-US')+' matching'), band.count);
      await page.locator('.property-panel > summary').click();
      await page.locator('#record-property-integral').selectOption('yes');
      await page.waitForFunction(() => document.querySelector('#record-count').textContent.includes('matching') && !document.querySelector('#record-list').getAttribute('aria-busy').includes('true'));
      await noOverflow(page, width, 'rank4-m128-integral');
      await page.locator('#record-scope').selectOption('profiles');
      await page.waitForFunction(() => document.querySelector('#record-count').textContent.includes('matching detailed profiles'));
      await page.locator('#record-reset').click();await ready(page);
      assert.match(await page.locator('#record-count').innerText(), /^1,434,042/);
      await page.locator('#record-search').fill('C4_128_1');
      await page.waitForFunction(() => document.querySelector('#record-count').textContent.startsWith('1 matching census ring'));
      await page.getByRole('link', {name: 'Open record →', exact: true}).click();await ready(page);
      assert.equal(await page.locator('#case-title').innerText(), 'C4_128_1');
      const pendingDownload = page.waitForEvent('download');
      await page.getByRole('button', {name: 'Download fusion tensor · Python .txt ↓', exact: true}).first().click();
      const download = await pendingDownload;
      assert.equal(download.suggestedFilename(), 'C4_128_1.txt');
      const local = path.join(out, download.suggestedFilename());await download.saveAs(local);
      const tensor = JSON.parse(fs.readFileSync(local, 'utf8'));
      assert.equal(tensor.length, 4);assert.equal(Math.max(...tensor.flat(2)), 128);
      const checksum = crypto.createHash('sha256').update(JSON.stringify(tensor)).digest('hex');
      assert.equal(await page.locator('.case-checksum').innerText(), checksum);
      await page.getByRole('button', {name: 'N3', exact: true}).click();
      assert.equal(await page.getByRole('button', {name: 'N3', exact: true}).getAttribute('aria-pressed'), 'true');
      await page.screenshot({path: path.join(out, 'phone-census-record.png'), fullPage: false});
      report.interactions.push('phone: rank, multiplicity, exact properties, coverage, reset, exact-ID search, tensor download and matrix switching');

      await page.goto(base+'/records.html?rank=3&m=1001', {waitUntil: 'networkidle'});
      await page.waitForFunction(() => document.querySelector('#record-list').textContent.includes('outside the published coverage'));
      assert(!/^0 matching/.test(await page.locator('#record-count').innerText()));
      report.interactions.push('unreleased bands are not displayed as zero census counts');

      await page.route('**/data/full-census/rank4/*.bin*', async route => {
        if (route.request().url().includes('/chunks.bin')) return route.continue();
        await route.fulfill({status: 200, contentType: 'application/octet-stream', body: Buffer.from('corrupt')});
      });
      await page.goto(base+'/case.html?id=C4_128_1', {waitUntil: 'networkidle'});
      await page.waitForFunction(() => document.querySelector('#case-detail').textContent.includes('does not match this snapshot'));
      assert.equal(await page.locator('#fusion-data').count(), 0);
      await page.unroute('**/data/full-census/rank4/*.bin*');
      report.interactions.push('corrupt binary payload produces an error and never a ring record');
    }
    assert.deepEqual(errors, [], 'Uncaught browser errors');
    report.requests.push({width, count: requests.length, no_full_legacy_catalogue: true});
    console.log('Complete census real-browser PASS:', width, 'px');
    await context.close();
  }
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2)+'\n');
  await browser.close();server.close();
})().catch(async error => {console.error(error);if (browser) await browser.close();server.close();process.exitCode=1;});
