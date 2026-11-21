"""Validated case records. The published set is also the boundary for metadata."""
import json
import re
from build_common import ROOT, E

STAGES = {
    'Problem': 'The question that started the work.',
    'Configuration': 'The aircraft, engine and installed equipment.',
    'Evidence': 'The observations and source records available.',
    'Evaluation': 'How the evidence informed the decision.',
    'Action': 'The work performed or submitted.',
    'Verification': 'The checks completed or still pending.',
    'Documentation': 'The record retained for the aircraft.',
}

def select_cases(records, subjects, preview):
    selected, slugs = [], set()
    for case in records:
        slug = case['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in slugs:
            raise ValueError('Invalid or duplicate case slug')
        slugs.add(slug)
        if case['state'] not in {'draft', 'published'} or not all(case[k] for k in ('title','limits','sources','status')):
            raise ValueError('Incomplete case: ' + slug)
        if [s['name'] for s in case['stages']] != list(STAGES):
            raise ValueError('Case needs seven ordered stages: ' + slug)
        for s in case['stages']:
            if not s['text'] or s['status'] not in {'done','pending'} or len(s['evidence']) > 2 or set(s['evidence']) - subjects:
                raise ValueError('Invalid case stage: ' + slug)
        if case['state'] == 'published' and ('[OWNER' in json.dumps(case) or not case.get('owner_confirmation')):
            raise ValueError('Published case needs confirmed facts: ' + slug)
        if preview or case['state'] == 'published':
            selected.append(case)
    return selected

def ribbon(case):
    return '<p class="ribbon">PRIVATE PREVIEW: owner fact-check required</p>' if case['state'] == 'draft' else ''

def pill(case):
    pending = any(s['status']=='pending' for s in case['stages'])
    return f'<span class="pill {"pending" if pending else "done"}">{E(case["status"])}</span>'

def case_stories(cases, figure, compact=False):
    blocks = []
    for case in cases:
        slug = case['slug']
        title = E(case['title'])
        heading = f'<h3>{title}</h3>' if compact else f'<h2>{title}</h2>'
        head = ribbon(case) + heading + pill(case)
        if compact:
            images = [i for s in case['stages'] for i in s['evidence']]
            pics = ''.join(figure(i, 'mosaic') for i in (images[:2]+images[4:5]))
            summary = E(case['stages'][0]['text'])
            body = f'<div class="story"><div class="pics">{pics}</div><div>{head}<p>{summary}</p><a href="/our-work#{slug}">Read the case</a></div></div>' if pics else f'{head}<p>{summary}</p><a href="/our-work#{slug}">Read the case</a>'
        else:
            rail = ''.join(f'<li class="{s["status"]}"><a href="#{slug}-{n}">{s["name"]} · {s["status"]}</a></li>' for n,s in enumerate(case['stages']))
            detail = []
            for n,s in enumerate(case['stages']):
                evidence = ''.join(figure(i,'case') for i in s['evidence'])
                detail.append(f'<section id="{slug}-{n}"><h3>{s["name"]} · {s["status"]}</h3><p>{E(s["text"])}</p><div class="proof-grid">{evidence}</div></section>')
            body = head + '<ol class="rail">'+rail+'</ol>'+''.join(detail)+f'<aside class="limits"><b>What this does and does not show</b><p>{E(case["limits"])}</p></aside>'
        blocks.append(f'<article id="{slug}" class="case-story">{body}</article>')
    return ''.join(blocks)
