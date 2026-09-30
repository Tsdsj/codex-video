import {chromium} from '/Users/tt/projects/tt-site/node_modules/playwright/index.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage();await page.goto('file://'+path.join(root,'preview.html'));const reports=[];
 for(const id of ['a','b']) {
  const r=await page.evaluate(async(id)=>{const v=document.getElementById(id);v.muted=true;await v.play();await new Promise((res,rej)=>{const timer=setTimeout(()=>rej(new Error('timeout')),12000);v.addEventListener('ended',()=>{clearTimeout(timer);res()},{once:true});v.addEventListener('error',()=>rej(new Error('media error')),{once:true})});const q=v.getVideoPlaybackQuality();return {id,ended:v.ended,duration:v.duration,width:v.videoWidth,total:q.totalVideoFrames,dropped:q.droppedVideoFrames,error:v.error,muted:v.muted}},id);
  if(!r.ended || r.width!==1280 || Math.abs(r.duration-8)>.05 || r.error)throw new Error(JSON.stringify(r));reports.push(r);
 }
 await page.locator('summary').click();
 const sources=await page.locator('audio').evaluateAll(async els=>Promise.all(els.map(el=>new Promise((res,rej)=>{el.onloadedmetadata=()=>res({duration:el.duration,error:el.error});el.onerror=()=>rej(new Error('candidate decode error'));el.load()}))));
 if(sources.length!==8 || sources.some(x=>!(x.duration>0)))throw new Error('candidate failure');
 const result={reports,candidates:sources,listening:'not_verified'};fs.writeFileSync(path.join(root,'playback.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
} finally {await browser.close()}
