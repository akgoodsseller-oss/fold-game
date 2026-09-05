import json
levels=json.load(open('src/levels.json'))['levels']
LJSON=json.dumps(levels, separators=(',',':'))

HTML = r'''<!doctype html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<title>Fold</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none;touch-action:none}
:root{--ink:#111418;--accent:#4F46E5;--accent2:#EC4899;--paper:#fff;--line:#e7e7ea;--hole:#f3f3f5}
html,body{height:100%;background:#fff;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif;overflow:hidden}
#app{position:fixed;inset:0;display:flex;flex-direction:column;align-items:center}
header{width:100%;max-width:520px;padding:18px 22px 6px;display:flex;align-items:center;justify-content:space-between}
.brand{font-weight:800;font-size:22px;letter-spacing:-.02em}
.brand b{color:var(--accent)}
.sub{font-size:12px;color:#8a8a90;font-weight:600;letter-spacing:.02em}
.hud{width:100%;max-width:520px;padding:2px 22px 10px;display:flex;gap:8px;align-items:center;justify-content:space-between}
.pill{font-size:12.5px;font-weight:700;color:#54545c;background:#f5f5f7;border-radius:999px;padding:6px 12px}
.pill b{color:var(--ink)}
.goal{font-size:12.5px;font-weight:800;color:#fff;background:var(--accent);border-radius:999px;padding:6px 13px}
.stage{flex:1;width:100%;display:flex;align-items:center;justify-content:center;position:relative;perspective:1400px}
.board{position:relative;transform-style:preserve-3d}
.cell{position:absolute;display:flex;align-items:center;justify-content:center;font-weight:800;border-radius:12px;transition:left .28s cubic-bezier(.4,0,.2,1),top .28s cubic-bezier(.4,0,.2,1),width .28s,height .28s}
.tile{background:#fff;border:2.5px solid var(--ink);color:var(--ink)}
.blank{background:#fafafb;border:2px dashed #dcdce1;color:transparent}
.hole{background:repeating-linear-gradient(45deg,#fff,#fff 5px,#f4f4f6 5px,#f4f4f6 10px);border:2px dotted #dedee3}
.flap{position:absolute;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;background:#fff;border:2.5px solid var(--ink);
  box-shadow:0 12px 30px rgba(30,30,60,.18);z-index:40;backface-visibility:hidden}
.merge{animation:pop .34s ease}
@keyframes pop{0%{transform:scale(1)}45%{transform:scale(1.22);color:var(--accent)}100%{transform:scale(1)}}
.grab{position:absolute;z-index:20}
.edgehint{position:absolute;background:var(--accent);opacity:.0;border-radius:8px;transition:opacity .15s;z-index:15;pointer-events:none}
footer{width:100%;max-width:520px;padding:10px 22px calc(18px + env(safe-area-inset-bottom));display:flex;gap:10px}
button{flex:1;font-family:inherit;font-weight:700;font-size:15px;border:2px solid var(--ink);background:#fff;color:var(--ink);border-radius:14px;padding:13px;cursor:pointer;transition:transform .06s}
button:active{transform:scale(.97)}
button.primary{background:var(--ink);color:#fff}
button:disabled{opacity:.35}
.hint{position:absolute;bottom:8px;left:0;right:0;text-align:center;font-size:12.5px;color:#a0a0a8;font-weight:600;pointer-events:none}
.overlay{position:fixed;inset:0;background:rgba(255,255,255,.86);backdrop-filter:blur(6px);display:none;flex-direction:column;align-items:center;justify-content:center;z-index:100;padding:24px}
.overlay.show{display:flex;animation:fade .3s ease}
@keyframes fade{from{opacity:0}to{opacity:1}}
.ov-t{font-size:14px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.ov-h{font-size:40px;font-weight:850;letter-spacing:-.03em;margin:6px 0 2px}
.ov-s{font-size:15px;color:#70707a;font-weight:600;margin-bottom:22px}
.big{font-size:64px;font-weight:850;border:3px solid var(--ink);border-radius:20px;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;color:var(--accent)}
.menu{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;width:100%;max-width:360px}
.lv{aspect-ratio:1;border:2.5px solid var(--ink);border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:800;font-size:20px;cursor:pointer;background:#fff}
.lv small{font-size:9px;font-weight:700;color:#9a9aa2;letter-spacing:.08em;margin-top:2px}
.lv.done{background:var(--ink);color:#fff}
.lv.done small{color:#bdbdd6}
</style></head>
<body><div id="app">
  <header><div class="brand">FO<b>L</b>D</div><div class="sub" id="lvlabel">LEVEL 1</div></header>
  <div class="hud">
    <div class="pill">Folds <b id="moves">0</b></div>
    <div class="goal" id="goal">Make&nbsp;<b>&nbsp;</b></div>
    <div class="pill">Par <b id="par">0</b></div>
  </div>
  <div class="stage" id="stage"><div class="board" id="board"></div><div class="hint" id="hint">drag an edge inward to fold</div></div>
  <footer>
    <button id="undo">Undo</button>
    <button id="restart">Restart</button>
    <button id="menuBtn">Levels</button>
  </footer>
</div>

<div class="overlay" id="win">
  <div class="ov-t">Folded flat</div>
  <div class="big" id="winval">0</div>
  <div class="ov-h" id="wintitle">Level Complete</div>
  <div class="ov-s" id="winsub"></div>
  <div style="display:flex;gap:10px;width:100%;max-width:360px">
    <button id="replay">Replay</button>
    <button class="primary" id="next">Next</button>
  </div>
</div>

<div class="overlay" id="menu">
  <div class="ov-t">Choose a level</div>
  <div class="ov-h" style="margin-bottom:18px">Fold</div>
  <div class="menu" id="menuGrid"></div>
  <button style="margin-top:20px;max-width:360px;width:100%" id="closeMenu">Close</button>
</div>

<script>
const LEVELS=__LJSON__;
const KEY='fold_progress_v1';
let done=JSON.parse(localStorage.getItem(KEY)||'[]');
let cur=0, st=null, history=[], moves=0, cell=64, animating=false;

const $=id=>document.getElementById(id);
const board=$('board'), stage=$('stage');

function loadLevel(i){
  cur=i; const L=LEVELS[i];
  const g={};
  for(let r=0;r<L.rows;r++)for(let c=0;c<L.cols;c++){const v=L.grid[r][c];g[r+'_'+c]=(v===-1?null:v);}
  st={g,r0:0,r1:L.rows-1,c0:0,c1:L.cols-1,rows:L.rows,cols:L.cols};
  history=[]; moves=0;
  $('lvlabel').textContent='LEVEL '+(i+1);
  $('par').textContent=L.par;
  $('goal').innerHTML='Make&nbsp;<b>'+L.T+'</b>';
  $('moves').textContent='0';
  hideOverlays();
  render(true);
}
function cloneState(s){return {g:Object.assign({},s.g),r0:s.r0,r1:s.r1,c0:s.c0,c1:s.c1,rows:s.rows,cols:s.cols};}
function combine(dst,src){ if(src===null&&dst===null)return null; if(src===null)return dst; if(dst===null)return 'X'; return dst+src; }

function computeCell(){
  const W=st.c1-st.c0+1, H=st.r1-st.r0+1;
  const availW=Math.min(stage.clientWidth-36, 460);
  const availH=stage.clientHeight-30;
  const gap=8;
  cell=Math.floor(Math.min((availW-(W-1)*gap)/W,(availH-(H-1)*gap)/H));
  cell=Math.max(30,Math.min(cell,92));
  return gap;
}
function render(){
  const gap=computeCell();
  const W=st.c1-st.c0+1, H=st.r1-st.r0+1;
  board.style.width=(W*cell+(W-1)*gap)+'px';
  board.style.height=(H*cell+(H-1)*gap)+'px';
  board.innerHTML='';
  for(let r=st.r0;r<=st.r1;r++)for(let c=st.c0;c<=st.c1;c++){
    const v=st.g[r+'_'+c];
    const d=document.createElement('div');
    d.className='cell '+(v===null?'hole':(v>0?'tile':'blank'));
    const x=(c-st.c0)*(cell+gap), y=(r-st.r0)*(cell+gap);
    d.style.left=x+'px'; d.style.top=y+'px'; d.style.width=cell+'px'; d.style.height=cell+'px';
    d.style.fontSize=Math.round(cell*0.42)+'px';
    if(v!==null&&v>0)d.textContent=v;
    board.appendChild(d);
  }
}

// ---- folding ----
function foldState(s,axis,k,dir){
  const ns=cloneState(s);
  if(axis==='V'){
    const move=[]; if(dir==='RL'){for(let c=k;c<=s.c1;c++)move.push(c);ns.c0=s.c0;ns.c1=k-1;} else {for(let c=s.c0;c<k;c++)move.push(c);ns.c0=k;ns.c1=s.c1;}
    for(const c of move){const dc=2*k-1-c; for(let r=s.r0;r<=s.r1;r++){const res=combine(ns.g[r+'_'+dc],s.g[r+'_'+c]); if(res==='X')return null; ns.g[r+'_'+dc]=res;}}
  } else {
    const move=[]; if(dir==='BT'){for(let r=k;r<=s.r1;r++)move.push(r);ns.r0=s.r0;ns.r1=k-1;} else {for(let r=s.r0;r<k;r++)move.push(r);ns.r0=k;ns.r1=s.r1;}
    for(const r of move){const dr=2*k-1-r; for(let c=s.c0;c<=s.c1;c++){const res=combine(ns.g[dr+'_'+c],s.g[r+'_'+c]); if(res==='X')return null; ns.g[dr+'_'+c]=res;}}
  }
  return ns;
}

// Perform a fold with animation. side = 'L','R','T','B' (edge grabbed); k = crease gridline.
function doFold(side,k){
  if(animating)return;
  let axis,dir;
  if(side==='L'){axis='V';dir='LR';} else if(side==='R'){axis='V';dir='RL';}
  else if(side==='T'){axis='H';dir='TB';} else {axis='H';dir='BT';}
  const ns=foldState(st,axis,k,dir);
  if(!ns){flashInvalid();return;}
  animating=true;
  const gap=8;
  // build flap overlay from current cells being folded
  const flap=document.createElement('div'); flap.style.position='absolute'; flap.style.transformStyle='preserve-3d';
  const rect=board.getBoundingClientRect();
  let originStyle, w,h,fx,fy, rot;
  const cw=cell, W=st.c1-st.c0+1,H=st.r1-st.r0+1;
  const step=cell+gap;
  if(axis==='V'){
    const fromCols = dir==='RL' ? range(k,st.c1) : range(st.c0,k-1);
    const width=fromCols.length;
    fx=(dir==='RL')?((k-st.c0)*step):0;
    w=width*cell+(width-1)*gap; h=board.clientHeight; fy=0;
    flap.style.left=fx+'px'; flap.style.top='0'; flap.style.width=w+'px'; flap.style.height=h+'px';
    flap.style.transformOrigin=(dir==='RL')?'left center':'right center';
    rot=(dir==='RL')?'rotateY(-180deg)':'rotateY(180deg)';
    fillFlap(flap,fromCols,'V',dir,k,step,gap);
  } else {
    const fromRows = dir==='BT' ? range(k,st.r1) : range(st.r0,k-1);
    const height=fromRows.length;
    fy=(dir==='BT')?((k-st.r0)*step):0;
    h=height*cell+(height-1)*gap; w=board.clientWidth; fx=0;
    flap.style.left='0'; flap.style.top=fy+'px'; flap.style.width=w+'px'; flap.style.height=h+'px';
    flap.style.transformOrigin=(dir==='BT')?'center top':'center bottom';
    rot=(dir==='BT')?'rotateX(180deg)':'rotateX(-180deg)';
    fillFlap(flap,fromRows,'H',dir,k,step,gap);
  }
  flap.style.transition='transform .34s cubic-bezier(.45,0,.25,1)';
  flap.style.transform='none';
  board.appendChild(flap);
  requestAnimationFrame(()=>{requestAnimationFrame(()=>{flap.style.transform=rot;flap.style.boxShadow='0 4px 14px rgba(30,30,60,.10)';});});
  setTimeout(()=>{
    history.push(cloneState(st)); st=ns; moves++; $('moves').textContent=moves;
    render();
    // merge pop on tiles
    [...board.querySelectorAll('.tile')].forEach(el=>{el.classList.add('merge');});
    animating=false;
    if(st.r0===st.r1&&st.c0===st.c1){ setTimeout(winLevel,260); }
  },340);
}
function range(a,b){const o=[];for(let i=a;i<=b;i++)o.push(i);return o;}
function fillFlap(flap,idxs,axis,dir,k,step,gap){
  // render the moving cells inside flap, mirrored so they read like folding paper
  idxs.forEach((idx,ii)=>{
    const list = axis==='V'? range(st.r0,st.r1): range(st.c0,st.c1);
    list.forEach((jj,jji)=>{
      let r,c; if(axis==='V'){r=jj;c=idx;} else {r=idx;c=jj;}
      const v=st.g[r+'_'+c]; if(v===null)return;
      const d=document.createElement('div'); d.className='flap';
      let lx,ly;
      if(axis==='V'){ const localCol = dir==='RL' ? (idx-k) : (idx-st.c0); lx=localCol*step; ly=jji*step; }
      else { const localRow = dir==='BT' ? (idx-k) : (idx-st.r0); ly=localRow*step; lx=jji*step; }
      d.style.left=lx+'px'; d.style.top=ly+'px'; d.style.width=cell+'px'; d.style.height=cell+'px';
      d.style.fontSize=Math.round(cell*0.42)+'px';
      if(v>0)d.textContent=v; else {d.style.background='#fafafb';d.style.border='2px dashed #dcdce1';}
      flap.appendChild(d);
    });
  });
}
function flashInvalid(){
  board.animate([{transform:'translateX(0)'},{transform:'translateX(-6px)'},{transform:'translateX(6px)'},{transform:'translateX(0)'}],{duration:220});
}

// ---- input: drag an edge inward ----
let drag=null;
stage.addEventListener('pointerdown',e=>{
  if(animating)return;
  const rect=board.getBoundingClientRect();
  const x=e.clientX-rect.left, y=e.clientY-rect.top;
  const m=26;
  let side=null;
  if(x>=-m&&x<=rect.width+m&&y>=-m&&y<=rect.height+m){
    const dl=x, dr=rect.width-x, dt=y, db=rect.height-y;
    const min=Math.min(dl,dr,dt,db);
    if(min> Math.min(rect.width,rect.height)/2) return;
    if(min===dl)side='L'; else if(min===dr)side='R'; else if(min===dt)side='T'; else side='B';
  } else return;
  drag={side,sx:e.clientX,sy:e.clientY,rect};
  stage.setPointerCapture(e.pointerId);
  $('hint').style.opacity=0;
});
stage.addEventListener('pointermove',e=>{
  if(!drag)return;
});
stage.addEventListener('pointerup',e=>{
  if(!drag){return;}
  const gap=8, step=cell+gap;
  const dx=e.clientX-drag.sx, dy=e.clientY-drag.sy;
  const s=drag; drag=null;
  let cells,k;
  if(s.side==='L'){ cells=Math.max(1,Math.round(dx/step)); k=st.c0+cells; if(k>st.c1)k=st.c1; doFoldSafe('L',k); }
  else if(s.side==='R'){ cells=Math.max(1,Math.round(-dx/step)); k=st.c1+1-cells; if(k<st.c0+1)k=st.c0+1; doFoldSafe('R',k); }
  else if(s.side==='T'){ cells=Math.max(1,Math.round(dy/step)); k=st.r0+cells; if(k>st.r1)k=st.r1; doFoldSafe('T',k); }
  else { cells=Math.max(1,Math.round(-dy/step)); k=st.r1+1-cells; if(k<st.r0+1)k=st.r0+1; doFoldSafe('B',k); }
});
function doFoldSafe(side,k){
  // clamp so flap<=base; if not possible, try minimal legal
  const W=st.c1-st.c0+1,H=st.r1-st.r0+1;
  if(side==='L'){ const maxk=st.c0+Math.floor(W/2); if(k>maxk)k=maxk; if(k<st.c0+1)k=st.c0+1; }
  if(side==='R'){ const mink=st.c1+1-Math.floor(W/2); if(k<mink)k=mink; if(k>st.c1)k=st.c1; }
  if(side==='T'){ const maxk=st.r0+Math.floor(H/2); if(k>maxk)k=maxk; if(k<st.r0+1)k=st.r0+1; }
  if(side==='B'){ const mink=st.r1+1-Math.floor(H/2); if(k<mink)k=mink; if(k>st.r1)k=st.r1; }
  doFold(side,k);
}

function winLevel(){
  if(!done.includes(cur)){done.push(cur);localStorage.setItem(KEY,JSON.stringify(done));}
  const L=LEVELS[cur];
  $('winval').textContent=L.T;
  $('winsub').textContent = moves<=L.par? ('Folded in '+moves+' — par '+L.par+' ✦') : ('Folded in '+moves+' folds');
  $('wintitle').textContent = cur===LEVELS.length-1?'You finished Fold!':'Level Complete';
  $('next').textContent = cur===LEVELS.length-1?'Levels':'Next';
  $('win').classList.add('show');
}
function hideOverlays(){$('win').classList.remove('show');$('menu').classList.remove('show');}

$('undo').onclick=()=>{ if(animating||!history.length)return; st=history.pop(); moves=Math.max(0,moves-1); $('moves').textContent=moves; render(); };
$('restart').onclick=()=>loadLevel(cur);
$('replay').onclick=()=>loadLevel(cur);
$('next').onclick=()=>{ if(cur===LEVELS.length-1){openMenu();} else loadLevel(cur+1); };
$('menuBtn').onclick=openMenu;
$('closeMenu').onclick=()=>{$('menu').classList.remove('show');};
function openMenu(){
  hideOverlays();
  const grid=$('menuGrid'); grid.innerHTML='';
  LEVELS.forEach((L,i)=>{
    const d=document.createElement('div'); d.className='lv'+(done.includes(i)?' done':'');
    d.innerHTML=(i+1)+'<small>'+L.rows+'×'+L.cols+'</small>';
    d.onclick=()=>{loadLevel(i);};
    grid.appendChild(d);
  });
  $('menu').classList.add('show');
}
window.addEventListener('resize',()=>{if(st)render();});
loadLevel(0);
</script>
</body></html>'''

open('src/index.html','w').write(HTML.replace('__LJSON__', LJSON))
import os
print('index.html bytes:', os.path.getsize('src/index.html'))
