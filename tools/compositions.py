"""Owner journeys, shared service composition, and proof placements."""
from build_common import ROOT, E, safe_link
from cases import STAGES, case_stories
from intake import form

def band(content, style=''):
    return f'<section class="section {style}"><div class="container">{content}</div></section>'

def chips(items):
    return '<ul class="chips">'+''.join(f'<li>{E(i)}</li>' for i in items)+'</ul>'

def links(pairs):
    return '<div class="related">'+''.join(f'<a href="{safe_link(u)}">{E(t)}</a>' for u,t in pairs)+'</div>' if pairs else ''

def details(s, site, ident='', opened=False):
    attrs = f' id="{ident}"' if ident else ''
    if opened: attrs+=' open'
    return f'<details{attrs}><summary>{E(s["heading"])}</summary>{paragraph(s,site)}</details>'

def themed_sections(page, site, used=(), extra=None):
    groups = {title: [] for title in page['themes']}
    for i, section in enumerate(page['sections']):
        if i in used:
            continue
        groups[section['theme']].append(f'<div id="section-{i+1}">{paragraph(section, site)}</div>')
    if extra:
        title, markup = extra
        groups[title].append(markup)
    return ''.join(f'<details><summary>{E(title)}</summary>{"".join(items)}</details>'
                   for title, items in groups.items() if items)

def paragraph(s, site):
    text = site['workflow'] if s['text']=='@workflow' else s['text']
    items = ''.join(f'<li>{E(x)}</li>' for x in s.get('items',[]))
    return '<p>'+E(text)+'</p>'+('<ul>'+items+'</ul>' if items else '')+links(s.get('links',[]))

def step_list(steps):
    return '<ol class="method">'+''.join(f'<li><h3>{E(h)}</h3><p>{E(t)}</p></li>' for h,t in steps)+'</ol>'

def system_map(site):
    return '<div class="system-map">'+(ROOT/'templates/system-map.html').read_text()+'<ol>'+''.join(f'<li>{E(s)}</li>' for s in site['systems'])+'</ol></div>'

def hero(p, key, images, actions):
    crumb=f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {E(p["heading"])}</nav>'
    text=f'{crumb}<p class="eyebrow">KAKH · Gastonia, NC</p><h1>{E(p["heading"])}</h1><p class="lead">{E(p["intro"])}</p>'
    if key not in ['thank-you','404','about-credentials','privacy','image-credits','security-disclosure','support-request','contact']:
        text+=actions(p['topic'])
    if key=='contact':text+=actions(p['topic'])
    photo = images.figure(p['hero_id'],'hero') if p.get('hero_id') else ''
    return f'<section class="interior {("intake-hero" if key=="support-request" else "")}"><div class="container split"><div>{text}</div>{photo}</div></section>'

