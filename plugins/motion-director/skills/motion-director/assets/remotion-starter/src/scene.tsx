import React from 'react';
import {AbsoluteFill, Html5Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {stage, travel} from './motion';

const palette = {paper: '#eeeae2', ink: '#222e2b', green: '#365e4e', muted: '#758078'};
// A local-frame component. It receives zero on its Sequence's first frame.
const Resolution = () => {
  const local = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = travel(local, 0, 0.55 * fps);
  return <div style={{position:'absolute', left:76, bottom:66, opacity:enter, transform:`translateY(${(1-enter)*12}px)`, fontSize:18, letterSpacing:1, color:palette.muted}}>INTENT → MOTION → CLARITY</div>;
};

export const MotionStudy: React.FC<{sound:boolean}> = ({sound}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = stage(f, fps);
  const reveal = s.reveal;
  const finish = spring({frame:f - 3.0 * fps, fps, config:{damping:24, stiffness:120, mass:1}, durationInFrames:Math.round(0.9*fps)});
  const x = 170 + 665 * s.x;
  const y = 442 - 68 * Math.sin(Math.PI * s.x);
  const cardX = 820;
  const title = travel(f, 4.3*fps, 4.8*fps);
  return <AbsoluteFill style={{backgroundColor:palette.paper, fontFamily:'Arial, sans-serif', color:palette.ink, overflow:'hidden'}}>
    {sound && <Html5Audio src={staticFile('study.wav')} volume={0.7} />}
    <div style={{position:'absolute', left:76, top:58, fontSize:14, letterSpacing:3, color:palette.muted}}>MOTION DIRECTOR / STUDY 01</div>
    <div style={{position:'absolute', right:76, top:58, fontSize:14, color:palette.muted}}>FORM & CONTINUITY</div>
    <div style={{position:'absolute', left:76, top:139, opacity:s.title, transform:`translateY(${(1-s.title)*16}px)`}}>
      <div style={{fontSize:76, lineHeight:1.04, letterSpacing:-4, fontWeight:500}}>Move with<br/>a reason.</div>
      <div style={{fontSize:19, marginTop:26, color:palette.muted}}>One gesture. A clear destination.</div>
    </div>
    <div style={{position:'absolute', left:130, right:144, top:511, height:1, background:'#c9cdc4'}} />
    {[2,1,0].map(i => {
      const fan = travel(f, (3.12 + i*0.1)*fps, (4.25 + i*0.1)*fps);
      return <div key={i} style={{position:'absolute', left:cardX-50 + i*25*fan, top:276-i*26*fan, width:234, height:238, borderRadius:18, background:i===0?'#fcfbf7':i===1?'#d5dace':'#b5c3b1', border:'1px solid #b6c1b4', opacity:fan, transform:`translateY(${(1-fan)*30}px) rotate(${i*4*fan}deg)`, transformOrigin:'50% 100%', boxShadow:i===0?'0 22px 30px #33433212':undefined}}>
        {i===0 && <><div style={{position:'absolute',left:26,top:26,width:32,height:4,background:palette.green}}/><div style={{position:'absolute',left:26,bottom:58,fontSize:28,letterSpacing:-1,opacity:reveal}}>Purpose,<br/>in every frame.</div><div style={{position:'absolute',left:26,bottom:24,fontSize:11,letterSpacing:2,color:palette.muted}}>DIRECTED MOTION</div></>}
      </div>;
    })}
    <div style={{position:'absolute', left:x-36, top:499, width:72, height:12, borderRadius:'50%', background:'#17251c', opacity:0.1*(1-0.35*Math.sin(Math.PI*s.x))*(1-travel(f,3.12*fps,3.55*fps)), filter:'blur(7px)', transform:`scaleX(${1-0.25*Math.sin(Math.PI*s.x)})`}} />
    <div style={{position:'absolute', left:x-44, top:y-44 - finish*8, width:88, height:88, borderRadius:44, opacity:1-travel(f,3.12*fps,3.55*fps), background:'radial-gradient(circle at 30% 25%, #9bac8c, #466a52 48%, #203e31 100%)', boxShadow:'inset -5px -5px 12px #14291c44'}} />
    <div style={{position:'absolute', left:770, top:556, fontSize:15, letterSpacing:2, color:palette.muted, opacity:title}}>LESS NOISE. MORE INTENT.</div>
    <Sequence from={Math.round(4.8*fps)}><Resolution/></Sequence>
  </AbsoluteFill>;
};
