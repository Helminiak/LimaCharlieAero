from build_common import *

def select_editorial(records, pages, asof):
    slugs = set()
    published = []
    public = []
    warnings = []
    for r in records:
        for key in ['slug', 'type', 'title', 'owner_question', 'summary', 'body', 'state', 'published', 'last_modified', 'last_review', 'next_review', 'reviewer', 'sources']:
            if key not in r:
                raise ValueError('Missing ' + key)
        if not all((isinstance(r[k], str) and r[k].strip() for k in ['title', 'owner_question', 'summary'])) or not (r['reviewer'] or r.get('source_note')):
            raise ValueError('Empty required editorial field')
        if not isinstance(r['body'], list) or not r['body'] or (not all((isinstance(t, str) and t.strip() for t in r['body']))):
            raise ValueError('Body needs nonempty paragraphs')
        if not isinstance(r['sources'], list):
            raise ValueError('Sources must be a list')
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', r['slug']) or r['slug'] in slugs or r['slug'] in pages:
            raise ValueError('Invalid or duplicate slug')
        slugs.add(r['slug'])
        if r['type'] not in ['notice', 'answer', 'work-note'] or r['state'] not in ['published', 'draft', 'superseded', 'archived']:
            raise ValueError('Invalid record classification')
        for key in ['published', 'last_modified', 'last_review', 'next_review']:
            date.fromisoformat(r[key])
        if date.fromisoformat(r['next_review']) < date.fromisoformat(r['last_review']):
            raise ValueError('Next review predates review')
        if date.fromisoformat(r['last_modified']) < date.fromisoformat(r['published']):
            raise ValueError('Modification predates publication')
        for u in r['sources']:
            safe_link(u)
        if r['type'] == 'notice' and (not all((r.get(k) for k in ['document', 'issue_date', 'sources']))):
            raise ValueError('Notice needs official document evidence')
        if not r.get('internal') and (not r.get('placeholder')) and (r['state'] in ['published', 'superseded', 'archived']) and (date.fromisoformat(r['published']) <= asof):
            if date.fromisoformat(r['last_modified']) > asof:
                raise ValueError('Published content has future modifications')
            if date.fromisoformat(r['last_review']) > asof:
                raise ValueError('Published content has future review date')
            public.append(r)
            if r['state'] == 'published':
                published.append(r)
            if r['state'] == 'superseded' and (not r.get('replaced_by')):
                raise ValueError('Superseded content requires replacement slug')
            if date.fromisoformat(r['next_review']) < asof:
                warnings.append({'slug': r['slug'], 'next_review': r['next_review'], 'action': 'Review source; never automatically hide an active notice'})
    for r in public:
        if r.get('replaced_by') and (r['replaced_by'] == r['slug'] or r['replaced_by'] not in {i['slug'] for i in public}):
            raise ValueError('Replacement must have a different, available public URL')
    return (public, published, warnings)
