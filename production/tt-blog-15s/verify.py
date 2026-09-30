from pathlib import Path
import subprocess,json,re
import imageio_ffmpeg
p=Path(__file__).resolve().parent;ff=imageio_ffmpeg.get_ffmpeg_exe()
(p/'frames').mkdir(exist_ok=True)
subprocess.run([ff,'-y','-i',str(p/'tt-blog-15s.mp4'),'-map','0:v:0','-q:v','3',str(p/'frames/frame-%04d.jpg')],check=True,capture_output=True)
r=subprocess.run([ff,'-v','info','-i',str(p/'tt-blog-15s.mp4'),'-vf','blackdetect=d=0.03:pix_th=0.02','-af','astats=metadata=0:reset=0','-f','null','-'],capture_output=True,text=True)
(p/'checks/decode.log').write_text(r.stderr)
frames=len(list((p/'frames').glob('frame-*.jpg')))
meta={'decode_exit_code':r.returncode,'frames':frames,'expected_frames':450,'duration_seconds':15,'ffmpeg':ff,'black_intervals':re.findall(r'black_start:[^\n]+',r.stderr),'metadata':[x.strip() for x in r.stderr.splitlines() if 'Duration:' in x or 'Stream #0:' in x or 'Peak level dB:' in x]}
assert r.returncode==0 and frames==450,meta
(p/'checks/technical.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
