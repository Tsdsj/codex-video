// Deterministic, frame-indexed scene. No wall clock or runtime randomness.
const board=document.querySelector('.board');board.id='stage';
const bridge=document.createElement('div');bridge.id='bridge';board.appendChild(bridge);
const scenes=[...document.querySelectorAll('.frame')];
const cv=document.createElement('canvas');cv.width=870;cv.height=680;document.querySelector('.sphere').appendChild(cv);const ctx=cv.getContext('2d');
const clamp=v=>Math.max(0,Math.min(1,v));const smooth=v=>{v=clamp(v);return v*v*(3-2*v)};const mix=(a,b,p)=>a+(b-a)*p;
const points=Array.from({length:10500},(_,i)=>{const y=1-2*(i+.5)/10500,r=Math.sqrt(1-y*y),a=i*2.399963229728653;return [r*Math.cos(a),y,r*Math.sin(a),i]});
function sphere(f){ctx.clearRect(0,0,870,680);const assemble=smooth(f/22),spread=smooth((f-66)/18),angle=f*.0028;
 for(const [x,y,z,i] of points){const rx=x*Math.cos(angle)+z*Math.sin(angle),rz=-x*Math.sin(angle)+z*Math.cos(angle);const depth=(rz+1)/2;
 const px=mix(430+rx*268,50+(i%150)*5.2,spread),py=mix(340+y*268+(1-assemble)*(220+((i*37)%190)),480+Math.floor(i/150)*1.5,spread);
 const green=(Math.abs(Math.sin(Math.atan2(z,x)*3+y*4))<.055);ctx.fillStyle=green?`rgba(124,255,178,${(.2+depth*.6)*mix(.55,1,assemble)})`:`rgba(200,204,215,${(.055+depth*.35)*mix(.4,1,assemble)})`;ctx.fillRect(px,py,green?1.5:1,green?1.5:1);
 }
}
function opacity(el,n){if(el)el.style.opacity=clamp(n)}
window.renderFrame=f=>{
 board.style.transform=`scale(${innerWidth/1600})`;
 const ranges=[[0,84],[66,183],[159,276],[252,378],[348,450]];
 scenes.forEach((s,i)=>{const [a,b]=ranges[i];let op=i===0?1:smooth((f-a)/18);if(i<4)op*=1-smooth((f-(b-18))/18);opacity(s,op);s.style.zIndex=i;
 const content=s.querySelector('.copy')||s.querySelector('.center');const enter=smooth((f-[6,84,177,270,366][i])/[18,12,12,12,12][i]),leave=i===4?1:1-smooth((f-[60,153,246,342][i])/12);opacity(content,enter*leave);content.style.transform=`translateY(${(1-enter)*16}px)`;
 opacity(s.querySelector('.channel'),i===0?smooth(f/12):enter);opacity(s.querySelector('.bottom'),i===0?smooth(f/15):enter);
 });
 sphere(f);
 const city=scenes[1].querySelector('.media img');city.style.transform=`scale(${1+.04*clamp((f-72)/87)})`;city.style.transformOrigin='60% 50%';
 const glass=scenes[2].querySelector('.image-window');glass.style.transform=`translateX(${48*(1-smooth((f-171)/18))}px)`;
 const pap=scenes[3].querySelector('.paper'),m=smooth((f-252)/30);Object.assign(pap.style,{left:mix(620,763,m)+'px',top:mix(265,175,m)+'px',width:mix(900,737,m)+'px',height:mix(347,565,m)+'px'});opacity(pap,smooth((f-258)/18)*(1-smooth((f-348)/12)));[...pap.children].forEach(e=>opacity(e,smooth((f-270)/12)));opacity(scenes[3].querySelector('.rail'),smooth((f-276)/12)*(1-smooth((f-348)/12)));
 const l=smooth((f-348)/12),grow=smooth((f-360)/18),ur=scenes[4].querySelector('.url').getBoundingClientRect(),scale=innerWidth/1600,tx=ur.left/scale,ty=ur.bottom/scale-2;
 Object.assign(bridge.style,{left:mix(736,tx,l)+'px',top:mix(175,ty,l)+'px',width:mix(2,ur.width/scale,grow)+'px',height:mix(565,2,l)+'px',transform:'none',opacity:f>=348&&f<378?String(.55*(1-smooth((f-372)/6))):'0'});
 return f;
};window.renderFrame(0);

