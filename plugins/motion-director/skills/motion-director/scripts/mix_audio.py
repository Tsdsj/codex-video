#!/usr/bin/env python3
"""Offline cue mixer. Python standard library + an installed FFmpeg; no API/network."""
import argparse,array,json,math,pathlib,re,shutil,subprocess,sys,wave
RATE=48000
ROLES=('sfx','music','ambience','voice')
def db_gain(db):
    return 10**(db/20)
def cue_start(frame,fps,anchor,rate=RATE):
    return round(frame*rate/fps)-round(anchor*rate)
def fade_gain(i,n,attack,release):
    return min(1,i/max(1,attack),(n-1-i)/max(1,release))
def duck_gain(t,ducks,fps):
    gain=1.0
    for d in ducks:
        start,end=d['start_frame']/fps,d['end_frame']/fps
        a,r=d.get('attack_seconds',.08),d.get('release_seconds',.25)
        if start<=t<=end: progress=1
        elif a>0 and start-a<t<start: progress=(t-start+a)/a
        elif r>0 and end<t<end+r: progress=1-(t-end)/r
        else: progress=0
        gain=min(gain,db_gain(d['gain_db']*progress))
    return gain

def number(v,lo,hi,label):
    if not isinstance(v,(int,float)) or not math.isfinite(v) or not lo<=v<=hi:
        raise ValueError(f'Invalid {label}: {v}')
def validate(j):
    number(j.get('fps'),1,240,'fps');number(j.get('duration_seconds'),.01,300,'duration_seconds')
    number(j.get('master_ceiling_db',-3),-30,0,'master ceiling')
    for role,g in j.get('bus_gain_db',{}).items():
        if role not in ROLES:raise ValueError('Unknown bus '+role)
        number(g,-120,12,'bus gain')
    if not isinstance(j.get('cues'),list):raise ValueError('cues must be a list')
    for c in j['cues']:
        if not isinstance(c.get('file'),str) or not c['file']:raise ValueError('Missing audio file')
        number(c.get('event_frame'),0,j['fps']*j['duration_seconds']-1,'event frame')
        if c.get('role','sfx') not in ROLES:raise ValueError('Unknown role')
        number(c.get('anchor_seconds',0),0,300,'anchor')
        number(c.get('gain_db',0),-120,12,'gain')
        for k in ('trim_start_seconds','fade_in_seconds','fade_out_seconds'):
            number(c.get(k,0),0,300,k)
        if 'trim_end_seconds' in c:
            number(c['trim_end_seconds'],c.get('trim_start_seconds',0)+.00001,300,'trim end')
    for d in j.get('ducks',[]):
        number(d.get('start_frame'),0,j['fps']*j['duration_seconds'],'duck start')
        number(d.get('end_frame'),d['start_frame']+1,j['fps']*j['duration_seconds'],'duck end')
        number(d.get('gain_db'),-60,0,'duck gain')
        for k in ('attack_seconds','release_seconds'):number(d.get(k,.1),0,10,k)
        if any(r not in ROLES for r in d.get('roles',['music','ambience'])):raise ValueError('Unknown duck role')

def executable(given):
    if given:return given
    found=shutil.which('ffmpeg')
    if found:return found
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:raise RuntimeError('FFmpeg not found. Pass --ffmpeg PATH or use an environment with imageio-ffmpeg.')
def decode(ff,path,limit):
    r=subprocess.run([ff,'-v','error','-i',str(path),'-t',str(limit),'-vn','-ac','2','-ar',str(RATE),'-f','f32le','pipe:1'],capture_output=True,check=True)
    values=array.array('f');values.frombytes(r.stdout)
    if sys.byteorder!='little':values.byteswap()
    if not values or any(not math.isfinite(v) for v in values):raise ValueError('Empty or invalid audio: '+str(path))
    return values

def write_wav(path,samples,gain=1):
    pcm=array.array('h',(round(max(-1,min(1,x*gain))*32767) for x in samples))
    if sys.byteorder!='little':pcm.byteswap()
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(pcm.tobytes())

