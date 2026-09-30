from pathlib import Path
import json,wave,array,math,hashlib
root=Path('plugins/motion-director/skills/motion-director/assets/original-audio')
assert (root/'catalog.json').is_file(),'Original sound pack not generated'
j=json.loads((root/'catalog.json').read_text());assert len(j['assets'])==24
hashes=set()
for a in j['assets']:
 p=root/a['file']
 with wave.open(str(p)) as w:
  assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,2,2)
  count=w.getnframes();pcm=array.array('h');pcm.frombytes(w.readframes(count))
 assert count==round(a['duration_seconds']*48000)
 assert 0<=a['anchor_seconds']<a['duration_seconds']
 assert max(abs(x) for x in pcm)<=16500
 assert max(abs(x) for x in pcm)>1000
 assert pcm[:2]==array.array('h',[0,0]) and pcm[-2:]==array.array('h',[0,0]),a['id']
 stereo=sum(x*x for x in pcm)/len(pcm)
 mono=sum(((pcm[k]+pcm[k+1])/2)**2 for k in range(0,len(pcm),2))/count
 assert mono/stereo>.65,(a['id'],'mono cancellation')
 sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==a['sha256'];hashes.add(sha)
assert len(hashes)==24,'Duplicate sound files'
print('24 WAVs verified: format, duration, anchors, peaks, edges, mono compatibility, unique hashes')
