# -*- coding: utf-8 -*-
"""Fold — engine + BFS + generator.  Win = reduce active paper to a single square.
Cell: None=hole ; int>=0 = paper (0 blank, >0 tile).  Overlap paper ADDS.
hole-over-paper -> paper stays ; paper-onto-hole -> ILLEGAL ; flap width<=base width."""
import random, json
from collections import deque

def combine(dst,src):
    if src is None and dst is None: return None
    if src is None: return dst
    if dst is None: return 'X'
    return dst+src

def legal_folds(s):
    r0,r1,c0,c1=s['r0'],s['r1'],s['c0'],s['c1']; out=[]
    for k in range(c0+1,c1+1):
        lw=k-c0; rw=c1-k+1
        if rw<=lw: out.append(('V',k,'RL'))
        if lw<=rw: out.append(('V',k,'LR'))
    for k in range(r0+1,r1+1):
        th=k-r0; bh=r1-k+1
        if bh<=th: out.append(('H',k,'BT'))
        if th<=bh: out.append(('H',k,'TB'))
    return out

def apply_fold(s,f):
    r0,r1,c0,c1=s['r0'],s['r1'],s['c0'],s['c1']; g=s['g']; ng=dict(g)
    axis,k,d=f
    if axis=='V':
        move=range(k,c1+1) if d=='RL' else range(c0,k)
        nc0,nc1=(c0,k-1) if d=='RL' else (k,c1); nr0,nr1=r0,r1
        for c in move:
            dc=2*k-1-c
            for r in range(r0,r1+1):
                res=combine(ng[(r,dc)],g[(r,c)])
                if res=='X': return None
                ng[(r,dc)]=res
    else:
        move=range(k,r1+1) if d=='BT' else range(r0,k)
        nr0,nr1=(r0,k-1) if d=='BT' else (k,r1); nc0,nc1=c0,c1
        for r in move:
            dr=2*k-1-r
            for c in range(c0,c1+1):
                res=combine(ng[(dr,c)],g[(r,c)])
                if res=='X': return None
                ng[(dr,c)]=res
    return {'g':ng,'r0':nr0,'r1':nr1,'c0':nc0,'c1':nc1}

def key(s):
    r0,r1,c0,c1=s['r0'],s['r1'],s['c0'],s['c1']
    return (r0,r1,c0,c1,tuple(s['g'][(r,c)] for r in range(r0,r1+1) for c in range(c0,c1+1)))

def solve(s,maxd=8):
    q=deque([(s,[])]); seen={key(s)}
    while q:
        cur,path=q.popleft()
        if cur['r0']==cur['r1'] and cur['c0']==cur['c1']:
            return path
        if len(path)>=maxd: continue
        for f in legal_folds(cur):
            ns=apply_fold(cur,f)
            if ns is None: continue
            kk=key(ns)
            if kk in seen: continue
            seen.add(kk); q.append((ns,path+[f]))
    return None

def greedy_ok(s,maxd=12):
    # a simple always-fold-first-legal heuristic; if it solves, level is 'trivial'
    cur=s; steps=0
    while not(cur['r0']==cur['r1'] and cur['c0']==cur['c1']):
        if steps>maxd: return False
        fs=legal_folds(cur); moved=False
        for f in fs:
            ns=apply_fold(cur,f)
            if ns is not None: cur=ns; moved=True; break
        if not moved: return False
        steps+=1
    return True

def rnd_level(R,C,tiles,holes,rng):
    coords=[(r,c) for r in range(R) for c in range(C)]; rng.shuffle(coords)
    hole=set(coords[:holes]); rest=[x for x in coords if x not in hole]
    cells={}
    for (r,c) in rest[:tiles]: cells[(r,c)]=rng.randint(1,6)
    for (r,c) in rest[tiles:]: cells[(r,c)]=0
    g={}
    for r in range(R):
        for c in range(C):
            g[(r,c)]=None if (r,c) in hole else cells[(r,c)]
    return {'g':g,'r0':0,'r1':R-1,'c0':0,'c1':C-1}, cells, hole

def gen(rng,R,C,tiles,holes,want,tries=1500,need_nontrivial=True):
    for _ in range(tries):
        s,cells,hole=rnd_level(R,C,tiles,holes,rng)
        sol=solve(s,maxd=want+1)
        if not sol or len(sol)!=want: continue
        if need_nontrivial and holes>0 and greedy_ok(s):
            continue  # too easy: naive folding solves it
        grid=[[(-1 if (r,c) in hole else cells[(r,c)]) for c in range(C)] for r in range(R)]
        return {'rows':R,'cols':C,'grid':grid,'T':sum(cells.values()),'par':len(sol)}
    return None

if __name__=='__main__':
    rng=random.Random(20260420)
    plan=[
      (3,3,3,0,2),(3,3,4,0,2),(3,4,4,0,3),
      (3,4,5,1,3),(4,3,5,1,3),(4,4,5,1,3),
      (4,4,6,2,4),(4,4,7,2,4),(4,5,7,2,4),
      (5,4,7,2,4),(5,4,8,3,5),(5,5,8,3,5),
      (5,5,9,3,5),(5,5,9,4,5),(5,5,10,4,6),
    ]
    out=[]
    for i,(R,C,t,h,m) in enumerate(plan):
        lv=None
        for _ in range(8):
            lv=gen(rng,R,C,t,h,m, need_nontrivial=(h>0))
            if lv: break
        if not lv:  # relax move count
            for mm in (m-1,m+1):
                lv=gen(rng,R,C,t,h,mm, need_nontrivial=False)
                if lv: break
        if not lv:
            print(f'L{i+1} FAIL {R}x{C} m{m}'); continue
        lv['id']=len(out)+1; out.append(lv)
        print(f"L{lv['id']}: {R}x{C} tiles={t} holes={h} par={lv['par']} T={lv['T']}")
    json.dump({'levels':out}, open('/home/claude/fold/src/levels.json','w'))
    print('TOTAL',len(out))
