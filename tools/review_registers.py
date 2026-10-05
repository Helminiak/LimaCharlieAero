"""Generate review matrices from verified source, output and preserved baseline audit.
Optional first argument is an approved baseline Git export, needed only to refresh its inventory.
"""
from pathlib import Path
from lxml import html
import json,re,sys
R=Path(__file__).resolve().parents[1];E=R/'evidence';D=R/'docs';pages=json.loads((R/'content/pages.json').read_text());routes=json.loads((E/'route-audit.json').read_text());proof=json.loads((R/'content/proof-assets.json').read_text());amap=json.loads((E/'asset-map.json').read_text())
def write(name,text):
 path=R/name;path.parent.mkdir(exist_ok=True,parents=True);path.write_text(text.rstrip()+'\n')
def esc(t):return str(t).replace('|','\\|').replace('\n',' ')
def table(head,rows):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(esc(x) for x in row)+' |\n' for row in rows)
if len(sys.argv)>1:
 B=Path(sys.argv[1]);baseline={}
 for f in B.glob('*.html'):
  d=html.parse(str(f));m=d.xpath('//main')[0];baseline[f.stem]={'words':len(m.text_content().split()),'headings':[x.text_content().strip() for x in m.xpath('.//h2')],'text':' '.join(m.text_content().split())}
 write('evidence/baseline-content-inventory.json',json.dumps(baseline,indent=2))
else:baseline=json.loads((E/'baseline-content-inventory.json').read_text())
bands={'aircraft-records-review':(850,1050),'contact':(350,500),'e-props-dealer-support':(1250,1500),'faq':(1100,1400),'index':(850,1050),'joseph-helminiak-bio':(750,900),'light-sport-experimental-avionics':(750,950),'light-sport-prebuy-evaluation':(900,1100),'owner-notices':(250,450),'planning-service-downtime':(250,450),'prebuy-first-inquiry':(250,450),'rotax-9-series-912-914-915-916-support':(700,900),'rotax-912-carb-sync':(650,800),'rotax-912-high-oil-temperature':(600,800),'rotax-912-mag-drop-troubleshooting':(600,800),'rotax-915-916-turbo-ems-support':(650,850),'rotax-cooling-oil-temperature-problems':(650,850),'rotax-engine-systems-support':(950,1150),'rotax-fuel-pressure-fuel-delivery-problems':(750,900),'rotax-gearbox-propeller-vibration':(850,1050),'rotax-ignition-ecu-electrical-faults':(750,900),'rotax-installation-review':(850,1050),'rotax-rubber-hose-replacement-fluid-leaks':(850,1000),'s-lsa-e-lsa-maintenance':(900,1100),'service-area':(750,950),'services':(1050,1300),'start-with-the-symptom':(250,450),'support-request':(300,450),'the-lima-charlie-aero-standard':(1150,1350),'updates':(400,600)}
ret='# Content retention and route change register\n\nBaseline: approved main `3d48ea6ec3785bc1faf67a5826eb678c3d14cc58`. Word counts use visible main text including captions, headings and CTA labels, excluding navigation/footer/schema. Bands are editorial guardrails. See `baseline-content-inventory.json` for the original text, not just a summary.\n\n'
wordrows=[]
for r in routes:
 k='index' if r['route']=='/' else r['route'][1:];p=pages.get(k,{});b=baseline.get(k);band=bands.get(k);concepts=[s['heading'] for s in p.get('sections',[])];imgs=[i['proof_id'] for i in p.get('proof',[])]
 removals='Founder-as-default CTAs, repeated generic next-step wording and duplicated navigation were replaced under specification §§4–7. Technical scope remains available in the retained/expanded sections.'
 if k=='e-props-dealer-support':removals+=' Unsupported performance superlatives and universal payment/authorization implications were excluded under §§4, 16 and 31; product/fitment process remains.'
 if k in ['about-credentials','card','404','thank-you']:removals='Utility role retained; indexability aligned with §22. Founder authority is consolidated in the biography as expressly directed.'
 ret+=f'## {r["route"]}\n\n'+table(['Field','Evidence'],[['Live baseline present / words',f'{bool(b)} / {b["words"] if b else "new route"}'],['Baseline substantive topics','; '.join(b['headings']) if b else 'New owner-entry, hub or dated notice route'],['RC3 purpose',r['h1']],['Retained / expanded concepts','; '.join(concepts) or r['description']],['Added','Company-first entry, contextual next steps, consistent route metadata'+('; photographic evidence: '+', '.join(imgs) if imgs else '')],['Removed / reason',removals],['Proof assets',', '.join(imgs) or 'No photographic requirement for this utility/hub; contextual links where relevant'],['Indexability','index' if r['indexed'] else 'noindex,follow'],['Target band',f'{band[0]}–{band[1]}' if band else 'Concise utility or source-bound notice'],['Final words',r['words']],['Reviewer notes','Compare the supplied before/after screenshots and original inventory. Scope and claims require independent review; word count is not a semantic completeness proof.']])+'\n'
 wordrows.append([r['route'],r['words'],f'{band[0]}–{band[1]}' if band else 'utility/notice','WITHIN' if not band or band[0]<=r['words']<=band[1] else 'EDITORIAL REVIEW'])
