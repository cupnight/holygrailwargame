const LOBBY=(()=>{

function rnd(seed){let a=seed;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const hsh=(x,y)=>{let n=Math.imul(x|0,374761393)+Math.imul(y|0,668265263);n=Math.imul(n^n>>>13,1274126177);return((n^n>>>16)>>>0)/4294967296};
const vn=(x,y)=>{const xi=Math.floor(x),yi=Math.floor(y),fx=x-xi,fy=y-yi,u=fx*fx*(3-2*fx),v=fy*fy*(3-2*fy);return(hsh(xi,yi)*(1-u)+hsh(xi+1,yi)*u)*(1-v)+(hsh(xi,yi+1)*(1-u)+hsh(xi+1,yi+1)*u)*v};
const fbm=(x,y,o=5)=>{let a=.5,f=1,s=0;for(let i=0;i<o;i++){s+=a*vn(x*f,y*f);a*=.5;f*=2.03}return s};
const L=(a,b,t)=>a+(b-a)*t,cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),sst=(a,b,v)=>{const t=cl((v-a)/(b-a));return t*t*(3-2*t)};
const mixc=(a,b,t)=>[L(a[0],b[0],t),L(a[1],b[1],t),L(a[2],b[2],t)],rgb=c=>`rgb(${c[0]|0},${c[1]|0},${c[2]|0})`;
const TIME={
 n:{sky:[[0,[3,6,16]],[.45,[7,16,38]],[.8,[13,34,66]],[1,[30,60,92]]],star:1,mw:1,cTop:[40,58,104],cBot:[26,30,60],warm:[255,150,84],rim:[70,90,130],haze:[24,44,74],front:[9,14,26],side:[6,9,18],top:[16,22,38],ground:[6,10,19],water:[14,32,62],label:'밤'},
 y:{sky:[[0,[3,6,16]],[.45,[7,16,38]],[.8,[13,34,66]],[1,[30,60,92]]],star:1,mw:1,cTop:[40,58,104],cBot:[26,30,60],warm:[255,150,84],rim:[70,90,130],haze:[24,44,74],front:[9,14,26],side:[6,9,18],top:[16,22,38],ground:[6,10,19],water:[14,32,62],label:'낮'},
 d:{sky:[[0,[22,30,66]],[.5,[62,66,112]],[.82,[176,118,128]],[1,[244,184,132]]],star:.5,mw:.45,cTop:[120,96,140],cBot:[80,62,104],warm:[255,170,110],rim:[110,70,60],haze:[150,110,126],front:[44,38,70],side:[32,28,54],top:[70,60,96],ground:[40,34,60],water:[150,112,130],label:'새벽'},
 e:{sky:[[0,[22,30,66]],[.5,[62,66,112]],[.82,[176,118,128]],[1,[244,184,132]]],star:.3,mw:.3,cTop:[120,96,140],cBot:[80,62,104],warm:[255,170,110],rim:[110,70,60],haze:[150,110,126],front:[44,38,70],side:[32,28,54],top:[70,60,96],ground:[40,34,60],water:[150,112,130],label:'해질녘'}};
function scene(cv,W,H,tk,lives,met,V,O){const Y=tk==='y';const T=Object.assign({},TIME[tk],V.T||{}),c=cv.getContext('2d'),S=2,wide=W>H,KX=wide?1.9:1,KA=wide?1.35:1,KY=wide?2.1:1,KS=wide?1.6:1,CX=W/2,HZ=wide?Math.round(H*.60):536,FY=wide?H-160:620;cv.width=W*S;cv.height=H*S;
 const lit=Math.pow(Math.min(1,Math.sqrt(lives)/12.3),1.35),q=Math.min(1,met/135),gl=Math.min(1,lit*1.3);
 // 1) 하늘: 마련한 그림을 깔고(세로 화면은 가운데를 잘라, 가로 화면은 폭에 맞춰), 구름이 없는 어두운 자리에만 별을 얹는다
 const w=W*S,h=(HZ+6)*S,o=document.createElement('canvas');o.width=w;o.height=h;const oc=o.getContext('2d'),A=new Float32Array(w*h),Im=new Float32Array(w*h),im2=IMGS[tk==='y'?V.img[0].replace('sky','day'):V.img[0]],ar=w/h;
 let sw2,sh2,sx2,sy2;if(im2.width/im2.height>ar){sh2=im2.height;sw2=sh2*ar;sx2=Math.max(0,Math.min(im2.width-sw2,V.img[1]*im2.width-V.img[2]*sw2));sy2=0}else{sw2=im2.width;sh2=sw2/ar;sx2=0;sy2=(im2.height-sh2)*V.img[3]}
 oc.drawImage(im2,sx2,sy2,sw2,sh2,0,0,w,h);if(O)O.crop=[sx2,sy2,sw2,sh2];const MOON=V.moonImg?[(V.moonImg*im2.width-sx2)/sw2*W,0,0]:null;
 { const dd=oc.getImageData(0,0,w,h).data,row=new Float32Array(w);for(let yy=0;yy<h;yy++){for(let xx=0;xx<w;xx++){const p=(yy*w+xx)*4;row[xx]=dd[p]*.3+dd[p+1]*.59+dd[p+2]*.11}const srt=Array.from(row).sort((a,b)=>a-b),base=srt[w*.12|0],low=sst(.50,.64,yy/h);for(let xx=0;xx<w;xx++)A[yy*w+xx]=Math.max(low,sst(2.5,8,row[xx]-base))}
  // 시간대: 같은 그림에 색만 덧입힌다
  const GR=(op,stops)=>{const g2=oc.createLinearGradient(0,0,0,h);stops.forEach(([o2,c2])=>g2.addColorStop(o2,c2));oc.globalCompositeOperation=op;oc.fillStyle=g2;oc.fillRect(0,0,w,h);oc.globalCompositeOperation='source-over'};
  if(tk==='n'||tk==='y'){}
  else if(tk==='d'){GR('screen',[[0,'rgba(46,70,128,.62)'],[.5,'rgba(86,120,170,.60)'],[1,'rgba(150,130,110,.50)']]);GR('soft-light',[[.3,'rgba(255,214,150,0)'],[.78,'rgba(255,214,150,.75)'],[1,'rgba(255,236,190,1)']]);GR('screen',[[.72,'rgba(255,214,150,0)'],[1,'rgba(255,220,160,.62)']])}
  else{GR('screen',[[0,'rgba(60,34,86,.42)'],[.55,'rgba(120,50,70,.46)'],[1,'rgba(150,70,40,.50)']]);GR('overlay',[[.25,'rgba(255,96,70,0)'],[.72,'rgba(255,96,70,.55)'],[1,'rgba(255,150,60,.85)']]);GR('screen',[[.76,'rgba(255,130,60,0)'],[1,'rgba(255,150,80,.62)']])}
  const dk=oc.createLinearGradient(0,0,0,h);dk.addColorStop(0,`rgba(4,8,22,${Y?0:.42*(1-q)})`);dk.addColorStop(1,'rgba(4,8,22,0)');oc.fillStyle=dk;oc.fillRect(0,0,w,h) }
 if(q>0&&!Y){const so=O?(O.small=document.createElement('canvas'),O.small.width=w,O.small.height=h,O.small.getContext('2d')):oc;const R=rnd(21),SC=['#ffffff','#dbe6ff','#c9dcff','#fff1dc','#bfd6ff'],inB=(x,y)=>{const dx=x-MX,dy=y-MY,v=-dx*sa+dy*ca;return Math.exp(-(v*v)/6400)};
  for(let i=0;i<70000*W/390;i++){const x=R()*w|0,y=R()*h|0;if(R()>(.06+.55*cl(Im[y*w+x]*2.4))*Math.pow(q,.7))continue;const cov=A[y*w+x];if(cov>.3)continue;const m=Math.pow(R(),10),a=cl(.25+.55*R()+m)*T.star*(1-cov*3)*(1-.6*cl((y/S-HZ+80)/80));so.fillStyle=SC[R()*5|0];
   if(m>.82){const r=1.2+(m-.82)*7;so.globalAlpha=.12*T.star;so.beginPath();so.arc(x,y,r*2.6,0,7);so.fill();so.globalAlpha=a;so.beginPath();so.arc(x,y,r*.6,0,7);so.fill()}else if(R()<.12){so.globalAlpha=a*.5;so.fillRect(x,y,2,2)}else{so.globalAlpha=a*.85;so.fillRect(x,y,1,1)}}
  const R3=rnd(77),tint=['#dfeaff','#ffe3c4','#cdeeff','#fff1c9','#e3d8ff','#d6e2ff','#ffd6d1'];
  for(let i=0;i<met;i++){const x=(8+R3()*(W-16))*S|0,y=(40+R3()*(HZ-150))*S|0,m=Math.pow(R3(),2.4),r=(.9+m*1.5)*S,k=tint[i%7];if(A[y*w+x]>.2)continue;if(O){O.big.push([x/S,y/S,r/S,i%7,m]);continue}
   const g2=oc.createRadialGradient(x,y,0,x,y,r*4.5);g2.addColorStop(0,k+'cc');g2.addColorStop(.14,k+'40');g2.addColorStop(1,k+'00');oc.globalAlpha=.75*T.star;oc.fillStyle=g2;oc.fillRect(x-r*5,y-r*5,r*10,r*10);oc.globalAlpha=T.star;oc.fillStyle='#fff';oc.beginPath();oc.arc(x,y,r*.6,0,7);oc.fill();
   if(m>.28){const Lh=r*4.6;for(const[ax,ay] of [[1,0],[0,1]]){const fl=oc.createLinearGradient(x-Lh*ax,y-Lh*ay,x+Lh*ax,y+Lh*ay);fl.addColorStop(0,k+'00');fl.addColorStop(.5,k+'cc');fl.addColorStop(1,k+'00');oc.strokeStyle=fl;oc.lineWidth=1;oc.beginPath();oc.moveTo(x-Lh*ax,y-Lh*ay);oc.lineTo(x+Lh*ax,y+Lh*ay);oc.stroke()}}}
  oc.globalAlpha=1}
 if(O)O.sky=o;else c.drawImage(o,0,0);c.scale(S,S);
 if(Y){const RB=rnd(41),nb=Math.round(met*.42),fl=[[.30,.50],[.66,.38],[.52,.66],[.16,.72],[.84,.62]];c.lineCap='round';for(let i=0;i<nb;i++){const f=fl[i%fl.length],x=W*f[0]+(RB()+RB()+RB()-1.5)*W*.13,y=HZ*f[1]+(RB()+RB()-1)*HZ*.09,sz=(2.2+RB()*3.2)*(wide?1.5:1),fp=.25+RB()*.5,tl=(RB()-.5)*.5;c.save();c.translate(x,y);c.rotate(tl);c.strokeStyle='rgba(30,52,96,.55)';c.lineWidth=sz*.26;c.beginPath();c.moveTo(-sz,-sz*fp+.6);c.quadraticCurveTo(-sz*.45,-sz*fp*1.5+.6,0,.6);c.quadraticCurveTo(sz*.45,-sz*fp*1.5+.6,sz,-sz*fp+.6);c.stroke();c.strokeStyle='#ffffff';c.lineWidth=sz*.22;c.beginPath();c.moveTo(-sz,-sz*fp);c.quadraticCurveTo(-sz*.45,-sz*fp*1.5,0,0);c.quadraticCurveTo(sz*.45,-sz*fp*1.5,sz,-sz*fp);c.stroke();c.restore()}}
 // 2) 산줄기 세 겹. 도시는 가장 앞 산줄기 너머 들판에 멀리 깔린다
 const R=rnd(5),D=tk!=='n',RC=tk==='y'?['#7f9fc6','#6687b2','#4f7098','#5f8a6e']:tk==='e'?['#573c63','#44304f','#32243d','#271b31']:D?['#4a4670','#39355a','#2a2745','#211e38']:(V.RC||['#101c33','#0b1526','#070e1b','#050a14']),RG=V.ridges;
 const rY0=(x,base,amp,f,sd)=>L(HZ+3,HZ+(base-HZ)*KA-amp*KA*(fbm(x*f+sd,sd,5)-.35)-amp*KA*.5*Math.max(0,Math.sin(x*f*2.2+sd)),V.fade?V.fade(x):1),rY=(sxp,base,amp,f,sd)=>rY0((sxp-CX)/KX+195,base,amp,f,sd),ridge=(base,amp,f,sd,col)=>{c.fillStyle=col;c.beginPath();c.moveTo(0,H);for(let x=0;x<=W;x+=2)c.lineTo(x,rY(x,base,amp,f,sd));c.lineTo(W,H);c.fill()};
 ridge(HZ+RG[0][0],RG[0][1],RG[0][2],RG[0][3],RC[0]);
 { const m=c.createLinearGradient(0,HZ-8,0,HZ+22);m.addColorStop(0,'rgba(120,150,200,0)');m.addColorStop(1,`rgba(${T.warm[0]},${T.warm[1]},${T.warm[2]},${.10+.16*lit})`);c.fillStyle=m;c.fillRect(0,HZ-8,W,30) }   // 산 사이의 안개: 도시 불빛을 받는다
 ridge(HZ+RG[1][0],RG[1][1],RG[1][2],RG[1][3],RC[1]);ridge(HZ+RG[2][0],RG[2][1],RG[2][2],RG[2][3],RC[2]);
 const Y0=HZ+33*KA,YD=64*KY,VX=205,XL=VX-(CX+10*KX+16)/(KX*.82),XR=VX+(W-CX-10*KX+16)/(KX*.82);c.fillStyle=RC[3];c.fillRect(0,Y0+3,W,H);
 // 들판 위의 자리: t=0은 먼 곳, t=1은 가까운 곳. 가까울수록 크게 그린다
 const at=(x,t)=>[CX+10*KX+(x-VX)*(.82+.36*t)*KX,Y0+4+Math.pow(t,1.25)*YD,(.55+1.05*t)*KS];
 const CL=V.CL;   // 도시 덩어리: x, 깊이, 가로 퍼짐, 깊이 퍼짐, 크기
 const dn=(x,t)=>{let d=0;for(const[cx,ct,sx,st,wt] of CL)d=Math.max(d,wt*Math.exp(-(Math.pow((x-cx)/sx,2)+Math.pow((t-ct)/st,2))));return d};
 // 호수: 들판 왼쪽 아래의 어두운 물
 const lake=V.wet;
 { c.fillStyle=tk==='y'?'#4f86c4':D?'#5a5484':V.wc;for(let t=0;t<=1;t+=.008){const p=at(0,t),hh=at(0,t+.008)[1]-p[1]+.4;let x0=null;for(let x=XL;x<=XR;x+=1.5){const w2=lake(x,t);if(w2&&x0===null)x0=x;if((!w2||x>=XR-1.5)&&x0!==null){const a2=at(x0,t)[0],b2=at(x,t)[0];c.fillRect(a2,p[1],b2-a2,hh);x0=null}}} }
 if(V.sea)V.sea(c,{HZ,Y0,W,H,at,D,MOON,R,T,Y,O,CX,KX});
 // 3) 도시: 가지런한 줄 위에 건물을 세운다. 먼 줄부터 그린다
 const lc=document.createElement('canvas');lc.width=W*S;lc.height=H*S;const lx=lc.getContext('2d');lx.scale(S,S);lx.lineCap='round';
 const on=Y?.55:Math.min(1,lit*2.6),grow=Y?.16+.84*lit:1,AMB='#ffc46e',snap=v=>Math.round(v*S)/S;
 const path=(fn,n,wd,a,col,over)=>{lx.strokeStyle=col;lx.globalAlpha=a*.40;let pv=null;for(let i=0;i<=n;i++){const q2=fn(i/n),ok=(over||!lake(q2[0],q2[1]))&&q2[1]>=0&&q2[1]<=1.02,p=at(q2[0],q2[1]);if(pv&&ok&&pv[3]){lx.lineWidth=wd*p[2];lx.beginPath();lx.moveTo(pv[0],pv[1]);lx.lineTo(p[0],p[1]);lx.stroke()}pv=[p[0],p[1],p[2],ok]}};
 const dot=(x,t,r,col,a)=>{const p=at(x,t);lx.globalAlpha=a*.6;lx.fillStyle=col;lx.beginPath();lx.arc(p[0],p[1],r*p[2],0,7);lx.fill()};
 const bez=P=>u=>{const m=1-u;return[m*m*P[0]+2*m*u*P[2]+u*u*P[4],m*m*P[1]+2*m*u*P[3]+u*u*P[5]]};
 // 골목: 도시 안쪽에만 옅게 깔리는 바둑판 길
 const NR=42,DXS=6.4;
 if(!V.nogrid){for(let i=1;i<NR;i+=3){const t=i/NR;for(let x=XL;x<XR;x+=DXS){const d=dn(x+DXS/2,t);if(d<.2||lake(x,t)||lake(x+DXS,t))continue;const a2=at(x,t),b2=at(x+DXS,t);lx.strokeStyle='#ff9a4a';lx.globalAlpha=.09*on*Math.min(1,d*1.4);lx.lineWidth=.4*a2[2];lx.beginPath();lx.moveTo(a2[0],a2[1]);lx.lineTo(b2[0],b2[1]);lx.stroke()}}
  for(let x=XL+DXS*2;x<XR;x+=DXS*4)for(let i=0;i<NR;i++){const t=i/NR,d=dn(x,t+.5/NR);if(d<.2||lake(x,t)||lake(x,t+1/NR))continue;const a2=at(x,t),b2=at(x,t+1/NR);lx.strokeStyle='#ff9a4a';lx.globalAlpha=.12*on*Math.min(1,d*1.4);lx.lineWidth=.45*a2[2];lx.beginPath();lx.moveTo(a2[0],a2[1]);lx.lineTo(b2[0],b2[1]);lx.stroke()}}
 // 큰길: 끊기지 않는 가는 불빛 줄
 for(const r of V.roads){path(bez(r[0]),40,2.2,.07*on,'#ff9a4a',r[0][6]);path(bez(r[0]),40,.55,.42*on,'#ffac5c',r[0][6])}
 const bcol=tk==='y'?[176,190,210]:tk==='e'?[74,52,84]:D?[62,56,96]:(V.bc||[13,20,36]);
 const build=(x,t,wd,ht,tone,tall)=>{const p=at(x,t),sc=p[2],w2=snap(Math.max(1.5,wd*sc)),h2=snap(Math.max(1,ht*sc*.62)),x0=snap(p[0]-w2/2),y0=snap(p[1]-h2),k=1+.45*tone;
  c.fillStyle=Y?rgb([Math.min(255,bcol[0]*(.86+.3*tone)+18*tone),Math.min(255,bcol[1]*(.86+.3*tone)+8*tone),Math.min(255,bcol[2]*(.86+.26*tone))]):rgb([bcol[0]*k,bcol[1]*k,bcol[2]*k]);c.fillRect(x0,y0,w2,h2);c.fillStyle=Y?rgb([88+30*tone,112+26*tone,156+20*tone]):rgb([bcol[0]*k*.62,bcol[1]*k*.62,bcol[2]*k*.66]);c.fillRect(x0+w2*.72,y0,w2*.28,h2);if(Y){c.fillStyle='rgba(60,90,140,.30)';for(let yy=y0+1.2;yy<y0+h2-.6;yy+=1.6)c.fillRect(x0+.3,snap(yy),w2*.72-.6,.5)}c.fillStyle=rgb([bcol[0]*k*1.9+8,bcol[1]*k*1.9+10,bcol[2]*k*1.8+14]);c.fillRect(x0,y0,w2*.72,.5);
  if(tall){c.fillStyle=rgb([bcol[0]*k,bcol[1]*k,bcol[2]*k]);c.fillRect(snap(p[0]-w2*.25),y0-snap(h2*.13),snap(w2*.5),snap(h2*.13));c.fillRect(p[0]-.3,y0-h2*.13-5*sc,.6,5*sc);lx.globalAlpha=.4+.6*on;lx.fillStyle='#ff6a6a';lx.beginPath();lx.arc(p[0],y0-h2*.13-5*sc,.8,0,7);lx.fill()}
  // 창: 칸을 맞춰 가지런히. 켜진 창은 절반을 넘지 않는다
  const cols=w2>=5?3:w2>=3?2:1,rows=Math.max(1,Math.floor((h2-.6)/1.6)),cw=(w2*.72-.6)/cols,lf=Y?0:Math.min(.72,lit*(.42+.6*R())),col=tone>.86?'#bfe2ff':AMB;lx.fillStyle=col;
  for(let j=0;j<rows;j++)for(let i=0;i<cols;i++)if(R()<lf){const wa=.85+R()*.15,wx=snap(x0+.35+i*cw),wy=snap(y0+.6+j*1.6),ww=Math.max(.6,snap(cw-.3));if(O)O.win.push([wx,wy,ww,1.05,col,wa]);else{lx.globalAlpha=wa;lx.fillRect(wx,wy,ww,1.05)}}};
 const SP=V.tw.slice().sort((a,b)=>a[1]-b[1]);let si=0;
 for(let i=0;i<=NR;i++){const t=(i+.5)/NR;while(si<SP.length&&SP[si][1]<=t){const q2=SP[si++];build(q2[0],q2[1],q2[2],q2[3],q2[4],1)}
  for(let x=XL+(i%2)*DXS/2;x<XR;x+=DXS){const xx=x+(R()-.5)*1.2,d=dn(xx,t),r1=R(),r2=R(),r3=R();if(lake(xx,t)||lake(xx+3,t)||lake(xx-3,t)||r1>(.20+d*1.4)*grow)continue;const core=Math.pow(d,1.7);build(xx,t,3.3+core*1.3,(1.4+r2*1.5)+core*(5+Math.pow(r2,1.6)*30)*V.th+(r3<.05?3+r3*90:0),r3,0)}}
 if(V.extra)V.extra({lx,at,lit,on,R,lake,path,dot,bez,O});
 for(let i=0;i<26;i++){if(R()>lit*1.6)continue;const x=R()*W,yy=rY(x,HZ+RG[2][0],RG[2][1],RG[2][2],RG[2][3])+2+R()*6;lx.globalAlpha=.6;lx.fillStyle=AMB;lx.beginPath();lx.arc(x,yy,.45,0,7);lx.fill()}      // 산비탈의 드문 불빛
 for(const[cx,ct,sx,st,wt] of CL){const p=at(cx,ct),g3=c.createRadialGradient(p[0],p[1],0,p[0],p[1],sx*1.7*KX);g3.addColorStop(0,`rgba(255,180,100,${Y?0:.24*lit*wt})`);g3.addColorStop(1,'rgba(255,180,100,0)');c.save();c.translate(p[0],p[1]);c.scale(1,.36);c.translate(-p[0],-p[1]);c.globalCompositeOperation='lighter';c.fillStyle=g3;c.fillRect(p[0]-sx*1.7*KX,p[1]-sx*1.7*KX,sx*3.4*KX,sx*3.4*KX);c.restore()}
 if(O){O.lights=lc}else{c.save();c.setTransform(1,0,0,1,0,0);if(Y){c.filter='grayscale(1) brightness(1.7)';c.globalAlpha=.8;c.drawImage(lc,0,0);c.filter='none'}else{c.globalCompositeOperation='lighter';c.filter='blur(5px)';c.globalAlpha=.5;c.drawImage(lc,0,0);c.filter='blur(1px)';c.globalAlpha=.35;c.drawImage(lc,0,0);c.filter='none';c.globalCompositeOperation='source-over';c.globalAlpha=1;c.drawImage(lc,0,0)}c.restore()}
 if(V.fg)V.fg(c,W,HZ,RC,fbm,KX,H);
 if(O){O.at=at;O.HZ=HZ;O.MOON=MOON;O.lit=lit;O.wide=wide}
 // 5) 글자 자리를 위한 어둠
 const f=c.createLinearGradient(0,FY,0,FY+34);f.addColorStop(0,'rgba(18,16,25,0)');f.addColorStop(1,'#121019');c.fillStyle=f;c.fillRect(0,FY,W,36);c.fillStyle='#121019';c.fillRect(0,FY+34,W,H);
 const f2=c.createLinearGradient(0,0,0,230);f2.addColorStop(0,`rgba(3,6,16,${Y?.16:.5})`);f2.addColorStop(1,'rgba(3,6,16,0)');c.fillStyle=f2;c.fillRect(0,0,W,230);}
// ① 산 너머 들판의 도시: 왼쪽 앞에 호수
const lk=(x,t)=>Math.pow((x-150)/78,2)+Math.pow((t-.72)/.13,2)<1;
const VL={img:['sky1.png',.5,.5,1],ang:-.62,mx:292,my:400,mc:[96,128,196],tl:[4,36,54],mag:1,cf:[.006,.05],bank:(x,y,HZ)=>Math.exp(-Math.pow((y-(HZ-30))/20,2))*sst(350,60,x)*.9,
 ridges:[[-6,44,.011,3],[10,34,.016,8],[30,20,.022,14]],wet:lk,wc:'#0c1c38',th:1,
 CL:[[300,.30,74,.20,1],[98,.36,50,.15,.62],[262,.74,40,.12,.42],[352,.78,34,.11,.34],[30,.44,30,.12,.26]],
 tw:[[292,.30,4.6,50,.9,2],[318,.34,4.2,42,.3,2],[96,.36,4,28,.6,2]],
 roads:[[[300,.30,200,.28,98,.36]],[[300,.30,310,.5,352,.78]],[[98,.36,50,.4,30,.44]],[[300,.30,290,.5,262,.74]],[[262,.74,250,.9,200,1.0]],[[78,.72,150,.71,226,.72,1]],[[98,.36,60,.52,74,.72]]],
 extra:({dot,on})=>{for(let i=0;i<=14;i++)dot(78+i*10.6,.72-.01*Math.sin(i/14*3.14),.5,'#ffe2ac',.95*on)}};
// ② 강을 낀 큰 도시: 넓은 강이 굽이쳐 지평선의 바다로 나간다
const xr=t=>232+92*Math.sin(t*3.6+.5)+70*Math.pow(1-t,3),wr=t=>10+16*t+30*Math.pow(1-t,6);
const VR={img:['sky2.png',.66,.6,1],ang:-1.05,mx:215,my:215,mc:[96,128,196],tl:[4,36,54],mag:.4,cf:[.013,.03],mws:.55,deck:1,sd:2,bank:()=>0,
 T:{sky:[[0,[3,9,28]],[.4,[9,28,72]],[.78,[26,66,128]],[1,[84,124,176]]],warm:[255,170,110]},
 ridges:[[-4,22,.011,3],[8,14,.016,8],[26,7,.022,14]],wet:(x,t)=>Math.abs(x-xr(t))<wr(t),wc:'#12305a',th:1.25,
 CL:[[xr(.30)-70,.30,62,.15,.95],[xr(.30)+76,.26,48,.12,.6],[xr(.62)+70,.62,50,.13,.55],[xr(.62)-78,.66,46,.12,.5],[50,.34,46,.16,.36],[352,.86,48,.12,.36],[100,.92,50,.10,.32]],
 tw:[[xr(.30)-64,.30,5,58,.9,2],[xr(.30)-90,.33,4.4,46,.3,2],[xr(.30)+72,.27,4.4,40,.6,2],[xr(.62)+66,.62,4,34,.2,2]],
 roads:[[[xr(.30)-70,.30,150,.45,xr(.62)-78,.66]],[[xr(.30)+76,.26,340,.44,xr(.62)+70,.62]],[[50,.34,110,.3,xr(.30)-70,.30]],[[xr(.62)+70,.62,345,.74,352,.86]],[[xr(.62)-78,.66,120,.78,100,.92]],[[-10,.55,60,.45,50,.34]]],
 extra:({path,dot,on,R})=>{for(const t of [.14,.24,.36,.50,.64,.80,.93]){path(u=>[xr(t)-wr(t)-3+u*(wr(t)*2+6),t],12,.7,.75*on,'#ffdca0',1);const n=Math.round(wr(t)/3)+2;for(let i=0;i<=n;i++)dot(xr(t)-wr(t)-3+i*(wr(t)*2+6)/n,t,.5,'#fff0d0',.95*on)}
  for(let i=0;i<7;i++){const t=.22+i*.11,x=xr(t)+(R()-.5)*wr(t)*.8;dot(x,t,.55,i%2?'#9fd8ff':'#ffe2ac',.9*on);dot(x+2,t,.4,'#ff8f6a',.8*on)}}};
// ③ 항구 도시: 왼쪽은 산, 오른쪽은 수평선까지 바다. 초승달처럼 휜 만을 따라 불빛이 깔린다
const cst=t=>196+150*Math.pow(Math.abs(t-.46)*1.9,1.7)+(fbm(t*7+2,5,3)-.5)*20+(fbm(t*23+9,1,2)-.5)*7;
const VH={img:['sky3.png',.724,.76,.28],moonImg:.724,ang:-1.12,mx:150,my:330,mc:[70,130,180],tl:[2,44,50],mag:.3,cf:[.006,.05],bank:(x,y,HZ)=>Math.exp(-Math.pow((y-(HZ-34))/22,2))*sst(230,20,x)*.9,fade:x=>sst(330,110,x),moon:[306,128,13],
 ridges:[[-6,44,.011,3],[10,34,.016,8],[30,20,.022,14]],wet:(x,t)=>x>cst(t),wc:'#0a1a36',th:1,
 CL:[[cst(.22)-52,.22,62,.15,1],[cst(.50)-36,.50,40,.12,.6],[cst(.84)-70,.84,56,.11,.6],[60,.34,44,.14,.36],[40,.70,34,.12,.3]],
 tw:[[cst(.22)-60,.22,4.8,48,.9,2],[cst(.22)-34,.25,4.2,38,.3,2],[cst(.84)-80,.84,4,28,.6,2]],
 roads:[[[cst(.22)-52,.22,90,.26,60,.34]],[[60,.34,30,.5,40,.70]],[[cst(.5)-36,.5,110,.56,40,.70]],[[40,.70,90,.9,cst(.84)-70,.84]]],
 sea:(c,{HZ,Y0,W,H,at,D,MOON,R,T,Y,O,CX,KX})=>{const p0=at(cst(0),0),xe=CX+(326-195)*KX,pts=[];for(let t=0;t<=1.001;t+=.01)pts.push(at(cst(t),t));
   const shore=()=>{c.beginPath();c.moveTo(xe,HZ+3);c.bezierCurveTo(xe-15*KX,HZ+3.2,p0[0]+31*KX,p0[1]-25,p0[0]+12*KX,p0[1]-9);c.quadraticCurveTo(p0[0]+1,p0[1]-2,p0[0],p0[1]);for(const p of pts)c.lineTo(p[0],p[1])};
   c.save();shore();c.lineTo(W+4,H);c.lineTo(W+4,HZ+1);c.closePath();c.clip();
   const sg=c.createLinearGradient(0,HZ,0,HZ+110);sg.addColorStop(0,Y?'#9fd0f2':D?'#c79aa2':'#2a547e');sg.addColorStop(.22,Y?'#4f96d8':D?'#7a6a96':'#143258');sg.addColorStop(1,Y?'#2f6fb4':D?'#3c3660':'#0a1a36');c.fillStyle=sg;c.fillRect(0,HZ,W,H);
   for(let i=0;i<140;i++){const yy=HZ+1+Math.pow(R(),1.3)*100;c.globalAlpha=.04+R()*.07;c.fillStyle=R()<.5?'#04101f':'#a9c6ee';c.fillRect(R()*W,yy,10+R()*40,.7)}
   if(T.star>.6)for(let i=0;i<120;i++){const yy=HZ+1+Math.pow(R(),1.25)*100,ww=(3+(yy-HZ)*.6)*(.4+R()),ga=.2+R()*.5,gx=MOON[0]-ww/2+(R()-.5)*(yy-HZ)*.5;if(O&&c.isPointInPath((gx+ww/2)*2,yy*2))O.glit.push([gx,yy,ww,ga]);c.globalAlpha=O?ga*.4:ga;c.fillStyle='#fff4d6';c.fillRect(gx,yy,ww,.8)}
   // 물가: 얕은 물이 뭍 쪽으로 갈수록 옅게 밝아지고, 물결이 해안선을 따라 몇 겹 밀려온다
   c.globalAlpha=1;c.lineJoin='round';c.lineCap='round';shore();c.filter='blur(7px)';c.strokeStyle=Y?'rgba(190,230,250,.5)':'rgba(96,150,214,.22)';c.lineWidth=15*KX;c.stroke();c.filter='blur(2.5px)';c.strokeStyle=Y?'rgba(220,244,255,.5)':'rgba(140,190,240,.17)';c.lineWidth=4.5*KX;c.stroke();c.filter='none';
   for(const[off,al] of [[3.2,.20],[6.4,.12],[10.5,.07]]){c.beginPath();let pen=0;pts.forEach((p,i)=>{const n=fbm(i*.21+off,3,2),x=p[0]+off*KX*(.7+.5*p[2])+ (n-.5)*3,y=p[1]+.6;if(n<.42){pen=0;return}pen?c.lineTo(x,y):c.moveTo(x,y);pen=1});c.strokeStyle=`rgba(200,224,250,${al})`;c.lineWidth=.6;c.stroke()}
   c.restore();
   // 뭍 쪽 가장자리: 젖은 모래톱처럼 한 줄 어둡게, 그 위에 아주 가는 흰 선
   const edge=()=>{c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]))};c.save();edge();c.strokeStyle='rgba(2,6,14,.55)';c.lineWidth=2.2;c.stroke();edge();c.strokeStyle=Y?'rgba(255,255,255,.5)':'rgba(170,200,235,.22)';c.lineWidth=.5;c.stroke();
   const hz=c.createLinearGradient(0,HZ-3,0,HZ+5);hz.addColorStop(0,'rgba(150,180,220,0)');hz.addColorStop(.5,'rgba(150,180,220,.20)');hz.addColorStop(1,'rgba(150,180,220,0)');c.fillStyle=hz;c.fillRect(xe,HZ-3,W-xe,8);c.restore()},
 extra:({lx,at,path,dot,on,R,O})=>{path(u=>[cst(u)-5,u],80,2.2,.07*on,'#ff9a4a');path(u=>[cst(u)-5,u],80,.55,.42*on,'#ffac5c');
  for(const t of [.16,.24,.33,.47,.56,.78,.88]){const len=34+((t*97)%1)*20;path(u=>[cst(t)+1+u*len,t],6,.7,.7*on,'#ffdca0',1);for(let i=1;i<=4;i++)dot(cst(t)+1+i*len/4,t,.45,i===4?'#ff7a6a':'#fff0d0',.95*on)}
  for(let i=0;i<8;i++){const t=.1+i*.11,x=cst(t)+70+((i*53)%120);dot(x,t,.55,i%2?'#ffe2ac':'#9fd8ff',.9*on);dot(x+2.2,t,.4,'#ff8f6a',.8*on)}
  const p=at(cst(.02)+2,.02);lx.globalAlpha=1;lx.fillStyle='#c8d2e6';lx.fillRect(p[0]-.8,p[1]-8,1.6,8);if(O){O.lh=[p[0],p[1]-8.5]}else{const bg=lx.createLinearGradient(p[0],p[1]-8,p[0]+90,p[1]-4);bg.addColorStop(0,'rgba(255,244,200,.5)');bg.addColorStop(1,'rgba(255,244,200,0)');lx.fillStyle=bg;lx.beginPath();lx.moveTo(p[0],p[1]-8.5);lx.lineTo(p[0]+92,p[1]-12);lx.lineTo(p[0]+92,p[1]+3);lx.fill()}lx.fillStyle='#fff6d8';lx.beginPath();lx.arc(p[0],p[1]-8.5,1.2,0,7);lx.fill()}};