def mix(manifest,out,ff):
    j=json.loads(manifest.read_text());validate(j)
    out.mkdir(parents=True,exist_ok=True)
    # Never overwrite a previous mix by accident.
    if (out/'mix.wav').exists():raise FileExistsError('Use a new output directory: '+str(out))
    n=round(j['duration_seconds']*RATE);buses={};events=[]
    for c in j['cues']:
        p=(manifest.parent/c['file']).resolve()
        if not p.is_file():raise FileNotFoundError(p)
        raw=decode(ff,p,300)
        a=round(c.get('trim_start_seconds',0)*RATE)
        b=min(len(raw)//2,round(c.get('trim_end_seconds',len(raw)/2/RATE)*RATE))
        if a>=b:raise ValueError('Empty trim: '+str(p))
        clip=raw[a*2:b*2];length=len(clip)//2
        anchor=c.get('anchor_seconds',0)
        if anchor*RATE>=length:raise ValueError('Anchor outside trimmed clip')
        start=cue_start(c['event_frame'],j['fps'],anchor)
        role=c.get('role','sfx');bus=buses.setdefault(role,array.array('f',[0])*(n*2))
        gain=db_gain(c.get('gain_db',0))
        attack=round(c.get('fade_in_seconds',.003)*RATE);release=round(c.get('fade_out_seconds',.025)*RATE)
        lo=max(0,-start);hi=min(length,n-start)
        for k in range(lo,hi):
            g=gain*fade_gain(k,length,attack,release)
            index=(start+k)*2;bus[index]+=clip[k*2]*g;bus[index+1]+=clip[k*2+1]*g
        events.append({'file':c['file'],'role':role,'event_frame':c['event_frame'],'start_sample':start,'anchor_sample':round(anchor*RATE),'clipped_head_samples':lo,'clipped_tail_samples':max(0,length-hi)})
    total=array.array('f',[0])*(n*2)
    for role,bus in buses.items():
        ds=[d for d in j.get('ducks',[]) if role in d.get('roles',['music','ambience'])]
        bus_gain=db_gain(j.get('bus_gain_db',{}).get(role,0))
        for k in range(n):
            g=bus_gain*(duck_gain(k/RATE,ds,j['fps']) if ds else 1)
            bus[k*2]*=g;bus[k*2+1]*=g
            total[k*2]+=bus[k*2];total[k*2+1]+=bus[k*2+1]
    peak=max((abs(v) for v in total),default=0)
    ceiling=db_gain(j.get('master_ceiling_db',-3))
    stem_peak=max((abs(v) for bus in buses.values() for v in bus),default=0)
    safe_peak=max(peak,stem_peak)
    attenuation=min(1,ceiling/safe_peak) if safe_peak else 1
    write_wav(out/'mix.wav',total,attenuation)
    for role,bus in buses.items():write_wav(out/f'{role}.wav',bus,attenuation)
    # Analysis only: this loudnorm invocation does not replace or normalize the mix.
    r=subprocess.run([ff,'-hide_banner','-i',str(out/'mix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    m=re.search(r'\{\s*"input_i"[\s\S]*?\}',r.stderr)
    measurement={k:v for k,v in json.loads(m.group()).items() if k.startswith('input_')} if m else None
    if measurement is None:raise RuntimeError('Loudness analysis missing')
    report={'sample_rate':RATE,'channels':2,'samples':n,'duration_seconds':n/RATE,'pre_master_peak':peak,'master_attenuation_db':20*math.log10(attenuation),'measurements':measurement,'events':events,'warnings':[],'listening':'not_verified'}
    if any(e['clipped_head_samples'] or e['clipped_tail_samples'] for e in events):report['warnings'].append('Some cue heads/tails were clipped at timeline boundaries; review events.')
    if float(measurement['input_tp'])>-1:report['warnings'].append('True peak above -1 dBTP; lower mix and review encoded delivery.')
    if not peak:report['warnings'].append('Silent mix')
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--ffmpeg');a=p.parse_args()
    mix(a.manifest.resolve(),a.output.resolve(),executable(a.ffmpeg))
if __name__=='__main__':main()