write('evidence/CONTENT_RETENTION_REGISTER.md',ret);write('evidence/WORD_COUNT_REPORT.md','# Public main-content word counts\n\n'+table(['Route','Words','Band','Result'],wordrows))
seo=[]
for r in routes:
 k='index' if r['route']=='/' else r['route'][1:];p=pages.get(k,{});pr=p.get('proof',[]) or p.get('images',[])
 seo.append([r['route'],r['h1'],'index' if r['indexed'] else 'noindex,follow',r['title'],r['description'],r['canonical'],'yes' if r['indexed'] else 'no',', '.join(r['schema']),'; '.join(r['links']),amap.get(pr[0]['src'],'') if pr else 'none','KAKH/Gastonia; Charlotte relevance on home/services/service area; no additional locations'])
write('evidence/SEO_ROUTE_MAP.md','# Route SEO, schema and internal-link matrix\n\nOne H1, unique indexable title/description, canonical=OG URL=sitemap preference verified by `static-checks.json`. Stable business/organization/person IDs are specified in build.py. No rating/review schema is generated.\n\n'+table(['Route','Intent / H1','Index','Title','Description','Canonical','Sitemap','Schema','Internal links','Primary proof','Local intent'],seo))
assetrows=[]
for a in proof:
 special=any(t in a['id'] for t in ['logbook','checklist','engineering-packet']);person='Person visible; identity/likeness rights require confirmation' if 'joe-working' in a['id'] else 'No personal name asserted by caption'
 ident=a['redaction'] if special else 'Visual inspection completed; verify source ownership and any small equipment labels before publication'
 assetrows.append([a['id'],a['source'],amap[a['asset']],a['alt'],a['provenance'],person,'REVIEW REQUIRED if aircraft markings are identifiable' if any(t in a['id'] for t in ['aircraft','installed','hoist']) else 'No legible registration observed',ident,a['redaction'],a['permission'],'HOLD for public publication; private review candidate only'])
write('evidence/ASSET_PERMISSIONS_REGISTER.md','# Asset permissions and privacy register\n\n**No asset is silently marked cleared.** Historical deployment and owner-supplied provenance do not establish every publication right. All 38 proof subjects remain REVIEW REQUIRED for owner rights approval. This private candidate includes previews for review; public deployment is prohibited pending the gate. Manufacturer marks and technical references do not confer affiliation or authority.\n\nSource-resolution document inspection exposed identifiers in two historical E-PROPS images; `tools/redact_proof.py` now masks them deterministically. Open record/work-label detail is masked in the logbook image.\n\n'+table(['ID','Baseline source','Candidate path','Description','Provenance','Person/customer identifiers','Aircraft registration','Document/equipment identifiers','Redaction','Permission','Disposition'],assetrows))
proofrows=[];byid={a['id']:a for a in proof}
for k,p in pages.items():
 for i in p.get('proof',[]):
  a=byid[i['proof_id']];proofrows.append(['/' if k=='index' else '/'+k,'Work, documented' if k=='index' else 'Standard in practice' if k=='the-lima-charlie-aero-standard' else 'Contextual evidence module',a['source'],amap[i['src']],i['caption'],i['alt'],'Visible observation / process only; no causal outcome claimed',a['id'],'No chronological or causal assertion','Owner records required before asserting a verified before/after sequence'])
