"""Original synthesized sound bed; no sampled or third-party audio."""
import math,wave,struct
from pathlib import Path
rate=48000;length=15
out=Path(__file__).resolve().parent/'sound.wav'
events=[(.2, .2, .48, 880, .1),(6.1,.2,.5,420,.07),(12.2,.4,.68,660,.09)]
with wave.open(str(out),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate)
 data=bytearray()
 for n in range(rate*length):
  t=n/rate
  fade=min(1,t/.65)*min(1,max(0,(15-t)/1.0))
  pad=fade*.012*(math.sin(2*math.pi*110*t)+.5*math.sin(2*math.pi*165*t)+.3*math.sin(2*math.pi*220*t))
  v=pad
  for start,peak,dur,hz,gain in events:
   u=t-start
   if 0<=u<dur:
    attack=min(1,u/max(.008,peak))
    tail=max(0,1-(u-peak)/max(.01,dur-peak)) if u>peak else 1
    env=attack*tail*tail
    v+=gain*env*(math.sin(2*math.pi*hz*u)+.25*math.sin(2*math.pi*hz*1.5*u))
  value=int(max(-1,min(1,v))*32767);data.extend(struct.pack('<hh',value,value))
 w.writeframes(data)
print(out)
