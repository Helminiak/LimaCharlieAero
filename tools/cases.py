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
        if case['state'] not in {'draft', 'published'} or not all(case[k] for k in ('title','sources','status')):
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

def stage_rail(stages):
    dots = []
    for n, stage in enumerate(stages, 1):
        description = E(stage['name'] + ' · ' + stage['status'])
        dots.append(f'<li class="{stage["status"]}" title="{description}">'
                    f'<span aria-hidden="true">{n}</span><span class="visually-hidden">{description}</span></li>')
    return '<ol class="stage-rail" aria-label="Case progress">' + ''.join(dots) + '</ol>'


def case_stories(cases, figure, compact=False):
    blocks = []
    for case in cases:
        slug, stages = case['slug'], case['stages']
        tag = 'h3' if compact else 'h2'
        heading = f'<{tag}>{E(case["title"])}</{tag}>'
        head = ribbon(case) + heading + pill(case)
        rail = stage_rail(stages)
        problem = f'<p>{E(stages[0]["text"])}</p>'
        images = [subject for stage in stages for subject in stage['evidence']]
        if compact:
            # Keep readings and inspection documents uncropped in the full record.
            photos = images[:2] + images[-1:] if len(images) > 2 else images
            mosaic = ''.join(figure(i, 'mosaic') for i in photos)
            if mosaic:
                visual = f'<div class="pics">{mosaic}</div>'
                summary = head + rail
            else:
                visual = f'<div class="case-panel">{pill(case)}{rail}</div>'
                summary = ribbon(case) + heading
            link = f'<a href="/our-work#{slug}">Read the case</a>'
            body = f'<div class="story">{visual}<div>{summary}{problem}{link}</div></div>'
        else:
            strip_ids = images[:2]
            strip = ''.join(figure(i, 'case') for i in strip_ids)
            sections = []
            evidence = []
            for n, stage in enumerate(stages[1:], 1):
                stage_id = f'{slug}-{n}'
                sections.append(f'<section id="{stage_id}"><h3>{stage["name"]} · {stage["status"]}</h3>'
                                f'<p>{E(stage["text"])}</p></section>')
            for stage in stages:
                for subject in stage['evidence']:
                    if subject not in strip_ids:
                        evidence.append(figure(subject, 'case', stage_label=stage['name']))
            limits = ''
            if case.get('limits'):
                limits = f'<aside class="limits"><b>What this does and does not show</b><p>{E(case["limits"])}</p></aside>'
            body = (f'<div class="case-intro"><div>{head}</div><div>{rail}<h3>Problem</h3>{problem}</div></div>'
                    + f'<div class="case-strip">{strip}</div>'
                    + '<details class="case-record"><summary>Full case record</summary>'
                    + '<div class="case-stages">' + ''.join(sections) + '</div>'
                    + '<div class="case-evidence">' + ''.join(evidence) + '</div>' + limits + '</details>')
        blocks.append(f'<article id="{slug}" class="case-story">{body}</article>')
    return ''.join(blocks)