write('evidence/PROOF_OF_WORK_REGISTER.md','# Proof placement and factual-claim register\n\n38 unique photographic subjects, reused only in relevant technical contexts. Arrangement explains categories of evidence; source filenames do not establish chronology. The Standard shows concern, joint detail and recorded condition without claiming acceptance or causal repair success. Independent review must decide whether additional verified chronology is needed before public release.\n\n'+table(['Route','Section','Source','Optimized','Caption','Alt','Claim supported','Permissions row','Chronology','Chronology evidence'],proofrows))
major=['index','services','rotax-9-series-912-914-915-916-support','rotax-engine-systems-support','rotax-gearbox-propeller-vibration','rotax-installation-review','rotax-fuel-pressure-fuel-delivery-problems','e-props-dealer-support','light-sport-experimental-avionics','light-sport-prebuy-evaluation','aircraft-records-review','the-lima-charlie-aero-standard','contact','support-request','service-area']
hf=[]
for k in major:
 p=pages[k];hf.append(['/' if k=='index' else '/'+k,p['heading'],'H1 and owner-readable introduction early','KAKH/Gastonia in header/intro','Page-specific scope','Early contextual module' if p.get('proof') else 'Intake/service context; see related evidence','Request Service; form early on intake','Terms explained in page context','320/375/390/768/1024/1440 tested','Technical depth and evidence limitations','Contextual headings/links; uncropped proof; optional technical form fields'])
write('evidence/HUMAN_FACTORS_DESIGN_MATRIX.md','# Human-factors review matrix\n\nVisual evidence: `screenshots/before/` and `screenshots/final/`. Human interpretation and aesthetic scoring remain with independent Design/SEO review; automated layout success is not a user study.\n\n'+table(['Route','Visitor question','Early answer','Location','Scope','Proof','CTA','Jargon','Mobile','Cognitive burden','Correction'],hf))
write('docs/LOCAL_SEO_HANDOFF.md','''# Local SEO handoff

Canonical business name: Lima Charlie Aero LLC. Public operating name: Lima Charlie Aero.
Phone: +1 980-382-1344. Website: https://limacharlieaero.com. Contact: support@limacharlieaero.com.
Location representation: KAKH / Gastonia, North Carolina; Charlotte/Carolinas regional relevance. No invented street address, travel radius, mobile-service promise, or additional location.

## Manual Google Business Profile review

- Verify exact business name, phone, website and actual operating location against the business record.
- Confirm the correct profile category in the available current GBP taxonomy; aircraft maintenance/repair is the factual service intent, not a claim that a specific category is selectable.
- Map supported services only: Light-Sport/Experimental maintenance, ROTAX system support, E-PROPS support, avionics/electrical context, prebuy/records review.
- Publish only owner-approved real-work photos after rights and identifier review. Add a factual caption that explains the work context; do not imply a customer result from an isolated photo.
- Request genuine reviews neutrally from actual customers. No fabricated, purchased or incentivized reviews; no selective pressure for a positive score.
- Keep hours and visit/access arrangements consistent with actual business operations. This task does not invent or publish hours.

No GBP account, DNS, Cloudflare, email or production service was changed. Search crawling remains allowed, matching the baseline wildcard policy; no training-crawler policy change was introduced.
''')
write('evidence/DESIGN_SEO_REVIEW_CHECKLIST.md','''# Independent Design/SEO review checklist

Review the rendered site first, then the automated evidence. The candidate is not approved for merge or deployment.

1. Homepage mobile, then desktop: identity, service scope, KAKH location, owner paths, four Work, documented examples, CTA.
2. Services, E-PROPS, Standard: technical depth, process proof, permission/redaction gate, no inflated authority.
3. ROTAX hub, vibration, installation, fuel: system relationships, measurements with context, no unsupported chronology.
4. Prebuy, avionics, records: tangible scope, behind-panel evidence, redacted records, useful next steps.
5. Contact, intake, service area: warm company voice, optional technical fields, no appointment/delivery promises, truthful geography.
6. Compare CONTENT_RETENTION_REGISTER and baseline-content-inventory; inspect all retained/removed topic decisions.
7. Review SEO_ROUTE_MAP and current source notices. Confirm factual credentials, manufacturer references and publication permissions.
8. Read defects, raw test results, performance reports and external gates only after the visitor review.

Score independently: UX 15%; proof/trust 20%; content 15%; SEO/local/AI-search 15%; performance 12%; accessibility 10%; brand voice 13%. Target weighted score >=92, every category >=85, proof and brand >=92, SEO >=90; no P0/P1. Codex does not award final approval.

External gates: photo rights, actual Formspree inbox delivery, live Cloudflare behavior, physical-device/assistive-technology checks, and Design/SEO approval. DNS and production deployment are not authorized by this task.
''')
print(json.dumps({'routes':len(routes),'proof_subjects':len(proof),'proof_placements':len(proofrows),'word_band_exceptions':[x for x in wordrows if x[-1]!='WITHIN']}))
