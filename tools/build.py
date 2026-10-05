"""Build the static site from validated structured content. Python 3.10+, stdlib only."""
from pathlib import Path
from string import Template
from urllib.parse import urlparse
from datetime import date
import json,hashlib,shutil,re,html,argparse
from PIL import Image
import io
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
def digest(d):return hashlib.sha256(d).hexdigest()
def safe_link(url):
 if not (url.startswith('/') and not url.startswith('//') or urlparse(url).scheme in ['https','mailto','tel','sms']):raise ValueError('Unsupported link: '+url)
 return E(url)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='dist');ap.add_argument('--as-of');args=ap.parse_args()
 site=json.loads((ROOT/'content/site.json').read_text(encoding="utf-8"));asof=date.fromisoformat(args.as_of or site['date']);pages=json.loads((ROOT/'content/pages.json').read_text(encoding="utf-8"));records=json.loads((ROOT/'content/updates.json').read_text(encoding="utf-8"));slugs=set();published=[];public=[];warnings=[]
 for r in records:
  for key in ['slug','type','title','owner_question','summary','body','state','published','last_modified','last_review','next_review','reviewer','sources']:
   if key not in r:raise ValueError('Missing '+key)
  if not all(isinstance(r[k],str) and r[k].strip() for k in ['title','owner_question','summary','reviewer']):raise ValueError('Empty required editorial field')
  if not isinstance(r['body'],list) or not r['body'] or not all(isinstance(t,str) and t.strip() for t in r['body']):raise ValueError('Body needs nonempty paragraphs')
  if not isinstance(r['sources'],list):raise ValueError('Sources must be a list')
  if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',r['slug']) or r['slug'] in slugs or r['slug'] in pages:raise ValueError('Invalid or duplicate slug')
  slugs.add(r['slug'])
  if r['type'] not in ['notice','answer','work-note'] or r['state'] not in ['published','draft','superseded','archived']:raise ValueError('Invalid record classification')
  for key in ['published','last_modified','last_review','next_review']:date.fromisoformat(r[key])
  if date.fromisoformat(r['next_review'])<date.fromisoformat(r['last_review']):raise ValueError('Next review predates review')
  if date.fromisoformat(r['last_modified'])<date.fromisoformat(r['published']):raise ValueError('Modification predates publication')
  for u in r['sources']:safe_link(u)
  if r['type']=='notice' and not all(r.get(k) for k in ['document','issue_date','sources']):raise ValueError('Notice needs official document evidence')
  if not r.get('internal') and not r.get('placeholder') and r['state'] in ['published','superseded','archived'] and date.fromisoformat(r['published'])<=asof:
   if date.fromisoformat(r['last_modified'])>asof:raise ValueError('Published content has future modifications')
   if date.fromisoformat(r['last_review'])>asof:raise ValueError('Published content has future review date')
   public.append(r)
   if r['state']=='published':published.append(r)
   if r['state']=='superseded' and not r.get('replaced_by'):raise ValueError('Superseded content requires replacement slug')
   if date.fromisoformat(r['next_review'])<asof:warnings.append({'slug':r['slug'],'next_review':r['next_review'],'action':'Review source; never automatically hide an active notice'})
 for r in public:
  if r.get('replaced_by') and (r['replaced_by']==r['slug'] or r['replaced_by'] not in {i['slug'] for i in public}):raise ValueError('Replacement must have a different, available public URL')
 out=Path(args.output);out=out if out.is_absolute() else ROOT/out
 out=out.resolve()
 if out==ROOT or ROOT not in out.parents or any(part in ['content','templates','assets-src','tools','reference','evidence','node_modules'] for part in out.relative_to(ROOT).parts):raise ValueError('Output must be a disposable build directory inside the project')
 out.mkdir(parents=True,exist_ok=True)
 for f in out.iterdir():shutil.rmtree(f) if f.is_dir() else f.unlink()
 amap={};metadata=json.loads((ROOT/'assets-src/dimensions.json').read_text(encoding="utf-8"))
 for f in sorted((ROOT/'assets-src').rglob('*')):
  if not f.is_file() or f.name=='dimensions.json':continue
  rel=f.relative_to(ROOT/'assets-src').as_posix();d=f.read_bytes()
  if rel in ['favicon.ico','apple-touch-icon.png']:name=rel
  else:name='assets/'+str(Path(rel).with_name(f.stem+'.'+digest(d)[:12]+f.suffix)).replace('\\','/')
  dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(d);amap['assets/'+rel]='/'+name
  if f.suffix=='.webp' and 'images/' in rel:
   with Image.open(io.BytesIO(d)) as im:
    if im.width>400:
     resized=im.copy();resized.thumbnail((400,10000));buf=io.BytesIO();resized.save(buf,'WEBP',quality=82,method=6);bd=buf.getvalue()
     vr=str(Path(rel).with_name(f.stem+'-responsive-400.webp'));vn='assets/'+str(Path(vr).with_name(Path(vr).stem+'.'+digest(bd)[:12]+'.webp'))
     (out/vn).parent.mkdir(parents=True,exist_ok=True);(out/vn).write_bytes(bd);amap['assets/'+vr]='/'+vn

 for f,key in [('site.css','css'),('site.js','js')]:
  d=(ROOT/'templates'/f).read_bytes();name='assets/'+Path(f).stem+'.'+digest(d)[:12]+Path(f).suffix;(out/name).write_bytes(d);amap[key]='/'+name
 def asset(src):return amap[src.split('?')[0]]
 def photo(img,priority=False,hero=False):
  src=img['src'];w,h=metadata[src.removeprefix('assets/')]
  variant=src.rsplit('.',1)[0]+'-responsive-400.webp'
  responsive=(f' srcset="{asset(variant)} 400w, {asset(src)} {w}w" sizes="(max-width:760px) calc(100vw - 32px), 520px"' if variant in amap else '')
  return f'<figure class="{"hero-photo" if hero else "single"}"><img src="{asset(src)}" alt="{E(img["alt"])}"{responsive} width="{w}" height="{h}" {"fetchpriority=high loading=eager" if priority else "loading=lazy decoding=async"}><figcaption>{E(img.get("caption",""))}</figcaption></figure>'
 def actions(topic='unsure'):
  return f'<div class="actions"><a class="button" href="/support-request?topic={E(topic)}">Request Service</a><a class="button secondary" href="tel:{site["phone"]}">Call the Shop</a><a class="button secondary" href="sms:{site["phone"]}">Text the Shop</a></div>'
 def path_route(topic):
  return '/'+{'symptom':'rotax-engine-systems-support','service':'services','prebuy':'light-sport-prebuy-evaluation','equipment':'e-props-dealer-support'}[topic]
 def card(item):
  return f'<article class="card"><p class="tag">{"Owner notice" if item["type"]=="notice" else "Owner answer"}</p><h3><a href="/{E(item["slug"])}">{E(item["title"])}</a></h3><p>{E(item["summary"])}</p><p class="meta">Published <time datetime="{item["published"]}">{item["published"]}</time></p></article>'
 def notices():
  ns=[r for r in published if r['type']=='notice']
  return '<aside class="notice-strip" aria-labelledby="notice-heading"><h2 id="notice-heading">ROTAX owner notices</h2><p>Check the exact engine, component and service history. A family name alone does not establish applicability.</p>'+''.join(f'<p><a href="/{r["slug"]}">{E(r["title"])}</a></p>' for r in ns)+'<a href="/owner-notices">Review source documents and next steps</a></aside>'
 def proof_module(images,title='Evidence from the work',intro=''):
  if not images:return ''
  return '<section class="work-proof"><h2>'+E(title)+'</h2>'+('<p class="section-intro">'+E(intro)+'</p>' if intro else '')+'<div class="proof-grid">'+''.join(photo(i) for i in images)+'</div></section>'
 def sections(p,key):
  result=''
  for i,s in enumerate(p['sections']):
   ident='credentials' if key=='contact' and i==1 else f'section-{i+1}'
   links='<div class="related">'+''.join(f'<a href="{safe_link(u)}">{E(t)}</a>' for u,t in s.get('links',[]))+'</div>' if s.get('links') else ''
   body=f'<p>{E(site["workflow"] if s["text"]=="@workflow" else s["text"])}</p>'+('<ul>'+''.join(f'<li>{E(t)}</li>' for t in s['items'])+'</ul>' if s.get('items') else '')+links
   result+=f'<section id="{ident}"><h2>{E(s["heading"])}</h2>{body}</section>'
   proof=p.get('proof',[])
   if proof:
    placement=1 if key not in ['services','e-props-dealer-support'] else 2
    if i==min(placement,len(p['sections'])-1):result+=proof_module(proof,'Standard in practice' if key=='the-lima-charlie-aero-standard' else 'Documented work and inspection evidence')
  return result
 def form():
  def field(ident,name,label,typ='text',required=False,autocomplete='',placeholder=''):
   return f'<div class="field"><label for="{ident}">{label}</label><input id="{ident}" name="{name}" type="{typ}" {"required" if required else ""} autocomplete="{autocomplete or "off"}" maxlength="180" placeholder="{E(placeholder)}" aria-describedby="{ident}-error"><p class="error" id="{ident}-error"></p></div>'
  opts=[('','Choose a topic (optional)'),('unsure','I’m not sure'),('symptom','Something feels wrong'),('service','Service or inspection planning'),('prebuy','Buying an airplane'),('records','Records review'),('equipment','Propeller or avionics help'),('eprops','Propeller / E-PROPS'),('avionics','Avionics / electrical'),('notice','ROTAX owner notice')]
  return f'''<div class="container intake-layout"><div class="form-card"><p id="topic-prefill" class="source-note" hidden></p><form id="aircraft-intake-form" action="{site['form_action']}" method="POST" accept-charset="UTF-8"><fieldset><legend>Start your inquiry</legend><p class="helper">Required: name, the selected reply method’s contact detail, and your message.</p><div class="field-grid">{field('support-name','name','Name (required)',required=True,autocomplete='name')}<div class="field"><label for="support-method">Preferred reply method</label><select id="support-method" name="preferred_contact" required><option value="email">Email</option><option value="phone">Phone call</option><option value="text">Text message</option></select></div>{field('support-email','email','Email<span id="email-required"></span>','email',autocomplete='email')}{field('support-phone','best_contact','Phone<span id="phone-required"></span>','tel',autocomplete='tel')}<div class="field wide"><label for="support-message">What is happening, or what are you planning? (required)</label><textarea id="support-message" name="message" required maxlength="8000" aria-describedby="support-message-error" placeholder="A brief description is enough. Technical details can follow."></textarea><p class="error" id="support-message-error"></p></div><div class="field"><label for="support-topic">Topic (optional)</label><select name="need_type" id="support-topic">{''.join(f'<option value="{v}">{E(t)}</option>' for v,t in opts)}</select></div><div class="field"><label for="support-urgency">Timing (optional)</label><select name="timeline_urgency" id="support-urgency"><option value="">Select if useful</option><option>Planning ahead</option><option>As soon as practical</option><option>Aircraft is down</option><option>Specific deadline — explain in message</option></select></div></div></fieldset><details class="optional-details"><summary>Aircraft details, if known (optional)</summary><div class="field-grid">{field('support-aircraft','aircraft_model','Aircraft model',placeholder='Unknown is fine')}{field('support-tail','n_number','Tail number (optional)')}{field('support-location','aircraft_location','Airport / location',placeholder='Unknown is fine')}{field('support-engine','engine_model','Engine model',placeholder='Unknown is fine')}</div></details><div class="hp" aria-hidden="true"><label for="support-hp">Leave empty</label><input id="support-hp" name="_gotcha" tabindex="-1" autocomplete="off"></div><input type="hidden" name="_subject" value="Lima Charlie Aero aircraft inquiry"><div id="form-status" class="form-status" role="status" aria-live="polite" tabindex="-1" hidden></div><div class="actions"><button class="button" type="submit">Send inquiry</button></div><p class="helper">This begins an inquiry; an appointment and work scope still need confirmation. Records or photos may be requested afterward. <a href="/privacy">Privacy and form handling</a></p><noscript><p>Include your email for an email reply, or your phone for a call/text reply. The form service handles submission. Call or text if you cannot confirm it was accepted.</p></noscript></form></div><aside class="side-card"><h2>Prefer to talk?</h2><p>You can describe the issue without a diagnosis.</p><a class="button" href="tel:{site['phone']}">Call {site['display_phone']}</a><div class="actions"><a href="sms:{site['phone']}">Text the Shop</a><a href="mailto:{site['email']}">Email the Shop</a></div><p>For time-sensitive concerns, call or text. This form is not a flight-readiness assessment.</p></aside></div>'''
 template=Template((ROOT/'templates/page.html').read_text(encoding="utf-8"));routes=[]
 def render(key,p,body,kind='website',article=None):
  route='/' if key=='index' else '/'+key;canonical=site['domain']+route
  nav=''.join(f'<a href="{u}" '+('aria-current="page" ' if u==route else '')+('class="button" ' if u=='/support-request' else '')+f'>{t}</a>' for u,t in [('/services','Services'),('/rotax-engine-systems-support','ROTAX'),('/e-props-dealer-support','E-PROPS'),('/light-sport-experimental-avionics','Avionics'),('/updates','Owner answers'),('/contact','Contact'),('/support-request','Request Service')])
  graph=[{'@type':'LocalBusiness','@id':site['domain']+'/#business','name':site['company'],'url':site['domain']+'/','telephone':site['phone'],'email':site['email'],'address':{'@type':'PostalAddress','addressLocality':'Gastonia','addressRegion':'NC','addressCountry':'US'}}, {'@type':'WebPage','@id':canonical,'name':p['title'],'url':canonical,'description':p['description']}]
  if article:graph.append({'@type':'Article','headline':p['title'],'mainEntityOfPage':canonical,'datePublished':article['published'],'dateModified':article['last_modified'],'publisher':{'@id':site['domain']+'/#business'}})
  page_entity=graph[1];page_entity['@id']=canonical+'#webpage';page_entity['isPartOf']={'@id':site['domain']+'/#website'}
  if key=='index':
   graph.extend([{'@type':'Organization','@id':site['domain']+'/#organization','name':site['company'],'url':site['domain']+'/'},{'@type':'WebSite','@id':site['domain']+'/#website','url':site['domain']+'/','name':site['name'],'publisher':{'@id':site['domain']+'/#business'}}])
  service_keys={'services','aircraft-records-review','light-sport-prebuy-evaluation','light-sport-experimental-avionics','s-lsa-e-lsa-maintenance','e-props-dealer-support'}
  if key in service_keys or (key.startswith('rotax-') and not key.endswith('-notice')):
   graph.append({'@type':'Service','@id':canonical+'#service','name':p.get('heading',p['title']),'description':p['description'],'url':canonical,'provider':{'@id':site['domain']+'/#business'}})
  if key not in ['index','404','card','thank-you']:
   graph.append({'@type':'BreadcrumbList','@id':canonical+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':site['domain']+'/'},{'@type':'ListItem','position':2,'name':p['title'],'item':canonical}]})
  if key=='faq':
   graph.append({'@type':'FAQPage','@id':canonical+'#faq','mainEntity':[{'@type':'Question','name':q['heading'],'acceptedAnswer':{'@type':'Answer','text':site['workflow'] if q['text']=='@workflow' else q['text']}} for q in p['sections']]})
  if key=='joseph-helminiak-bio':
   page_entity['@type']='ProfilePage';page_entity['mainEntity']={'@id':site['domain']+'/#joseph-helminiak'}
   graph.append({'@type':'Person','@id':site['domain']+'/#joseph-helminiak','name':'Joseph Helminiak','worksFor':{'@id':site['domain']+'/#business'},'url':canonical})
  if article:
   graph[2]['author']={'@id':site['domain']+'/#business'};graph[2]['image']=site['domain']+asset('assets/images/rotax-engine-installed-green-covers-800.webp')
  data={'@context':'https://schema.org','@graph':graph}
  markup=template.substitute(inline_css=(ROOT/'templates/site.css').read_text(),menu_js=(ROOT/'templates/menu.js').read_text(encoding="utf-8"),title=E(p['title']),description=E(p['description']),canonical=E(canonical),robots='<meta name="robots" content="noindex,follow">' if key in ['404','thank-you','card','about-credentials'] else '',ogtype=kind,social=site['domain']+asset('assets/images/rotax-engine-installed-green-covers-800.webp'),css=amap['css'],js=amap['js'],schema=json.dumps(data,ensure_ascii=False).replace('<','\\u003c'),icon=asset('assets/brand/lca-icon-lc-aircraft-v26b-transparent-128.png'),wordmark=asset('assets/brand/lca-wordmark-v17-transparent-640.webp'),nav=nav,main=body,**{k:E(site[k]) for k in ['phone','display_phone','email']})
  banned=['Tell Joe','Contact Joe','Call Joe','Text Joe','Meet Joe','Joe reviews','owner-operated']
  assert not any(x.lower() in markup.lower() for x in banned),'Banned brand phrase in '+key
  (out/(key+'.html')).write_text(markup, encoding="utf-8", newline="\n");routes.append({'route':route,'file':key+'.html','last_modified':p.get('last_modified',site['date']),'indexed':key not in ['404','thank-you','card','about-credentials']})
 for key,p in pages.items():
  for k in ['title','heading','intro','sections','images','last_modified']:assert k in p
  crumbs='' if key in ['index','support-request','card'] else '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>'+E(p['title'])+'</span></nav>'
  hero=f'<section class="hero"><div class="container">{crumbs}<p class="eyebrow">KAKH / Gastonia · Aircraft owner support</p><h1>{E(p["heading"])}</h1><p class="lead">{E(p["intro"])}</p>{actions(p["topic"]) if key not in ["thank-you","404","about-credentials","privacy","image-credits","security-disclosure"] else ""}</div></section>'
  text=sections({**p,'proof':[]} if key=='index' else p,key)
  actual_ids={'main','notice-heading','site-nav',*[f'section-{i+1}' for i in range(len(p['sections']))]}
  if key=='contact':actual_ids.add('credentials')
  # Preserve legacy anchors as explicit aliases, outside any new semantic sections.
  aliases=''.join(f'<span id="{E(i)}" class="legacy-anchor"></span>' for i in dict.fromkeys(p.get('legacy_ids',[])) if i not in actual_ids)
  if key=='index':
   p=dict(p);p['last_modified']=max([p['last_modified']]+[r['last_modified'] for r in published])
   body=f'<section class="hero home"><div class="container hero-grid"><div><p class="eyebrow">KAKH / Gastonia, North Carolina • Serving the Charlotte / Carolinas region by appointment</p><h1>{E(p["heading"])}</h1><p class="hero-credential">ROTAX 9-Series Specialty</p><p class="lead">{E(p["intro"])}</p>{actions()}</div>{photo(p["images"][0],True,True)}</div></section>'
   paths=[('Something feels wrong','Starting, running, warnings, leaks or vibration. Describe the change; no diagnosis required.','symptom'),('Service or an inspection is due','Plan the work, records, estimate and downtime around your aircraft.','service'),('I am buying an airplane','Start with a listing and the decision you need to make. A tail number can follow.','prebuy'),('Propeller or avionics help','Discuss equipment, fitment, an upgrade or an installation concern.','equipment')]
   body+='<section class="section"><div class="container"><h2>Where would you like to start?</h2><p class="section-intro">Choose the closest need, or call the shop and talk it through.</p><div class="cards">'+''.join(f'<article class="card owner-path"><h3>{E(t)}</h3><p>{E(d)}</p><a class="card-link" href="{path_route(topic)}">Explore this service →</a>'+('<div class="related"><a href="/light-sport-experimental-avionics">Avionics details</a><a href="/e-props-dealer-support">E-PROPS details</a></div>' if topic=='equipment' else '')+'</article>' for t,d,topic in paths)+'</div></div></section>'
   body+='<section class="section proof-band"><div class="container">'+proof_module(p.get('proof',[])[:4],'Work, documented','Measurements, observed conditions and installation detail make the work visible. Each example explains what the image can support.')+'</div></section>'
   body+='<section class="section"><div class="container"><div class="prose">'+text+'</div>'+proof_module(p.get('proof',[])[4:],'Aircraft access at the shop')+notices()+'</div></section>'
   latest=sorted(published,key=lambda x:(x['published'],x['slug']),reverse=True)[:3]
   body+='<section class="section alt"><div class="container"><h2>Owner answers and updates</h2><p class="section-intro">Practical questions, planning information and maintained source notices.</p><div class="cards">'+''.join(card(r) for r in latest)+'</div><div class="actions"><a href="/updates">Browse all owner answers and updates</a></div></div></section>'
   body+=f'<section class="section"><div class="container"><h2>A clear next step for your aircraft</h2><p class="section-intro">{E(site["workflow"])}</p>'+actions()+'</div></section>'
  elif key=='support-request':body=f'<section class="form-hero"><div class="container"><h1>{E(p["heading"])}</h1><p>{E(p["intro"])}</p></div></section>'+form()+'<section class="section alt"><div class="container prose">'+text+'</div></section>'
  elif key=='card':body=f'<div class="container"><section class="utility-card"><h1>{E(p["heading"])}</h1><p>{E(p["intro"])}</p><p>ROTAX · Light-sport · E-PROPS · Avionics</p><a class="button" href="{asset("assets/downloads/joseph-helminiak-lima-charlie-aero.vcf")}" download="Joseph-Helminiak-Lima-Charlie-Aero.vcf">Save contact</a>{actions()}<a href="mailto:{site["email"]}">{site["email"]}</a></section></div>'
  elif key=='faq':body=hero+'<section class="section"><div class="container prose faq">'+''.join(f'<details id="question-{i+1}"><summary>{E(s["heading"])}</summary><p>{E(site["workflow"] if s["text"]=="@workflow" else s["text"])}</p></details>' for i,s in enumerate(p['sections']))+'</div></section>'
  else:
   if key in ['rotax-engine-systems-support','rotax-915-916-turbo-ems-support','rotax-gearbox-propeller-vibration']:text=notices()+text
   if key=='light-sport-prebuy-evaluation':text='<div class="table-wrap" tabindex="0" role="region" aria-label="Prebuy review options"><table><caption>Prebuy review options</caption><thead><tr><th scope="col">Review</th><th scope="col">Deliverable</th><th scope="col">Access / timing basis</th></tr></thead><tbody><tr><th scope="row">Courtesy glance</th><td>Initial questions from the available listing/details.</td><td>Limited information; discuss the next review step.</td></tr><tr><th scope="row">Standard evaluation</th><td>Agreed records and condition findings for a buying decision.</td><td>Records, aircraft access and checks determine the estimate and timing.</td></tr><tr><th scope="row">Detailed records and condition audit</th><td>Deeper review of history, gaps and condition evidence.</td><td>Complexity and specialist inputs affect scope and timing.</td></tr></tbody></table></div>'+text
   if key=='aircraft-records-review':text+='<div class="table-wrap" tabindex="0" role="region" aria-label="Illustrative records findings"><table><caption>Illustrative findings format — not a customer report</caption><thead><tr><th scope="col">Question</th><th scope="col">Evidence status</th><th scope="col">Next step</th></tr></thead><tbody><tr><th scope="row">Last relevant inspection</th><td>Example: entry not supplied.</td><td>Request the relevant logbook page; do not assume compliance.</td></tr><tr><th scope="row">Component replacement</th><td>Example: invoice present, installation entry unavailable.</td><td>Clarify installed identity and maintenance record.</td></tr></tbody></table></div>'
   gallery='<div class="proof-grid">'+''.join(photo(i) for i in p['images'])+'</div>' if p['images'] else ''
   body=hero+'<section class="section"><div class="container body-layout"><div class="prose">'+text+gallery+'</div><aside class="side-card"><h2>'+E(p['heading'])+'</h2><p>Send the observations and records relevant to this service.</p>'+actions(p['topic'])+'</aside></div></section>'
  existing_ids=set(re.findall(r'\bid="([^"]+)"',body))
  aliases=''.join(f'<span id="{E(i)}" class="legacy-anchor"></span>' for i in dict.fromkeys(p.get('legacy_ids',[])) if i not in actual_ids and i not in existing_ids)
  # Retired section names fall back to the retained page's introduction, rather
  # than scrolling visitors into its footer. Current field/credential anchors
  # above retain their actual semantic positions.
  render(key,p,aliases+body)
 for r in public:
  p={'title':r['title'],'description':r['summary'],'last_modified':r['last_modified']}
  meta=f'<p class="meta">Published {r["published"]} · Substantive update {r["last_modified"]}'+(f' · Source checked {r["last_review"]}' if r['type']=='notice' else '')+'</p>'
  review=f'<p class="source-note">Review status: source checked {r["last_review"]}; next review {r["next_review"]}. Reviewer: {E(r["reviewer"])}.</p>' if r['type']=='notice' else ''
  state=(f'<p class="notice-strip">This entry is {r["state"]}. '+(f'<a href="/{E(r["replaced_by"])}">Read the replacement notice</a>.' if r.get('replaced_by') else 'It is retained for reference; check current source documents.')+'</p>' if r['state']!='published' else '')
  doc=(f'<p><strong>Manufacturer reference:</strong> {E(r["document"])} · Issue {r["issue_date"]}</p><p class="meta">Supersedes {E(r.get("supersedes",""))}. Source documents were checked; this is not an aircraft compliance determination. Check the manufacturer portal for later revisions.</p>'+review if r['type']=='notice' else '')
  sources='<h2>Official source documents</h2><ul class="source-list">'+''.join(f'<li><a href="{safe_link(u)}">{("Manufacturer document: "+E(r.get("document",""))) if i==0 else ("ROTAX technical documentation portal" if "technical-documentation" in u else "FAA AD 2026-16-11 — official rule" if "govinfo.gov" in u else "EASA AD 2026-0170 — official record" if "ad.easa.europa.eu" in u else urlparse(u).netloc)}</a></li>' for i,u in enumerate(r['sources']))+'</ul>' if r['sources'] else ''
  body='<section class="hero"><div class="container"><p class="eyebrow">'+('Owner notice' if r['type']=='notice' else 'Owner answer')+'</p><h1>'+E(r['title'])+'</h1><p class="lead">'+E(r['summary'])+'</p></div></section><section class="section"><div class="container prose">'+state+meta+doc+''.join('<p>'+E(t)+'</p>' for t in r['body'])+sources+actions(r.get('topic','unsure'))+'<a href="/updates">All owner answers and updates</a></div></section>'
  render(r['slug'],p,body,'article',r)
 for key,title,summary,items in [('updates','Owner answers and updates','Useful owner questions, service planning and source-backed notices.',published),('owner-notices','ROTAX owner notices','Maintain the exact source, revision and applicability review for your aircraft.',[r for r in published if r['type']=='notice'])]:
  hub_sections=json.loads((ROOT/'content/hubs.json').read_text()).get(key,[])
  hub_content=''.join('<section><h2>'+E(h['heading'])+'</h2><p>'+E(h['text'])+'</p></section>' for h in hub_sections)
  body=f'<section class="hero"><div class="container"><h1>{title}</h1><p class="lead">{summary}</p></div></section><section class="section"><div class="container"><div class="cards">'+''.join(card(r) for r in items)+'</div><div class="prose">'+hub_content+'</div><p class="source-note">This is a maintained selection of notices relevant to the services described here, not a complete bulletin database or a determination of your aircraft’s status.</p>'+actions('notice' if key=='owner-notices' else 'unsure')+'</div></section>'
  render(key,{'title':title,'description':summary,'last_modified':max([site['date']]+[r['last_modified'] for r in items])},body)
 redirect='/e-props-usa-dealer-support /e-props-dealer-support 301\n/e-props-usa-dealer-support.html /e-props-dealer-support 301\n/rotax-912-rubber-replacement /rotax-rubber-hose-replacement-fluid-leaks 301\n/rotax-912-rubber-replacement.html /rotax-rubber-hose-replacement-fluid-leaks 301\n/prebuy /light-sport-prebuy-evaluation 301\n/prebuy.html /light-sport-prebuy-evaluation 301\n'
 redirect+='/e-props-usa-dealer-support/ /e-props-dealer-support 301\n/rotax-912-rubber-replacement/ /rotax-rubber-hose-replacement-fluid-leaks 301\n/prebuy/ /light-sport-prebuy-evaluation 301\n'
 redirect+='/_headers /__missing-config-resource 302\n/_redirects /__missing-config-resource 302\n'
 (out/'_redirects').write_text(redirect, encoding="utf-8", newline="\n")
 headers='/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: geolocation=(), microphone=(), camera=()\n  X-Frame-Options: SAMEORIGIN\n\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n\n/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n\n/site.webmanifest\n  Cache-Control: public, max-age=0, must-revalidate\n\n/favicon.ico\n  Cache-Control: public, max-age=0, must-revalidate\n\n/apple-touch-icon.png\n  Cache-Control: public, max-age=0, must-revalidate\n\n'+asset('assets/downloads/joseph-helminiak-lima-charlie-aero.vcf')+'\n  Content-Type: text/vcard; charset=utf-8\n  Content-Disposition: attachment; filename="Joseph-Helminiak-Lima-Charlie-Aero.vcf"\n'
 headers+='\nhttps://limacharlieaero.com/*\n  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n  Content-Security-Policy: upgrade-insecure-requests\n'
 (out/'_headers').write_text(headers, encoding="utf-8", newline="\n")
 manifest={'name':site['company'],'short_name':'LCAero','start_url':'/','display':'standalone','background_color':'#092a44','theme_color':'#092a44','icons':[{'src':asset(f'assets/brand/lca-icon-lc-aircraft-v26b-transparent-{sz}.png'),'sizes':f'{sz}x{sz}','type':'image/png'} for sz in [192,512]]}
 (out/'site.webmanifest').write_text(json.dumps(manifest,indent=2), encoding="utf-8", newline="\n")
 (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+site['domain']+'/sitemap.xml\n', encoding="utf-8", newline="\n")
 xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+E(site['domain']+r['route'])+'</loc><lastmod>'+r['last_modified']+'</lastmod></url>' for r in routes if r['indexed'])+'</urlset>\n';(out/'sitemap.xml').write_text(xml, encoding="utf-8", newline="\n")
 for f in ['security.txt','.well-known/security.txt']:
  dest=out/f;dest.parent.mkdir(exist_ok=True);dest.write_text(f'Contact: mailto:{site["email"]}\nExpires: 2027-04-04T00:00:00Z\nCanonical: {site["domain"]}/.well-known/security.txt\nPolicy: {site["domain"]}/security-disclosure\nPreferred-Languages: en\n', encoding="utf-8", newline="\n")
 evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
 (evidence/'asset-map.json').write_text(json.dumps(amap,indent=2), encoding="utf-8", newline="\n");(evidence/'routes.json').write_text(json.dumps(routes,indent=2), encoding="utf-8", newline="\n");(evidence/'review-warnings.json').write_text(json.dumps(warnings,indent=2), encoding="utf-8", newline="\n")
 files={f.relative_to(out).as_posix():digest(f.read_bytes()) for f in sorted(out.rglob('*')) if f.is_file()};(evidence/'deployment-manifest.json').write_text(json.dumps(files,indent=2), encoding="utf-8", newline="\n")
 print(json.dumps({'output':str(out),'release':site['release'],'html_pages':len(routes),'files':len(files),'bytes':sum(f.stat().st_size for f in out.rglob('*') if f.is_file()),'review_warnings':warnings}))
if __name__=='__main__':main()