// ④ 분지의 도시: 높은 산이 둘러싼 둥근 도시. 길이 고리와 바큇살로 퍼진다
const bx=t=>60+300*t+18*Math.sin(t*9);
const VB={img:['sky4.png',.36,.5,1],ang:-.16,mx:200,my:300,mc:[124,104,196],tl:[30,10,46],mag:1.5,cf:[.012,.03],bank:(x,y,HZ)=>Math.exp(-Math.pow((y-(HZ-72))/34,2))*sst(210,370,x)*.9,nogrid:1,
ridges:[[-10,78,.009,5],[8,52,.015,11],[28,26,.021,17]],wet:(x,t)=>Math.abs(x-bx(t))<2.4+3.2*t,wc:'#12244a',th:.42,
 CL:[[200,.50,92,.26,.85],[60,.16,30,.08,.3],[350,.20,30,.08,.3],[40,.92,36,.08,.28],[366,.9,34,.08,.28]],
 tw:[[196,.47,3.4,32,.3,2],[226,.53,3,26,.9,2],[170,.55,3,24,.6,2]],roads:[],
 extra:({path,dot,on,bez})=>{
  // 고리 길은 네 겹만, 조금씩 찌그러지고 군데군데 끊긴다
  const RING=[[1.0,[[.02,.46],[.52,.98]]],[2.1,[[.05,.34],[.40,.71],[.76,1.0]]],[3.5,[[.0,.22],[.30,.58],[.66,.93]]],[5.1,[[.08,.30],[.44,.62],[.72,.90]]]];
  for(const[k,segs] of RING){const f=u=>{const a=u*6.283,w=1+.07*Math.sin(a*3+k*1.7)+.04*Math.sin(a*5+k);return[200+Math.cos(a)*27*k*w,.50+Math.sin(a)*.078*k*w]};
   for(const[u0,u1] of segs){const g=u=>f(u0+(u1-u0)*u),n=Math.round(90*(u1-u0))+4;path(g,n,2,.06*on,'#ff9a4a',1);path(g,n,.55,(k<3?.46:.34)*on,'#ffad5c',1)}}
  // 바큇살은 아홉 가닥, 길이가 제각각이고 조금 휜다
  [[.12,.06,1],[.82,.10,.72],[1.45,.04,.95],[2.2,.30,.8],[2.9,.05,1],[3.55,.12,.66],[4.2,.03,.92],[4.9,.26,.85],[5.6,.08,.75]].forEach(([a,s0,s1],j)=>{const bend=(j%2?1:-1)*.10;path(u=>{const rr=(s0+(s1-s0)*u)*150,aa=a+bend*u;return[200+Math.cos(aa)*rr,.50+Math.sin(aa)*rr*.0029]},26,.5,.30*on,'#ffad5c',1)});
  // 고리를 가로지르는 옛길 둘
  path(bez([70,.22,190,.40,330,.30]),30,.5,.28*on,'#ffad5c',1);path(bez([90,.86,220,.62,350,.78]),30,.5,.28*on,'#ffad5c',1);
  for(const t of [.3,.46,.6,.76])for(let i=-2;i<=2;i++)dot(bx(t)+i*2.2,t,.45,'#fff0d0',.9*on)},
 fg:(c,W,HZ,RC,fbm,k,H2)=>{c.fillStyle=RC[3];for(const side of [0,1]){c.beginPath();c.moveTo(side?W+4:-4,H2);for(let i=0;i<=50;i++){const u=i/50,x=side?W+4-u*96*k:-4+u*96*k,y=HZ+78*k+Math.pow(u,1.6)*40*k-14*k*(1-u)*(.5+fbm(x*.04/k+side*9,4,4));c.lineTo(x,y)}c.lineTo(side?W-96*k:96*k,H2);c.fill()}}};

