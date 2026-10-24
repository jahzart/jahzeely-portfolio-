#!/usr/bin/env python3
"""Generate the static site from src/content.json.

Usage: python3 src/build.py
Writes index.html, projects.html and project/<slug>.html at the repo root.
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, 'src', 'content.json'), encoding='utf-8'))
# Newest first: by the last year in the 'year' field (e.g. "2022 - 2024" counts as 2024);
# within the same year, the project added most recently to content.json goes first
PROJECTS = [p for _, p in sorted(enumerate(DATA['projects']),
                                 key=lambda ip: (int(ip[1]['year'].split('-')[-1].strip()), ip[0]), reverse=True)]
EXTERNAL = DATA['external']
BY_SLUG = {p['slug']: p for p in PROJECTS}

EMAIL = 'jahzeelysinai@gmail.com'
BEHANCE = 'https://www.behance.net/jahzeelysinaiperez'
SOCIALS = [('Behance', BEHANCE), ('Instagram', 'https://instagram.com/jahzartdesign'), ('Post.pro', 'https://post.pro/profile/jahzeelysinai')]
YEAR = 2026
SITE = 'https://jahzeely-portfolio.vercel.app/'
GSAP = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/'
FONTS = 'https://fonts.googleapis.com/css2?family=Anton&family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,400&display=swap'


def bust(path):
    """Append the file's modification time so browsers fetch replaced files with the same name."""
    full = os.path.join(ROOT, path)
    return f'{path}?v={int(os.path.getmtime(full))}' if os.path.exists(full) else path


def src(path, rel):
    """Local asset paths are made relative to the page (and versioned); URLs pass through."""
    return path if path.startswith('http') else rel + bust(path)


def a(s):
    return escape(s, quote=True)


def t(en, es=None, tag='span', cls='', attrs=''):
    """Bilingual element. Text defaults to English; site.js swaps it."""
    es = en if es is None else es
    c = f' class="{cls}"' if cls else ''
    data = f' data-en="{a(en)}" data-es="{a(es)}"' if es != en else ''
    return f'<{tag}{c}{data}{attrs}>{escape(en)}</{tag}>'


def tb(d, tag='span', cls='', attrs=''):
    return t(d['en'], d['es'], tag, cls, attrs)


# ---------- icons ----------
ARROW_NE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 12.5 12.5 3.5M5 3.5h7.5V11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_TOP = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_DOWN = '<svg viewBox="0 0 120 140" aria-hidden="true"><path d="M60 4v128M8 80l52 52 52-52" fill="none" stroke="currentColor" stroke-width="5"/></svg>'
SPARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 0c1.6 10.6 8.4 18.4 20 20-11.6 1.6-18.4 9.4-20 20-1.6-10.6-8.4-18.4-20-20C11.6 18.4 18.4 10.6 20 0z" fill="currentColor"/></svg>'

# Generated photo for each work category, in SERVICES order
SVC_IMG = ['branding', 'logos', 'social', 'packaging', 'illustration', 'web', 'ai']

SERVICES = [
    ('Branding', 'Branding', 'Complete visual identities that communicate the essence of each brand.', 'Identidades visuales completas que comunican la esencia de cada marca.', 'filter:branding'),
    ('Logos', 'Logos', 'Unique and memorable symbols with strategic intention.', 'Símbolos únicos y memorables con intención estratégica.', 'filter:logo'),
    ('Social Media', 'Social Media', 'Visual content for social networks that connects and converts.', 'Contenido visual para redes que conecta y convierte.', 'filter:social'),
    ('Packaging', 'Packaging', 'Packages that live on shelves and in consumer memory.', 'Empaques que viven en estantes y en la memoria.', 'filter:packaging'),
    ('Illustration', 'Ilustración', 'Original visual worlds, traditional and digital.', 'Mundos visuales propios, tradicional y digital.', 'filter:illustration'),
    ('Websites & Apps', 'Websites & Apps', 'UI/UX for user-centered digital interfaces.', 'UI/UX para interfaces digitales centradas en el usuario.', 'filter:digital'),
    ('AI Lab', 'AI Lab', 'Photography, video and experiences created with AI.', 'Fotografía, video y experiencias creadas con IA.', 'filter:ai'),
]

