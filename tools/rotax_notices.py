"""ROTAX technical updates, rendered from the selected editorial records."""
from datetime import date
from urllib.parse import urlsplit
import re
from build_common import E, safe_link

IRMT = 'https://rotaxirmt.com/irmt-place/7534'
LIBRARY = 'https://rotax.my.salesforce-sites.com/DocumentsSearch'
CTA = '<a class="button" href="/support-request?topic=notice">Request Applicability Review</a>'
SEVERITIES = ('safety','routine','optional')
OFFICIAL = {'rotax.my.salesforce-sites.com','www.flyrotax.com','www.govinfo.gov','www.federalregister.gov'}

def featured(records):
    selected = [r for r in records if r['prominence']=='featured']
    if any(r['severity'] not in SEVERITIES for r in selected):
        raise ValueError('Unknown notice severity')
    return sorted(selected,key=lambda r:(SEVERITIES.index(r['severity']),-date.fromisoformat(r['issue_date']).toordinal()))

def validate(records, asof):
    selected = featured([r for r in records if r['state']=='published'])
    if len(selected)!=2 or len({r['subject'].casefold().strip() for r in selected})!=2:
        raise ValueError('R1 requires two distinct featured subjects')
    for r in records:
        ad = r['faa_ad']
        if r['status']=='ad_in_effect' and (not ad or r['prominence'] not in {'safety','featured'}):
            raise ValueError('R2 active AD hidden in archive')
        if r['rotax_category'] not in {'optional','mandatory','obligatory','recommended'} or (
            (r['severity']=='safety') != bool(ad or r['rotax_category']=='mandatory')):
            raise ValueError('R3 inconsistent safety classification')
        verified=date.fromisoformat(r['source_verified'])
        if not verified <= asof <= date.fromisoformat(r['next_review']) or r['source_verified']!=r['last_review']:
            raise ValueError('R4 source verification is stale or inconsistent')
        if not r['documents'] or not r['engine_families'] or not r['subject'].strip():
            raise ValueError('Missing notice identification')
        for d in r['documents']:
            u=urlsplit(d['url'])
            if u.scheme!='https' or u.hostname not in OFFICIAL or u.username or u.password:
                raise ValueError('R5 unofficial bulletin URL')
            if d['variant'] not in {'certified','astm'} or not all(d.get(k) for k in ('number','revision','issue_date','library_file','engines')):
                raise ValueError('Incomplete bulletin reference')
        supersedes=r.get('supersedes','')
        if supersedes and not any(re.fullmatch(re.escape(d['number'])+r'(?:R\d+| initial issue)?',supersedes,re.I) for d in r['documents']):
            raise ValueError('R7 unrelated supersession')

def date_label(value):
    d=date.fromisoformat(value)
    return f'{d.day} {d:%B %Y}'

def doc_link(d):
    return f'<a href="{safe_link(d["url"])}">{E(d["number"])} ({E(d["variant"].upper() if d["variant"]=="astm" else "certified")})</a>'

def cards(records, images):
    parts=['<section class="technical-updates"><h2>Latest ROTAX technical updates</h2>']
    for r in featured([r for r in records if r['state']=='published']):
        ad=r['faa_ad']
        category=r['rotax_category'].title()+' (ROTAX)'
        labels=[*r['engine_families'],category,('FAA AD '+ad['number']+' · certified engines') if ad else 'No FAA AD']
        badges=''.join('<span>'+E(v)+'</span>' for v in labels)
        photo=images.figure(r['photo'],'notice',caption='Oil type is one of the records this bulletin depends on.') if r.get('photo') else ''
        flag='<b class="safety-label">Safety · FAA AD in effect</b>' if ad else ''
        parts.append(f'<article class="update-card" data-featured="{E(r["subject"])}">{photo}<div>{flag}'
                     f'<p class="meta"><time datetime="{r["issue_date"]}">{date_label(r["issue_date"])}</time></p>'
                     f'<h3>{E(r["card_title"])}</h3><div class="update-chips">{badges}</div><p>{E(r["summary"])}</p>'
                     f'<p class="applicability">{E(r["applicability"])}</p><div class="actions">{CTA}'
                     f'<a href="/{E(r["slug"])}">What it means for your engine</a></div><p class="originals">'
                     + ' · '.join(doc_link(d) for d in r['documents'])+'</p></div></article>')
    return ''.join(parts)+'</section>'

def home_module(records,images):
    items=cards(records,images)
    for r in records:
        if r['severity']=='safety' and r['prominence']!='featured':
            ad=r['faa_ad']
            name=('FAA AD '+ad['number']) if ad else r['document']
            items+=f'<p class="safety-label">Also in effect: {E(name)} ({E(r["subject"])}) · <a href="/{E(r["slug"])}">Check applicability</a></p>'
    return items+'<a href="/owner-notices">All ROTAX notices</a>'

