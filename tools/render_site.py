from build_common import *
from intake import form
from metadata import page_schema

def render_site(out, site, pages, public, published, amap, metadata):

    def asset(src):
        return amap[src.split('?')[0]]

    def photo(img, priority=False, hero=False):
        src = img['src']
        w, h = metadata[src.removeprefix('assets/')]
        variant = src.rsplit('.', 1)[0] + '-responsive-400.webp'
        responsive = f' srcset="{asset(variant)} 400w, {asset(src)} {w}w" sizes="(max-width:760px) calc(100vw - 32px), 520px"' if variant in amap else ''
        return f'''<figure class="{('hero-photo' if hero else 'single')}"><img src="{asset(src)}" alt="{E(img['alt'])}"{responsive} width="{w}" height="{h}" {('fetchpriority=high loading=eager' if priority else 'loading=lazy decoding=async')}><figcaption>{E(img.get('caption', ''))}</figcaption></figure>'''

    def actions(topic='unsure'):
        return f"""<div class="actions"><a class="button" href="/support-request?topic={E(topic)}">Request Service</a><a class="button secondary" href="tel:{site['phone']}">Call the Shop</a><a class="button secondary" href="sms:{site['phone']}">Text the Shop</a></div>"""

    def path_route(topic):
        return '/' + {'symptom': 'rotax-engine-systems-support', 'service': 'services', 'prebuy': 'light-sport-prebuy-evaluation', 'equipment': 'e-props-dealer-support'}[topic]

    def card(item):
        return f'''<article class="card"><p class="tag">{('Owner notice' if item['type'] == 'notice' else 'Owner answer')}</p><h3><a href="/{E(item['slug'])}">{E(item['title'])}</a></h3><p>{E(item['summary'])}</p><p class="meta">Published <time datetime="{item['published']}">{item['published']}</time></p></article>'''

    def notices():
        ns = [r for r in published if r['type'] == 'notice']
        return '<aside class="notice-strip" aria-labelledby="notice-heading"><h2 id="notice-heading">ROTAX owner notices</h2><p>Check the exact engine, component and service history. A family name alone does not establish applicability.</p>' + ''.join((f"""<p><a href="/{r['slug']}">{E(r['title'])}</a></p>""" for r in ns)) + '<a href="/owner-notices">Review source documents and next steps</a></aside>'

    def proof_module(images, title='Evidence from the work', intro=''):
        if not images:
            return ''
        return '<section class="work-proof"><h2>' + E(title) + '</h2>' + ('<p class="section-intro">' + E(intro) + '</p>' if intro else '') + '<div class="proof-grid">' + ''.join((photo(i) for i in images)) + '</div></section>'

    def sections(p, key):
        result = ''
        for i, s in enumerate(p['sections']):
            ident = 'credentials' if key == 'contact' and i == 1 else f'section-{i + 1}'
            links = '<div class="related">' + ''.join((f'<a href="{safe_link(u)}">{E(t)}</a>' for u, t in s.get('links', []))) + '</div>' if s.get('links') else ''
            body = f"<p>{E(site['workflow'] if s['text'] == '@workflow' else s['text'])}</p>" + ('<ul>' + ''.join((f'<li>{E(t)}</li>' for t in s['items'])) + '</ul>' if s.get('items') else '') + links
            result += f'''<section id="{ident}"><h2>{E(s['heading'])}</h2>{body}</section>'''
            proof = p.get('proof', [])
            if proof:
                placement = 1 if key not in ['services', 'e-props-dealer-support'] else 2
                if i == min(placement, len(p['sections']) - 1):
                    result += proof_module(proof, 'Standard in practice' if key == 'the-lima-charlie-aero-standard' else 'Documented work and inspection evidence')
        return result
    template = Template((ROOT / 'templates/page.html').read_text(encoding='utf-8'))
    routes = []

    def render(key, p, body, kind='website', article=None):
        route = '/' if key == 'index' else '/' + key
        canonical = site['domain'] + route
        nav = ''.join((f'<a href="{u}" ' + ('aria-current="page" ' if u == route else '') + ('class="button" ' if u == '/support-request' else '') + f'>{t}</a>' for u, t in [('/services', 'Services'), ('/rotax-engine-systems-support', 'ROTAX'), ('/e-props-dealer-support', 'E-PROPS'), ('/light-sport-experimental-avionics', 'Avionics'), ('/updates', 'Owner answers'), ('/contact', 'Contact'), ('/support-request', 'Request Service')]))
        data = page_schema(key, p, site, canonical, article, asset)
        markup = template.substitute(inline_css=(ROOT / 'templates/site.css').read_text(), menu_js=(ROOT / 'templates/menu.js').read_text(encoding='utf-8'), title=E(p['title']), description=E(p['description']), canonical=E(canonical), robots='<meta name="robots" content="noindex,follow">' if key in ['404', 'thank-you', 'card', 'about-credentials'] else '', ogtype=kind, social=site['domain'] + asset('assets/images/rotax-engine-installed-green-covers-800.webp'), css=amap['css'], js=amap['js'], schema=json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'), icon=amap['header-icon'], wordmark=amap['header-wordmark'], nav=nav, main=body, **{k: E(site[k]) for k in ['phone', 'display_phone', 'email']})
        banned = ['Tell Joe', 'Contact Joe', 'Call Joe', 'Text Joe', 'Meet Joe', 'Joe reviews', 'owner-operated']
        assert not any((x.lower() in markup.lower() for x in banned)), 'Banned brand phrase in ' + key
        (out / (key + '.html')).write_text(markup, encoding='utf-8', newline='\n')
        routes.append({'route': route, 'file': key + '.html', 'last_modified': p.get('last_modified', site['date']), 'indexed': key not in ['404', 'thank-you', 'card', 'about-credentials']})
    for key, p in pages.items():
        for k in ['title', 'heading', 'intro', 'sections', 'images', 'last_modified']:
            assert k in p
        crumbs = '' if key in ['index', 'support-request', 'card'] else '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>' + E(p['title']) + '</span></nav>'
        hero = f"""<section class="hero"><div class="container">{crumbs}<p class="eyebrow">KAKH / Gastonia · Aircraft owner support</p><h1>{E(p['heading'])}</h1><p class="lead">{E(p['intro'])}</p>{(actions(p['topic']) if key not in ['thank-you', '404', 'about-credentials', 'privacy', 'image-credits', 'security-disclosure'] else '')}</div></section>"""
        text = sections({**p, 'proof': []} if key == 'index' else p, key)
        actual_ids = {'main', 'notice-heading', 'site-nav', *[f'section-{i + 1}' for i in range(len(p['sections']))]}
        if key == 'contact':
            actual_ids.add('credentials')
        aliases = ''.join((f'<span id="{E(i)}" class="legacy-anchor"></span>' for i in dict.fromkeys(p.get('legacy_ids', [])) if i not in actual_ids))
        if key == 'index':
            p = dict(p)
            p['last_modified'] = max([p['last_modified']] + [r['last_modified'] for r in published])
            body = f"""<section class="hero home"><div class="container hero-grid"><div><p class="eyebrow">KAKH / Gastonia, North Carolina • Serving the Charlotte / Carolinas region by appointment</p><h1>{E(p['heading'])}</h1><p class="hero-credential">ROTAX 9-Series Specialty</p><p class="lead">{E(p['intro'])}</p>{actions()}</div>{photo(p['images'][0], True, True)}</div></section>"""
            paths = [('Something feels wrong', 'Starting, running, warnings, leaks or vibration. Describe the change; no diagnosis required.', 'symptom'), ('Service or an inspection is due', 'Plan the work, records, estimate and downtime around your aircraft.', 'service'), ('I am buying an airplane', 'Start with a listing and the decision you need to make. A tail number can follow.', 'prebuy'), ('Propeller or avionics help', 'Discuss equipment, fitment, an upgrade or an installation concern.', 'equipment')]
            body += '<section class="section"><div class="container"><h2>Where would you like to start?</h2><p class="section-intro">Choose the closest need, or call the shop and talk it through.</p><div class="cards">' + ''.join((f'<article class="card owner-path"><h3>{E(t)}</h3><p>{E(d)}</p><a class="card-link" href="{path_route(topic)}">Explore this service →</a>' + ('<div class="related"><a href="/light-sport-experimental-avionics">Avionics details</a><a href="/e-props-dealer-support">E-PROPS details</a></div>' if topic == 'equipment' else '') + '</article>' for t, d, topic in paths)) + '</div></div></section>'
            body += '<section class="section proof-band"><div class="container">' + proof_module(p.get('proof', [])[:4], 'Work, documented', 'Measurements, observed conditions and installation detail make the work visible. Each example explains what the image can support.') + '</div></section>'
            body += '<section class="section"><div class="container"><div class="prose">' + text + '</div>' + proof_module(p.get('proof', [])[4:], 'Aircraft access at the shop') + notices() + '</div></section>'
            latest = sorted(published, key=lambda x: (x['published'], x['slug']), reverse=True)[:3]
            body += '<section class="section alt"><div class="container"><h2>Owner answers and updates</h2><p class="section-intro">Practical questions, planning information and maintained source notices.</p><div class="cards">' + ''.join((card(r) for r in latest)) + '</div><div class="actions"><a href="/updates">Browse all owner answers and updates</a></div></div></section>'
            body += f"""<section class="section"><div class="container"><h2>A clear next step for your aircraft</h2><p class="section-intro">{E(site['workflow'])}</p>""" + actions() + '</div></section>'
        elif key == 'support-request':
            body = f"""<section class="form-hero"><div class="container"><h1>{E(p['heading'])}</h1><p>{E(p['intro'])}</p></div></section>""" + form(site) + '<section class="section alt"><div class="container prose">' + text + '</div></section>'
        elif key == 'card':
            body = f'''<div class="container"><section class="utility-card"><h1>{E(p['heading'])}</h1><p>{E(p['intro'])}</p><p>ROTAX · Light-sport · E-PROPS · Avionics</p><a class="button" href="{asset('assets/downloads/joseph-helminiak-lima-charlie-aero.vcf')}" download="Joseph-Helminiak-Lima-Charlie-Aero.vcf">Save contact</a>{actions()}<a href="mailto:{site['email']}">{site['email']}</a></section></div>'''
        elif key == 'faq':
            body = hero + '<section class="section"><div class="container prose faq">' + ''.join((f"""<details id="question-{i + 1}"><summary>{E(s['heading'])}</summary><p>{E(site['workflow'] if s['text'] == '@workflow' else s['text'])}</p></details>""" for i, s in enumerate(p['sections']))) + '</div></section>'
        else:
            if key in ['rotax-engine-systems-support', 'rotax-915-916-turbo-ems-support', 'rotax-gearbox-propeller-vibration']:
                text = notices() + text
            if key == 'light-sport-prebuy-evaluation':
                text = '<div class="table-wrap" tabindex="0" role="region" aria-label="Prebuy review options"><table><caption>Prebuy review options</caption><thead><tr><th scope="col">Review</th><th scope="col">Deliverable</th><th scope="col">Access / timing basis</th></tr></thead><tbody><tr><th scope="row">Courtesy glance</th><td>Initial questions from the available listing/details.</td><td>Limited information; discuss the next review step.</td></tr><tr><th scope="row">Standard evaluation</th><td>Agreed records and condition findings for a buying decision.</td><td>Records, aircraft access and checks determine the estimate and timing.</td></tr><tr><th scope="row">Detailed records and condition audit</th><td>Deeper review of history, gaps and condition evidence.</td><td>Complexity and specialist inputs affect scope and timing.</td></tr></tbody></table></div>' + text
            if key == 'aircraft-records-review':
                text += '<div class="table-wrap" tabindex="0" role="region" aria-label="Illustrative records findings"><table><caption>Illustrative findings format — not a customer report</caption><thead><tr><th scope="col">Question</th><th scope="col">Evidence status</th><th scope="col">Next step</th></tr></thead><tbody><tr><th scope="row">Last relevant inspection</th><td>Example: entry not supplied.</td><td>Request the relevant logbook page; do not assume compliance.</td></tr><tr><th scope="row">Component replacement</th><td>Example: invoice present, installation entry unavailable.</td><td>Clarify installed identity and maintenance record.</td></tr></tbody></table></div>'
            gallery = '<div class="proof-grid">' + ''.join((photo(i) for i in p['images'])) + '</div>' if p['images'] else ''
            body = hero + '<section class="section"><div class="container body-layout"><div class="prose">' + text + gallery + '</div><aside class="side-card"><h2>' + 'Request service' + '</h2><p>Send the observations and records relevant to this service.</p>' + actions(p['topic']) + '</aside></div></section>'
        existing_ids = set(re.findall('\\bid="([^"]+)"', body))
        aliases = ''.join((f'<span id="{E(i)}" class="legacy-anchor"></span>' for i in dict.fromkeys(p.get('legacy_ids', [])) if i not in actual_ids and i not in existing_ids))
        render(key, p, aliases + body)
    for r in public:
        p = {'title': r['title'], 'description': r['summary'], 'last_modified': r['last_modified']}
        meta = f"""<p class="meta">Published {r['published']} · Substantive update {r['last_modified']}""" + (f" · Source checked {r['last_review']}" if r['type'] == 'notice' else '') + '</p>'
        review = f"""<p class="source-note">Review status: source checked {r['last_review']}; next review {r['next_review']}. Reviewer: {E(r['reviewer'])}.</p>""" if r['type'] == 'notice' else ''
        state = f"""<p class="notice-strip">This entry is {r['state']}. """ + (f"""<a href="/{E(r['replaced_by'])}">Read the replacement notice</a>.""" if r.get('replaced_by') else 'It is retained for reference; check current source documents.') + '</p>' if r['state'] != 'published' else ''
        doc = f"""<p><strong>Manufacturer reference:</strong> {E(r['document'])} · Issue {r['issue_date']}</p><p class="meta">Supersedes {E(r.get('supersedes', ''))}. Source documents were checked; this is not an aircraft compliance determination. Check the manufacturer portal for later revisions.</p>""" + review if r['type'] == 'notice' else ''
        sources = '<h2>Official source documents</h2><ul class="source-list">' + ''.join((f'''<li><a href="{safe_link(u)}">{('Manufacturer document: ' + E(r.get('document', '')) if i == 0 else 'ROTAX technical documentation portal' if 'technical-documentation' in u else ('FAA AD 2026-22-03 — official rule' if '2026-22307' in u else 'FAA AD 2026-16-11 — official rule') if 'govinfo.gov' in u else 'EASA AD 2026-0170 — official record' if 'ad.easa.europa.eu' in u else urlparse(u).netloc)}</a></li>''' for i, u in enumerate(r['sources']))) + '</ul>' if r['sources'] else ''
        body = '<section class="hero"><div class="container"><p class="eyebrow">' + ('Owner notice' if r['type'] == 'notice' else 'Owner answer') + '</p><h1>' + E(r['title']) + '</h1><p class="lead">' + E(r['summary']) + '</p></div></section><section class="section"><div class="container prose">' + state + meta + doc + ''.join(('<p>' + E(t) + '</p>' for t in r['body'])) + sources + actions(r.get('topic', 'unsure')) + '<a href="/updates">All owner answers and updates</a></div></section>'
        render(r['slug'], p, body, 'article', r)
    for key, title, summary, items in [('updates', 'Owner answers and updates', 'Useful owner questions, service planning and source-backed notices.', published), ('owner-notices', 'ROTAX owner notices', 'Maintain the exact source, revision and applicability review for your aircraft.', [r for r in published if r['type'] == 'notice'])]:
        hub_sections = json.loads((ROOT / 'content/hubs.json').read_text()).get(key, [])
        hub_content = ''.join(('<section><h2>' + E(h['heading']) + '</h2><p>' + E(h['text']) + '</p></section>' for h in hub_sections))
        body = f'<section class="hero"><div class="container"><h1>{title}</h1><p class="lead">{summary}</p></div></section><section class="section"><div class="container"><div class="cards">' + ''.join((card(r) for r in items)) + '</div><div class="prose">' + hub_content + '</div><p class="source-note">This is a maintained selection of notices relevant to the services described here, not a complete bulletin database or a determination of your aircraft’s status.</p>' + actions('notice' if key == 'owner-notices' else 'unsure') + '</div></section>'
        render(key, {'title': title, 'description': summary, 'last_modified': max([site['date']] + [r['last_modified'] for r in items])}, body)
    return routes