FEATURED = ['curious-cafe', 'zen', 'kenzo', 'asimov', 'period-app', 'cryptomonitor']
FEATURED_BIG = 'asimov'  # ocupa 2 columnas x 2 filas en el mosaico
TOOLS = ['Adobe Illustrator', 'Photoshop', 'InDesign', 'After Effects', 'Figma', 'Branding', 'Motion Graphics', 'AI Tools']
FILTERS = [('all', 'All', 'Todos'), ('branding', 'Branding', 'Branding'), ('packaging', 'Packaging', 'Packaging'),
           ('digital', 'Digital', 'Digital'), ('social', 'Social Media', 'Social Media'), ('illustration', 'Illustration', 'Ilustración'), ('logo', 'Logo', 'Logo'), ('ai', 'AI Lab', 'AI Lab')]


# ---------- shared pieces ----------
def head(title, desc, rel, image=None):
    og = f'<meta property="og:image" content="{a(src(image, SITE))}">' if image else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{a(desc)}">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:type" content="website">
{og}
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}{bust('assets/site.css')}">
</head>
<body>
'''


def lang_switch():
    return '<div class="lang" role="group" aria-label="Language"><button type="button" data-lang="en">EN</button><button type="button" data-lang="es">ES</button></div>'


def burger():
    return '<button type="button" class="burger" data-menu-open data-en-aria="Open menu" data-es-aria="Abrir menú" aria-label="Open menu"><i></i><i></i></button>'


def logo(rel):
    return f'<a href="{rel}index.html" class="logo"><span>Jahzeely Sinai<small>Design</small></span></a>'


def nav_items(rel):
    return [
        (f'{rel}index.html', 'Home', 'Inicio'),
        (f'{rel}projects.html', 'Projects', 'Proyectos'),
        (f'{rel}index.html#about', 'About', 'Sobre mí'),
        (f'{rel}index.html#contact', 'Contact', 'Contacto'),
    ]


def overlays(rel, lightbox=False):
    links = ''.join(f'<a href="{h}">{t(en, es)}</a>' for h, en, es in nav_items(rel))
    socials = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIALS)
    lb = ('<div class="lightbox" role="dialog" aria-label="Image viewer"><button type="button" class="lb-close" aria-label="Close">&times;</button>'
          '<button type="button" class="lb-prev" aria-label="Previous">&larr;</button><img src="" alt="">'
          '<button type="button" class="lb-next" aria-label="Next">&rarr;</button></div>') if lightbox else ''
    return f'''<div class="loader" aria-hidden="true"><div class="loader-word">{''.join(f'<span>{c}</span>' for c in 'Loading')}</div><div class="loader-bar"></div></div>
<div class="menu" aria-hidden="true">
  <div class="menu-top">{logo(rel)}<div class="head-right">{lang_switch()}<button type="button" class="menu-close" data-menu-close aria-label="Close menu"></button></div></div>
  <nav class="menu-links" aria-label="Main">{links}</nav>
  <div class="menu-foot"><a href="mailto:{EMAIL}">{EMAIL}</a><div class="socials">{socials}</div></div>
</div>
<button type="button" class="to-top" aria-label="Back to top">{ARROW_TOP}</button>
{lb}
<div id="smooth-wrapper"><div id="smooth-content">
'''


def site_head(rel):
    return f'''<header class="site-head"><div class="wrap">{logo(rel)}<div class="head-right">{lang_switch()}{burger()}</div></div></header>
'''


def footer(rel):
    links = ''.join(f'<a href="{h}">{t(en, es)}</a>' for h, en, es in nav_items(rel)) + f'<a href="{BEHANCE}" target="_blank" rel="noopener">Behance</a>'
    word = f'<span>Jahzeely Sinai {SPARK}</span>'
    return f'''<footer class="foot">
  <div class="marquee" aria-label="Jahzeely Sinai"><div class="marquee-inner">{word}{word}</div></div>
  <div class="wrap"><nav class="foot-links" aria-label="Footer">{links}</nav></div>
  <div class="foot-copy">&copy; {YEAR} <b>Jahzeely Sinai Pérez</b> · {t('Creative Designer & AI Artist · Spain', 'Creative Designer & AI Artist · España')}</div>
</footer>
</div></div>
'''


def scripts(rel):
    libs = ''.join(f'<script src="{GSAP}{f}" defer></script>' for f in ['gsap.min.js', 'ScrollTrigger.min.js', 'ScrollSmoother.min.js', 'SplitText.min.js'])
    return f'''{libs}
