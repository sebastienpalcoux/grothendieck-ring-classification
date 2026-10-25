const fs=require('node:fs'),path=require('node:path');
const {chromium,devices}=require('playwright');
const args=process.argv.slice(2),get=name=>{const i=args.indexOf(name);return i<0?null:args[i+1]};
if(!get('--output-dir')){console.error('Usage: node site/check_responsive.cjs --output-dir NEW_DIRECTORY [--census-root OTHER_REPOSITORY]');process.exit(2)}
const out=path.resolve(get('--output-dir'));if(fs.existsSync(out))throw Error('Choose a new output directory');fs.mkdirSync(out,{recursive:true});
const root=path.join(__dirname,'dist');
const crypto=require('node:crypto');
const sourceHashes=()=>Object.fromEntries(fs.readdirSync(root).filter(n=>/\.(?:html|css|js)$/.test(n)).sort().map(n=>[n,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,n))).digest('hex')]));
const sources=sourceHashes();const interactions=[];
const routes=['/','/records.html','/unresolved.html','/constructions.html','/theory.html','/review.html','/case.html?id=R6_2_143','/case.html?id=R9_2_137'];
const records=[];
async function serve(root){
 const http=require('node:http');const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.pdf':'application/pdf'};
 const server=http.createServer((req,res)=>{try{let f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!f.startsWith(root+path.sep)&&f!==root)throw Error('path');if(fs.statSync(f).isDirectory())f=path.join(f,'index.html');res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(fs.readFileSync(f));}catch{res.writeHead(404);res.end('Not found')}});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));return {server,url:'http://127.0.0.1:'+server.address().port};
}
(async()=>{
 const atlas=await serve(root);const censusSite=get('--census-root')?await serve(path.resolve(get('--census-root'))):null;
 const browser=await chromium.launch({...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],headless:true});
 for(const width of [320,390,430,768,1440]){
  const context=await browser.newContext(width<=430?{...devices['iPhone 13'],viewport:{width,height:844},deviceScaleFactor:1,reducedMotion:'reduce'}:{viewport:{width,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const route of routes){
   await page.goto(atlas.url+route,{waitUntil:'networkidle'});
   const result=await page.evaluate(()=>({inner:innerWidth,viewport:document.documentElement.clientWidth,document:document.documentElement.scrollWidth,body:document.body.scrollWidth,title:document.title,offenders:[...document.querySelectorAll('body *')].filter(e=>{const b=e.getBoundingClientRect(),s=getComputedStyle(e);return b.width>0&&s.display!=='none'&&(b.left< -1||b.right>innerWidth+1)&&!e.closest('.table-scroll,.profile-table-scroll,.case-table-scroll,.theory-table-wrap,.profile-tabs,pre')}).map(e=>({tag:e.tagName,class:e.className,id:e.id,width:Math.round(e.getBoundingClientRect().width)})).slice(0,12)}));
   if(route==='/')await page.locator('.count-cell').first().waitFor();
   if(route.startsWith('/case.html')){const title=await page.locator('#case-title').innerText();if(!title.includes(route.split('=')[1]))throw Error('Case data did not render: '+route)}
   const record={width,route,...result,passed:result.document<=width+1&&result.inner<=width+1};records.push(record);console.log(width,route,record.passed?'PASS':'OVERFLOW',result.document);
   if((width===390&&['/','/records.html','/constructions.html','/case.html?id=R6_2_143'].includes(route))||(width===1440&&route==='/'))await page.screenshot({path:path.join(out,`w${width}-${route==='/'?'home':route.split('?')[0].replaceAll('/','').replace('.html','')}.png`)});
   if(width===390&&route==='/'){
    const button=page.getByRole('button',{name:'Menu',exact:true});await button.click();
    if(await button.getAttribute('aria-expanded')!=='true')throw Error('Mobile menu did not open');
    await page.screenshot({path:path.join(out,'phone-menu.png')});await button.press('Escape');
    if(await button.getAttribute('aria-expanded')!=='false')throw Error('Escape did not close mobile menu');
    interactions.push({check:'phone_menu_open_and_escape',passed:true});
    const region=page.locator('#table-scroll');const scroll=await region.evaluate(e=>{e.scrollLeft=e.scrollWidth;return {left:e.scrollLeft,width:e.scrollWidth,viewport:e.clientWidth}});
    if(scroll.left<=0)throw Error('Count table cannot scroll sideways');
    interactions.push({check:'horizontal_count_table_scroll',passed:true});
    const fits=await page.locator('.count-cell').evaluateAll(all=>all.every(b=>b.scrollWidth<=b.clientWidth+1&&b.scrollHeight<=b.clientHeight+1));if(!fits)throw Error('Count digits wrap or clip');
    await page.locator('#rank-filters button').filter({hasText:/^6$/}).click();
    const single=await region.evaluate(e=>e.scrollWidth<=e.clientWidth+2);if(!single)throw Error('Single-rank table should fit the phone');
    await page.locator('#rank-filters button').filter({hasText:/^ALL$/i}).click();
    interactions.push({check:'counts_fit_and_single_rank_adapts',passed:true});
    await region.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'phone-table.png')});
    await page.getByRole('button',{name:/Fusion rings ALL CENSUSED/i}).click();
    if(await page.locator('#view-fusion').getAttribute('aria-pressed')!=='true')throw Error('Fusion mode did not switch');
    await page.locator('#range-select').selectOption('all');
    await region.evaluate(e=>{e.scrollTop=e.scrollHeight});
    await page.waitForFunction(()=>[...document.querySelectorAll('#count-table tbody tr:not(.virtual-spacer) td:first-child')].some(e=>e.textContent==='1000'));
    const rowHeights=await page.locator('#count-table tbody tr:not(.virtual-spacer)').evaluateAll(rows=>rows.map(r=>r.getBoundingClientRect().height));
    if(!rowHeights.every(h=>Math.abs(h-40)<1))throw Error('Mobile row heights differ from virtual scroll geometry: '+rowHeights.join(','));
    await page.locator('#jump-input').fill('500');
    await page.locator('#jump-input').press('Enter');
    await page.waitForFunction(()=>[...document.querySelectorAll('#count-table tbody tr:not(.virtual-spacer) td:first-child')].some(e=>e.textContent==='500'));
    await page.locator('#jump-input').fill('600');
    await page.locator('#jump-input').press('Tab');
    await page.waitForFunction(()=>[...document.querySelectorAll('#count-table tbody tr:not(.virtual-spacer) td:first-child')].some(e=>e.textContent==='600'));
    interactions.push({check:'virtualized_full_range_and_multiplicity_jump',passed:true});
    await page.locator('#range-select').selectOption('8');
    await page.locator('.count-cell').first().click();
    await page.waitForFunction(()=>document.querySelector('#cell-detail').getBoundingClientRect().top<30);
    await page.locator('.mobile-count-return').click();
    interactions.push({check:'fusion_switch_and_selection_navigation',passed:true});
    await page.locator('.open-ring').first().click();
    const dialog=page.locator('#ring-dialog');await dialog.waitFor({state:'visible'});
    for(const tab of await page.locator('.profile-tabs button').all()){
      await tab.click();const box=await dialog.boundingBox();if(!box||box.x<0||box.x+box.width>width+1)throw Error('Model dialog extends past the phone');
    }
    await page.locator('#close-ring').click();interactions.push({check:'model_dialog_and_all_profile_tabs',passed:true});
    await page.setViewportSize({width:844,height:390});
    if(await button.isVisible()||!(await page.locator('.top-nav').isVisible()))throw Error('Landscape navigation did not adapt');
    if(await page.evaluate(()=>document.documentElement.scrollWidth)>845)throw Error('Landscape overflow');
    await page.setViewportSize({width,height:844});interactions.push({check:'portrait_landscape_resize',passed:true});
   }
  }
  if(errors.length)throw Error('Browser errors: '+errors.join('; '));
  await context.close();
 }
 if(censusSite){
  for(const width of [320,390,768,1440]){const context=await browser.newContext({viewport:{width,height:844},isMobile:width<500,hasTouch:width<500});const page=await context.newPage();await page.goto(censusSite.url+'/docs/',{waitUntil:'networkidle'});const census=await page.evaluate(()=>({document:document.documentElement.scrollWidth,inner:innerWidth}));records.push({site:'census',width,...census,passed:census.document<=width+1&&census.inner<=width+1});console.log('census',width,census);await context.close();}
 }
 const fallback=await browser.newContext({viewport:{width:320,height:740},javaScriptEnabled:false});const fallbackPage=await fallback.newPage();await fallbackPage.goto(atlas.url+'/',{waitUntil:'networkidle'});if(!(await fallbackPage.locator('.top-nav').isVisible())||await fallbackPage.evaluate(()=>document.documentElement.scrollWidth)>321)throw Error('No-JavaScript navigation fallback failed');await fallback.close();interactions.push({check:'phone_navigation_without_javascript',passed:true});
 if(JSON.stringify(sourceHashes())!==JSON.stringify(sources))throw Error('UI source changed during browser checks');
 await browser.close();atlas.server.close();if(censusSite)censusSite.server.close();const receipt={status:records.every(r=>r.passed)?'PASS':'FAIL',browser:'Chromium '+browser.version(),source_sha256:sources,interactions,scope:'Actual browser layout at five viewport widths; phone touch emulation, navigation open/Escape, count-table horizontal scrolling and fusion-view switching. No physical device or WebKit execution is claimed.',records};fs.writeFileSync(path.join(out,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');if(receipt.status!=='PASS')process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
