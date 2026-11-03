# -*- coding: utf-8 -*-
"""Render a blog post as a structural clone of the existing template."""
import re,json,html as H,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from plan import links_for,SERVICES,CLUSTERS,EXISTING

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE="https://waterdamagerestorationlargo.com"
TPL=open(os.path.join(ROOT,'blog/mold-timeline-florida-humidity/index.html'),encoding='utf-8').read()
SVC_NAMES={}
for jf in ('_data/services-a.json','_data/services-b.json'):
    for e in json.load(open(os.path.join(ROOT,jf),encoding='utf-8')):
        SVC_NAMES[e['slug']]=e['name']
e=lambda s: H.escape(str(s),quote=True)

def _registry():
    """slug -> description, for posts already written or already live."""
    reg={}
    mp=os.path.join(ROOT,'_scheduled/_manifest.json')
    if os.path.exists(mp):
        for s,v in json.load(open(mp,encoding='utf-8')).items(): reg[s]=v['desc']
    for s in list(EXISTING)+[d for d in os.listdir(os.path.join(ROOT,'blog'))
                             if os.path.isdir(os.path.join(ROOT,'blog',d))]:
        f=os.path.join(ROOT,'blog',s,'index.html')
        if os.path.exists(f):
            m=re.search(r'<meta name="description" content="([^"]*)">',open(f,encoding='utf-8').read())
            if m: reg[s]=H.unescape(m.group(1))
    return reg

def blurb(slug):
    r=_registry().get(slug)
    if not r: raise KeyError(f"no description known for link target {slug}")
    return r

def _body(blocks):
    out=[]
    for b in blocks:
        if isinstance(b,str): out.append(f"<p>{e(b)}</p>")
        elif b[0]=='ul': out.append("<ul>"+''.join(f"<li>{e(x)}</li>" for x in b[1])+"</ul>")
        elif b[0]=='table':
            head,rows=b[1],b[2]
            out.append('<div class="tbl-wrap"><table class="tbl"><thead><tr>'
                +''.join(f"<th>{e(c)}</th>" for c in head)+'</tr></thead><tbody>'
                +''.join('<tr>'+''.join(f"<td>{e(c)}</td>" for c in r)+'</tr>' for r in rows)
                +'</tbody></table></div>')
    return ''.join(out)

