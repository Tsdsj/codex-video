#!/usr/bin/env python3
"""Original deterministic sound synthesis; Python standard library, no recordings/API."""
import argparse,array,hashlib,html,json,math,pathlib,random,sys,wave
SR=48000
TAU=2*math.pi
# id, label, synthesis mode, seconds, design anchor, frequency, characteristic, pan travel
PACKS={
 'soft-ui':('柔和交互',[
 ('soft-tap','柔点','tap',.18,.006,650,.025,0),
 ('felt-click','毡面点击','tap',.22,.006,290,.05,0),
 ('toggle-on','开关开启','toggle',.32,.012,540,1,0),
 ('toggle-off','开关关闭','toggle',.32,.012,540,-1,0),
 ('select-double','双点选择','double',.38,.09,780,.055,0),
 ('quiet-dismiss','轻收起','sweep',.35,.15,1700,-1,-.15)]),
 'air-motion':('空气转场',[
 ('air-pass','轻掠','sweep',.65,.30,1800,1,.45),
 ('silk-swipe','丝滑扫过','sweep',.95,.44,950,1,.35),
 ('quick-cut','短切','sweep',.25,.105,3400,1,.2),
 ('rise-soft','柔和上升','rise',1.25,1.02,500,1,.2),
 ('fall-soft','柔和回落','rise',1.10,.16,2100,-1,-.2),
 ('reverse-bloom','反向展开','bloom',1.20,.90,880,1,.15)]),
 'tactile':('材质触感',[
 ('wood-touch','木质轻触','material',.40,.004,310,0,0),
 ('ceramic-touch','陶质落点','material',.70,.004,1250,1,0),
 ('glass-tick','玻璃轻响','material',1.15,.004,1850,2,0),
 ('metal-soft','金属轻碰','material',.90,.004,820,3,0),
 ('paper-settle','纸面收拢','paper',.65,.19,800,1,.15),
 ('cushioned-land','缓冲落地','land',.55,.025,110,1,0)]),
 'resolution':('完成提示',[
 ('confirm-warm','温暖确认','notes',.90,.012,440,0,0),
 ('complete-clear','清晰完成','notes',1.25,.19,660,1,0),
 ('reveal-spark','揭示微光','notes',1.35,.26,880,2,.15),
 ('resolve-low','低调收束','notes',1.15,.012,220,3,0),
 ('soft-attention','柔和提醒','notes',.85,.012,520,4,0),
 ('brand-signoff','片尾签名','notes',1.65,.29,330,5,.1)])}

def edge(t,d):
 return min(1,t/.005,max(0,(d-t-1/SR)/.035))
def onset(t,decay,attack=.003):
 return 0 if t<0 else min(1,t/attack)*math.exp(-t/decay)
def tone(t,freq,decay):
 return math.sin(TAU*freq*t)*onset(t,decay)
def synth(recipe):
 ident,label,mode,d,anchor,freq,kind,pan=recipe
 rng=random.Random(int(hashlib.sha256(ident.encode()).hexdigest()[:16],16))
 n=round(d*SR);values=array.array('f');low=0;slow=0;phase=0
 for i in range(n):
  t=i/SR;u=t/d;noise=rng.uniform(-1,1)
  # Variable low-pass and a slower low-pass difference form a moving noise band.
  center=freq*(.45+2.4*(u if kind>=0 else 1-u))
  alpha=1-math.exp(-TAU*min(center,8500)/SR)
  low+=alpha*(noise-low);slow+=(alpha*.17)*(noise-slow);band=low-slow
  if mode=='tap':
   x=.8*tone(t,freq,kind)+.25*noise*onset(t,.008)
  elif mode=='toggle':
   phase+=TAU*freq*(1+kind*.35*min(1,t/.09))/SR
   x=math.sin(phase)*onset(t,.05)+.13*noise*onset(t,.012)
  elif mode=='double':
   x=tone(t,freq,.045)+.70*tone(t-.09,freq*1.25,.055)
  elif mode=='sweep':
   env=math.sin(math.pi*u)**2.5
   x=band*env*(.8+.2*math.sin(TAU*3*u))
  elif mode=='rise':
   env=(u**1.8 if kind>0 else (1-u)**1.8)*math.sin(math.pi*u)**.65
   phase+=TAU*(90+140*(u if kind>0 else 1-u))/SR
   x=(band*.85+.06*math.sin(phase))*env
  elif mode=='bloom':
   env=(t/anchor)**3 if t<anchor else math.exp(-(t-anchor)/.09)
   x=(band+.17*math.sin(TAU*freq*t))*env
  elif mode=='material':
   ratios=[(1,2.72,4.15),(1,1.57,2.83),(1,2.32,4.25),(1,1.43,2.71)][int(kind)]
   decay=[.055,.12,.25,.18][int(kind)]
   x=sum((.6**k)*tone(t,freq*r,decay/(1+k*.4)) for k,r in enumerate(ratios))+.13*noise*onset(t,.006)
  elif mode=='paper':
   env=sum(math.exp(-((t-c)/w)**2) for c,w in [(.12,.055),(.23,.035),(.35,.07)])
   x=band*env*(.65+.35*math.sin(TAU*47*t)**2)
  elif mode=='land':
   phase+=TAU*(freq+150*math.exp(-t/.024))/SR
   x=math.sin(phase)*onset(t,.065,.006)+.45*low*onset(t,.055,.005)
  elif mode=='notes':
   sequences=[[(0,1,.6),(.13,1.25,.45)],[(0,1,.5),(.18,1.5,.65)],[(0,1,.45),(.12,1.25,.4),(.25,1.5,.5)],[(0,1,.65),(.16,2,.2)],[(0,1,.55),(.14,1.125,.35)],[(0,1,.5),(.14,1.5,.35),(.28,2,.5)]]
   x=0
   for at,ratio,amp in sequences[int(kind)]:
    tt=t-at
    if tt>=0:x+=amp*(tone(tt,freq*ratio,.15)+.15*tone(tt,freq*ratio*2,.065))
  else:raise ValueError(mode)
  x*=edge(t,d)
  balance=pan*(2*u-1)
  # Amplitude-only pan: no polarity inversion or stereo phase tricks.
  values.append(x*math.cos((balance+1)*math.pi/4));values.append(x*math.sin((balance+1)*math.pi/4))
 # Remove residual DC, then reapply edge taper to retain exact zero endpoints.
 for ch in (0,1):
  mean=sum(values[ch::2])/n
  for i in range(n):values[2*i+ch]=(values[2*i+ch]-mean)*edge(i/SR,d)
 peak=max(abs(v) for v in values);target=10**((-9 if mode in ('tap','toggle','double') else -7)/20)
 pcm=array.array('h',(round(v/peak*target*32767) for v in values))
 return pcm