<script src="{rel}{bust('assets/site.js')}" defer></script>
</body>
</html>
'''


def project_link(p, rel):
    return f'{rel}project/{p["slug"]}.html'


# ---------- home ----------
def build_home():
    rel = ''
    A = BY_SLUG['asimov']
    svc_rows = []
    for i, (en, es, den, des, target) in enumerate(SERVICES):
        if target.startswith('filter:'):
            href, ext = f'projects.html?filter={target[7:]}', ''
            btn = t('View projects', 'Ver proyectos')
        elif target == 'lab':
            href, ext = '#lab', ''
            btn = t('Discover', 'Descubrir')
        else:
            href, ext = BEHANCE, ' target="_blank" rel="noopener"'
            btn = '<span>Behance</span>' + ARROW_NE
        svc_rows.append(f'''<article class="svc-row" style="z-index:{i + 1}">
  <div class="svc-num">S/ {i + 1:03d}</div>
  <div class="svc-body">{t(en, es, 'h3')}{t(den, des, 'p')}<a class="pill" href="{href}"{ext}>{btn}</a></div>
  <div class="svc-art" data-clip><img src="{bust(f'assets/categories/{SVC_IMG[i]}.jpg')}" alt="{a(en)}" loading="lazy"></div>
</article>''')

    works = []
    for s in FEATURED:
        p = BY_SLUG[s]
        works.append(f'''<a class="work{' big' if s == FEATURED_BIG else ''}" href="{project_link(p, rel)}"><div class="work-img" data-parallax><img src="{a(src(p['cover'], rel))}" alt="{a(p['title'])}" loading="lazy"></div><h3>{escape(p['title'])}</h3>{tb(p['category'])}</a>''')

    # A row links to the AI projects once it has at least one; otherwise it says "Coming soon"
    lab_rows = [
        ('AI · Photography', 'AI · Fotografía', 'Generative Photography', 'Fotografía Generativa', 'ai-photo'),
        ('AI · Video', 'AI · Video', 'Generative Video', 'Video Generativo', 'ai-video'),
        ('AI · Application', 'AI · Aplicación', 'AI Digital Experience', 'Experiencia Digital AI', 'ai-app'),
    ]
    def lab_row(k, ke, n, ne, tag):
        if any(tag in p.get('ai', []) for p in PROJECTS):
            return (f'<a class="lab-row" href="projects.html?filter=ai" data-reveal>{t(k, ke, "span", "kind")}{t(n, ne, "h3")}'
                    f'<span class="status">{t("View projects", "Ver proyectos")} {ARROW_NE}</span></a>')
        return f'<div class="lab-row" data-reveal>{t(k, ke, "span", "kind")}{t(n, ne, "h3")}{t("Coming soon", "Próximamente", "span", "status")}</div>'
    lab = ''.join(lab_row(*r) for r in lab_rows)
    socials = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIALS)
    tools = ''.join(f'<li>+ {escape(x)}</li>' for x in TOOLS)
    star = ' <span style="color:var(--accent)">✦</span> '
    big = star.join([t('Unleash your brand', 'Desata tu marca'), t('Design that connects', 'Diseño que conecta'), t('Unleash your brand', 'Desata tu marca')])

    html = head('Jahzeely Sinai | Creative Designer & AI Artist',
                'Branding, visual identity, illustration and digital experiences. Graphic designer and AI artist based in Spain.',
                rel, A['cover'])
    html += overlays(rel)
    html += f'''<main>
<section class="hero on-dark">
  <div class="wrap hero-inner">
    <div class="hero-bar">{lang_switch()}{burger()}</div>
    <div class="hero-photo" aria-hidden="true"><img src="{bust('assets/jahzeely.webp')}" alt="" width="900" height="1205"></div>
    <h1 class="hero-title" aria-label="Jahzeely Sinai">
      <span class="line" aria-hidden="true">Jahzeely</span>
      <span class="line" aria-hidden="true">Sinai</span>
    </h1>
    <div class="hero-intro">
      {t('Design that connects and is never forgotten.', 'Diseño que conecta y no se olvida.', 'h2')}
      <div>
        {t('Branding, visual identity, illustration and digital experiences. Creating soulful work from Spain for the world.', 'Branding, identidad visual, ilustración y experiencias digitales. Creando trabajo con alma desde España para el mundo.', 'p')}
        <a class="pill light" href="projects.html">{t('View projects', 'Ver proyectos')}</a>
      </div>
    </div>
  </div>
