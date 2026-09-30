import {fileURLToPath} from 'node:url';
import fs from 'node:fs';
import path from 'node:path';
export function createSound(root) {
  // Original synthetic guide track, no third-party recordings; not a finished mix.
  const rate = 48000, count = rate * 8, pcm = Buffer.alloc(count * 2);
  for (let i=0; i<count; i++) {
    const t=i/rate;
    let value=0;
    for (const [at,freq,amp] of [[3,220,0.14],[4.8,440,0.08]]) {
      const dt=t-at;
      if(dt>=0 && dt<0.5) value += amp*Math.min(1,dt/0.004)*Math.exp(-dt*16)*Math.sin(2*Math.PI*freq*dt);
    }
    pcm.writeInt16LE(Math.round(Math.max(-1,Math.min(1,value))*32767),i*2);
  }
  const h=Buffer.alloc(44); h.write('RIFF');h.writeUInt32LE(36+pcm.length,4);h.write('WAVEfmt ',8);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(1,22);h.writeUInt32LE(rate,24);h.writeUInt32LE(rate*2,28);h.writeUInt16LE(2,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(pcm.length,40);
  fs.mkdirSync(path.join(root,'public'),{recursive:true});fs.writeFileSync(path.join(root,'public/study.wav'),Buffer.concat([h,pcm]));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  createSound(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'));
}