const BOARDS=[{V:VL,f:'sky1'},{V:VR,f:'sky2'},{V:VH,f:'sky3'},{V:VB,f:'sky4'}];
const bezf=P=>u=>{const m=1-u;return[m*m*P[0]+2*m*u*P[2]+u*u*P[4],m*m*P[1]+2*m*u*P[3]+u*u*P[5]]};
const qs=s=>document.querySelector(s),RM=matchMedia('(prefers-reduced-motion: reduce)').matches,K_B='cupnight.lobby.board';
const IMGS={};let stage=null,Lr=null,raf=0,T0=0,lives=0,met=0,BI=0,active=false,SPR=null,tok=0;
const mk=(w,h,cls)=>{const c=document.createElement('canvas');c.width=w;c.height=h;if(cls)c.className=cls;return c};
const TINT=['#dfeaff','#ffe3c4','#cdeeff','#fff1c9','#e3d8ff','#d6e2ff','#ffd6d1'];
// 별 그림: 빛깔마다 한 번만 그려 두고 찍어 쓴다 (빛살이 있는 것 / 없는 것)
const mkSpr=()=>TINT.map(k=>[0,1].map(fl=>{const c=mk(96,96),x=c.getContext('2d'),g=x.createRadialGradient(48,48,0,48,48,43);g.addColorStop(0,k+'cc');g.addColorStop(.14,k+'40');g.addColorStop(1,k+'00');x.globalAlpha=.75;x.fillStyle=g;x.fillRect(0,0,96,96);x.globalAlpha=1;x.fillStyle='#fff';x.beginPath();x.arc(48,48,5.6,0,7);x.fill();
  if(fl)for(const[ax,ay] of [[1,0],[0,1]]){const f=x.createLinearGradient(48-44*ax,48-44*ay,48+44*ax,48+44*ay);f.addColorStop(0,k+'00');f.addColorStop(.5,k+'cc');f.addColorStop(1,k+'00');x.strokeStyle=f;x.lineWidth=1.6;x.beginPath();x.moveTo(48-44*ax,48-44*ay);x.lineTo(48+44*ax,48+44*ay);x.stroke()}return c}));