</section>

<section class="services" id="services">
  <div class="wrap">
    <div class="sec-head">{t('Specialties', 'Especialidades', 'span', 'label')}<span class="label">{len(SERVICES):02d}</span></div>
    {t('Work categories', 'Categorías de trabajo', 'h2', 'sec-title', ' data-split style="margin-bottom:60px"')}
    <div class="svc">{''.join(svc_rows)}</div>
  </div>
</section>

<section class="works" id="work">
  <div class="wrap">
    <div class="sec-head">{t('Featured projects', 'Proyectos destacados', 'span', 'label')}<span class="label">{len(FEATURED):02d}</span></div>
    {t('Selected work', 'Trabajo selecto', 'h2', 'sec-title', ' data-split')}
    <div class="works-grid">{''.join(works)}</div>
    <div class="works-more"><a class="pill" href="projects.html">{t('All projects', 'Todos los proyectos')}</a></div>
  </div>
</section>

<section class="big-type" aria-hidden="true"><div class="track">{big}</div></section>

<section class="about" id="about">
  <div class="wrap about-grid">
    <div class="stats">
      <div class="stat" data-reveal><b>12+</b>{t('Projects', 'Proyectos')}</div>
      <div class="stat" data-reveal><b>7</b>{t('Categories', 'Categorías')}</div>
      <div class="stat" data-reveal><b>7+</b>{t('Years of experience', 'Años de experiencia')}</div>
    </div>
    <div class="about-copy">
      {t('About me', 'Sobre mí', 'span', 'label')}
      {t("Designer with an artist's soul", 'Diseñadora con alma de artista', 'h2', '', ' data-split')}
      {t("I'm Jahzeely Sinai, a passionate graphic designer with years of experience creating visual identities that endure. My work connects strategic branding, illustration and technology.", 'Soy Jahzeely Sinai, diseñadora gráfica apasionada con años de experiencia creando identidades visuales que perduran. Mi trabajo conecta branding estratégico, ilustración y tecnología.', 'p', '', ' data-reveal')}
      {t('Currently based in Spain, I work with international clients on projects ranging from full corporate identities to experiences powered by artificial intelligence.', 'Actualmente basada en España, trabajo con clientes internacionales en proyectos que van desde identidades corporativas hasta experiencias potenciadas con inteligencia artificial.', 'p', '', ' data-reveal')}
      <ul class="tools" data-reveal>{tools}</ul>
      <a class="pill" href="#contact">{t("Let's Talk", 'Hablemos')}</a>
    </div>
  </div>
</section>

<section class="lab on-dark" id="lab">
  <div class="wrap">
    <div class="lab-head">
      <div>{t('Artificial intelligence', 'Inteligencia artificial', 'span', 'label')}<h2 data-split>AI Lab</h2></div>
      {t('Creative exploration at the frontier of human design and artificial intelligence. Generative photography, video, interfaces and digital experiences powered by AI.', 'Exploración creativa en la frontera entre diseño humano e inteligencia artificial. Fotografía generativa, video, interfaces y experiencias digitales potenciadas con IA.', 'p', '', ' data-reveal')}
    </div>
    <div>{lab}</div>
  </div>
</section>

<section class="contact" id="contact">
  <div class="wrap contact-grid">
    <div>
      {t('Contact', 'Contacto', 'span', 'label')}
      {t('Got a project in mind?', '¿Tienes un proyecto en mente?', 'h2', '', ' data-split')}
      {t("Tell me your idea and together we'll create something the world hasn't seen yet.", 'Cuéntame tu idea y juntas creamos algo que el mundo no ha visto todavía.', 'p', '', ' data-reveal')}
    </div>
    <div class="contact-side" data-reveal>
      <a class="contact-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <div class="contact-social">{socials}</div>
    </div>
  </div>
</section>
</main>
'''
    html += footer(rel) + scripts(rel)
    return html


# ---------- projects list ----------
def build_projects():
    rel = ''
    counts = {f: 0 for f, _, _ in FILTERS}
    items = []
    for p in PROJECTS:
        for f in p['filter'].split():
            counts[f] += 1
        items.append(f'''<a class="pitem" href="{project_link(p, rel)}" data-cat="{p['filter']}">
  <div class="pitem-img" data-clip><img src="{a(src(p['cover'], rel))}" alt="{a(p['title'])}" loading="lazy"></div>
  <h2>{escape(p['title'])}</h2>
  <div class="meta">{tb(p['category'])}<i></i><span>{escape(p['year'])}</span></div>
