import random, json
import importlib.util
spec=importlib.util.spec_from_file_location('fg','tools/foldgen.py')
fg=importlib.util.module_from_spec(spec); spec.loader.exec_module(fg)

FMIN={1:0,2:1,3:2,4:2,5:3,6:3}
def minpar(R,C): return FMIN[R]+FMIN[C]

def gen_exact(rng,R,C,tiles,holes,tries=800,nontrivial=True):
    par=minpar(R,C)
    for _ in range(tries):
        s,cells,hole=fg.rnd_level(R,C,tiles,holes,rng)
        sol=fg.solve(s,maxd=par)          # bounded at true min -> fast
        if not sol or len(sol)!=par: continue
        if nontrivial and holes>0 and fg.greedy_ok(s): continue
        grid=[[(-1 if (r,c) in hole else cells[(r,c)]) for c in range(C)] for r in range(R)]
        return {'rows':R,'cols':C,'grid':grid,'T':sum(cells.values()),'par':par}
    return None

rng=random.Random(4242)
plan=[
  (3,3,3,0),(3,3,4,0),(3,4,4,0),(3,4,5,1),
  (4,3,5,1),(4,4,5,1),(4,4,6,2),(4,4,7,2),
  (4,5,7,2),(5,4,7,2),(5,4,8,3),(5,5,8,3),
  (5,5,9,3),(5,5,10,4),
]
out=[]
for i,(R,C,t,h) in enumerate(plan):
    lv=None
    for _ in range(6):
        lv=gen_exact(rng,R,C,t,h,nontrivial=(h>0))
        if lv: break
    if not lv:
        for _ in range(6):
            lv=gen_exact(rng,R,C,t,h,nontrivial=False)
            if lv: break
    if not lv: print(f'L{i+1} FAIL {R}x{C}'); continue
    lv['id']=len(out)+1; out.append(lv)
    print(f"L{lv['id']}: {R}x{C} tiles={t} holes={h} par={lv['par']} T={lv['T']}")
json.dump({'levels':out}, open('src/levels.json','w'))
print('TOTAL',len(out))
