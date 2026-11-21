from build_common import *

def page_schema(key, p, site, canonical, article, asset):
    graph = [{'@type': 'LocalBusiness', '@id': site['domain'] + '/#business', 'name': site['company'], 'url': site['domain'] + '/', 'telephone': site['phone'], 'email': site['email'], 'address': {'@type': 'PostalAddress', 'addressLocality': 'Gastonia', 'addressRegion': 'NC', 'addressCountry': 'US'}}, {'@type': 'WebPage', '@id': canonical, 'name': p['title'], 'url': canonical, 'description': p['description']}]
    if article:
        graph.append({'@type': 'Article', 'headline': p['title'], 'mainEntityOfPage': canonical, 'datePublished': article['published'], 'dateModified': article['last_modified'], 'publisher': {'@id': site['domain'] + '/#business'}})
    page_entity = graph[1]
    page_entity['@id'] = canonical + '#webpage'
    page_entity['isPartOf'] = {'@id': site['domain'] + '/#website'}
    if key == 'index':
        graph.extend([{'@type': 'Organization', '@id': site['domain'] + '/#organization', 'name': site['company'], 'url': site['domain'] + '/'}, {'@type': 'WebSite', '@id': site['domain'] + '/#website', 'url': site['domain'] + '/', 'name': site['name'], 'publisher': {'@id': site['domain'] + '/#business'}}])
    service_keys = {'services', 'aircraft-records-review', 'light-sport-prebuy-evaluation', 'light-sport-experimental-avionics', 's-lsa-e-lsa-maintenance', 'e-props-dealer-support'}
    if key in service_keys or (key.startswith('rotax-') and (not key.endswith('-notice'))):
        graph.append({'@type': 'Service', '@id': canonical + '#service', 'name': p.get('heading', p['title']), 'description': p['description'], 'url': canonical, 'provider': {'@id': site['domain'] + '/#business'}})
    if key not in ['index', '404', 'card', 'thank-you']:
        graph.append({'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': site['domain'] + '/'}, {'@type': 'ListItem', 'position': 2, 'name': p['title'], 'item': canonical}]})
    if key == 'faq':
        graph.append({'@type': 'FAQPage', '@id': canonical + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q['heading'], 'acceptedAnswer': {'@type': 'Answer', 'text': site['workflow'] if q['text'] == '@workflow' else q['text']}} for q in p['sections']]})
    if key == 'joseph-helminiak-bio':
        page_entity['@type'] = 'ProfilePage'
        page_entity['mainEntity'] = {'@id': site['domain'] + '/#joseph-helminiak'}
        graph.append({'@type': 'Person', '@id': site['domain'] + '/#joseph-helminiak', 'name': 'Joseph Helminiak', 'worksFor': {'@id': site['domain'] + '/#business'}, 'url': canonical})
    if article:
        graph[2]['author'] = {'@id': site['domain'] + '/#business'}
        graph[2]['image'] = site['domain'] + asset('assets/images/rotax-engine-installed-green-covers-800.webp')
    data = {'@context': 'https://schema.org', '@graph': graph}
    return data
