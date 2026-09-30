import importlib.util,pathlib,tempfile,wave,array,json,contextlib,io
p=pathlib.Path('plugins/motion-director/skills/motion-director/scripts/mix_audio.py').resolve();s=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);clip=array.array('h',[0])*4800;clip[480]=16384
 with wave.open(str(d/'impulse.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(clip.tobytes())
 manifest={'fps':60,'duration_seconds':.5,'master_ceiling_db':-6,'cues':[{'file':'impulse.wav','event_frame':12,'anchor_seconds':.01,'fade_in_seconds':0,'fade_out_seconds':0,'gain_db':12}]*2}
 (d/'cues.json').write_text(json.dumps(manifest))
 with contextlib.redirect_stdout(io.StringIO()):m.mix(d/'cues.json',d/'out',m.executable(None))
 with wave.open(str(d/'out/mix.wav')) as w:
  assert w.getnframes()==24000
  a=array.array('h');a.frombytes(w.readframes(w.getnframes()))
 peak=max(range(len(a)),key=lambda k:abs(a[k]))
 assert peak//2==9600,(peak//2,'expected event at 0.2s')
 assert max(abs(x) for x in a)<=round(m.db_gain(-6)*32767)+1
 assert (d/'out/sfx.wav').exists()
 try:m.mix(d/'cues.json',d/'out',m.executable(None));raise AssertionError('overwrite allowed')
 except FileExistsError:pass
print('Integration passed: sample alignment, summed clipping protection, duration, stem, overwrite refusal')

with tempfile.TemporaryDirectory() as td:
 import math
 d=pathlib.Path(td);tone=array.array('h',(round(3000*math.sin(2*math.pi*200*i/48000)) for i in range(96000)))
 with wave.open(str(d/'tone.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(tone.tobytes())
 j={'fps':60,'duration_seconds':2,'cues':[{'file':'tone.wav','event_frame':0,'role':'music'}],'ducks':[{'start_frame':30,'end_frame':60,'gain_db':-12,'attack_seconds':.1,'release_seconds':.2}]}
 (d/'cues.json').write_text(json.dumps(j))
 with contextlib.redirect_stdout(io.StringIO()):m.mix(d/'cues.json',d/'out',m.executable(None))
 with wave.open(str(d/'out/music.wav')) as w:
  a=array.array('h');a.frombytes(w.readframes(w.getnframes()))
 def rms(start):
  chunk=a[round(start*48000)*2:round((start+.1)*48000)*2];return (sum(x*x for x in chunk)/len(chunk))**.5
 assert abs(rms(.7)/rms(.2)-m.db_gain(-12))<.001
 assert abs(rms(1.4)/rms(.2)-1)<.001
print('Ducking integration passed: measured attenuation and recovery in exported music stem')