// 로비에 들어올 때마다 네 판 가운데 하나. 직전 판은 연달아 나오지 않는다
function pick(){let last=-1;try{last=+(localStorage.getItem(K_B)??-1)}catch(e){}let i=Math.floor(Math.random()*4);if(i===last)i=(i+1+Math.floor(Math.random()*3))%4;try{localStorage.setItem(K_B,i)}catch(e){}return i}
function build(){cancelAnimationFrame(raf);if(!active)return;const vw=innerWidth,vh=innerHeight,wide=vw/vh>1.15,W=wide?1440:390,H=wide?900:800,SA=wide?1:2;
 const B=BOARDS[BI],V=B.V,ground=mk(1,1,'lay'),O={big:[],win:[],glit:[]};scene(ground,W,H,'n',lives,met,V,O);
 const HS=O.HZ+6,skyg=document.createElement('div');skyg.className='skyg';skyg.style.cssText=`width:${W}px;height:${HS}px`;
 O.sky.className='lay';skyg.appendChild(O.sky);if(O.small){O.small.className='lay small';skyg.appendChild(O.small)}
 const star=mk(W*SA,HS*SA,'lay');skyg.appendChild(star);
 const lights=mk(W*2,H*2,'lay lights'),bloom=mk(W,H,'lay bloom'),fx=mk(W*SA,H*SA,'lay');
 const lx=lights.getContext('2d');lx.drawImage(O.lights,0,0);lx.scale(2,2);
 stage.classList.remove('in');stage.replaceChildren(skyg,ground,bloom,lights,fx);stage.style.width=W+'px';stage.style.height=H+'px';
 document.body.classList.toggle('lb-wide',wide);
 const R=rnd(9);O.win.forEach(w=>w.thr=R());O.win.sort((a,b)=>a.thr-b.thr);O.big.forEach(b=>{b.ph=R()*6.28;b.sp=.5+R()*1.6;b.t0=.3+R()*2.4});
 const routes=[];
 if(V===VH)routes.push(u=>[cst(u)-5,u]);
 if(V.roads)V.roads.forEach(rd=>routes.push(bezf(rd[0])));
 if(V===VL)routes.push(u=>[78+u*148,.72-.01*Math.sin(u*3.1416)]);
 if(V===VR)[.14,.24,.36,.50,.64,.80,.93].forEach(t=>routes.push(u=>[xr(t)-wr(t)-3+u*(wr(t)*2+6),t]));
 if(V===VB)for(let k=1;k<=5;k++)routes.push(u=>{const a=u*6.283,w2=1+.07*Math.sin(a*3+k*1.7)+.04*Math.sin(a*5+k);return[200+Math.cos(a)*27*k*w2,.50+Math.sin(a)*.078*k*w2]});
 const cars=routes.length?Array.from({length:wide?18:11},(_,i)=>({r:routes[i%routes.length],u:R(),v:(.010+R()*.014)*(R()<.5?1:-1)})):[];
 const boats=V===VR?Array.from({length:4},()=>({t:.25+R()*.6,o:(R()-.5)*.9,v:(R()<.5?1:-1)*(.0025+R()*.003)})):[];
 Lr={W,H,HS,SA,wide,O,V,skyg,ground,star,lights,bloom,fx,lx,cars,boats,wi:0,off:[],bloomed:false,shoot:null,nextShoot:4+R()*5,R};
 fit();T0=performance.now();requestAnimationFrame(()=>{void stage.offsetWidth;stage.classList.add('in')});
 if(RM)frame(T0+9000);else raf=requestAnimationFrame(frame)}