</a>''')
    for e in EXTERNAL:
        counts[e['filter']] += 1
        items.append(f'''<a class="pitem" href="{a(e['url'])}" target="_blank" rel="noopener" data-cat="{e['filter']}">
  <div class="pitem-img" data-clip><img src="{a(src(e['cover'], rel))}" alt="{a(e['title'])}" loading="lazy"></div>
  <h2>{escape(e['title'])}</h2>
  <div class="meta">{tb(e['category'])}<i></i><span class="ext">Behance{ARROW_NE}</span></div>
</a>''')
    counts['all'] = len(PROJECTS) + len(EXTERNAL)
    filters = ''.join(f'<button type="button" data-filter="{f}" aria-pressed="{"true" if f == "all" else "false"}">{t(en, es)}<sup>{counts[f]:02d}</sup></button>' for f, en, es in FILTERS)

    html = head('Projects | Jahzeely Sinai', 'Branding, packaging, illustration, logos and digital design projects by Jahzeely Sinai.', rel, PROJECTS[0]['cover'])
    html += overlays(rel) + site_head(rel)
    html += f'''<main>
<section class="page-hero">
  <div class="wrap page-hero-grid">
    <h1 class="page-title">
      {t('Selected work', 'Trabajo selecto', 'span', '', ' data-intro style="display:block"')}
      <span class="row2">{t('all projects', 'todos los proyectos', 'span', '', ' data-intro')}{t('Branding, visual identity, illustration and digital experiences. Creating soulful work from Spain for the world.', 'Branding, identidad visual, ilustración y experiencias digitales. Creando trabajo con alma desde España para el mundo.', 'span', 'lead')}</span>
    </h1>
    <div class="page-arrow" aria-hidden="true">{ARROW_DOWN}</div>
  </div>
</section>
<section class="wrap">
  <div class="filters" role="group" aria-label="Filter projects">{filters}</div>
  <div class="plist">{''.join(items)}</div>
