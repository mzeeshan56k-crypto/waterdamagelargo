#!/usr/bin/env python3
"""Rebuild the article listing on blog/index.html from every published post.

Scans blog/<slug>/index.html, groups posts by topic cluster and writes the
listing newest first within each group. Run after publishing; it is idempotent
and self healing, so the listing can never drift from what is actually live.
"""
import os,re,json,html as H,datetime,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(ROOT,'tools'))
from plan import CLUSTER_OF
BASE="https://waterdamagerestorationlargo.com"
e=lambda s:H.escape(str(s),quote=True)

GROUPS=[("emergency","Emergency Response"),("sources","What Causes Water Damage"),
        ("mold","Mold"),("drying","Drying and Equipment"),
        ("materials","Materials and Salvage"),("insurance","Insurance and Cost"),
        ("local","Largo and Pinellas County")]
LEGACY={"burst-pipe-first-steps-largo":"emergency",
        "mold-timeline-florida-humidity":"mold",
        "how-water-spreads-in-a-largo-slab-home":"local"}

def _existing_cards(idx):
    """Preserve the hand written date and excerpt already on the index."""
    out={}
    for m in re.finditer(r'<article class="card"><h3><a href="[^"]*/blog/([a-z0-9-]+)/">.*?</a></h3>'
                         r'<p class="postmeta"><span>([^<]*)</span>.*?</p><p>(.*?)</p></article>',idx,re.S):
        out[m.group(1)]=(m.group(2),H.unescape(m.group(3)))
    return out

def collect():
    posts=[]
    for slug in sorted(os.listdir(os.path.join(ROOT,'blog'))):
        p=os.path.join(ROOT,'blog',slug,'index.html')
        if not os.path.isfile(p): continue
        h=open(p,encoding='utf-8').read()
        title=H.unescape(re.search(r'<h1[^>]*>(.*?)</h1>',h,re.S).group(1)).strip()
        desc=H.unescape(re.search(r'<meta name="description" content="([^"]*)">',h).group(1))
        date=None
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
            o=json.loads(b)
            if o.get('@type')=='BlogPosting': date=o.get('datePublished')
        posts.append({"slug":slug,"title":re.sub('<[^>]+>','',title),"desc":desc,
                      "date":date or "1970-01-01",
                      "cluster":CLUSTER_OF.get(slug) or LEGACY.get(slug) or "local"})
    return posts

def build():
    idx_p=os.path.join(ROOT,'blog/index.html'); idx=open(idx_p,encoding='utf-8').read()
    keep=_existing_cards(idx)
    posts=collect()
    by={k:[] for k,_ in GROUPS}
    for p in posts: by[p['cluster']].append(p)
    for k in by: by[k].sort(key=lambda x:x['date'],reverse=True)

    blocks=[]
    total=len(posts)
    blocks.append('<section class="rv"><div class="wrap">\n'
      f'<div class="sec-head"><h2>All {total} Water Damage Guides for Largo and Pinellas County</h2>'
      '<p class="lead">Every guide we have published, grouped by topic. '
      'New articles are added through the week.</p></div>\n</div></section>\n')
    for key,label in GROUPS:
        group=by[key]
        if not group: continue
        cards=[]
        for p in group:
            d,ex = keep.get(p['slug'],(None,None))
            if not d:
                dt=datetime.date.fromisoformat(p['date'])
                d=f"{dt.strftime('%B')} {dt.day}, {dt.year}"
            cards.append(f'<article class="card"><h3><a href="{BASE}/blog/{p["slug"]}/">{e(p["title"])}</a></h3>'
                         f'<p class="postmeta"><span>{e(d)}</span><span>Largo, FL</span></p>'
                         f'<p>{e(ex or p["desc"])}</p></article>')
        tint=' sec-tint' if len(blocks)%2==0 else ''
        blocks.append(f'<section class="rv{tint}"><div class="wrap">\n'
          f'<div class="sec-head"><p class="eyebrow">{e(label)}</p>'
          f'<h2>{e(label)} Guides ({len(group)})</h2></div>\n'
          f'<div class="grid g3">{"".join(cards)}</div>\n</div></section>\n')
    new=''.join(blocks)

    # replace everything from the old listing section up to (not including) the services section
    start=idx.index('<section class="rv"><div class="wrap">\n<div class="sec-head"><h2>') \
          if '<div class="sec-head"><h2>All ' not in idx else idx.index('<section class="rv"><div class="wrap">\n<div class="sec-head"><h2>All ')
    end=idx.index('<section class="sec-tint rv">')   # services block follows
    idx=idx[:start]+new+'\n'+idx[end:]
    open(idx_p,'w',encoding='utf-8').write(idx)
    return total,{k:len(v) for k,v in by.items() if v}

if __name__=='__main__':
    t,by=build(); print("posts listed:",t,by)
