import {chromium} from '/Users/tt/projects/tt-site/node_modules/playwright/index.mjs';
import sharp from '/Users/tt/projects/tt-site/node_modules/sharp/lib/index.js';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const dir=path.dirname(fileURLToPath(import.meta.url));
const b=await chromium.launch({headless:true});
const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
const parts=[];
const labels=['01 / ONLINE     00:00—00:02.4','02 / CITY       00:02.4—00:05.7','03 / DETAIL     00:05.7—00:08.8','04 / WRITING    00:08.8—00:12.0','05 / VISIT      00:12.0—00:15.0'];
for(let i=1;i<=5;i++){
 await p.goto(`file://${dir}/keyframes.html?frame=${i}`);
 await p.evaluate(()=>document.fonts.ready);
 await p.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(im=>im.complete?Promise.resolve():new Promise(r=>{im.onload=r;im.onerror=r}))));
 const out=path.join(dir,`keyframe-0${i}.png`);await p.screenshot({path:out});
 const small=await sharp(out).resize(800,450).toBuffer();const x=32+((i-1)%2)*824,y=112+Math.floor((i-1)/2)*508;
 parts.push({input:small,left:x,top:y});
 const label=Buffer.from(`<svg width="800" height="40"><text x="0" y="26" fill="#bdbdc7" font-family="monospace" font-size="17">${labels[i-1]}</text></svg>`);parts.push({input:label,left:x,top:y+450});
}
const title=Buffer.from('<svg width="1680" height="90"><text x="32" y="47" fill="#ededef" font-family="sans-serif" font-size="29">tt-blog / SIGNAL, ONLINE.</text><text x="32" y="78" fill="#7cffb2" font-family="monospace" font-size="16">DIRECTOR BOARD 01 · 15 SECONDS · 16:9 · STATIC KEYFRAMES</text></svg>');parts.push({input:title,left:0,top:0});
await sharp({create:{width:1680,height:1640,channels:3,background:'#151518'}}).composite(parts).jpeg({quality:94}).toFile(path.join(dir,'contact-sheet.jpg'));
console.log('Rendered five 1600×900 keyframes and contact sheet.');await b.close();