def home(p,site,img,actions,cases,notices):
    begin,end=p['heading'].split(', ',1)
    first=f'<div class="container hero-copy"><p class="eyebrow">KAKH · Gastonia, North Carolina</p><h1>{E(begin)}, <em>{E(end)}</em></h1><p class="lead">{E(p["intro"])}</p><div class="actions"><a class="button" href="/support-request">Request Service</a><a class="button secondary" href="tel:{site["phone"]}">Call {site["display_phone"]}</a></div></div>'
    result=f'<section class="flight-hero">{img.home_picture(p["hero_id"])}{first}</section>'
    trust = []
    for item in p['trust']:
        title, _, detail = item.partition(': ')
        label = f'<b>{E(title)}</b>{E(detail)}'
        if title == 'ROTAX iRMT':
            label = ('<a href="https://rotaxirmt.com/irmt-place/7534" rel="noopener" '
                     'aria-label="ROTAX iRMT listing for Lima Charlie Aero (opens rotaxirmt.com)">' + label + '</a>')
        trust.append('<li>' + label + '</li>')
    trust = ''.join(trust)
    result+=f'<div class="trust"><ul class="container">{trust}</ul></div>'
    tiles=''
    for tile in p['tiles']:
        picture=img.image(tile['image'],'tile',caption=tile['line'])
        tiles+=f'<a class="tile" href="{tile["destination"]}">{picture}<div><h3>{E(tile["title"])}</h3><p>{E(tile["line"])}</p></div></a>'
    title,intro=p['problem'][:2]
    result+=band(f'<div class="intro"><h2>{E(title)}</h2><p>{E(intro)} <a href="/start-with-the-symptom">Start with the symptom</a></p></div><div class="tiles">{tiles}</div>')
    label,title,body=p['system']
    result+='<section class="system-band">'+img.figure('aircraft-open-cowling-under-canopy-800','band')+f'<div><p class="eyebrow">{E(label)}</p><h2>{E(title)}</h2><p>{E(body)}</p>{chips(site["systems"])}<a href="/the-lima-charlie-aero-standard">How we work →</a></div></section>'
    title,intro=p['stories'] if cases else p['empty_stories']
    work_link='Explore our work' if cases else 'See more of our work'
    stories=case_stories(cases[:2],img.figure,True) if cases else gallery(p['proof'][:4],img)
    result+=band(f'<div class="intro"><h2>{E(title)}</h2><p>{E(intro)}</p></div>{stories}<a href="/our-work">{work_link}</a>','sand')
    result+=band('<h2>'+E(p['method'])+'</h2>'+step_list(p['steps']))
    if notices:result+=band(notices,'notice-section')
    label,title,body=p['founder']
    result+=band('<div class="split">'+img.figure('proof-owner-joe-airfield','founder')+f'<div><p class="eyebrow">{E(label)}</p><h2>{E(title)}</h2><p>{E(body)}</p><a href="/the-lima-charlie-aero-standard">About the shop →</a></div></div>','sand')
    title,line=p['final'];return result+band(f'<h2>{E(title)}</h2><p>{E(line)}</p>'+actions(),'final')

def gallery(items,img):
    return '<div class="proof-grid">'+''.join(img.figure(i['proof_id'],caption=i['caption'],alt=i['alt']) for i in items)+'</div>'

def service_index(tiles,img):
    rows=''
    for url,title,subject,caption in tiles:
        rows+=f'<li><a href="{url}">{img.image(subject,"thumbnail",caption=caption)}<span>{E(title)}</span><span aria-hidden="true">→</span></a></li>'
    return '<ul class="service-index">'+rows+'</ul>'

def related_cases(cases, slugs):
    return links([('/our-work#'+c['slug'],c['title']) for c in cases if c['slug'] in slugs])

def service_page(key,p,pages,site,img,actions,cases,notices,table):
    sections=p['sections'];model=p['service'];result=hero(p,key,img,actions)
    if key=='rotax-engine-systems-support':
        rows=[('/'+k,v['heading'],v['hero_id'],v['intro']) for k,v in pages.items() if k.startswith('rotax-') and k!=key]
        result+=band('<h2>Find your ROTAX concern</h2>'+service_index(rows,img)+notices)
    plan=model['layout']
    used={plan['situation'],plan['systems']}
    situation=sections[plan['situation']];systems=sections[plan['systems']]
    result+=band('<div class="split text-split"><div><h2>Is this you?</h2>'+paragraph(situation,site)+'</div><div><h2>Aircraft &amp; systems involved</h2>'+chips(model['systems'])+paragraph(systems,site)+'</div></div>')
    checklist=plan['checklist']
    if isinstance(checklist,int):
        check_section=sections[checklist]
        used.add(checklist)
        checklist=check_section['items']
        context='<p>'+E(check_section['text'])+'</p>'+links(check_section.get('links',[]))
    else:context=''
    listing='<ul class="checklist">'+''.join('<li>'+E(i)+'</li>' for i in checklist)+'</ul>'
    steps=plan['steps']
    how='Authorization path' if key=='e-props-dealer-support' else 'How we approach it'
    result+=band(f'<div class="split text-split"><div><h2>What to send us</h2>{context}{listing}</div><div><h2>How we approach it</h2>'+('<h3>Authorization path</h3>' if how=='Authorization path' else '')+'<ol class="rail vertical">'+''.join('<li>'+E(step)+'</li>' for step in steps)+'</ol></div></div>','sand')
    proof=p['proof']
    if key=='rotax-gearbox-propeller-vibration':
        pair=[i for i in proof if 'dynavibe-' in i['proof_id'] and ('good-' in i['proof_id'] or 'bad-' in i['proof_id'])]
        result+=band('<h2>Measured, not guessed</h2><div class="pair">'+''.join(img.figure(i['proof_id'],caption=i['caption']) for i in pair)+'</div>')
        proof=[i for i in proof if i not in pair]
    result+=band('<h2>From the work</h2>'+gallery(proof[:4],img))
    used.update(i for i, section in enumerate(sections)
                if section['text'] in ('@workflow', model['limits']))
    extra = (p['themes'][0], gallery(proof[4:],img)) if proof[4:] else None
    result+=band('<h2>Service details</h2>'+table+themed_sections(p,site,used,extra),'sand')
    if key in ['rotax-915-916-turbo-ems-support','rotax-gearbox-propeller-vibration']:result+=band(notices)
    related=related_cases(cases,plan.get('cases',[]))
    return result+band('<aside class="limits"><h2>'+E(model.get('limits_heading','Authorization & limits'))+'</h2><p>'+E(model['limits'])+'</p></aside>'+related+links([('/services','All services'),('/our-work','Our Work')]))+band(actions(p['topic']),'final')

