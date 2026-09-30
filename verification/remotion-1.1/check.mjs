import {chromium} from '/Users/tt/projects/tt-site/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const out=path.join(root,'starter/out');
fs.writeFileSync(path.join(out,'preview.html'),'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Remotion 机制样片</title><body style="margin:32px;background:#eeeae2;font:16px Arial"><h1>Remotion 机制样片 · 8秒 / 60fps</h1><video id="video" controls style="width:min(100%,1280px)" src="motion-study.mp4"></video><p>帧时钟、错相、阅读停留验证；合成提示音为示例。</p></body></html>');
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1360,height:900}});
 await page.goto('file://'+path.join(out,'preview.html'));
 const report=await page.evaluate(async()=>{
  const v=document.querySelector('video');v.muted=true;
  await v.play();
  await new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(new Error('media error'));setTimeout(()=>reject(new Error('playback timeout')),15000)});
  const q=v.getVideoPlaybackQuality();
  return {ended:v.ended,currentTime:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight,total:q.totalVideoFrames,dropped:q.droppedVideoFrames,muted:v.muted,error:v.error};
 });
 if(!report.ended || report.width!==1280 || report.height!==720 || Math.abs(report.duration-8)>0.05)throw new Error(JSON.stringify(report));
 fs.writeFileSync(path.join(root,'playback.json'),JSON.stringify(report,null,2));console.log(report);
} finally {await browser.close()}
