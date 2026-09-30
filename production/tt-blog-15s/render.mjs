import {chromium} from '/Users/tt/projects/tt-site/node_modules/playwright/index.mjs';
import {spawn,execFileSync} from 'node:child_process';import {once} from 'node:events';import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));const ff=execFileSync(path.join(dir,'.venv/bin/python'),['-c','import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'],{encoding:'utf8'}).trim();
fs.mkdirSync(path.join(dir,'checks'),{recursive:true});
const args=['-y','-f','image2pipe','-framerate','30','-vcodec','png','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',path.join(dir,'tt-blog-15s-silent.mp4')];
const ffproc=spawn(ff,args,{stdio:['pipe','ignore','pipe']});let log='';ffproc.stderr.on('data',d=>log+=d);const done=once(ffproc,'close');
const b=await chromium.launch({headless:true});const p=await b.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1});p.on('pageerror',e=>{throw e});
await p.goto(`file://${dir}/scene.html`);await p.evaluate(()=>document.fonts.ready);await p.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(im=>im.decode())));
const checks=new Set([0,12,24,48,66,71,72,78,83,90,123,159,170,171,177,182,189,219,252,263,264,270,275,282,318,348,359,360,366,377,378,408,449]);
for(let f=0;f<450;f++){await p.evaluate(f=>window.renderFrame(f),f);const png=await p.screenshot({type:'png'});if(checks.has(f))fs.writeFileSync(path.join(dir,'checks',`source-${String(f).padStart(3,'0')}.png`),png);if(!ffproc.stdin.write(png))await once(ffproc.stdin,'drain');if(f%60===0)console.log(`Rendered ${f}/450`)}
ffproc.stdin.end();await b.close();const [code]=await done;fs.writeFileSync(path.join(dir,'encode.log'),log);if(code!==0)throw new Error(log.slice(-2500));
execFileSync(ff,['-y','-i',path.join(dir,'tt-blog-15s-silent.mp4'),'-i',path.join(dir,'sound.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-t','15','-movflags','+faststart',path.join(dir,'tt-blog-15s.mp4')],{stdio:'ignore'});
console.log('Exported sound and silent versions');