</section>
</main>
'''
    html += footer(rel) + scripts(rel)
    return html


# ---------- project detail ----------
def img_block(src, alt, size=None):
    """One gallery image. With a size it becomes a cell of a justified row:
    its width grows with its aspect ratio, so both cells share one height."""
    style = ''
    if size:
        ar = size[0] / size[1]
        style = f' style="flex:{ar:.3f} 1 0;aspect-ratio:{size[0]}/{size[1]}"'
    if src.endswith('.mp4'):
        # Looping clip that behaves like a GIF: muted autoplay, no controls
        poster = src[:-4] + '.jpg'
        return (f'<div class="d-img d-video"{style} data-clip><video src="{a(src)}" poster="{a(poster)}" '
                f'autoplay muted loop playsinline preload="metadata" aria-label="{a(alt)}"></video></div>')
    return f'<div class="d-img"{style} data-lightbox data-clip><img src="{a(src)}" alt="{a(alt)}" loading="lazy"></div>'


def gallery_rows(items, alt, rel):
    """Alternate single and paired rows. Two images only share a row when their
    shapes are close enough that neither ends up a thin sliver."""
    html, k, pair_turn = '', 0, True
    while k < len(items):
        if pair_turn and k + 1 < len(items):
            (u1, s1), (u2, s2) = items[k], items[k + 1]
            r1, r2 = s1[0] / s1[1], s2[0] / s2[1]
            if max(r1, r2) / min(r1, r2) <= 3:
                html += f'<div class="d-row">{img_block(src(u1, rel), alt, s1)}{img_block(src(u2, rel), alt, s2)}</div>'
                k += 2
                pair_turn = False
                continue
        html += img_block(src(items[k][0], rel), alt)
        k += 1
        pair_turn = True
    return html


POST_ICONS = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 8 3.6 4.5 7.2 4.5c2 0 3.6 1.1 4.8 2.8 1.2-1.7 2.8-2.8 4.8-2.8 3.6 0 5.8 3.5 4.5 6.8-1.8 4.6-9.3 9.2-9.3 9.2z"/></svg>'
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.6a8.4 8.4 0 0 1-12.3 7.5L3.5 20.5l1.4-4.6A8.5 8.5 0 1 1 20.5 11.6z"/></svg>'
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 3.5 10.6 13.4M21.5 3.5l-6.8 17-4.1-7.1-7.1-4.1z"/></svg>'
)
POST_SAVE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3.5h12v17l-6-4.4-6 4.4z"/></svg>'


def post_card(x, handle, alt, rel):
    """Feed post shown as a minimal Instagram-style card."""
    return (f'<figure class="p-card" data-clip><figcaption class="p-head"><span class="p-avatar"></span>{escape(handle)}</figcaption>'
            f'<div class="p-img" style="aspect-ratio:{x["size"][0]}/{x["size"][1]}" data-lightbox><img src="{a(src(x["src"], rel))}" alt="{a(alt)}" loading="lazy"></div>'
            f'<div class="p-actions">{POST_ICONS}<span class="p-save">{POST_SAVE}</span></div></figure>')


def detail_gallery(p, title, rel):
    g = p['gallery']
    # The cover leads the page, so the whole Behance gallery goes below it
    items = list(zip(g, p['gallery_sizes']))
    first = gallery_rows(items[:3], title, rel)
    rest = gallery_rows(items[3:], title, rel)
    # Optional images that always get a full row to themselves, e.g. boards
    # with small text that must stay readable
    solo = lambda key: ''.join(img_block(src(x['src'], rel), title) for x in p.get(key, []))
    rest = solo('after_process') + rest + solo('gallery_end')

    return first, rest


def build_detail(i):
    rel = '../'
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    title = p['title']
    paras = p['paragraphs']

    if p.get('layout') == 'social':
        # Social projects: feed posts in an Instagram-like grid, stories in a row
        cell = lambda x, cls: f'<div class="{cls}" data-lightbox data-clip><img src="{a(src(x["src"], rel))}" alt="{a(title)}" loading="lazy"></div>'
        first = f'<div class="p-feed">{"".join(post_card(x, p["handle"], title, rel) for x in p["posts"])}</div>'
        rest = f'<div class="p-feed p-stories">{"".join(post_card(x, p["handle"], title, rel) for x in p["stories"])}</div>' if p['stories'] else ''
    elif p.get('layout') == 'cards':
        # Two-sided cards: front portrait, hover (or tap) flips to the ornamental back
        flip = ''.join(f'<figure class="flip" tabindex="0" data-clip><div class="flip-in">'
                       f'<img class="flip-f" src="{a(src(x["front"], rel))}" alt="{a(x["name"])}" loading="lazy">'
                       f'<img class="flip-b" src="{a(src(x["back"], rel))}" alt="" loading="lazy"></div>'
                       f'<figcaption>{escape(x["name"])}</figcaption></figure>' for x in p['cards'])
        first = f'<div class="flips">{flip}</div>'
        rest = ''
    elif p.get('layout') == 'sections':
        # Labelled grids, each cell keeps the image's own proportions
        def section(s):
            if s.get('posts'):
                label = tb(s['label'], 'span', 'label s-label') if s.get('label') else ''
                return f'{label}<div class="p-feed">{"".join(post_card(x, p["handle"], title, rel) for x in s["items"])}</div>'
            if s.get('browser'):
                label = tb(s['label'], 'span', 'label s-label') if s.get('label') else ''
                wins = ''.join(f'<div class="browser" data-clip><div class="browser-bar"><i></i><i></i><i></i><span>{escape(s["url"])}</span></div>'
                               f'<div data-lightbox><img src="{a(src(x["src"], rel))}" alt="{a(title)}" loading="lazy"></div></div>' for x in s['items'])
                return f'{label}<div class="browsers">{wins}</div>'
            if s.get('phones'):
                label = tb(s['label'], 'span', 'label s-label') if s.get('label') else ''
                phones = ''.join(f'<div class="phone" data-clip><div class="phone-screen" data-lightbox>'
                                 f'<img src="{a(src(x["src"], rel))}" alt="{a(title)}" loading="lazy"></div></div>' for x in s['items'])
                return f'{label}<div class="phones{" dark" if s.get("dark") else ""}">{phones}</div>'
            def cell(x):
                ratio = f'aspect-ratio:{x["size"][0]}/{x["size"][1]}'
                if x['src'].endswith('.mp4'):
                    return (f'<div class="s-cell s-video" style="{ratio}" data-clip><video src="{a(src(x["src"], rel))}" '
                            f'poster="{a(src(x["src"][:-4] + ".jpg", rel))}" autoplay muted loop playsinline preload="metadata"></video></div>')
                return (f'<div class="s-cell" style="{ratio}" data-lightbox data-clip>'
                        f'<img src="{a(src(x["src"], rel))}" alt="{a(title)}" loading="lazy"></div>')
            if any(x['src'].endswith('.mp4') for x in s['items']):
                label = tb(s['label'], 'span', 'label s-label') if s.get('label') else ''
                return f'{label}<div class="s-grid" style="--cols:{s["cols"]}">{"".join(cell(x) for x in s["items"])}</div>'
            cells = ''.join(f'<div class="s-cell" style="aspect-ratio:{x["size"][0]}/{x["size"][1]}" data-lightbox data-clip>'
                            f'<img src="{a(src(x["src"], rel))}" alt="{a(title)}" loading="lazy"></div>' for x in s['items'])
            label = tb(s['label'], 'span', 'label s-label') if s.get('label') else ''
            return f'{label}<div class="s-grid" style="--cols:{s["cols"]}">{cells}</div>'
        first = section(p['sections'][0])
        rest = ''.join(section(s) for s in p['sections'][1:])
    else:
        first, rest = detail_gallery(p, title, rel)

    tools = ''.join(f'<li>+ {escape(x)}</li>' for x in p['tools'])
    steps = ''.join(f'<li>{n}. <b>{tb(s["title"])}.</b> {tb(s["desc"])}</li>' for n, s in enumerate(p['process'], 1))

    html = head(f'{title} | Jahzeely Sinai', p['subtitle']['en'], rel, p['cover'])
    html += overlays(rel, lightbox=True) + site_head(rel)
    html += f'''<main>
