import {chromium} from '/Users/tt/projects/tt-site/node_modules/playwright/index.mjs';
import fs from 'node:fs';import path from 'node:path';
const root=path.resolve('plugins/motion-director/skills/motion-director/assets/original-audio');
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage();await page.goto('file://'+root+'/preview.html');
 const meta=await page.locator('audio').evaluateAll(async els=>Promise.all(els.map(el=>new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error('load timeout')),10000);el.onloadedmetadata=()=>{clearTimeout(timer);resolve({src:el.getAttribute('src'),duration:el.duration})};el.onerror=()=>{clearTimeout(timer);reject(new Error('load error'))};el.load()}))));
 if(meta.length!==28 || meta.some(x=>!(x.duration>0)))throw new Error('missing audio');
 const exclusive=await page.evaluate(async()=>{const [a,b]=document.querySelectorAll('audio');a.muted=b.muted=true;await a.play();await b.play();const result=a.paused&&!b.paused;b.pause();return result});
 if(!exclusive)throw new Error('overlapping playback');
 fs.writeFileSync('verification/audio-1.3/browser.json',JSON.stringify({audio_count:meta.length,exclusive_playback:exclusive,metadata:meta,listening:'not_verified'},null,2));console.log('28 audio players loaded; single-player playback verified');
}finally{await browser.close()}