def render(slug,post,date):
    title,desc,h1 = post['title'],post['desc'],post['h1']
    assert len(title)<=60 and len(desc)<=150, f"{slug}: meta length {len(title)}/{len(desc)}"
    url=f"{BASE}/blog/{slug}/"
    links,cluster=links_for(slug)
    h=TPL

    # --- head ---
    h=re.sub(r'<title>.*?</title>',lambda m:f"<title>{e(title)}</title>",h,count=1,flags=re.S)
    h=re.sub(r'<meta name="description" content="[^"]*">',
             f'<meta name="description" content="{e(desc)}">',h,count=1)
    h=re.sub(r'<meta property="og:title" content="[^"]*">',
             f'<meta property="og:title" content="{e(title)}">',h,count=1)
    h=re.sub(r'<meta property="og:description" content="[^"]*">',
             f'<meta property="og:description" content="{e(desc)}">',h,count=1)
    h=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{url}">',h,count=1)
    h=re.sub(r'<meta property="og:url" content="[^"]*">',
             f'<meta property="og:url" content="{url}">',h,count=1)

    # --- schema ---
    def swap(pred,new):
        nonlocal h
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
            d=json.loads(m.group(1))
            if pred(d):
                blob='<script type="application/ld+json">'+json.dumps(new,ensure_ascii=False,separators=(',',':'))+'</script>'
                h=h[:m.start()]+blob+h[m.end():]; return True
        return False
    lb=json.loads(re.search(r'<script type="application/ld\+json">(\{"@context":"https://schema\.org","@type":\["LocalBusiness".*?)</script>',h,re.S).group(1))
    lb['url']=url; lb['description']=desc
    swap(lambda d:isinstance(d.get('@type'),list) and 'LocalBusiness' in d['@type'], lb)
    swap(lambda d:d.get('@type')=='BreadcrumbList',{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":BASE+"/blog/"},
        {"@type":"ListItem","position":3,"name":h1,"item":url}]})
    swap(lambda d:d.get('@type')=='BlogPosting',{"@context":"https://schema.org","@type":"BlogPosting",
        "headline":h1,"description":desc,"datePublished":date,"dateModified":date,
        "mainEntityOfPage":{"@type":"WebPage","@id":url},"url":url,
        "author":{"@type":"Organization","name":"Water Damage Restoration Largo","url":BASE+"/"},
        "publisher":{"@type":"Organization","name":"Water Damage Restoration Largo","url":BASE+"/",
            "logo":{"@type":"ImageObject","url":BASE+"/assets/water-damage-restoration-largo-logo.jpg"}},
        "image":BASE+"/assets/"+post.get('img','water-damage-hallway-air-movers-largo-home.jpg'),
        "articleSection":cluster,"inLanguage":"en-US"})
    swap(lambda d:d.get('@type')=='FAQPage',{"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in post['faqs']]})

    # --- breadcrumb visible ---
    h=re.sub(r'(<li aria-current="page">)[^<]*(</li>)',lambda m:m.group(1)+e(h1)+m.group(2),h,count=1)

    # --- main ---
    guides=''.join(
        f'<article class="card"><h3><a href="{BASE}/blog/{s}/">{e(t)}</a></h3>'
        f'<p>{e(blurb(s))}</p></article>' for s,t in links)
    svcs=''.join(
        f'<article class="card"><h3><a href="{BASE}/service/{s}/">{e(SVC_NAMES[s])}</a></h3>'
        f'<p>{e(post["svcblurbs"][i])}</p></article>' for i,s in enumerate(SERVICES[cluster]))
    faqs=''.join(f'<details><summary>{e(q)}</summary><div class="ans"><p>{e(a)}</p></div></details>'
                 for q,a in post['faqs'])
    body=''.join(f'<h2>{e(hh)}</h2>'+_body(bb) for hh,bb in post['sections'])

    main=f'''<main id="main">
<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol><li><a href="{BASE}/">Home</a></li><li><a href="{BASE}/blog/">Blog</a></li><li aria-current="page">{e(h1)}</li></ol></div></nav>

<section class="sec-tint rv"><div class="wrap narrow">
<p class="eyebrow">{e(post.get('eyebrow','Water damage guide'))}</p>
<h1>{e(h1)}</h1>
<p class="lead">{e(post['intro'][0])}</p>
<p>{e(post['intro'][1])}</p>
<div class="callstrip"><p>{e(post.get('cta','Water coming in right now? Call and we will confirm an arrival window for your address.'))}</p><a class="btn btn-call" href="tel:+18332899993">Call (833) 289-9993</a></div>
</div></section>

<section class="rv"><div class="wrap narrow prose">
{body}
<p>For the full scope of extraction, drying and repair work across Pinellas County, see <a href="{BASE}/">water damage restoration in Largo, FL</a>.</p>
</div></section>

<section class="rv"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Related guides</p><h2>{e(post['guides_h2'])}</h2></div>
<div class="grid g2">{guides}</div>
</div></section>

<section class="sec-dark rv"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Services</p><h2>Services Related to This Article</h2></div>
<div class="grid g2">{svcs}</div>
</div></section>

<section class="rv"><div class="wrap narrow">
<p class="eyebrow">Questions</p><h2>{e(post['faq_h2'])}</h2>
<div class="faq">{faqs}</div>
</div></section>

<section class="ctaband rv"><div class="wrap">
<h2>Water Damage in Largo or Pinellas County?</h2>
<p>Call and describe what you are seeing. We confirm an arrival window for your address.</p>
<div class="hero-cta"><a class="btn btn-call" href="tel:+18332899993">Call (833) 289-9993</a></div>
</div></section>
</main>'''
    h=re.sub(r'<main.*?</main>',lambda m:main,h,count=1,flags=re.S)
    return h

def write(slug,post,date,outdir):
    d=os.path.join(ROOT,outdir,slug); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(render(slug,post,date))
