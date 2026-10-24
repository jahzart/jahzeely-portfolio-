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
PROJECTS = DATA['projects']
EXTERNAL = DATA['external']
BY_SLUG = {p['slug']: p for p in PROJECTS}

EMAIL = 'jahzeelysinai@gmail.com'
BEHANCE = 'https://www.behance.net/jahzeelysinaiperez'
SOCIALS = [('Behance', BEHANCE), ('Instagram', 'https://instagram.com/jahzartdesign'), ('Post.pro', 'https://post.pro/profile/jahzeelysinai')]
YEAR = 2026
GSAP = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/'
FONTS = 'https://fonts.googleapis.com/css2?family=Anton&family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,400&display=swap'


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
ARROW_UP = '<svg viewBox="0 0 100 130" aria-hidden="true"><path d="M50 8 L50 122 M10 50 L50 8 L90 50" fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_NE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 12.5 12.5 3.5M5 3.5h7.5V11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_TOP = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_DOWN = '<svg viewBox="0 0 120 140" aria-hidden="true"><path d="M60 4v128M8 80l52 52 52-52" fill="none" stroke="currentColor" stroke-width="5"/></svg>'
SPARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 0c1.6 10.6 8.4 18.4 20 20-11.6 1.6-18.4 9.4-20 20-1.6-10.6-8.4-18.4-20-20C11.6 18.4 18.4 10.6 20 0z" fill="currentColor"/></svg>'

# Orange geometric artwork for each work category (original shapes)
O = 'var(--accent)'
SVC_ART = [
    # Branding: circle with a quarter missing + square
    f'<svg viewBox="0 0 240 240"><path d="M120 20a100 100 0 1 0 100 100H120z" fill="{O}"/><rect x="132" y="8" width="100" height="100" fill="{O}" opacity=".55"/></svg>',
    # Logos: ring and core
    f'<svg viewBox="0 0 240 240"><circle cx="120" cy="120" r="92" fill="none" stroke="{O}" stroke-width="34"/><circle cx="120" cy="120" r="30" fill="{O}"/></svg>',
    # Social media: grid of tiles
    f'<svg viewBox="0 0 240 240"><rect x="16" y="16" width="96" height="96" rx="22" fill="{O}"/><circle cx="176" cy="64" r="48" fill="{O}"/><rect x="16" y="128" width="96" height="96" rx="48" fill="{O}" opacity=".55"/><rect x="128" y="128" width="96" height="96" rx="22" fill="{O}"/></svg>',
    # Packaging: isometric box
    f'<svg viewBox="0 0 240 240"><path d="M120 18 214 66 120 114 26 66z" fill="{O}" opacity=".55"/><path d="M26 66v108l94 48V114z" fill="{O}"/><path d="M214 66v108l-94 48V114z" fill="{O}" opacity=".8"/></svg>',
    # Illustration: rising sun with rays
    f'<svg viewBox="0 0 240 240"><path d="M30 190a90 90 0 0 1 180 0z" fill="{O}"/><g stroke="{O}" stroke-width="12" stroke-linecap="round"><path d="M120 20v40M40 60l26 26M200 60l-26 26M8 130h34M232 130h-34"/></g><rect x="8" y="206" width="224" height="16" fill="{O}" opacity=".55"/></svg>',
    # Flyers: stacked sheets
    f'<svg viewBox="0 0 240 240"><rect x="58" y="24" width="124" height="168" fill="{O}" opacity=".35" transform="rotate(-14 120 108)"/><rect x="58" y="36" width="124" height="168" fill="{O}" opacity=".6" transform="rotate(-5 120 120)"/><rect x="58" y="50" width="124" height="168" fill="{O}" transform="rotate(5 120 134)"/></svg>',
    # Websites & apps: window with blocks
    f'<svg viewBox="0 0 240 240"><rect x="14" y="32" width="212" height="176" rx="14" fill="none" stroke="{O}" stroke-width="14"/><path d="M14 74h212" stroke="{O}" stroke-width="14"/><rect x="38" y="96" width="78" height="88" fill="{O}"/><rect x="132" y="96" width="70" height="36" fill="{O}" opacity=".55"/><rect x="132" y="148" width="70" height="36" fill="{O}" opacity=".55"/></svg>',
    # AI lab: sparkles
    f'<svg viewBox="0 0 240 240"><path d="M100 20c8 52 30 76 80 84-50 8-72 32-80 84-8-52-30-76-80-84 50-8 72-32 80-84z" fill="{O}"/><path d="M190 140c4 26 15 38 40 42-25 4-36 16-40 42-4-26-15-38-40-42 25-4 36-16 40-42z" fill="{O}" opacity=".55"/></svg>',
]

SERVICES = [
    ('Branding', 'Branding', 'Complete visual identities that communicate the essence of each brand.', 'Identidades visuales completas que comunican la esencia de cada marca.', 'filter:branding'),
    ('Logos', 'Logos', 'Unique and memorable symbols with strategic intention.', 'Símbolos únicos y memorables con intención estratégica.', 'filter:logo'),
    ('Social Media', 'Social Media', 'Visual content for social networks that connects and converts.', 'Contenido visual para redes que conecta y convierte.', 'behance'),
    ('Packaging', 'Packaging', 'Packages that live on shelves and in consumer memory.', 'Empaques que viven en estantes y en la memoria.', 'filter:packaging'),
    ('Illustration', 'Ilustración', 'Original visual worlds, traditional and digital.', 'Mundos visuales propios, tradicional y digital.', 'filter:illustration'),
    ('Flyers', 'Flyers', 'Print and digital pieces with immediate visual impact.', 'Piezas impresas y digitales con impacto visual inmediato.', 'behance'),
    ('Websites & Apps', 'Websites & Apps', 'UI/UX for user-centered digital interfaces.', 'UI/UX para interfaces digitales centradas en el usuario.', 'filter:digital'),
    ('AI Lab', 'AI Lab', 'Photography, video and experiences created with AI.', 'Fotografía, video y experiencias creadas con IA.', 'lab'),
]