def hub(records,images,card):
    active=[r for r in records if r['status']=='ad_in_effect']
    body=cards(records,images)+'<section id="in-effect"><h2>Airworthiness directives in effect</h2><div class="cards">'
    body+=''.join(card(r) for r in active)+'</div></section><section><h2>Reference archive</h2>'
    body+='<div class="table-wrap" tabindex="0" role="region" aria-label="ROTAX bulletin archive"><table><thead><tr>'
    body+=''.join('<th scope="col">'+label+'</th>' for label in ('Document','Rev/issued','Engines','Category','Status','Source checked'))+'</tr></thead><tbody>'
    for r in sorted(records,key=lambda x:x['issue_date'],reverse=True):
        for d in r['documents']:
            ad=r['faa_ad'] if d['variant']=='certified' else None
            status=('AD in effect · FAA AD '+ad['number']+' (certified)') if ad and r['status']=='ad_in_effect' else r['state'].title() if r['state']!='published' else 'Current bulletin'
            body+='<tr><th scope="row">'+doc_link(d)+f'<br><a href="/{E(r["slug"])}">Owner notice</a></th>'
            body+=''.join('<td>'+E(v)+'</td>' for v in (d['revision']+' · '+date_label(d['issue_date']),d['engines'],r['rotax_category'].title(),status,r['source_verified']))+'</tr>'
    return body+'</tbody></table></div><p>This maintained selection covers issues relevant to our services. Search the <a href="'+LIBRARY+'">ROTAX publication library</a> for other bulletins.</p></section>'

def detail(r,meta,review):
    ad=r['faa_ad']; regulatory=''.join('<p>'+E(v)+'</p>' for v in r['body'])
    links=[doc_link(d) for d in r['documents']]
    if ad:
        links.append(f'<a href="{safe_link(ad["url"])}">FAA AD {E(ad["number"])} — official rule</a>')
        links.extend('<a href="'+safe_link(u)+'">Federal Register correction to the effective date</a>' for u in ad['corrections'])
    references='<ul class="source-list">'+''.join('<li>'+link+'</li>' for link in links)+'</ul>'
    facts='<dl class="notice-facts">'+''.join('<dt>'+k+'</dt><dd>'+E(v)+'</dd>' for k,v in [
        ('Issued',date_label(r['issue_date'])),('ROTAX category',r['rotax_category'].title()),('Approval basis',r['approval'])])+'</dl>'
    ranges=''
    if r.get('serial_ranges'):
        ranges='<table><caption>Starting engine serials</caption><thead><tr><th>Model</th><th>Serial number</th></tr></thead><tbody>'+''.join(
            f'<tr><th scope="row">{E(s["engine_type"])}</th><td>from&nbsp;{s["from_sn"]}</td></tr>' for s in r['serial_ranges'])+'</tbody></table>'
    help_text=('We can review records and serial-number applicability and schedule the work where our ROTAX iRMT ratings and your aircraft’s maintenance requirements allow. '
               f'<a href="{IRMT}" rel="noopener">View our ROTAX iRMT listing</a>.')
    sections=[('What changed?', '<p>'+E(r['change'])+'</p>'+facts),
              ('Does it affect my engine?', ranges+'<p>'+E(r['scope'])+'</p>'+regulatory),
              ('What records or identification are needed?', '<p>'+E(r['records_needed'])+'</p>'),
              ('What should I do next?', '<p>'+E(r['next_step'])+'</p>'),
              ('Where can I read the original bulletin?',references+review),
              ('How can Lima Charlie Aero help?', '<p>'+help_text+'</p>'+CTA)]
    return meta+''.join('<section class="'+('notice-help' if i==6 else 'notice-question')+'"><h2>'+E(title)+'</h2>'+body+'</section>' for i,(title,body) in enumerate(sections,1))

def check_surfaces(root, records):
    from lxml import html
    from html import unescape
    from proof_privacy import REGISTRATION, SERIAL
    for path in root.rglob('*'):
        if path.suffix not in {'.html','.json','.xml','.txt','.js','.css','.webmanifest','.vcf'} and path.name not in {'_redirects','_headers'}:
            continue
        text=unescape(path.read_text())
        text=re.sub(r'\\u([a-fA-F0-9]{4})',lambda m:chr(int(m[1],16)),text)
        if '[OWNER' in text:
            raise ValueError('Owner placeholder in '+path.name)
        if REGISTRATION.search(text) or SERIAL.search(text):
            raise ValueError('Private aircraft identifier in '+path.name)
        if path.suffix=='.html':
            doc=html.parse(path)
            for href in doc.xpath('//@href'):
                host=(urlsplit(href).hostname or '').lower().rstrip('.')
                if host=='faa.gov' or host.endswith('.faa.gov'):
                    raise ValueError('FAA website href in '+path.name)
    home=html.parse(root/'index.html')
    if home.xpath('//div[@class="trust"]//a/@href')!=[IRMT]:
        raise ValueError('Trust strip needs exactly the direct iRMT link')
    current=[r for r in records if r['state']=='published']
    subjects=[r['subject'] for r in featured(current)]
    hub_doc=html.parse(root/'owner-notices.html')
    for doc in (home,hub_doc):
        if doc.xpath('//article/@data-featured')!=subjects:
            raise ValueError('R1 featured order or count differs from safety-first selection')
    module=home.xpath('//section[contains(@class,"notice-section")]')[0]
    home_links=module.xpath('.//a/@href')
    hub_links=hub_doc.xpath('//*[@id="in-effect"]//a/@href')
    for r in records:
        if r['severity']=='safety' and r['state']=='published' and '/'+r['slug'] not in home_links:
            raise ValueError('R3 safety notice missing from home')
        if r['status']=='ad_in_effect' and '/'+r['slug'] not in hub_links:
            raise ValueError('R3 active directive missing from hub')
        main=html.parse(root/(r['slug']+'.html')).xpath('string(//main)')
        if re.search(r'\b(?:compliant|airworthy|safe to fly|cleared|eligible)\b', main, re.I):
            raise ValueError('R6 unconditional notice assurance')