// 도시 아랫줄은 늘 버튼 묶음 바로 위에. 배경 폭의 78%는 늘 보이게
function fit(){if(!Lr||!active)return;const vw=innerWidth,vh=innerHeight,W=Lr.W,H=Lr.H,FY=Lr.wide?H-160:620,acts=qs('#intro .lb-acts'),top=acts?Math.min(vh,acts.getBoundingClientRect().top+scrollY):vh*.7,line=top-6;
 let s=Math.max(vw/W,vh/H)*1.035,y=line-FY*s;if(y>0){s=Math.max(s,line/FY);y=line-FY*s}
 const sMax=vw/(W*.78);if(s>sMax){s=sMax;y=line-FY*s}
 Lr.skyShift=Math.min(Lr.wide?90:150,Math.max(0,-y/s));const x=(vw-W*s)/2;stage.style.transform=`translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)})`;Lr.skyg.style.transform=`translateY(${Lr.skyShift.toFixed(1)}px)`;
 const fd=qs('#lobbyBg .lb-fade');if(fd)fd.style.top=Math.max(0,top-70)+'px';
 try{const c=Lr.O.sky.getContext('2d').getImageData(Lr.O.sky.width>>1,2,1,1).data;qs('#lobbyBg').style.background=`linear-gradient(rgb(${c[0]},${c[1]},${c[2]}),rgb(${c[0]},${c[1]},${c[2]}) 40%,#121019 41%)`}catch(e){}}
