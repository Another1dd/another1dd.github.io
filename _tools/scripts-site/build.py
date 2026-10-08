#!/usr/bin/env python3
"""Render the Kin Compass scripts library (/kincompass/scripts/) from content/*.json.

Usage: python3 _tools/scripts-site/build.py [--og] [--en PATH_TO_en.json]

Standard library only. Output is committed HTML (no build step on GitHub Pages).
"""
import argparse
import glob
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'kincompass', 'scripts')
BASE = 'https://another1dd.github.io'
DEFAULT_EN = os.path.abspath(os.path.join(ROOT, '..', '..', 'flutter', 'KinCompass', 'assets', 'translations', 'en.json'))
APP_STORE = 'https://apps.apple.com/app/id6791076115'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

AUTHOR = {
    "@type": "Person",
    "@id": f"{BASE}/#tsimafei-lemeshchanka",
    "name": "Tsimafei Lemeshchanka",
    "url": "https://github.com/Another1dd",
    "jobTitle": "Developer",
    "sameAs": ["https://github.com/Another1dd", "https://www.linkedin.com/in/timophei-lemeshchenko/"],
}
PUBLISHER = {"@type": "Organization", "name": "Chepatapa Apps", "url": f"{BASE}/"}
DISCLAIMER = ('Practical communication techniques, not medical advice, and not a substitute for your pediatrician or '
              'therapist. Written by the developer of Kin Compass from published parent-training material and the '
              'app\'s script library; no parenting or clinical experience is claimed.')


def esc(s):
    return html.escape(s, quote=True)


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('«', '').replace('»', '').replace('’', "'")).strip().lower()


def load_pages():
    pages = []
    for f in sorted(glob.glob(os.path.join(HERE, 'content', '*.json'))):
        with open(f, encoding='utf-8') as fh:
            pages.append(json.load(fh))
    return pages


def check_phrases(pages, en_path):
    """Warn when a script phrase on a page is not found in the app's en.json for its source scripts."""
    if not os.path.exists(en_path):
        print(f'warning: {en_path} not found, skipping phrase check', file=sys.stderr)
        return
    with open(en_path, encoding='utf-8') as fh:
        en = json.load(fh)
    for page in pages:
        known = set()
        for sid in page['app_ids']:
            for k, v in en.items():
                if k.startswith(f'playbook.script.{sid}.') and k.endswith('_phrase'):
                    known.add(norm(v))
        extra_steps = [st for sec in page.get('extra_sections', []) for st in sec.get('steps', [])]
        for step in page['steps'] + page.get('variations_steps', []) + extra_steps:
            if norm(step['phrase']) not in known:
                print(f"warning: {page['slug']}: phrase not found in en.json: {step['phrase']!r}", file=sys.stderr)


def steps_html(steps):
    out = []
    for i, s in enumerate(steps, 1):
        out.append(
            f'<div class="step"><h3><span class="n">{i}</span>{esc(s["title"])}</h3>'
            f'<blockquote class="phrase">&ldquo;{esc(s["phrase"])}&rdquo;</blockquote>'
            f'<p class="tip">{esc(s["tip"])}</p></div>')
    return '\n        '.join(out)


def head(title, desc, url, og_image, jsonld_blocks, kicker_type='article'):
    ld = '\n'.join(f'  <script type="application/ld+json">\n  {json.dumps(b, ensure_ascii=False)}\n  </script>\n' for b in jsonld_blocks)
    with open(os.path.join(HERE, 'style.css'), encoding='utf-8') as fh:
        css = fh.read()
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <script>
    (function () {{
      var t = localStorage.getItem('theme');
      if (t) document.documentElement.setAttribute('data-theme', t);
    }})();
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{esc(desc)}">
  <meta name="color-scheme" content="light dark">
  <title>{esc(title)} — Kin Compass</title>
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#FDF6EF" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#1E1815" media="(prefers-color-scheme: dark)">

  <meta property="og:type" content="{kicker_type}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png">
  <link rel="icon" type="image/png" sizes="512x512" href="/assets/favicon-512.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
  <link rel="shortcut icon" href="/assets/favicon.ico">

{ld}
  <link rel="preload" href="/assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>

  <style>
{css}
  </style>
</head>
<body>
  <button class="theme-toggle" id="theme-toggle" aria-label="Toggle dark mode">
    <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
    <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/></svg>
  </button>