FEATURED = ['curious-cafe', 'zen', 'kenzo', 'asimov', 'period-app', 'cryptomonitor']
FEATURED_BIG = 'asimov'  # ocupa 2 columnas x 2 filas en el mosaico
TOOLS = ['Adobe Illustrator', 'Photoshop', 'InDesign', 'After Effects', 'Figma', 'Branding', 'Motion Graphics', 'AI Tools']
FILTERS = [('all', 'All', 'Todos'), ('branding', 'Branding', 'Branding'), ('packaging', 'Packaging', 'Packaging'),
           ('digital', 'Digital', 'Digital'), ('illustration', 'Illustration', 'Ilustración'), ('logo', 'Logo', 'Logo')]


# ---------- shared pieces ----------
def head(title, desc, rel, image=None):
    og = f'<meta property="og:image" content="{a(image)}">' if image else ''
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
<link rel="stylesheet" href="{rel}assets/site.css">
</head>
<body>
'''


def lang_switch():
    return '<div class="lang" role="group" aria-label="Language"><button type="button" data-lang="en">EN</button><button type="button" data-lang="es">ES</button></div>'


def burger():
    return '<button type="button" class="burger" data-menu-open data-en-aria="Open menu" data-es-aria="Abrir menú" aria-label="Open menu"><i></i><i></i></button>'


def logo(rel):
    return f'<a href="{rel}index.html" class="logo"><span class="logo-mark" aria-hidden="true">JS</span><span>Jahzeely Sinai<small>Design</small></span></a>'


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
<script src="{rel}assets/site.js" defer></script>
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
  <div class="svc-art" aria-hidden="true">{SVC_ART[i]}</div>
</article>''')

    works = []
    for s in FEATURED:
        p = BY_SLUG[s]
        works.append(f'''<a class="work{' big' if s == FEATURED_BIG else ''}" href="{project_link(p, rel)}"><div class="work-img" data-parallax><img src="{a(p['cover'])}" alt="{a(p['title'])}" loading="lazy"></div><h3>{escape(p['title'])}</h3>{tb(p['category'])}</a>''')

    lab_rows = [
        ('AI · Photography', 'AI · Fotografía', 'Generative Photography', 'Fotografía Generativa'),
        ('AI · Video', 'AI · Video', 'Generative Video', 'Video Generativo'),
        ('AI · Application', 'AI · Aplicación', 'AI Digital Experience', 'Experiencia Digital AI'),
    ]
    lab = ''.join(f'<div class="lab-row" data-reveal>{t(k, ke, "span", "kind")}{t(n, ne, "h3")}{t("Coming soon", "Próximamente", "span", "status")}</div>' for k, ke, n, ne in lab_rows)
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
    <h1 class="hero-title" aria-label="Jahzeely Sinai">
      <span class="line" aria-hidden="true">Jahzeely</span>
      <span class="line" aria-hidden="true">S<span class="arrow">{ARROW_UP}</span>nai</span>
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
      <div class="stat" data-reveal><b>8</b>{t('Categories', 'Categorías')}</div>
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
  <div class="pitem-img" data-parallax><img src="{a(p['cover'])}" alt="{a(p['title'])}" loading="lazy"></div>
  <h2>{escape(p['title'])}</h2>
  <div class="meta">{tb(p['category'])}<i></i><span>{escape(p['year'])}</span></div>
</a>''')
    for e in EXTERNAL:
        counts[e['filter']] += 1
        items.append(f'''<a class="pitem" href="{a(e['url'])}" target="_blank" rel="noopener" data-cat="{e['filter']}">
  <div class="pitem-img" data-parallax><img src="{a(e['cover'])}" alt="{a(e['title'])}" loading="lazy"></div>
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
def img_block(src, alt, full):
    cls = 'd-img full' if full else 'd-img'
    return f'<div class="{cls}" data-lightbox data-clip><img src="{a(src)}" alt="{a(alt)}" loading="lazy"></div>'


def build_detail(i):
    rel = '../'
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    g = p['gallery']
    title = p['title']
    paras = p['paragraphs']

    first = ''
    if len(g) > 2:
        first += img_block(g[1], title, False) + img_block(g[2], title, False)
    if len(g) > 3:
        first += img_block(g[3], title, True)
    rest, k, pair_turn = '', 4, False
    while k < len(g):
        if pair_turn and k + 1 < len(g):
            rest += img_block(g[k], title, False) + img_block(g[k + 1], title, False)
            k += 2
        else:
            rest += img_block(g[k], title, True)
            k += 1
        pair_turn = not pair_turn

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
  <div class="d-cover-img" data-parallax><img src="{a(g[0])}" alt="{a(title)}"></div>
  <div class="d-card">
    <dl>
      <div><dt>{t('Client', 'Cliente')}</dt><dd>{escape(p['client'] or title)}</dd></div>
      <div><dt>{t('Service', 'Servicio')}</dt><dd>{tb(p['category'])}</dd></div>
      <div><dt>{t('Year', 'Año')}</dt><dd>{escape(p['year'])}</dd></div>
    </dl>
    <a href="{a(p['behance'])}" target="_blank" rel="noopener">{t('View on Behance', 'Ver en Behance')}{ARROW_NE}</a>
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
    <div class="thumb"><img src="{a(nxt['cover'])}" alt="" loading="lazy"></div>
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