def write(path,pcm):
 path.parent.mkdir(parents=True,exist_ok=True)
 if sys.byteorder!='little':pcm=pcm[:];pcm.byteswap()
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())

def build(out):
 if out.exists() and any(out.iterdir()):raise FileExistsError('Use a new empty output directory')
 out.mkdir(parents=True,exist_ok=True);assets=[];sections=[]
 for pack,(title,recipes) in PACKS.items():
  reel=array.array('h');cards=[];reel_cues=[]
  for recipe in recipes:
   ident,label,mode,d,anchor,*_=recipe;pcm=synth(recipe);rel=f'{pack}/{ident}.wav';p=out/rel;write(p,pcm)
   peak=max(abs(v) for v in pcm)/32767
   reel_cues.append({'id':ident,'start_seconds':len(reel)/2/SR});reel.extend(pcm);reel.extend(array.array('h',[0])*round(.45*SR)*2)
   assets.append({'id':ident,'pack':pack,'label':label,'file':rel,'duration_seconds':d,'anchor_seconds':anchor,'anchor_method':'designed gesture/contact point; confirm perceptually','suggested_gain_db':-9,'synthesis':mode,'peak_dbfs':20*math.log10(peak),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'original procedural synthesis; no third-party recording','listening':'not_verified'})
   cards.append(f'<article><b>{html.escape(label)}</b><small>{ident} · {d}s · 对齐 {anchor}s</small><audio controls preload="none" src="{rel}"></audio><a href="{rel}" download>下载 WAV</a></article>')
  write(out/f'{pack}-reel.wav',reel)
  (out/f'{pack}-reel.json').write_text(json.dumps(reel_cues,indent=2)+'\n')
  sections.append(f'<section><h2>{title}</h2><p>整组串听（按下方顺序，间隔 0.45 秒）</p><audio controls preload="none" src="{pack}-reel.wav"></audio><div class="grid">'+''.join(cards)+'</div></section>')
 (out/'catalog.json').write_text(json.dumps({'version':'1.0.0','sample_rate':SR,'channels':2,'format':'PCM WAV 16-bit','assets':assets},ensure_ascii=False,indent=2)+'\n')
 (out/'preview.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>原创动效音效包</title><style>body{max-width:1100px;margin:36px auto;padding:0 20px;background:#f5f3ef;color:#26352e;font:16px/1.6 system-ui}h1{line-height:1.2}section{margin:48px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px;margin-top:20px}article{padding:20px;background:white;border:1px solid #dce0d7;border-radius:12px}small{display:block;color:#626e65}audio{display:block;width:min(100%,400px);margin:14px 0}a{color:#315c43}</style><h1>原创动效音效 · 24 款</h1><p>48 kHz / 16-bit / 双声道。四个系列，可下载单个 WAV 或整组串听。请从低音量试听。</p><p>这是程序合成的设计音效，材质名称表示风格化方向，不是真实拟音。技术检查与主观听感验收分开记录。</p>'''+''.join(sections)+'''<script>document.querySelectorAll('audio').forEach(el=>el.addEventListener('play',()=>document.querySelectorAll('audio').forEach(other=>{if(other!==el)other.pause()})))</script></html>''')
 print(f'Generated {len(assets)} originals and 4 audition reels at {out}')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=pathlib.Path);a=p.parse_args();build(a.output)
