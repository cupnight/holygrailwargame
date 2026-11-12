import sys,json,os
sys.path.insert(0,'.'); import epi2_rev as R
import glob
done={}
for f in sorted(glob.glob('epi2_tr*.py')):
    ns={}; exec(open(f,encoding='utf8').read(),ns); done.update(ns.get('TR',{}))
sel=sys.argv[1].split(',')
for g in R.G:
    if g['id']=='tags' or g['id'].startswith('n_'): continue
    if not any(g['id']==x or (x.endswith('*') and g['id'].startswith(x[:-1])) for x in sel): continue
    print('##',g['id'],'|',g['t'])
    for r in g['rows']:
        if r['id'] in done: continue
        print(r['id'].replace(g['id']+'.','.',1) if r['id'].startswith(g['id']+'.') else r['id'],'\t',' ¦ '.join(r['L']))
