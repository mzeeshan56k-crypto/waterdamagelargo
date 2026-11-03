#!/usr/bin/env python3
"""Promote scheduled blog posts whose publish date has arrived.

Moves _scheduled/<slug>/ to blog/<slug>/, adds a card to the blog index
and a <url> to sitemap.xml. Safe to re-run: already published posts are skipped.
"""
import os,sys,json,re,shutil,datetime,html as H
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE="https://waterdamagerestorationlargo.com"
e=lambda s:H.escape(str(s),quote=True)

def run(today=None,dry=False):
    today=today or datetime.date.today()
    man_p=os.path.join(ROOT,'_scheduled/_manifest.json')
    if not os.path.exists(man_p): print("no manifest; nothing scheduled"); return []
    man=json.load(open(man_p,encoding='utf-8'))
    due=[(s,v) for s,v in man.items()
         if datetime.date.fromisoformat(v['date'])<=today
         and os.path.isdir(os.path.join(ROOT,'_scheduled',s))
         and not os.path.isdir(os.path.join(ROOT,'blog',s))]
    due.sort(key=lambda x:x[1]['date'])
    if not due: print("nothing due on",today); return []
    if dry:
        for s,v in due: print("  would publish",v['date'],s)
        return [s for s,_ in due]

    idx_p=os.path.join(ROOT,'blog/index.html'); idx=open(idx_p,encoding='utf-8').read()
    sm_p=os.path.join(ROOT,'sitemap.xml'); sm=open(sm_p,encoding='utf-8').read()
    published=[]
    for slug,v in due:
        shutil.move(os.path.join(ROOT,'_scheduled',slug), os.path.join(ROOT,'blog',slug))
        d=datetime.date.fromisoformat(v['date'])
        pretty=f"{d.strftime('%B')} {d.day}, {d.year}"
        card=(f'<article class="card"><h3><a href="{BASE}/blog/{slug}/">{e(v["h1"])}</a></h3>'
              f'<p class="postmeta"><span>{pretty}</span><span>Largo, FL</span></p>'
              f'<p>{e(v["desc"])}</p></article>')
        anchor='<div class="grid g3">'
        assert idx.count(anchor)>=1, "blog index grid not found"
        idx=idx.replace(anchor, anchor+card, 1)          # newest first
        loc=f"{BASE}/blog/{slug}/"
        if loc not in sm:
            sm=sm.replace('</urlset>',
              f'<url><loc>{loc}</loc><lastmod>{v["date"]}</lastmod>'
              f'<changefreq>monthly</changefreq><priority>0.6</priority></url>\n</urlset>',1)
        published.append(slug); print("  published",v['date'],slug)
    open(idx_p,'w',encoding='utf-8').write(idx)
    open(sm_p,'w',encoding='utf-8').write(sm)
    return published

if __name__=='__main__':
    dry='--dry' in sys.argv
    override=[a for a in sys.argv[1:] if re.fullmatch(r'\d{4}-\d{2}-\d{2}',a)]
    t=datetime.date.fromisoformat(override[0]) if override else None
    out=run(t,dry)
    print(f"{len(out)} post(s) {'would be ' if dry else ''}published")
