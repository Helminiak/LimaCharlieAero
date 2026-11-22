from build_common import *
from compositions import showcase
from image_layouts import Images, home_preloads
from build_assets import SOCIAL
import rotax_notices
from metadata import page_schema

def render_site(out, site, pages, public, published, amap, metadata, registry, cases, preview):

    asset_bytes = {url: (out / url.lstrip('/')).stat().st_size for url in set(amap.values()) if url.endswith('.webp')}

    def asset(src):
        return amap[src.split('?')[0]]

    def actions(topic='unsure'):
        return f"""<div class="actions"><a class="button" href="/support-request?topic={E(topic)}">Request Service</a><a class="button secondary" href="tel:{site['phone']}">Call the Shop</a><a class="button secondary" href="sms:{site['phone']}">Text the Shop</a></div>"""

    def card(item):
        return f'''<article class="card"><p class="tag">{('Owner notice' if item['type'] == 'notice' else 'Owner answer')}</p><h3><a href="/{E(item['slug'])}">{E(item['title'])}</a></h3><p>{E(item['summary'])}</p><p class="meta">Published <time datetime="{item['published']}">{item['published']}</time></p></article>'''

    def notices():
        ns = [r for r in published if r['type'] == 'notice']
        return '<aside class="notice-strip" aria-labelledby="notice-heading"><h2 id="notice-heading">ROTAX owner notices</h2><p>Check the exact engine, component and service history. A family name alone does not establish applicability.</p>' + ''.join((f"""<p><a href="/{r['slug']}">{E(r['title'])}</a></p>""" for r in ns)) + '<a href="/owner-notices">Review source documents and next steps</a></aside>'

    template = Template((ROOT / 'templates/page.html').read_text(encoding='utf-8'))
    routes = []

    def render(key, p, body, kind='website', article=None):
        route = '/' if key == 'index' else '/' + key
        canonical = site['domain'] + route
        nav = ''.join(f'<a href="{item["url"]}"' +
                      (' aria-current="page"' if item['url']==route else '') +
                      (' class="button"' if item['url']=='/support-request' else '') +
                      f'>{E(item["label"])}</a>' for item in site['nav'])
        indexed = not preview and key not in {'404','thank-you','card','about-credentials'}
        robots = 'index,follow,max-image-preview:large' if indexed else 'noindex,follow'
        family = ('propeller' if key=='e-props-dealer-support' else 'rotax' if key.startswith('rotax-')
                  else 'work' if key=='our-work' else 'avionics' if 'avionics' in key
                  else 'records' if 'records' in key or 'prebuy' in key else 'shop')
        social = site['domain']+amap[f'social-{family}.jpg']
        data = page_schema(key,p,site,canonical,article,asset)
        if key=='our-work':
            for case in cases:
                data['@graph'].append({'@type':'CreativeWork','@id':canonical+'#'+case['slug'],
                                       'name':case['title'],'isPartOf':{'@id':canonical+'#webpage'}})
        notice = ''
        if any(r.get('status')=='ad_in_effect' for r in published):
            notice = '<div class="notice-bar"><div class="container">'+E(site['notice_bar'])+' <a href="/owner-notices#in-effect">Check applicability</a></div></div>'
        markup = template.substitute(image_preload=home_preloads(amap) if key=='index' else '', menu_js=(ROOT/'templates/menu.js').read_text(), title=E(p['title']),
                    description=E(p['description']), canonical=E(canonical), robots=robots, ogtype=kind,
                    social=social, social_alt=E(registry[SOCIAL[family]]['alt']), css=amap['css'], js=amap['js'],
                    schema=json.dumps(data,ensure_ascii=False).replace('<',r'\u003c'), wordmark=amap['header-wordmark'],
                    nav=nav, main=body, notice=notice, page_class='home' if key=='index' else 'inside',
                    **{k:E(site[k]) for k in ['phone','display_phone','email']})
        banned = ['Tell Joe', 'Contact Joe', 'Call Joe', 'Text Joe', 'Meet Joe', 'Joe reviews', 'owner-operated']
        assert not any((x.lower() in markup.lower() for x in banned)), 'Banned brand phrase in ' + key
        (out / (key + '.html')).write_text(markup, encoding='utf-8', newline='\n')
        routes.append({'route': route, 'file': key + '.html', 'last_modified': p.get('last_modified', site['date']), 'indexed': indexed})
    selected_notices = [r for r in published if r['type']=='notice']
    for key, p in pages.items():
        if key == 'our-work' and not cases:
            p = {**p, **p['empty']}
        if key == 'card':
            body = f'''<div class="container"><section class="utility-card"><h1>{E(p['heading'])}</h1><p>{E(p['intro'])}</p><p>ROTAX · Light-sport · E-PROPS · Avionics</p><a class="button" href="{asset('assets/downloads/joseph-helminiak-lima-charlie-aero.vcf')}" download="Joseph-Helminiak-Lima-Charlie-Aero.vcf">Save contact</a>{actions()}<a href="mailto:{site['email']}">{site['email']}</a></section></div>'''
        else:
            images = Images(registry,amap,metadata,asset_bytes)
            table = (ROOT/'templates'/(p['topic']+'-table.html')).read_text() if key in {'light-sport-prebuy-evaluation','aircraft-records-review'} else ''
            body = showcase(key,p,pages,site,images,actions,cases,rotax_notices.home_module(selected_notices,images) if key=='index' else notices(),table)
        actual_ids = {'main','site-nav'}
        existing_ids = set(re.findall('\\bid="([^"]+)"', body))
        aliases = ''.join((f'<span id="{E(i)}" class="legacy-anchor"></span>' for i in dict.fromkeys(p.get('legacy_ids', [])) if i not in actual_ids and i not in existing_ids))
        render(key, p, aliases + body)
    for r in public:
        p = {'title': r['title'], 'description': r['summary'], 'last_modified': r['last_modified']}
        meta = f"""<p class="meta">Published {r['published']} · Substantive update {r['last_modified']}""" + (f" · Source checked {r['last_review']}" if r['type'] == 'notice' else '') + '</p>'
        review = f"""<p class="source-note">Review status: source checked {r['last_review']}; next review {r['next_review']}. Reviewer: {E(r['reviewer'])}.</p>""" if r['type'] == 'notice' else ''
        if r.get('source_note'):
            checked = date.fromisoformat(r['last_review'])
            note = r['source_note'].replace('{last_review}', f'{checked:%B} {checked.day}, {checked.year}')
            review = '<p class="source-note">' + E(note) + '</p>'
            if r['reviewer']:
                review += '<p>Reviewer: ' + E(r['reviewer']) + '.</p>'
        state = f"""<p class="notice-strip">This entry is {r['state']}. """ + (f"""<a href="/{E(r['replaced_by'])}">Read the replacement notice</a>.""" if r.get('replaced_by') else 'It is retained for reference; check current source documents.') + '</p>' if r['state'] != 'published' else ''
        doc = f"""<p><strong>Manufacturer reference:</strong> {E(r['document'])} · Issue {r['issue_date']}</p><p class="meta">Supersedes {E(r.get('supersedes', ''))}. Source documents were checked; this is not an aircraft compliance determination. Check the manufacturer portal for later revisions.</p>""" + review if r['type'] == 'notice' else ''
        sources = '<h2>Official source documents</h2><ul class="source-list">' + ''.join((f'''<li><a href="{safe_link(u)}">{('Manufacturer document: ' + E(r.get('document', '')) if i == 0 else 'ROTAX technical documentation portal' if 'technical-documentation' in u else ('FAA AD 2026-22-03 — official rule' if '2026-22307' in u else 'FAA AD 2026-16-11 — official rule') if 'govinfo.gov' in u else 'Federal Register correction to FAA AD 2026-22-03' if '/C1-2026-22307/' in u else 'EASA AD 2026-0170 — official record' if 'ad.easa.europa.eu' in u else urlparse(u).netloc)}</a></li>''' for i, u in enumerate(r['sources']))) + '</ul>' if r['sources'] else ''
        body = '<section class="hero"><div class="container"><p class="eyebrow">' + ('Owner notice' if r['type'] == 'notice' else 'Owner answer') + '</p><h1>' + E(r['title']) + '</h1><p class="lead">' + E(r['summary']) + '</p></div></section><section class="section"><div class="container prose">' + state + meta + doc + ''.join(('<p>' + E(t) + '</p>' for t in r['body'])) + sources + actions(r.get('topic', 'unsure')) + '<a href="/updates">All owner answers and updates</a></div></section>'
        if r.get('change'):
            hero = body.split('</section>',1)[0]+'</section>'
            body = hero+'<section class="section"><div class="container prose">'+state+rotax_notices.detail(r,meta,review)+'<p><a href="/owner-notices">All ROTAX notices</a></p></div></section>'
        render(r['slug'], p, body, 'article', r)
    for key, title, summary, items in [('updates', 'Owner answers and updates', 'Useful owner questions, service planning and source-backed notices.', published), ('owner-notices', 'ROTAX owner notices', 'Maintain the exact source, revision and applicability review for your aircraft.', [r for r in published if r['type'] == 'notice'])]:
        hub_sections = json.loads((ROOT / 'content/hubs.json').read_text()).get(key, [])
        hub_content = ''.join(('<section><h2>' + E(h['heading']) + '</h2><p>' + E(h['text']) + '</p></section>' for h in hub_sections))
        body = f'<section class="hero"><div class="container"><h1>{title}</h1><p class="lead">{summary}</p></div></section><section class="section"><div class="container"><div class="cards">' + ''.join((card(r) for r in items)) + '</div><div class="prose">' + hub_content + '</div><p class="source-note">This is a maintained selection of notices relevant to the services described here, not a complete bulletin database or a determination of your aircraft’s status.</p>' + actions('notice' if key == 'owner-notices' else 'unsure') + '</div></section>'
        if key == 'owner-notices':
            archive_records = [r for r in public if r['type']=='notice']
            hero = body.split('</section>',1)[0]+'</section>'
            body = hero+'<section class="section"><div class="container notice-hub">'+rotax_notices.hub(archive_records,images,card)+'<div class="prose">'+hub_content+'</div></div></section>'
        render(key, {'title': title, 'description': summary, 'last_modified': max([site['date']] + [r['last_modified'] for r in items])}, body)
    return routes