def showcase(key,p,pages,site,img,actions,cases,notices,table):
    if key=='index':return home(p,site,img,actions,cases,notices)
    if 'service' in p:return service_page(key,p,pages,site,img,actions,cases,notices,table)
    result=hero(p,key,img,actions)
    if key=='our-work':
        legend='<ol class="legend">'+''.join(f'<li><b>{name}</b> {text}</li>' for name,text in STAGES.items())+'</ol>'
        limits_title = 'What these cases do and don’t show' if cases else 'What these photographs show'
        return result+band('<h2>How we document the work</h2>'+legend)+band(case_stories(cases,img.figure) if cases else '<h2>Evidence from the work</h2>'+gallery(pages['index']['proof'][:4],img)+links([('/rotax-installation-review','Installation review'),('/rotax-gearbox-propeller-vibration','Vibration measurements')]),'sand')+band('<aside class="limits"><h2>'+limits_title+'</h2><p>'+E(p['limits'])+'</p></aside>'+actions())
    if key=='services':
        rows=[(t['destination'],t['title'],t.get('index_image',t['image']),t['line']) for t in pages['index']['tiles']]
        result+=band('<h2>Aircraft systems and service paths</h2>'+system_map(site))+band('<h2>Choose a starting point</h2>'+service_index(rows,img),'sand')
    if key=='the-lima-charlie-aero-standard':
        result+=band('<h2>One aircraft, ten connected systems</h2>'+system_map(site))
        method=[(s['heading'][3:].capitalize(),s['text']) for s in p['sections'] if s['heading'][:1].isdigit()]
        result+=band('<h2>How we work</h2>'+step_list(method),'sand')
        result+=band('<h2>The paper trail</h2>'+gallery(p['proof'],img))
        result+=band('<div class="split">'+img.figure('proof-owner-joe-airfield','founder')+'<div><h2>'+E(pages['index']['founder'][1])+'</h2><p>'+E(pages['index']['founder'][2])+'</p>'+links([('/joseph-helminiak-bio','Founder background'),('/about-credentials','Training and qualifications'),('/service-area','Service area')])+'</div></div>','sand')
    if key=='support-request':result+=form(site)
    substantive=[]
    if p.get('themes'):
        used = {i for i,s in enumerate(p['sections']) if 'theme' not in s}
        substantive.append(themed_sections(p,site,used))
    for n,s in enumerate([] if p.get('themes') else p['sections']):
        if key=='the-lima-charlie-aero-standard' and s['heading'][:1].isdigit():continue
        ident='credentials' if key=='contact' and n==1 else f'section-{n+1}'
        if key=='faq':
            substantive.append(f'<div id="{ident}">'+details(s,site,f'question-{n+1}')+'</div>')
        elif len(p['sections'])>5:substantive.append(details(s,site,ident))
        else:substantive.append(f'<section id="{ident}"><h2>{E(s["heading"])}</h2>'+paragraph(s,site)+'</section>')
    if substantive:result+=band('<div class="prose">'+''.join(substantive)+'</div>')
    if p.get('proof') and key!='the-lima-charlie-aero-standard':result+=band('<h2>From the work</h2>'+gallery(p['proof'],img),'sand')
    if key in ['services','the-lima-charlie-aero-standard','contact']:result+=band(actions(p['topic']),'final')
    return result