function drawWin(L,w,on){const x=L.lx;if(on){x.globalAlpha=w[5];x.fillStyle=w[4];x.fillRect(w[0],w[1],w[2],w[3])}else x.clearRect(w[0]-.1,w[1]-.1,w[2]+.2,w[3]+.2)}
function frame(now){if(!active||!Lr)return;if(document.documentElement.classList.contains('birth-on')){raf=requestAnimationFrame(frame);return}// 태어나기 연출이 덮고 있는 동안은 쉰다
 const L=Lr,T=(now-T0)/1000,O=L.O,{W,H,HS,SA}=L;
 const sx=L.star.getContext('2d');sx.setTransform(SA,0,0,SA,0,0);sx.clearRect(0,0,W,HS);
 for(const b of O.big){const ap=Math.max(0,Math.min(1,(T-b.t0)/.7));if(ap<=0)continue;const tw=.62+.38*Math.sin(T*b.sp+b.ph)*Math.sin(T*b.sp*.37+b.ph*2),r=b[2]*(1+.12*(tw-.62)),d=r*10*(1+(1-ap)*1.2);sx.globalAlpha=ap*tw;sx.drawImage(SPR[b[3]][b[4]>.28?1:0],b[0]-d/2,b[1]-d/2,d,d)}
 const p=Math.max(0,Math.min(1,(T-.9)/3.4)),pe=p*p*(3-2*p);while(L.wi<O.win.length&&O.win[L.wi].thr<=pe)drawWin(L,O.win[L.wi++],1);
 if(p>=1&&!L.bloomed){L.bloomed=true;const bx2=L.bloom.getContext('2d');bx2.clearRect(0,0,W,H);bx2.filter='blur(3px)';bx2.drawImage(L.lights,0,0,W,H);L.bloom.classList.add('on')}
 if(p>=1&&!RM&&O.win.length){for(let i=0;i<2;i++)if(L.R()<.22){if(L.off.length>O.win.length*.04||(L.off.length&&L.R()<.5)){drawWin(L,L.off.splice(L.R()*L.off.length|0,1)[0],1)}else{const w=O.win[L.R()*O.win.length|0];if(!w.off){w.off=1;L.off.push(w);drawWin(L,w,0);setTimeout(()=>{w.off=0},9000)}}}}
 const f=L.fx.getContext('2d');f.setTransform(SA,0,0,SA,0,0);f.clearRect(0,0,W,H);const fi=Math.max(0,Math.min(1,(T-1.2)/2));
 f.fillStyle='#fff4d6';O.glit.forEach((g,i)=>{const a=g[3]*(.5+.5*Math.sin(T*(1.3+(i%7)*.33)+i*1.7));f.globalAlpha=a*fi;f.fillRect(g[0]+Math.sin(T*.8+i)*.8,g[1],g[2],.8)});
 if(O.lh){const [lx0,ly0]=O.lh,a=T*.9,cs=Math.cos(a),sn=Math.sin(a),len=(L.wide?150:92)*Math.abs(cs),dir=cs>0?1:-1,al=.55*Math.pow(Math.abs(cs),.6)*fi;
  if(len>4){const g=f.createLinearGradient(lx0,ly0,lx0+dir*len,ly0);g.addColorStop(0,`rgba(255,244,200,${al})`);g.addColorStop(1,'rgba(255,244,200,0)');f.globalAlpha=1;f.fillStyle=g;f.beginPath();f.moveTo(lx0,ly0-.5);f.lineTo(lx0+dir*len,ly0-len*.07-1);f.lineTo(lx0+dir*len,ly0+len*.09+1);f.fill()}
  const fl=Math.max(0,sn);f.globalAlpha=(.25+.75*fl*fl*fl)*fi;const g2=f.createRadialGradient(lx0,ly0,0,lx0,ly0,3+9*fl*fl);g2.addColorStop(0,'#fff6d8');g2.addColorStop(1,'rgba(255,246,216,0)');f.fillStyle=g2;f.fillRect(lx0-14,ly0-14,28,28)}
 for(const c of L.cars){c.u+=c.v/60;if(c.u>1)c.u=0;if(c.u<0)c.u=1;const p0=c.r(c.u);if(p0[1]<0||p0[1]>1.02)continue;const q=O.at(p0[0],p0[1]);f.globalAlpha=.85*fi*Math.sin(Math.min(1,Math.min(c.u,1-c.u)*8)*1.57);f.fillStyle=c.v>0?'#fff3d6':'#ff9a7a';f.beginPath();f.arc(q[0],q[1],.55*q[2],0,7);f.fill()}
 for(const b of L.boats){b.t+=b.v/60;if(b.t>.92)b.v=-Math.abs(b.v);if(b.t<.2)b.v=Math.abs(b.v);const q=O.at(xr(b.t)+b.o*wr(b.t),b.t);f.globalAlpha=.9*fi;f.fillStyle='#ffe2ac';f.beginPath();f.arc(q[0],q[1],.6*q[2],0,7);f.fill();f.fillStyle='#ff8f6a';f.beginPath();f.arc(q[0]+2*q[2],q[1],.45*q[2],0,7);f.fill();f.globalAlpha=.18*fi;f.fillStyle='#ffd08a';f.fillRect(q[0]-.5,q[1]+1,1.6*q[2],5*q[2])}
 if(L.V===VB&&O.crop){const[cx,cy,cw,ch]=O.crop,mp=(ix,iy)=>[(ix-cx)/cw*W,(iy-cy)/ch*HS],pulse=.5+.5*Math.sin(T*1.1),flick=.85+.15*Math.sin(T*7.3);f.globalAlpha=1;f.lineCap='round';
  for(const[seg,wd] of [[[...Array(41)].map((_,i)=>{const x=470+i*26.5;return[x,2.006e-4*x*x-.9027*x+911.2]}),1],[[[450,332],[731,0]],.55]]){const P=seg.map(q=>mp(q[0],q[1])),hx=P[0][0],hy=P[0][1];
   for(const[lw,al] of [[7*wd,.10],[3*wd,.22],[1.2*wd,.5]]){const g=f.createLinearGradient(hx,hy,P[P.length-1][0],P[P.length-1][1]);g.addColorStop(0,`rgba(150,200,255,${al*(.35+.65*pulse)*flick*fi})`);g.addColorStop(.5,`rgba(110,170,255,${al*.5*pulse*fi})`);g.addColorStop(1,'rgba(110,170,255,0)');f.strokeStyle=g;f.lineWidth=lw;f.beginPath();P.forEach((q,i)=>i?f.lineTo(q[0],q[1]):f.moveTo(q[0],q[1]));f.stroke()}
   const gh=f.createRadialGradient(hx,hy,0,hx,hy,10*wd);gh.addColorStop(0,`rgba(220,236,255,${(.4+.5*pulse)*flick*fi})`);gh.addColorStop(1,'rgba(150,200,255,0)');f.fillStyle=gh;f.fillRect(hx-12*wd,hy-12*wd,24*wd,24*wd)}}
 if(!RM){if(!L.shoot&&T>L.nextShoot){const d=L.wide?1.6:1;L.shoot={t:T,x:W*(.25+L.R()*.6),y:HS*(.08+L.R()*.3),dx:-(90+L.R()*70)*d,dy:(34+L.R()*30)*d,dur:.75+L.R()*.4}}
  if(L.shoot){const s=L.shoot,u=(T-s.t)/s.dur;if(u>=1){L.shoot=null;L.nextShoot=T+5+L.R()*9}else{const hx=s.x+s.dx*u,hy=s.y+s.dy*u,tl=Math.min(u,.35),tx0=hx-s.dx*tl,ty0=hy-s.dy*tl,g=f.createLinearGradient(tx0,ty0,hx,hy),a=Math.sin(u*3.1416);g.addColorStop(0,'rgba(200,225,255,0)');g.addColorStop(1,`rgba(235,244,255,${a})`);f.globalAlpha=1;f.strokeStyle=g;f.lineWidth=1.2;f.lineCap='round';f.beginPath();f.moveTo(tx0,ty0);f.lineTo(hx,hy);f.stroke();f.fillStyle=`rgba(255,255,255,${a})`;f.beginPath();f.arc(hx,hy,1.1,0,7);f.fill()}}}
 if(!RM&&!document.hidden&&active)raf=requestAnimationFrame(frame)}
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&Lr&&active&&!RM){cancelAnimationFrame(raf);raf=requestAnimationFrame(frame)}});
let rz=0;addEventListener('resize',()=>{if(!active)return;fit();clearTimeout(rz);rz=setTimeout(()=>{const wide=innerWidth/innerHeight>1.15;if(!Lr||wide!==Lr.wide)build();else fit()},200)});
function enter(o){stage=stage||qs('#lbStage');if(!stage)return;SPR=SPR||mkSpr();lives=o.lives|0;met=o.met|0;active=true;qs('#lobbyBg').hidden=false;document.body.classList.add('lb-on');BI=pick();
 const B=BOARDS[BI],key=B.V.img[0],my=++tok;if(IMGS[key]){build();return}const im=new Image();im.onload=()=>{IMGS[key]=im;if(my===tok&&active)build()};im.onerror=()=>{};im.src='assets/lobby/'+B.f+'.webp'}
function leave(){active=false;tok++;cancelAnimationFrame(raf);Lr=null;const bg=qs('#lobbyBg');if(bg)bg.hidden=true;document.body.classList.remove('lb-on','lb-wide');if(stage)stage.replaceChildren()}
return {enter,leave,fit,get active(){return active}};
})();
