import { FilesetResolver, HandLandmarker } from 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22-rc.20250304/vision_bundle.mjs';
const token = location.hash.slice(1); history.replaceState(null, '', '/');
const status = document.querySelector('#status'), video = document.querySelector('#video');
let tracker, stream, active=false, held=false, right=false, leftCount=0, rightCount=0, prev=null, scrollY=null, lastVideo=-1, busy=false;
async function send(data) {
  try { const r=await fetch('/command',{method:'POST',headers:{'Content-Type':'application/json','X-Handswizard-Token':token},body:JSON.stringify(data),cache:'no-store'}); if(!r.ok) throw Error(); return true; }
  catch { active=false; held=false; status.textContent='Connexion perdue : souris en pause. Recharge la page.'; return false; }
}
function reset(){ held=false; right=false; leftCount=rightCount=0; prev=null; scrollY=null; }
async function pause(){ active=false; reset(); await send({type:'pause'}); document.querySelector('#toggle').textContent='Activer la souris'; status.textContent='En pause.'; }
document.querySelector('#stop').onclick=pause;
document.querySelector('#toggle').onclick=async()=>{if(active){await pause();return;} reset(); if(await send({type:'resume'})){active=true;document.querySelector('#toggle').textContent='Mettre en pause';status.textContent='Souris active';}};
document.querySelector('#start').onclick=async()=>{try{
 status.textContent='Chargement du suivi et demande de webcam…';
 const vision=await FilesetResolver.forVisionTasks('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22-rc.20250304/wasm');
 tracker=await HandLandmarker.createFromOptions(vision,{baseOptions:{modelAssetPath:'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'},runningMode:'VIDEO',numHands:1});
 stream=await navigator.mediaDevices.getUserMedia({video:true,audio:false}); video.srcObject=stream; await video.play();
 document.querySelector('#start').disabled=true; document.querySelector('#toggle').disabled=false; status.textContent='Webcam prête. Active la souris quand tu es prête.'; requestAnimationFrame(frame);
 }catch(e){status.textContent='Impossible de démarrer : vérifie Internet et les permissions webcam. '+e.message;}};
const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y), clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
async function frame(){requestAnimationFrame(frame);if(!tracker || busy || video.currentTime===lastVideo)return;lastVideo=video.currentTime;busy=true;
 try { const lm=tracker.detectForVideo(video,performance.now()).landmarks[0];
 if(!active)return;
 if(!lm){ if(held){await send({type:'button',button:'left',down:false});held=false;} prev=null;leftCount=rightCount=0;right=false;scrollY=null; await send({type:'move',dx:0,dy:0}); return; }
 const size=Math.max(dist(lm[0],lm[9]),.0001), lp=dist(lm[4],lm[8])/size, rp=dist(lm[4],lm[12])/size;
 const scroll=lm[8].y<lm[6].y && lm[12].y<lm[10].y && lm[16].y>lm[14].y && lm[20].y>lm[18].y && lp>.6 && rp>.6;
 if(scroll){if(held){await send({type:'button',button:'left',down:false});held=false;} if(scrollY!==null){const steps=clamp(Math.round((scrollY-lm[9].y)*100),-4,4);if(steps)await send({type:'scroll',steps});}scrollY=lm[9].y;prev=null;leftCount=rightCount=0;await send({type:'move',dx:0,dy:0});return;}
 scrollY=null;const x=1-lm[5].x,y=lm[5].y;
 if(prev){await send({type:'move',dx:clamp((x-prev.x)*2500,-55,55),dy:clamp((y-prev.y)*1800,-55,55)});}else await send({type:'move',dx:0,dy:0});prev={x,y};
 leftCount=lp<.27?leftCount+1:0; rightCount=rp<.27&&!held?rightCount+1:0;
 if(!held&&leftCount>=3){held=await send({type:'button',button:'left',down:true});}else if(held&&lp>.43){await send({type:'button',button:'left',down:false});held=false;}
 if(rightCount>=3&&!right&&!held){await send({type:'click',button:'right'});right=true;}if(rp>.43)right=false;
 }catch(e){await pause();status.textContent='Suivi interrompu : '+e.message;}finally{busy=false;}}
document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
window.addEventListener('pagehide',()=>{if(stream)stream.getTracks().forEach(t=>t.stop());});