'''


FOOT = '''
  <footer>
    &copy; 2026 <a href="/">Chepatapa Apps</a> &middot; built by Tsimafei Lemeshchanka &middot; <a href="/kincompass/">Kin Compass</a> &middot; <a href="/build-log/">Build Log</a>
  </footer>

  <script>
    document.getElementById('theme-toggle').addEventListener('click', function () {
      var isDark = (document.documentElement.getAttribute('data-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark';
      var next = isDark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  </script>
</body>
</html>
'''


def render_page(page, by_slug):
    slug = page['slug']
    url = f'{BASE}/kincompass/scripts/{slug}/'
    og = f'{BASE}/kincompass/scripts/assets/og-{slug}.png'
    article = {
        "@context": "https://schema.org", "@type": "Article", "headline": page['title'], "description": page['meta_description'],
        "url": url, "datePublished": page['published'], "dateModified": page['updated'], "inLanguage": "en", "image": og,
        "author": AUTHOR, "publisher": PUBLISHER,
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Kin Compass", "item": f"{BASE}/kincompass/"},
            {"@type": "ListItem", "position": 3, "name": "Scripts", "item": f"{BASE}/kincompass/scripts/"},
            {"@type": "ListItem", "position": 4, "name": page['title'], "item": url}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in page['faq']]}
    out = head(page['title'], page['meta_description'], url, og, [article, crumbs, faq])

    extra = ''
    for sec in page.get('extra_sections', []):
        body = ''
        if 'dialogue' in sec:
            body += '<div class="dialogue">' + ''.join(
                f'<p><span class="who">{esc(w)}</span>{esc(t)}</p>' for w, t in sec['dialogue']) + '</div>'
            if sec.get('after'):
                body += f'<p>{esc(sec["after"])}</p>'
        if sec.get('steps'):
            body += steps_html(sec['steps'])
        for p in sec.get('paragraphs', []):
            body += f'<p>{esc(p)}</p>'
        extra += f'\n    <section class="card">\n      <h2>{esc(sec["title"])}</h2>\n      {body}\n    </section>\n'

    why = ''.join(f'<p>{esc(p)}</p>' for p in page['why'])
    avoid = ''.join(f'<li>{esc(a)}</li>' for a in page['avoid'])
    sources = ''.join(
        f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a><br><span class="source-note">{esc(s["note"])}</span></li>'
        for s in page['sources'])
    related = ''.join(
        f'<a class="rel" href="/kincompass/scripts/{r}/">{esc(by_slug[r]["title"])}</a>' for r in page['related'] if r in by_slug)
    related += '<a class="rel" href="/kincompass/routine-charts/">Free printable routine charts for preschoolers</a>'
    faq_html = ''.join(f'<details><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for q in page['faq'])

    out += f'''
  <header>
    <a class="back" href="/kincompass/scripts/">&#8592; All scripts</a>
  </header>

  <main>
    <section class="hero">
      <p class="kicker">{page['kicker']}</p>
      <h1>{esc(page['title'])}</h1>
      <p class="dek">{esc(page['summary'])}</p>
    </section>

    <section class="card">
      <h2>The script</h2>
      {steps_html(page['steps'])}
    </section>

    <section class="card">
      <h2>Why it tends to work</h2>
      {why}
    </section>

    <section class="card">
      <h2>{esc(page['variations_title'])}</h2>
      <p>{esc(page['variations_intro'])}</p>
      {steps_html(page['variations_steps'])}
      <p style="margin-top:14px">{page['variations_after']}</p>
    </section>
{extra}
    <section class="card">
      <h2>What to avoid saying</h2>
      <ul class="plain">{avoid}</ul>
    </section>

    <section class="card">
      <h2>Want these scripts in your pocket?</h2>
      <p>
        Kin Compass keeps routines, reminders and scripts like this one on your phone, so you have the
        words ready in the moment. Free to start, no account.
      </p>
      <div class="cta-row">
        <a href="{APP_STORE}"><img src="/kincompass/assets/app-store-badge.svg" alt="Download Kin Compass on the App Store" height="44"></a>
      </div>
    </section>

    <section class="card">
      <h2>Questions</h2>
      {faq_html}
    </section>

    <section class="card related">
      <h2>Related</h2>
      {related}
    </section>

    <section class="card">
      <h2>Sources</h2>
      <ul class="plain">{sources}</ul>
      <p class="disclaimer">{esc(DISCLAIMER)}</p>
    </section>
  </main>
'''
    out += FOOT
    return out


def render_hub(pages):
    url = f'{BASE}/kincompass/scripts/'
    title = 'What to say to a preschooler: scripts for hard moments'
    desc = ('Practical scripts for the moments that go sideways with a preschooler: refusing to get dressed, leaving the park, '
            'tantrums and bedtime. Exact wording, why it tends to work, and sources.')
    coll = {"@context": "https://schema.org", "@type": "CollectionPage", "headline": title, "description": desc, "url": url,
            "inLanguage": "en", "dateModified": max(p['updated'] for p in pages), "author": AUTHOR, "publisher": PUBLISHER,
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i, "url": f"{BASE}/kincompass/scripts/{p['slug']}/", "name": p['title']}
                for i, p in enumerate(pages, 1)]}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Kin Compass", "item": f"{BASE}/kincompass/"},
        {"@type": "ListItem", "position": 3, "name": "Scripts", "item": url}]}
    out = head(title, desc, url, f'{BASE}/kincompass/scripts/assets/og-hub.png', [coll, crumbs], 'website')
    cards = ''.join(
        f'<a class="hub-card" href="/kincompass/scripts/{p["slug"]}/"><strong>{esc(p["title"])}</strong>'
        f'<span>{esc(p["summary"].split(". ")[0])}.</span></a>' for p in pages)
    out += f'''
  <header>
    <a class="back" href="/kincompass/">&#8592; Kin Compass</a>
  </header>

  <main>
    <section class="hero">
      <p class="kicker">Scripts &middot; Kin Compass</p>
      <h1>{esc(title)}</h1>
      <p class="dek">
        Short, practical scripts for the moments that tend to go sideways with a preschooler. Each page gives
        the exact words, why they tend to work, and where the ideas come from. They come from the script library
        in the Kin Compass app.
      </p>
    </section>

    <section class="card">
      <h2>Scripts</h2>
      {cards}
    </section>

    <section class="card">
      <h2>Also free</h2>
      <p>
        Prefer paper? Print one of the
        <a href="/kincompass/routine-charts/">free routine charts</a> for mornings, after daycare, dinner and bedtime.
      </p>
      <p class="disclaimer">{esc(DISCLAIMER)}</p>
    </section>
  </main>
'''
    out += FOOT
    return out


def render_og(slug, title, kicker='Kin Compass &middot; Scripts'):
    font = os.path.join(ROOT, 'assets', 'fonts', 'fraunces-latin.woff2')
    icon = os.path.join(ROOT, 'kincompass', 'assets', 'icon-512.png')
    doc = f'''<html><head><style>
@font-face{{font-family:F;src:url("file://{font}")}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#EDF5F0;position:relative;overflow:hidden;font-family:-apple-system,'Helvetica Neue',sans-serif;color:#2B2B2B}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:14px;background:#4F8A6E}}
.icon{{position:absolute;left:80px;top:80px;width:96px;height:96px;border-radius:22px;box-shadow:0 8px 24px rgba(0,0,0,.15)}}
.k{{position:absolute;left:200px;top:110px;font-size:30px;color:#44765E;font-weight:600;letter-spacing:.02em}}
h1{{position:absolute;left:80px;top:230px;width:1040px;font-family:F,Georgia,serif;font-weight:600;font-size:68px;line-height:1.15}}
.by{{position:absolute;left:80px;bottom:52px;font-size:24px;color:#9E8E84}}
</style></head><body><div class="bar"></div><img class="icon" src="file://{icon}"><div class="k">{kicker}</div>
<h1>{esc(title)}</h1><div class="by">Chepatapa Apps</div></body></html>'''
    tmp = os.path.join('/tmp', f'og-{slug}.html')
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(doc)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--window-size=1200,630', f'--screenshot={os.path.join(OUT, "assets", f"og-{slug}.png")}', f'file://{tmp}'],
                   capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--og', action='store_true', help='also render 1200x630 OG cards with headless Chrome')
    ap.add_argument('--en', default=DEFAULT_EN, help="path to the app's en.json")
    args = ap.parse_args()

    pages = load_pages()
    by_slug = {p['slug']: p for p in pages}
    check_phrases(pages, args.en)

    os.makedirs(OUT, exist_ok=True)
    for p in pages:
        d = os.path.join(OUT, p['slug'])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(render_page(p, by_slug))
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(render_hub(pages))

    if args.og:
        for p in pages:
            render_og(p['slug'], p['title'])
        render_og('hub', 'What to say to a preschooler: scripts for hard moments')
    print(f'rendered {len(pages)} pages + hub into {OUT}')


if __name__ == '__main__':
    main()
