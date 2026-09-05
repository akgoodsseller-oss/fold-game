const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:412,height:820},deviceScaleFactor:2});
  const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
  p.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  await p.goto('file://'+process.cwd()+'/src/index.html');
  await p.waitForTimeout(400);
  await p.screenshot({path:'tools/s1_start.png'});
  // read active rect + do a fold by dragging right edge left by ~1.5 cells
  const box=await p.$eval('#board',el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};});
  // drag from right edge inward
  await p.mouse.move(box.x+box.w-4, box.y+box.h/2);
  await p.mouse.down();
  await p.mouse.move(box.x+box.w-70, box.y+box.h/2,{steps:6});
  await p.mouse.up();
  await p.waitForTimeout(500);
  await p.screenshot({path:'tools/s2_afterfold.png'});
  const moves=await p.$eval('#moves',e=>e.textContent);
  // now auto-solve: repeatedly fold smallest side until 1x1, using page context knowledge
  // simple: keep dragging alternating edges inward
  for(let i=0;i<8;i++){
    const st=await p.evaluate(()=>({W:st.c1-st.c0+1,H:st.r1-st.r0+1,anim:animating}));
    if(st.W===1&&st.H===1)break;
    const bb=await p.$eval('#board',el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};});
    if(st.W>=st.H){ // fold vertical: drag right edge left by half
      await p.mouse.move(bb.x+bb.w-4,bb.y+bb.h/2);await p.mouse.down();
      await p.mouse.move(bb.x+bb.w/2+4,bb.y+bb.h/2,{steps:5});await p.mouse.up();
    } else {
      await p.mouse.move(bb.x+bb.w/2,bb.y+bb.h-4);await p.mouse.down();
      await p.mouse.move(bb.x+bb.w/2,bb.y+bb.h/2+4,{steps:5});await p.mouse.up();
    }
    await p.waitForTimeout(430);
  }
  await p.waitForTimeout(400);
  await p.screenshot({path:'tools/s3_win.png'});
  const winShown=await p.$eval('#win',e=>e.classList.contains('show'));
  const winval=await p.$eval('#winval',e=>e.textContent).catch(()=>'?');
  console.log('moves after 1 fold:',moves,'| winShown:',winShown,'| winval:',winval,'| errors:',errs.length,errs.slice(0,3));
  await b.close();
})();