<section class="d-hero">
  <div class="wrap">
    <h1 class="d-title" data-intro>{escape(title)}</h1>
    <div class="d-cols">{tb(p['subtitle'], 'p', '', ' data-reveal')}{tb(paras[0], 'p', '', ' data-reveal')}</div>
  </div>
</section>
<section class="wrap d-cover">
  <div class="d-cover-img" data-clip><img src="{a(src(p['cover'], rel))}" alt="{a(title)}"></div>
  <div class="d-card">
    <dl>
      <div><dt>{t('Client', 'Cliente')}</dt><dd>{escape(p['client'] or title)}</dd></div>
      <div><dt>{t('Service', 'Servicio')}</dt><dd>{tb(p['category'])}</dd></div>
      <div><dt>{t('Year', 'Año')}</dt><dd>{escape(p['year'])}</dd></div>
    </dl>
    {f'<a href="{a(p["behance"])}" target="_blank" rel="noopener">' + t('View on Behance', 'Ver en Behance') + ARROW_NE + '</a>' if p.get('behance') else ''}
    {f'<a href="{a(p["url"])}" target="_blank" rel="noopener">' + (tb(p['url_label']) if p.get('url_label') else t('Visit website', 'Ver sitio web')) + ARROW_NE + '</a>' if p.get('url') else ''}
  </div>
</section>
<section class="wrap d-sec">
  {tb(p['heading'], 'h2', '', ' data-split')}
  {''.join(tb(x, 'p', '', ' data-reveal') for x in paras[1:])}
  <div class="d-tools" data-reveal>{t('Tools used', 'Herramientas', 'span', 'label')}<ul>{tools}</ul></div>
</section>
<section class="wrap"><div class="d-imgs">{first}</div></section>
<section class="wrap d-sec">
  {t('Creative process', 'Proceso creativo', 'h2', '', ' data-split')}
  <ol class="d-process" data-reveal>{steps}</ol>
</section>
<section class="wrap"><div class="d-imgs">{rest}</div></section>
<section class="wrap d-next">
  <a href="{nxt['slug']}.html">
    <div>{t('Next project', 'Siguiente proyecto', 'span', 'label')}<h2>{escape(nxt['title'])}</h2></div>
    <div class="thumb"><img src="{a(src(nxt['cover'], rel))}" alt="" loading="lazy"></div>
  </a>
</section>
</main>
'''
    html += footer(rel) + scripts(rel)
    return html


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', path)


if __name__ == '__main__':
    write('index.html', build_home())
    write('projects.html', build_projects())
    for i, p in enumerate(PROJECTS):
        write(f'project/{p["slug"]}.html', build_detail(i))
